#!/usr/bin/env python3
"""RC5 source-regression checks; not a Windows executable/IME/GPU test."""
from pathlib import Path
P=Path(__file__).resolve().parents[1]
ui=(P/'crates/ui-egui/src/panels/export_mode.rs').read_text(encoding='utf-8')
text=(P/'crates/ui-egui/src/panels/graphics.rs').read_text(encoding='utf-8')
assert 'if app.ui.export.quick_path.is_empty() {' in ui
assert 'ends_with(&format!(".{ext}"))' not in ui
assert 'quick_path_with_extension' in ui
assert 'app.ui.export.quick_preset != selected_before' in ui
assert 'Keep the preset, filename and encoder choices available for retry' in ui
assert 'one_commit_only_swallows_one_matching_text_echo' in text
assert 'ImeFrameEchoBudget::new(&events)' in text
assert 'echo_budget.apply(&mut text, &mut ed, ev, &events)' in text
assert 'ed.ime_preedit.clear();' in text
print('[OK] RC5 path editing, export retry and IME commit echo regression checks')
