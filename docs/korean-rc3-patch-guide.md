# FilmCraft v0.6.0 RC1 → RC3 patch instructions

1. Back up your current RC1 source tree and your projects.
2. Extract `FilmCraft_v0.6.0_RC3_Korean_Update_Patch.zip` **into the root folder containing `Cargo.toml`**, preserving paths, and allow replacing existing files.
3. On Windows 10/11 x64 with Rust 1.95+, Visual Studio 2022 C++ Build Tools, Python 3 and Inno Setup 6.3+: run `TEST.cmd`, then `BUILD.cmd`, `PACKAGE.cmd`, `INSTALL.cmd`, and `VERIFY.cmd`.
4. Check the `docs/testing-korean-v060-rc3.md` checklist, notably Korean IME input, CP949/UTF-8 subtitle imports, font selection, video burn-in, update/uninstall.
5. This source patch is **not** a binary upgrade installer. It must be compiled on Windows.

RC3 is based on the RC1 full source from this conversation, not an upstream FilmCraft release. The Rust package version remains as upstream (0.5.0) in Cargo.toml and Cargo.lock.
