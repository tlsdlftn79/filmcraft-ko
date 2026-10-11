# FilmCraft v0.6.0 RC19 — 부분 완성 기능 정리 및 수락 기준

**구분:** 이 문서는 테스트 절차이며, Windows에서 수행한 시험 결과는 아닙니다.

## RC19 수정 내용

1. **빠른 내보내기·일반 내보내기·대기열 경로 전체 검사:** 파일 이름뿐 아니라 상위 폴더의 Windows 금지 문자와 예약 장치명을 차단합니다. `C:\NUL\영상.mp4`, `C:\bad?folder\영상.mp4`, `COM¹.mp4`처럼 출력 불가능한 경로를 거부합니다. 유효한 UNC(`\\server\share\영상.mp4`) 및 한글 경로는 허용합니다.
2. **프리셋 확장자 변경:** Windows 역슬래시와 점(`.`)을 포함한 상위 폴더를 안전하게 처리합니다.
3. **Windows 수락 검사:** 빌드, 테스트, 설치·포터블 배포 검증을 JSON 파일로 기록하고, 수동 검증이 필요한 항목은 `NOT_TESTED`로 남깁니다.
4. **기존 기능 유지:** 한국어 IME 코드, 한글 자막, YouTube Shorts, 후원·Discord 링크, NVENC/CPU 내보내기, 설치 스크립트는 유지합니다.

## 테스트

Windows PowerShell에서:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\rc19-windows-acceptance.ps1 -RunBuild
```

실행 파일이 준비되어 있다면 화면 실행 요청까지:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File scripts\rc19-windows-acceptance.ps1 -Launch
```

보고서: `build-logs\rc19-acceptance.json`. 자동 검사와 실제 GUI 동작은 별개이며, 수동 검사 항목을 자동 성공 처리하지 않습니다.

## Windows 수동 수락 조건

- [ ] 문자 도구로 `안녕하세요`, `한글 ABC 123`, `한한` 입력 및 Backspace/Enter/방향키 정상
- [ ] 한글 SRT·WebVTT 자막 불러오기 → 수정 → 저장 → 재열기
- [ ] MP4 출력 후 한글 자막 깨짐 없음, 오디오 정상
- [ ] Shorts 1080×1920 H.264 MP4 재생·디코딩 성공 (`python scripts\verify_shorts_mp4.py "영상.mp4"`)
- [ ] 후원 버튼에서 `https://ctee.kr/place/caw` 실제 브라우저 열림
- [ ] Discord 버튼에서 커뮤니티 링크 실제 브라우저 열림
- [ ] NVENC 사용 가능한 GPU 실기기에서 인코딩, 불가 환경에서 CPU 대체 및 MP4 디코딩 검증
- [ ] Windows 설치/업데이트/제거 및 사용자 프로젝트·설정 유지

## 미완성 또는 미검증 (정식 완료로 표기 금지)

- AMD AMF와 Intel Quick Sync의 **FilmCraft 내부** H.264 인코더 통합은 여전히 미구현입니다. 기존 FFmpeg 시험·후처리 도구는 별개입니다.
- Windows 컴파일, 실제 GUI 한국어 IME, 지원 GPU에서의 NVENC, 설치·제거, 실제 FilmCraft MP4 출력은 **이 환경에서 미검증**입니다.
- 한국어 UI 번역 키 대응과 실사용 UI 품질/글꼴 품질은 별개입니다.

**최종 Stable 판정:** 위 필수 수락 조건의 실제 Windows 결과 및 로그가 있어야 합니다.
