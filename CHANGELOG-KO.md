# FilmCraft 한국어판 변경 이력

## v0.6.0 Stable — 2026-10-11 (소스 배포 준비)

- 실제 Rust workspace 패키지 버전과 Cargo.lock의 49개 로컬 패키지를 0.6.0으로 통일.
- Inno Setup, Windows CLI 빌드, 포터블 ZIP, GitHub Actions 배포 파일명을 `0.6.0_Stable`로 통일.
- 소스·설치·포터블 버전 일치성을 검사하는 Stable release gate 추가.
- `VERIFY.cmd`에서 배포 산출물의 SHA-256·크기·검사 범위를 JSON manifest로 작성.
- RC 시점의 오래된 README를 별도 보존하고 Stable 안내서·수락 기준 정리.
- 기존 한글 IME, 자막·Shorts, NVENC, FFmpeg 기반 AMD AMF / Intel QSV, 파일 보호 동작 유지.

**검증 범위:** 사용자는 11/11 항목의 Windows 통과를 보고했으나, 이 소스 배포 준비 환경에서는 Windows/MSVC와 실기기 검증을 독립 재현하지 않았습니다. 최종 EXE 설치·배포는 Windows에서 `TEST.cmd → BUILD.cmd → PACKAGE.cmd → INSTALL.cmd → VERIFY.cmd`를 실행해 확인해야 합니다.

## v0.6.0 RC22

- GPU 출력 파일 복구 실패 시 기존 출력과 CPU 임시 파일 보호 강화.

## v0.6.0 RC20–RC21

- 한글 IME 테스트 전용 함수 경고 정리.
- FFmpeg 기반 AMD AMF·Intel QSV 내보내기 후처리 연결, 취소·검사·오류 진단 보강.

## v0.6.0 RC16–RC19

- 외부 후원·Discord 링크 상태 안내, 한국어 IME 포커스 처리 보완.
- 빠른 내보내기·대기열의 Windows 파일명·경로 검사 강화.
