# FilmCraft v0.6.0 RC3 — Korean text and captions

비공식 FilmCraft 한국어 패치. **RC1 전체 소스를 기반으로 한 RC3 업데이트**입니다. 공식 앱 릴리스 또는 Windows 검증 완료판이 아닙니다.

## 실제 수정

- 기존 `CaptionStyle.font` 값이 미리보기/최종 자막 렌더링에 반영되지 않고 Inter 고정으로 처리되던 경로 수정. 측정·줄바꿈·렌더링이 동일한 지정 글꼴 사용.
- 한국어 CP949 (Windows EUC-KR 호환) SRT 불러오기 지원. BOM이 있거나 유효한 UTF-8이면 기존 유니코드 경로를 우선 사용하며, 구형 서구권 Windows-1252 fallback도 유지.
- 긴 한글 자막의 실제 안전폭 계산에 외곽선·배경 여백을 포함; 프레임 밖까지 불필요하게 할당되던 임시 영상 버퍼를 영상 크기로 제한.
- 한글/영문 혼합 그래픽 텍스트 스타일·레이아웃, CP949→UTF-8 자막 왕복, BOM 호환성, 자막 글꼴·출력 범위 회귀 테스트 추가.
- Windows 설치 프로그램 및 CI 산출물 이름을 RC3로 갱신. 실제 Windows 생성·설치·MP4 내보내기는 검증 필요.

## 검증

`TEST.cmd` → `BUILD.cmd` → `PACKAGE.cmd` → `INSTALL.cmd` → `VERIFY.cmd`.
이 실행 환경에는 Rust/Cargo 및 Windows GUI가 없어 Cargo 테스트, MSVC 빌드, 한국어 IME 실기기 입력, GPU 미리보기와 MP4 인코딩을 실행하지 못했습니다. Python 정적 검사 통과는 바이너리/영상 출력 성공을 증명하지 않습니다.
