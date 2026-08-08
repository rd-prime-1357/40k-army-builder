# SESSION HANDOFF 218

**Turn type:** data-only (World Eaters units — per `WORLD_EATERS_BUILD_SCOPE.md` §9 step 1).
`units.json`, `unit_loadouts.json` shipped end to end. `detachments.json` and `wargear_points.json`
beyond the two surfaced items were deliberately untouched, per scope.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: 33/34 gates green. The one
   red was the documented, expected pre-existing B108 finding (unchanged, your action). Private
   source repo fetched and verified fresh: 85/85 source files byte-match `source_manifest.json`.

2. **`units.json` built.** `wahapedia_transform.py` → `mfm_points_parser.py` → `convert_to_json.py`
   against `MFM_World_Eaters_v1.1.txt`, mirroring the Grey Knights/Emperor's Children shape exactly.
   Diff-guarded: **30 units added, 0 changed, 0 removed elsewhere.** `abilities.json` gained 39 World
   Eaters entries (0 changed/removed); `rules.json`/`keywords.json`/`weapon_abilities.json`
   unaffected. `faction_taxonomy.json` deliberately untouched — World Eaters' `built` flag stays
   `false` until detachments ship (same call as Grey Knights at D298).

3. **`units_repro_check.py` updated.** World Eaters block added (REQUIRED list, transform/points/
   convert calls, merge input). In the same edit, `MFM_Emperors_Children_v1.1.txt` was added to
   `REQUIRED` — a pre-existing small gap (the pipeline call already referenced it; it just wasn't
   preflight-checked), closed alongside World Eaters' own addition.

4. **`unit_loadouts.json` built.** `repro_check.py`: `WE` added to `FACTIONS`; Jakhals (`000002628`)
   added to `HAND_AUTHORED`. Jakhals' composition is a genuinely new two-option shape joined by a
   bare `or:` line tying two size brackets (10-model: 1 Pack Leader, 1 Dishonoured, 8 Jakhals;
   20-model: 1 Pack Leader, 2 Dishonoured, 17 Jakhals) — `classify_comp_row`'s OR-profile split only
   recognises a literal `OR` line, so this is authored directly using the `per_bracket` schema
   already shipped for 000004175/000004182, not a parser extension. Default weapons per named group
   read directly off the datasheet's own loadout prose — Dishonoured carry no sidearm, confirmed by
   the text's own omission, not assumed. Three options authored (per-10 chainblade→mauler chainblade
   swap; any-number paired manglers→skullsmasher and mangler swap; per-10 Icon of Khorne add), each
   matching an already-shipped sentence shape. Helbrute (`000002632`) needed no hand authoring — the
   real parser run resolved it automatically with the same `UNMATCHED` flag already accepted on
   Death Guard/CSM/Thousand Sons' own Helbrutes. Full regen (loadout_parser.py + the seven-faction
   equipped_parser.py web-pass chain + the final `--datasheets` pass) diff-guarded: **30 entries
   added (29 auto + 1 hand-authored), 0 changed, 0 removed elsewhere.**

5. **A test-harness false alarm, investigated and closed, not shipped as a finding.** Mid-session, a
   diagnostic run appeared to show three unrelated units (Deathwatch Veterans `000002783`, a Space
   Marine jump-pack kill team `000003874`, Space Wolves Thunderwolf Cavalry `000000322`) changing as
   a side effect of adding World Eaters. Traced to a mistake in my own seed file construction — it
   accidentally carried the *entire* committed `unit_loadouts.json` instead of just the six true
   hand-authored entries, so those three already-fully-processed units ran through the
   `equipped_parser.py` fan/dedup chain a second time on top of already-fanned data. Rebuilding with
   a seed matching `repro_check.py`'s own construction exactly reproduced all three untouched — no
   engine issue, confirmed by full byte-diff before anything was banked.

