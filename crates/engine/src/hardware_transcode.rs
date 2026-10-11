//! Integrated Windows GPU H.264 export finishing stage.
//!
//! FilmCraft renders and muxes a valid CPU H.264 MP4 first, then *from inside
//! the export job* invokes FFmpeg's vendor-backed h264_amf or h264_qsv encoder.
//! The CPU output stays intact until the GPU MP4 has been decoded and checked.
//! This is application-integrated FFmpeg hardware encoding, NOT a native
//! Media Foundation/AMF/QSV Rust API implementation. FFmpeg + ffprobe must be
//! installed on PATH; drivers and the correct encoder build are required.
//! No Python scripts or command shell are used for application export.

use std::io::Read;
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};
use std::sync::atomic::{AtomicBool, Ordering};
use std::time::Duration;

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum GpuEncoder { AmdAmf, IntelQsv }

impl GpuEncoder {
    pub fn parse(request: Option<&str>) -> Result<Option<Self>, String> {
        match request.unwrap_or("auto") {
            "auto" | "cpu" | "" => Ok(None),
            "amd" => Ok(Some(Self::AmdAmf)),
            "intel" => Ok(Some(Self::IntelQsv)),
            other => Err(format!("unsupported gpuEncoder '{other}' (use auto, cpu, amd or intel)")),
        }
    }
    pub fn ffmpeg_name(self) -> &'static str {
        match self { Self::AmdAmf => "h264_amf", Self::IntelQsv => "h264_qsv" }
    }
}

/// The temporary file must be in the destination directory so final rename
/// stays on the same volume. The caller allocates a unique job id.
pub fn staging_path(target: &Path, job_id: u64, step: &str) -> PathBuf {
    let base = target.file_stem().and_then(|x| x.to_str()).unwrap_or("filmcraft");
    let name = format!(".{base}.filmcraft-rc22-{}-{job_id}-{step}.mp4", std::process::id());
    target.with_file_name(name)
}

struct RemoveOnDrop(PathBuf);
impl Drop for RemoveOnDrop { fn drop(&mut self) { let _ = std::fs::remove_file(&self.0); } }

/// Retain only the tail of FFmpeg's stderr to avoid unbounded log memory.
/// The separate reader thread also prevents a child from deadlocking when
/// stderr fills the OS pipe buffer.
fn read_error_tail(mut stderr: impl Read) -> String {
    const LIMIT: usize = 8192;
    let mut tail = Vec::new();
    let mut block = [0u8; 4096];
    loop {
        match stderr.read(&mut block) {
            Ok(0) | Err(_) => break,
            Ok(n) => {
                tail.extend_from_slice(&block[..n]);
                if tail.len() > LIMIT { tail.drain(..tail.len() - LIMIT); }
            }
        }
    }
    String::from_utf8_lossy(&tail).trim().to_string()
}

/// Run FFmpeg / ffprobe without a shell. stdout can be redirected to a file
/// (used for ffprobe); stderr is consumed concurrently so errors are useful.
/// The wait loop checks Export's Cancel flag, including during verification.
fn checked_command_with_output(
    mut command: Command, cancel: &AtomicBool, what: &str, output: Option<&Path>,
) -> Result<(), String> {
    command.stdin(Stdio::null()).stderr(Stdio::piped());
    if let Some(path) = output {
        let file = std::fs::File::create(path)
            .map_err(|e| format!("cannot create {what} report: {e}"))?;
        command.stdout(Stdio::from(file));
    } else {
        command.stdout(Stdio::null());
    }
    let mut child = command.spawn().map_err(|e| {
        format!("cannot start {what}; check FFmpeg/ffprobe installation and PATH: {e}")
    })?;
    let stderr_reader = child.stderr.take()
        .map(|stderr| std::thread::spawn(move || read_error_tail(stderr)));
    let outcome = loop {
        if cancel.load(Ordering::Relaxed) {
            let _ = child.kill();
            let _ = child.wait();
            break Err("cancelled".to_string());
        }
        match child.try_wait() {
            Ok(Some(code)) if code.success() => break Ok(()),
            Ok(Some(code)) => break Err(format!("{what} exited with {code}")),
            Ok(None) => std::thread::sleep(Duration::from_millis(80)),
            Err(e) => {
                let _ = child.kill();
                let _ = child.wait();
                break Err(format!("{what}: {e}"));
            }
        }
    };
    let diagnostic = stderr_reader.and_then(|h| h.join().ok()).unwrap_or_default();
    outcome.map_err(|err| {
        if err == "cancelled" || diagnostic.is_empty() { err }
        else { format!("{err}: {diagnostic}") }
    })
}

fn checked_command(command: Command, cancel: &AtomicBool, what: &str) -> Result<(), String> {
    checked_command_with_output(command, cancel, what, None)
}

