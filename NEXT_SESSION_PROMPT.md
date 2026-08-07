# NEXT SESSION PROMPT — Session 209

## Recommended turn type: scoping-only (Emperor's Children)

Read `SESSION_HANDOFF_208.md` first, then this prompt. S208 shipped B106-DATA — both Grey Knights
Dreadknights' ranged-weapon options are authored, `unit_loadouts.json` and `wargear_points.json`
regenerated and diff-guarded, new `B106-DATA` structural assertion added. **Grey Knights is fully
complete: 25/25 units, zero residual `_parser_flags`.** B100 closed.

## Corrected faction-priority finding — read before picking work

S206 and S207's prompts both said "move to the next Adeptus Astartes faction" after Grey Knights.
That phrasing was stale. S208 checked `units.json` directly rather than trusting it: **all twelve
Adeptus Astartes chapters in the standing priority order are already built** — Black Templars, Dark
Angels, Blood Angels, Deathwatch, Grey Knights, Imperial Fists, Iron Hands, Raven Guard, Salamanders,
Space Wolves, Ultramarines, White Scars, plus the generic Adeptus Astartes pool. Grey Knights was in
fact the last one open, not mid-list — consistent with D293 (S200), which already described Grey
Knights joining "sixteen pre-existing armies."

Of the Heretic Astartes tier: Chaos Space Marines, Thousand Sons, and Death Guard are built.
**Emperor's Children and World Eaters are not.** Chaos Daemons is already built (shipped out of the
tier's nominal order in an earlier session — not a gap, already done). Drukhari is not started.

**Emperor's Children is the correct next faction to build**, per the standing priority order
(Heretic Astartes precedes Chaos Daemons/Drukhari, and within Heretic Astartes, Emperor's Children
precedes World Eaters).

## Primary task: scope Emperor's Children

No `EMPEROR'S_CHILDREN_BUILD_SCOPE.md` exists yet. Follow the CSM/Thousand Sons/Grey Knights
precedent (`CSM_BUILD_SCOPE.md`, `THOUSAND_SONS_BUILD_SCOPE.md`, `GREY_KNIGHTS_BUILD_SCOPE.md`) —
scoping is data-gathering and analysis, not a build. Recommended checks, all against source directly,
not assumed from any prior document:

- Current-edition datasheet count from `MFM_Emperors_Children_v1.1.txt` (build from newest per D293),
  cross-checked against `Datasheets.csv`'s Emperor's Children rows — confirm the LEGENDS exclusions
  the same way Grey Knights' were confirmed (against the MFM's own header, not Wahapedia's
  classification).
- Full pipeline dry run (transform → points → convert) for a clean read: unpriced datasheets,
  unparsable costs, bracket collisions, dropped attach-list entries — same checklist Grey Knights used.
- Loadout complexity census: how many units need loadouts authored, and whether any sentence shapes
  are genuinely new (unlikely at this point in the project, but check rather than assume — Emperor's
  Children has some Noise Marine-specific wargear that may not match existing classifiers).
- Detachment count, enhancement count, unique tags, and whether v1_0 vs v1.1 differ materially
  (same check Grey Knights ran).
- Confirm nothing in `add_chapter_point_overrides.py`'s `CHAPTERS` list or any other chapter-override
  chain affects Emperor's Children (Grey Knights needed no such check to pass; Emperor's Children,
  being Heretic Astartes rather than Space Marine-descended, almost certainly doesn't either, but
  confirm rather than assume).

Output: a new `EMPEROR'S_CHILDREN_BUILD_SCOPE.md`, plus a decision log entry recording the findings
and the recommended build sequencing (units half / loadouts half / detachments half, same split
pattern as every prior faction). No committed data, parser, or engine file should change this
session — scoping-only, per the CSM/TS/GK precedent.

## Also open: B109 (small, unscoped)

Ryan's change request from S208: on the "My Army Lists" page, replace the "Target ####" label with
"#### Points". Not yet scoped against `index.html` — find the render site before touching anything.
This is UI-copy-only, XS, no rules content. Could be picked up as a quick engine-only turn either
before or after the Emperor's Children scoping pass, at your discretion — it doesn't block or get
blocked by anything else currently open.

## Standing reminders

- `./baseline.sh --fetch` at open (scoping turns don't need `--data-turn`, but sources are already
  loaded from S208 and should still pass the sources_loaded check either way).
- All 34 gates should be green at S208 close except `repo_check` (B108, Ryan action) — confirm before
  starting new work.
- Re-derive from source, don't trust prior-session prose — this prompt's own faction-priority
  correction is itself a case in point.
- Turn typing: scoping is its own type. Do not mix in unrelated engine, parser, or data changes.

## Close

Produce the four documents, register `SESSION_HANDOFF_209.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
