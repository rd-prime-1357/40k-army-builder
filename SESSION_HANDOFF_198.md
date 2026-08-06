# SESSION HANDOFF 198

**Turn type:** data-only. B89's fourth migration shipped: the six-file Space Marines group (base +
Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves) moved to MFM v1.1 as one atomic
turn. `index.html` untouched, stays v6.16.

## What happened
1. **Baseline opened green.** `./baseline.sh --fetch --data-turn`: 32/32 gates pass.
2. **Resolved S197's open chaining question.** Traced (not guessed) how
   `add_chapter_point_overrides.py` derives chapter overrides: it compares each chapter's shared-unit
   prices against the *current* generic Adeptus Astartes price on every build, re-parsing all five
   chapter MFM files itself from its own hardcoded list. If base and any chapter sit at different MFM
   versions, that comparison is version-mismatched and corrupts every affected chapter's overrides —
   confirmed the six-file group cannot split faction-by-faction like CD/DG/TS did.
3. **Confirmed this does not need new tooling.** `mfm_points_parser.py`'s `FACTION_BY_MFM` dict already
   has all six v1.1 filenames mapped (done ahead of time under B87/D275). `rules_assertions.py`'s P4
   source census regex only matches underscore-style filenames, so dot-versioned v1.1 filenames are
   invisible to it and it needed no update (same reason TS/DG's v1.1 filenames were never added there).
   The only real edit: synchronize the hardcoded v1_0 filenames to v1.1 in two places —
   `units_repro_check.py` (SM `--mfm` arg, `CHAPTER_POINTS` list, `REQUIRED` list) and
   `add_chapter_point_overrides.py` (`CHAPTERS` list).
4. **Ran the real pipeline** (via `units_repro_check.py`'s own `repro()`, wrapped to preserve the temp
   dir instead of deleting it, so the rebuilt `units.json` could be inspected before promotion).
5. **Found a genuine source-text defect, not shipped silently.** The first pipeline run surfaced 47
   changed units; 46 fit the expected shape (points changes) but one — Marneus Calgar in Armour of
   Antilochus — also lost two units from his `leader_eligible_units`. Traced to
   `MFM_Space_Marines_v1.1.txt`'s raw LEADER line: `...ERADICATOR SQUAD STERNGUARD VETERAN SQUAD...`,
   missing the comma between the two unit names. The parser correctly drops the resulting unresolvable
   glued token (by design, per B73/D260) — this is a transcription defect in the source text, not a
   parser bug or a genuine v1.1 rules change (both squads are legal units, comma-separated correctly in
   the v1_0 file). Wrote a detector (does a dropped attach-list token split cleanly into 2-3 known
   current unit names with no separator) and ran it against all six SM-family files' validation
   reports — confirmed isolated to this one instance, not systemic.
6. **Stopgap-fixed in `mfm_points_parser.py`**, per Ryan's "continue" after the finding was flagged: a
   new `_KNOWN_SOURCE_FIXES` dict does a literal, filename-and-substring-scoped find/replace on the raw
   text before parsing, and raises loudly if the expected substring isn't found (so it can't silently
   no-op if the source changes underneath it). Not a general glue-detection heuristic — scoped to this
   one known defect only. Re-ran the pipeline: Calgar's leader list now matches the correct (v1_0-
   equivalent-plus-legitimate-v1.1-changes) shape exactly.
7. **Diff-guard confirmed scope.** 47 unit_ids changed, all six confined to the SM-family armies
   (Adeptus Astartes 14, Ultramarines 8, Dark Angels 9, Space Wolves 7, White Scars 1, Black Templars
   8). All ten other armies, all four merged lookups (`abilities.json`, `rules.json`, `keywords.json`,
   `weapon_abilities.json`), and `faction_taxonomy.json` confirmed byte-identical. Fields touched:
   `points` (47), `chapter_point_overrides` (2 — Inceptor Squad newly gains four chapter overrides at
   v1.1's changed base price; Vanguard Veteran Squad With Jump Packs' existing Blood Angels override
   re-prices from 105/210 to 110/220), `model_groups` (1 — Uriel Ventris legitimately gains Victrix
   Honour Guard as an attach option, confirmed correct/comma-separated in the raw v1.1 text).
