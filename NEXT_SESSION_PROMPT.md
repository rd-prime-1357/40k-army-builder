# Next-session prompt — Session 177

**Assigned: development-manager's call.** B73 shipped S176 (D267). The two follow-on tickets it
created — E26 (engine: Leader/Support stacking) and E27 (UI: popup/output wording) — are the natural
next steps, but both are engine/UI turns and must not mix with data or with each other's turn type.
B70 (Wardens join mechanic) is now unblocked and holds a real MFM-vs-datasheet conflict to resolve.
B75/B85 still wait on Ryan providing real faction-pack output. P4 (project-area eviction) still open.
**13 open items.**

## Open at session start

Read `SESSION_HANDOFF_176.md` first, then D267 in `40K_Decision_Log.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

**Verify you are not opening against a stale project area** — clone the repo and compare its newest
`SESSION_HANDOFF_*.md` against the project area before trusting the mount. S175 and S176 both found
`40K_Decision_Log.md` missing from the mount entirely (content fine, verified via clone). If that's
still happening, ask Ryan for a file-list screenshot rather than re-diagnosing.

Run the full baseline: `./baseline.sh --fetch` (add `--data-turn` only if the session builds against
the MFM parser again — E26/E27 do not; they are engine/UI). Expect **111** rules assertions,
including the new `B73`.

## E26 - enforce one-Leader-one-Support stacking, with exceptions (engine turn; analysis-typed, flag model/effort)

Ryan's stipulations 1+2 (D267). Core rules 19.01/24.22/24.34: a bodyguard may hold one Leader **and**
one Support at once, and some datasheet/detachment rules widen that. The data half is done - B73 set
`leader_ability_name` to "Leader"/"Support" correctly. This turn teaches the attach gate to read that
name and enforce the rule. Start from what already exists: `canAttachLeader` (index.html) caps total
attachers at 2 (D157) with a pairwise `permitsCoLeader` permit, but it is ability-blind. Decide how the
Leader/Support distinction folds into that cap and how special-rule exceptions are expressed -
this is a rules-legality design call (a wrong judgment ships an illegal-list-reachable bug, against
D0), so it needs a scoping pass before code. Add/extend a `*_check.js` gate and update the
`canAttachLeader` assertion in `rules_assertions.py`.

## E27 - state Leader vs Support correctly in popups and exported output (engine/UI turn)

Ryan's stipulation 3 (D267). `leaderSectionHtml` (index.html ~6549) hardcodes the heading "Leader"
(line 6568) and generic body text, so a Support unit renders under a "Leader" heading. Make the
heading and body read the unit's actual `leader_ability_name`, and word the stacking rule correctly.
Depends only on data B73 already ships. Smaller than E26; could pair as the UI follow-on once E26's
enforcement lands, but keep them separate turns (engine logic vs. display) if E26 grows.

## B70 - Wardens join mechanic, now unblocked, holds a conflict to resolve (engine; analysis-typed)

Ryan approved building the "join and increase Starting Strength" mechanic (D266). B73 (D267) carved
Wardens out - its `leader_eligible_units` is now empty. Before building, resolve the MFM-vs-datasheet
conflict B73 surfaced: the MFM tags Wardens `SUPPORT` with **six** units; the printed `HEROES OF
ULTRAMAR` ability lists **three** (Assault Intercessor Squad, Bladeguard Veteran Squad, Intercessor
Squad). Ryan's standing rule is MFM-as-source-of-truth, but he asked to be told of pack conflicts -
this is one, and which list governs the join is a product/legality call for him. Batch it into the
scoping turn rather than blocking. New mechanic category, precedent applies beyond Wardens.

## Waiting on Ryan for data, not a product call

**B75 + B85 - faction pack column resolution and keyword-detector noise.** Unchanged: need a local
run of `faction_pack_transform.py` (current version, B85-CONTEXT diagnostic) against 2-3 packs, at
minimum Thousand Sons - console output or the actual pages for p1/p5.

## Candidates that don't need Ryan first

- **E23** - Tank Ace Character grant. M-sized, needs a scoping turn (analysis-typed).
- **B86** - Chaos Daemons pack p13 image-only. Blocked on the same PDF-access gap as B75/B85.
- **P4** - Project-area capacity. Ryan reported 80% at S175. The M2 setup (token,
  `source_manifest.json`) is in place but M1/M2 eviction hasn't run - the area still holds the
  repo-resident set plus GW source files. Worth deciding whether to run the eviction now.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session. E26 (engine), E27
  (engine/UI), B70 (engine) and any data work each need their own session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold - legality-critical claims go in
  `rules_assertions.py`; harness-testable engine logic goes in a `*_check.js` gate.
- GW-derived material never enters the public repo. That includes faction pack PDFs and their
  converted `.md` files.
- No further extraction of code out of `index.html` without a positive reason.
- Session close ends with `pipeline_manifest.py --write` then `pipeline_manifest.py
  --freshness-check`, in that order, as the literal last two commands. Add the new handoff to
  `GUARDED` in the same turn it's written.
- Diagnoses from prior sessions are re-derived from source before building on them - S176 is a fresh
  example: two S175 assumptions (Support = a separate mechanic; separate fields) were wrong and were
  caught only by reading the rules and the engine before regenerating.
- **Ryan cannot download from the project Files panel.** Any file needed in the repo that lives only
  there must be re-delivered by Claude.
- The decision log's entry format is bullet items (`- **D267** -`), not `## D` headings.
- Parallel conversations have **no merge protocol.**
- This environment has no access to raw faction-pack PDFs and likely never will. Any future
  faction-pack tooling work needs Ryan to run the script locally and share real output.
