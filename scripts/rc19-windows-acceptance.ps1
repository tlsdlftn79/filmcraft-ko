# FilmCraft RC22 Windows acceptance gate. No installation, uninstallation or
# changes to user projects. Actual GUI interactions must be tested manually.
[CmdletBinding()]
param(
    [switch]$RunBuild,
    [switch]$Launch,
    [string]$Report = 'build-logs\rc20-acceptance.json'
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
    throw 'RC22 Windows acceptance requires Windows 10/11 x64.'
}
$checks = [ordered]@{}
$checks['Windows_x64'] = [Environment]::Is64BitOperatingSystem
$checks['Rust'] = [bool](Get-Command cargo.exe -ErrorAction SilentlyContinue)
$checks['Python'] = [bool](Get-Command python.exe -ErrorAction SilentlyContinue)
$checks['Installer_compiler'] = [bool](Get-Command ISCC.exe -ErrorAction SilentlyContinue)
$checks['FFprobe'] = [bool](Get-Command ffprobe.exe -ErrorAction SilentlyContinue)
$steps = @()
if ($RunBuild) {
    Push-Location $root
    try {
        foreach ($cmd in @('TEST.cmd', 'BUILD.cmd', 'PACKAGE.cmd', 'INSTALL.cmd', 'VERIFY.cmd')) {
            Write-Host "[RC22] Running $cmd"
            & (Join-Path $root $cmd)
            $code = $LASTEXITCODE
            $steps += [ordered]@{ command = $cmd; exit_code = $code; passed = ($code -eq 0) }
            if ($code -ne 0) { break }
        }
    } finally { Pop-Location }
}
$dist = Join-Path $root 'dist'
$setup = Join-Path $dist 'FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe'
$portable = Join-Path $dist 'FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Portable.zip'
$checks['Installer_EXE_present'] = Test-Path -LiteralPath $setup -PathType Leaf
$checks['Portable_ZIP_present'] = Test-Path -LiteralPath $portable -PathType Leaf
$built = Join-Path $root 'target\release\filmcraft.exe'
$checks['GUI_EXE_present'] = Test-Path -LiteralPath $built -PathType Leaf
if ($Launch) {
    if (-not $checks['GUI_EXE_present']) { throw "Missing $built. Run BUILD.cmd first." }
    Start-Process -FilePath $built -WorkingDirectory (Split-Path $built)
    $checks['GUI_launch_requested'] = $true
} else {
    $checks['GUI_launch_requested'] = $false
}
# Never mark these checks as passed based solely on a process launch or file presence.
$manual = [ordered]@{
    Korean_IME_commit_and_backspace = 'NOT_TESTED'
    Korean_subtitle_SRT_round_trip = 'NOT_TESTED'
    Shorts_1080x1920_MP4_decodes = 'NOT_TESTED'
    Discord_browser_clicked = 'NOT_TESTED'
    Donation_browser_clicked = 'NOT_TESTED'
    NVENC_or_CPU_output_decodes = 'NOT_TESTED'
    Installer_upgrade_and_uninstall = 'NOT_TESTED'
    Settings_and_projects_preserved = 'NOT_TESTED'
}
$reportObj = [ordered]@{
    release = 'FilmCraft v0.6.0 RC22'
    timestamp_utc = [DateTime]::UtcNow.ToString('o')
    automatic_checks = $checks
    build_steps = $steps
    manual_verification = $manual
    note = 'NOT_TESTED means no execution evidence; file presence is not runtime proof.'
}
$out = if ([IO.Path]::IsPathRooted($Report)) { $Report } else { Join-Path $root $Report }
$folder = Split-Path -Parent $out
if (-not (Test-Path -LiteralPath $folder)) { New-Item -ItemType Directory -Path $folder -Force | Out-Null }
$reportObj | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $out -Encoding UTF8
Write-Host "[REPORT] $out"
if ($RunBuild -and $steps.Count -lt 5) { throw 'RC22 build/release gate stopped at a failed step. See report.' }
if ($RunBuild -and ($steps | Where-Object { -not $_.passed })) { throw 'RC22 build/release gate failed. See report.' }
