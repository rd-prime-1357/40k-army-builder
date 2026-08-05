# NEXT SESSION PROMPT — Session 191

## Turn type: depends on what's answered at open (see below).

Read `SESSION_HANDOFF_190.md` first, then this prompt. Read **D283** in `40K_Decision_Log.md` in
full before starting — it carries the B87 close, the Rubric Marines fix, the B90 answer, and the B88
rescope, and the next work items branch off it.

## Session open
1. Data-turn baseline with sources: `./baseline.sh --fetch --data-turn`.
2. Verify the S190 hashes in the handoff's Files section at open.
3. Confirm Ryan has pushed S190's changes and deleted the five old-named files (carried over from
   S189, still outstanding: `40K_Decision_Log_v3_0.md`, `40K_Architecture_Overview_v0_5.md`,
   `40K_Data_Dictionary_v2_0.md`, `40K_Data_Pipeline_Process_v0_6.md`, `40K_Functional_Spec_v0_7.md`).
   If not yet done, that's expected drift, not a failure — proceed, but don't write new content to any
   old-named file if one is still present.
4. The project mount may not carry `40K_Decision_Log.md` / `BACKLOG_ARCHIVE.md` — pull from a repo
   clone and verify hashes rather than treating absence as loss (as S189 and S190 both did).

## What's next — check in this order

**If Ryan has answered B94 (copy-4 tier schema — real 4th tier vs fold rule) →** that's the natural
next arc, but it's engine-first (schema + `resolveUnits`/points lookup in `index.html` + the
`resolved_pool`/points mirror in `rules_assertions.py`), then data, then assertion — strictly
separated. Do NOT start it as a mixed turn. If Ryan picks "add the real tier" (the recommendation),
turn 1 is the engine/schema change only. Full scope in the B94 backlog entry.

**Else -> B88 (MFM v1.1 reconciliation reports + v1.1 detachment-layout parsing).** B87 is done, so
B88 is unblocked. It has two parts now (D283 rescope): first extend `detachment_parser.py` with
v1.1-layout support (its `MFM_DP_RE`/`MFM_ENH_RE` assume v1_0 — DP jammed onto the name, bulleted
enhancements; v1.1 puts DP on its own line and drops the bullet), mirroring B87's sniff-and-normalize
approach; then generalize `mfm_reconcile.py` to emit a per-faction delta report (points, roster,
attach lists, Leader/Support flips, wargear, detachment deltas) comparing each faction's newest
capture against its built-from version. **Tooling turn.** Output is B89's work order.

If neither is available, fall back to the next backlog item under the faction priority order rather
than blocking. Note B90 turn 2 is now fully unblocked on decisions but still sequences after B88/B89
per D274.

## Standing reminders
- Turn-typing strict. S190 is a live example of the one exception's shape: a tooling fix that
  corrects a parser will change the data that parser produces, and you cannot leave the repro gate
  red. When that happens, regenerate the coupled data through the real pipeline in the same turn
  (never shim the gate to reproduce a known-wrong value) and record it as a coupled correction — but
  that is only for data the fix itself forces, not an excuse to mix unrelated data work.
- Fix parsers, never hand-edit output. `units.json`'s two corrected values this session came from a
  real pipeline run, not an edit.
- Source-first: the B90 answer, the Rubric Marines bug, and the B88 rescope were all found by reading
  the actual MFM files and the actual parsers, not the tickets' summaries of themselves.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `--freshness-check` as the **last** command — after every other edit, including edits to the
  handoff itself (leave the handoff's own row in its Files table as "(this file)").
