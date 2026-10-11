//! Korean Hangul fallback for the UI (and Korean filenames, even when UI is English).
//! No font file is bundled: prefer optional craft-fonts (`Kore`), otherwise an installed system
//! font. The font is inserted into all egui families once theme fonts are installed.

use std::sync::{Arc, OnceLock};

use egui::{FontData, FontDefinitions, FontFamily};

const SAMPLE: &str = "한국어 파일 편집 저장 메뉴 영상 자막 가나다";
const PREFERRED: &[&str] = &[
    "Malgun Gothic", "맑은 고딕", "Apple SD Gothic Neo", "AppleGothic",
    "Noto Sans CJK KR", "Noto Sans KR", "Source Han Sans KR", "NanumGothic",
    "Nanum Gothic", "UnDotum", "Baekmuk Dotum",
];

pub(crate) fn craft_fonts() -> impl Iterator<Item = &'static filmcraft_text::fonts::CraftFont> {
    filmcraft_text::fonts::CRAFT_FONTS.iter().filter(|f| f.scripts.contains(&"Kore"))
}

/// A declared `Kore` script alone does not prove that a custom face contains Hangul.
/// Check real glyph coverage before accepting the optional craft-fonts for the UI.
fn craft_font_available() -> bool {
    craft_fonts().next().is_some()
        && filmcraft_text::fonts::all_faces().iter().any(|face| {
            face.info.origin == filmcraft_text::fonts::CRAFT_ORIGIN
                && SAMPLE.chars().all(|ch| face.has_char(ch))
        })
}

fn system_font() -> Option<Arc<FontData>> {
    static FONT: OnceLock<Option<Arc<FontData>>> = OnceLock::new();
    FONT.get_or_init(|| {
        if cfg!(target_arch = "wasm32") {
            return None;
        }
        filmcraft_text::fonts::scan_system();
        let faces: Vec<_> = filmcraft_text::fonts::all_faces()
            .into_iter()
            .filter(|f| f.info.origin == "system" && !f.info.italic)
            .collect();
        let covers = |f: &filmcraft_text::fonts::Face| SAMPLE.chars().all(|ch| f.has_char(ch));
        let by_weight = |f: &&Arc<filmcraft_text::fonts::Face>| f.info.weight.abs_diff(400);
        let preferred = PREFERRED.iter().find_map(|name| {
            faces.iter().filter(|f| f.info.family.eq_ignore_ascii_case(name) && covers(f)).min_by_key(by_weight)
        });
        let face = preferred.or_else(|| faces.iter().filter(|f| covers(f)).min_by_key(by_weight))?;
        Some(Arc::new(FontData {
            font: std::borrow::Cow::Owned(face.data()?),
            index: face.info.index,
            tweak: Default::default(),
        }))
    }).clone()
}

/// False on the web if no `Kore` font was provided through CRAFT_FONTS_DIR.
pub(crate) fn available() -> bool {
    craft_font_available() || system_font().is_some()
}

pub(crate) fn install(fonts: &mut FontDefinitions) {
    // A custom font may advertise the script while omitting glyphs used in the UI.
    // In that case use an installed system font rather than displaying missing-glyph boxes.
    let korean: Vec<_> = if craft_font_available() { craft_fonts().collect() } else { Vec::new() };
    if korean.is_empty() {
        if let Some(font) = system_font() {
            fonts.font_data.insert("system-korean".into(), font);
            for stack in fonts.families.values_mut() {
                stack.push("system-korean".into());
            }
        }
        return;
    }
    let name = |f: &filmcraft_text::fonts::CraftFont| format!("craft:{} {}", f.family, f.style);
    for f in &korean {
        fonts.font_data.insert(name(f), Arc::new(FontData::from_static(f.bytes)));
    }
    for (family, stack) in &mut fonts.families {
        let heavy = matches!(family, FontFamily::Name(n) if matches!(n.as_ref(), "semibold" | "medium"));
        let mut order = korean.clone();
        order.sort_by_key(|f| ((f.style == "Bold") != heavy, !f.family.contains("Sans")));
        stack.extend(order.iter().map(|f| name(f)));
    }
}
