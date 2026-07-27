# Next-session prompt — Session 153

B68 closed (S152, D235): `equipped_parser.py` now resolves web-composition titles within the
composition file's own faction, so Death Guard and Chaos Space Marines no longer bleed loadout defaults
across their seven shared generic Chaos vehicle names. `repro_check` is byte-identical again.

## Read this first

`SESSION_HANDOFF_152.md`, the D235 entry at the tail of `40K_Decision_Log_v3_0.md`, and
`CSM_BUILD_SCOPE.md` (especially §5 Loadout defaults and §6 the exact build surface) before starting.
Don't trust remembered numbers — check this file's header against `SESSION_HANDOFF_152.md`.

## Baseline at open

Run `baseline.sh --fetch --data-turn` (this is a data turn — sources must be verified loaded, not
tier-A-only). Expect all pipeline/gate/repro gates green. `repo_check` will fail naming this batch's
push-pending files (`equipped_parser.py`, `pipeline_manifest.py`, `pipeline_manifest.json`,
`40K_Decision_Log_v3_0.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_152.md`) plus
the long-standing `40K_Data_Pipeline_Process_v0_6.md` drift — all pending the next upload batch, none
blocking. If the count or names differ from that list, reconcile before proceeding.

## This session — CSM turn B (data-only)

CSM's loadout-defaults pass, `CSM_BUILD_SCOPE.md` §5. Now unblocked by B68. Per §6, the config edits are
small and additive:

- `repro_check.py` — add `CSM` to `FACTIONS`; add `Chaos_Space_Marines` to `WEB_PASSES`.
- `units_repro_check.py` — add the CSM per-faction block and a fourth `--in` to the merge call.
- `detachment_parser.py` — add CSM rows to `ARMY_TO_MFM`, `MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`.
- `detachments_repro_check.py` — add `MFM_Chaos_Space_Marines_v1_0.txt` to its required-inputs list.

Then run the CSM web pass (`Chaos_Space_Marines_web.txt`) as the sixth `equipped_parser.py` pass and
`loadout_parser.py --factions ... CSM`, regenerate `unit_loadouts.json`, and diff-trace against the
currently-committed file: every change should be CSM's own new entries plus (correctly) the DG/CSM
shared vehicles now each carrying their own faction-scoped defaults. Nothing else should move.

**B68 dependency — do not rename the web file.** `equipped_parser.py` infers the pass's faction scope
from the composition filename. `Chaos_Space_Marines_web.txt` must keep exactly that name so it maps to
the "Chaos Space Marines" army block; renaming it silently drops the scope back to flat resolution and
reopens the bleed.

**Turn type: data-only.** Config-list additions plus the parser output they regenerate. No engine logic
change to `loadout_parser.py`/`equipped_parser.py` beyond what the config lists drive; no tooling change.
This is the M2 dress rehearsal per the P4 sequence.

## Housekeeping (fold in when convenient, not blocking)

The standalone `D2NN_entry.md` pattern was a workaround for the decision log being evicted under M1;
the log is workspace-resident again. Fold `D232`–`D234` into `40K_Decision_Log_v3_0.md` and retire the
standalone-entry pattern. Small, do it opportunistically.

## After CSM turn B

Per the standing sequence: M2 (Ryan, evict the 71 GW sources) → CSM turn C. Confirm CSM turn B's
diff-trace is clean before treating M2 as unblocked.
