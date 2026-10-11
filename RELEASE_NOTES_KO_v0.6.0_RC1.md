# FilmCraft Korean Patch v0.6.0 RC1 (배포 후보)

원본 FilmCraft의 Cargo package version은 `0.5.0`으로 유지합니다. 이 문서의 `0.6.0 RC1`은 **비공식 한국어 패치 버전**이며 공식 FilmCraft의 버전이 아닙니다.

## 코드 변경

- Type Tool에서 한글 IME 조합 종료를 알리는 빈 `Preedit` 이벤트가 키보드 이벤트와 같은 프레임에 도착하면, 진행 중이던 조합을 닫은 Enter / Backspace / Escape 등이 문서 편집 작업으로 중복 적용되지 않도록 보정했습니다.
- 조합 종료 직후의 `Event::Text`(영문 등)는 계속 입력되도록 기존 로직을 보존했습니다.
- IME 종료 프레임 테스트 추가 (`korean_ime_dismissal_prevents_double_enter_backspace_and_escape`).
- 설치 파일·포터블 ZIP 버전 표기를 `v0.6.0_RC1`로 갱신했습니다.
- `VERIFY.cmd`, `scripts/verify_release.py`: 배포 파일의 체크섬, 구성 파일, 아카이브 무결성 및 MZ 헤더 검사 추가.
- 배포 검증 코드 자체에 대한 Python 단위 테스트 5개 추가.
- 수동 GitHub Actions 워크플로 `.github/workflows/korean-windows-rc.yml` 추가 (Windows 2022 러너에서 TEST → BUILD → PACKAGE → INSTALL → VERIFY).

## Windows 사용법

빌드 PC에 Rust >=1.95, Visual Studio 2022 C++ Build Tools와 SDK, Python 3, Inno Setup 6.3+가 필요합니다.

```bat
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
```

성공 시 `dist/FilmCraft_v0.6.0_RC1_Korean_Windows_x64_Setup.exe`와 `...Portable.zip`, 각각의 `.sha256` 파일이 생성됩니다. **이 ZIP에 컴파일된 Windows 실행 파일은 포함되어 있지 않습니다.**

## 품질 게이트 / 남은 작업

- Python 정적/회귀 검사는 작성한 환경에서 실행할 수 있지만, Rust `cargo check`, Windows MSI/EXE 설치·제거·업그레이드, Microsoft Korean IME 입력, MP4 렌더링은 Windows 실기기에서 별도로 검증해야 합니다.
- GitHub Actions 워크플로는 추가되었지만 **실행 성공 여부는 아직 검증되지 않았습니다.**
- 설치 파일은 기본적으로 코드 서명되어 있지 않습니다. Windows SmartScreen이 경고할 수 있습니다.
- 정식 v0.6.0 안정판 표기는 위 실기기 검사 완료 후 결정해야 합니다.

실기기 체크리스트: [`docs/testing-korean-v060-rc1.md`](docs/testing-korean-v060-rc1.md)
