# FilmCraft 한국어판 v0.6.0 RC4 개발 변경사항

## 우선 수정: 문자 도구 한글 입력
- `graphics.rs`에서 편집 중인 텍스트 위젯에 매 프레임 반복되던 `request_focus` 제거
- 처음 진입했을 때만 포커스를 요청하여 Windows IME 조합 중단 가능성을 해결
- 다른 입력창에 포커스가 넘어가면 해당 입력 이벤트를 문자 도구가 재처리하지 않도록 분리
- IME 커서 위치 출력도 실제 포커스가 있을 때로 제한
- Rust 포커스 회귀 테스트 1개 추가(Windows IME 실제 테스트는 아직 필요)

## 빠른 내보내기
- YouTube Shorts 1080×1920(9:16) 프리셋: H.264 MP4, 12 Mbps 목표/16 Mbps 최대, AAC 스테레오 48 kHz, 원본 프레임 속도 유지. 전체 화면 채움(가로 영상은 크롭됨).
- 3분 초과 길이에 대한 안내
- CPU(소프트웨어), GPU(자동 하드웨어 인코더), GPU 효과 합성 별도 선택
- 기존 Windows NVIDIA NVENC, macOS VideoToolbox 경로에 연결, GPU 인코딩 불가 시 CPU 폴백
- AMD AMF와 Intel QSV 인코더 신규 구현이나 복수 GPU 선택 기능은 포함하지 않음

## 검증
- 번역 키/설치/PE/배포 정적 검사 및 ZIP 검사 예정
- 미검증: Rust Cargo 실제 빌드, Windows IME, GPU 인코딩 속도, MP4 실영상 내보내기, Windows 설치 EXE
