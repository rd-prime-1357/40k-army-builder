# NEXT SESSION PROMPT — Session 250

## Read first

`SESSION_HANDOFF_249.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

State at S249 close: `index.html` **v6.25**, decision log through **D346**, `SCHEMA_VERSION` **5**,
baseline **40/40**, rules assertions **133/133**, **24 open** backlog items.

## Open

Run `./baseline.sh --fetch --data-turn`. It covers every gate in one command. **40/40 must pass**,
including the new `b126_check`. If a gate fails, reconcile before starting — do not work around it.

Then verify the S249 file hashes in `SESSION_HANDOFF_249.md`'s Files table against the fetched repo.
This is deliberately redundant with `repo_check`, so a bad sync is still caught when the repo is
unreachable or stale.

**Two things to check rather than assume at open.** First, S248's handoff recorded its close as
38/38 when the gate it added made it 39/39; that number is wrong and S249 corrected it. Do not use
any pre-S249 handoff's gate count as a comparison baseline. Second, if a `^### ` grep of the
backlog's Open Items section disagrees with its stated count, that is a real defect to fix, not a
discrepancy to explain — S249 found three closed-pointer stubs sitting there and removed them.

## Assigned work: B103 — engine turn

**Type this turn engine-only.** No data or tooling work mixed in.

`loRollup`'s multi-model body branch pushes every tallied `replacement_choices` pick into `emit` and
only then clamps the total for the source charge. Two consequences, both live: more replacement
weapons can be emitted than the cap allows, and because the *source* charge is the clamped figure,
`overAllocated` never sees the overrun — the list reads clean while being wrong. The fixed-1 branch
clamps differently again (bounding each pick against the remaining cap as it goes), so the two
branches disagree on the same shape.

Read B103's full entry in `OPEN_ITEMS_BACKLOG.md`, then re-derive from source before planning
anything. The entry describes what was seen at S201; it is not evidence about what is true now.

**Sequencing note.** B127 sits above B103 in the header list but is not buildable — it is source
acquisition, and its own entry says there is nothing to build until source exists. B93 is the other
obvious candidate and was passed over deliberately: it is L, spans sessions, and is partly blocked by
B127's 74 text-less records. B103 is engine, M, self-contained, and affects the points of already-
saved lists across shipped factions, which makes it the higher-value pick.

**This ticket changes the points of saved lists, so it needs a census before a fix.** Establish which
shipped units can actually reach an over-cap tally, and get before/after figures, before touching
`loRollup`. A fix that silently re-prices existing lists without knowing which ones it moves is not
shippable.

**Product call to put to Ryan, batched — do not stop the session for it.** When a saved list exceeds
a cap, should the engine clamp silently or clamp *and* fire `overAllocated`? S201's reading, recorded
in the ticket, is that it should clamp silently (D0 — the state was never legal, so there is nothing
to warn about) and that `overAllocated` should stay reserved for genuine same-source contention.
Proceed on that reading and surface it in the handoff unless the census turns up something that
makes it wrong.

**Flag the model before any analysis turn.** The census, the branch-reconciliation call and the
clamping decision are analysis; baselines, diffs, doc writing and harness edits are mechanical.

## Precedents from S249 that will matter again

**D0 forbids finished illegal armies, not intermediate steps of a visibly-flagged multi-part edit.**
Ryan's ruling. S249's first build refused a mark change that would leave an attached pair
mismatched; that was over-strict, because re-marking a pair is inherently two clicks and refusing
the first one forces a detach-and-reattach dance. The attach itself is still refused outright. When
a rule couples two entries, ask whether the illegal state is a *destination* or a *waypoint* before
gating it. This bears directly on B103's clamp-silently-or-warn question.

**A unit has a keyword if any of its models has it.** Ryan's ruling, D346. Any keyword test must
read `model_keyword_names` as well as `keyword_names` and `faction_keyword_names`, or it will
silently miss units whose keyword sits on one model. `Masters of the Maelstrom` has an empty
`keyword_names` with everything at model level; `Dark Commune`'s `PSYKER` is on the `MINDWITCH`
model alone. `markKeywordSet` in `index.html` and `_mark_kw_set` in `rules_assertions.py` are the
reference implementations. `unitInTankAcePool` deliberately does not do this — check which behaviour
a new test needs rather than copying either by default.

**A slice-based harness passing is not evidence its slice is complete.** `e4b_check.js` and
`e4c_check.js` both passed at S249 with a latent `ReferenceError` in place, because no existing
fixture reached the new code path. If a change makes an existing function call something new, trace
which harnesses slice that function and extend their slices — do not wait for a red gate. B103
touches `loRollup` and `wargearCostForRollup`, which several harnesses slice.

**A rule about state the app does not model is unrepresentable, not unenforced.** `enforced: false`
means "a representable effect deliberately left off", and `E21a-4` asserts that inventory is empty.
Use `unmodelled_restrictions` on the effect instead, with a `why_unmodelled` reason, and open a
ticket for the feature it would need first.

## Close

Four rolling documents updated (`40K_Decision_Log.md`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_250.md`), this file rewritten for S251, then:

1. add `SESSION_HANDOFF_250.md` to `pipeline_manifest.py`'s `GUARDED` list **before** writing
2. `python3 pipeline_manifest.py --write`
3. `python3 pipeline_manifest.py --freshness-check`

Those two commands are the literal last two of the session.

## Outstanding Ryan action carried forward from S248 and S249

**A render check covering both sessions' UI.** Two engine turns have now shipped without anyone
looking at them on screen — S248's Tank Ace checkbox and S249's Mark of Chaos selector, roster
sub-lines and modal pills. Both handoffs carry step-by-step scripts. If S250 ships a third unseen
engine change, say so plainly in the handoff rather than letting it accumulate quietly.
