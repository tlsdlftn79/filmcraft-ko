# FilmCraft v0.6.0 Stable — 한국어판 (비공식 커뮤니티 패치)

FilmCraft 오픈소스 영상 편집기의 한국어판입니다. **공식 FilmCraft 배포판이 아닌 커뮤니티 패치**이며, 원본 프로젝트와 별도로 유지됩니다.

## 주요 기능

- 한국어 UI 및 Windows 한글 IME 기반 문자 그래픽 편집
- 한국어 자막 불러오기·수정·내보내기 (SRT, WebVTT, CP949 호환 입력)
- YouTube Shorts 1080×1920(9:16) H.264/AAC MP4 프리셋
- CPU H.264, NVIDIA NVENC 및 FFmpeg 기반 AMD AMF·Intel QSV 재인코딩 경로
- 하드웨어 인코딩 실패 시 CPU 출력 대체, 출력 파일 백업·복구 처리
- 한국어판 후원 및 Discord 커뮤니티 링크, Windows 설치·포터블 구성

**GPU 관련 주의:** AMD·Intel 경로는 FilmCraft가 FFmpeg를 별도 실행하여 CPU 결과를 다시 인코딩하는 방식으로, AMF/QSV 네이티브 SDK 인코더가 아닙니다. FFmpeg/ffprobe가 설치되어 있고 해당 인코더·드라이버가 지원돼야 합니다. GPU 하드웨어 성능 개선을 보장하지 않습니다.

## Windows 빌드 및 배포

필요 환경: Windows 10/11 x64, Rust 1.95+ (x86_64-pc-windows-msvc), Visual Studio 2022 C++ Build Tools + Windows SDK, Python 3, Inno Setup 6.3+.

```bat
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
```

출력 위치는 `dist/` 입니다.

- `FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Setup.exe`
- `FilmCraft_v0.6.0_Stable_Korean_Windows_x64_Portable.zip`
- 각 결과물의 `.sha256` 체크섬 파일
- `FilmCraft_v0.6.0_Stable_RELEASE_MANIFEST.json` (VERIFY.cmd가 검증에 성공한 후 생성)

**중요:** 이 소스 ZIP에는 Windows용 EXE가 포함되지 않습니다. `TEST.cmd`와 `VERIFY.cmd`는 각각 컴파일/정적 검증 및 산출물 구성·체크섬 검증을 수행하므로, 모든 작업의 성공과 실제 Windows 사용성 테스트는 별개입니다. `INSTALL.cmd`는 디지털 서명을 자동 추가하지 않습니다.

### 포터블과 설치판

- 설치판: `%LOCALAPPDATA%\Programs\FilmCraft Korean` 경로에 사용자 권한으로 설치하며, 기존 비공식 커뮤니티 패치의 설치 AppId를 유지하여 업그레이드 가능합니다.
- 포터블: `portable.txt`를 포함해 EXE 옆의 데이터 폴더에 설정·로그를 저장합니다. 제거할 때 개인 프로젝트 및 사용자 데이터를 먼저 백업하세요.
- 원본 FilmCraft와 설치 식별자 및 경로를 별도로 사용합니다.

## 검증 및 출시 상태

사용자가 Windows Release 컴파일·Rust 테스트·한글 IME·자막·Shorts·NVENC·AMF·QSV·설치·포터블까지 11개 항목이 통과했다고 보고했습니다(2026-10-11). 단, 이 작업 환경에서는 Windows/MSVC 빌드 로그, 하드웨어 테스트 기록, 설치판 파일을 직접 확인하지 못했습니다. 따라서 **사용자 통과 보고**와 **이 소스에서 수행한 정적 검사**를 구분합니다. 자세한 기준은 [`STABLE_RELEASE_GATE_KO.md`](STABLE_RELEASE_GATE_KO.md).

## 프로젝트 및 라이선스

원본 FilmCraft: https://github.com/storytold/filmcraft  
비공식 한국어판 후원: https://ctee.kr/place/caw  
라이선스: MIT OR Apache-2.0 (`LICENSE-MIT`, `LICENSE-APACHE`)

이전 버전 변경 이력은 [`docs/README-KOREAN-RELEASE-CANDIDATE-HISTORY.md`](docs/README-KOREAN-RELEASE-CANDIDATE-HISTORY.md)를 참고하세요.
