> 아래 내용은 이전 RC 버전의 보존 기록이며, v0.6.0 Stable의 현재 검증 현황을 설명하지 않습니다.

# FilmCraft 한국어 패치 v0.6.0 RC19

> 비공식 커뮤니티 한국어 패치입니다. 공식 FilmCraft와 별도로 버전을 관리하며, 원본 Rust Cargo 패키지 버전은 그대로 유지합니다.
> **Windows Rust 컴파일, 한글 입력 실기기, MP4 렌더링, 설치/제거는 아직 검증되지 않았습니다.** RC19는 정식 안정판이 아닙니다.

## RC19 — 빠른 내보내기 경로 전체 검증 및 Windows 수락 검사

- 빠른 내보내기·일반 내보내기·대기열에 사용하는 Windows 경로의 파일명뿐 아니라 **중간 폴더 이름도** 금지 문자·예약 장치명·잘못된 경로 구성인지 검사합니다. `C:\\bad?dir\\video.mp4`, `C:\\NUL\\video.mp4` 등은 내보내기를 시작하지 않습니다.
- UNC 네트워크 경로와 한글 폴더·파일명은 유효한 경우 허용합니다.
- 프리셋 전환 시 부모 폴더 이름에 점(`.`)이나 Windows 역슬래시가 있어도 파일 확장자만 바꾸도록 수정했습니다.
- Windows 빌드·테스트·패키징 검사를 수행하고 통과 여부를 JSON으로 남기는 `scripts/rc19-windows-acceptance.ps1`을 추가했습니다. **GUI 입력 및 버튼 실제 동작은 자동 통과로 표시하지 않습니다.**
- AMD AMF·Intel QSV FilmCraft 내부 인코딩, Windows 실제 IME 동작 및 정식 Setup EXE 검증은 **아직 완료하지 못했습니다.**
- 상세한 수락 조건과 테스트 절차: [`RC19_TEST_GUIDE_KO.md`](RC19_TEST_GUIDE_KO.md).

## RC18 — 빠른 내보내기 파일명 보호 및 Windows 설치 검증

- Windows 예약 이름(CON/NUL/COM1/LPT9 등)이나 잘못된 빈 파일명을 내보내기 전에 차단하고 오류를 한국어로 표시합니다. 유효한 한글 파일명은 보존합니다.
- TEST.cmd에 RC18 정적 검사와 Rust 경로 검증 테스트를 추가했습니다.
- `scripts/rc18-windows-smoke.ps1`로 설치 등록·시작 메뉴 바로가기·실행 파일을 읽기 전용으로 확인할 수 있습니다. 실제 한글 입력, Discord/후원 링크, MP4 출력은 별도 수동 확인이 필요합니다.
- 실제 Rust MSVC 빌드와 Windows GUI 검증은 **미완료**입니다.
- 자세한 내용은 [`RC18_TEST_GUIDE_KO.md`](RC18_TEST_GUIDE_KO.md).

## RC11 — 문자 도구·GPU 실기기 진단

- 문자 도구 진입 직후 한 번만 키보드 포커스를 요청하여 첫 한글 조합 이벤트 누락 가능성 완화
- 새 글자 레이어 편집·기존 글자 레이어 재편집 진입에 동일 처리 적용
- `scripts/probe_h264_gpu.py`에서 외부 FFmpeg를 통한 NVIDIA/AMD/Intel H.264 시험 인코딩 지원
- 주의: 진단 스크립트가 성공해도 FilmCraft 내보내기에서 AMF/QSV가 사용되는 것은 아닙니다.
- 자세한 내용: [`RELEASE_NOTES_KO_v0.6.0_RC11.md`](RELEASE_NOTES_KO_v0.6.0_RC11.md)

## RC10 — Windows 하드웨어 인코더 후보 진단

Media Foundation에서 하드웨어 등록 H.264 인코더 이름을 비동기 조회하고 빠른 내보내기에 표시합니다. **후보 탐지는 AMF/QSV 인코딩 구현을 의미하지 않습니다.** 기존 GPU 자동(NVENC) 및 CPU 대체 경로는 유지됩니다.

자세한 내용은 [`RELEASE_NOTES_KO_v0.6.0_RC10.md`](RELEASE_NOTES_KO_v0.6.0_RC10.md).

## RC10 — 문자 도구 IME 입력 누락 수정 및 GPU 식별

