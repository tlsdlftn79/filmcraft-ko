# FilmCraft v0.6.0 RC12 — 한글 입력 진단 및 GPU 내보내기 검증 강화

기준: v0.6.0 RC11 전체 소스. 기존 UI, 한국어 번역, 자막, YouTube Shorts, 크티 후원 버튼 및 Windows 설치 프로그램 기능 유지.

## 실제 코드 변경

- 문자 도구에 `FILMCRAFT_IME_DIAGNOSTICS=1` 진단 옵션 추가. 기본값은 꺼짐. `IME Preedit / Commit / DeleteSurrounding / Text / Paste` 이벤트의 **유형과 글자 수** 및 편집 포커스 상태만 출력하며, 실제 입력한 문장은 로그에 남기지 않음.
- 잘못된 UTF-8 바이트 위치에서 `DeleteSurrounding`이 전달되었을 때 문자 경계로 복원한 후 처리하도록 개선. IME 삭제 길이는 Unicode scalar 기준을 준수.
- 회귀 테스트: 진단 로그에 원문이 없음을 확인, 잘못된 커서 바이트 위치, 빈 삭제 요청.
- FFmpeg GPU 시험 인코딩의 성공 판정 강화: `ffprobe -count_frames`로 24프레임을 확인하고 별도의 전체 H.264 디코딩 검사를 통과해야 통과로 판정.
- Windows 패키지 이름·Inno Setup 채널·CI 아티팩트 버전 RC12 갱신.

## Windows 실행 명령

```bat
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
```

한글 입력 진단은 Windows 명령 프롬프트에서 다음처럼 실행합니다.

```bat
set FILMCRAFT_IME_DIAGNOSTICS=1
target\release\filmcraft.exe 2> ime-rc12.log
```

로그는 이벤트 유형과 문자 **개수**만 표시하지만, 환경/시스템에 관한 다른 로그가 포함될 수 있으므로 외부 공유 전 검토하세요.

외부 FFmpeg GPU 시험:

```bat
python scripts\probe_h264_gpu.py --encoder all --json
python scripts\probe_h264_gpu.py --encoder intel --require
```

## 아직 미완료 / 검증 한계

- Windows 실제 한글 IME 편집·자막 렌더링 테스트: **미실행**.
- Rust MSVC 컴파일/설치/내보내기 실기기 테스트: **미실행**.
- Media Foundation AMD AMF/Intel QSV **FilmCraft 자체 인코딩 구현은 없음**. 현재는 장치·인코더 후보 조회, 외부 FFmpeg 시험 도구까지이며, 두 결과를 혼동하지 마세요.
- RC12는 정식 안정판이 아니며 FFmpeg 시험 통과만으로 실제 FilmCraft GPU 인코딩을 보장하지 않습니다.
