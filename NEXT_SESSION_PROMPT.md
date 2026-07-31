# Next-session prompt — Session 175

**Assigned: development-manager's call.** Same three items blocked as S174: two on Ryan's product
judgment (B70/B73, unchanged since S170), one on Ryan providing real data (B75/B85, unchanged since
S173). 12 open items.

## Open at session start

Read `SESSION_HANDOFF_174.md` first, then D264/D265 in `40K_Decision_Log.md` (renamed this session
— see below). Do not trust any session/version/decision number from memory; the handoff chain is
the only authority.

**Verify you are not opening against a stale project area** — clone the repo and compare its newest
`SESSION_HANDOFF_*.md` against the project area before trusting the mount.

**Filenames changed this session (B76, D265).** Five docs were renamed, content unchanged:
`40K_Decision_Log_v3_0.md` → `40K_Decision_Log.md`, `40K_Data_Pipeline_Process_v0_6.md` →
`40K_Data_Pipeline_Process.md`, `40K_Functional_Spec_v0_7.md` → `40K_Functional_Spec.md`,
`40K_Architecture_Overview_v0_5.md` → `40K_Architecture_Overview.md`,
`40K_Data_Dictionary_v2_0.md` → `40K_Data_Dictionary.md`. If Ryan has not yet pushed the rename by
session open, the repo will still have the old names — check which set is actually present before
assuming either way, and if the old names are still there, that's expected push-lag, not a
regression.

Run the full baseline: `./baseline.sh --fetch`. S174 fixed a real manifest defect, not push-lag:
`pipeline_manifest.json`'s hash for `SESSION_HANDOFF_172.md` did not match the file actually
committed to the repo (D264) — confirmed two independent ways, root cause unconfirmed. If
`fetch-verify` fails again on a *different* file with the same symptom (recorded hash doesn't match
a freshly-fetched copy, verified two ways), treat it the same way D264 did: don't guess, verify
against an independently-fetched copy, and reconcile before starting.

## Decisions waiting on Ryan (do not build past these without an answer)

**B70 — Wardens of Ultramar.** Confirmed: no Leader ability in any source. Its real ability,
`HEROES OF ULTRAMAR`, is a "joins another unit, increases Starting Strength" mechanic the engine has
never implemented. **Ask Ryan:** close as not-a-bug, or build the join mechanic as new scope (likely
M/L)?

**B73 — Leader lists include out-of-chapter units.** Confirmed systemic across all 13 currently-built
LEADER-typed Epic Heroes. Root cause: `leader_eligible_units` comes primarily from Wahapedia's
`Datasheets_leader.csv` (10th-edition-sourced); the MFM backfill only fills a blank cell, never checks
a populated one against the MFM's own current `LEADER` list. **Ask Ryan:** should the MFM's list be
authoritative wherever both exist (recommended), falling back to Wahapedia only where the MFM has no
`LEADER` block?

## Waiting on Ryan for data, not a product call

**B75 + B85 — faction pack column resolution and keyword-detector noise.** Still cannot be fixed
correctly from this environment — no PDF access. **Ask Ryan:** run `faction_pack_transform.py`
locally (current version, with the B85 `B85-CONTEXT` diagnostic) against 2-3 representative packs, at
minimum Thousand Sons, and share either the console output or the actual pages for p1/p5.

## Candidates that don't need Ryan first

- **E23** — HEADHUNTER TASK FORCE Tank Ace Character grant. M-sized, needs a scoping turn first
  (analysis-typed, not mechanical — flag model/effort before starting).
- **B86** — Chaos Daemons pack p13 is image-only; confirm by eye whether it carries rules. XS, may be
  nothing. Blocked on the same PDF-access gap as B75/B85.
- **P4** — Project-area capacity → long-term architecture, M2 next. Last confirmed 73% at S172;
  Ryan reported 80% at S174's open — watch closely, may need to act soon.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`; harness-testable engine logic goes in a `*_check.js` gate.
- GW-derived material never enters the public repo. That includes faction pack PDFs and their
  converted `.md` files.
- No further extraction of code out of `index.html` without a positive reason.
- Session close ends with `pipeline_manifest.py --write` then `pipeline_manifest.py
  --freshness-check`, in that order, as the literal last two commands. Add the new handoff to
  `GUARDED` in the same turn it's written — S172 skipped this once already; S174 did not repeat it.
- Diagnoses from prior sessions are re-derived from source before building on them.
- **Ryan cannot download from the project Files panel.** Any file needed in the repo that lives only
  there must be re-delivered by Claude.
- The decision log's entry format is bullet items (`- **D256** —` and later), not `## D` headings.
- Parallel conversations have **no merge protocol.**
- This environment has no access to raw faction-pack PDFs and likely never will. Any future
  faction-pack tooling work needs Ryan to run the script locally and share real output.
