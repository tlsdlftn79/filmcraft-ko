# Shared Windows PE32+ validation for FilmCraft release artifacts.
# The PE header contains a four-byte signature and a 20-byte COFF file header.
# The Subsystem is at optional-header offset 0x44, NOT PE-signature offset 0x44.
# See https://learn.microsoft.com/windows/win32/debug/pe-format
function Assert-Win64Pe([string]$Path, [int]$Subsystem) {
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) { throw "Executable missing: $Path" }
    $file = [IO.File]::OpenRead($Path)
    try {
        if ($file.Length -lt 0x40) { throw "File is too short to hold a DOS header: $Path" }
        $reader = [IO.BinaryReader]::new($file)
        if ($reader.ReadUInt16() -ne 0x5A4D) { throw "Missing MZ header: $Path" }
        $file.Position = 0x3C
        $offset = $reader.ReadInt32()
        if ($offset -lt 0x40 -or $offset -gt ($file.Length - 0x18)) {
            throw "Invalid PE signature offset: $Path"
        }
        $file.Position = $offset
        if ($reader.ReadUInt32() -ne 0x00004550) { throw "Missing PE signature: $Path" }
        if ($reader.ReadUInt16() -ne 0x8664) { throw "Not an x64 executable: $Path" }
        $file.Position = $offset + 0x14
        $optionalSize = [int]$reader.ReadUInt16()
        if ($optionalSize -lt 0x46) { throw "PE optional header too small for Subsystem: $Path" }
        $optionalHeader = $offset + 0x18
        if (($optionalHeader + $optionalSize) -gt $file.Length) {
            throw "Truncated PE optional header: $Path"
        }
        $file.Position = $optionalHeader
        if ($reader.ReadUInt16() -ne 0x20B) { throw "Expected PE32+ executable: $Path" }
        $file.Position = $optionalHeader + 0x44
        if ($reader.ReadUInt16() -ne $Subsystem) { throw "Unexpected Windows subsystem in $Path" }
    } finally { $file.Dispose() }
}
