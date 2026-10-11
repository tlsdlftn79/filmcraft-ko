# FilmCraft v0.6.0 Stable Korean patch - MSVC build / regression / portable package.
# Run from BUILD.cmd, TEST.cmd or PACKAGE.cmd (Windows PowerShell 5.1+).
[CmdletBinding()]
param([ValidateSet('Build','Test','Package')][string]$Mode = 'Build')
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

function Require-Tool([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Missing $Name in PATH. Install Rust >= 1.95 (https://rustup.rs/) and Visual Studio 2022 C++ Build Tools."
    }
}
function Invoke-Cargo([string[]]$Arguments) {
    Write-Host ('[RUN] cargo ' + ($Arguments -join ' '))
    & cargo @Arguments
    if ($LASTEXITCODE -ne 0) { throw "cargo failed with exit code $LASTEXITCODE" }
}
function Check-Toolchain {
    Require-Tool 'cargo'
    Require-Tool 'rustc'
    $versionText = (& rustc --version)
    if ($LASTEXITCODE -ne 0 -or $versionText -notmatch 'rustc\s+(\d+)\.(\d+)\.(\d+)') {
        throw 'Could not determine the rustc version.'
    }
    $version = [version]::new([int]$Matches[1], [int]$Matches[2], [int]$Matches[3])
    if ($version -lt [version]::new(1,95,0)) {
        throw "Rust 1.95+ required by this project; found $version. Run rustup update stable."
    }
    $info = & rustc -vV
    if ($LASTEXITCODE -ne 0) { throw 'rustc -vV failed.' }
    $hostTriple = ($info | Select-String -Pattern '^host:\s*(.+)' | Select-Object -First 1)
    if (-not $hostTriple -or $hostTriple.Matches[0].Groups[1].Value -notmatch '^x86_64-pc-windows-msvc$') {
        throw "Expected Windows MSVC Rust host. Found: $hostTriple. Install x86_64-pc-windows-msvc via rustup."
    }
    Write-Host ('[OK] ' + $versionText)
    Write-Host ('[OK] Host: ' + $hostTriple.Matches[0].Groups[1].Value)
    $vswhere = Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio\Installer\vswhere.exe'
    if (Test-Path $vswhere) {
        $vs = & $vswhere -latest -version '[17.0,18.0)' -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
        if ($LASTEXITCODE -eq 0 -and $vs) { Write-Host ('[OK] Visual Studio 2022 C++: ' + $vs) }
        else { Write-Warning 'Visual Studio 2022 C++ build tools not detected. Cargo may fail at native dependencies.' }
    } else {
        Write-Warning 'VS discovery tool not found; install Visual Studio 2022 Build Tools with Desktop development with C++ and Windows SDK.'
    }
}

. (Join-Path $PSScriptRoot 'windows-pe.ps1')
. (Join-Path $PSScriptRoot 'stable-build-stamp.ps1')

Push-Location $root
try {
    if (-not (Test-Path 'Cargo.lock')) { throw 'Cargo.lock missing.' }
    if (-not (Test-Path 'crates/ui-egui/src/i18n/ko.tsv')) { throw 'Korean translation catalog is missing.' }
    if (Get-Command py.exe -ErrorAction SilentlyContinue) { & py -3 'scripts/check_stable_release.py' }
    elseif (Get-Command python.exe -ErrorAction SilentlyContinue) { & python 'scripts/check_stable_release.py' }
    else { throw 'Python 3 required for Stable release identity validation.' }
    if ($LASTEXITCODE -ne 0) { throw 'Stable source version/lockfile verification failed.' }
    Check-Toolchain
    if ($env:CARGO_BUILD_TARGET) { throw 'CARGO_BUILD_TARGET is set; unset it to build Windows x64 at target\release.' }
    $targetDir = if ($env:CARGO_TARGET_DIR) {
        if ([IO.Path]::IsPathRooted($env:CARGO_TARGET_DIR)) { $env:CARGO_TARGET_DIR }
        else { Join-Path $root $env:CARGO_TARGET_DIR }
    } else { Join-Path $root 'target' }
    $binary = Join-Path $targetDir 'release\filmcraft.exe'
    $cliBinary = Join-Path $targetDir 'release\filmcraft-cli.exe' 
    switch ($Mode) {
        'Build' {
            $env:FILMCRAFT_REQUIRE_WINRES = '1'
            Invoke-Cargo -Arguments @('build','--locked','--release','-p','filmcraft','-p','filmcraft-cli')
            if (-not (Test-Path $binary)) { throw "Build reported success but filmcraft.exe is missing at $binary" }
            Assert-Win64Pe -Path $binary -Subsystem 2
            Assert-Win64Pe -Path $cliBinary -Subsystem 3
            Write-StableBuildStamp -BinDir (Split-Path $binary -Parent) -RootPath $root
            Write-Host "[OK] Windows x64 GUI: $binary"
            Write-Host "[OK] Windows x64 CLI: $cliBinary"
        }
        'Test' {
            # stdlib-only catalog verification if Python 3 is installed (not needed for the app).
            $py = Get-Command 'py.exe' -ErrorAction SilentlyContinue
            $python = Get-Command 'python.exe' -ErrorAction SilentlyContinue
            if ($py) {
                & py -3 'scripts/check_i18n.py'
                if ($LASTEXITCODE -ne 0) { throw 'Translation static checks failed.' }
                & py -3 'scripts/check_installer.py'
                if ($LASTEXITCODE -ne 0) { throw 'Installer static checks failed.' }
                & py -3 'scripts/test_installer_pe.py'
                if ($LASTEXITCODE -ne 0) { throw 'PE regression tests failed.' }
                & py -3 'scripts/check_korean_input.py'
                if ($LASTEXITCODE -ne 0) { throw 'Korean input checks failed.' }
                & py -3 'scripts/check_korean_stability.py'
                if ($LASTEXITCODE -ne 0) { throw 'Korean Unicode/stability static checks failed.' }
                & py -3 'scripts/check_rc4_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC4 baseline feature checks failed.' }
                & py -3 'scripts/check_rc5_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC5 regression checks failed.' }
                & py -3 'scripts/check_rc6_support.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC6 support link checks failed.' }
                & py -3 'scripts/check_rc7_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC7 focus / GPU static checks failed.' }
                & py -3 'scripts/check_rc8_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC8 GPU probe checks failed.' }
                & py -3 'scripts/check_rc9_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC9 IME / adapter checks failed.' }
                & py -3 'scripts/check_rc10_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC10 Media Foundation hardware encoder discovery checks failed.' }
                & py -3 'scripts/check_rc11_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC22 source regression checks failed.' }
                & py -3 'scripts/check_rc12_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC22 IME diagnostics / GPU smoke regression checks failed.' }
                & py -3 'scripts/probe_h264_gpu.py' '--self-test'
                if ($LASTEXITCODE -ne 0) { throw 'RC22 GPU smoke-test harness unit tests failed.' }
                & py -3 'scripts/verify_shorts_mp4.py' '--self-test'
                if ($LASTEXITCODE -ne 0) { throw 'Shorts stream validation tests failed.' }
                & py -3 'scripts/test_release.py'
                if ($LASTEXITCODE -ne 0) { throw 'Release verifier regression tests failed.' }
            } elseif ($python) {
                & python 'scripts/check_i18n.py'
                if ($LASTEXITCODE -ne 0) { throw 'Translation static checks failed.' }
                & python 'scripts/check_installer.py'
                if ($LASTEXITCODE -ne 0) { throw 'Installer static checks failed.' }
                & python 'scripts/test_installer_pe.py'
                if ($LASTEXITCODE -ne 0) { throw 'PE regression tests failed.' }
                & python 'scripts/check_korean_input.py'
                if ($LASTEXITCODE -ne 0) { throw 'Korean input checks failed.' }
                & python 'scripts/check_korean_stability.py'
                if ($LASTEXITCODE -ne 0) { throw 'Korean stability static checks failed.' }
                & python 'scripts/check_rc4_features.py' 
                if ($LASTEXITCODE -ne 0) { throw 'RC4 baseline feature checks failed.' }
                & python 'scripts/check_rc5_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC5 regression checks failed.' }
                & python 'scripts/check_rc6_support.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC6 support link checks failed.' }
                & python 'scripts/check_rc7_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC7 focus / GPU static checks failed.' }
                & python 'scripts/check_rc8_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC8 GPU probe checks failed.' }
                & python 'scripts/check_rc9_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC9 IME / adapter checks failed.' }
                & python 'scripts/check_rc10_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC10 Media Foundation hardware encoder discovery checks failed.' }
                & python 'scripts/check_rc11_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC22 source regression checks failed.' }
                & python 'scripts/check_rc12_features.py'
                if ($LASTEXITCODE -ne 0) { throw 'RC22 IME diagnostics / GPU smoke regression checks failed.' }
                & python 'scripts/probe_h264_gpu.py' '--self-test'
                if ($LASTEXITCODE -ne 0) { throw 'RC22 GPU smoke-test harness unit tests failed.' }
                & python 'scripts/verify_shorts_mp4.py' '--self-test'
                if ($LASTEXITCODE -ne 0) { throw 'Shorts stream validation tests failed.' }
                & python 'scripts/test_release.py'
                if ($LASTEXITCODE -ne 0) { throw 'Release verifier regression tests failed.' }
            } else {
                throw 'Python 3 is required for the v0.6.0 RC22 localization/release verification tests.'
            }
            if ($py) { & py -3 'scripts/test_stable_release.py' }
            else { & python 'scripts/test_stable_release.py' }
            if ($LASTEXITCODE -ne 0) { throw 'Stable source identity regression tests failed.' }
            # BuildFix1/2 checks are intentionally shared across Python-launcher branches.
            if ($py) {
                & py -3 'scripts/check_mf_h264_buildfix.py'
                if ($LASTEXITCODE -ne 0) { throw 'Media Foundation H.264 / Result API checks failed.' }
                & py -3 'scripts/test_mf_buildfix2.py'
            } else {
                & python 'scripts/check_mf_h264_buildfix.py'
                if ($LASTEXITCODE -ne 0) { throw 'Media Foundation H.264 / Result API checks failed.' }
                & python 'scripts/test_mf_buildfix2.py'
            }
            if ($LASTEXITCODE -ne 0) { throw 'BuildFix2 COM / Windows cargo regression tests failed.' }
            # RC22: text-tool candidate keys must not eat later independent editing keys.
            if ($py) {
                & py -3 'scripts/check_rc13_ime.py'
            } else {
                & python 'scripts/check_rc13_ime.py'
            }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 IME input routing checks failed.' }
            # RC22: external FFmpeg GPU post-export bridge regression tests (no GPU needed).
            # This is NOT the in-process AMF / Quick Sync export factory.
            if ($py) {
                & py -3 'scripts/test_rc14_gpu_transcode.py'
            } else {
                & python 'scripts/test_rc14_gpu_transcode.py'
            }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 GPU transcode regression tests failed.' }
            if ($py) {
                & py -3 'scripts/check_rc14_features.py'
            } else {
                & python 'scripts/check_rc14_features.py'
            }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 release or Unicode navigation checks failed.' }
            # RC22 external browser links & header click hit regions (no browser launched).
            if ($py) {
                & py -3 'scripts/check_rc15_links.py'
            } else {
                & python 'scripts/check_rc15_links.py'
            }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 native links regression checks failed.' }
            # RC22: explicit UI click feedback, native link launcher fallback,
            # IME focus paths and release version checks.
            if ($py) {
                & py -3 'scripts/check_rc16_ui.py'
            } else {
                & python 'scripts/check_rc16_ui.py'
            }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 UI link / Korean input regression checks failed.' }


            # RC22: test-only IME helper must not produce a dead_code warning in library builds.
            if ($py) {
                & py -3 'scripts/check_rc17_ime_dead_code.py'
            } else {
                & python 'scripts/check_rc17_ime_dead_code.py'
            }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 IME dead_code regression checks failed.' }

            # RC22: validate quick-export destinations before launching jobs,
            # preserving Unicode filenames; this test runs without a GPU.
            if ($py) {
                & py -3 'scripts/check_rc18_export.py'
            } else {
                & python 'scripts/check_rc18_export.py'
            }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 quick export path / release verification failed.' }

            # RC22 regression guard for Windows path components and release identity.
            if ($py) {
                & py -3 'scripts/check_rc19_features.py'
            } else {
                & python 'scripts/check_rc19_features.py'
            }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 export/installer validation failed.' }

            # RC22: integrated GPU export bridge / IME warning regression guard.
            if ($py) { & py -3 'scripts/check_rc20_integrated_gpu.py' }
            else { & python 'scripts/check_rc20_integrated_gpu.py' }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 integrated GPU / IME checks failed.' }
            # RC22: cancellable ffprobe, bounded diagnostic capture and CPU fallback guard.
            if ($py) { & py -3 'scripts/check_rc21_gpu_reliability.py' }
            else { & python 'scripts/check_rc21_gpu_reliability.py' }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 GPU export reliability checks failed.' }
            # RC22: ensure a failed final replacement preserves earlier MP4s,
            # stale backups and the staged CPU result for manual recovery.
            if ($py) { & py -3 'scripts/check_rc22_gpu_recovery.py' }
            else { & python 'scripts/check_rc22_gpu_recovery.py' }
            if ($LASTEXITCODE -ne 0) { throw 'RC22 GPU file-recovery safety checks failed.' }



            # Fail fast with platform / UI compiler diagnostics, including Windows-only
            # Media Foundation bindings, before running the much longer Rust test matrix.
            # `cargo check` does not prove hardware or IME runtime correctness.
            Invoke-Cargo -Arguments @('check','--locked','-p','filmcraft-platform')
            Invoke-Cargo -Arguments @('check','--locked','-p','filmcraft-ui-egui')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-ui-egui','rc18_export_path_tests')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-ui-egui','korean_quick_export_rc5_tests')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-ui-egui','korean_')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-ui-egui','korean_rc14_selection_tests')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-text','hangul_')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-captions','korean_')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-render','korean_text_layer_font_and_graphemes_survive_layout')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-engine','hangul_graphics_')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-engine','youtube_shorts_')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-engine','hardware_transcode::tests')
            # Hardware integration test is opt-in: may encode several frames and
            # requires driver/decoder setup on the current Windows machine.
            # Run: set FILMCRAFT_TEST_NVENC=1  &  TEST.cmd
            # Optional external FFmpeg real H.264 GPU smoke test (NOT integrated export).
            # Set FILMCRAFT_TEST_GPU_ENCODERS=1 to exercise available vendor backends;
            # failures are reported without failing the normal test suite.
            if ($env:FILMCRAFT_TEST_GPU_ENCODERS -eq '1') {
                if (Get-Command py -ErrorAction SilentlyContinue) {
                    & py -3 'scripts/probe_h264_gpu.py' '--encoder' 'all'
                } else {
                    & python 'scripts/probe_h264_gpu.py' '--encoder' 'all'
                }
                if ($LASTEXITCODE -ne 0) { Write-Warning 'GPU smoke probe could not run (FFmpeg/ffprobe may be unavailable).' }
            }
            if ($env:FILMCRAFT_TEST_NVENC -eq '1') {
                Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-platform','--test','nvenc_export','--','--test-threads=1')
            }
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-ui-egui','korean_ime_rc9_tests')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-ui-egui','korean_ime_rc11_first_focus_tests')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-platform','gpu_vendor_id_is_not_encoder_availability')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-ui-egui','catalogs_are_well_formed')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-ui-egui','korean_v057_covers_all_reference_ui_keys')
            Invoke-Cargo -Arguments @('test','--locked','-p','filmcraft-engine','interface_language')
            Invoke-Cargo -Arguments @('check','--locked','-p','filmcraft')
            Write-Host '[OK] Focused localization checks and desktop cargo check passed.'
        }
        'Package' {
            # Always rebuild here to avoid packing a stale executable.
            $env:FILMCRAFT_REQUIRE_WINRES = '1'
            Invoke-Cargo -Arguments @('build','--locked','--release','-p','filmcraft','-p','filmcraft-cli')
            Assert-Win64Pe -Path $binary -Subsystem 2
            Assert-Win64Pe -Path $cliBinary -Subsystem 3
            Write-StableBuildStamp -BinDir (Split-Path $binary -Parent) -RootPath $root
            $out = Join-Path $root 'dist'
            if (-not (Test-Path $out)) { New-Item -ItemType Directory -Path $out | Out-Null }
            $zip = Join-Path $out 'FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Portable.zip'
            $stage = Join-Path $env:TEMP ('FilmCraft-Korean-' + [guid]::NewGuid().ToString('N'))
            New-Item -ItemType Directory -Path $stage | Out-Null
            try {
                Copy-Item -LiteralPath $binary -Destination $stage
                Copy-Item -LiteralPath $cliBinary -Destination $stage
                Set-Content -Encoding Ascii -Path (Join-Path $stage 'portable.txt') -Value @(
                    'FilmCraft portable: settings, logs, and recovery data use the data subfolder next to the exe.',
                    'Delete portable.txt to use the normal Windows per-user data directory.'
                )
                foreach ($item in @('README-KOREAN.md','CHANGELOG-KO.md','STABLE_RELEASE_GATE_KO.md','LICENSE-MIT','LICENSE-APACHE')) {
                    Copy-Item (Join-Path $root $item) -Destination $stage
                }
                if (Test-Path $zip) { Remove-Item $zip -Force }
                Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $zip -CompressionLevel Optimal
                if (-not (Test-Path $zip)) { throw 'Archive was not created.' }
                $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $zip).Hash.ToLowerInvariant()
                $checksumFile = "$zip.sha256"
                Set-Content -LiteralPath $checksumFile -Value "$hash  $(Split-Path -Leaf $zip)" -Encoding Ascii
                Write-Host "[OK] Portable release: $zip"
                Write-Host "[SHA256] $hash"
                Write-Host "[CHECKSUM] $checksumFile"
            } finally { Remove-Item $stage -Recurse -Force -ErrorAction SilentlyContinue }
        }
    }
} catch {
    Write-Error ('[FAIL] ' + $_.Exception.Message)
    exit 1
} finally { Pop-Location }
