# FilmCraft v0.5.8 비공식 한국어판 Windows 설치 프로그램

## 준비사항

- Windows 10 또는 11 x64
- Visual Studio 2022 C++ Build Tools 및 Windows SDK (C++ 데스크톱 개발)
- MSVC Rust 1.95 이상 (`rustc -vV`에서 `host: x86_64-pc-windows-msvc`)
- Inno Setup 6.3 이상, **Inno Setup 6** `ISCC.exe` 필요
  - 공식 다운로드: https://jrsoftware.org/isdl.php
  - 일반적인 설치 명령: `winget install --id JRSoftware.InnoSetup -e -s winget -i`
- 최초 빌드 때 Cargo 패키지 다운로드를 위한 인터넷 연결 가능성이 있음

## 사용법

압축을 풀고 `filmcraft-main` 폴더에서:

```bat
TEST.cmd
INSTALL.cmd
```

최종 산출물은 **`dist\FilmCraft_v0.5.8_Korean_Windows_x64_Setup.exe`** 입니다.
빌드된 두 실행 파일이 필요하며 `INSTALL.cmd`가 기본적으로 항상 최신 릴리스 빌드를 수행합니다.

```bat
REM 이미 직접 빌드한 filmcraft.exe / filmcraft-cli.exe를 사용할 때만
INSTALL.cmd -SkipBuild

REM Inno Setup ISCC.exe 자동 탐지에 실패한 경우
set "INNO_ISCC=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
INSTALL.cmd
```

`CARGO_TARGET_DIR`을 설정한 경우에는 그 경로의 `release\` 아래 실행 파일 두 개를 사용합니다.
기존의 `PACKAGE.cmd`는 포터블 버전이고 `INSTALL.cmd`는 제거 프로그램이 있는 Windows 설치 EXE를 만듭니다.

## 사용자에게 제공하는 기능

| 구분 | 동작 |
| --- | --- |
| 설치 UI | 한국어 / 영어, 시스템 UI 언어 자동 선택 |
| 기본 설치 경로 | `%LOCALAPPDATA%\Programs\FilmCraft Korean` |
| 권한 | 일반 사용자별 설치, 관리자 승격 불필요 |
| 바로가기 | 시작 메뉴 자동, 바탕화면 선택 |
| 실행 | 설치 완료 화면에서 실행 여부 선택 |
| 제거 | Windows 설정 → 앱 → 설치된 앱에서 제거 |
| 사용자 데이터 | 프로그램 설치 파일만 제거; 프로젝트/사용자 설정 자동 삭제하지 않음 |
| 기존 정식 MSI | 별도 AppId 및 설치 폴더 사용. **동시 사용 시 사용자 설정 저장소는 공유할 수 있으니 백업 권장** |
| 포터블 모드 | 사용하지 않음(`portable.txt` 없음) |

## 실패할 때 점검

1. Rust/Cargo 설치: `rustc --version`, `cargo --version`.
2. Rust 호스트: `rustc -vV` → `host: x86_64-pc-windows-msvc`.
3. C++ 빌드 도구 및 Windows SDK의 `link.exe`, `rc.exe` 확인.
4. Inno Setup 6의 `ISCC.exe` 설치 또는 `INNO_ISCC` 환경변수 지정.
5. 테스트 오류는 `TEST.cmd`를 먼저 실행하고 해당 출력 확인.
6. `-SkipBuild`를 사용했다면 `target\release\filmcraft.exe`와 `filmcraft-cli.exe`가 **Windows x64** 빌드인지 확인.

빌드 성공 시 설치 프로그램 옆에 `<설치 파일명>.sha256` 체크섬 파일이 생성됩니다. `PACKAGE.cmd`로 만든 포터블 ZIP도 같은 형식의 체크섬이 생성됩니다.

## 개발/배포 검증

- `py -3 scripts\check_installer.py` : Windows 외 환경에서도 가능한 **정적 검사**.
- **실행 검증 미완료**: 실제 Win10/11에서 `INSTALL.cmd` → Setup.exe 설치 → GUI 실행 → 제거 → 설정 유지 → 재설치 테스트 필요.
- Setup.exe **기본 코드 서명 없음**. 외부 배포 때 신뢰 가능한 서명 인증서로 서명하고 SHA-256 체크섬을 배포할 것을 권장.
- 설치 마법사의 일반 페이지 중심 한국어 번역을 포함하나, 일부 Inno Setup 내부 메시지는 영어일 수 있음.
- 이 설치 프로그램은 원본 제작사에서 발행한 **공식** 설치 프로그램이 아님.


## RC11 추가 진단

`TEST.cmd`는 한글 첫 포커스 관련 정적 검사와 GPU 테스트 도구의 독립 유닛 테스트를 실행합니다. 실기기 GPU 진단은 `set FILMCRAFT_TEST_GPU_ENCODERS=1` 후 `TEST.cmd`를 실행하세요. AMF/QSV는 FilmCraft 자체 내보내기 기능이 아닙니다.
