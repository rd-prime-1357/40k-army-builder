# Next-session prompt — Session 174

**Assigned: development-manager's call.** Three items are blocked — two on Ryan's product judgment
(B70/B73, unchanged since S170), one on Ryan providing real data (B75/B85, new as of S173). 13 open
items.

## Open at session start

Read `SESSION_HANDOFF_173.md` first, then D263 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

**Verify you are not opening against a stale project area** — clone the repo and compare its newest
`SESSION_HANDOFF_*.md` against the project area before trusting the mount. This has bitten the project
twice now (S159's resumed conversation at S172); it's cheap to check and expensive to skip.

Run the full baseline: `./baseline.sh --fetch`. S173 reconciled the manifest gap S172 left (guarded
set now includes `SESSION_HANDOFF_172.md` and `SESSION_HANDOFF_173.md`) and closed 27/28 gates —
`repo_check` will still show `NEXT_SESSION_PROMPT.md`, `SESSION_HANDOFF_172.md`,
`SESSION_HANDOFF_173.md`, `pipeline_manifest.py`, `pipeline_manifest.json` as differing from the repo
until S173's output is pushed. That's expected push-lag, not a new failure — confirm the byte content
matches what S173 delivered rather than re-diagnosing it.

## Decisions waiting on Ryan (do not build past these without an answer)

**B70 — Wardens of Ultramar.** Confirmed: no Leader ability in any source. Its real ability,
`HEROES OF ULTRAMAR`, is a "joins another unit, increases Starting Strength" mechanic the engine has
never implemented. The engine correctly refuses to attach it as a Leader; B70 as filed describes
intended behaviour. **Ask Ryan:** close as not-a-bug, or build the join mechanic as new scope (likely
M/L)?

**B73 — Leader lists include out-of-chapter units.** Confirmed systemic across all 13 currently-built
LEADER-typed Epic Heroes. Root cause: `leader_eligible_units` comes primarily from Wahapedia's
`Datasheets_leader.csv` (10th-edition-sourced); the MFM backfill only fills a blank cell, never checks a
populated one against the MFM's own current `LEADER` list. **Ask Ryan:** should the MFM's list be
authoritative wherever both exist (recommended — consistent with the project's MFM-first precedent for
points and DP), falling back to Wahapedia only where the MFM has no `LEADER` block? Roster-wide, and it
reverses a design choice `wahapedia_transform.py`'s comments defend on purpose.

## Waiting on Ryan for data, not a product call

**B75 + B85 — faction pack column resolution and keyword-detector noise.** S173 confirmed this
environment cannot reach the raw faction-pack PDFs (the private source repo holds only two already-
converted `.md` outputs). A synthetic test of B85's reported bleed pattern did not reproduce it, so
guessing the fix risks a third wrong diagnosis (D262 already corrected two). `faction_pack_transform.py`
now prints a `B85-CONTEXT` line with 30 characters of context before every faction-keyword match. **Ask
Ryan:** run the converter locally against 2-3 representative packs (at least Thousand Sons) and share
either that console output or the actual pages for p1/p5. Once real data is in hand, design B75's
column-clustering rewrite and B85's regex fix together in one tooling turn, verified against that data
before banking.

## Candidates that don't need Ryan first

- **B76** — rolling documents drop version numbers from filenames. Small, low-risk filler; touches many
  cross-references and is a repo delete-plus-add. Clarity only, no safety gain.
- **E23** — HEADHUNTER TASK FORCE Tank Ace Character grant. M-sized, needs a scoping turn first.
- **B86** — Chaos Daemons pack p13 is image-only; confirm by eye whether it carries rules. XS, may be
  nothing. Also blocked on the PDF-access gap above — Ryan would need to look at the actual page.
- **P4** — Project-area capacity → long-term architecture, M2 next. Last confirmed 73% at S172 (79% at
  S171 before that). Still watch, not blocking.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`; harness-testable engine logic goes in a `*_check.js` gate.
- GW-derived material never enters the public repo. That includes faction pack PDFs and their converted
  `.md` files.
- No further extraction of code out of `index.html` without a positive reason.
- Session close ends with `pipeline_manifest.py --write` then `pipeline_manifest.py --freshness-check`,
  in that order, as the literal last two commands (B81/D257). Add the new handoff to `GUARDED` in the
  same turn it's written — S172 skipped this and left a gap S173 had to find and fix.
- Diagnoses from prior sessions are re-derived from source before building on them. B75's own history is
  the cautionary example: two prior sessions got its scope and failure mode wrong from insufficient
  verification.
- **Ryan cannot download from the project Files panel.** Any file needed in the repo that lives only
  there must be re-delivered by Claude.
- The decision log's entry format changed after D255 — entries D256+ are bullet items (`- **D256** —`),
  not `## D` headings. Grepping only for headings makes the log look truncated at D255 when it is
  complete.
- Parallel conversations have **no merge protocol**. Numbered decisions, the handoff chain, the single
  overwritten `NEXT_SESSION_PROMPT.md` and the manifest all assume one writer. If two sessions run at
  once they will collide, and whichever uploads second silently discards the first.
- This environment has no access to raw faction-pack PDFs and likely never will (they're GW-copyrighted
  binaries that don't belong in either repo). Any future faction-pack tooling work needs Ryan to run
  the script locally and share real output — plan session scope around that constraint rather than
  rediscovering it.