6. **Companion literal/regen updates, all verified before changing:**
   - `rules_assertions.py`'s `ALLIED_CARRIER_GROUPS` (B61): World Eaters' five Blood Legions
     carriers (Skarbrand, Bloodthirster, Bloodletters, Bloodcrushers, Flesh Hounds) added, mirroring
     D305's Emperor's Children precedent. B61-1/2/3 all iterate this one dict; one edit closed all
     three.
   - `wargear_points.json` (E14-1) regenerated from the real parser across every `MFM_*.txt` file
     including World Eaters' now-present source. Diff-guarded: **2 units added** (Forgefiend 5 pts
     Ectoplasma cannon; Defiler 15/15 pts Hades lascannon/Heavy reaper autocannon), **0 changed/
     removed elsewhere** — matching `WORLD_EATERS_BUILD_SCOPE.md` §5's forecast exactly.
   - `rules_assertions.py`'s E14-2 literal: World Eaters contributes 10 qualifying free-add options
     across 8 units. Verified by full per-army breakdown before updating the literal — every other
     army's count summed to exactly the prior 98/67 unchanged. 98/67 → 108/75.
   - `datasheet_wargear_abilities.json` regenerated: **5 World Eaters datasheets added, 0 changed/
     removed elsewhere.**

7. **Full baseline re-run** after all six file updates: every gate green except the expected
   pre-`--write` P3/`pipeline_manifest`/`repo_check` state (files changed this session, not yet
   re-pinned — resolved by the `--write` at the end of this handoff).

## State at close

- `units.json`, `unit_loadouts.json`, `abilities.json`, `wargear_points.json`,
  `datasheet_wargear_abilities.json`: all updated, diff-guarded, byte-verified.
- `units_repro_check.py`, `repro_check.py`, `rules_assertions.py`: updated (World Eaters
  registration, EC `REQUIRED` gap closed, `ALLIED_CARRIER_GROUPS` + E14-2 literal).
- `40K_Decision_Log.md`: D312 appended. `DECISION_INDEX.md`: D312 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: no ticket opened or closed (faction-build turn, not a ticket turn);
  ledger header updated to S218, count unchanged at 23.
- `detachments.json`, `faction_taxonomy.json`, `index.html`: untouched, per scope.
- `pipeline_manifest.py`: `SESSION_HANDOFF_218.md` registered in GUARDED before `--write`.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged;
   ideally scrub git history), and push it to the private source repo.
2. Push this session's changed/new files to the public repo (listed below).

## Decisions waiting on Ryan

None. World Eaters units shipping surfaced zero "how it works" questions — every ambiguity
(Jakhals' composition shape, Dishonoured's missing sidearm) resolved directly from source text.

## Files (SHA-256, first 12)

Verify these at S219 open.

| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | `10e8b8d7517e` | +30 World Eaters units |
| `unit_loadouts.json` | `36cbbaf75e1c` | +30 World Eaters entries (29 auto + Jakhals hand-authored) |
| `abilities.json` | `a8e0d410f0fa` | +39 World Eaters abilities |
| `wargear_points.json` | `0d553d723bda` | +2 units (Forgefiend, Defiler) |
| `datasheet_wargear_abilities.json` | `82946ea169be` | +5 World Eaters datasheets |
| `units_repro_check.py` | `6249e75d755c` | WE block added; EC `REQUIRED` gap closed |
| `repro_check.py` | `5bd1e02a9168` | WE added to FACTIONS; Jakhals added to HAND_AUTHORED |
| `rules_assertions.py` | `10082f064f18` | ALLIED_CARRIER_GROUPS + E14-2 literal updated for WE |
| `40K_Decision_Log.md` | `1c54119c1916` | D312 appended |
| `DECISION_INDEX.md` | `a8b58ad1b23b` | D312 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `f163ea0f1738` | ledger header S218, count unchanged (23) |
| `pipeline_manifest.py` | (pre-`--write`; re-pinned by `--write`) | `SESSION_HANDOFF_218.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S219 |
| `SESSION_HANDOFF_218.md` | (this file) | |

## Net New Files

None. Every file touched this session is a versioned pipeline output or an existing script/doc
update — no new file role was introduced.

## Backlog

23 open at S217 close; 23 open here (no ticket opened or closed — a faction-build data turn).
Beginning: B113, B110, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2,
P4, E23, B67b, E12, B17, B112 (23). Resolved: none (0). Added: none (0). Ending: B113, B110, B108,
B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17, B112
(23).
