# FilmCraft v0.6.0 RC11 — 한국어 문자 도구 및 GPU 진단

## 수정 내용

- 문자 도구에서 기존 텍스트 레이어를 클릭해 편집하거나 새 텍스트 레이어를 만든 **같은 프레임**에 키보드 포커스를 한 번 요청합니다. 다음 프레임마다 포커스를 재요청하는 방식은 사용하지 않습니다.
- 한글 IME 확정·분할 에코·영문 동시 입력과 다른 Source Text 입력창의 포커스 보존을 위한 Rust 테스트를 추가했습니다.
- FFmpeg/ffprobe가 설치된 컴퓨터에서 NVIDIA NVENC / AMD AMF / Intel Quick Sync의 H.264 인코딩 및 MP4 스트림을 검증하는 **선택적 진단 도구** `scripts/probe_h264_gpu.py`를 추가했습니다.
- `TEST.cmd`에 RC11 정적 검사 및 진단 도구의 독립 유닛 테스트를 추가했습니다. 실제 GPU 시험 인코딩은 `FILMCRAFT_TEST_GPU_ENCODERS=1`로 선택 실행합니다.
- Windows 설치 프로그램, 포터블 파일명, 검사 도구 버전을 RC11로 갱신했습니다.

## 선택적 GPU 인코딩 테스트

```bat
python scripts\probe_h264_gpu.py --self-test
python scripts\probe_h264_gpu.py --encoder all
python scripts\probe_h264_gpu.py --encoder amd --require
python scripts\probe_h264_gpu.py --encoder intel --require
python scripts\probe_h264_gpu.py --encoder all --json
```

`--require`는 요청한 인코딩이 실패하거나 사용 불가능하면 종료 코드 1을 돌려줍니다. FFmpeg나 ffprobe가 없으면 종료 코드 2입니다. 출력 파일은 임시 폴더에서 테스트한 후 삭제됩니다.

### 중요한 범위 제한

- 이 도구는 **외부 FFmpeg를 통한 시험 인코딩**입니다. FilmCraft 자체 인코더 등록, Media Foundation 패킷 생성 또는 AMF/QSV 내보내기 경로와 연결된 것은 아닙니다.
- 기존 FilmCraft의 H.264 GPU 자동 인코딩은 Windows에서 NVIDIA NVENC만 사용합니다. AMD/Intel에서는 CPU로 대체됩니다.
- Rust 컴파일, 실제 Windows IME 입력, 실제 GPU 장치 테스트, 실제 설치·업데이트·제거는 현재 환경에서 수행되지 않았습니다.
- 수정에 따른 기능 안정성을 확정하려면 Windows 사용자가 `TEST.cmd`, `BUILD.cmd`, `INSTALL.cmd`, 그리고 문자 도구 테스트를 실행해야 합니다.
