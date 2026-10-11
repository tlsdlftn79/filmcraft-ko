# FilmCraft v0.6.0 RC18 — Windows 검증 안내

이번 버전은 `RC17`에서 다음 부분을 수정했습니다.

1. 빠른 내보내기에서 빈 파일명, Windows 예약 이름(CON/NUL/COM1 등), 사용 불가능한 문자가 들어간 이름을 내보내기 명령 전에 차단합니다. 대화상자는 열린 상태를 유지하며, 한글 파일명은 그대로 사용할 수 있습니다.
2. 한국어 오류 문구와 Rust 회귀 테스트를 추가했습니다.
3. Windows 설치형/포터블 배포 버전과 GitHub Actions 아티팩트명을 RC18으로 맞췄습니다.
4. 실제 Windows 실기기 점검용 **읽기 전용** 스모크 테스트를 추가했습니다.

## 빌드·검사

```bat
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
```

## 실제 Windows 검사

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\rc18-windows-smoke.ps1 -Launch
```

실행 파일 탐색, 설치 등록 상태, 시작 메뉴 바로가기 존재 여부를 보고서에 기록합니다. `-Launch`는 앱만 실행하며 **설치하거나 제거하지 않습니다**. `build-logs\rc18-windows-smoke.txt`의 수동 점검표로 한글 IME, 후원/Discord 버튼, Shorts 내보내기, 인코딩 기능을 직접 확인하세요.

이 환경에서는 Windows Rust MSVC 빌드, 브라우저 클릭, 한글 IME, Windows 설치를 실제로 확인하지 못했습니다. Python 정적 검사는 해당 기능의 실기기 성공을 보장하지 않습니다.

정상화 조건: Windows Release 빌드 및 Rust 단위 테스트 통과, 문자 도구 한글 조합/확정/삭제 성공, 설치/업그레이드/제거, Shorts H.264 MP4 출력·재생 검증.
