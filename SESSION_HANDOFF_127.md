# Session 127 handoff — analysis/scoping: E4 designed (D199), E4a cancelled, E4b/E4c opened

**Turn type: analysis/scoping.** `index.html` (6.3), every `.json` data file, every parser, every
CSV, `list_store.js` and every harness untouched. Authoritative write-up is **D199** in
`40K_Decision_Log_v3_0.md`. This handoff is the pointer, not the design.

---

## Open state — and a project-knowledge sync gap

**Baseline: 19/19 gates pass**, but reconciliation was needed first. The Claude Project's file
store was missing `repro_check.py` and `pipeline_manifest.py` entirely, and its copy of
`pipeline_manifest.json` was stale (pre-T4 hash for `bundle_check.js`, `3fc8677b3798` instead of
S126's recorded `310c988bc085`). All three were pulled from the GitHub repo — which held the
correct versions, matching `SESSION_HANDOFF_126.md`'s hashes exactly — and the full suite then
passed clean. **The repo was right; the project area was behind.** T2 hash verification caught it
precisely as designed, first live use.

**Action for Ryan:** re-upload `repro_check.py`, `pipeline_manifest.py` and the current
`pipeline_manifest.json` (repo versions) to the Claude Project so S128 doesn't repeat the detour.

All nine S126 hashes otherwise verified: `bundle_check.js`, `OPEN_ITEMS_BACKLOG.md`,
`40K_Decision_Log_v3_0.md`, `PROCESS_IMPROVEMENT_PLAN.md`, `repo_check.py`, `baseline.sh`,
`BACKLOG_ARCHIVE.md`, `DECISION_INDEX.md` all match; `pipeline_manifest.json` was the one mismatch,
resolved above.

---

## What this session produced

**D199 — E4's full design.** Summary of what it settles (details in the entry):

- **No data turn needed.** All 515 enhancement records verified build-ready. E4a is cancelled as a
  session; its content lands as E4b assertions.
- **Eligibility keys off `unit_type`**, verified equivalent to keyword-derived eligibility
  everywhere keywords are populated (they aren't for Chaos Daemons).
- **Duplicate rule is name-keyed army-wide** — forced by 29 reachable same-army cross-detachment
  name collisions.
- **Stored assignment carries `{name, detachment_key}`** — forced by Deathwing Assault existing at
  30 pts and 15 pts in two Dark Angels detachments (both confirmed in MFM).
- **Hard block on the D114/D115 line**, one read-path function, separate Upgrade counter, an
  attach-action gate as the second enforcement point, schema v2→v3, flag-don't-drop on stale
  imports.
- **Split: E4b engine+persistence (S128), E4c UI (S129).**

## Decisions batched for Ryan (all reversible; work proceeds on the recommendations)

1. **Duplicate identity is by name, army-wide.** Same name in two selected detachments is still one
   allowed copy.
2. **Epic Heroes cannot take Upgrades.** The Upgrade bullets lift only the Character-only and
   duplicate/count rules.
3. **Per-enhancement free-text restrictions ("TERMINATOR model only") are displayed, not
   machine-enforced.** Parsing prose would guess, and a wrong guess hard-blocks a legal pick.
4. **UI: inline single-select row in the unit's existing config panel** plus a roster-level
   "Enhancements n/limit" chip — this was the product question the session prompt flagged. Why: it
   reuses the config-panel idiom the player already knows; a modal adds a second interaction
   pattern for a decision no harder than a wargear swap.

---

## Files

**Changed (SHA-256, first 12):**
- `40K_Decision_Log_v3_0.md` — appended D199 — `c5bb5b4657e6`
- `DECISION_INDEX.md` — `b72138b14861`
- `OPEN_ITEMS_BACKLOG.md` — `0642d31f383c`
- `NEXT_SESSION_PROMPT.md` — `b51b4e25608b`

Verify at S128 open per T2.

**Net new:** none. `SESSION_HANDOFF_127.md` is the rolling handoff series.

**Unchanged:** `index.html` (6.3), every `.json` data file, every parser, every CSV,
`list_store.js`, all 13 harnesses, `bundle_check.js`, `baseline.sh`, `repo_check.py`,
`pipeline_manifest.json` (repo version now in the working area — same bytes as the repo).

---

## Backlog

| | |
|---|---|
| **Beginning** | 6 — P2, E21, E4, E12, B56, B17 |
| **Resolved** | 1 — E4 (parent, scoping complete; replaced by its parts) |
| **Added** | 2 — E4b, E4c |
| **Ending** | 7 — P2, E21, E4b, E4c, E12, B56, B17 |
