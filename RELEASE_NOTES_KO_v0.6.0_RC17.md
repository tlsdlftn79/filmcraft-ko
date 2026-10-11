# FilmCraft v0.6.0 RC17 — IME 미사용 함수 경고 수정

## 수정
- `crates/ui-egui/src/panels/graphics.rs`의 `has_ime_edit()`에 `#[cfg(test)]` 적용.
- 기존 한글 IME 단위 테스트 유지; 일반 라이브러리 빌드에서는 해당 테스트 보조 함수 제외.
- `#[allow(dead_code)]`로 경고를 숨기지 않음.
- Windows `TEST.cmd`에 `scripts/check_rc17_ime_dead_code.py` 정적 회귀 검사 추가.
- RC17 설치/포터블 버전 표기 및 Windows CI 산출물 경로 갱신.

## 검증 명령 (Windows)
```bat
python scripts\check_rc17_ime_dead_code.py
cargo check --locked -p filmcraft-ui-egui
cargo test --locked -p filmcraft-ui-egui korean_ime_tests
TEST.cmd
BUILD.cmd
INSTALL.cmd
```

## 한계
- 이 패치는 제보된 `has_ime_edit is never used` 경고에 집중한 수정입니다.
- Rust/MSVC 실제 컴파일, Windows 한글 IME, 후원/Discord 클릭, GPU 인코딩 및 설치 프로그램 실행은 별도 검증이 필요합니다.
