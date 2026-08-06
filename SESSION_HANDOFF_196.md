# SESSION HANDOFF 196

**Turn type:** data-only. B94's data turn (second faction) and B89's second migration both shipped for
Death Guard. `index.html` untouched, stays v6.16. `rules_assertions.py` untouched (no Death Guard points
values were pinned; nothing to reconcile).

## What happened
1. **Baseline opened green.** `./baseline.sh --fetch --data-turn`: 32/32 gates pass. Verified S195's
   hashes via `pipeline_manifest.json` (the authoritative source) rather than the handoff table; repo
   matched, confirming the S195 push.
2. **Chose Death Guard**, per the S196 prompt's own recommendation — same simple shape as Thousand Sons:
   fully self-sourced, no chapter points, no cross-file cult-troop append inside its own build.
3. **Both MFM source files hash-verified directly** against `source_manifest.json` before use. Diffed
   `_v1_0.txt` vs `_v1.1.txt` directly first — confirmed real re-pricing exists, not just layout changes.
   Every `▲`/`▼` price-change marker in the raw v1.1 source was traced to a specific unit before running
   the pipeline, per the prompt's caution not to assume the pre-computed reconciliation report is
   complete.
4. **Found the reconciliation report wrong on one point**: `MFM_v1_1_Reconciliation.md` lists Defiler's
   Hades lascannon and Heavy reaper autocannon as "removed" under v1.1. The raw source shows both still
   present on Defiler, each simply repriced 10→15 pts. Out of scope either way (`wargear_points.json`,
   not touched by a units-only turn) but the report's characterization should not be trusted verbatim
   when that file is eventually worked — flagged in the decision log and backlog, not corrected in the
   report itself this turn.
5. **Full pipeline chain run** (transform → points → convert → merge → `add_loadout_groups` →
   `add_co_leader` → `add_bodyguard_stat_flags` → `add_chapter_point_overrides`), swapping only Death
   Guard's MFM source (`_v1.1.txt`) and adding `--emit-fourth-plus`, mirroring S195's approach exactly.
6. **Confirmed all 15 non-Death-Guard armies came out byte-identical** to committed `units.json`.
7. **Exactly 5 Death Guard units differ, all confined to `points`**, matching
   `MFM_v1_1_Reconciliation.md`'s pre-existing "adopt-mechanically" list for Death Guard exactly:
   Plague Marines (190→180 at 10 models), Chaos Rhino (85→75/85, gains `fourth_plus` — B94's second
   faction), Deathshroud Terminators (320/330→305/315 at 6 models), Mortarion (400→390), Defiler
   (290/320→300/340). No diff fell outside the points block.
8. **`rules_assertions.py` checked for pinned Death Guard point values** on all five changed units —
   none exist (Plague Marines' per-5 wargear-swap checks and the allied-carrier tagging reference its
   unit ID structurally, never a specific points number), so nothing needed reconciling. 118/118 still
   passes unmodified — confirmed both against the prior committed file and, via a temporary file swap,
   against the regenerated one (only the expected repro/manifest-drift assertions moved during the
   swap, nothing else).
9. **`source_manifest.json` required no change** — both `_v1.1.txt` and `_v1_0.txt` were already present
   and correctly hashed; this migration doesn't add or retire a source file (`_v1_0.txt` stays required
   for CSM's cult-troop cross-legion pricing, which reads Plague Marines' CSM-army datasheet price from
   it until CSM's own B89 turn).
10. **Left untouched, already tracked, out of scope:** Death Guard's 2 investigate-first items from the
    reconciliation report — the Defiler wargear repricing above (`wargear_points.json`) and the
    CONTAGION ENGINES detachment force-disposition change (`detachments.json`). Neither file is touched
    by a units-only data turn.
11. **`units_repro_check.py` updated** (a change to the check, not the pipeline, per the prompt's own
    scoping): added `MFM_Death_Guard_v1.1.txt` to `REQUIRED` (kept `_v1_0.txt` for the CSM
    cross-reference above), swapped the Death Guard build block to `_v1.1.txt` + `--emit-fourth-plus`,
    updated the docstring. Re-ran: green, byte-identical to the now-regenerated committed `units.json`.
12. **`units.json` regenerated and committed** — full 16-army merged output from the real pipeline.
13. Decision log (D289) and backlog updated; manifest regenerated last with `--write`, then
    `pipeline_manifest.py --freshness-check` run as the final command.

## State
- Baseline: green at close (`--no-repo`; `repo_check` pending push). All 29 local gates pass.
- `index.html`: untouched, **v6.16**.
- `rules_assertions.py`: untouched, 118/118 (no Death Guard points-value assertions existed to
  reconcile).
- `units.json`: **regenerated** — Death Guard's 5 units carry new points, Chaos Rhino carries
  `fourth_plus`. All other 15 armies byte-identical to the prior committed file.
- `units_repro_check.py`: Death Guard block now builds from `_v1.1.txt` with `--emit-fourth-plus`;
  `_v1_0.txt` stays in `REQUIRED` for CSM's cult-troop cross-reference.
- `source_manifest.json`: unchanged — both Death Guard source files were already correctly hashed.
- `OPEN_ITEMS_BACKLOG.md`: 19 open, unchanged count — B94 and B89 both advanced (second faction/second
  migration) but neither closes; both still need the remaining priority-order factions.
- `pipeline_manifest.json`: regenerated at close, 154 guarded files.
- `repo_check` will show drift until pushed: `units.json`, `units_repro_check.py`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`,
  `pipeline_manifest.json`, `NEXT_SESSION_PROMPT.md`, `SESSION_HANDOFF_196.md` (net-new).

## Ryan action required
1. Push this session's changes.
2. No file-list screenshot needed — nothing this session turned on project-area presence/absence.

## Decisions still waiting on Ryan
None outstanding. Faction choice (Death Guard, the prompt's own recommendation) was a dev-manager
sequencing call, recorded here rather than surfaced. The reconciliation-report correction (Defiler
wargear repriced, not removed) is a factual finding, not a decision — no product call attached to it
yet, since `wargear_points.json` hasn't been touched.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | 3dd1e3d96188 | Death Guard: 5 units' points updated, 1 gains `fourth_plus` |
| `units_repro_check.py` | 473dc9a38c55 | DG block: `_v1.1.txt` + `--emit-fourth-plus`; `_v1_0.txt` kept in REQUIRED |
| `40K_Decision_Log.md` | 542c44575f58 | D289 appended |
| `DECISION_INDEX.md` | 07dcc1cd40a0 | D289 index entry |
| `OPEN_ITEMS_BACKLOG.md` | c3f72f4faf79 | B94 + B89 updated with S196 progress; 19 open |
| `pipeline_manifest.py` | f17acc69a2f4 | `SESSION_HANDOFF_196.md` registered in GUARDED |
| `pipeline_manifest.json` | regenerated at close | `--write`, 154 guarded files (final pass, includes this handoff) |
| `NEXT_SESSION_PROMPT.md` | (unguarded by design) | S197 (B89's third migration) |
| `SESSION_HANDOFF_196.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
19 open, unchanged from S196 open. Beginning: B99, B98, B97, E28, B93, B90, B94, B89, B85, B86, B69,
B70, B75, P2, P4, E23, B67b, E12, B17 (19). Resolved: none. Added: none. Ending: same 19 — B94 and B89
both advanced (Death Guard migrated) but neither ticket closes; each still spans the remaining
priority-order factions.