- 한글 조합 이벤트와 같은 프레임의 **관계없는 일반 문자 입력**이 누락되는 코드 경로 수정 및 회귀 테스트 추가.
- Windows DXGI를 통해 GPU 제조사 및 모델 이름을 백그라운드에서 감지해 빠른 내보내기에서 표시. 이것은 **인코더 지원 여부 탐지가 아님**.
- AMD AMF 및 Intel Quick Sync 인코딩은 아직 미구현. 기존 NVENC 사용 시도·CPU 대체 동작 유지.
- FFmpeg `ffprobe`가 있으면 `python scripts/verify_shorts_mp4.py "영상.mp4"`로 Shorts 메타데이터 검사 가능.
- 자세한 내용은 [`RELEASE_NOTES_KO_v0.6.0_RC10.md`](RELEASE_NOTES_KO_v0.6.0_RC10.md).

Windows 실기기 체크리스트: [`docs/testing-korean-v060-rc9.md`](docs/testing-korean-v060-rc9.md).

## 주요 기능

- 한국어(`ko`) 언어 선택 및 설정 유지
- 한국어 문자열 3,783개 (`scripts/check_i18n.py` 기준 참조 키 전부 대응)
- Windows 한글 IME Preedit/Commit 처리, 조합 취소 후 Enter/Backspace/Escape 중복 처리 방지
- 한국어 글꼴 폴백, SRT/WebVTT 및 긴 한글 자막 줄바꿈 개선
- 자막 트랙에 지정한 글꼴을 미리보기/내보내기에서 일관되게 적용
- CP949 인코딩으로 저장된 구형 한국어 SRT 읽기(UTF-8로 저장)
- 자막 외곽선·배경 여백을 고려한 화면 내 줄바꿈 및 프레임 밖 임시 이미지 제한
- Inno Setup 기반 **비공식 한국어판** 설치 프로그램 및 포터블 배포 스크립트
- Windows 빌드·설치·패키지 검사 자동화, SHA-256 결과 파일

## Windows 빌드

Rust 1.95 이상 (`x86_64-pc-windows-msvc`), Visual Studio 2022 C++ Build Tools + Windows SDK, Python 3, Inno Setup 6.3 이상 필요.

```bat
TEST.cmd
BUILD.cmd
PACKAGE.cmd
INSTALL.cmd
VERIFY.cmd
```

정상 빌드의 산출물은 `dist/FilmCraft_v0.6.0_RC19_Korean_Windows_x64_Setup.exe`,
`dist/FilmCraft_v0.6.0_RC19_Korean_Windows_x64_Portable.zip` 및 각 `.sha256` 파일입니다.
`VERIFY.cmd`는 체크섬·포터블 구성 등 파일 수준 검사만 하며 설치 실행을 검증하지 않습니다.

CI (수동 실행): GitHub Actions → `FilmCraft Korean Windows RC (manual)` → Run workflow. 아직 실행 검증되지 않았습니다.

변경사항: [`RELEASE_NOTES_KO_v0.6.0_RC4.md`](RELEASE_NOTES_KO_v0.6.0_RC4.md). 실기기 검증: [`docs/testing-korean-v060-rc4.md`](docs/testing-korean-v060-rc4.md).

## RC7 — 문자 도구 포커스 복원과 GPU 인코딩 진단

- **문자 도구:** 다른 입력창을 사용한 후 영상 텍스트 레이어를 다시 클릭하면 해당 레이어에 키보드 포커스를 복구합니다. 매 프레임 재요청하지 않으므로 기존 한글 IME 조합을 불필요하게 중단하지 않습니다.
- **한글 중복 처리:** `ImeEvent::Commit("한국")` 뒤에 `Event::Text("한")`, `Event::Text("국")`처럼 나뉘어 들어오는 중복 문자열도 한 번만 걸러냅니다. 문자 반복 입력은 계속 허용합니다.
- **GPU 인코딩 안내:** Windows의 하드웨어 H.264 인코딩은 현재 NVIDIA NVENC 경로만 제공하며, AMD AMF / Intel Quick Sync 인코딩은 구현되지 않았음을 빠른 내보내기에 표시합니다. 지원 안 되는 경우 CPU로 돌아갑니다. GPU *합성* 선택은 별개입니다.
- **GPU 실기기 테스트(옵션):** `set FILMCRAFT_TEST_NVENC=1` 설정 후 `TEST.cmd`를 실행하면 플랫폼 NVENC/CPU 폴백 비교 테스트도 수행하도록 했습니다. 자동으로 Windows 드라이버를 설치하지는 않습니다.
- Windows 빌드·한글 입력·실제 NVENC 성능·설치/제거는 이 환경에서 테스트하지 못했습니다.

