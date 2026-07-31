# Next-session prompt — Session 168

**Assigned: development-manager's call.** B81 filed (S167/D256), no ticket closed. 15 open items;
no single ticket pre-assigned — pick per normal sequencing at session open.

## Open at session start

Read `SESSION_HANDOFF_167.md` first, then D256 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch`. It closed at 22/22 (offline
gates) at the end of S167, 3 tier-B skipped, 121 guarded files, `SESSION_HANDOFF_167.md` newly
guarded. `repo_check` ran clean at S167 close (0 differs, 0 GW material) — if it names anything at
S168 open, that is new and needs reconciling before work starts. If the project mount is missing any
guarded file at open (rolling docs, old handoffs, `repo_check.py`), verify via repo clone before
flagging — routine, not a data-loss signal, per the pattern S167 itself worked through.

**Manifest ordering rule (D251, standing, and the direct subject of S167's finding):** at close,
finish the session handoff's text completely, append its own filename to `pipeline_manifest.py`'s
`GUARDED` at creation time, then issue `pipeline_manifest.json` last, touching nothing after. S167
found this had silently slipped twice before (D239, and the `40K_Decision_Log_v3_0.md` /
`SESSION_HANDOFF_166.md` pair this session) — B81 proposes automating the check; consider it as a
candidate below.

## Candidates, not pre-sequenced

- **B69, B70, B72, B73, B80** — remaining Ryan-reported UI/data bugs (Guilliman popup mislabel, Wardens
  of Ultramar attach, Outrider ATV gating, Ultramarine Leader eligibility list, bodyguard popup arrow).
  Still untriaged against source. Several look small (S-sized) — a reasonable place to start. B73 is
  explicitly M-sized and may span multiple Leaders; size it before committing to it as a filler.
- **B81** — automate the manifest-freshness check (re-hash the decision log and session handoff right
  after `--write`, fail loudly on drift). Small, self-contained, directly prevents a defect that has
  now recurred three times. A reasonable place to start if no other constraint applies.
- **B76** — rolling documents drop version numbers from filenames. Small, low-risk filler.
- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, never hand-edit output).
  Re-check the ticket's framing against source before starting.
- **B75** — Rules Updates column resolution. Still awaiting Ryan's flag counts across the pack set —
  do not start without them.
- **P4** — Project-area capacity → long-term architecture, M2 next. Ryan reported the area at 79%
  full going into S167. Watch, not blocking; consider whether M2 is due before it becomes
  session-blocking.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`.
- GW-derived material never enters the public repo.
- Diagnoses from prior sessions are re-derived from source before building on them. This has caught
  real regressions seven times now (S159, S160, S161, S162's manifest-ordering drift, S163's E14-2
  stale count, S165's index.html version number, S167's manifest-hash staleness on the decision log
  and prior handoff).
- Project file area capacity: 79% full as of S166 (Ryan-reported, unconfirmed since). P4's long-term
  architecture ticket is the standing lever if this becomes blocking.
