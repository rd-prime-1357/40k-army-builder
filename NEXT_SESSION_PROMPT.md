# NEXT SESSION PROMPT — Session 195

## Turn type: data-only. No exceptions.

Read `SESSION_HANDOFF_194.md` first, then this prompt. Read **D287** in `40K_Decision_Log.md` in full
before starting — it carries B94's pipeline-emit turn (the opt-in `--emit-fourth-plus` mechanism that
shipped S194) and folds B96 closed. This session is B94's **data turn**, which per D283 folds into
B89's MFM v1.1 adoption arc rather than running standalone.

## Session open
1. Baseline: `./baseline.sh --fetch --data-turn`.
2. Verify the S194 hashes in the handoff's Files section at open (the manifest itself is the
   authoritative hash source — the handoff table intentionally points to it rather than hand-copying
   values, to avoid the exact staleness this session's open had to reconcile).
3. Confirm Ryan has pushed S194's changes.

## This session's work — B94 data turn, folded into B89's first migration

**Data only — regenerating committed JSON from already-shipped tooling. Do not touch
`mfm_points_parser.py`, `convert_to_json.py`, `baseline.sh`, or any other pipeline code this session.**

B89 is the MFM v1.1 adoption arc: per-faction data-only turns that regenerate points from each
faction's `_v1.1.txt` source (instead of `_v1_0.txt`), run the full pipeline through convert and merge,
and key-level diff against committed output — expected diffs are points values only, any structural
diff investigated before acceptance. No faction has migrated yet; `units_repro_check.py` still builds
every priority faction from `_v1_0.txt`. B94's data turn is the same shape of work (regenerate,
diff-guard, verify) but additionally passes `convert_to_json.py --emit-fourth-plus`, so a faction's
v1.1 migration and its esc4 4th-tier capture land in one diff-guarded pass rather than two.

**Recommendation (mine to make, not a call for Ryan): start with Death Guard or Thousand Sons, not
Space Marines.** `units_repro_check.py`'s own docstring notes both are "fully self-sourced... no
cross-file append, no chapter points" — the simplest builds in the priority set. Space Marines' build
pulls in five chapter-override files (Black Templars, Blood Angels, Dark Angels, Death Watch, Space
Wolves) layered through `add_chapter_point_overrides.py`, which is real added complexity for a first
migration proving out both the v1.1 layout switch and `--emit-fourth-plus` together. Prove the pattern
on the simpler faction first; Space Marines and its chapters follow as their own turn(s) once the
pattern is confirmed clean. Thousand Sons is probably the better of the two: it's already the faction
this project's build scope is focused on (`THOUSAND_SONS_BUILD_SCOPE.md`), and S194 already verified
its esc4 units (Rubric Marines, Chaos Rhino) by hand — this session would be extending that same
verification into a real committed-data change rather than starting cold.

**Steps, for whichever faction is chosen:**
1. Re-verify the chosen faction's `_v1.1.txt` source against `source_manifest.json` (should already be
   verified by the baseline's `source-fetch` step; confirm rather than assume).
2. Run the real per-faction pipeline — `wahapedia_transform.py` -> `mfm_points_parser.py` (pointed at
   the `_v1.1.txt` file, not `_v1_0.txt`) -> `convert_to_json.py --emit-fourth-plus` — mirroring
   `units_repro_check.py`'s own per-faction block for that army, but swapping the MFM file and adding
   the flag.
3. Key-level diff the regenerated units.json blocks for that faction against the currently-committed
   ones. Expected diffs: points values from the v1.1 source revision (may differ from v1_0 — check
   whether GW actually re-priced anything in v1.1 for this faction, don't assume it's identical), plus
   `fourth_plus` newly present on that faction's esc4 units. Any diff outside those two categories is a
   structural regression — stop and investigate before accepting.
4. Update `source_manifest.json` for the migrated faction per B89's own instruction.
5. Regenerate `units_repro_check.py` / `repro_check.py` to build from the new v1.1 source + flag for
   that faction going forward (the harness's `REQUIRED`/build-block logic will need the faction's
   `_v1.1.txt` swapped in and `--emit-fourth-plus` added to its `mfm_points_parser.py` call — this is a
   tooling change to the *check*, not the pipeline; if it turns out to require touching
   `mfm_points_parser.py`/`convert_to_json.py` themselves, stop and scope that as a separate tooling
   turn rather than mixing it into this data turn).
6. Commit the regenerated `units.json`, `source_manifest.json`, and updated repro-check.

**Do not migrate every faction this session.** One faction, diff-guarded and verified, banked cleanly,
beats a partial multi-faction migration. The remaining priority-order factions continue under B89 in
later sessions; B94's ticket closes only once all 34 esc4 units across every migrated faction carry
`fourth_plus` and the data-side assertion (mentioned in B94's remaining-work note) is added — likely
its own tooling-adjacent turn once B89 is far enough along to know the assertion's real shape.

## Standing reminders
- Turn-typing strict: data only. No pipeline code changes.
- Fix parsers/schema, never hand-edit output — this session runs the existing pipeline, it does not
  patch `units.json` by hand.
- Diff-guard before banking: any regenerated output is verified by key-level diff against the prior
  committed file before being accepted.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `pipeline_manifest.py --freshness-check` as the **last** command — after every other edit, including
  edits to the handoff itself (leave the handoff's own row in its Files table as "(this file)").
