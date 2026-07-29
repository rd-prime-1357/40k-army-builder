# Session Handoff 157

## Baseline at open

Read `SESSION_HANDOFF_156.md` and `NEXT_SESSION_PROMPT.md` (S157 header) as instructed. Memory's
picture of this project (S126, index.html v6.3, E1 backlog) was badly stale — confirmed the real
state from the handoff chain and a live clone of the public repo per standing practice: S157,
decision log through D239, 23/23 gates, 107/107 assertions.

`40K_Decision_Log_v3_0.md` and most guarded files were absent from the mounted project area again
this session — expected under the documented 96%-capacity pruning, confirmed (not re-flagged) via
direct repo clone. Assembled the working tree from the repo (scripts, committed data, all guarded
files) plus the GW source files the mount holds and the repo correctly doesn't (MFM files, Wahapedia
CSVs, web composition files). Diffed every file this session would touch between mount and repo
before starting: all matched.

Ran `repro_check.py` and `units_repro_check.py` directly before any change: both byte-identical
against committed output. `baseline.sh --no-repo`: 20/20 gates green (tier-B repro checks skip in
this sandbox with no live-fetched sources; both direct repro runs above cover that gap).

## What shipped — D240, CSM cult-troop cross-file points, roster closed 58/58

**The fix.** Khorne Berzerkers, Plague Marines, Rubric Marines, and Noise Marines carry no cost in
CSM's own MFM; each priced once, in its own god-legion's MFM (World Eaters, Death Guard, Thousand
Sons, Emperor's Children). `units_repro_check.py`'s CSM build: the S147-turn-A stats-exclusion is
gone (Unit_Stats.csv is no longer filtered before the base points run); after the base 54-unit run,
each of the four gets its own `mfm_points_parser.py --army "Chaos Space Marines" --scope-to-army
--append` call against its own legion's MFM.

**The relabel wrinkle CSM_BUILD_SCOPE.md §4 flagged, resolved.** `--scope-to-army` already produces
the right Army Name on the output row (the transform's own Unit_Stats.csv already labels these four
`Chaos Space Marines`, since their datasheets are CSM's own) — no manual relabeling code was needed.
What *was* needed: scoping each append call's `--stats` input to a single row. Checked directly:
several of CSM's other 54 already-priced units — Chaos Rhino, Helbrute, Defiler, Chaos Predator
Annihilator/Destructor, Chaos Land Raider, Chaos Spawn, Maulerfiend, Heldrake, Forgefiend, Chaos
Vindicator, Sorcerer, Sorcerer in Terminator Armour — are *also* priced, separately, in one or more
of these same four legion MFMs. Passing the full CSM stats block to any of the four append calls
would have let those names resolve in scope and be silently overridden by append mode's
same-key-wins rule the moment a call ran against a file that also prices them (three of the four
do). New `_scope_stats_csv()` in `units_repro_check.py` writes a single-row stats file (keyed by
Datasheet ID) before each call, making that override unreachable. Verified empirically: each of the
four calls added exactly one row — confirmed from each parser run's own report, not assumed.

**Checked source directly, not just derived output.** Grepped all five relevant MFM files for the
four units' names and every wargear item on their loadouts (Icon of Khorne, Khornate eviscerator,
Blastmaster, Soulreaper cannon, etc.): none carry a separate WARGEAR OPTIONS price. `wargear_points.json`
correctly gained zero new entries — a confirmed source fact, not an absence-of-evidence guess.

**Regenerated in sequence, fixed point checked at each step:**
- `units.json`: +4 units (`000003582` Khorne Berzerkers, `000003583` Rubric Marines, `000003584`
  Plague Marines, `000004099` Noise Marines). 324 → 328 total. Diff-traced key-by-key: 0 changed,
  0 removed anywhere else.
- `unit_loadouts.json`: +4 entries, additive only, re-derived from the updated `units.json` through
  the standing `repro_check.py` mechanism (no hand edit).
- `rules_assertions.py`: `CSM-1` moved from the 54/58-gap pin to a clean 58/58 pass; `E14-2`'s
  literal updated 64/44 → 65/45 (Khorne Berzerkers' Icon of Khorne is the only one of the four
  units' options that qualifies as a free, unpriced, ungated single add).
- `pipeline_manifest.py --write` reissued three times (post-regeneration, post-assertion-literal
  update, post-decision-log/backlog/scope-doc update) — 108 guarded files, clean each time.

**Full baseline:** 20/20 gates green (`--no-repo`). `rules_assertions.py`: 70/70 (37 tier-B
skipped). `repro_check.py` and `units_repro_check.py` run directly: both byte-identical.
`index.html` untouched — data-only turn, matching the S157 prompt's scope. This closes
`CSM_BUILD_SCOPE.md` §4 in full — the CSM build is complete except for M2 (Ryan, GW source
eviction, no Claude action, already unblocked since D237).

## Decisions needed

None. The relabel mechanism and the single-row scoping requirement were both re-derived from source
and verified empirically this session, not product or legality judgment calls.

## Net New Files

None. `units.json`, `unit_loadouts.json`, `rules_assertions.py`, `units_repro_check.py`,
`CSM_BUILD_SCOPE.md`, `40K_Decision_Log_v3_0.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
`pipeline_manifest.json`, and `NEXT_SESSION_PROMPT.md` are all updates to existing files.

## Files (SHA-256, first 12 chars)

- `units.json` — `54118e7dbfb2`
- `unit_loadouts.json` — `9bd1c219d366`
- `rules_assertions.py` — `767c4688fb5f`
- `units_repro_check.py` — `c7a75e459b7d`
- `CSM_BUILD_SCOPE.md` — `53c4828c1853`
- `40K_Decision_Log_v3_0.md` — `1677e1565812`
- `DECISION_INDEX.md` — `a3aa7936993d`
- `OPEN_ITEMS_BACKLOG.md` — `2955f7f7423d`
- `pipeline_manifest.py` — `17a85b8ebb79`
- `pipeline_manifest.json` — `1b950d5f29e3`
- `NEXT_SESSION_PROMPT.md` — `3978dfd63b14`
