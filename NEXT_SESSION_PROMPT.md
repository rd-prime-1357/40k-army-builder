# Next-session prompt — Session 176

**Assigned: development-manager's call.** B70/B73 are decided (D266, S175) but both need a scoping
turn before code — bigger than S170's audit assumed. B75/B85 still blocked on Ryan providing real
data. P4 needs a call on whether to run the M1/M2 eviction now. 12 open items.

## Open at session start

Read `SESSION_HANDOFF_175.md` first, then D266 in `40K_Decision_Log.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

**Verify you are not opening against a stale project area** — clone the repo and compare its newest
`SESSION_HANDOFF_*.md` against the project area before trusting the mount. S175 found
`40K_Decision_Log.md` missing from the mount entirely (content was fine, verified via clone) — if
that's still happening, ask Ryan for a file-list screenshot rather than re-diagnosing from scratch.

Run the full baseline: `./baseline.sh --fetch` (add `--data-turn` if the session ends up building
against B73's parser, since that needs the real MFM text loaded).

## B70 — needs a scoping turn (analysis-typed, flag model/effort before starting)

Ryan approved building the "unit joins another unit, increases Starting Strength" mechanic (D266).
D260 estimated M/L but didn't scope it. Before writing any engine code: work out how the join
mechanic should interact with roster validation, point cost, and display — this is a new mechanic
category, not a variant of Leader-attach, and precedent set here likely applies to any future unit
with the same ability shape, not just Wardens.

## B73 — needs a scoping/build turn (data turn; the parser rework is more than an override tweak)

Ryan chose MFM as authoritative wherever both exist, Wahapedia only where the MFM has no `LEADER`
block for that character (D266). S175 re-derived the actual mechanism from source and found
`mfm_points_parser.py` has no `LEADER`-handling code path at all today — only `SUPPORT` is
recognized. The build needs:

1. A new collection path for `LEADER`-headed blocks in `mfm_points_parser.py`, written to its own
   field — do not merge with the existing `support_lines` collection; `LEADER` and `SUPPORT` mean
   different things (Leader-attach eligibility vs. the join/Starting-Strength mechanic B70 covers).
2. An override rule: for named Epic Heroes with their own datasheet id, the MFM's `LEADER` list (once
   captured) replaces Wahapedia's `Datasheets_leader.csv`-derived list wherever the MFM has one for
   that character. For the generic shared datasheets (Captain, Chaplain, Librarian, Ancient,
   Apothecary, Lieutenant) — leave existing behavior alone; D260 found the broad list intentional
   there, and S175 didn't test whether an MFM `LEADER` block exists for those or what it would say.
   Confirm this before assuming the same override applies.
3. Reprocess, diff-guard against the currently-committed `units.json`, and check the 13 previously-
   audited Epic Heroes' `leader_eligible_units` now matches each one's actual MFM `LEADER` list.
4. Add an assertion covering the LEADER-vs-SUPPORT distinction so this doesn't regress silently.
5. While in the parser: stop letting a `SUPPORT`-headed block fill `leader_eligible_units` at all
   (that's the Wardens mislabeling S175 found) — this is the data half B70's join mechanic will need,
   so sequence this parser change before B70 needs the data.

Sequence B73's parser rework before B70's engine build, since B70 will want the `SUPPORT`-derived
field this same parser change produces.

## Waiting on Ryan for data, not a product call

**B75 + B85 — faction pack column resolution and keyword-detector noise.** Unchanged: need a local
run of `faction_pack_transform.py` (current version, B85-CONTEXT diagnostic) against 2–3 packs, at
minimum Thousand Sons — console output or the actual pages for p1/p5.

## Candidates that don't need Ryan first

- **E23** — Tank Ace Character grant. M-sized, needs a scoping turn (analysis-typed).
- **B86** — Chaos Daemons pack p13 image-only. Blocked on the same PDF-access gap as B75/B85.
- **P4** — Project-area capacity. Ryan reported 80% again at S175 (unchanged trend since S172's
  73%). S175 confirmed the M2 setup (token, `source_manifest.json`) is already in place, but M1/M2
  eviction itself hasn't run — the area still holds the repo-resident set plus at least one GW
  source file. Worth deciding whether to run the eviction now.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session. B70 (engine) and B73
  (data) each need their own session even once scoped.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`; harness-testable engine logic goes in a `*_check.js` gate.
- GW-derived material never enters the public repo. That includes faction pack PDFs and their
  converted `.md` files.
- No further extraction of code out of `index.html` without a positive reason.
- Session close ends with `pipeline_manifest.py --write` then `pipeline_manifest.py
  --freshness-check`, in that order, as the literal last two commands. Add the new handoff to
  `GUARDED` in the same turn it's written.
- Diagnoses from prior sessions are re-derived from source before building on them — S175 is itself
  an example of why: D260's mechanism description didn't match the actual parser code.
- **Ryan cannot download from the project Files panel.** Any file needed in the repo that lives only
  there must be re-delivered by Claude.
- The decision log's entry format is bullet items (`- **D256** —` and later), not `## D` headings.
- Parallel conversations have **no merge protocol.**
- This environment has no access to raw faction-pack PDFs and likely never will. Any future
  faction-pack tooling work needs Ryan to run the script locally and share real output.
