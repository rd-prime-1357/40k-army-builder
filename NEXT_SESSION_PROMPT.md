# NEXT SESSION PROMPT — Session 194

## Turn type: tooling-only. No exceptions.

Read `SESSION_HANDOFF_193.md` first, then this prompt. Read **D286** in `40K_Decision_Log.md` in
full before starting — it carries B94's engine turn (the schema/lookup/mirror that shipped S193) and
opens B96. This session is B94's **pipeline-emit tooling turn**, the direct dependency that unblocks
B94's later data turn.

## Session open
1. Baseline: `./baseline.sh --fetch --data-turn`. (Use `--data-turn` — this turn reads GW sources,
   and it also sidesteps the B96 false-failure until B96 is fixed.)
2. Verify the S193 hashes in the handoff's Files section at open.
3. Confirm Ryan has pushed S193's changes (`repo_check` / `fetch-verify` will flag drift otherwise).
4. `40K_Decision_Log.md` mount question (open since S192): still absent from the `/mnt/project` mount
   but present and current in the repo at close of S193. If Ryan reports it present now, treat the
   earlier finding as resolved mount staleness; if still absent, it is a real project-area gap worth
   a file-list screenshot, since this prompt and the next depend on reading it at open.

## This session's work — B94 pipeline-emit (tooling)

**Tooling only — the parsers and the JSON build path. Do NOT regenerate committed `units.json` this
session (that is B94's data turn, and it folds into B89 so the 34 units migrate once).**

The engine (S193/D286) now honours an optional `points.sizes[*].fourth_plus` tier via `copyTierPts`,
but no data can reach it yet: `mfm_points_parser.py`'s `to_points_row` attaches the 4th tier as
`_esc4_fourth_plus` to the in-memory parse `info` only — it is **not** written into the CSV row, so
it never survives to `units.json`. This turn:
- Read `to_points_row` and the CSV column contract it emits (`Size_1..3` + `Points_b-t` +
  `Allied_Group`) **directly** before designing — the row shape is fixed-column, so carrying a 4th
  tier means either new columns or a documented side-channel; pick the mechanism that convert/merge
  can read without ambiguity, and check `convert_to_json.py`/`merge_factions.py`'s reader for the
  existing tiers before adding to it.
- Teach the pipeline to carry `_esc4_fourth_plus` through into `points.sizes[*].fourth_plus` on the
  affected rows, and to emit **no** `fourth_plus` key on rows that don't have a 4th break (the engine
  fallback depends on absence, not on a `fourth_plus == third_plus` sentinel).
- Verify against synthetic input and the parser's own output that the 34 esc4 units would now carry a
  correct `fourth_plus` and every other unit carries none — **without** regenerating the committed
  `units.json`. The reproduction gates must still pass against the currently-committed 3-tier data
  (i.e. the pipeline change must be provably inert until the data turn runs it).
- `b87_check.js` already pins the parser's `_esc4_fourth_plus` capture; extend it (or add the check)
  to pin that the row/JSON now carries `fourth_plus` through to the built structure.

**Fold in B96 (also tooling, XS):** move `b87_check`/`b88_check` from `baseline.sh`'s always-run block
into the `if [ "$SOURCES_OK" -eq 1 ]` block so they `SKIP` cleanly when sources are absent, matching
the three repro checks. Two tooling items in one tooling session is turn-consistent; keep them as
separate, clearly-labelled edits for clean bisection.

## Standing reminders
- Turn-typing strict: tooling only. If the pipeline change turns out to need a coupled data
  correction the way B87 did, stop and scope the data as its own turn — there is no shipped-live-bug
  forcing reason here (the engine falls back gracefully), so the B87 exception does not apply.
- Fix parsers/schema, never hand-edit output.
- Source-first: read `to_points_row`'s real column contract and convert/merge's real reader before
  designing the carry-through — the S192/S193 findings both came from reading the actual consumer,
  not the ticket's framing.
- Do not regenerate `units.json`. The data turn (folding into B89) and the data-side assertion are
  later turns per D283/D286.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `pipeline_manifest.py --freshness-check` as the **last** command — after every other edit,
  including edits to the handoff itself (leave the handoff's own row in its Files table as
  "(this file)").
