# FilmCraft 한국어 패치 v0.5.8 — Windows 빌드/설치 검사 안정화

## 수정 내용

- **v0.5.7의 PE Subsystem 필드 오프셋 회귀 오류 해결:** `Subsystem`은 선택적 헤더에서 +`0x44`, PE 서명에서 +`0x5C`입니다. 이전 구현은 이를 혼동하여 PE 서명 +`0x44`를 검사했습니다. 새 `scripts/windows-pe.ps1`에서 선택적 헤더 시작 위치(+`0x18`)를 따로 계산합니다.
- **PE 검사 공통화:** `BUILD.cmd`, `PACKAGE.cmd`, `INSTALL.cmd`가 모두 동일한 검사 루틴을 사용합니다. 64비트 MSVC PE32+ 형식과 GUI(2)/CLI(3) Subsystem을 검사하며 잘못된/짧은 헤더를 거부합니다.
- **설치/포터블 구성 일치:** 두 경로 모두 `filmcraft.exe`와 `filmcraft-cli.exe`를 빌드·포함하며, Release 리소스 생성 실패를 확인하도록 `FILMCRAFT_REQUIRE_WINRES=1` 설정을 통합했습니다.
- **배포 파일 무결성:** 빌드 성공 시 설치 EXE와 포터블 ZIP 각각에 `.sha256` 체크섬 파일을 생성합니다.
- **회귀 테스트 강화:** 올바른 PE 서명 기준 위치가 아니면 테스트가 실패하도록 합성 PE32+ 벡터를 재작성했습니다. 헤더 손상, x86 이미지, 서브시스템 불일치, 선택적 헤더 길이 오류를 검사합니다.
- 기존 한국어 번역 사전(3,756개 항목), 텍스트 IME 처리, 한국어 자막 코드 및 설치 UI 번역을 보존했습니다.

## 빌드/테스트

Windows 10/11 x64에서 Rust 1.95 이상(MSVC x64), VS 2022 C++ Build Tools 및 Inno Setup 6.3 이상을 설치합니다.

```bat
TEST.cmd
BUILD.cmd
INSTALL.cmd
PACKAGE.cmd
```

`dist\FilmCraft_v0.5.8_Korean_Windows_x64_Setup.exe` (설치판)와 `dist\FilmCraft_v0.5.8_Korean_Windows_x64_Portable.zip` (포터블)이 생성되도록 구성했습니다. 각각 옆에 `.sha256` 파일을 생성합니다.

## 미검증 항목

현재 개발 환경에 Windows 및 Rust/Cargo와 Inno Setup이 없어 **실제 컴파일·설치 EXE 생성·한글 입력·영상 출력·설치/제거 작업은 실행하지 못했습니다.** Python 기반 정적 검증과 ZIP 비교는 실제 실행 검증을 대체하지 않습니다.
