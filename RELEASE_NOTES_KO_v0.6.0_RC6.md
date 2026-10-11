# FilmCraft v0.6.0 RC6 — 비공식 한국어판 후원 버튼

## 주요 변경점

- 상단 헤더에 `한국어판 후원` 버튼 추가: `https://ctee.kr/place/caw`를 시스템 브라우저에서 엽니다.
- 도움말 메뉴에 `한국어 패치 후원…` 추가 (좁은 창에서도 접근 가능).
- 정보 창에 후원 링크와 비공식 커뮤니티 패치라는 안내 추가.
- 기존 링크·동작과 분리하여 공식 ArtCraft 후원 링크로 오인되지 않도록 표기.
- 6개 번역 사전(한국어/일본어/스페인어/포르투갈어/우크라이나어/중국어)에 4개의 새 메시지 번역 추가.
- RC6 포터블·설치 파일명·배포 검사 및 Windows CI 산출물 이름 갱신. 원본 Cargo 버전과 인스톨러 AppId는 변경하지 않음.
- 기존 한국어 IME, 자막, YouTube Shorts, NVENC/CPU 빠른 내보내기 기능은 유지.

## 검증

`python scripts/check_rc6_support.py`와 `python scripts/check_i18n.py` 등을 실행해 링크 연결과 번역 목록을 검증하세요.
Windows Rust 컴파일, 실제 클릭과 브라우저 열림, 설치·제거는 **미검증**입니다. 컴파일된 EXE는 포함하지 않습니다.

## 수정 파일 적용

`FilmCraft_v0.6.0_RC5_Korean_IME_Export_Full_Source.zip` 압축 해제 폴더에 `FilmCraft_v0.6.0_RC5_to_RC6_Update_Patch.zip`을 같은 경로로 덮어쓰기 하세요.
