# NEXT SESSION PROMPT — Session 258

## Read first

`SESSION_HANDOFF_257.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

State at S257 close: `index.html` **v6.27** (untouched this session), decision log through
**D354**, `SCHEMA_VERSION` **5**, `rules_assertions.py` at **139** assertions, **42** gates in
`baseline.sh`, **23 open** backlog items.

## Open

**Before anything else: confirm `detachments_repro_check.py` in the project area matches the
repo.** This has now been stale at open for two consecutive sessions (S256, S257) despite the ask
each time. If still stale, take the repo copy, say so, and consider raising to Ryan directly
whether the re-upload step should just be dropped in favor of always pulling the repo copy at
open — see S257 handoff's Ryan action.

Then run `./baseline.sh --fetch --data-turn` and verify the S257 file hashes in
`SESSION_HANDOFF_257.md`'s Files table against the fetched repo.

## Assigned work: B93 turn 4 — the final tooling pass, closing the arc

**Turn type: tooling.** Do not touch `index.html`, `detachments.json` or any parser this session.

The four-turn sequence `B93_SCOPE.md` §7 laid out is functionally complete: data (S254, D351),
engine (S256, D353), independent census (S257, D354). Turn 4 is not new mechanism — it is closing
out the paper trail so nothing is left half-stated across the documents that describe B93:

1. **`B93_SCOPE.md` itself.** Written S240 under D334/D335 with a recommended mechanism section
   (§7) that predates the actual build. Add a short status note at the top (or a new final
   section) recording what actually shipped and where: data turn S254, engine turn S256, census
   turn S257, and that §7.2's "demote the type gate" instruction was superseded by D335 and never
   built (already recorded in D353, but not yet reflected in the scope doc itself — the doc still
   reads as a forward-looking plan). Do not rewrite the historical sections; append a closing note.

2. **`OPEN_ITEMS_BACKLOG.md`'s B93 entry.** Move it from Open Items to Closed / Shipped once this
   turn's close note is written, following the standing rule that an item moves to Closed/Shipped
   as soon as its last piece of work ships. Confirm first that there is no fifth piece hiding —
   re-read `B93_SCOPE.md` §4 (the four blockers) and confirm all four are actually resolved:
   B125 (closed S243), B128 (closed — verify session), B126 (closed — verify session), B127
   (still open — confirm B127 is NOT a B93 blocker for closing B93 itself, since B127 covers the
   74 no-text records, which are simply out of scope for a bearer restriction that does not
   exist; re-read `B93_SCOPE.md` §6 to confirm this reading before closing B93).

3. **Sanity pass on `b93_check.js` and `B93-ENGINE-CENSUS`'s continued agreement.** No new
   population change is expected this session (no data/engine turn), so this is a re-run and
   confirm, not new work — but confirm explicitly rather than assuming turn 3's numbers still hold
   after any repo sync.

4. **Only if it fits:** the render check backlog (five sessions deep now — S248, S249, S250,
   S256, and nothing new from S257 since it touched no UI) is Ryan's action, not a session task,
   but if B93 closes cleanly with time remaining, a written note summarizing exactly what a
   from-scratch verification pass would need to check (consolidating the four separate scripts
   currently scattered across handoffs into one place) would reduce the chance a fifth item gets
   added to an already-long list Ryan has not had a chance to work through.

## Precedents that will matter again

**A check can pass for the wrong reason.** B129's `Thicket of Bladed Bone` exemption was zero for
one reason (its own parser missed an alias) while being justified for a different, wrong reason
(mistaking an Upgrade for a Character-gated record). Two independent-looking checks agreeing is
not the same as either one being right — cross-checking against a genuinely independent
derivation (this session's `B93-ENGINE-CENSUS`) is what surfaced it, not re-reading either check's
own logic in isolation.

**When a prompt or scope document cites a decision and an instruction that disagree, the decision
wins.** Third time this has mattered across B93 alone (D350's stale premise, S256's §7.2, this
session's D351 framing of the SPAWN alias).

## Close

Four rolling documents updated (`40K_Decision_Log.md`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_258.md`), this file rewritten for S259, then:

1. add `SESSION_HANDOFF_258.md` to `pipeline_manifest.py`'s `GUARDED` list **before** writing the
   handoff's Files table — this file's own hash is one of that table's rows and gets edited a
   second time by the append; see `pipeline_manifest.py`'s FILES-TABLE ORDERING note (added S257)
2. `python3 pipeline_manifest.py --write`
3. `python3 pipeline_manifest.py --freshness-check`

Those two commands are the literal last two of the session.

## Outstanding Ryan actions carried forward

**`detachments_repro_check.py` re-upload**, two sessions overdue as of S257 — see that handoff's
Ryan action for the suggestion to just drop the ask if it keeps being missed.

**A render check covering five sessions' UI**, unchanged since S257 (which touched no UI):
S248's Tank Ace checkbox, S249's Mark of Chaos selector, S250's silent truncation of an over-cap
tally on size reduction, S256's enhancement picker. S250's is still the one that matters most —
the only one that edits a saved list without telling the player. Scripts are in the named
handoffs.
