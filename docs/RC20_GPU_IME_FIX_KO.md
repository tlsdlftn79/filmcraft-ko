# FilmCraft v0.6.0 RC20 — GPU 인코딩과 한글 IME 경고 수정

- `has_ime_edit` 및 `ime_consumes_editor_keys` 테스트 보조 함수를 그래픽 패널 테스트 모듈 안으로 이동하여 일반 라이브러리 빌드에서 미사용 경고가 생길 경로를 없앴습니다.
- AMD AMF / Intel Quick Sync는 **FilmCraft 앱의 내보내기 작업에서** FFmpeg 인코더를 호출합니다. 별도 Python 수작업이 필요하지 않습니다.
- 선택 경로: 빠른 내보내기 → GPU(자동) → AMD AMF / Intel QSV. 기존 NVENC 자동과 CPU 모드 유지.
- 환경: Windows 10/11, PATH에서 `ffmpeg`·`ffprobe` 실행 가능, 지원 GPU·드라이버 및 인코더가 포함된 FFmpeg 빌드.
- 구현 방식은 FFmpeg 하드웨어 백엔드를 내보내기 작업에 통합한 것으로 **AMF/QSV 네이티브 Rust SDK 기반 인코더가 아닙니다.**
- CPU H.264 MP4를 먼저 안전한 임시 경로에 렌더링하고, GPU 변환 → H.264 코덱 검증 → 전체 비디오 디코딩 검증 후 최종 출력에 반영합니다.
- GPU 실패 시 오류를 기록하고 CPU MP4로 대체합니다. 취소 시 FFmpeg 프로세스 종료 후 임시 파일 정리.
- 기본 CPU/NVENC 처리, 일반 큐 내보내기와 외부 Python 진단 도구는 변경하지 않습니다. `file.exportMedia`와 `export.quick`에 `gpuEncoder: amd|intel|auto|cpu` 선택 인수를 추가했습니다.
- FFmpeg 필수 사항과 오류는 앱 사용 전에 확인해야 합니다. 실제 Windows 컴파일/AMD/Intel GPU 출력 성공은 실기기 검증이 필요합니다.

## Windows 테스트

```bat
python scripts\check_rc20_integrated_gpu.py
cargo check --locked -p filmcraft-engine -p filmcraft-ui-egui
cargo test --locked -p filmcraft-ui-egui korean_ime_tests
TEST.cmd
BUILD.cmd
```

FFmpeg 설치 및 인코더 확인:

```bat
ffmpeg -hide_banner -encoders | findstr /i "h264_amf h264_qsv"
ffprobe -version
```

새로운 실행 파일을 사용해야 경고 변경이 적용됩니다.
