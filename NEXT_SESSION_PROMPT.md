# Next-session prompt — Session 152

S151 confirmed M1 already ran and fixed a real fetch-verify design gap along the way (D234). The area
now holds only the per-session working set; `--fetch` correctly recovers the repo-resident set at open.

## Read this first

`SESSION_HANDOFF_151.md`, `D234_entry.md`, and the P4 body in `OPEN_ITEMS_BACKLOG.md` before starting.
Don't trust remembered numbers — check this file's header against `SESSION_HANDOFF_151.md`.

## Baseline at open

Run `baseline.sh --fetch`. Expect 22/25 gates green: `repro_check` and `rules_assertions` fail naming
the same seven B68 unit_ids as every session since S147 (`000001046`-`000001050`, `000002461`,
`000004209`) - carried-forward, diagnosed, not a regression, and this session's actual assignment.
`repo_check` fails naming `baseline.sh`, `pipeline_manifest.py`, `pipeline_manifest.json`,
`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `40K_Data_Pipeline_Process_v0_6.md` (differ) and
`SESSION_HANDOFF_151.md` (missing from repo) - all S151's own edits and the one pre-existing drift,
pending the next upload batch. None of this blocks starting; if the count or file names differ from
this list, reconcile before proceeding.

## This session - B68 (engine-only)

Per `OPEN_ITEMS_BACKLOG.md`'s B68 entry (D230): `loadout_parser.py`/`equipped_parser.py` resolve by
unit name rather than army+unit_id, so Death Guard and Chaos Space Marines' seven shared generic Chaos
vehicle datasheets (Chaos Rhino, Chaos Land Raider, Chaos Predator Annihilator/Destructor, Chaos Spawn,
Defiler, Helbrute) bleed loadout defaults across factions once both are present in `units.json`.
Isolate the name-keyed match in both parsers, switch to army+unit_id (or unit_id outright), and confirm
via `repro_check.py` that the seven previously-diverging unit_ids reproduce clean and that no other
unit's defaults shift as a side effect.

**Blocks:** `CSM_BUILD_SCOPE.md` section 5 (CSM's own loadout-defaults pass, i.e. CSM turn B).

## Turn type

**Engine-only.** `loadout_parser.py`/`equipped_parser.py` only. No data file content changes beyond
what the fixed parsers regenerate; no tooling changes. `unit_loadouts.json` regeneration is expected as
the parser's own output, not a separate data turn.

## After B68

Per the standing sequence: CSM turn B (data) as the M2 dress rehearsal -> M2 (Ryan, evict the 71 GW
sources) -> CSM turn C. Confirm B68 actually closes the repro_check divergence before treating CSM turn
B as unblocked - don't assume from the diagnosis alone.
