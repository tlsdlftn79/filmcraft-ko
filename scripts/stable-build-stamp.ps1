# Assert binaries match the Rust lockfile before INSTALL.cmd -SkipBuild.
$StableBuildVersion = '0.6.0'
function Get-StableBuildStampPath([string]$BinDir) {
    return (Join-Path $BinDir 'filmcraft-korean-stable-build.json')
}
function Get-StableSourceFingerprint([string]$RootPath) {
    # Fail closed when app sources changed after the last BUILD/PACKAGE execution.
    # Include Korean TSV, Rust, shader and icon inputs, but never generated `target` output.
    $records = New-Object 'System.Collections.Generic.List[string]'
    foreach ($directory in @('crates','apps','xtask','assets')) {
        $path = Join-Path $RootPath $directory
        if (-not (Test-Path -LiteralPath $path -PathType Container)) { throw "Missing source directory: $path" }
        $files = Get-ChildItem -LiteralPath $path -File -Recurse | Where-Object {
            $_.FullName -notmatch '[\\/]target[\\/]' -and $_.FullName -notmatch '[\\/]__pycache__[\\/]'
        } | Sort-Object FullName
        foreach ($file in $files) {
            $relative = $file.FullName.Substring($RootPath.TrimEnd('\').Length + 1).Replace('\','/')
            $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $file.FullName).Hash.ToLowerInvariant()
            $records.Add("$relative $hash")
        }
    }
    foreach ($file in @('Cargo.toml','Cargo.lock')) {
        $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $RootPath $file)).Hash.ToLowerInvariant()
        $records.Add("$file $hash")
    }
    $bytes = [Text.Encoding]::UTF8.GetBytes([string]::Join("`n",$records))
    $algorithm = [Security.Cryptography.SHA256]::Create()
    try {
        return [BitConverter]::ToString($algorithm.ComputeHash($bytes)).Replace('-','').ToLowerInvariant()
    } finally { $algorithm.Dispose() }
}

function Write-StableBuildStamp([string]$BinDir, [string]$RootPath) {
    $gui = Join-Path $BinDir 'filmcraft.exe'
    $cli = Join-Path $BinDir 'filmcraft-cli.exe'
    $lock = Join-Path $RootPath 'Cargo.lock'
    foreach ($f in @($gui,$cli,$lock)) { if (-not (Test-Path -LiteralPath $f -PathType Leaf)) { throw "Stable build stamp input missing: $f" } }
    $data = [ordered]@{
        version = $StableBuildVersion
        source_sha256 = (Get-StableSourceFingerprint -RootPath $RootPath)
        cargo_lock_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $lock).Hash.ToLowerInvariant()
        gui_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $gui).Hash.ToLowerInvariant()
        cli_sha256 = (Get-FileHash -Algorithm SHA256 -LiteralPath $cli).Hash.ToLowerInvariant()
    }
    $out = Get-StableBuildStampPath $BinDir
    $data | ConvertTo-Json -Depth 2 | Set-Content -LiteralPath $out -Encoding UTF8
    Write-Host "[STAMP] $out"
}
function Assert-StableBuildStamp([string]$BinDir, [string]$RootPath) {
    $stamp = Get-StableBuildStampPath $BinDir
    if (-not (Test-Path -LiteralPath $stamp -PathType Leaf)) {
        throw 'Stable build stamp missing; run BUILD.cmd again before INSTALL.cmd -SkipBuild.'
    }
    $data = Get-Content -LiteralPath $stamp -Raw | ConvertFrom-Json
    if ($data.version -ne $StableBuildVersion) { throw 'Stale Rust release version in build stamp.' }
    $sourceHash = Get-StableSourceFingerprint -RootPath $RootPath
    if ($data.source_sha256 -ne $sourceHash) { throw 'Sources changed since the last Stable BUILD/PACKAGE; rebuild before -SkipBuild.' }
    foreach ($entry in @(
        @('cargo_lock_sha256',(Join-Path $RootPath 'Cargo.lock')),
        @('gui_sha256',(Join-Path $BinDir 'filmcraft.exe')),
        @('cli_sha256',(Join-Path $BinDir 'filmcraft-cli.exe'))
    )) {
        $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $entry[1]).Hash.ToLowerInvariant()
        if ($hash -ne $data.($entry[0])) { throw "Stale or modified stable artifact: $($entry[1])" }
    }
    Write-Host '[OK] Stable build stamp matches Cargo.lock and GUI/CLI hashes.'
}
