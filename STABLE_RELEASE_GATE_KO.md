# FilmCraft v0.6.0 Stable — 출시 수락 기준

## 검증 출처

2026-10-11 사용자 메시지는 다음 **11개 항목 모두 통과**라고 보고했습니다. 이 파일은 사용자 보고를 기록한 것이며, 이 소스에서 자동 실행·확인한 결과를 의미하지 않습니다.

- [x] Windows Release 빌드 및 Rust 테스트 통과 (사용자 보고)
- [x] 한글 문자 도구 조합·확정·삭제 정상 작동 (사용자 보고)
- [x] 한글 자막 저장·재열기·MP4 출력 (사용자 보고)
- [x] 후원·Discord 버튼 브라우저 실행 (사용자 보고)
- [x] Shorts 1080×1920 H.264/AAC 정상 출력 (사용자 보고)
- [x] NVIDIA NVENC 검증 (사용자 보고)
- [x] AMD AMF 검증 (사용자 보고)
- [x] Intel QSV 검증 (사용자 보고)
- [x] GPU 실패·취소 시 파일 보존 (사용자 보고)
- [x] Windows 설치·업데이트·제거 (사용자 보고)
- [x] 포터블 실행 및 배포 체크섬 검증 (사용자 보고)

## 정식 배포 절차 (Windows x64)

1. 이 Stable 소스에서 `python scripts/check_stable_release.py`를 실행하고 버전 일치 검사 통과 확인.
2. `TEST.cmd`, `BUILD.cmd`, `PACKAGE.cmd`, `INSTALL.cmd`, `VERIFY.cmd` 순으로 실행.
3. 생성된 `dist/FilmCraft_v0.6.0_Stable_RELEASE_MANIFEST.json`의 검증된 파일 크기·SHA-256 확인.
4. **Stable로 새로 빌드한** GUI에서 한글 문자 도구·자막·후원·Discord 링크 확인.
5. **Stable로 새로 빌드한** MP4의 Shorts 출력·CPU/NVENC/AMF/QSV·취소·복구 확인.
6. 실제 설치·업데이트·제거·포터블 데이터 경로 테스트 및 배포 전 백업.
7. 배포 파일 서명 여부·SmartScreen 알림·사용 라이브러리 라이선스 확인.

`VERIFY.cmd`는 SHA-256·ZIP 항목·EXE 기본 헤더 검사만 수행하며 실제 프로그램을 실행하지 않습니다. `*_RELEASE_MANIFEST.json`의 `windows_runtime_verified`는 자동으로 true가 되지 않습니다. 검증 로그 없는 성공 주장을 추가하지 마세요.
