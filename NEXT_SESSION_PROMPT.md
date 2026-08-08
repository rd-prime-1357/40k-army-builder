# NEXT SESSION PROMPT — Session 218

## Recommended turn type: data-only (World Eaters units)

Read `SESSION_HANDOFF_217.md` and `WORLD_EATERS_BUILD_SCOPE.md` first. S217 scoped World Eaters
clean: 30 units, 28 Legends exclusions, zero engine gaps, 2 units needing manual loadout authoring.
Baseline should be fully green this session except `repo_check` (B108, pre-existing, your action,
unchanged) — no other known-red carried forward.

Open with `./baseline.sh --fetch --data-turn`. Confirm clean before starting.

## World Eaters units — the work

Per `WORLD_EATERS_BUILD_SCOPE.md` Section 9, step 1:

1. Register `WE` in `units_repro_check.py` and `merge_factions.py` (mirrors the GK/TS/EC block
   pattern exactly — see either script for the shape).
2. Build `units.json` end to end from `MFM_World_Eaters_v1.1.txt` and the Wahapedia CSVs
   (`wahapedia_transform.py` → `mfm_points_parser.py` → `convert_to_json.py`), the same sequence
   the scoping dry run already ran clean.
3. Author the two flagged units:
   - **Jakhals** — new two-option composition (`1 Pack Leader, 1 Dishonoured, 8 Jakhals` for the
     10-model bracket; `1 Pack Leader, 2 Dishonoured, 17 Jakhals` for the 20-model bracket). This
     is a genuinely new shape (confirmed unique in `Datasheets_unit_composition.csv`), not a copy
     of existing precedent — take care with it.
   - **Helbrute** — copy the already-shipped pattern from Death Guard, Chaos Space Marines, or
     Thousand Sons' own Helbrute (`unit_loadouts.json` keys `000000954`, `000001021`, `000001046`)
     — identical sentence, already-solved.
4. Diff-guard the output before banking: confirm exactly 30 World Eaters units added, 0 changed or
   removed elsewhere, `units_repro_check.py` byte-identical.

This is units only — do not touch `detachments.json` (that's the next data turn, per the scope
doc's step 2). Do not touch `wargear_points.json` (all three World Eaters wargear items already
exist there from sibling factions — confirm this stays true, don't regenerate).

## Also open, at your discretion

- **B112** — Chaos Daemons LORDS OF THE WARP disposition, now unblocked (a v1.1 CD MFM file exists
  in the private repo as of S217). Same-pattern data-only fix mirroring D306/D307. Not a World
  Eaters-session fit; its own turn.
- **B113** — detachment enhancement `LEADER:` eligibility restriction discarded as parser noise
  (4 instances across CSM/TS/EC today, 2 more once World Eaters ships). Engine turn, small. Not
  urgent — pre-existing and unenforced on 3 shipped factions already.

## Standing reminders

- Re-derive from source, don't trust prior-session prose.
- Turn typing: World Eaters units is data-only. If it surfaces an engine or tooling need, note it
  for a future typed session — don't fold it into this one.
- No decisions currently waiting on Ryan from S217.

## Close

Produce the four documents, register `SESSION_HANDOFF_218.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
