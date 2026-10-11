#!/usr/bin/env python3
"""Static installer contract checks (does not replace an ISCC compile or Windows smoke test)."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent.parent
ISS = ROOT / "packaging/windows/filmcraft-korean.iss"
PS1 = ROOT / "scripts/build-installer.ps1"
CMD = ROOT / "INSTALL.cmd"
WXS = ROOT / "packaging/windows/filmcraft.wxs"


def expect(value: bool, message: str) -> None:
    if not value:
        raise AssertionError(message)


def main() -> None:
    iss = ISS.read_text(encoding="utf-8-sig")
    ps = PS1.read_text(encoding="utf-8-sig")
    cmd = CMD.read_text(encoding="utf-8-sig")
    wxs = WXS.read_text(encoding="utf-8-sig")
    # Installer intentionally has a unique identity and cannot overwrite upstream MSI.
    app_id = re.search(r"(?m)^AppId=\{\{([0-9a-fA-F-]{36})\}", iss)
    expect(bool(app_id), "The installer needs a stable, distinct GUID AppId")
    expect(app_id.group(1).lower() not in wxs.lower(), "AppId must differ from the upstream MSI")
    expect("PrivilegesRequired=lowest" in iss, "Install should not demand administrator rights")
    expect("ArchitecturesAllowed=x64compatible" in iss, "Must explicitly target x64-compatible Windows")
    expect("MinVersion=10.0" in iss, "Windows 10+ only")
    expect('Name: "ko"' in iss and 'Name: "en"' in iss, "Missing Korean/English installer language")
    expect("ko.LanguageID=$0412" in iss, "Korean LCID missing")
    expect("ko.WelcomeLabel1=" in iss and "ko.FinishedHeadingLabel=" in iss, "Main Korean wizard messages missing")
    expect('Flags: unchecked' in iss, "Desktop shortcut should be opt-in")
    for file in ("filmcraft.exe", "filmcraft-cli.exe", "README-KOREAN.md", "CHANGELOG-KO.md", "STABLE_RELEASE_GATE_KO.md", "LICENSE-MIT", "LICENSE-APACHE"):
        expect(f'\\{file}"; DestDir: "{{app}}"' in iss, f"Required installer payload missing: {file}")
    expect("[UninstallDelete]" not in re.sub(r"(?m)^\s*;.*$", "", iss), "Never delete user data on uninstall")
    expect("portable.txt" not in re.sub(r"(?m)^\s*;.*$", "", iss), "Installer must not enable portable mode")
    pe = (ROOT / "scripts/windows-pe.ps1").read_text(encoding="utf-8")
    expect("$optionalHeader = $offset + 0x18" in pe, "PE optional header begins 24 bytes after signature")
    expect("$file.Position = $optionalHeader + 0x44" in pe, "Subsystem is at offset 0x44 within the optional header")
    expect("$file.Position = $offset + 0x44" not in pe, "Do not read Subsystem at PE-signature offset 0x44")
    expect("$optionalSize -lt 0x46" in pe, "Truncated optional header must be rejected")
    expect(". (Join-Path $PSScriptRoot 'windows-pe.ps1')" in ps, "Installer must load PE validation")
    winbuild = (ROOT / "scripts/build-win.ps1").read_text(encoding="utf-8")
    expect(". (Join-Path $PSScriptRoot 'windows-pe.ps1')" in winbuild, "Build and package must validate PE")
    expect("Copy-Item -LiteralPath $cliBinary -Destination $stage" in winbuild, "Portable distribution needs CLI")
    expect("$env:FILMCRAFT_REQUIRE_WINRES = '1'" in winbuild, "Windows builds must require icon resources")
    expect("$zip.sha256" in winbuild and '"$expected.sha256"' in ps, "Release checksum output missing")
    expect("Assert-Win64Pe -Path $gui -Subsystem 2" in ps, "GUI PE validation missing")
    expect("Assert-Win64Pe -Path $cli -Subsystem 3" in ps, "CLI PE validation missing")
    expect("cargo build --locked --release -p filmcraft -p filmcraft-cli" in ps, "Missing reproducible release build")
    expect("/DStageDir=" in ps and "/DOutDir=" in ps, "Inno staging args missing")
    expect("Get-FileHash -Algorithm SHA256" in ps, "Installer integrity hash missing")
    expect("build-installer.ps1" in cmd and "%*" in cmd, "INSTALL.cmd must dispatch arguments to the builder")
    expect((ROOT / "assets/app-icon/filmcraft.ico").is_file(), "Installer icon missing")
    print("[OK] Static Windows setup contract: language, identity, content, arch, safety and builder")
    print("[NOTE] ISCC compilation, installation and uninstall have NOT been performed.")


if __name__ == "__main__":
    main()
