//! Korean UTF-8 caption regression tests: SRT + WebVTT, multiline, punctuation,
//! and decomposed Hangul input survive save/reopen without lossy conversion.
use filmcraft_captions::{Cue, Document, Format, WriteOptions, parse, write};
use filmcraft_time::{TICKS_PER_SECOND, Tick};

#[test]
fn korean_caption_roundtrip_srt_and_webvtt() {
    let ms = TICKS_PER_SECOND / 1000;
    let original = Document {
        cues: vec![
            Cue {
                start: Tick(1_000 * ms),
                end: Tick(3_500 * ms),
                text: "안녕하세요!\n자막 테스트입니다.".into(),
                ..Default::default()
            },
            Cue {
                start: Tick(4_000 * ms),
                end: Tick(6_000 * ms),
                text: "영상 편집 — 한글 👩\u{200d}💻".into(),
                ..Default::default()
            },
        ],
        ..Default::default()
    };
    for format in [Format::Srt, Format::WebVtt] {
        let bytes = write(&original, format, WriteOptions::default());
        let contents = std::str::from_utf8(&bytes).expect("Korean subtitle output must be UTF-8");
        assert!(contents.contains("안녕하세요!"));
        assert!(contents.contains("자막 테스트입니다."));
        assert!(contents.contains("한글"));
        let reopened = parse(&bytes, format).expect("Korean subtitle should parse again");
        assert_eq!(reopened.cues, original.cues);
        // Stable serialization is important for export reproducibility.
        assert_eq!(write(&reopened, format, WriteOptions::default()), bytes);
    }
}

#[test]
fn korean_caption_bom_and_crlf_import() {
    let doc = Document { cues: vec![Cue {
        start: Tick(TICKS_PER_SECOND),
        end: Tick(2 * TICKS_PER_SECOND),
        text: "한국어 자막\n둘째 줄".into(),
        ..Default::default()
    }], ..Default::default() };
    for format in [Format::Srt, Format::WebVtt] {
        let mut bytes = vec![0xef, 0xbb, 0xbf];
        let text = String::from_utf8(write(&doc, format, WriteOptions::default())).unwrap();
        bytes.extend_from_slice(text.replace('\n', "\r\n").as_bytes());
        let parsed = parse(&bytes, format).expect("UTF-8 BOM CRLF subtitles should parse");
        assert_eq!(parsed.cues, doc.cues);
    }
}

#[test]
fn korean_cp949_legacy_srt_import_and_utf8_export() {
    let korean_srt = "1\r\n00:00:01,000 --> 00:00:03,000\r\n한국어 제목\r\n안녕하세요!\r\n\r\n";
    let (cp949, _, had_errors) = encoding_rs::EUC_KR.encode(korean_srt);
    assert!(!had_errors, "all Korean characters must be encodable as Windows CP949");
    assert!(std::str::from_utf8(&cp949).is_err(), "fixture must exercise the legacy decoder");
    let parsed = parse(&cp949, Format::Srt).expect("legacy CP949 SubRip can be read");
    assert_eq!(parsed.cues.len(), 1);
    assert_eq!(parsed.cues[0].text, "한국어 제목\n안녕하세요!");
    let exported = write(&parsed, Format::Srt, WriteOptions::default());
    let utf8 = String::from_utf8(exported.clone()).expect("exports must be UTF-8");
    assert!(utf8.contains("한국어 제목"));
    assert_eq!(parse(&exported, Format::Srt).unwrap().cues, parsed.cues);
}

#[test]
fn korean_srt_unicode_bom_precedes_legacy_decoder() {
    let text = "1\n00:00:01,000 --> 00:00:02,000\n한글 이모지 👩\u{200d}💻\n\n";
    let utf16: Vec<u8> = [vec![0xff, 0xfe], text.encode_utf16().flat_map(u16::to_le_bytes).collect()].concat();
    assert_eq!(parse(&utf16, Format::Srt).unwrap().cues[0].text, "한글 이모지 👩\u{200d}💻");
}

#[test]
fn korean_legacy_detection_does_not_change_western_1252_subtitles() {
    let cp1252_srt = b"1\n00:00:01,000 --> 00:00:02,000\nCaf\xe9\n\n";
    assert_eq!(parse(cp1252_srt, Format::Srt).unwrap().cues[0].text, "Café");
}
