# FilmCraft RC12 BuildFix2 → RC13 업데이트

1. 원본 RC12 BuildFix2 전체 소스를 별도 백업합니다.
2. RC13 업데이트 ZIP의 `filmcraft-main/` 내부 파일을 원본 `filmcraft-main/` 폴더에 같은 경로로 덮어씁니다.
3. `python scripts\check_rc13_ime.py` 실행 후 `TEST.cmd`를 실행합니다.
4. `BUILD.cmd`와 `INSTALL.cmd`로 Windows 실행·설치 파일을 생성합니다.

이 패치는 RC12 BuildFix2 소스 기준입니다. 이전 버전으로 바로 적용하지 마십시오.
