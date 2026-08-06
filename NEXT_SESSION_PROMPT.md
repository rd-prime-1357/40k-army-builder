# NEXT SESSION PROMPT — Session 196

## Turn type: data-only. No exceptions.

Read `SESSION_HANDOFF_195.md` first, then this prompt. Session 195 shipped Thousand Sons as B89's
first MFM v1.1 migration (and, riding along, B94's first `fourth_plus` faction — Rubric Marines,
Chaos Rhino). This session is B89's **second** per-faction migration.

## Session open
1. Baseline: `./baseline.sh --fetch --data-turn`.
2. Verify S195's hashes via `pipeline_manifest.json` (the authoritative source), not by hand-copying
   the handoff table.
3. Confirm Ryan has pushed S195's changes.

## This session's work — B89's second migration

**Data only — regenerating committed JSON from already-shipped tooling. Do not touch
`mfm_points_parser.py`, `convert_to_json.py`, `baseline.sh`, or any other pipeline code this session.**

**Recommendation (mine to make, not a call for Ryan): Death Guard next.** It was S195's other
candidate — `units_repro_check.py`'s own docstring calls it "fully self-sourced... no cross-file
append, no chapter points," same simple shape as Thousand Sons. No Death Guard esc4 units are known
yet (S195 didn't check) — confirm during this session's diff whether any of Death Guard's units gain
`fourth_plus` under v1.1, same as Thousand Sons' two did; don't assume there are none.

**Steps, mirroring S195's approach exactly:**
1. Hash-verify `MFM_Death_Guard_v1.1.txt` and `_v1_0.txt` directly against `source_manifest.json`
   (don't assume from the baseline's own source-fetch pass). Diff the two MFM text files directly
   first to see what actually changed for this faction before running anything.
2. Run the **full** `units_repro_check.py` chain, not just transform→points→convert — S195 found that
   skipping the merge-time post-processors (`add_loadout_groups`, `add_co_leader`,
   `add_bodyguard_stat_flags`, `add_chapter_point_overrides`) produces a false structural diff
   (`bodyguard_stat_flags` keys go missing). The cleanest approach is patching a working copy of
   `units_repro_check.py` itself (swap Death Guard's MFM file + add `--emit-fourth-plus` to its build
   block only) and running the full `repro()` function, same as S195 did.
3. Confirm all 15 non-Death-Guard armies come out byte-identical — if anything outside Death Guard
   moves, stop and investigate before accepting.
4. Key-level diff Death Guard's block. Expected: points values (check `MFM_v1_1_Reconciliation.md`'s
   Death Guard section for the pre-computed adopt-mechanically list and cross-check against it, the
   way S195 did for Thousand Sons) plus `fourth_plus` on any Death Guard esc4 units. Anything else is
   a structural regression — stop and investigate.
5. Check `rules_assertions.py` for any pinned Death Guard points values needing reconciliation (S195
   found none for Thousand Sons — don't assume the same is true here without checking).
6. Update `source_manifest.json` only if it actually needs it — S195 found no change was needed
   (both source files were already correctly hashed); verify the same is true here rather than
   assuming.
7. Update `units_repro_check.py` permanently: add `MFM_Death_Guard_v1.1.txt` to `REQUIRED`, swap
   Death Guard's build block to it with `--emit-fourth-plus`. Keep `_v1_0.txt` in `REQUIRED` too if
   anything else still depends on it (check before removing — Thousand Sons' migration kept its
   `_v1_0.txt` required for CSM's cross-legion cult-troop pricing; verify whether Death Guard has an
   equivalent dependency before dropping it).
8. Commit the regenerated `units.json`, updated `source_manifest.json` (if needed), and updated
   `units_repro_check.py`.

**Do not migrate any faction beyond Death Guard this session.** One faction, diff-guarded and
verified, banked cleanly, beats a partial multi-faction migration.

## Standing reminders
- Turn-typing strict: data only. No pipeline code changes (the `units_repro_check.py` edit is a
  change to the check, not the pipeline).
- Fix parsers/schema, never hand-edit output — this session runs the existing pipeline.
- Diff-guard before banking: any regenerated output is verified by key-level diff against the prior
  committed file before being accepted.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `pipeline_manifest.py --freshness-check` as the **last** command — after every other edit, including
  edits to the handoff itself (leave the handoff's own row in its Files table as "(this file)").
