# FilmCraft v0.6.0 Stable Korean patch — Windows x64, Inno Setup 6.3+.
# Called by INSTALL.cmd. No administrator rights needed to build or install.
[CmdletBinding()]
param([switch]$SkipBuild)
$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path

function Require-Tool([string]$Name) {
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "$Name was not found. Install Rust 1.95+ for x86_64-pc-windows-msvc and VS 2022 C++ Build Tools."
    }
}

function Find-Iscc {
    if ($env:INNO_ISCC) {
        if (-not (Test-Path -LiteralPath $env:INNO_ISCC -PathType Leaf)) {
            throw "INNO_ISCC does not refer to a file: $($env:INNO_ISCC)"
        }
        return (Resolve-Path -LiteralPath $env:INNO_ISCC).Path
    }
    $command = Get-Command 'ISCC.exe' -ErrorAction SilentlyContinue
    if ($command) { return $command.Source }
    $locations = @(
        (Join-Path ${env:ProgramFiles(x86)} 'Inno Setup 6\ISCC.exe'),
        (Join-Path $env:ProgramFiles 'Inno Setup 6\ISCC.exe')
    )
    foreach ($location in $locations) {
        if (Test-Path -LiteralPath $location -PathType Leaf) { return $location }
    }
    throw 'Inno Setup 6.3+ compiler ISCC.exe not found. Install from https://jrsoftware.org/isdl.php (or set INNO_ISCC).'
}

. (Join-Path $PSScriptRoot 'windows-pe.ps1')
. (Join-Path $PSScriptRoot 'stable-build-stamp.ps1')

Push-Location $root
try {
    if (-not [Environment]::Is64BitOperatingSystem) { throw 'Windows x64 is required.' }
    if ([Environment]::OSVersion.Platform -ne [PlatformID]::Win32NT) { throw 'Run INSTALL.cmd on Windows.' }
    if (Get-Command py.exe -ErrorAction SilentlyContinue) { & py -3 (Join-Path $root 'scripts/check_stable_release.py') }
    elseif (Get-Command python.exe -ErrorAction SilentlyContinue) { & python (Join-Path $root 'scripts/check_stable_release.py') }
    else { throw 'Python 3 required to validate Stable release identity.' }
    if ($LASTEXITCODE -ne 0) { throw 'Stable source identity check failed.' }
    $iscc = Find-Iscc
    # No stale build may be packed by default; this switch is for reproducing a prior verified release.
    if (-not $SkipBuild) {
        Require-Tool 'cargo'
        Require-Tool 'rustc'
        $versionLine = & rustc --version
        if ($LASTEXITCODE -ne 0 -or $versionLine -notmatch '^rustc\s+(\d+)\.(\d+)\.(\d+)') {
            throw 'Cannot read rustc version.'
        }
        $version = [version]::new([int]$Matches[1], [int]$Matches[2], [int]$Matches[3])
        if ($version -lt [version]::new(1,95,0)) { throw "Rust 1.95+ is required; found $version" }
        $info = & rustc -vV
        if ($LASTEXITCODE -ne 0 -or -not ($info -match '^host: x86_64-pc-windows-msvc$')) {
            throw 'Use Rust host x86_64-pc-windows-msvc (Visual Studio 2022 and Windows SDK required).'
        }
    }
    if ($env:CARGO_BUILD_TARGET) {
        throw 'Unset CARGO_BUILD_TARGET; this installer requires x64 MSVC output under target\release.'
    }
    $targetDir = if ($env:CARGO_TARGET_DIR) {
        if ([IO.Path]::IsPathRooted($env:CARGO_TARGET_DIR)) { $env:CARGO_TARGET_DIR }
        else { Join-Path $root $env:CARGO_TARGET_DIR }
    } else { Join-Path $root 'target' }
    if (-not $SkipBuild) {
        if (-not (Test-Path -LiteralPath (Join-Path $root 'Cargo.lock'))) { throw 'Cargo.lock missing.' }
        $env:FILMCRAFT_REQUIRE_WINRES = '1'
        Write-Host '[BUILD] cargo build --locked --release -p filmcraft -p filmcraft-cli'
        & cargo build --locked --release -p filmcraft -p filmcraft-cli
        if ($LASTEXITCODE -ne 0) { throw "Cargo build failed (exit $LASTEXITCODE)." }
    }
    $bin = Join-Path $targetDir 'release'
    $gui = Join-Path $bin 'filmcraft.exe'
    $cli = Join-Path $bin 'filmcraft-cli.exe'
    Assert-Win64Pe -Path $gui -Subsystem 2
    Assert-Win64Pe -Path $cli -Subsystem 3
    if ($SkipBuild) { Assert-StableBuildStamp -BinDir $bin -RootPath $root }
    else { Write-StableBuildStamp -BinDir $bin -RootPath $root }
    Write-Host '[OK] x64 GUI and CLI Windows PE headers verified.'

    $stage = Join-Path $targetDir 'filmcraft-korean-installer-stage'
    if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
    New-Item -ItemType Directory -Path $stage -Force | Out-Null
    foreach ($item in @('README-KOREAN.md','CHANGELOG-KO.md','STABLE_RELEASE_GATE_KO.md','LICENSE-MIT','LICENSE-APACHE')) {
        $source = Join-Path $root $item
        if (-not (Test-Path -LiteralPath $source -PathType Leaf)) { throw "Required installer file missing: $source" }
        Copy-Item -LiteralPath $source -Destination $stage -ErrorAction Stop
    }
    Copy-Item -LiteralPath $gui -Destination $stage -ErrorAction Stop
    Copy-Item -LiteralPath $cli -Destination $stage -ErrorAction Stop

    $dist = Join-Path $root 'dist'
    New-Item -ItemType Directory -Path $dist -Force | Out-Null
    $expected = Join-Path $dist 'FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe'
    if (Test-Path -LiteralPath $expected) { Remove-Item -LiteralPath $expected -Force }
    $script = Join-Path $root 'packaging\windows\filmcraft-korean.iss'
    if (-not (Test-Path -LiteralPath $script)) { throw 'Installer .iss script is missing.' }
    Write-Host "[INSTALLER] $iscc"
    & $iscc "/DStageDir=$stage" "/DOutDir=$dist" $script
    if ($LASTEXITCODE -ne 0) { throw "Inno Setup compiler failed (exit $LASTEXITCODE)." }
    if (-not (Test-Path -LiteralPath $expected -PathType Leaf)) { throw "No Setup.exe at $expected" }
    if ((Get-Item -LiteralPath $expected).Length -lt 4096) { throw 'Setup.exe is unexpectedly small.' }
    $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $expected).Hash
    Write-Host "[OK] Installer: $expected"
    $checksumFile = "$expected.sha256"
    # Standard format: SHA256 followed by the artifact basename (ASCII, without BOM).
    Set-Content -LiteralPath $checksumFile -Value "$($hash.ToLowerInvariant())  $(Split-Path -Leaf $expected)" -Encoding Ascii
    Write-Host "[SHA256] $hash"
    Write-Host "[CHECKSUM] $checksumFile"
    Write-Warning 'Installer is unsigned by default; Windows SmartScreen may warn. Code signing needs a trusted certificate.'
    Write-Warning 'Install/uninstall smoke tests must be run separately on an actual Windows 10/11 PC.'
} catch {
    Write-Host ('[ERROR] ' + $_.Exception.Message) -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}