검증: `python scripts/check_rc7_features.py`, `python scripts/check_i18n.py` 및 Windows `TEST.cmd`.
기존 [RC6 후원 버튼](https://ctee.kr/place/caw) 기능은 유지됩니다.

## RC6 — 한국어 패치 후원 버튼

- **상단 헤더: 한국어판 후원** 버튼 추가(창이 좁으면 겹침을 막기 위해 숨김).
- **도움말 → 한국어 패치 후원…** 은 창 크기에 관계없이 접근 가능.
- **FilmCraft 정보 → 한국어판 후원** 링크 및 비공식 패치 안내 표시.
- 후원 링크: https://ctee.kr/place/caw (기본 브라우저의 새 탭에서 열림).
- 후원은 선택 사항이며 FilmCraft의 편집, 내보내기, 설치·업데이트 기능에 영향을 주지 않음.
- **비공식 커뮤니티 한국어 패치 후원**으로 표기하며 ArtCraft 공식 후원으로 오인하지 않도록 분리.
- 정적 확인: `python scripts/check_rc6_support.py`; 실제 버튼 클릭·브라우저 동작은 Windows에서 확인 필요.

변경 사항: [`RELEASE_NOTES_KO_v0.6.0_RC6.md`](RELEASE_NOTES_KO_v0.6.0_RC6.md).
테스트: [`docs/testing-korean-v060-rc6.md`](docs/testing-korean-v060-rc6.md).

## RC5 — 한글 입력 반복·빠른 내보내기 파일명 안정화

이번 버전은 **RC4를 기준으로 하는 증분 패치**입니다. 한글 파일명 자동 덮어쓰기 방지, 프리셋 확장자 처리, 내보내기 오류 시 재시도와 `ImeEvent::Commit` 중복 텍스트 계산을 보완했습니다.

- 소스 변경 내역: [`RELEASE_NOTES_KO_v0.6.0_RC5.md`](RELEASE_NOTES_KO_v0.6.0_RC5.md)
- Windows 테스트 체크리스트: [`docs/testing-korean-v060-rc5.md`](docs/testing-korean-v060-rc5.md)
- Windows 실제 실행이 검증될 때까지 **Release Candidate** 상태를 유지합니다.

## RC4 — 한글 문자 도구 / YouTube Shorts / GPU 내보내기

- **문자 도구 한글 입력**: 텍스트 레이어가 매 프레임 키보드 포커스를 다시 요청하며 Windows IME 한글 조합을 끊는 오류를 수정했습니다. 이제 편집 시작 시에만 포커스를 요청하고, 다른 텍스트 입력창으로 이동하면 포커스를 빼앗지 않습니다. Windows 실기기 입력 테스트는 아직 필요합니다.
- **빠른 내보내기 → YouTube Shorts 1080×1920 (9:16)**: H.264 MP4, 12 Mbps, AAC 48 kHz 스테레오. 원본 시퀀스의 프레임 속도 유지, 화면을 가득 채우는 확대(Scale to Fill) 기본값이므로 가로 원본은 좌우가 잘립니다. 내보내기 전에 미리보기를 확인하세요. 영상 길이가 3분을 넘으면 YouTube에서 Shorts로 분류되지 않을 수 있습니다.
- **빠른 내보내기 → CPU/GPU 인코더**: CPU(기본), GPU(자동) 선택. Windows는 기존 NVIDIA NVENC, macOS는 VideoToolbox 지원 경로를 사용하며 불가하면 소프트웨어로 대체합니다. **AMD AMF·Intel Quick Sync 인코딩은 새로 구현하지 않았으며 GPU 모델별 강제 선택은 지원하지 않습니다.** GPU 영상 효과 합성은 별도 선택 항목입니다.
- 검사: `TEST.cmd`, 빌드: `BUILD.cmd`, 설치 파일: `INSTALL.cmd`, ZIP: `PACKAGE.cmd`, 검증: `VERIFY.cmd`

RC3 → RC4 덮어쓰기 사용 방법: [`RC4_PATCH_GUIDE_KO.md`](RC4_PATCH_GUIDE_KO.md).


## v0.6.0 RC12 — 한글 입력 진단 및 GPU 검사 강화

RC12에서는 기존 한국어 입력·쇼츠·후원 기능을 유지하면서 문자 도구의 IME 진단을 추가했습니다. 기본값은 비활성화이며 `FILMCRAFT_IME_DIAGNOSTICS=1` 환경 변수를 지정하면 이벤트 **종류·문자 수·포커스 상태만** 표시합니다. 텍스트 원문은 기록하지 않습니다.

GPU 인코더 시험 명령은 `python scripts/probe_h264_gpu.py --encoder all --json`입니다. 이는 외부 FFmpeg를 검증할 뿐 AMD/Intel GPU를 FilmCraft 자체 내보내기에 추가하지 않습니다. Windows 실제 사용성 검증 전까지 RC12는 개발용 릴리스 후보입니다. 상세 변경은 [RC12 변경 내역](RELEASE_NOTES_KO_v0.6.0_RC12.md)을 참고하세요.
