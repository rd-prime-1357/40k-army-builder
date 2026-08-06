# NEXT SESSION PROMPT — Session 197

## Turn type: data-only, unless the open question below forces a scope split. No exceptions otherwise.

Read `SESSION_HANDOFF_196.md` first, then this prompt. Session 196 shipped Death Guard as B89's
**second** per-faction migration (and, riding along, B94's second `fourth_plus` faction — Chaos Rhino).
This session is B89's **third** migration, but the candidate needs a mechanism check before committing
to it — read the open question below before starting the build.

## Session open
1. Baseline: `./baseline.sh --fetch --data-turn`.
2. Verify S196's hashes via `pipeline_manifest.json` (the authoritative source), not by hand-copying
   the handoff table.
3. Confirm Ryan has pushed S196's changes.

## Open question to resolve before picking today's faction

The remaining migration candidates among the 10 currently-built factions are: Space Marines (base),
Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves, Chaos Space Marines, Chaos Daemons.
None of these are as simple as Thousand Sons or Death Guard, for two different reasons — check both
before choosing:

1. **Chaos Daemons (9 adopt-mechanically, 1 investigate-first per `MFM_v1_1_Reconciliation.md` — the
   smallest remaining scope)** is Gen-1 hand-built data. Its points live in the root `Unit_Points.csv`
   and never pass through `mfm_points_parser.py` — `units_repro_check.py`'s CD block calls
   `convert_to_json.py` directly against the project root's own CSVs, no MFM file involved at all
   (D132). Migrating CD to v1.1 therefore cannot be "swap the source file, rerun the parser" like
   Thousand Sons/Death Guard — it would mean hand-editing `Unit_Points.csv`'s 9 changed values
   directly. Whether that is the correct, precedented mechanism for this specific Gen-1 file (it is
   already treated as hand-authored source, not generated output) or whether it needs a small new
   parser first is a scope/mechanism call — investigate how CD's root CSVs have been touched in past
   sessions (search the decision log for CD data edits, e.g. D216) before deciding, and record the
   decision either way.

2. **Space Marines base + its 5 chapter files (Black Templars, Blood Angels, Dark Angels, Deathwatch,
   Space Wolves)** are the largest remaining scope (30 + 22/19/29/19/26 adopt-mechanically) and are
   chained: the five chapter files apply via `--scope-to-army --append` on top of the base SM build
   (B56a). Confirm whether a single chapter can migrate to v1.1 while base SM stays on `_v1_0.txt`, or
   whether the chapter v1.1 files assume a v1.1 base — check `MFM_Black_Templars_v1.1.txt` (or another
   chapter) against its `_v1_0.txt` for any change that only makes sense against an already-migrated
   base, before assuming they're independent.

Chaos Space Marines is not a candidate yet — its cult-troop cross-legion pricing needs World Eaters and
Emperor's Children built first (neither is), and CSM's own migration is explicitly deferred to "CSM's
own B89 turn" per `units_repro_check.py`'s existing comments.

**Recommendation (mine to make, not a call for Ryan): investigate Chaos Daemons first.** Smallest
scope, and the mechanism question is answerable from the decision log rather than guesswork. If CD's
hand-edit path turns out to be genuinely precedented and safe, do that migration this session, diff-
guarded the same way as every other data turn. If it is not resolvable cleanly within the session's
data-only turn typing (e.g., it turns out to need a new parser, which would be a tooling turn), stop
after the investigation, bank nothing risky, and hand the mechanism decision to the next tooling
session instead — a banked investigation beats a partial or wrong CD edit.

## If Chaos Daemons is deemed migratable this session

**Steps, mirroring S195/S196's diff-and-verify discipline:**
1. Hash-verify `MFM_Chaos Daemons_v1.1.txt` (note the space vs underscore in the committed filename per
   `source_manifest.json`) and whatever CD's actual "before" reference is — check `source_manifest.json`'s
   CD entries before assuming a `_v1_0.txt` equivalent exists.
2. Diff the two Chaos Daemons text files directly to confirm the 9 points changes and 1
   investigate-first item independently, the way S196 did for Death Guard's raw source (the
   reconciliation report's Death Guard wargear note turned out to be wrong — verify CD's report entries
   against the raw source rather than trusting them blind).
3. Confirm all 15 other armies are untouched by whatever CD update mechanism is used.
4. Check `rules_assertions.py` for any pinned Chaos Daemons points values needing reconciliation.
5. Record the mechanism decision (hand-edit vs. new tooling) explicitly in the decision log regardless
   of outcome — this is the kind of call that should not go unrecorded even if CD turns out simple.

## Standing reminders
- Turn-typing strict: data only, unless the mechanism investigation above concludes CD genuinely needs
  new parsing tooling — in that case, stop and hand off rather than mixing a tooling change into this
  data-only session.
- Fix parsers/schema, never hand-edit output — this is exactly the question CD raises; resolve whether
  its root CSVs count as source or output before touching them.
- Diff-guard before banking: any regenerated or hand-edited output is verified by key-level diff against
  the prior committed file before being accepted.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `pipeline_manifest.py --freshness-check` as the **last** command — after every other edit, including
  edits to the handoff itself (leave the handoff's own row in its Files table as "(this file)").
