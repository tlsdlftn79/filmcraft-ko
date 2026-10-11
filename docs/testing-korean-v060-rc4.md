# RC4 Windows 실기기 테스트 체크리스트

1. `TEST.cmd`, `BUILD.cmd`, `PACKAGE.cmd`, `INSTALL.cmd`, `VERIFY.cmd` 성공 여부 기록
2. 문자 도구(T) 선택 → 새 텍스트 레이어 생성 → Windows 한글 입력기에서 `한글 입력 확인`을 천천히 입력. 조합 중 글씨가 유지되고 확정되며 중복되지 않는지 확인
3. 글자를 여러 번 입력한 다음 Backspace, 방향키, Enter, 영문으로 전환하여 혼합 입력 및 멈춤 없는지 확인
4. 문자 도구 편집 중 속성의 Source Text 입력칸을 클릭. 그쪽으로 포커스가 이동하고 한글 조합이 정상적인지 확인
5. 프로젝트 저장/닫기/열기 후 텍스트 확인, 파일명에 한글 사용하여 내보내기
6. 빠른 내보내기 → `YouTube Shorts 1080×1920 (9:16)` 선택 후 영상 9:16, AAC, 원본 FPS 확인; 16:9 영상은 좌우가 잘릴 수 있으므로 화면 확인
7. 빠른 내보내기 CPU 선택 → MP4 출력, GPU(자동) 선택 → MP4 출력. NVIDIA GPU에서 NVENC 실사용 여부 드라이버 로그·GPU 영상 엔진 통계 등으로 확인. GPU 없는 PC에서 CPU 대체되는지 확인
8. 외부 영상 분석: `ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate -of json output.mp4`
9. Setup.exe 설치·제거/업그레이드 이후 프로젝트와 설정 보존 확인

## 수집 로그
- `cargo --version`, `rustc --version`
- `cargo check --locked -p filmcraft-ui-egui`
- 오류 또는 경고 전체 로그, 발생하는 Windows 버전, GPU 모델/드라이버, 한글 입력기 종류

실행 환경 내에서 위 항목의 실기기 완료 여부를 표시할 수 없습니다.