/// Check that the produced file is non-empty, H.264 MP4 and decodes fully.
/// Neither filesize alone nor the encoder exit code establishes a usable file.
fn verify(path: &Path, cancel: &AtomicBool) -> Result<(), String> {
    if std::fs::metadata(path).map(|m| m.len()).unwrap_or(0) < 256 {
        return Err("GPU output is empty or too small".into());
    }
    // Avoid Command::output(): it blocks without checking Cancel. Keep the
    // small probe report on the same disk, and delete it even if an error occurs.
    let probe_path = path.with_extension("ffprobe.txt");
    let _probe_guard = RemoveOnDrop(probe_path.clone());
    let mut probe_cmd = Command::new("ffprobe");
    probe_cmd.args(["-v", "error", "-select_streams", "v:0", "-count_frames",
                    "-show_entries", "stream=codec_name,nb_read_frames", "-of", "default=nw=1:nk=1"])
        .arg(path);
    checked_command_with_output(probe_cmd, cancel, "GPU H.264 ffprobe", Some(&probe_path))?;
    let report = std::fs::read_to_string(&probe_path)
        .map_err(|e| format!("cannot read GPU output ffprobe report: {e}"))?;
    let lines: Vec<_> = report.lines().map(str::trim).collect();
    if !lines.contains(&"h264") ||
        !lines.iter().any(|value| value.parse::<u64>().is_ok_and(|count| count > 0)) {
        return Err("GPU output is not a nonempty H.264 stream".into());
    }
    let mut cmd = Command::new("ffmpeg");
    cmd.args(["-hide_banner", "-nostdin", "-v", "error", "-xerror", "-i"])
        .arg(path).args(["-map", "0:v:0", "-f", "null", "-"]);
    checked_command(cmd, cancel, "GPU output decode verification")
}

/// Adopt an already verified GPU (or fallback CPU) MP4 without destroying
/// recoverable user data. A previous interrupted job may have left a backup:
/// never delete or overwrite it on a subsequent attempt.
fn replace_file(candidate: &Path, dest: &Path, job_id: u64) -> Result<(), String> {
    if candidate == dest {
        return Err("export candidate and destination must differ".into());
    }
    let backup = staging_path(dest, job_id, "old-output");
    // Prior recovery files may be the only remaining copy after a failed
    // restore. An unconditional remove_file(&backup) silently lost that copy.
    if backup.exists() {
        return Err(format!(
            "prior export recovery backup exists at {}; move or recover it before retrying",
            backup.display()
        ));
    }
    let had_old = dest.exists();
    if had_old {
        std::fs::rename(dest, &backup)
            .map_err(|e| format!("cannot back up prior output {}: {e}", dest.display()))?;
    }
    match std::fs::rename(candidate, dest) {
        Ok(()) => {
            if had_old {
                // A failed cleanup must not make the successful export fail;
                // report the retained backup rather than deleting it later.
                if let Err(e) = std::fs::remove_file(&backup) {
                    log::warn!("export succeeded; old backup retained at {}: {e}", backup.display());
                }
            }
            Ok(())
        }
        Err(adopt_error) => {
            if had_old {
                match std::fs::rename(&backup, dest) {
                    Ok(()) => Err(format!(
                        "cannot replace output: {adopt_error}; previous output restored"
                    )),
                    Err(restore_error) => Err(format!(
                        "cannot replace output: {adopt_error}; restoration failed: {restore_error}; \
                         previous output is preserved at {} and must be recovered manually",
                        backup.display()
                    )),
                }
            } else {
                Err(format!("cannot replace output: {adopt_error}"))
            }
        }
    }
}

