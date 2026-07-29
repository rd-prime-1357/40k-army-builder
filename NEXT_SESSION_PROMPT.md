# Next-session prompt — Session 155

CSM turn C closed (S154, D237): `detachments.json` +17 CSM detachments (160 total), diff-traced clean
against the committed file, `detachments_repro_check.py` green. This closes the CSM detachment build
arc and unblocks M2. Two gaps surfaced and filed, neither fixed this session: E4b-3's same-army
enhancement-collision literal is stale (29→30), and new ticket B74 — CSM's Chaos Cult detachment grants
BATTLELINE with no `detachment_effects.json` row.

## Read this first

`SESSION_HANDOFF_154.md` and `D237_entry.md` before starting. `40K_Decision_Log_v3_0.md` was unreachable
in the mounted project area at S154 open (contradicting S153's own account of it) — check whether a
fresh upload has resolved this. If the log is present and intact, fold `D237_entry.md` into it (same
treatment D231–D234 got at S153) and delete the standalone file. If it's still absent, keep banking
standalone and flag again.

## Baseline at open

Full `baseline.sh --fetch --data-turn` run needed — S154 only verified `detachments_repro_check.py`
against the detachment-build input set, not the full gate suite. Expect `repo_check` to name this
batch's push-pending files (`detachment_parser.py`, `detachments_repro_check.py`, `detachments.json`,
`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_154.md`, `NEXT_SESSION_PROMPT.md`, plus
`D237_entry.md` if still standalone) alongside the long-standing `40K_Data_Pipeline_Process_v0_6.md`
drift — none blocking. `rules_assertions.py` is expected to fail E4b-3 and E21a-5 until this session's
work lands them — both are known, both are this session's job, not baseline drift.

## This session — CSM tooling turn (tooling-only)

Per `CSM_BUILD_SCOPE.md` §8 step 4. Roster stands at 54 of 58 (four cult-troop units — Khorne
Berzerkers, Plague Marines, Rubric Marines, Noise Marines — remain unpriced pending their own
cross-file data turn per §4; not this session's job).

- **New CSM assertions in `rules_assertions.py`:** roster count (58 target / 54 actual, recorded as
  such — do not round up), detachment count 17, the two prose-less detachments named and recorded as
  `text_source: none` by design, not a gap.
- **E4b-3 literal update:** 29→30 same-army enhancement collisions, 5→6 distinct colliding names —
  re-derive from a fresh scan, don't just bump the number; confirm which name is the new sixth collision
  and that it's CSM-internal before writing the literal.
- **Manifest reissue** (`pipeline_manifest.py --write`) once the above lands.
- **Full harness pass** — confirm nothing else moved.

## After the tooling turn

- **B74** (Chaos Cult BATTLELINE grant, no `detachment_effects.json` row) — its own small data turn,
  once this session's CSM assertions are in and the effects-file shape is fresh in view. Don't fold it
  into the tooling turn itself; it's a data edit, not an assertion.
- **Cult-troop cross-file points** (the four units, `CSM_BUILD_SCOPE.md` §4) — remains open, unscheduled,
  its own data turn.
- **M2** (Ryan, evict the 71 GW sources) — unblocked as of D237; no Claude action, but don't assume it's
  done without confirming.
