# Next-session prompt — Session 169

**Assigned: development-manager's call.** B81 shipped (S168/D257). 14 open items; no single
ticket pre-assigned — pick per normal sequencing at session open.

## Open at session start

Read `SESSION_HANDOFF_168.md` first, then D257 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch`. It closed at 24/24 gates
(offline, 3 tier-B skipped) at the end of S168, 121 guarded files, `SESSION_HANDOFF_168.md` newly
guarded. `repo_check` will show differs for the 5 files S168 changed until they are pushed
(`40K_Decision_Log_v3_0.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`,
`pipeline_manifest.json`) — expected, not a new failure. If it names anything beyond those five at
S169 open, that is new and needs reconciling before work starts.

**Manifest ordering rule (D251, standing) — now machine-checked (B81/D257):** at close, finish the
session handoff's text completely, append its own filename to `pipeline_manifest.py`'s `GUARDED`
at creation time, run `pipeline_manifest.py --write`, then run `pipeline_manifest.py
--freshness-check` as the literal last command before delivering. A FAIL there means the decision
log or the handoff was touched after `--write` — reissue and check again. This replaces "remember
to do this last" with a step that fails loudly instead of surviving to the next session's baseline.

## Candidates, not pre-sequenced

- **B69, B70, B72, B73, B80** — remaining Ryan-reported UI/data bugs (Guilliman popup mislabel, Wardens
  of Ultramar attach, Outrider ATV gating, Ultramarine Leader eligibility list, bodyguard popup arrow).
  Still untriaged against source. Several look small (S-sized) — a reasonable place to start. B73 is
  explicitly M-sized and may span multiple Leaders; size it before committing to it as a filler.
- **B76** — rolling documents drop version numbers from filenames. Small, low-risk filler.
- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, never hand-edit output).
  Re-check the ticket's framing against source before starting.
- **B75** — Rules Updates column resolution. Still awaiting Ryan's flag counts across the pack set —
  do not start without them.
- **P4** — Project-area capacity → long-term architecture, M2 next. Ryan reported the area at 79%
  full going into S167, unconfirmed since. Watch, not blocking; consider whether M2 is due before
  it becomes session-blocking.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`.
- GW-derived material never enters the public repo.
- Session close ends with `pipeline_manifest.py --write` then `pipeline_manifest.py
  --freshness-check`, in that order, as the literal last two commands (B81/D257, S168).
- Diagnoses from prior sessions are re-derived from source before building on them. This has caught
  real regressions seven times now (S159, S160, S161, S162's manifest-ordering drift, S163's E14-2
  stale count, S165's index.html version number, S167's manifest-hash staleness on the decision log
  and prior handoff).
- Project file area capacity: 79% full as of S166 (Ryan-reported, unconfirmed since). P4's long-term
  architecture ticket is the standing lever if this becomes blocking.