/// Do hardware encode inside an ordinary FilmCraft export job. Returns true if
/// the GPU passed verification, false if the original CPU result was safely
/// substituted. The caller supplies a completed CPU file in `source`.
pub fn finish(source: &Path, dest: &Path, job_id: u64, gpu: GpuEncoder, cancel: &AtomicBool) -> Result<bool, String> {
    if cancel.load(Ordering::Relaxed) { return Err("cancelled".into()); }
    if source == dest {
        return Err("GPU staging source and destination must be different".into());
    }
    if std::fs::metadata(source).map(|m| m.len()).unwrap_or(0) < 256 {
        return Err("CPU source MP4 is missing or empty; GPU export stopped".into());
    }
    let candidate = staging_path(dest, job_id, "gpu-output");
    let _guard = RemoveOnDrop(candidate.clone());
    let _ = std::fs::remove_file(&candidate);
    let mut cmd = Command::new("ffmpeg");
    cmd.args(["-hide_banner", "-nostdin", "-v", "error", "-y", "-i"])
        .arg(source)
        .args(["-map", "0:v:0", "-map", "0:a?", "-map", "0:s?",
               "-c:v", gpu.ffmpeg_name(), "-pix_fmt", "nv12", "-b:v", "12M",
               "-c:a", "copy", "-c:s", "copy", "-movflags", "+faststart", "-f", "mp4"])
        .arg(&candidate);
    let gpu_result = checked_command(cmd, cancel, gpu.ffmpeg_name())
        .and_then(|_| verify(&candidate, cancel));
    if cancel.load(Ordering::Relaxed) { return Err("cancelled".into()); }
    if let Err(why) = &gpu_result {
        log::warn!("{} GPU H.264 export failed ({why}); using FilmCraft CPU H.264 output", gpu.ffmpeg_name());
    }
    let verified = gpu_result.is_ok();
    replace_file(if verified { &candidate } else { source }, dest, job_id)?;
    if verified { let _ = std::fs::remove_file(source); }
    Ok(verified)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn backend_selection_is_explicit() {
        assert_eq!(GpuEncoder::parse(Some("amd")).unwrap(), Some(GpuEncoder::AmdAmf));
        assert_eq!(GpuEncoder::parse(Some("intel")).unwrap(), Some(GpuEncoder::IntelQsv));
        assert_eq!(GpuEncoder::parse(Some("auto")).unwrap(), None);
        assert!(GpuEncoder::parse(Some("unspecified")).is_err());
    }
    #[test] fn staging_preserves_unicode_and_mp4_extension() {
        let p = staging_path(Path::new(r"C:\작업\영상 쇼츠.mp4"), 42, "gpu-output");
        assert_eq!(p.extension().unwrap(), "mp4");
        assert!(p.to_string_lossy().contains("rc22"));
        assert!(p.to_string_lossy().contains("42"));
    }
    #[test]
    fn errors_keep_only_bounded_stderr_tail() {
        let large = "고장".repeat(10000);
        let tail = read_error_tail(large.as_bytes());
        assert!(tail.len() <= 8192 + 8); // UTF-8 lossy boundary replacement
        assert!(tail.contains("고장"));
    }
    #[test]
    fn replace_file_keeps_existing_output_on_failed_candidate() {
        let parent = std::env::temp_dir().join(format!(
            "filmcraft-rc22-{}-{:?}", std::process::id(), std::thread::current().id()));
        std::fs::create_dir_all(&parent).unwrap();
        let dest = parent.join("영상.mp4");
        std::fs::write(&dest, b"original").unwrap();
        assert!(replace_file(&parent.join("missing.mp4"), &dest, 987654321).is_err());
        assert_eq!(std::fs::read(&dest).unwrap(), b"original");
        let _ = std::fs::remove_file(&dest);
        let _ = std::fs::remove_dir(&parent);
    }
    #[test]
    fn successful_replace_retires_old_output() {
        let parent = std::env::temp_dir().join(format!(
            "filmcraft-rc22-success-{}-{:?}", std::process::id(), std::thread::current().id()));
        std::fs::create_dir_all(&parent).unwrap();
        let dest = parent.join("출력.mp4");
        let candidate = parent.join("candidate.mp4");
        std::fs::write(&dest, b"old").unwrap();
        std::fs::write(&candidate, b"new").unwrap();
        replace_file(&candidate, &dest, 987654322).unwrap();
        assert_eq!(std::fs::read(&dest).unwrap(), b"new");
        assert!(!candidate.exists());
        assert!(!staging_path(&dest, 987654322, "old-output").exists());
        let _ = std::fs::remove_file(&dest);
        let _ = std::fs::remove_dir(&parent);
    }
    #[test]
    fn stale_recovery_backup_is_never_overwritten_or_deleted() {
        let parent = std::env::temp_dir().join(format!(
            "filmcraft-rc22-backup-{}-{:?}", std::process::id(), std::thread::current().id()));
        std::fs::create_dir_all(&parent).unwrap();
        let dest = parent.join("출력.mp4");
        let candidate = parent.join("새파일.mp4");
        let backup = staging_path(&dest, 987654323, "old-output");
        std::fs::write(&dest, b"current").unwrap();
        std::fs::write(&candidate, b"candidate").unwrap();
        std::fs::write(&backup, b"recoverable-original").unwrap();
        let err = replace_file(&candidate, &dest, 987654323).unwrap_err();
        assert!(err.contains("recovery backup"));
        assert_eq!(std::fs::read(&backup).unwrap(), b"recoverable-original");
        assert_eq!(std::fs::read(&dest).unwrap(), b"current");
        assert_eq!(std::fs::read(&candidate).unwrap(), b"candidate");
        let _ = std::fs::remove_dir_all(&parent);
    }
    #[test]
    fn newly_created_output_needs_no_previous_backup() {
        let parent = std::env::temp_dir().join(format!(
            "filmcraft-rc22-new-{}-{:?}", std::process::id(), std::thread::current().id()));
        std::fs::create_dir_all(&parent).unwrap();
        let dest = parent.join("새영상.mp4");
        let candidate = parent.join("encoded.mp4");
        std::fs::write(&candidate, b"new-output").unwrap();
        replace_file(&candidate, &dest, 987654324).unwrap();
        assert_eq!(std::fs::read(&dest).unwrap(), b"new-output");
        assert!(!candidate.exists());
        assert!(!staging_path(&dest, 987654324, "old-output").exists());
        let _ = std::fs::remove_dir_all(&parent);
    }
    #[test]
    fn replacing_file_with_itself_is_rejected() {
        let dest = Path::new("same-video.mp4");
        assert!(replace_file(dest, dest, 987654325).is_err());
    }

}
