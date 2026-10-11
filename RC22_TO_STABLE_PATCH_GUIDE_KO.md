# RC22 → v0.6.0 Stable 업데이트 패치 적용 방법

이 패치는 `FilmCraft_v0.6.0_RC22_GPU_Recovery_Full_Source.zip`에서 출발하는 **소스코드 업데이트**입니다. 설치된 Windows 프로그램의 바이너리 패치가 아닙니다.

1. RC22 전체 소스 ZIP의 `filmcraft-main` 폴더를 압축 해제합니다.
2. `FilmCraft_v0.6.0_RC22_to_Stable_Source_Patch.zip`의 `filmcraft-main/` 파일을 **같은 폴더에 덮어씁니다**.
3. `python scripts/check_stable_release.py`를 실행하고 Stable 소스 버전 일치를 검사합니다.
4. Windows x64에서 `TEST.cmd`, `BUILD.cmd`, `PACKAGE.cmd`, `INSTALL.cmd`, `VERIFY.cmd` 순서로 실행합니다.
5. `dist/`에 생성된 Stable 설치판, 포터블판, SHA-256 및 JSON 배포 목록을 확인합니다.

Rust `Cargo.toml`과 `Cargo.lock`이 모두 0.6.0으로 변경됐습니다. `INSTALL.cmd -SkipBuild`는 이전 RC22 실행 파일을 잘못 재포장하지 않도록 최신 빌드의 해시·소스 지문을 검사합니다. 이전 빌드와 섞이면 `BUILD.cmd`를 먼저 실행하세요.

사용자는 11개 Windows 검증 항목 통과를 보고했지만, 이 패치의 새 Windows 실행 파일은 해당 환경에서 컴파일·실행하지 못했습니다. `VERIFY.cmd`는 파일 체크섬·구성 검사이며 수동 하드웨어 검증을 대체하지 않습니다.
