# SESSION HANDOFF 195

**Turn type:** data-only. B94's data turn (first faction) and B89's first migration both shipped for
Thousand Sons. `index.html` untouched, stays v6.16. `rules_assertions.py` untouched (no TS points
values were pinned; nothing to reconcile).

## What happened
1. **Baseline opened green.** `./baseline.sh --fetch --data-turn`: 32/32 gates pass. Verified S194's
   hashes via `pipeline_manifest.json` (the authoritative source) rather than the handoff table; repo
   matched, confirming the S194 push.
2. **Chose Thousand Sons over Death Guard**, per the prompt's own recommendation — fully self-sourced,
   and S194 had already hand-verified its two esc4 units against the real v1.1 source.
3. **Both MFM source files hash-verified directly** against `source_manifest.json` before use (not
   assumed from the baseline's own pass). Diffed `_v1_0.txt` vs `_v1.1.txt` directly first — confirmed
   real re-pricing exists for this faction, not just layout changes.
4. **First pipeline attempt (no post-processors) produced a false structural diff** — every unit's
   `model_groups` differed by an empty `bodyguard_stat_flags: []` key. Traced before accepting: that key
   is populated by `add_bodyguard_stat_flags.py` (B7b, D157/D159), which runs on the *merged* output
   after `merge_factions.py`, not inside the per-faction build. Rebuilt using the real
   `units_repro_check.py` chain end to end (transform → points → convert → merge → `add_loadout_groups`
   → `add_co_leader` → `add_bodyguard_stat_flags` → `add_chapter_point_overrides`), swapping only
   Thousand Sons' MFM source (`_v1.1.txt`) and adding `--emit-fourth-plus`.
5. **Confirmed all 15 non-Thousand-Sons armies came out byte-identical** to committed `units.json` —
   the post-processors are cross-faction but nothing outside TS's own data moved.
6. **Exactly 12 Thousand Sons units differ, all confined to `points`.** 11 are real re-prices, checked
   one-by-one against `MFM_v1_1_Reconciliation.md`'s pre-existing "adopt-mechanically" list for
   Thousand Sons — exact match. The 12th, Rubric Marines, gains `fourth_plus` (110/200) — B94's target,
   not a v1.1 re-price. Chaos Rhino carries both a real re-price (90→80/90 base) and a new `fourth_plus`
   (90). No diff fell outside the points block.
7. **`rules_assertions.py` checked for pinned Thousand Sons point values** — none exist (the suite pins
   roster/detachment counts and structural facts, never a specific price), so nothing needed
   reconciling. 118/118 still passes unmodified.
8. **`source_manifest.json` required no change** — both `_v1.1.txt` and `_v1_0.txt` were already present
   and correctly hashed; this migration doesn't add or retire a source file (`_v1_0.txt` stays required
   for CSM's cult-troop cross-legion pricing, which reads Rubric Marines' CSM-army datasheet price from
   it until CSM's own B89 turn).
9. **Left untouched, already tracked, out of scope:** Thousand Sons' 4 investigate-first items from the
   reconciliation report — a Defiler wargear removal (`wargear_points.json`) and 3 detachment
   force-disposition/unique-tag changes (`detachments.json`). Neither file is touched by a units-only
   data turn.
10. **`units_repro_check.py` updated** (a change to the check, not the pipeline, per the prompt's own
    scoping): added `MFM_Thousand_Sons_v1.1.txt` to `REQUIRED` (kept `_v1_0.txt` for the CSM
    cross-reference above), swapped the TS build block to `_v1.1.txt` + `--emit-fourth-plus`, updated
    the docstring. Re-ran: green, byte-identical to the now-regenerated committed `units.json`.
11. **`units.json` regenerated and committed** — full 16-army merged output from the real pipeline.
12. Decision log (D288) and backlog updated; manifest regenerated last with `--write`, then
    `pipeline_manifest.py --freshness-check` run as the final command.

## State
- Baseline: green at close (`--no-repo`; repo_check pending push). All 29 local gates pass.
- `index.html`: untouched, **v6.16**.
- `rules_assertions.py`: untouched, 118/118 (no TS points-value assertions existed to reconcile).
- `units.json`: **regenerated** — Thousand Sons' 12 units carry new points, Rubric Marines and Chaos
  Rhino carry `fourth_plus`. All other 15 armies byte-identical to the prior committed file.
- `units_repro_check.py`: Thousand Sons block now builds from `_v1.1.txt` with `--emit-fourth-plus`;
  `_v1_0.txt` stays in `REQUIRED` for CSM's cult-troop cross-reference.
- `source_manifest.json`: unchanged — both TS source files were already correctly hashed.
- `OPEN_ITEMS_BACKLOG.md`: 19 open, unchanged count — B94 and B89 both advanced (first faction/first
  migration) but neither closes; both still need the remaining priority-order factions.
- `pipeline_manifest.json`: regenerated at close, 153 guarded files.
- `repo_check` will show drift until pushed: `units.json`, `units_repro_check.py`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`,
  `pipeline_manifest.json`, `NEXT_SESSION_PROMPT.md`, `SESSION_HANDOFF_195.md` (net-new).

## Ryan action required
1. Push this session's changes.
2. No file-list screenshot needed — nothing this session turned on project-area presence/absence.

## Decisions still waiting on Ryan
None outstanding. Faction choice (Thousand Sons over Death Guard) was a dev-manager sequencing call,
made per the prompt's own recommendation and recorded here rather than surfaced.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | 564045f11889 | Thousand Sons: 12 units' points updated, 2 gain `fourth_plus` |
| `units_repro_check.py` | 449dc469f472 | TS block: `_v1.1.txt` + `--emit-fourth-plus`; `_v1_0.txt` kept in REQUIRED |
| `40K_Decision_Log.md` | bf1977968bb9 | D288 appended |
| `DECISION_INDEX.md` | c9170d9f637b | D288 index entry |
| `OPEN_ITEMS_BACKLOG.md` | f8b334b9cc6c | B94 + B89 updated with S195 progress; 19 open |
| `pipeline_manifest.py` | (verify at open) | `SESSION_HANDOFF_195.md` registered in GUARDED |
| `pipeline_manifest.json` | regenerated at close | `--write`, 154 guarded files (final pass, includes this handoff) |
| `NEXT_SESSION_PROMPT.md` | (unguarded by design) | S196 (B89's second migration) |
| `SESSION_HANDOFF_195.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
19 open, unchanged from S195 open. Beginning: B99, B98, B97, E28, B93, B90, B94, B89, B85, B86, B69,
B70, B75, P2, P4, E23, B67b, E12, B17 (19). Resolved: none. Added: none. Ending: same 19 — B94 and B89
both advanced (Thousand Sons migrated) but neither ticket closes; each still spans the remaining
priority-order factions.
