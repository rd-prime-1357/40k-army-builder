# Next-session prompt — Session 156

CSM tooling turn C closed (S155, D238): three new CSM census assertions landed, E4b-3's
collision census corrected to 30/6 (CSM's Warp-Fuelled Thrusters, confirmed CSM-internal),
manifest reissued. 106/107 assertions pass; the sole remaining failure is E21a-5/B74, deferred
by design. This closes out the CSM tooling arc from `CSM_BUILD_SCOPE.md` §8.

## Read this first

`SESSION_HANDOFF_155.md` and `D238_entry.md` before starting. `40K_Decision_Log_v3_0.md` has now
been absent from the mounted project area for three consecutive sessions (S153 present, S154
absent, S155 absent). If a fresh upload has resolved this, fold `D231_entry.md`–`D234_entry.md`,
`D237_entry.md`, and `D238_entry.md` into it in order and delete the five standalone files — same
treatment D231–D234 got at S153. If it's still absent, keep banking standalone and flag again;
by S157 this is worth asking Ryan directly rather than re-flagging silently a fourth time.

## Baseline at open

Full `baseline.sh --fetch --data-turn` run needed. Expect `repo_check` to name this batch's
push-pending files (`rules_assertions.py`, `pipeline_manifest.json`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `D238_entry.md`, `SESSION_HANDOFF_155.md`, `NEXT_SESSION_PROMPT.md`)
alongside the long-standing `40K_Data_Pipeline_Process_v0_6.md` drift — none blocking.
`rules_assertions.py` is expected to fail only E21a-5 (B74) — this session's job. If anything
else fails, that's real drift, not expected shape; reconcile before starting.

## This session — B74 (data-only turn)

Chaos Cult's construction effect needs a row in `detachment_effects.json`, matching the shape
already used for the five existing `battleline`-kind rows (see Blood Angels' The Lost Brethren
or Dark Angels' Company Of Hunters entries for the pattern). Confirmed this session:

- Detachment key: `Chaos Space Marines|CHAOS CULT`. Its `rule_text` KEYWORDS clause reads
  "TRAITOR GUARDSMEN SQUAD units from your army gain the BATTLELINE keyword."
- Traitor Guardsmen Squad exists in `units.json` under Chaos Space Marines, `unit_type: Infantry`
  — reachable, not a cross-army resolve like the Dark Angels/Outrider Squad case.
- No `restrictions` text on this detachment; the effect is unconditional while the detachment
  is selected.

Add the row (`kind: battleline`, `target.units: ['Traitor Guardsmen Squad']`, `enforced: true`,
with a `source` note following the existing rows' convention), then confirm E21a-5 passes and
nothing else in `detachment_effects.json`'s five existing rows moved. This should not need an
`index.html` change — the elevation mechanism (`effectiveUnitType()`) already exists and reads
this file; CSM simply hadn't had a row.

Full harness pass after, plus manifest reissue if `detachment_effects.json`'s hash needs to be
picked up anywhere it's guarded.

## After B74

- **Cult-troop cross-file points** (Khorne Berzerkers, Plague Marines, Rubric Marines, Noise
  Marines — `CSM_BUILD_SCOPE.md` §4) — remains open, unscheduled, its own data turn. This is the
  last piece of the CSM roster gap (54/58 → 58/58).
- **M2** (Ryan, evict the 71 GW sources) — unblocked since D237; no Claude action, but don't
  assume it's done without confirming.
