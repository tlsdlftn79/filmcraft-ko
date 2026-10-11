# RC7 Windows 실기기 검증 체크리스트

Rust 1.95+, Visual Studio 2022 MSVC Build Tools, Python 3, Inno Setup 6.3+가 설치된 Windows 10/11 x64에서 진행하세요.

## 1. 문자 도구

1. 문자 도구(T)로 영상에 새 텍스트를 만들고 `안녕하세요 한국어 테스트`를 입력합니다.
2. 조합 중 밑줄 표시를 확인하고, 확정 후 문자가 중복되지 않는지 확인합니다.
3. 속성 패널의 Source Text에 포커스를 옮깁니다. 이후 영상의 같은 텍스트 레이어를 클릭해서 `다시 입력`을 붙여 봅니다.
4. `한국한국`, `Hello한글123`, `한😀글`을 입력하고 Backspace / 방향키를 확인합니다.
5. 프로젝트를 저장한 뒤 다시 열어서 텍스트가 그대로인지 확인합니다.
6. SRT를 불러온 뒤 MP4로 내보내 미리보기와 동일한지 확인합니다.

## 2. CPU/GPU 내보내기

1. 빠른 내보내기 → YouTube Shorts 1080×1920 프리셋, H.264 / 9:16을 선택합니다.
2. CPU 소프트웨어 인코딩 및 GPU 자동을 각각 테스트합니다.
3. Windows NVIDIA NVENC 드라이버가 없는 경우 GPU 자동은 CPU로 대체되는지 확인합니다.
4. NVIDIA를 쓰는 PC에서 NVENC 실제 사용을 검사하려면 `set FILMCRAFT_TEST_NVENC=1` 후 `TEST.cmd`를 실행합니다.
5. AMD 및 Intel 환경은 현재 AMF/QSV 전용 인코딩을 지원하지 않습니다. GPU 렌더링 체크박스는 별도의 기능입니다.

## 3. 빌드·배포

```bat
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
```

설치 후 시작 메뉴 바로가기·설치 경로·제거·기존 설정 보존을 직접 확인합니다.
`VERIFY.cmd`는 체크섬과 구성만 검사하며 실제 실행 테스트를 대체하지 못합니다.
