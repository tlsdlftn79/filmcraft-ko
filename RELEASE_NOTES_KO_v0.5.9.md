# FilmCraft v0.5.9 — egui IME deprecation fix

## 수정된 문제

v0.5.8은 `crates/ui-egui/src/panels/graphics.rs`에서 더 이상 사용되지 않는 `egui::ImeEvent::Disabled`를 두 군데 사용해 컴파일 시 deprecated 경고가 발생했습니다. 과거 회귀 테스트에서도 같은 이벤트를 사용했습니다.

egui 0.36의 API에서는 **빈 `ImeEvent::Preedit`가 조합 종료/취소를 뜻**하고 `Commit`도 조합을 종료합니다. 새 패치에서는 다음과 같이 처리합니다.

- 비어 있지 않은 `Preedit`는 임시 조합 문자열을 유지하되 프로젝트에 저장하지 않습니다.
- 빈 `Preedit`는 임시 조합을 지우고 일반 텍스트 입력을 차단하지 않습니다.
- `Commit`은 최종 문자열을 저장하고 임시 조합을 지웁니다.
- 같은 프레임에 도착하는 IME 확정/일반 텍스트 이벤트의 중복 억제 로직을 보존합니다.
- deprecated 변형을 사용하는 모든 Rust 테스트를 현재 API 이벤트로 교체했습니다.

## 검사 방법

```bat
TEST.cmd
BUILD.cmd
INSTALL.cmd
```

Rust 단위 테스트만 별도로 확인하려면:

```bat
cargo test --locked -p filmcraft-ui-egui korean_ime
cargo check --locked -p filmcraft-ui-egui
```

Windows에서 경고가 사라지는지 확인할 때:

```bat
cargo check --locked -p filmcraft-ui-egui 2>&1 | findstr /C:"ImeEvent::Disabled" /C:"deprecated"
```

`findstr` 출력이 없더라도 Cargo 명령 자체의 성공 여부를 함께 확인해야 합니다.

## 검증 범위

Python 정적 검사/ZIP 무결성 및 패치 동등성 검사는 수행합니다. 현재 작업 환경에는 Rust 컴파일러와 Windows IME가 없어 실제 Cargo 빌드, 설치 및 실기기 한글 입력 성공은 확정할 수 없습니다.

## 공식 참고자료

- egui 0.36 API: https://docs.rs/egui/0.36.2/egui/enum.ImeEvent.html
