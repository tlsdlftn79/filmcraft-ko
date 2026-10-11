#!/usr/bin/env python3
"""Zero-dependency translation regression check. Matches FilmCraft's TSV semantics.
Run from any directory: py -3 scripts/check_i18n.py
"""
from collections import Counter
import argparse
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "crates/ui-egui/src/i18n"
LANGS = ["es", "ja", "ko", "pt-br", "uk", "zh-cn"]


def unescape(src):
    # Same escapes as src/i18n/catalog.rs (`\\n`, `\\t`, `\\\\`); others remain literal.
    out = []
    i = 0
    while i < len(src):
        if src[i] == "\\" and i + 1 < len(src):
            t = src[i + 1]
            if t in "nt\\":
                out.append({"n": "\n", "t": "\t", "\\": "\\"}[t])
                i += 2
                continue
            out.extend((src[i], t))
            i += 2
        else:
            out.append(src[i])
            i += 1
    return "".join(out)


def entries(lang):
    result, errors = [], []
    path = BASE / (lang + ".tsv")
    for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        if not line.strip() or line.startswith("#"):
            continue
        cols = line.split("\t")
        if len(cols) != 3 or not cols[1] or not cols[2]:
            errors.append(f"{lang}:{number}: expected context<TAB>source<TAB>translation")
            continue
        c, src, dst = map(unescape, cols)
        result.append((c, src, dst, number))
    seen = set()
    for c, src, dst, number in result:
        key = (c, src)
        if key in seen:
            errors.append(f"{lang}:{number}: duplicate key {key!r}")
        seen.add(key)
        if sorted(re.findall(r"\{([^}]*)\}", src)) != sorted(re.findall(r"\{([^}]*)\}", dst)):
            errors.append(f"{lang}:{number}: placeholder mismatch: {src!r}")
        if src.endswith("…") != dst.endswith("…"):
            errors.append(f"{lang}:{number}: ellipsis mismatch: {src!r}")
    return result, errors


def main():
    parser = argparse.ArgumentParser(description="Validate localized UI strings and report Korean coverage")
    parser.add_argument("--min-ko-coverage", type=float, default=100.0,
                        help="Minimum Korean coverage vs the Spanish source-key reference (default: 100 percent)")
    parser.add_argument("--write-ko-missing", metavar="FILE", type=Path,
                        help="Write the untranslated source keys as a UTF-8 TSV file")
    args = parser.parse_args()
    errors = []
    catalogs = {}
    for lang in LANGS:
        values, invalid = entries(lang)
        catalogs[lang] = values
        errors.extend(invalid)
    ko = {(context, src) for context, src, _, _ in catalogs["ko"]}
    reference = {(context, src) for context, src, _, _ in catalogs["es"]}
    translated = ko & reference
    missing = reference - ko
    coverage = (100.0 * len(translated) / len(reference)) if reference else 0.0
    if coverage + 1e-9 < args.min_ko_coverage:
        errors.append(f"ko: coverage regression {coverage:.2f}% is below {args.min_ko_coverage:.2f}%")
    if args.write_ko_missing:
        args.write_ko_missing.parent.mkdir(parents=True, exist_ok=True)
        with args.write_ko_missing.open("w", encoding="utf-8", newline="\n") as f:
            f.write("context\tEnglish source\n")
            for context, src in sorted(missing):
                f.write(f"{context}\t{src.replace(chr(10), r'\n').replace(chr(9), r'\t')}\n")
    ko_plain = {src for context, src, _, _ in catalogs["ko"] if not context}
    # 348-key historical menu corpus, used by Rust unit tests too.
    for context, src, _, _ in catalogs["pt-br"]:
        if src not in ko_plain:
            errors.append(f"ko: missing historic menu label {src!r}")
    code_files = {
        "crates/ui-egui/src/i18n/mod.rs": ["Ko,", '"ko" => Some(Self::Ko)', 'include_str!("ko.tsv")'],
        "crates/ui-egui/src/menus.rs": ['"app.language.korean"', 'Language::Ko'],
        "crates/engine/src/settings.rs": ['("ko", "한국어")'],
        "crates/ui-egui/src/theme.rs": ['crate::korean::install(&mut fonts);'],
    }
    for name, needles in code_files.items():
        data = (ROOT / name).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in data:
                errors.append(f"{name}: missing integration {needle}")
    print("FilmCraft localization static validation")
    for lang in LANGS:
        print(f"  {lang:<6} {len(catalogs[lang]):>5} entries")
    print(f"  Korean plain keys: {len(ko_plain)}")
    print(f"  Korean coverage vs Spanish key set: {len(translated)}/{len(reference)} ({coverage:.2f}%)")
    print(f"  Untranslated reference keys: {len(missing)}")
    if errors:
        print("FAILED:")
        for e in errors[:80]:
            print("  " + e)
        if len(errors) > 80:
            print(f"  ... plus {len(errors)-80} more")
        return 1
    print("[OK] All catalogs, translation placeholders, ellipses and Korean integrations verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
