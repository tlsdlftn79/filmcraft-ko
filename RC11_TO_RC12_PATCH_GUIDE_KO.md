# FilmCraft v0.6.0 RC11 → RC12 업데이트 안내

본 패치는 **FilmCraft v0.6.0 RC11 Korean 전체 소스** 전용입니다. 기존 소스 디렉터리 구조가 바뀌지 않도록 ZIP 안의 `filmcraft-main/` 내용을 같은 위치에 덮어쓰세요. 다른 RC 버전에는 덮어쓰지 말고 RC12 전체 소스 ZIP을 사용하세요.

## 업데이트 내용

1. 문자 도구에서 한글 IME 이벤트 유형·문자 수·포커스만 기록하는 `FILMCRAFT_IME_DIAGNOSTICS=1` 진단(기본 꺼짐).
2. IME DeleteSurrounding에서 비정상 UTF-8 커서 위치를 안전하게 보정.
3. FFmpeg GPU 인코더 진단: H.264 MP4 출력의 24개 디코딩 프레임 및 전체 디코딩 검사.
4. 설치 프로그램 및 빌드 출력 이름을 RC12로 갱신, 관련 회귀 테스트 보강.

## 빌드·테스트

```bat
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
```

## 한글 입력 진단(선택)

```bat
set FILMCRAFT_IME_DIAGNOSTICS=1
target\release\filmcraft.exe 2> ime-rc12.log
```

로그는 원문을 출력하지 않지만, 외부 공유 전에 전체 로그의 다른 항목을 검토하세요.

## GPU 외부 시험

```bat
python scripts\probe_h264_gpu.py --encoder all --json
```

**중요:** 외부 FFmpeg 시험이 성공하더라도 FilmCraft 자체 AMD AMF/Intel QSV 인코딩은 아직 구현된 상태가 아닙니다. Rust/Windows 실제 컴파일과 설치·입력 검증은 Windows 장치에서 추가 수행해야 합니다.
