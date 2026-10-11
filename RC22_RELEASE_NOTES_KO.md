# FilmCraft v0.6.0 RC22 — GPU 내보내기 복구 안전성

이번 소스는 RC21 전체 소스를 기준으로 만든 비공식 한국어 개발 패치입니다.

## 변경 사항

- GPU 출력 파일의 교체가 실패했을 때 기존 영상 파일이 복원되지 못하는 경우를 구분해 오류 메시지에 **백업 경로**를 표시합니다.
- 이전 작업에서 남긴 복구 백업 파일이 발견되면 덮어쓰거나 삭제하지 않고 중단합니다.
- GPU 출력 파일을 최종 경로로 옮기지 못했을 때 정상 생성된 CPU 임시 MP4를 보존하고 복구 경로를 오류 메시지에 표시합니다.
- 사용자가 내보내기를 취소했거나 CPU 렌더링 자체가 실패한 경우에는 기존과 같이 임시 파일을 정리합니다.
- 파일 교체 복구를 확인하는 Rust 테스트 3개와 소스 정적 검사 6개를 추가하고 `TEST.cmd`에 연결했습니다.
- Windows 설치 프로그램 및 포터블 파일명, 검증 스크립트 표시를 RC22로 갱신했습니다.

## Windows 검증 절차

프로젝트 폴더에서 아래 명령을 실행합니다.

```bat
python scripts\check_rc22_gpu_recovery.py
cargo check --locked -p filmcraft-engine
cargo test --locked -p filmcraft-engine hardware_transcode::tests
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
```

다음 항목은 **Windows 실기기 수동 검증**이 필요합니다.

1. 문자 도구 한글 IME 조합·확정·삭제, 한영 전환
2. 후원 버튼과 Discord 버튼을 눌렀을 때 기본 브라우저 연결
3. Shorts MP4 출력, 한글 자막 및 오디오 싱크
4. AMD AMF / Intel QSV: GPU 성공 및 GPU 실패 후 CPU 출력 보존
5. 이미 존재하는 출력 파일이 잠겼을 때 오류와 복구 백업 상태
6. 설치·업그레이드·제거 시 사용자 파일·설정 보존

## 제약

이 개발 환경에는 Rust 및 Windows 실기기 GPU가 없어 Rust/MSVC 컴파일, 실제 GUI 클릭, AMF/QSV 인코딩 성공 및 설치 프로그램 실행을 검증하지 못했습니다. 정적 검사의 성공을 실기기 기능 완료로 해석하면 안 됩니다.

AMD·Intel 인코딩은 기존처럼 앱에서 FFmpeg를 호출하여 CPU H.264 결과를 다시 인코딩합니다. 네이티브 AMF/QSV SDK 통합이 아닙니다.
