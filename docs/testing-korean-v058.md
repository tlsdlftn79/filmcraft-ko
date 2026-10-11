# FilmCraft v0.5.8 Windows 실기기 QA 체크리스트

테스트 대상: Windows 10/11 x64, Rust MSVC 및 Visual Studio 2022 SDK, Inno Setup 6.3+, 한국어 Microsoft IME.

## 빌드 및 PE 검사
- [ ] `py -3 scripts\test_installer_pe.py` 실행 성공
- [ ] `TEST.cmd`에서 Rust 단위 테스트 및 `cargo check` 통과
- [ ] `BUILD.cmd`에서 GUI/CLI x64 PE32+ Subsystem 검증 통과
- [ ] `INSTALL.cmd`로 `dist\FilmCraft_v0.5.8_Korean_Windows_x64_Setup.exe` 생성
- [ ] `PACKAGE.cmd`로 포터블 ZIP 생성, `filmcraft.exe`, `filmcraft-cli.exe`, `portable.txt` 포함
- [ ] `Get-FileHash -Algorithm SHA256` 값이 옆의 `.sha256` 파일과 일치

## 설치/업데이트/제거
- [ ] 관리자 권한 없는 사용자 계정에서 새 설치 테스트
- [ ] 이전 v0.5.7 설치판 위로 업그레이드 설치 확인
- [ ] 한국어·영어 설치 UI 선택 및 바탕화면 바로가기 동작
- [ ] 설치된 프로그램 실행, `filmcraft-cli.exe --help` 동작
- [ ] 삭제 후 사용자 프로젝트·자막·설정 데이터 유지
- [ ] 기존 공식 MSI 설치와 앱/바로가기/설치 경로가 분리되는지 검증

## 한글 편집 및 출력
- [ ] 프로그램 텍스트 도구에서 `안녕하세요 한글ABC123` 입력
- [ ] 한국어 IME 조합/확정, Backspace, Escape, 한영 전환
- [ ] 분해 자모·이모지 단위 선택/삭제 확인
- [ ] 긴 한글 자막 SRT·WebVTT 불러오기/내보내기
- [ ] 영상 미리보기와 MP4 렌더 결과의 한글 폰트 및 줄바꿈 비교
- [ ] 재시작 후 한국어 UI 언어 설정 유지

**기록**: Windows 버전, Rust 버전, 설치 도구 버전, 테스트 출력 및 실패 시 화면/재현 단계를 기록합니다.
