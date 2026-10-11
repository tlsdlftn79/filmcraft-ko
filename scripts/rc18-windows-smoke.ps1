# Read-only Windows smoke report for FilmCraft v0.6.0 RC22.
# It will not install, uninstall, alter user settings, or upload data.
[CmdletBinding()]
param(
    [switch]$Launch,
    [string]$Report = 'build-logs\rc18-windows-smoke.txt'
)
$ErrorActionPreference = 'Stop'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) {
    throw 'Windows 10/11 required to run this smoke test.'
}
$installed = Join-Path $env:LOCALAPPDATA 'Programs\FilmCraft Korean\filmcraft.exe'
$built = Join-Path $root 'target\release\filmcraft.exe'
$exe = if (Test-Path -LiteralPath $installed -PathType Leaf) { $installed }
       elseif (Test-Path -LiteralPath $built -PathType Leaf) { $built }
       else { $null }
$shortcut = Join-Path $env:APPDATA 'Microsoft\Windows\Start Menu\Programs\FilmCraft 한국어판.lnk'
$uninstall = Get-ItemProperty -Path 'HKCU:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*' -ErrorAction SilentlyContinue |
    Where-Object { $_.Publisher -eq 'FilmCraft Korean Community Patch' } | Select-Object -First 1
$lines = @(
    'FilmCraft RC22 Windows manual smoke test (read-only)'
    'IMPORTANT: these are file/registration checks, not proof of correct GUI behavior.'
    ('Date: ' + (Get-Date).ToString('s'))
    ('Windows: ' + [Environment]::OSVersion.VersionString)
    ('Executable found: ' + [bool]$exe)
    ('Per-user installation found: ' + (Test-Path -LiteralPath $installed -PathType Leaf))
    ('Start menu shortcut found: ' + (Test-Path -LiteralPath $shortcut -PathType Leaf))
    ('Uninstall registry entry found: ' + [bool]$uninstall)
    ''
    'MANUAL CHECKS (record PASS/FAIL only after actually testing):'
    '[ ] Type tool: 한글 테스트 123 ABC, Backspace, arrows and Enter'
    '[ ] Korean SRT: import -> edit -> export -> reimport'
    '[ ] Discord button opens default browser'
    '[ ] Support button opens https://ctee.kr/place/caw'
    '[ ] Shorts: 1080x1920 MP4, H.264/AAC; check with verify_shorts_mp4.py'
    '[ ] GPU unavailable -> CPU fallback; final MP4 decodes'
    '[ ] Settings and project survive upgrade/uninstall (test separately)'
)
if ($Launch) {
    if (-not $exe) { throw 'No filmcraft.exe found. Run BUILD.cmd or INSTALL.cmd first.' }
    Write-Host "[LAUNCH] $exe"
    Start-Process -FilePath $exe -WorkingDirectory (Split-Path $exe)
    $lines += 'Launch requested: yes (the GUI result still requires manual verification).'
} else {
    $lines += 'Launch requested: no (use -Launch to open the app).'
}
$destination = if ([IO.Path]::IsPathRooted($Report)) { $Report } else { Join-Path $root $Report }
$parent = Split-Path -Parent $destination
if (-not (Test-Path $parent)) { New-Item -ItemType Directory -Path $parent -Force | Out-Null }
$lines | Set-Content -LiteralPath $destination -Encoding UTF8
$lines | ForEach-Object { Write-Host $_ }
Write-Host "[REPORT] $destination"
