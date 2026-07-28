# Next-session prompt — Session 154

CSM turn B closed (S153, D236): `unit_loadouts.json` +54 CSM entries, `wargear_points.json` +2 entries
(a second gap the loadout data surfaced), `rules_assertions.py` E14-2 updated 53/33 → 64/44. All 23
non-repo gates green. `detachment_parser.py` / `detachments_repro_check.py` deliberately untouched —
CSM turn C's job.

## Read this first

`SESSION_HANDOFF_153.md` and the D236 entry at the tail of `40K_Decision_Log_v3_0.md` before starting.
Don't trust remembered numbers — check this file's header against `SESSION_HANDOFF_153.md`.

## Baseline at open

Run `baseline.sh --fetch --data-turn`. Expect all pipeline/gate/repro gates green. `repo_check` will
fail naming this batch's push-pending files (`repro_check.py`, `unit_loadouts.json`,
`wargear_points.json`, `rules_assertions.py`, `pipeline_manifest.py`, `pipeline_manifest.json`,
`40K_Decision_Log_v3_0.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_153.md`)
plus the deletion of `D231_entry.md`–`D234_entry.md` (folded into the main log, S153) plus the
long-standing `40K_Data_Pipeline_Process_v0_6.md` drift — all pending the next upload batch, none
blocking. If the count or names differ from that list, reconcile before proceeding.

## This session — CSM turn C (data-only): detachment build

Per `CSM_BUILD_SCOPE.md` §3 and §6. The config edits:

- `detachment_parser.py` — add CSM rows to `ARMY_TO_MFM` (`"Chaos Space Marines": "MFM_Chaos_Space_Marines_v1_0.txt"`),
  `MFM_SOURCE_NAME` (`"MFM_Chaos_Space_Marines_v1_0.txt": "Chaos Space Marines"`), and
  `ARMY_TO_WAHA_FACTION` (`"Chaos Space Marines": "CSM"`).
- `detachments_repro_check.py` — add `MFM_Chaos_Space_Marines_v1_0.txt` to its required-inputs list.

Then regenerate `detachments.json` and verify: **17 CSM detachments** (D192/§3 — MFM is the source of
record; the two MFM-only detachments, Devotees of Destruction and Murdertalon Raiders, are included
with no rule prose and enhancement names/points only; the three Wahapedia-only detachments are dropped
as stale). Diff-trace against the currently-committed file: every change should be CSM's own 17 new
detachment entries; nothing else should move. `detachments_repro_check.py` must reproduce the result
byte-for-byte.

**Turn type: data-only.** Config-list additions plus the parser output they regenerate. No engine logic
change to `detachment_parser.py` beyond what the config lines drive; no tooling change.

## After CSM turn C

Per the standing sequence: M2 (Ryan, evict the 71 GW sources) is unblocked once CSM turn C's diff-trace
is confirmed clean — CSM turn C was the last piece of CSM build work gating it. Then the tooling turn:
CSM-specific assertions into `rules_assertions.py` (roster count 58/54-plus-4-pending-cult-troop-pricing,
detachment count 17, the two prose-less detachments recorded as such), manifest reissue, full harness
pass. Cult-troop cross-file points (the four units in sibling MFMs — Khorne Berzerkers, Plague Marines,
Rubric Marines, Noise Marines, per `CSM_BUILD_SCOPE.md` §4) remains open, unscheduled — CSM's roster
stays at 54 of 58 until that lands as its own data turn.
