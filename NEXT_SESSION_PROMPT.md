# Next-session prompt — Session 167

**Assigned: development-manager's call.** B71 is closed (S166/D255). 14 open items remain; no single
ticket is pre-assigned — pick per normal sequencing at session open.

## Open at session start

Read `SESSION_HANDOFF_166.md` first, then D255 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch`. It closed at 26/27 at the end of
S166 (3 tier-B skipped, 120 guarded files, `b71_check.js` and `SESSION_HANDOFF_166.md` both newly
guarded). The one non-tier-B failure, `repo_check`, is expected: it names exactly the 10 files S166
touched (2 new, 8 modified), none pushed to the repo yet — clears once pushed, not a data-loss signal.
If it names anything beyond those 10 files at S167 open, that is new and needs reconciling before work
starts. If the project mount is missing any guarded file at open (rolling docs, old handoffs,
`repo_check.py`), verify via repo clone before flagging — routine, not a data loss signal.

**Manifest ordering rule (D251, still standing):** at close, finish the session handoff's text
completely, append its own filename to `pipeline_manifest.py`'s `GUARDED` at creation time (not
after), then issue `pipeline_manifest.json` last, touching nothing after.

## Candidates, not pre-sequenced

- **B69, B70, B72, B73, B80** — remaining Ryan-reported UI/data bugs (Guilliman popup mislabel, Wardens
  of Ultramar attach, Outrider ATV gating, Ultramarine Leader eligibility list, bodyguard popup arrow).
  None yet triaged against source this session cycle. Several look small (S-sized) — a reasonable place
  to start if no other constraint applies. B73 is explicitly M-sized and may span multiple Leaders, so
  size it before committing to it as a filler.
- **B76** — rolling documents drop version numbers from filenames. Small, low-risk; a reasonable filler
  if a chosen item closes early with time left.
- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, never hand-edit output).
  Re-check the ticket's framing against source before starting; it may be stale from before the TS
  build closed.
- **B75** — Rules Updates column resolution. Still awaiting Ryan's flag counts across the pack set — do
  not start without them.
- **P4** — Project-area capacity → long-term architecture, M2 next. Ryan reported the area at 79% full
  going into S166 (down from 90%+ readings earlier in the project, likely from his routine handoff
  deletions) — watch, not blocking. Consider whether M2 is due before capacity becomes
  session-blocking rather than just a watch item.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`.
- GW-derived material never enters the public repo.
- Diagnoses from prior sessions are re-derived from source before building on them. This has caught
  real regressions six times now (S159, S160, S161, S162's manifest-ordering drift, S163's E14-2
  stale count, S165's index.html version number). S166 added a smaller instance of the same
  discipline: a build-time harness (`bundle_check.js`) silently depended on an internal variable name
  that the B71 fix removed, caught only by actually running the full baseline rather than trusting the
  new harness's own green result in isolation.
- Project file area capacity: 79% full as of S166 (Ryan-reported). P4's long-term architecture ticket
  is the standing lever if this becomes blocking; watch it, don't let it surprise a session.
