# FilmCraft v0.6.0 RC16 — 한국어판 안정화 패치

기준: RC15 전체 소스. 기존 편집·GPU·Shorts·후원 기능을 유지합니다.

## 개선
- Windows 외부 링크 열기: Explorer URL 핸들러 우선, `rundll32 url.dll,FileProtocolHandler` 대체 경로.
- 후원·Discord 버튼 및 도움말·정보 창에서 브라우저 시작 실패를 상태 메시지로 표시하고 URL을 클립보드에 복사.
- 상단 헤더에서 메뉴와 Discord 클릭 영역이 겹치면 버튼을 숨김(도움말 메뉴에서 접근 가능).
- 새 텍스트 레이어 생성·재편집 직후 첫 프레임에 Windows IME 활성화 위치를 전달해 첫 한글 글자 누락 가능성 완화. 기존 포커스·IME 이벤트 경로 회귀 검사 추가.
- RC16 Windows 설치/배포 스크립트 버전 갱신.

## Windows에서 꼭 검증할 내용
1. `TEST.cmd`, `BUILD.cmd`, `INSTALL.cmd` 순서로 실행.
2. 상단 후원 및 Discord, 도움말 메뉴, 정보 창의 링크 클릭. 기본 브라우저가 열리는지 확인.
3. 문자 도구 `안녕하세요 한글 테스트 ABC` 입력. Backspace/Enter/영문 전환 확인.
4. 브라우저가 열리지 않으면 상태 표시 문구 확인 후 클립보드 URL 수동 접속.
5. `FILMCRAFT_IME_DIAGNOSTICS=1` 환경변수로 실행하면 민감한 문자 내용 없이 IME 유형·글자 수를 stderr에 기록.

**주의:** 정적 검사가 실제 Windows 버튼·IME 동작 성공을 보장하지는 않습니다. GPU 인코더의 지원 범위는 RC15와 동일합니다.
