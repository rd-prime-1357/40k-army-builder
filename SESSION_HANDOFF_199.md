# SESSION HANDOFF 199

**Turn type:** data-only. B89's fifth migration shipped: Chaos Space Marines regenerated to MFM v1.1.
`index.html` untouched, stays v6.16.

## What happened
1. **Baseline opened green.** `./baseline.sh --fetch --data-turn`: 32/32 gates pass. Confirmed the
   private repo's `MFM_Space_Marines_v1.1.txt` **still has** the missing-comma defect from S198 (not
   yet pushed by Ryan) — the `_KNOWN_SOURCE_FIXES` stopgap in `mfm_points_parser.py` is still needed
   and still working correctly.
2. **Checked S198's carried-forward "CSM blocked on World Eaters/Emperor's Children" assumption against
   source, rather than repeating it a third time.** `CSM_BUILD_SCOPE.md` and `units_repro_check.py`'s
   own `CSM_CULT_TROOP_POINTS` mechanism confirm the cult-troop cross-reference (Khorne Berzerkers,
   Plague Marines, Rubric Marines, Noise Marines) only ever needs the sibling legion's raw MFM *text* —
   isolated to one row of CSM's own `Unit_Stats.csv` via `_scope_stats_csv`, never a full built army
   for World Eaters or Emperor's Children. Confirmed `MFM_World_Eaters_v1.1.txt` and
   `MFM_Emperors_Children_v1.1.txt` both exist and both still price their respective cult-troop unit.
   **The blocker was stale, not real** — it applied to the original 2023-era build question (did the
   pricing mechanism exist at all), not to migrating an already-built CSM.
3. **Also checked Grey Knights**, S198's other suggested candidate: not in `units.json`'s army list at
   all — never built, v1_0 or otherwise. Not a migration candidate; needs a full faction build first,
   out of B89's scope.
4. **Synchronized five filenames to v1.1** in `units_repro_check.py`: CSM's own `--mfm` arg, the
   `REQUIRED` list (CSM + all four siblings), and `CSM_CULT_TROOP_POINTS`. No chaining question like
   S198's SM group — CSM has no chapter/sub-faction split (`CSM_BUILD_SCOPE.md` §0), same self-sourced
   shape as TS/DG.
5. **Ran S198's glued-token detector** (built to catch a dropped attach-list entry that's really two
   known unit names glued together with a missing comma) against CSM's own v1.1 validation report —
   none found. No source-text defect this time.
6. **Diff-guard confirmed scope.** 19 unit_ids changed, all Chaos Space Marines, confined to `points`.
   All 15 other armies and all four merged lookups (`abilities.json`, `rules.json`, `keywords.json`,
   `weapon_abilities.json`) plus `faction_taxonomy.json` byte-identical. Includes Khorne Berzerkers and
   Plague Marines' cult-troop cross-reference re-pricing; Rubric Marines and Noise Marines re-ran but
   produced unchanged values (not a bug — their v1.1 sibling prices happen to match v1_0).
7. **`rules_assertions.py` checked for pinned points values** on all 19 changed unit_ids — none found.
   118/118 unmodified.
8. **Full local baseline re-run clean** (`--no-repo`): 27/29 before the manifest regenerate (the two
   expected P3/manifest fails), clean after.
9. `SESSION_HANDOFF_199.md` registered in `pipeline_manifest.py`'s GUARDED list, manifest regenerated
   with `--write`, `pipeline_manifest.py --freshness-check` run last.
10. Decision log (D292) and index, and backlog (B89) updated.

## What's explicitly not done
`detachments.json` scope untouched (CSM's 17 detachments, enhancement re-prices) — tracked separately
per the standing convention, same as the SM chain's own detachments side from S198.

## State
- Baseline: green at close (`--no-repo`; `repo_check` pending push — S198's changes also still
  unpushed). Local gates pass.
- `index.html`: untouched, **v6.16**.
- `units.json`: **regenerated** — 19 Chaos Space Marines units changed (see decision log for the full
  list); all else byte-identical, including S198's 47 SM-family units from the prior commit.
- `units_repro_check.py`: CSM + 4 sibling filenames now v1.1.
- `rules_assertions.py`: untouched, 118/118.
- `mfm_points_parser.py`: unchanged this session — the S198 `_KNOWN_SOURCE_FIXES` stopgap is still
  present and still needed (confirmed the private repo hasn't been fixed yet).
- `OPEN_ITEMS_BACKLOG.md`: 19 open, unchanged count — B89 advanced (fifth migration) but doesn't close.
  **With this migration, every currently-built faction (all 16 armies) is now at MFM v1.1.** Flagged in
  the backlog as a scope-completion point worth discussing with Ryan.
- `pipeline_manifest.json`: regenerated at close, 158 guarded files (SESSION_HANDOFF_199.md added).
- `repo_check` will show drift until pushed: everything from S198's list, plus this session's
  `units.json`, `units_repro_check.py`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `pipeline_manifest.json`, `NEXT_SESSION_PROMPT.md`,
  `SESSION_HANDOFF_199.md` (net-new).

## Ryan action required
1. Same S198 item, still open: **push the missing-comma fix to the private repo's
   `MFM_Space_Marines_v1.1.txt`** (Marneus Calgar's LEADER line). Confirmed this session it still hasn't
   landed — the stopgap is doing its job in the meantime.
2. Push S198's and this session's public-repo changes together (nothing has been pushed since S197).
3. **Product/sequencing question, not urgent:** with every built faction now at v1.1, B89 has no more
   already-built stragglers to migrate — its remaining work is "migrate whichever of Grey Knights,
   World Eaters, or Emperor's Children gets built next," which only makes sense once one of those full
   builds is scheduled. Worth deciding whether B89 should be marked functionally complete for now (with
   a note to reopen per-faction as builds land) or left open as-is. Not blocking — flagging for your
   call whenever convenient.
4. No file-list screenshot needed — nothing this session turned on project-area presence/absence.

## Decisions still waiting on Ryan
None blocking. Item 3 above is a sequencing/labeling question, not a blocker — I'll continue treating
B89 as open (current state) until told otherwise.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | a247b761576b | 19 Chaos Space Marines units updated |
| `units_repro_check.py` | aeac0f5950e5 | CSM + 4 sibling filenames -> v1.1 |
| `40K_Decision_Log.md` | 928132daedbe | D292 appended |
| `DECISION_INDEX.md` | 2723e9c58bf1 | D292 index entry |
| `OPEN_ITEMS_BACKLOG.md` | 94fd1b90f3be | B89 updated with S199 progress; 19 open |
| `pipeline_manifest.py` | cff0a9514d78 | `SESSION_HANDOFF_199.md` registered in GUARDED |
| `pipeline_manifest.json` | (regenerated) | `--write`, 158 guarded files (final pass) |
| `NEXT_SESSION_PROMPT.md` | (unguarded by design) | S200 |
| `SESSION_HANDOFF_199.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
19 open, unchanged from S198 open. Beginning: B99, B98, B97, E28, B93, B90, B94, B89, B85, B86, B69,
B70, B75, P2, P4, E23, B67b, E12, B17 (19). Resolved: none. Added: none. Ending: same 19 — B89 advanced
(fifth migration; every built faction now at v1.1) but doesn't close.
