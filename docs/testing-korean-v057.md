# FilmCraft v0.5.7 — Windows 실제 검증 체크리스트

검증 PC: Windows 10/11 x64, 한국어 Microsoft IME 설치, Rust 1.95+/MSVC, Inno Setup 6.3+

## 1. 빌드
- [ ] `TEST.cmd` 성공(소스/폰트/자막 Rust 단위 테스트 포함)
- [ ] `BUILD.cmd` 완료 및 `target\release\filmcraft.exe` 실행
- [ ] `INSTALL.cmd` 완료 및 `dist\FilmCraft_v0.5.7_Korean_Windows_x64_Setup.exe` 생성
- [ ] Setup.exe 보안 서명/배포 전 SmartScreen 정책 확인(기본 미서명)

## 2. 한국어 IME 및 자막
- [ ] 언어를 한국어로 설정 후 앱 재시작, 한국어 유지
- [ ] Program Monitor 텍스트 도구에서 '안녕하세요' 실시간 입력
- [ ] '한글ABC123', 영문/한글 전환, 한영 키 입력 반복
- [ ] IME 한글 조합 중 Escape / Backspace / Enter 동작 확인
- [ ] IME 종료 직후 라틴 문자 및 Delete/방향키 동작 확인
- [ ] Ctrl+A, 붙여넣기, 한국어 선택 영역 교체, 삭제 동작 확인
- [ ] 분해 자모/이모지 조합의 삭제가 문자를 쪼개지 않는지 확인
- [ ] SRT/WebVTT 한글·UTF-8 BOM·CRLF 자막 가져오기
- [ ] 띄어쓰기 없는 긴 자막 줄바꿈 및 글꼴 대체 확인
- [ ] 실제 출력한 MP4에서 한글 글리프/위치/줄바꿈 확인

## 3. 설치 (테스트용 VM 또는 별도 PC 권장)
- [ ] 기존 공식 FilmCraft MSI와 한국어 패치 설치가 충돌하지 않는지 확인
- [ ] 사용자 권한으로 한국어 설치 마법사 실행
- [ ] 시작 메뉴/바탕화면 바로가기 선택 동작
- [ ] 설치된 GUI 실행, CLI `--help` 확인
- [ ] 기존 v0.5.6 한국어 패치가 있다면 업그레이드 설치 확인
- [ ] Windows 설정의 설치된 앱에서 제거 가능 확인
- [ ] 제거 후 사용자가 만든 프로젝트/설정이 유지되는지 확인
- [ ] 영문 설치 마법사 전환 확인

실패 시 Windows 버전, `TEST.cmd`/`INSTALL.cmd` 출력, 입력 방식과 재현 단계를 기록해 주세요.
