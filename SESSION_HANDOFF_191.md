# SESSION HANDOFF 191

**Turn type:** tooling/analysis. B88 closed in full (both parts: v1.1 DETACHMENTS-layout support in
`detachment_parser.py`, and `mfm_reconcile.py` generalized into a per-faction delta tool). No engine
or data-file change — `ARMY_TO_MFM` untouched, `detachments.json` not regenerated this turn; the new
parsing capability is dormant until B89 adopts it, same shape B87 left points in. **Outcome:** shipped.
B88 closed, B95 opened (incidental, found while scoping the report).

## What happened
1. **Baseline opened green.** `./baseline.sh --fetch --data-turn`, 31/31 (b87_check now a permanent
   gate). Repo confirmed genuinely current this session, not stale as first assumed mid-session — a
   first repo clone caught mid-push (before Ryan finished pushing S190) read as one session behind; a
   second check later in the session found `SESSION_HANDOFF_190.md` and D283 present in both
   `DECISION_INDEX.md` and `40K_Decision_Log.md` in the repo. Worth flagging as a process note: if a
   repo check happens to land mid-push, it can look like unpushed drift that isn't real. Re-verify
   before treating repo-vs-mount disagreement as a finding.
2. **B88 part 1 — `detachment_parser.py` v1.1 DETACHMENTS support.** Same sniff-and-normalize pattern
   as B87 (▲/▼ marker file-level sniff; normalization scoped to the DETACHMENTS...LEGENDS/EOF slice
   only, never the UNITS section). Verified against source before writing any rule: every DP line and
   every enhancement-cost line in all 15 v1.1 files is immediately preceded by its name line with
   nothing interposed, no blank lines inside any block — a straight adjacent-pair join is correct, no
   lookahead needed. Two quirks beyond B87's precedent: a bare trailing marker with no delta on a DP
   line itself (Thousand Sons HEXWARP THRALLBAND, `3DP ▲`, 2→3 DP) and a third note string,
   `UNIQUE TAG REMOVED` (World Eaters) — missed on a first pass keyed only off the Space Marines file,
   caught once World Eaters was actually parsed (raised `SystemExit`), then confirmed complete by an
   exhaustive all-caps-short-line sweep of all 15 files. One false alarm chased down and cleared:
   `CHANGEHOST OF DECEIT` looked like a parsing artifact (a stray "CHANGE" glued to a name) but is
   confirmed genuine against the v1_0 file too. Result: all 15 v1.1 files parse their DETACHMENTS
   block cleanly (0 before, all raised `SystemExit`); v1_0 output proven structurally byte-identical
   (not just count-matched) for all 10 files in `ARMY_TO_MFM`. **One real bug in my own first edit,
   caught by testing:** the sniff/normalize helper functions were written and added, but the call
   site in `parse_mfm_detachments` was never actually wired to use them — the first full-file test run
   raised `SystemExit` on the very first v1.1 file tried. Fixed before any further work.
3. **Net-new `b88_check.js`**, registered in `baseline.sh` and `pipeline_manifest.py`. Pins: all 15
   v1.1 files parse without raising; v1_0 output unchanged on the two spot-checked live-army files;
   the Hexwarp Thrallband bare-marker DP line, the Warpmeld Pact ordinary UNIQUE tag, and the Brazen
   Engines `UNIQUE TAG REMOVED` note all resolve correctly.
4. **B88 part 2 — `mfm_reconcile.py` generalized.** Old script was a one-off SM-only pass with several
   now-absent file dependencies (`Source.csv`, `Datasheets.csv`, `out/Unit_Stats.csv`, `mfm_sm.txt`).
   Rewritten to diff, for the 10 distinct MFM files backing the app's built armies (`ARMY_TO_MFM`
   deduplicated), the v1_0 file the app was built from against the v1.1 capture — points, roster,
   wargear, attach lists (incl. Leader/Support flips), and detachments (DP, force disposition, unique
   tag, enhancements) — using `mfm_points_parser.parse_mfm` and `detachment_parser.parse_mfm_detachments`
   as the only sources of truth, no parsing logic duplicated. Every delta classified
   adopt-mechanically vs investigate-first. **A real bug in the first draft, caught by review before
   shipping:** detachment force-disposition and unique-tag changes were initially lumped in with DP as
   adopt-mechanically — they're a rules-shape property, not a value (a disposition swap can change
   which missions a detachment is legal for), so they belong in investigate-first. Fixing this moved
   44 deltas across the 10 factions from adopt to investigate (233/27 → 189/71). The corrected report
   independently reproduced the exact Hexwarp Thrallband DP change found while building the parser,
   and independently surfaced the `single→esc4` mode change on Drop Pod/Impulsor/Razorback/Rhino/
   Chaos Rhino — matching B94's own 34-unit scope description with no cross-reference between the two.
   Report banked as `MFM_v1_1_Reconciliation.md` (189 adopt-mechanically, 71 investigate-first across
   the 10 factions), registered alongside `MFM_FW_Reconciliation.md`/`MFM_Standalone_Pass.md`. Output
   is B89's work order.
