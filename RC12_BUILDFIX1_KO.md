# FilmCraft v0.6.0 RC12 — BuildFix1 (Windows MSVC)

## 해결하는 컴파일 오류

- E0425: `MFVideoFormat_H264` import 누락 (`mft.rs`)
- E0107 / E0271 / E0277 / E0308: `filmcraft_codecs::Result<T>` 별칭과 `std::result::Result<T, String>` 혼동 (`mod.rs`)

## 변경 사항

1. `crates/platform/src/media_foundation/mft.rs` — 기존 Media Foundation `use` 목록에 `MFVideoFormat_H264` 추가. H.264 인코더 출력 subtype을 NV12로 바꾸지 않습니다.
2. `crates/platform/src/media_foundation/mod.rs` — 진단 함수의 반환 타입에 `std::result::Result<Vec<String>, String>`을 명시. 기존 `CodecError` 기반 `Result<T>`은 디코딩 코드에서 그대로 유지합니다.
3. `scripts/check_mf_h264_buildfix.py` — 동일한 코드 실수를 다시 만들지 않도록 두 변경 지점을 검사합니다.

## 기존 RC12에 업데이트 적용

`FilmCraft_v0.6.0_RC12_BuildFix1_Update_Patch.zip`을 RC12 프로젝트 폴더의 **상위 폴더**에 압축 해제하고 같은 경로의 파일을 덮어씁니다. 패치 ZIP에는 `filmcraft-main/` 경로가 포함되어 있습니다.

## Windows 검증

```bat
python scripts\check_mf_h264_buildfix.py
cargo check --locked -p filmcraft-platform --target x86_64-pc-windows-msvc
cargo check --locked -p filmcraft-ui-egui --target x86_64-pc-windows-msvc
TEST.cmd
BUILD.cmd
```

`--target` 검사는 Windows MSVC 툴체인을 설치한 Windows에서 실행하십시오.

## 검증 범위

Python 회귀 검사는 소스 구조만 검사하며 Windows에서 `cargo check`를 실제로 실행한 결과는 아닙니다. 5개 제보 오류의 직접 원인을 수정했으나 새로운 컴파일 오류 발생 여부는 Windows 빌드 로그로 확인해야 합니다.

기존 번역·IME·자막·GPU 진단·Shorts·후원·설치 프로그램 소스는 변경하지 않았습니다.
