# FilmCraft 비공식 한국어 패치 v0.5.3 — InstallerFix

## 신규 기능

- **INSTALL.cmd**: Windows에서 Release 빌드 후 **Inno Setup 6.3+**를 이용해 설치용 EXE 생성.
- **한국어/영어 설치 마법사**: Windows UI 언어 기반 기본 선택, 설치 위치 확인, 설치 완료 후 실행 옵션.
- **관리자 권한 없는 사용자별 설치**: `%LOCALAPPDATA%\Programs\FilmCraft Korean` 기본 위치.
- **시작 메뉴 바로가기**, 선택식 **바탕화면 바로가기**, Windows 앱 및 기능의 **제거 프로그램** 제공.
- **GUI+CLI** (`filmcraft.exe`, `filmcraft-cli.exe`) 포함, 프로젝트/설정/캐시 제거 자동화 없음.
- **비공식 패치 독립 AppId**: 업스트림 공식 WiX MSI의 설치 및 업데이트 코드와 분리.
- Rust 릴리스 빌드 실패, 바이너리 누락, x64 PE 형식 및 GUI/CLI subsystem 불일치 때 설치 패키지 생성 중단.
- 설치 프로그램 SHA-256 출력, 기존 WiX MSI 배포 스크립트 유지.
- `scripts/check_installer.py`로 정적 설치 계약 검사 추가, 기존 TEST.cmd와 통합.
- PACKAGE.cmd의 포터블 산출물 이름 v0.5.3으로 변경(실제 애플리케이션 원본 Cargo 버전은 변경 없음).

## 출력 (Windows에서 직접 빌드해야 함)

```bat
TEST.cmd
INSTALL.cmd
```

출력: `dist\FilmCraft_v0.5.3_Korean_Windows_x64_Setup.exe`

기존 `PACKAGE.cmd`는 독립적인 **포터블 ZIP** 빌드 명령으로 남겨 둡니다.

## 검증

- 통과: 설치 스크립트 구조 정적 검사, 번역 사전 검사, 소스/패치 무결성 테스트.
- 미검증: Rust/Cargo Windows 실제 컴파일, Inno Setup ISCC 컴파일, 설치 GUI 클릭, 실행/업그레이드/제거 실기동.
- **실제 Setup.exe 파일을 배포하는 것이 아닙니다**. 사용자의 Windows 빌드 환경에서 `INSTALL.cmd`를 실행해야 합니다.
- 코드 서명 없음. 다운로드한 설치 프로그램을 타인에게 배포할 때 SmartScreen 경고가 표시될 수 있습니다.
- 원본 FilmCraft의 Cargo 버전 `0.5.0` 유지. `0.5.3`은 이 비공식 패치의 설치 프로그램 버전입니다.
- 일부 기본 설치 프로그램 경고와 오류 문자열은 Inno Setup 기본 영어 문구로 나타날 수 있습니다.
- 한국어 번역은 이전 v0.5.2의 2,876개(스페인어 참조 키 기준 약 74.84%)이며 이번 버전에서 모든 UI가 번역된 것은 아닙니다.
