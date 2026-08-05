# NEXT SESSION PROMPT — Session 192

## Turn type: depends on what's answered at open (see below).

Read `SESSION_HANDOFF_191.md` first, then this prompt. Read **D284** in `40K_Decision_Log.md` in
full before starting — it carries the B88 close (both parts) and the B95 open, and the next work
items branch off it.

## Session open
1. Baseline: `./baseline.sh --fetch --data-turn`.
2. Verify the S191 hashes in the handoff's Files section at open.
3. Confirm Ryan has pushed S191's changes.
4. If a repo-vs-mount check disagrees mid-session, re-check before treating it as a finding — S191
   caught itself mid-push once and briefly mis-read a partially-pushed repo as stale drift.

## What's next — check in this order

**If Ryan has answered B94 (copy-4 tier schema — real 4th tier vs fold rule) ->** engine-first (schema
+ `resolveUnits`/points lookup in `index.html` + the `resolved_pool`/points mirror in
`rules_assertions.py`), then data, then assertion — strictly separated, do NOT start as a mixed turn.
If Ryan picks "add the real tier" (the recommendation), turn 1 is the engine/schema change only. Full
scope in the B94 backlog entry.

**Else if Ryan has answered B95 (faction_taxonomy.json `built` flag for CSM/Thousand Sons) ->** small
doc/data turn to reconcile the flag with reality (or document why "built" means something narrower);
should close in one session.

**Else -> B89 (MFM v1.1 adoption arc), but sequenced behind B94 by design (D283/D284): the copy-4
shape B94 will decide touches 34 units across nearly every faction, so starting B89's per-faction
migration before B94 resolves risks a two-pass re-migration for those units. If B94 is still
unanswered, do not start B89 broadly.** Instead fall to the next backlog item under the faction
priority order (standing project instructions) — check `OPEN_ITEMS_BACKLOG.md`'s Open Items section
for the next unblocked item in priority order rather than blocking the session.

`MFM_v1_1_Reconciliation.md` (S191) is B89's work order once it starts: 189 deltas classified
adopt-mechanically, 71 investigate-first, across the 10 built-army faction files. Read it before
scoping B89's first turn.

## Standing reminders
- Turn-typing strict, no exceptions except the documented B87/S190-shape one (a tooling fix that
  forces a coupled data correction, regenerated through the real pipeline in the same turn, never
  shimmed).
- Fix parsers, never hand-edit output.
- Source-first: three real findings this session (the Hexwarp bare-marker DP line, the World Eaters
  `UNIQUE TAG REMOVED` note, and the reconcile script's own force-disposition misclassification) were
  all caught by testing against actual source files and actual output, not assumed from the B87
  precedent or a first draft.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `--freshness-check` as the **last** command — after every other edit, including edits to the
  handoff itself (leave the handoff's own row in its Files table as "(this file)").
