# NEXT SESSION PROMPT — Session 252

## Read first

`SESSION_HANDOFF_251.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

State at S251 close: `index.html` **v6.26** (unchanged — S251 was a data turn), decision log through
**D348**, `SCHEMA_VERSION` **5**, baseline **41/41**, rules assertions **137/137**, **25 open**
backlog items.

## Open

Run `./baseline.sh --fetch --data-turn`. It covers every gate in one command. **41/41 must pass.**
If a gate fails, reconcile before starting — do not work around it.

Then verify the S251 file hashes in `SESSION_HANDOFF_251.md`'s Files table against the fetched repo.
This is deliberately redundant with `repo_check`, so a bad sync is still caught when the repo is
unreachable or stale.

## Assigned work: B137 — data turn

**Type this turn data-only.** No engine or tooling work mixed in.

Chaos Space Marines' `units.json` block still builds from `MFM_Chaos_Space_Marines_v1_0.txt` and is
shipping wrong points today. Read B137's full entry in `OPEN_ITEMS_BACKLOG.md`, then **re-derive the
diff from the two MFM files yourself before planning anything**. B137's numbers were measured at
S251 and are good, but S251's own opening lesson was that a ticket's population figure is a snapshot
— the entry says 17 units and three tier-shape changes; confirm that against source rather than
building to it.

The shape mirrors S212's detachments migration and S198's Space Marines group turn: re-point
`units_repro_check.py`'s CSM block and its four `CSM_CULT_TROOP_POINTS` entries at the v1.1 files,
add `--emit-fourth-plus` to the CSM convert call, regenerate, diff-guard, reconcile any pinned points
value in `rules_assertions.py` against the new source rather than loosening it.

**Three things to check rather than assume.**

1. **A unit-count diff-guard is not sufficient here.** Three units change tier *shape*, not value —
   Accursed Cultists, Dark Commune and Chosen move from `1st unit`/`2nd +` to `1st to 2nd`/`3rd +`,
   so the **second copy's** price moves even where the printed numbers did not. Read the changed
   `second_unit` cells directly.
2. **The four cult troops are cross-file appends, priced from their god-legion's MFM, not CSM's.**
   Two of them currently disagree with their own parent legion (Plague Marines 180 in DG / 190 in
   CSM; Khorne Berzerkers 170/330 in WE / 180/345 in CSM). Migrating CSM's own file alone does not
   fix those — the `CSM_CULT_TROOP_POINTS` entries must move too, and the result should be checked
   for agreement with the parent legion's committed block afterwards.
3. **Whether `MFM_Chaos_Space_Marines_v1_0.txt` still belongs in `units_repro_check.py`'s `REQUIRED`
   list after the swap.** Check what reads it; do not carry it forward by default and do not delete
   it on assumption.

**`B94-2` will police the 4th tier for you.** The moment CSM's Chaos Rhino prices move to 65, the
assertion demands its `fourth_plus` of 75 and fails loudly if `--emit-fourth-plus` was forgotten.
That is the gate working as designed — if it fires, add the flag, do not touch the assertion. **B94
closes when B137 does**, on that one unit.

**Flag the model before any analysis turn.** Deciding whether a tier-shape change is read correctly,
and reconciling a cult-troop price against its parent legion, is analysis; regenerating, diffing,
running gates and writing docs are mechanical.

## Precedents from S251 that will matter again

**A ticket's population figure is a snapshot, not a fact.** B94 said 31 units remained; the real
number was 5, because four factions had picked the field up in their own build turns and nobody
updated the entry. Re-derive from source before scoping. This is the second session running where
re-deriving changed the answer.

**A gate that reproduces the pipeline cannot see an incompletely-invoked pipeline.**
`units_repro_check.py` reproduced a `convert_to_json.py` call missing `--emit-fourth-plus` as
faithfully as a correct one, for fifty sessions, green the whole time. When adding an opt-in flag to
the pipeline, the assertion that the flag is *passed where it should be* is a separate piece of work
from the flag itself — and it belongs in the same turn.

**An assertion that needs to know which source file a faction is built from should elect it, not be
told it.** `B94-2` scores every candidate MFM file against the committed prices and takes the top
scorer, so a migration is picked up automatically. A hardcoded army→filename map is exactly the
artefact that went stale here.

**Report, don't fail, on known-open debt.** `B94-2` reports an army still on a v1_0 source rather
than failing — a gate that goes red on tracked, ticketed work stops every session until it is done.

**D0 forbids finished illegal armies, not intermediate steps of a visibly-flagged multi-part edit**
(D346, Ryan's ruling, still current). And **a unit has a keyword if any of its models has it**
(D346) — any keyword test must read `model_keyword_names` as well as `keyword_names` and
`faction_keyword_names`.

## Close

Four rolling documents updated (`40K_Decision_Log.md`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_252.md`), this file rewritten for S253, then:

1. add `SESSION_HANDOFF_252.md` to `pipeline_manifest.py`'s `GUARDED` list **before** writing
2. `python3 pipeline_manifest.py --write`
3. `python3 pipeline_manifest.py --freshness-check`

Those two commands are the literal last two of the session.

## Outstanding Ryan action carried forward from S248, S249 and S250

**A render check covering three sessions' UI.** S248's Tank Ace checkbox, S249's Mark of Chaos
selector, S250's silent truncation of an over-cap tally on size reduction. S251 shipped no UI, so
the backlog is three deep and unchanged rather than four. S250's is the one that matters most — it
is the only one that edits a saved list without telling the player. All three handoffs carry
step-by-step scripts. If S252 ships a fourth unseen engine change, say so plainly in the handoff
rather than letting it accumulate quietly.
