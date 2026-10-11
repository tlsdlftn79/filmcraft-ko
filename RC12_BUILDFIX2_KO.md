# FilmCraft v0.6.0 RC12 BuildFix2 — Windows 컴파일·COM 초기화 보강

기준: `FilmCraft_v0.6.0_RC12_BuildFix1_Full_Source.zip`

## 변경 내용

1. `crates/platform/src/media_foundation/mft.rs`의 `api()`에서 **매 호출 스레드마다** `ensure_com()`을 호출합니다. 이전 코드는 `OnceLock` 초기화를 처음 실행하는 스레드에서만 `load()`가 COM을 초기화했기 때문에, 이미 캐시된 API를 다른 스레드의 인코더 검색에서 사용하는 경우 해당 스레드의 COM 초기화가 누락될 수 있었습니다.
2. `scripts/build-win.ps1`의 `TEST.cmd` 경로에 BuildFix1/BuildFix2 정적 검사와 `filmcraft-platform`, `filmcraft-ui-egui` Windows 컴파일 확인을 Rust 장기 테스트보다 앞에 배치했습니다.
3. `scripts/test_mf_buildfix2.py`에는 6개 회귀 테스트가 있으며, 첫 스레드에서만 COM을 초기화하거나 `Result` 오류 타입이 다시 충돌하는 경우 실패합니다.
4. BuildFix1에서 수정한 `MFVideoFormat_H264` import와 `std::result::Result<Vec<String>, String>`은 보존합니다.

## Windows 10/11 MSVC 검사

프로젝트 폴더에서 실행:

```bat
python scripts\check_mf_h264_buildfix.py
python scripts\test_mf_buildfix2.py
cargo check --locked -p filmcraft-platform
cargo check --locked -p filmcraft-ui-egui
TEST.cmd
BUILD.cmd
```

실패한 Cargo 진단을 파일로 저장하려면:

```bat
if not exist build-logs mkdir build-logs
cargo check --locked -p filmcraft-platform > build-logs\platform-check.log 2>&1
cargo check --locked -p filmcraft-ui-egui > build-logs\ui-check.log 2>&1
```

오류 보고 시 첫 번째 `error[E...]`부터 마지막 `could not compile`까지 포함된 로그를 공유하면 됩니다.

## 중요한 검증 범위

이번 단계의 코드 수정과 Python 정적 검사 통과는 **Windows Rust 실제 컴파일 통과**나 GPU 인코딩 성공을 증명하지 않습니다. `cargo`, MSVC 및 GPU 드라이버를 갖춘 Windows에서 결과를 확인해야 합니다. AMD AMF/Intel Quick Sync는 여전히 FilmCraft 내부 내보내기에서 구현되지 않았습니다. 기존 NVENC 및 CPU 대체 코드에는 손대지 않았습니다.
