# FilmCraft v0.6.0 RC7 — 한국어 편집과 빠른 내보내기 개선

개발 기준: **v0.6.0 RC6 전체 소스**. RC7 ZIP 패치는 RC6 전용입니다.

## 실제 수정

1. 영상 텍스트 편집 도중 다른 속성 입력창으로 포커스가 넘어갔다가 영상 화면의 **동일 텍스트 레이어를 클릭**해도 포커스가 돌아오지 않아 타이핑이 되지 않는 경로 수정.
2. IME의 `Commit` 문자열이 여러 `Event::Text` 조각으로 중복 전달될 경우 각각의 접두어를 한 번만 소비하도록 변경. 한글 반복 입력 보호.
3. Windows 빠른 내보내기의 GPU 자동 선택에 대해 NVIDIA NVENC 지원 범위·AMD/Intel CPU 폴백을 명확히 표시.
4. RC7 빌드·설치·포터블 배포 파일명 및 체크섬 검사 설정으로 갱신.
5. 정적 회귀 검사와 선택적 NVENC 내보내기 통합 테스트 실행 경로 추가.

## 미완료 및 검증 조건

- Windows MSVC Release 실제 빌드 성공 **미확인**.
- Windows 한국어 IME 실기기 입력 성공 **미확인**.
- AMD AMF·Intel Quick Sync 인코더 구현 **미완료** (기존 NVIDIA NVENC/CPU 폴백 유지).
- NVENC 실기기 인코딩, MP4 자막, 설치·제거 **미확인**.

실제 Windows에서 `TEST.cmd`, `BUILD.cmd`, `INSTALL.cmd`, `VERIFY.cmd` 및 한글 입력을 확인해야 안정판으로 승격할 수 있습니다.
