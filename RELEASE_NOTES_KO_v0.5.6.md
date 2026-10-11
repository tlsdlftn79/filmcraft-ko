# FilmCraft Korean Patch v0.5.6 — IME & Caption Stability

## 실제 수정

1. 동일 프레임의 IME Commit과 `Event::Text`가 일치하는 경우에만 중복을 제거하도록 처리 범위를 축소했습니다. 다른 키보드 문자열은 보존합니다.
2. IME Disabled 이후 영문 입력이 누락되는 상황을 대상으로 회귀 테스트를 추가했습니다.
3. 단어 단위 커서 이동도 Unicode grapheme 경계에서 끝나도록 보완했습니다.
4. 긴 띄어쓰기 없는 한국어/CJK 자막은 grapheme 경계에서 자동 줄바꿈하도록 구현했습니다. 분해 자모와 ZWJ 이모지 조합의 문자열 경계 검증 테스트를 추가했습니다.
5. `filmcraft-captions`의 `unicode-segmentation` 의존성과 `Cargo.lock`을 함께 갱신했습니다.
6. Windows 빌드/설치 파일 버전 및 정적 검사를 v0.5.6에 맞췄습니다.

## 보존

- v0.5.5 한국어 번역 2,876개 항목과 기존 편집 기능
- Windows 설치 프로그램(관리자 권한 없는 설치·제거) 및 자동 빌드 스크립트

## 검증

- Python 번역/IME/자막/설치 정적 검사: 패키지 생성 환경에서 실행
- Rust/Windows GUI/IME/영상 렌더링/실제 Setup.exe 컴파일: **미검증**
- 880개 미번역 기준 UI 키: **미완료**

다음: `docs/testing-korean-v056.md`의 Windows 수동 검증을 실시하고 나온 로그에 따라 수정할 것.
