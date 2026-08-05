# SESSION HANDOFF 190

**Turn type:** tooling, plus one coupled two-value data correction the tooling fix forced (Rubric
Marines points). Ryan answered B90's last sub-question (Legends/Forge-World roster legality) in
conversation and confirmed the recommendation to bundle the coupled data fix into this turn. Every
source claim checked against the primary source before acting. **Outcome:** shipped. B87 closed, B94
opened, B90 fully unblocked on decisions. No engine or assertion change; `index.html` untouched.

## What happened
1. **Baseline opened green.** `./baseline.sh --fetch --data-turn`, 29/29. The project mount did not
   carry `40K_Decision_Log.md` or `BACKLOG_ARCHIVE.md` this session; both were pulled from a fresh
   clone of the public repo and their hashes matched S189's Files table exactly — nothing lost, just
   not re-uploaded to the mount. Also brought in `Thousand_Sons_web.txt` and `SOURCE_REPO_TOKEN.txt`
   from the project area to complete the working tree.
2. **S189 hash note.** S189's Files table lists `pipeline_manifest.json` as `ca199fb24c4c`; the
   actual committed file (regenerated fresh against the full guarded set) is `923dd792412f` and is
   internally self-consistent. Stale hash in S189's own table, not a data problem — recorded here so
   it isn't chased as drift later.
3. **The five old-named files are still in the repo** (`40K_Decision_Log_v3_0.md` + four siblings),
   not yet deleted. Expected per S189's Ryan-action note. Nothing was written to any of them.
4. **B87 built — v1.1 layout support in `mfm_points_parser.py`.** Per-file sniff (keyed on the ▲/▼
   markers, absent from every v1_0 file) + a normalization pass that rewrites each v1.1-exclusive
   quirk into the v1_0 line shape the existing readers already parse (drops the `UNITS` header, the
   standalone markers, the `UPDATED`/`REQUISITION`/`FORCE DISPOSITION` notes; strips inline
   `▼ (-10)`/`▲ (+10)` annotations leaving the final value). Cost readers made bullet-optional so one
   reader serves both editions; v1_0 files bypass normalization entirely. All 15 v1.1 files now cost
   fully (SM 179/179, 0 before). 15 filenames registered in `source_manifest.json` and
   `FACTION_BY_MFM`.
5. **A shipped points bug found and fixed in-flight.** The tier shape `1ST TO 3RD / 4TH+` had no
   reader; the parser fell through to single-mode and kept the pricier 4th+ line. Rubric Marines
   (CSM 000003583, TS 000001020) shipped at 110/200 instead of the correct 100/190 for the 1st-3rd
   copies — every player's first three copies overcharged by 10 pts. Added an `esc4` reader that
   emits the 1st-to-3rd price across the 3-tier schema and captures the 4th+ tier as
   `_esc4_fourth_plus` for B94. The corrected parser then diverged from committed `units.json`, so
   `units_repro_check` went red on exactly those two ids. Rather than shim the gate to reproduce a
   known-wrong value, regenerated the two values through the real pipeline and banked `units.json`;
   verified the ONLY change vs committed is those two units' points (points-only, every other field
   byte-identical). Grey Knights' Brotherhood Terminator Squad shares the shape but GK isn't built,
   so nothing shipped there.
6. **B94 opened** for the deferred copy-4 schema decision (34 units use the shape in v1.1 — transports
   plus Rubric Marines). Product/schema call: add a real 4th copy-tier vs document a fold rule.
   Recommendation recorded: add the real tier.
7. **B90's last sub-question answered (Ryan).** Legends/Forge-World datasheets a chapter's own current
   MFM prices ARE legal roster members. Verified: Astraeus and Thunderhawk Gunship priced like
   ordinary units in all five Tier-2 chapter MFMs. Turn-2 note recorded: both are currently excluded
   app-wide by `wahapedia_transform.py`'s `source_is_excluded` (their source is tagged "…(Forge
   World)", bundled with genuine Legends content the code can't presently distinguish); turn 2 must
   carve them out for the five chapters.
8. **v1.1 detachment parsing rescoped from B87 to B88.** Detachments have a separate parser
   (`detachment_parser.py`) whose MFM readers assume v1_0 layout; B88 now owns extending it. B87
   should not grow a duplicate detachment reader.
9. **Net-new `b87_check.js`** added to the harness suite and GUARDED; pins v1.1 full costing, v1_0
   stability, and the Rubric Marines fix. Baseline green at close (verified after `--write`).

## State
- Baseline: green at close.
- `index.html` unchanged, still **v6.15**.
- `rules_assertions.py` unchanged, **116/116**.
- Live behaviour: Rubric Marines now prices correctly (100/190 for 5/10 models, copies 1–3) in both
  Chaos Space Marines and Thousand Sons. No other user-visible change.
- `repo_check` will show drift until pushed: `mfm_points_parser.py`, `units.json`,
  `source_manifest.json`, `baseline.sh`, `OPEN_ITEMS_BACKLOG.md`, `40K_Decision_Log.md`,
  `DECISION_INDEX.md`, `pipeline_manifest.py`, `pipeline_manifest.json`, `b87_check.js` (net-new),
  `SESSION_HANDOFF_190.md` (net-new). The five old-named files still show repo-only. Expected.

## Ryan action required
Push this session's changes. The five old-named files from S189 still need deleting from the repo
(`40K_Decision_Log_v3_0.md`, `40K_Architecture_Overview_v0_5.md`, `40K_Data_Dictionary_v2_0.md`,
`40K_Data_Pipeline_Process_v0_6.md`, `40K_Functional_Spec_v0_7.md`) — carried over from S189, still
outstanding.

## Decisions still waiting on Ryan
1. **B94:** copy-4 tier schema — add a real 4th copy-tier to the points schema + engine lookup +
   Python mirror, or document a fold rule. Recommendation: add the real tier. Needed before B89
   adopts the 34 affected units.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `mfm_points_parser.py` | d5cb3ba7337e | v1.1 sniff + normalize; esc4 tier reader; v1.1 files in FACTION_BY_MFM |
| `units.json` | e2da8329f64b | two Rubric Marines instances corrected 110/200 → 100/190; nothing else changed |
| `b87_check.js` | ef36ffc04251 | net-new; pins v1.1 costing, v1_0 stability, Rubric Marines fix |
| `source_manifest.json` | b80182dc4822 | 15 v1.1 MFM files registered (70 → 85 source files) |
| `baseline.sh` | 4a3b52a8f129 | b87_check gate registered |
| `OPEN_ITEMS_BACKLOG.md` | d651d2b22475 | B87 closed; B94 added; B88 rescoped; B90 sub-question answered; 17 open |
| `40K_Decision_Log.md` | f0de6cc9bfb8 | D283 appended |
| `DECISION_INDEX.md` | 1b7083642059 | D283 index entry |
| `pipeline_manifest.py` | b6aaac7dbb42 | b87_check.js + SESSION_HANDOFF_190.md appended to GUARDED |
| `pipeline_manifest.json` | regenerated after this edit | regenerated, `--write` |
| `NEXT_SESSION_PROMPT.md` | (see next file) | S191 (unguarded by design) |
| `SESSION_HANDOFF_190.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
17 open, unchanged in count from S189 (B87 closed, B94 opened). Beginning: B69, B70, B75, B85, B86,
P2, P4, E23, B67b, E12, B17, B87, B88, B89, B90, E28, B93. Resolved: B87 (closed, D283). Added: B94
(D283). Ending: B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, B88, B89, B90, E28, B93, B94.
