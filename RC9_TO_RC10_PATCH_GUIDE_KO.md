# FilmCraft v0.6.0 RC9 → RC10 패치 안내

1. RC9 전체 소스 폴더를 백업합니다.
2. 패치 ZIP 안의 `filmcraft-main/` 내용을 RC9 `filmcraft-main/`에 덮어씁니다.
3. Windows에서 `TEST.cmd`, `BUILD.cmd`, `INSTALL.cmd`를 차례대로 실행합니다.
4. 빠른 내보내기에서 Windows H.264 하드웨어 인코더 **후보** 목록을 확인합니다.

**주의:** 이 패치는 GPU 드라이버 등록 후보를 읽는 진단 기능을 추가합니다. AMD AMF / Intel QSV 패킷 인코더를 활성화하지 않습니다. CPU 대체 및 기존 NVENC 경로는 그대로 유지됩니다. 실제 Windows 컴파일 및 UI/영상 출력 검증은 필요합니다.
