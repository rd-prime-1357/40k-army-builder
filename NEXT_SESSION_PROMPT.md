# NEXT SESSION PROMPT — Session 217

## Recommended turn type: scoping-only (World Eaters — next faction in priority order)

Read `SESSION_HANDOFF_216.md` first. S216 closed B111 (data half — `wargear_points.json`
regenerated from v1.1, D310; tooling half was D309). Baseline should be fully green this session
except `repo_check` (B108, pre-existing, your action, unchanged) — no other known-red carried
forward.

Open with `./baseline.sh --fetch --data-turn` (sources still needed for a scoping pass that will
read MFM/Datasheets source files, even though nothing gets regenerated). Confirm clean before
starting.

## World Eaters scoping — the work

All of Heretic Astartes except World Eaters is now built (Chaos Space Marines, Thousand Sons,
Death Guard, Emperor's Children). World Eaters is next in the standing priority order. Produce
`WORLD_EATERS_BUILD_SCOPE.md` following the `CSM_BUILD_SCOPE.md` / `EMPEROR_S_CHILDREN_BUILD_SCOPE.md`
pattern: unit list from source (`MFM_World_Eaters_v1.1.txt`, `Datasheets.csv` and siblings,
`World_Eaters_web.txt` if present in the private repo — check, don't assume), leader/support
attachment mapping, wargear cost items, detachment list, any faction-specific mechanism that
doesn't fit the existing engine cleanly (flag those explicitly — they're "how it works" questions
for Ryan, not build-it-yourself calls).

This is scoping only — no committed pipeline file touched (not `units.json`, not
`unit_loadouts.json`, not `wargear_points.json`, not `detachments.json`). That's what makes it a
separate session from any data turn. Re-derive every fact from source; do not carry forward
assumptions from the other four Heretic Astartes builds about how World Eaters' unit or
detachment shape works — check.

## Also open, at your discretion

- **B110** — Grey Knights `faction_taxonomy.json` `built: false` until it has detachments
  (`detachments.json` has zero GK entries). No change since S211. Not a scoping-session fit;
  leave for its own data/engine turn.
- **B112** — Chaos Daemons LORDS OF THE WARP disposition unverified against v1.1; blocked until GW
  publishes a v1.1 CD detachment file. Just check whether one exists yet in the private repo.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — this is what caught the B111
  not-splittable finding in S215 and the stale Emperor's Children priority assumption earlier.
- Turn typing: World Eaters scoping is scoping-only. If the scoping pass surfaces a data or engine
  need, note it for a future typed session — don't fold it into this one.
- No decisions currently waiting on Ryan from S216.

## Close

Produce the four documents, register `SESSION_HANDOFF_217.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
