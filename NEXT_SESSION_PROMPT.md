# Next-session prompt — Session 172

**Assigned: development-manager's call, but two items are blocked on Ryan.** B70 and B73 are still
audited-not-fixed (S170/D260) and need a decision from Ryan before any build. B77 closed S171 (D261,
already-resolved, no build needed). 11 open items.

## Open at session start

Read `SESSION_HANDOFF_171.md` first, then D261 (and D260, still relevant) in `40K_Decision_Log_v3_0.md`.
Do not trust any session/version/decision number from memory; the handoff chain is the only authority.
`index.html` is still at **v6.12** — nothing shipped S170 or S171.

Run the full baseline before any new work: `./baseline.sh --fetch`. It closed at 29/29 gates at the end
of S171. Nothing changed in code or data this session — only `40K_Decision_Log_v3_0.md`,
`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, plus the two rolling files (`SESSION_HANDOFF_171.md` new,
`NEXT_SESSION_PROMPT.md` overwritten). `repo_check` will show differs for exactly those until pushed —
expected, not a new failure.

## Decisions waiting on Ryan (do not build past these without an answer)

**B70 — Wardens of Ultramar.** Confirmed: no Leader ability in any source. Its real ability,
`HEROES OF ULTRAMAR`, is a "joins another unit, increases Starting Strength" mechanic the engine has
never implemented. The engine correctly refuses to attach it as a Leader; B70 as filed describes intended
behavior. **Ask Ryan:** close as not-a-bug, or build the join mechanic as new scope (likely M/L)? Do not
start a build on B70 until answered.

**B73 — Leader lists include out-of-chapter units.** Confirmed systemic across all 13 currently-built
LEADER-typed Epic Heroes. Root cause: `leader_eligible_units` comes primarily from Wahapedia's
`Datasheets_leader.csv` (10th-edition-sourced); the MFM backfill only fills a blank cell, never checks a
populated one against the MFM's own current `LEADER` list. **Ask Ryan:** should the MFM's list be
authoritative wherever both exist (recommended — consistent with the project's MFM-first precedent for
points/DP), falling back to Wahapedia only where the MFM has no `LEADER` block? This is roster-wide and
reverses a design choice `wahapedia_transform.py`'s own comments defend on purpose. Do not start a build
on B73 until answered.

Once B73 is answered, fixing it will likely also resolve Wardens' SUPPORT-vs-LEADER bleed and the
one-line MFM-block over-read as a side effect of the same data turn — unless B70 goes the join-mechanic
route, in which case Wardens' list should go back to null/empty instead.

## B77 — closed, no action needed

Audited and closed S171 (D261) without reaching Ryan: the six Scintillating Legions carriers already
carry the faction keyword in `units.json` (sourced from Wahapedia's own keyword CSV) and it already
renders in the UI as `Faction: Scintillating Legions`. `keywords.json`'s absence of an entry is correct
— faction keywords don't look it up. Nothing to build. Don't reopen without new evidence.

## Candidates that don't need Ryan first

- **B76** — rolling documents drop version numbers from filenames. Small, low-risk filler; touches many
  cross-references and is a repo delete-plus-add. Clarity only, no safety gain. Best pick if B70/B73
  answers aren't in yet.
- **B75** — Rules Updates column resolution. Still blocked on Ryan's flag counts across the pack set — do
  not start without them.
- **E23** — HEADHUNTER TASK FORCE Tank Ace Character grant. M-sized, needs a scoping turn first.
- **P4** — Project-area capacity → long-term architecture, M2 next. Ryan confirmed 79% full at S171 (last
  prior confirmation was S166/167) — still watch, not blocking, but worth another check if it's been
  several more sessions by the time this is read.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session. S171 was audit-only (no
  code changed at all) — same discipline as S170.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`; harness-testable engine logic goes in a `*_check.js` gate.
- GW-derived material never enters the public repo.
- No further extraction of code out of `index.html` without a positive reason.
- Session close ends with `pipeline_manifest.py --write` then `pipeline_manifest.py
  --freshness-check`, in that order, as the literal last two commands (B81/D257).
- Diagnoses from prior sessions are re-derived from source before building on them — S171 is itself an
  example: a filed ticket's diagnosis (B77) turned out to already be stale, and checking first avoided
  redundant work.
