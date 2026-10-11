# FilmCraft 비공식 한국어 패치 v0.5.4 — KoreanIMEFix

## 수정
- Program Monitor 텍스트 도구: IME 조합(Preedit)과 확정(Commit) 구분; 화면에 조합 표시, 확정 후 명령 실행
- IME 후보 선택 중 키 입력이 텍스트 커서 이동·삭제·편집 종료로 중복 처리되는 문제 완화
- Unicode 글자 단위 주변 문자 삭제, UTF-8 문자열 선택 영역 교체
- 한글 영상 텍스트 렌더링: UI 언어가 영어여도 설치된 Windows 시스템 한글 폰트 폴백
- Essential Graphics 원본 텍스트 위젯 ID 안정화
- Windows Installer 버전 및 생성물 경로 업데이트

## 검사
- Python 정적 코드 계약 테스트·번역/설치 검사
- Rust 한국어 IME 상태 전이·엔진 문자열 라운드트립·폰트 테스트 코드 작성

## 미검증
- Windows MSVC cargo 실제 컴파일 및 회귀 테스트 실행
- Windows IME 후보 표시 위치·실제 키 입력·영상 렌더 및 내보내기
- Inno Setup 설치 파일 실컴파일·설치·제거

## 적용
- 전체 소스 ZIP 사용 또는 **v0.5.3 한국어판 전체 소스** 위에 변경 파일 전용 패치 ZIP 덮어쓰기
- CMD: TEST.cmd / BUILD.cmd / INSTALL.cmd
