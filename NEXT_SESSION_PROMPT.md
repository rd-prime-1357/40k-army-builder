# NEXT SESSION PROMPT — Session 251

## Read first

`SESSION_HANDOFF_250.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

State at S250 close: `index.html` **v6.26**, decision log through **D347**, `SCHEMA_VERSION` **5**,
baseline **41/41**, rules assertions **136/136**, **24 open** backlog items.

## Open

Run `./baseline.sh --fetch --data-turn`. It covers every gate in one command. **41/41 must pass**,
including the new `b103_check`. If a gate fails, reconcile before starting — do not work around it.

Then verify the S250 file hashes in `SESSION_HANDOFF_250.md`'s Files table against the fetched repo.
This is deliberately redundant with `repo_check`, so a bad sync is still caught when the repo is
unreachable or stale.

**One thing to check rather than assume at open.** S250 shipped a change that silently edits saved
lists — an over-cap `replacement_choices` tally is now truncated in storage, not just clamped on the
way out. If Ryan reports a saved list whose points moved, that is expected behaviour and the seven
affected units are named in the S250 handoff; it is not a regression to chase.

## Assigned work: B94 — data turn

**Type this turn data-only.** No engine or tooling work mixed in.

B94's copy-4 tier schema is built and its engine, pipeline-emit and first two data turns have all
shipped (D286/D287/D288/D289). What remains is the data turn folded into B89 — the per-faction pass
applying the real 1st-to-3rd / 4th+ rows. Read B94's full entry in `OPEN_ITEMS_BACKLOG.md` and B89's
alongside it, then re-derive the remaining population from the MFM sources before planning anything.
Both entries describe what was true several sessions ago; neither is evidence about what is true now.

**Sequencing note, so it is not re-litigated.** B136 was opened by S250 and is small, but it is
unreachable on today's data by a scan run that session — nothing can hit the bad path until a
faction ships a `requires_weapon` gate whose prerequisite is itself a replacement choice — so it is
deliberately below a ticket that moves real data. B127 remains unbuildable (source acquisition, and
its own entry says there is nothing to build until source exists). B93 is still L, spans sessions,
and is still partly blocked by B127's 74 text-less records. B90 blocks further faction work and is
the obvious candidate after B94.

**Diff-guard this one hard.** A points data turn must confirm that exactly the expected units
changed and zero others before anything is promoted. `units_repro_check.py` reproducing byte-for-byte
is necessary, not sufficient — it proves the pipeline is deterministic, not that the change was the
one intended.

**Flag the model before any analysis turn.** Reading a points table against source and deciding
which tier a row belongs to is analysis; regenerating, diffing, running gates and writing docs are
mechanical.

## Precedents from S250 that will matter again

**A single fixture is not a census.** S250's first pass at the re-pricing census filled each option's
cap one way and found five affected units. Filling the same cap three different ways found seven.
When a claim is "these are the units affected", vary the input shape before believing the answer —
the fill that happens to be written first is not the one a player would necessarily build.

**A gate that has not been negative-tested is not known to be a gate.** `b103_check.js` was run
against a copy of the engine with the single defect line restored and confirmed to fail 10
assertions. This costs one command and is the only thing that distinguishes a real gate from one
that passes because it tests nothing. Do it for every new harness.

**Reachability is worth establishing before scope.** B103's whole population turned out to be "a
saved list whose size bracket was reduced", which made the census tractable and the fix small. The
same question applied to `loCarriers` found zero reachable cases, which turned a tempting scope
widening into B136. Ask what can actually reach the bad path before deciding how big the ticket is.

**`loMaxCount` returns 0, not Infinity, for an option with no cap field.** An uncapped option of that
shape does not mean "no limit" — it means the rollup silently emits nothing. `B103-1` now asserts
every `replacement_choices` option carries an authored cap. If a parser change makes that assertion
fail, the fix is in the parser, not in the assertion.

**D0 forbids finished illegal armies, not intermediate steps of a visibly-flagged multi-part edit**
(D346, Ryan's ruling, still current). And **a unit has a keyword if any of its models has it**
(D346) — any keyword test must read `model_keyword_names` as well as `keyword_names` and
`faction_keyword_names`.

## Close

Four rolling documents updated (`40K_Decision_Log.md`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_251.md`), this file rewritten for S252, then:

1. add `SESSION_HANDOFF_251.md` to `pipeline_manifest.py`'s `GUARDED` list **before** writing
2. `python3 pipeline_manifest.py --write`
3. `python3 pipeline_manifest.py --freshness-check`

Those two commands are the literal last two of the session.

## Outstanding Ryan action carried forward from S248, S249 and S250

**A render check covering three sessions' UI.** Three engine turns have now shipped without anyone
looking at them on screen — S248's Tank Ace checkbox, S249's Mark of Chaos selector, and S250's
silent truncation of an over-cap tally on size reduction. All three handoffs carry step-by-step
scripts. S250's is the one that matters most, because it is the only one that edits a saved list
without telling the player. If S251 ships a fourth unseen engine change, say so plainly in the
handoff rather than letting it accumulate quietly.
