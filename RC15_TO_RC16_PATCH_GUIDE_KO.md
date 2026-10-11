# FilmCraft v0.6.0 RC15 → RC16 업데이트 안내

## 적용 대상
- 정확히 RC15 전체 소스 (`FilmCraft_v0.6.0_RC15_Buttons_BrowserFix_Full_Source.zip`) 기준입니다.
- 압축을 풀고 본 ZIP의 `filmcraft-main/` 폴더를 원본 위에 병합·덮어쓰세요.
- RC14 이하에 RC15→RC16 패치만 적용하지 마세요. 그 경우 RC16 전체 소스를 사용하세요.

## Windows 검증
```bat
python scripts\check_rc16_ui.py
TEST.cmd
BUILD.cmd
INSTALL.cmd
VERIFY.cmd
```

후원 버튼 URL: https://ctee.kr/place/caw
Discord URL: https://discord.gg/artcraft

문자 도구 실기기 검사: 새 텍스트 생성 후 `안녕하세요 한글 테스트 ABC`를 입력하고 Backspace/Enter를 확인하세요.
진단 로그: `set FILMCRAFT_IME_DIAGNOSTICS=1` 실행 후 표준 오류 스트림을 저장하세요. 문자열 내용은 기록하지 않습니다.

## 아직 검증되지 않은 항목
이 ZIP은 수정된 Rust 소스이며 Windows 빌드 완료 EXE가 아닙니다. 실제 브라우저 열기, 한글 IME 입력, GPU 인코딩, 설치·업데이트·제거는 Windows에서 별도 검증이 필요합니다.