5. **P4 source census updated.** `rules_assertions.py`'s `p4_source_census` static-scans
   `mfm_reconcile.py` (already in `P4_SCANNED`) and flagged the new `MFM_v1_1_Reconciliation.md`
   filename as unregistered; added to `P4_REFERENCED_SOURCES`. `rules_assertions.py` still 116/116.
6. **B95 opened, incidental.** `faction_taxonomy.json` marks Chaos Space Marines and Thousand Sons
   `built: false`; `units.json` already holds real data for both (CSM includes the Rubric Marines
   instance B87 corrected). Found while scoping the reconciliation report to "every built faction" —
   had to use "has rows in `units.json`" rather than the taxonomy flag to get the right 10-file scope.
   Not investigated further, filed for a decision (stale flag vs "built" meaning something narrower).

## State
- Baseline: green at close (pending this handoff's own hash, verified last via `--freshness-check`).
- `index.html` unchanged, still **v6.15**.
- `rules_assertions.py`: 116/116, P4 census updated, no new legality assertion.
- Live behaviour: **unchanged**. `ARMY_TO_MFM` still reads every built army's v1_0 file;
  `detachments.json` not regenerated this session.
- `repo_check` will show drift until pushed: `detachment_parser.py`, `mfm_reconcile.py`,
  `rules_assertions.py`, `baseline.sh`, `pipeline_manifest.py`, `OPEN_ITEMS_BACKLOG.md`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `b88_check.js` (net-new),
  `MFM_v1_1_Reconciliation.md` (net-new), `SESSION_HANDOFF_191.md` (net-new).

## Ryan action required
Push this session's changes.

## Decisions still waiting on Ryan
1. **B94:** copy-4 tier schema — carried over from S190, untouched this session.
2. **B95 (new):** is `faction_taxonomy.json`'s `built: false` for Chaos Space Marines and Thousand
   Sons stale (flip to `true`), or does "built" mean something narrower than "has unit rows" that
   neither has reached yet? See D284 / backlog for detail.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `detachment_parser.py` | 1715a49b1500 | v1.1 sniff + normalize for DETACHMENTS block; v1_0 output byte-identical |
| `mfm_reconcile.py` | b13fee40b951 | generalized from one-off SM pass to 10-faction delta tool |
| `b88_check.js` | 18455c7419dd | net-new; pins v1.1 DETACHMENTS parsing, v1_0 stability, 3 v1.1-exclusive quirks |
| `MFM_v1_1_Reconciliation.md` | 5ebd959dd5b3 | net-new; 189 adopt-mechanically / 71 investigate-first across 10 factions |
| `rules_assertions.py` | 0994f7fbed30 | P4 source census updated for the new report filename; 116/116 unchanged |
| `baseline.sh` | 900ebb9c3e3f | b88_check gate registered |
| `pipeline_manifest.py` | 2f39a4fa3aca | b88_check.js, MFM_v1_1_Reconciliation.md, SESSION_HANDOFF_191.md added to GUARDED |
| `OPEN_ITEMS_BACKLOG.md` | 9c6aa55d14fb | B88 closed; B95 added; 17 open |
| `40K_Decision_Log.md` | cabe12d4aa60 | D284 appended |
| `DECISION_INDEX.md` | bc06f967a896 | D284 index entry |
| `pipeline_manifest.json` | regenerated after this edit | regenerated, `--write` |
| `NEXT_SESSION_PROMPT.md` | (see next file) | S192 (unguarded by design) |
| `SESSION_HANDOFF_191.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
17 open, unchanged in count from S190 (B88 closed, B95 opened). Beginning: B69, B70, B75, B85, B86,
P2, P4, E23, B67b, E12, B17, B88, B89, B90, E28, B93, B94. Resolved: B88 (closed, D284). Added: B95
(D284). Ending: B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, B89, B90, E28, B93, B94, B95.
