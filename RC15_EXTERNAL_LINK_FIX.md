# FilmCraft v0.6.0 RC15 — Discord / Korean support button fix

Base source: **FilmCraft v0.6.0 RC14**, without removing previous Korean IME, Shorts, GPU diagnosis, and installer features.

## Cause and changes

The desktop uses `eframe` with `default-features = false`; its optional `links` feature was not enabled. Consequently `egui::Context::open_url` could issue a UI command that the native backend ignored. The old full-width header drag hit target also overlapped the Discord and support buttons.

- `crates/ui-egui/src/links.rs`: use the operating system's default URL handler on desktop (Windows `rundll32.exe url.dll,FileProtocolHandler URL`, macOS `open`, Linux `xdg-open`) without shell-interpolating URLs; egui's native browser output remains in use on the web build. If the desktop launcher cannot start, log the failure and copy the URL to the clipboard. HTTPS-only for external project/community links.
- `crates/ui-egui/src/header.rs`: make only unoccupied title-bar space draggable, away from the Discord and support click rectangles.
- Retain Help-menu, About-dialog and Import-page link wiring. Donation URL remains `https://ctee.kr/place/caw`; Discord remains the upstream project's `https://discord.gg/artcraft`.
- Keep `Cargo.lock` unchanged; no new crate dependencies are required. RC15 packaging filenames and regression guards are updated.

## Windows build and verification

From the extracted `filmcraft-main` directory:

```bat
python scripts\check_rc15_links.py
TEST.cmd
BUILD.cmd
INSTALL.cmd
```

Manual GUI acceptance test:

1. Launch the rebuilt **RC15** `filmcraft.exe` (not an already installed RC14 binary).
2. Click **Discord** in the top header. It should invoke the Windows registered default browser with `https://discord.gg/artcraft`.
3. Click **한국어판 후원**. It should invoke the browser with `https://ctee.kr/place/caw`.
4. Re-test Help → Discord / Korean support and About → both links. Check that clicking title text still drags the window but clicking buttons does not.
5. If no browser opens, inspect application logs for `Could not launch default browser`; a failure to start the OS URL handler also copies the URL to the clipboard. Check that a system-wide default browser is configured in Windows settings.

## Validation limitation

Python static checks and ZIP/file equivalence checks can be run in the patching environment. Rust compilation, physical button clicks and external browser launch must be checked on Windows; they are **not yet certified as passing**.
