# FilmCraft v0.6.0 RC3 → RC4 업데이트 가이드

이번 ZIP은 **기존 RC3 한국어 전체 소스**를 RC4 소스로 업데이트합니다. RC1이나 다른 버전에 적용하지 마세요.

1. 기존 RC3 폴더와 프로젝트 파일을 먼저 백업합니다.
2. `FilmCraft_v0.6.0_RC3_to_RC4_Update_Patch.zip`을 RC3 소스의 **상위 폴더**에 압축 해제하고 같은 경로의 파일을 덮어씁니다. ZIP 최상위는 `filmcraft-main/`입니다.
3. Rust 1.95 이상, Visual Studio 2022 Build Tools와 Windows SDK가 설치된 Windows x64 환경에서 `TEST.cmd` → `BUILD.cmd`를 실행합니다.
4. `PACKAGE.cmd`로 포터블 ZIP을, Inno Setup 6.3 이상을 설치한 상태에서 `INSTALL.cmd`로 설치 EXE를 생성합니다. `VERIFY.cmd`로 생성한 두 배포 파일을 검사합니다.
5. 반드시 `docs/testing-korean-v060-rc4.md`의 문자 도구, 쇼츠, GPU 인코딩 실기기 테스트를 진행하세요.

> 이 패치는 컴파일 완료 바이너리를 포함하지 않으며, 작성 환경에서 실제 Windows 한글 IME/그래픽카드/설치 프로그램 동작은 검증하지 못했습니다.
