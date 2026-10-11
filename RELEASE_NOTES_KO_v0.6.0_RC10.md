# FilmCraft v0.6.0 RC10 — Media Foundation 인코더 후보 진단

## 실제 수정
- Windows Media Foundation `MFTEnumEx`에서 하드웨어 H.264 **인코더** 후보를 조회합니다. 디코더 목록과 달리 `MFT_CATEGORY_VIDEO_ENCODER`, 출력 형식 `MFVideoFormat_H264`로 필터링합니다.
- 별도 작업자 스레드에서 검색하고 빠른 내보내기에 확인 중, 없음, 후보 이름, 오류 상태를 표시합니다.
- 기존 NVIDIA NVENC / CPU 대체 기능, 문자 도구 한글 IME 수정, Shorts 프리셋 및 후원 버튼을 유지합니다.
- 6개 언어에 후보 진단 문구를 추가하고 RC10 테스트 및 Windows 배포 버전 설정을 갱신했습니다.

## 한계 및 다음 작업
- **하드웨어 인코더 후보 발견 ≠ 실제 GPU 인코딩 지원**. AMD AMF·Intel Quick Sync는 여전히 실제 패킷 인코더, 설정 협상, MP4 샘플 정보 수집, 오류 복구 구현이 필요합니다. 후보 목록에 나타나더라도 GPU 사용 가능 옵션으로 활성화하지 않습니다.
- Windows Rust 컴파일, Media Foundation 드라이버 열거 및 한글 문자 도구 실기기 검증은 이 환경에서 하지 못했습니다.
- 테스트: `TEST.cmd`, 빌드 `BUILD.cmd`, 설치 `INSTALL.cmd`를 Windows에서 실행해 주세요.
