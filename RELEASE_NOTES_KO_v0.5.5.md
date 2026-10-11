# FilmCraft Korean Patch v0.5.5 — 한글 텍스트·자막 안정화

## 수정된 코드

1. 영상 미리보기 편집의 `Event::Text` 중복 처리를 IME 이벤트와 분리해 한글 중복 입력 방지.
2. 글자 삭제 및 좌우 이동을 Unicode grapheme cluster 단위로 변경해 분해 자모와 이모지 조합 손상 방지.
3. IME 주변 글자 삭제는 scalar 단위로 처리하여 egui-winit의 이벤트 계약 유지.
4. 저장된 커서/선택 바이트 위치가 글자 중간을 가리켜도 패닉 없이 경계로 이동.
5. 실제 이벤트 처리 함수를 Rust 단위 테스트로 검증하는 코드 추가.
6. SRT·WebVTT 한글, 개행, UTF-8 BOM/CRLF 문서 왕복 테스트 추가.
7. Windows 빌드 테스트 스크립트에 자막 및 구조적 회귀 검사 추가.
8. 한국어 사용자별 Inno Setup 설치 프로그램 소스 버전을 v0.5.5로 반영.

## 이전 기능 유지

- 기존 한국어 번역 2,876개, 언어 설정 저장·자동 감지, 폰트 폴백.
- Windows 설치/제거 소스와 BUILD/TEST/INSTALL/PACKAGE 명령.
- 기존 원본 프로젝트·자막·영상 편집 기능.

## 테스트 결과 (개발 환경)

- Python: `check_i18n.py`, `check_korean_input.py`, `check_korean_stability.py`, `check_installer.py` 통과.
- Rust 단위 테스트, Windows GUI 실사용, 설치 EXE 생성, 한글 영상 내보내기 **미검증** (`cargo` 및 Windows 환경 없음).

## 후속 과제

- 실제 Windows 한국어 IME(마이크로소프트 옛/새 입력기)에서 테스트.
- 자막 텍스트 모양, 폰트 커버리지 및 내보내기 프레임 육안 확인.
- 미번역 880개 기준 UI 키 검토.
