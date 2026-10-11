# FilmCraft v0.6.0 RC13 — 한국어 문자 도구 IME 입력 경로 수정

기준: RC12 BuildFix2 전체 소스. RC13은 한국어 입력 안정화를 우선하는 개발 후보이며, Windows에서의 실제 동작을 검증한 정식판은 아닙니다.

## 수정 사항

- 문자 도구에서 IME 이벤트가 포함된 프레임의 **모든** 키를 무시하던 로직을 변경했습니다.
- 후보 선택에 사용되는 편집 키는 IME 조합 중에만 차단하며, 확정된 한글 뒤 별도로 누른 Enter·화살표 키 등은 정상 처리합니다.
- Windows 백엔드가 Key 이벤트를 Preedit/Commit보다 먼저 보내는 순서에도 대응하도록 다음 입력 이벤트와의 관계를 확인합니다.
- 조합 취소 직후의 Backspace 처리, 영문 혼합 입력 등 5개 회귀 테스트를 소스에 추가했습니다.
- 기존 한국어 번역, 자막, YouTube Shorts, NVENC·CPU 내보내기 및 후원 버튼을 보존했습니다.
- 설치 프로그램·포터블 ZIP·배포 CI의 패치 버전을 RC13으로 갱신했습니다.

## Windows 검사 방법

```bat
python scripts\check_rc13_ime.py
cargo check --locked -p filmcraft-platform
cargo check --locked -p filmcraft-ui-egui
cargo test --locked -p filmcraft-ui-egui korean_rc13_ime_key_routing_tests
TEST.cmd
BUILD.cmd
INSTALL.cmd
```

실제 문자 도구에서 `안녕하세요`, `한글 테스트 123 ABC`, 문자 뒤 Enter, Backspace, 커서 이동, 영어/한국어 전환을 확인하십시오.
필요하다면 `set FILMCRAFT_IME_DIAGNOSTICS=1`로 개인정보가 아닌 이벤트 종류·글자 수·포커스 상태만 기록할 수 있습니다.

## 확인할 사항

- RC13 소스의 정적 검사와 파일 패키징은 자동 검증합니다.
- 현재 실행 환경에는 Rust/Cargo 및 Windows GUI가 없어 실제 Cargo 컴파일, IME 조합, MP4 인코딩, 설치 실행 결과는 검증하지 못했습니다.
- AMD·Intel 전용 실제 하드웨어 인코딩은 여전히 구현되지 않았습니다.
