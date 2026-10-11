# FilmCraft v0.6.0 RC9 — 한국어 IME 및 GPU 진단

## RC8 대비 변경사항

1. 문자 도구의 `text_is_ime_echo`가 Preedit가 있다는 이유만으로 관계없는 `Event::Text`를 모두 무시하는 로직을 수정했습니다. 이제 **일치하는 조합 후보/Commit만 중복 이벤트로 처리**합니다. 동일 프레임 내 한글·영문 입력 순서와 IME 취소 후 영문 입력을 검증하는 Rust 테스트 4개를 추가했습니다.
2. Windows DXGI 그래픽 어댑터 비동기 탐색을 추가했습니다. NVIDIA/AMD/Intel PCI 벤더 및 그래픽카드 이름을 빠른 내보내기에 표시하지만, **GPU가 감지되었다고 인코딩 지원을 의미하지 않습니다.**
3. NVIDIA NVENC가 지원되는 설정에서만 기존 GPU 인코딩을 시도하며, AMD AMF/Intel Quick Sync는 여전히 구현되지 않았습니다. 미지원 환경에서는 기존 H.264 CPU 폴백을 유지합니다.
4. `scripts/verify_shorts_mp4.py`를 추가해 실제 Shorts MP4의 H.264, 1080×1920, AAC(오디오가 있는 경우), 길이 및 프레임레이트를 `ffprobe`로 검사할 수 있습니다.
5. Windows 설치·포터블 ZIP 파일명과 배포 검증 설정을 RC9로 갱신했습니다.

## Windows 테스트

```bat
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
python scripts\verify_shorts_mp4.py --self-test
python scripts\verify_shorts_mp4.py "D:\Videos\내 쇼츠.mp4"
```

**검증 한계:** Linux 환경에서 Python 정적 검사 및 검사기 단위 테스트만 실행했습니다. Rust/Windows 컴파일, 실제 IME, AMD/Intel/NVIDIA GPU와 MP4 편집기 출력 테스트는 **미검증**입니다. 이 단계는 정식 안정판이 아닙니다.
