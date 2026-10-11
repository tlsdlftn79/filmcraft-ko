# FilmCraft 한국어 패치 v0.5.1 변경 이력

## 포함
- v0.5.0 한국어 번역 및 기존 다국어 선택 기능 유지
- `Kore`로 선언된 사용자 지정 글꼴의 실제 한글 글리프 확인: 불완전한 경우 시스템 글꼴 사용
- 한국어 시스템 로캘 변형 회귀 테스트
- egui 주요 폰트 패밀리 한글 폴백 등록 검사
- BUILD.cmd / TEST.cmd / PACKAGE.cmd (Windows PowerShell 오케스트레이션)
- 6개 언어 사전 정적 검사 도구 (Python 표준 라이브러리)
- 한국어 빌드 및 문제 해결 안내 문서

## 검증 현황
- 번역 사전 및 파일 통합 정적 검사: PASS (Python 실행)
- 압축 무결성 검사: ZIP 패키징 이후 검사
- Rust cargo test / cargo check / cargo build: NOT RUN (해당 실행 환경에 Rust 설치되어 있지 않음)
- Windows GUI / 실제 영상 편집 / 내보내기: NOT RUN

## 적용 및 배포
전체 소스 ZIP은 압축을 풀고 `filmcraft-main\\TEST.cmd`,
`filmcraft-main\\BUILD.cmd`를 실행합니다.
기존 v0.5.0 패치 적용 소스는 추가 패치 ZIP으로도 업데이트할 수 있습니다.
Rust 의존성 업데이트를 강제하지 않도록 Cargo.lock과 workspace 버전은 변경하지 않았습니다.
