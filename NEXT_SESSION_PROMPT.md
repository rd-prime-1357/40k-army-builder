# Next-session prompt — Session 165

**Assigned: E25 — Force Disposition selection (engine-only).** The Thousand Sons build is closed
(turns A/S161/D250, B/S163/D252, C/S160/D248, tooling/S164/D253). This is the next engine-only
session per the S162/S163/S164 sequencing.

## Open at session start

Read `SESSION_HANDOFF_164.md` first, then D253 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch`. This is an engine-only session
(no data-turn source fetch needed). It closed clean at the end of S164 (20/20 gates, 3 tier-B
skipped, 116 guarded files). If the project mount is missing any guarded file at open (rolling
docs, old handoffs, `repo_check.py`), verify via repo clone before flagging — routine, not a data
loss signal.

**Manifest ordering rule (D251, still standing):** at close, finish the session handoff's text
completely, append its own filename to `pipeline_manifest.py`'s `GUARDED` at creation time (not
after), then issue `pipeline_manifest.json` last, touching nothing after.

## E25 scope

Full spec is in `OPEN_ITEMS_BACKLOG.md` under E25 (data side already done — `e1a_dp_and_disposition`
pins 169/169 detachment records carrying exactly one `force_disposition`). Seven numbered points
cover: available-set derivation (list-tolerant, `[].concat(...)`), auto-select on a singleton set,
additive `force_disposition` field inside the list_store v1 envelope, invalidation on detachment
change, missing-selection as a flag-and-warn (not hard-block) same as a missing warlord, a UI
control near the warlord picker (exact placement is a build-session call — decide and proceed, this
is a "how it gets built" question), and a new `e25_check.js` harness pinning derivation, auto-select,
invalidation, and the army-list output line.

`index.html` changes are in scope here (the no-further-extraction rule still applies — this is
additive work inside the existing single-file architecture, not an extraction).
`faction_pack_transform.py` needs no change.

This is engine-only: no `units.json`, `detachments.json`, or other data-file changes. If anything
looks like it needs a data fix while doing this, stop and flag it rather than mixing turn types.

## Then, in later sessions

- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, never hand-edit output).
  Re-check the ticket's framing against source before starting; it may be stale from before the TS
  build closed.
- **B75** — Rules Updates column resolution. Awaiting Ryan's flag counts across the pack set.
- **B76** — rolling documents drop version numbers. Small, low-risk; a reasonable filler if E25
  closes early in a session with time left.
- **B69–B73, B80** — Ryan-reported UI/data bugs (Guilliman popup mislabel, Wardens of Ultramar
  attach, config panel collapse behaviour, Outrider ATV gating, Ultramarine Leader eligibility list,
  bodyguard popup arrow). None yet triaged against source this session cycle; worth a look once E25
  is done if capacity allows, since several look small (S-sized).

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`.
- GW-derived material never enters the public repo.
- Diagnoses from prior sessions are re-derived from source before building on them. This has caught
  real regressions five times now (S159, S160, S161, S162's manifest-ordering drift, S163's E14-2
  stale count).
- Project file area is running high on capacity (79% full as of S164) — P4's long-term architecture
  ticket is the standing lever if this becomes blocking; watch it, don't let it surprise a session.
