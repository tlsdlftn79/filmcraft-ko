# FilmCraft v0.6.0 RC9 Windows 검증 체크리스트

RC9 소스 정적 검사는 실제 Windows 동작을 보증하지 않습니다. 이 체크리스트는 **Windows 10/11 x64 직접 확인**을 위한 것입니다.

## 환경 정보 기록

- Windows 빌드 번호:
- Rust `rustc -V`, `cargo -V`:
- GPU 제조사/모델/드라이버 버전:
- 한국어 Microsoft IME 버전:
- `TEST.cmd` 종료 코드:
- `INSTALL.cmd` 및 `VERIFY.cmd` 종료 코드:

## 1. 문자 도구 — 최우선

1. 영상/이미지가 있는 시퀀스에서 문자 도구(T)로 텍스트 레이어 생성
2. 한국어 Microsoft IME로 `안녕하세요`, `한한`, `한글 테스트 123 ABC` 입력
3. 초성·중성 조합 과정에서 텍스트가 저장되거나 중복 표시되지 않는지 확인
4. 한글 조합 중 영문 입력기로 바꿔 `ABC` 입력: 정상 문자 누락 여부 확인
5. 글자 선택·Backspace·Delete·Enter·Esc, 텍스트 레이어 재클릭 및 재진입 확인
6. 프로젝트 저장 → 닫기 → 다시 열기 → 문자 및 커서 위치 확인

**버그 제보 시:** 입력한 문자열, 실제 결과, 입력기 설정, `graphics.rs` 관련 콘솔/로그, 재현 키 순서를 첨부합니다.

## 2. GPU 빠른 내보내기

- Windows에서 GPU 제조사·모델 문자열이 나오더라도 **인코더 지원 검증이 아님**에 유의
- NVIDIA GPU: NVENC 드라이버 감지/인코딩 시도/실제 결과 파일/CPU 폴백 확인
- AMD/Intel GPU: RC9은 AMF/QSV **미구현**이므로 CPU 소프트웨어 인코딩 결과 확인
- GPU(자동) / CPU 각각 한글 파일명(`한글 쇼츠.mp4`)으로 10초 영상 출력 후 재생
- 작업 관리자 GPU 인코딩 엔진 사용량 또는 별도 드라이버 도구로 **실제** 하드웨어 가속 여부를 추가 검증

## 3. Shorts MP4 검사

유튜브 쇼츠 1080×1920 (9:16) 빠른 내보내기 이후:

```bat
python scripts\verify_shorts_mp4.py "D:\Videos\한글 쇼츠.mp4"
```

검사 도구는 `ffprobe`(FFmpeg 설치)를 사용해 1080×1920 H.264, 음성이 있으면 AAC, FPS·길이·샘플 종횡비를 확인합니다. **하드웨어 인코딩 사용 여부나 화질·한글 자막 픽셀 정확성을 판정하지 않습니다.** 영상 미리보기도 직접 확인해야 합니다.

## 4. 설치 프로그램

```bat
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
```

설치·업그레이드·삭제를 실제 Windows에서 테스트하고, 제거 후 사용자 프로젝트·설정 보존 여부를 확인하세요. 정상적인 ZIP 구조 검사만으로 Windows 설치 성공을 주장하지 마세요.
