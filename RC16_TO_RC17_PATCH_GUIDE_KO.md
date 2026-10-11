# RC16 → RC17 업데이트 패치

`FilmCraft_v0.6.0_RC16_Korean_Stability_Full_Source.zip`을 압축 해제한 뒤 RC17 패치 ZIP 안의 `filmcraft-main/` 파일을 **동일한 경로에 덮어쓰기** 하세요. 기존 수정 사항이 있다면 먼저 백업하세요.

새 작업 폴더로 시작할 경우 RC17 전체 소스 ZIP을 사용하세요.

검사: `python scripts\check_rc17_ime_dead_code.py` → `TEST.cmd` → `BUILD.cmd` → `INSTALL.cmd`.

이번 변경은 Rust 라이브러리에서 테스트 전용 함수의 `dead_code` 경고를 제거하는 것입니다. 실제 Windows 빌드는 여기서 수행하지 못했습니다.