8. **`rules_assertions.py` checked for pinned points values** on all 47 changed unit_ids. One hit:
   `b56a_bt_negative_control` pinned the Impulsor's Adeptus-Astartes-vs-Black-Templars distinctness
   check to the v1_0 values (80/85). Reconciled to the new v1.1 values (70/75) — the distinctness the
   control actually checks (BT's own datasheet stays different from the generic one) is unchanged,
   only the absolute numbers moved. 118/118 after reconciliation.
9. **Full local baseline re-run clean** (`--no-repo`; sources already local from this session's fetch):
   29/29 gates pass before the manifest regenerate; `pipeline_manifest` gate itself expectedly failed
   until step 10.
10. `SESSION_HANDOFF_198.md` registered in `pipeline_manifest.py`'s GUARDED list, then manifest
    regenerated with `--write`, then `pipeline_manifest.py --freshness-check` run last.
11. Decision log (D291) and its index entry, and backlog (B89) updated.

## What's explicitly not done
`detachments.json` scope untouched, tracked separately per the CD/DG/TS convention — the raw v1.1 diff
showed Black Templars gaining a new VENGEFUL HOSTS detachment and several enhancement re-prices across
the six files; not investigated in detail this turn, flagged for whoever picks up the SM-chain
detachments migration.

## State
- Baseline: green at close (`--no-repo`; `repo_check` pending push). 29/29 local gates pass.
- `index.html`: untouched, **v6.16**.
- `units.json`: **regenerated** — 47 units changed across the six SM-family armies as described above;
  all other 10 armies and all four merged lookups byte-identical.
- `units_repro_check.py`: SM base + 5 chapter filenames now point at v1.1; `REQUIRED` list updated.
- `add_chapter_point_overrides.py`: `CHAPTERS` list now v1.1.
- `mfm_points_parser.py`: new `_KNOWN_SOURCE_FIXES` stopgap dict, one entry (Calgar glued token).
  **Remove this entry once the private-repo source fix lands.**
- `rules_assertions.py`: `b56a_bt_negative_control` reconciled 80/85 -> 70/75. 118/118.
- `OPEN_ITEMS_BACKLOG.md`: 19 open, unchanged count — B89 advanced (fourth migration, largest so far)
  but doesn't close; still spans the remaining priority-order factions.
- `pipeline_manifest.json`: regenerated at close, 157 guarded files (SESSION_HANDOFF_198.md added).
- `repo_check` will show drift until pushed: `units.json`, `units_repro_check.py`,
  `add_chapter_point_overrides.py`, `mfm_points_parser.py`, `rules_assertions.py`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`,
  `pipeline_manifest.json`, `NEXT_SESSION_PROMPT.md`, `SESSION_HANDOFF_198.md` (net-new).

## Ryan action required
1. **Push the missing-comma fix to the private `rd-prime-1357-data-sources` repo's
   `MFM_Space_Marines_v1.1.txt`** — the LEADER line for Marneus Calgar in Armour of Antilochus needs a
   comma inserted between "ERADICATOR SQUAD" and "STERNGUARD VETERAN SQUAD". Once pushed and the
   private repo's hash is confirmed, the `_KNOWN_SOURCE_FIXES` stopgap in `mfm_points_parser.py` should
   be removed (it will raise loudly and fail the build if it's left in place after the source no longer
   contains the glued substring, which is by design — it won't silently linger unnoticed).
2. Push this session's public-repo changes (see file list above).
3. No file-list screenshot needed — nothing this session turned on project-area presence/absence.

## Decisions still waiting on Ryan
None outstanding for this session's own scope. The stopgap-vs-source-fix choice was raised as a
decision mid-session; Ryan's "continue" was taken as approval to apply the documented, reversible
parser-side stopgap now (rather than block the session on a private-repo push), with the source repo
still flagged as the durable fix above.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | fd3cf67a876a | 47 SM-family units updated |
| `units_repro_check.py` | 88dcc8708eef | SM chain filenames -> v1.1 |
| `add_chapter_point_overrides.py` | d674545bd261 | `CHAPTERS` list -> v1.1 |
| `mfm_points_parser.py` | 3b64d8dc5227 | `_KNOWN_SOURCE_FIXES` stopgap added |
| `rules_assertions.py` | 8b43dc4dba5f | `b56a_bt_negative_control` reconciled to 70/75 |
| `40K_Decision_Log.md` | a93b3e46cc11 | D291 appended |
| `DECISION_INDEX.md` | 00e3e65821e1 | D291 index entry |
| `OPEN_ITEMS_BACKLOG.md` | 45a8a4ac13cf | B89 updated with S198 progress; 19 open |
| `pipeline_manifest.py` | bce5bc014da3 | `SESSION_HANDOFF_198.md` registered in GUARDED |
| `pipeline_manifest.json` | df971abed5ed | `--write`, 157 guarded files (final pass) |
| `NEXT_SESSION_PROMPT.md` | 3c791bd46506 | (unguarded by design) S199 |
| `SESSION_HANDOFF_198.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
19 open, unchanged from S197 open. Beginning: B99, B98, B97, E28, B93, B90, B94, B89, B85, B86, B69,
B70, B75, P2, P4, E23, B67b, E12, B17 (19). Resolved: none. Added: none. Ending: same 19 — B89 advanced
(six-file SM group migrated, fourth and largest migration of the arc) but doesn't close; still spans
the remaining priority-order factions.
