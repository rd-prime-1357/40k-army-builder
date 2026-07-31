# Next-session prompt — Session 170

**Assigned: development-manager's call.** B72 and B80 shipped (S169/D258). 12 open items; no single
ticket pre-assigned — pick per normal sequencing at session open.

## Open at session start

Read `SESSION_HANDOFF_169.md` first, then D258 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority. `index.html` is
at **v6.12**.

Run the full baseline before any new work: `./baseline.sh --fetch`. It closed at 25/25 gates (offline,
3 tier-B skipped) at the end of S169 — note the new `b72_check` gate brings the count up by one. 123
guarded files, `SESSION_HANDOFF_169.md` and `b72_check.js` newly guarded. `repo_check` will show
differs for the files S169 changed until they are pushed (`index.html`, `baseline.sh`,
`rules_assertions.py`, `pipeline_manifest.py`, `pipeline_manifest.json`, `40K_Decision_Log_v3_0.md`,
`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, plus the two net-new/rolling files) — expected, not a new
failure. If it names anything beyond the S169 set at S170 open, that is new and needs reconciling
before work starts.

## A decision waiting on Ryan — B69 (corrected + generalized, D259)

Ryan's instruction, now recorded: **remove** the "(see left)" cue from Guilliman's *Author of the Codex*
and render the abilities it grants **directly beneath** the selector, grouped — not rewrite the cue to
"(see below)". Investigating this generalized it (D259): the same "select N [X] abilities" shape, whose
"(see left)"/"(see above)" cue points to a boxed pool printed elsewhere on the card, appears on **six
units across four factions** — Guilliman (*Author of the Codex*), Grimaldus (*Temple Relics*), Mortarion
(*Lord of the Death Guard*), Abaddon (*The Warmaster*), Magnus (*Unearthly Power*), Ulrik (*Oathbound*,
"(see above)"). All render the pool as unlinked sibling ability rows.

The selector→pool link is **not in our data** (`abilities.json` is name+description only; the source's
left/right-column typing that encodes it was collapsed at B4/D155), so it can't be derived engine-side —
and a blanket cue-strip is unsafe because the 28 "(see below)" cues (Nurgle's Gift across the Death Guard
roster, Blessings of Khorne) reference content inside the same description and are correct.

**Correct build shape:** a **data turn** — parser re-captures each selector's ability pool from the source
column-typing (never hand-edit `units.json`), backed by an assertion carrying the six selector→pool maps —
then an **engine turn** rendering each pool nested under its selector, dropping the resolved "(see left)/
(see above)" cue and leaving "(see below)" alone. Two turns, two types; do not mix.

**Open scope choice for Ryan:** fix all six select-N-from-pool units in one arc (**recommended** — the
marginal cost over Guilliman-alone is small once the parser captures the pool, and it clears the identical
bug on five other Epic Heroes), or Guilliman-only as a stopgap (a fragile engine hardcode of his pool,
asserted, buys immediate visibility at the cost of correctness-at-source). B69 is not started until Ryan
picks the scope.

## Candidates, not pre-sequenced

- **B70 + B73** — one linked data/audit arc, and the strongest next pick. B73 (M-sized) is a
  source-level audit of Leader `leader_eligible_units` lists against actual Matched Play legality;
  "Wardens of Ultramar" already shows the two symptoms (null `leader_ability_name`, and an
  out-of-faction `VANGUARD VETERAN SQUAD WHITE SCARS` in its eligibility list), so B70 falls out of the
  same audit. Start with the audit, not a build. Likely a parser fix — never hand-edit `units.json`.
  This is a **data/parser turn**, kept apart from any engine work.
- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, regenerate output; retain
  `allied_group` — it feeds E22b's gate). Re-check the ticket's framing against source before starting.
  Small.
- **B76** — rolling documents drop version numbers from filenames. Small, low-risk filler; touches many
  cross-references and is a repo delete-plus-add. Clarity only, no safety gain (manifest hash already
  handles content identity).
- **B75** — Rules Updates column resolution. Still blocked on Ryan's flag counts across the pack set —
  do not start without them.
- **E23** — HEADHUNTER TASK FORCE Tank Ace Character grant. M-sized, needs a scoping turn first
  (a fifth `detachment_effects` kind vs. its own mechanism). Over-restriction, not a D0 violation.
- **P4** — Project-area capacity → long-term architecture, M2 next. Watch, not blocking; Ryan reported
  79% at S166/167, unconfirmed since. Consider whether M2 is due before it becomes session-blocking.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session. (S169 was engine-only;
  B70/B73/B77 are data/parser turns — do not fold them into an engine turn.)
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`; harness-testable engine logic goes in a `*_check.js` gate.
- GW-derived material never enters the public repo.
- No further extraction of code out of `index.html` without a positive reason.
- Session close ends with `pipeline_manifest.py --write` then `pipeline_manifest.py
  --freshness-check`, in that order, as the literal last two commands (B81/D257).
- Diagnoses from prior sessions are re-derived from source before building on them. This has caught
  real regressions eight times now (S159–S167, and S169's confirmation that B72's data was already
  correct so the fix belonged in the engine, not the data).
