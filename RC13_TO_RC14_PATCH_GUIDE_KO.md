# FilmCraft v0.6.0 RC14 — 한국어 문자 도구 및 GPU 후처리

기준: **RC13 전체 소스**. 변경 파일만 담긴 ZIP을 RC13 소스 루트에 덮어쓰거나, RC14 전체 소스 ZIP을 사용하십시오. 실행 파일 및 설치 EXE는 포함하지 않습니다.

## 주요 변경

1. 문자 도구에서 IME 확정 뒤 같은 프레임에 Home/End/위·아래 화살표를 누를 때, 갱신 이전의 레이아웃 대신 현재 편집 중인 텍스트 레이아웃으로 이동 위치를 계산합니다.
2. 한글 조합 자모, 이모지, 영문 혼합 선택·삭제에 대한 Rust 테스트 4개를 추가했습니다.
3. **별도 외부 도구** `scripts/gpu_mp4_transcode.py` 추가: FilmCraft가 이미 내보낸 MP4를 FFmpeg의 NVIDIA NVENC / AMD AMF / Intel QSV / CPU H.264로 다시 인코딩합니다. 원본 파일을 덮어쓰지 않으며 출력 파일의 코덱·해상도·전체 디코딩을 확인한 뒤 게시합니다. 오디오와 자막 스트림 보존도 검사합니다.
4. 인코더 구동 실패는 명시적으로 보고합니다. CPU로 자동 전환하려면 `--allow-cpu-fallback`을 추가해야 합니다.
5. 기존 Windows 설치 및 포터블 빌드 파일 이름을 RC14로 갱신했습니다.

## GPU 인코딩 (독립 후처리 기능)

Windows에서 FFmpeg/ffprobe를 `PATH`에 설치한 뒤, FilmCraft로 먼저 MP4를 내보냅니다.

```cmd
python scripts\gpu_mp4_transcode.py "기존 내보내기.mp4" "AMD 출력.mp4" --encoder amd --bitrate-kbps 12000
python scripts\gpu_mp4_transcode.py "기존 내보내기.mp4" "Intel 출력.mp4" --encoder intel --bitrate-kbps 12000
python scripts\gpu_mp4_transcode.py "기존 내보내기.mp4" "쇼츠 출력.mp4" --encoder auto --shorts --allow-cpu-fallback
```

**주의:** 이 도구는 FilmCraft 내부의 빠른 내보내기 GPU 인코더 연결을 완성한 것이 아닙니다. FilmCraft 내부 AMD/Intel 통합에는 Media Foundation/FFmpeg 인코더 패킷을 `VideoEncoder`에 제공하는 별도의 후속 개발과 Windows GPU별 실제 검증이 필요합니다. FFmpeg를 설치했더라도 AMD·Intel GPU의 하드웨어 드라이버가 지원하지 않으면 인코딩이 실패할 수 있습니다.

## Windows 검증

```cmd
python scripts\test_rc14_gpu_transcode.py
python scripts\check_rc14_features.py
cargo test --locked -p filmcraft-ui-egui korean_rc14_selection_tests
cargo check --locked -p filmcraft-platform
TEST.cmd
BUILD.cmd
INSTALL.cmd
```

이 소스의 실제 Windows 컴파일 및 GPU 인코딩 성공은 아직 확인되지 않았습니다.
