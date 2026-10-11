# FilmCraft v0.6.0 RC21 — GPU 내보내기 안정화

## 변경 사항

- **FFmpeg 오류 로그 보존:** FFmpeg의 stderr를 별도 스레드에서 끝까지 읽으면서 마지막 8KB만 저장합니다. 오류가 나면 종료 코드와 함께 원인을 기록합니다.
- **검사 취소 지원:** `ffprobe`도 취소 플래그를 확인하는 자식 프로세스 관리 함수로 실행합니다. 내보내기 종료를 기다리지 않고 취소를 처리할 수 있습니다.
- **CPU 출력 안전성:** 없는 파일·빈 CPU 출력은 거부하고, GPU 변환에 실패한 경우 CPU 출력 결과를 보존합니다.
- **기존 출력 보존:** 파일 교체 실패 시 원래 목적지 파일 복구를 확인하는 Rust 테스트를 추가했습니다.
- **기존 기능 유지:** 한국어 입력, 자막, Shorts 9:16, 후원·Discord, NVENC, 외부 FFmpeg AMF/QSV, Windows 설치 프로그램.

## Windows 테스트

```bat
python scripts\check_rc21_gpu_reliability.py
cargo check --locked -p filmcraft-engine
cargo test --locked -p filmcraft-engine hardware_transcode
cargo check --locked -p filmcraft-ui-egui
TEST.cmd
BUILD.cmd
INSTALL.cmd
VERIFY.cmd
```

AMD AMF / Intel QSV는 FFmpeg·GPU·드라이버가 지원하는 Windows 환경에서 실물 파일을 내보내고 검증해야 합니다. 이 ZIP에는 컴파일된 EXE가 없습니다.

**상태:** 소스 검사 및 패키징 검사 수행. Rust 컴파일, Windows GUI, GPU 성능·동작은 미검증.
