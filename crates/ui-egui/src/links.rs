//! Community, project and Korean-patch support links (Help menu, About dialog, header, Home screen).
//!
//! FilmCraft is part of the ArtCraft family: the community lives on the ArtCraft Discord, every
//! app has a page on the ArtCraft website and a public GitHub repository.

/// The app's short name, used in the website and repository URLs.
pub const APP: &str = "filmcraft";

/// The ArtCraft community Discord.
pub const DISCORD: &str = "https://discord.gg/artcraft";
/// The ArtCraft website.
pub const WEBSITE: &str = "https://getartcraft.com";
/// FilmCraft's page on the ArtCraft website.
pub const APP_PAGE: &str = "https://getartcraft.com/apps/filmcraft";
/// FilmCraft's source repository.
pub const GITHUB: &str = "https://github.com/storytold/filmcraft";
/// New issue on FilmCraft's repository.
pub const ISSUES: &str = "https://github.com/storytold/filmcraft/issues";
/// Optional community donation for the unofficial Korean-language patch (not an upstream ArtCraft donation).
pub const KOREAN_PATCH_SUPPORT: &str = "https://ctee.kr/place/caw";

/// (command id, label, url) for every link, in menu order.
pub const ALL: [(&str, &str, &str); 6] = [
    ("help.discord", "Join the ArtCraft Discord…", DISCORD),
    ("help.website", "ArtCraft Website", WEBSITE),
    ("help.appPage", "FilmCraft on getartcraft.com", APP_PAGE),
    ("help.github", "FilmCraft on GitHub", GITHUB),
    ("help.reportIssue", "Report an Issue…", ISSUES),
    ("help.supportKorean", "Support the Korean community patch…", KOREAN_PATCH_SUPPORT),
];

/// The URL a `help.*` link command opens.
pub fn url_for(command: &str) -> Option<&'static str> {
    ALL.iter().find(|(id, _, _)| *id == command).map(|(_, _, u)| *u)
}

/// Ask the operating system to open an HTTPS URL using its registered browser.
///
/// A successful process spawn only means that the request was dispatched. It
/// cannot guarantee that a browser/tab actually opened. Report launch errors
/// to the UI and copy the URL as a manual fallback.
///
/// We do not rely on egui-winit's optional `links` feature for the native app;
/// this project's eframe workspace intentionally disables default features.
pub fn open(ctx: &egui::Context, url: &str) -> Result<(), String> {
    if !url.starts_with("https://") {
        return Err("Refusing a non-HTTPS link".to_owned());
    }
    #[cfg(target_arch = "wasm32")]
    {
        ctx.open_url(egui::OpenUrl::new_tab(url));
        Ok(())
    }
    #[cfg(not(target_arch = "wasm32"))]
    {
        let mut failures = Vec::new();
        for mut command in native_browser_commands(url) {
            // Do not block the GUI while the browser starts, and don't inherit
            // a console window or pipes from the FilmCraft process.
            command.stdout(std::process::Stdio::null()).stderr(std::process::Stdio::null());
            match command.spawn() {
                Ok(_) => return Ok(()),
                Err(e) => failures.push(e.to_string()),
            }
        }
        ctx.copy_text(url.to_owned());
        let reason = if failures.is_empty() {
            "No desktop URL handler configured".to_owned()
        } else {
            failures.join("; ")
        };
        log::warn!("External browser request failed; link copied to clipboard: {reason}");
        Err(reason)
    }
}

/// Native protocol handlers. Windows Explorer is first because it forwards an
/// HTTPS URL through ShellExecute to the registered default browser. The
/// previous url.dll launcher is a fallback for systems that lack Explorer.
/// Arguments are passed without a command shell, so metacharacters in URLs
/// never become commands.
#[cfg(not(target_arch = "wasm32"))]
fn native_browser_commands(url: &str) -> Vec<std::process::Command> {
    let mut commands = Vec::new();
    #[cfg(target_os = "windows")]
    {
        let mut explorer = std::process::Command::new("explorer.exe");
        explorer.arg(url);
        commands.push(explorer);
        let mut fallback = std::process::Command::new("rundll32.exe");
        fallback.arg("url.dll,FileProtocolHandler").arg(url);
        commands.push(fallback);
    }
    #[cfg(target_os = "macos")]
    {
        let mut cmd = std::process::Command::new("open");
        cmd.arg(url);
        commands.push(cmd);
    }
    #[cfg(target_os = "linux")]
    {
        let mut cmd = std::process::Command::new("xdg-open");
        cmd.arg(url);
        commands.push(cmd);
    }
    #[cfg(not(any(target_os = "windows", target_os = "macos", target_os = "linux")))]
    let _ = url;
    commands
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn link_ids_are_stable() {
        assert_eq!(APP_PAGE, format!("{WEBSITE}/apps/{APP}"));
        assert_eq!(GITHUB, format!("https://github.com/storytold/{APP}"));
        assert!(ALL.iter().all(|(id, _, url)| id.starts_with("help.") && url.starts_with("https://")));
        assert_eq!(url_for("help.discord"), Some(DISCORD));
        assert_eq!(url_for("help.supportKorean"), Some("https://ctee.kr/place/caw"));
        assert_eq!(url_for("help.unknown"), None);
    }

    #[test]
    fn non_https_urls_are_rejected() {
        let ctx = egui::Context::default();
        assert!(open(&ctx, "file:///C:/Windows/system.ini").is_err());
        assert!(open(&ctx, "javascript:alert(1)").is_err());
    }

    #[cfg(not(target_arch = "wasm32"))]
    #[test]
    fn url_arguments_are_not_interpolated_through_a_shell() {
        let candidate = format!("{KOREAN_PATCH_SUPPORT}?key=a&foo=b");
        let commands = native_browser_commands(&candidate);
        assert!(!commands.is_empty());
        for cmd in commands {
            let args: Vec<_> = cmd.get_args().map(|v| v.to_string_lossy().into_owned()).collect();
            assert_eq!(args.last().map(String::as_str), Some(candidate.as_str()));
            assert_ne!(cmd.get_program().to_string_lossy(), "cmd.exe");
        }
    }

    #[cfg(target_os = "windows")]
    #[test]
    fn windows_default_browser_has_a_fallback_command() {
        let commands = native_browser_commands(DISCORD);
        assert_eq!(commands.len(), 2);
        assert_eq!(commands[0].get_program(), "explorer.exe");
        assert_eq!(commands[1].get_program(), "rundll32.exe");
    }
}
