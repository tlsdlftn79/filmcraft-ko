# Korean localization status — FilmCraft Korean patch v0.5.2

- Source-key reference: `crates/ui-egui/src/i18n/es.tsv`, 3,497 distinct keys.
- Korean translations: `crates/ui-egui/src/i18n/ko.tsv`, 2,876 keys.
- Shared keys: 2,617, measured by `(context, English source)` exact match.
- Reference keys without Korean translation: **880** (74.84% coverage).
- For untranslated keys see `ko_remaining.tsv` in this folder.

The Spanish translation catalog is a pragmatic coverage reference, **not a certified enumeration of every hardcoded UI string**. Translation coverage is not evidence of complete UI localization or runtime quality. Unknown keys fall back to English.

### Refresh the missing-key report

```shell
python scripts/check_i18n.py --write-ko-missing docs/localization/ko_remaining.tsv
```

Tests fail if the Korean coverage of the reference key set falls below 74%, a guard against accidentally deleting large groups of translations. To add a translation, append a `context<TAB>English<TAB>Korean` row to `ko.tsv` and rerun the validator. Placeholder identifiers and trailing ellipses must match.
