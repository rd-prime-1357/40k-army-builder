# Next-session prompt — Session 166

**Assigned: development-manager's call.** E25 is closed (S165/D254). 15 open items remain; no
single ticket is pre-assigned — pick per normal sequencing at session open.

## Open at session start

Read `SESSION_HANDOFF_165.md` first, then D254 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch`. It closed clean at the end of
S165 (22/22 gates, 3 tier-B skipped, 118 guarded files — up from 116, `e25_check.js` and
`SESSION_HANDOFF_165.md` both newly guarded). If the project mount is missing any guarded file at
open (rolling docs, old handoffs, `repo_check.py`), verify via repo clone before flagging —
routine, not a data loss signal.

**Manifest ordering rule (D251, still standing):** at close, finish the session handoff's text
completely, append its own filename to `pipeline_manifest.py`'s `GUARDED` at creation time (not
after), then issue `pipeline_manifest.json` last, touching nothing after.

## Candidates, not pre-sequenced

- **B69–B73, B80** — Ryan-reported UI/data bugs (Guilliman popup mislabel, Wardens of Ultramar
  attach, config panel collapse behaviour, Outrider ATV gating, Ultramarine Leader eligibility list,
  bodyguard popup arrow). None yet triaged against source this session cycle. Several look small
  (S-sized) — a reasonable place to start if no other constraint applies.
- **B76** — rolling documents drop version numbers from filenames. Small, low-risk; a reasonable
  filler if a chosen item closes early with time left.
- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, never hand-edit output).
  Re-check the ticket's framing against source before starting; it may be stale from before the TS
  build closed.
- **B75** — Rules Updates column resolution. Still awaiting Ryan's flag counts across the pack set —
  do not start without them.
- **P4** — Project-area capacity → long-term architecture, M2 next. The project file area was
  reported at 79% full going into S165; watch this, and consider whether M2 is due before capacity
  becomes session-blocking rather than just a watch item.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`.
- GW-derived material never enters the public repo.
- Diagnoses from prior sessions are re-derived from source before building on them. This has caught
  real regressions six times now (S159, S160, S161, S162's manifest-ordering drift, S163's E14-2
  stale count, S165's index.html version number — memory said 6.3, the file said 6.9).
- Project file area capacity: 79% full as of S164/S165. P4's long-term architecture ticket is the
  standing lever if this becomes blocking; watch it, don't let it surprise a session.
