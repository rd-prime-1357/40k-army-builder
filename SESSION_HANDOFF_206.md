# SESSION HANDOFF 206

**Turn type:** tooling+data. `loadout_parser.py`, `repro_check.py`, `rules_assertions.py`,
`pipeline_manifest.py` changed (tooling). `unit_loadouts.json`, `wargear_points.json` regenerated
(data, mechanical consequence of the tooling fixes plus GK's first-time inclusion). No engine change.

## What happened

1. **Baseline reconciled at open — two genuine gaps found, both fixed, distinct from routine
   housekeeping.**
   - `SESSION_HANDOFF_203.md`: re-verified S205's finding via a fresh clone. Confirmed genuinely
     unrecoverable — absent from the repo, absent from git history, absent from the project area.
     Its substance already lives in the decision log as D296 (reconstructed by S204). Removed its
     `GUARDED` entry in `pipeline_manifest.py` (D299) rather than leave the gate permanently red.
   - `Thousand_Sons_web.txt`: found missing from `source_manifest.json`'s tracked file list during
     the data-turn source fetch — it has only ever lived in the project mount, the same failure
     pattern that lost the S203 handoff. Pulled a working copy from the project area to unblock this
     session (sha256:12 `44f751b55246`). **Cannot fix permanently — the private-repo token is
     read-only.** Ryan action needed (see below).
   - P4 source census (`rules_assertions.py`) was stale after S205's B104 change — 5 filenames added
     to `P4_REFERENCED_SOURCES`, no functional change.

2. **B105 shipped (D300).** New classifier `classify_one_model_passive_swap` in `loadout_parser.py`
   for the passive "N `<model>` can have its X replaced with Y" sentence shape. Regression-checked
   against the full options corpus before regenerating anything: 13 matches, all previously
   unclassified by any existing function; only 2 belong to a currently-built unit (Brotherhood
   Terminator Squad, Paladin Squad — the actual B105 targets).

3. **B107 opened and closed same session (D300).** Verifying B105's target units surfaced a second,
   real defect the backlog had incorrectly described as already-fixed: `weapon_abilities.json`'s raw
   punctuation vs. `loadout_parser.py`'s post-`clean()` option text — "Ancient's Banner" (curly
   apostrophe only in the allowlist) failed to resolve and fell back to a bad-cased placeholder,
   dropping `equipment_parts`. "Apothecary's Narthecium" happened to resolve by coincidence, because
   `weapon_abilities.json` holds duplicate entries for it in both punctuation styles. Fixed by running
   the allowlist's source names through `clean()` before keying. Diff-guarded: touches only Grey
   Knights' two affected units.

4. **`GK` added to `repro_check.py`'s `FACTIONS`.** `unit_loadouts.json` regenerated from source
   (seeded with only the four `HAND_AUTHORED` entries, matching `repro_check.py`'s own methodology —
   not a full-file carry-forward, which would have silently preserved pre-fix `UNMATCHED` residuals).
   Key-level diff against the previously committed file: **25 added (Grey Knights' full roster), 0
   removed, 0 changed.** `repro_check` passes byte-identical. Confirmed the only two residual
   `_parser_flags` left anywhere in Grey Knights are the two Dreadknights' B106-blocked line — nothing
   new, nothing missed.

5. **`wargear_points.json` regenerated — same class of gap D236 found for CSM in S153.** GK's
   first-time presence in `unit_loadouts.json` let `build_wargear_points()` resolve its MFM WARGEAR
   OPTIONS lines for the first time; `E14-1` correctly caught the staleness. Regenerated using the
   canonical `FACTION_BY_MFM` insertion order + remaining files appended — **not** alphabetical: a
   first attempt with sorted-glob order reproduced identical costs but silently changed `source`
   provenance on 2 unrelated pre-existing entries (Black Templars processed before Space Marines),
   discarded before committing, same trap D236 documented. Diff-guarded: **4 units added, 0 removed, 0
   changed.** `E14-1` passes.

6. **`E14-2`'s pinned census updated 75/54 → 90/61.** Verified by faction breakdown before updating
   the literal: every non-GK faction's contribution is unchanged, GK contributes exactly +15 options
   across +7 units.

7. **Full baseline green.** All repro checks, all 21+ JS harness gates, and `rules_assertions`
   (119/120 logical — the 120th, P3, only fails on the expected mid-session manifest-hash staleness,
   resolved by the `--write` below) pass.

## State at close

- `loadout_parser.py`: B105 classifier added; B107 quote-normalisation fix in `equipment_items`
  loading.
- `repro_check.py`: `GK` added to `FACTIONS`; stale B104-era comment updated.
- `unit_loadouts.json`: regenerated; 25 GK units added, 0 changed elsewhere; `repro_check` passes.
- `wargear_points.json`: regenerated; 4 GK units added, 0 changed elsewhere; `E14-1` passes.
- `rules_assertions.py`: P4 census updated (5 filenames); `E14-2` literal updated 75/54 → 90/61.
  Assertion count unchanged (still 120).
- `pipeline_manifest.py`: `SESSION_HANDOFF_203.md` removed from `GUARDED` (D299, with note);
  `SESSION_HANDOFF_206.md` appended.
- `index.html`, `equipped_parser.py`, `detachment_parser.py`, `units.json`: untouched.
- `Thousand_Sons_web.txt`: present locally, sha256:12 `44f751b55246` — not yet in the private repo.
- `OPEN_ITEMS_BACKLOG.md`: **22 open** (down from 23 — B105 closed; B107 opened and closed same
  session).
- B100 (Grey Knights) substantially closed. **B106** (Dreadknights' distinct-addition engine gap)
  remains open, untouched — correctly the only thing left blocking Grey Knights' full completion.

## Ryan action required

1. **Push `Thousand_Sons_web.txt` to the private `rd-prime-1357-data-sources` repo and regenerate
   `source_manifest.json`.** This file has only ever lived in the project mount and is at the same
   risk of silent loss that claimed `SESSION_HANDOFF_203.md`. I can't fix this myself — the token in
   `SOURCE_REPO_TOKEN.txt` is read-only.
2. Push this session's changed files to the public repo (listed below).
3. No product/rules-legality decision waiting.

## Decisions waiting on Ryan

None blocking. Everything this session was a process/tooling call within my own authority, noted here
rather than asked.

## Files (SHA-256, first 12)

Verify these at S207 open.

| file | sha256:12 | note |
|------|-----------|------|
| `loadout_parser.py` | `f83e6579c5c2` | B105 classifier + B107 fix |
| `repro_check.py` | `b63c96690312` | `GK` added to `FACTIONS` |
| `unit_loadouts.json` | `9e05ae6583ec` | 25 GK units added, 0 changed elsewhere |
| `wargear_points.json` | `f19434e8c197` | 4 GK units added, 0 changed elsewhere |
| `rules_assertions.py` | `6a9aa3da9e79` | P4 census + `E14-2` literal updated |
| `pipeline_manifest.py` | `5c49ea2ad13e` | S203 removed from GUARDED (D299); S206 appended |
| `pipeline_manifest.json` | `69b72b3129e0` | regenerated via `--write` at session close |
| `40K_Decision_Log.md` | `6bf0cb562124` | D299, D300 appended |
| `DECISION_INDEX.md` | `f8a213ee1e39` | D299, D300 entries |
| `OPEN_ITEMS_BACKLOG.md` | `68c3310c190c` | B105 closed, B107 opened+closed, B100 updated; 22 open |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S207 |
| `Thousand_Sons_web.txt` | `44f751b55246` | present locally only — see Ryan action above |
| `SESSION_HANDOFF_206.md` | `3ec7e8dd047b` | this file (hash is pre-computation; verify against banked copy) |

`index.html`, `equipped_parser.py`, `detachment_parser.py`, `units.json`, `abilities.json`,
`weapon_abilities.json`, `datasheet_wargear_abilities.json`, `detachments.json`,
`detachment_effects.json`, `faction_taxonomy.json`, `source_manifest.json`: **untouched**, no entry
needed. (`source_manifest.json` needs a *future* update once Ryan pushes `Thousand_Sons_web.txt` to
the private repo — not this session's job.)

## Backlog

23 open at S205 close, down to 22 here (B105 closed; B107 opened and closed same session). Beginning:
B105, B106, B99, B98, B97, B103, E28, B93, B90, B94, B89, B100, B85, B86, B69, B70, B75, P2, P4, E23,
B67b, E12, B17 (23 — matches S205's ending count). Resolved: B105. Added: none counted as open (B107
opened and closed same session). Ending: B106, B99, B98, B97, B103, E28, B93, B90, B94, B89, B100,
B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (22).
