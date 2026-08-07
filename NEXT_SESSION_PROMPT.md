# NEXT SESSION PROMPT — Session 210

## Recommended turn type: data-only (Emperor's Children units)

Read `SESSION_HANDOFF_209.md` first, then this prompt. S209 scoped Emperor's Children
(`EMPEROR'S_CHILDREN_BUILD_SCOPE.md`, D303) — no committed file changed. Findings: 23 datasheets,
zero LEGENDS exclusions, **zero engine gaps** (a first — Grey Knights needed the B106 engine fix
first; Emperor's Children needs none). Only 2 units flagged for loadout authoring, both the same
already-solved free-item shape.

## Primary task: build Emperor's Children units

Follow the Grey Knights/Thousand Sons precedent, per `EMPEROR'S_CHILDREN_BUILD_SCOPE.md` §9:

1. Register `EC` in `units_repro_check.py`'s faction list (mirroring the existing block pattern).
2. Build `units.json` from `MFM_Emperors_Children_v1.1.txt` and the Wahapedia CSVs (23 units,
   `--emit-fourth-plus`). Diff-guard: expect exactly 23 units added, 0 elsewhere.
3. Author the two flagged units' loadouts — Tormentors (`000004079`) and Infractors (`000004080`),
   both need the free "icon of excess" equip-only item added via the existing `add` + `equipment` +
   `max_total` shape (no new schema).
4. Author the six manually-built option groups and two compound replacements the scope doc's §6
   lists (Lord Kakophonist, Noise Marines x2, Maulerfiend, Chaos Rhino, Defiler x2), plus one new
   `bundled_swaps.json` entry for Chaos Terminators' combi-bolter+accursed-weapon -> paired accursed
   weapons swap. Five ambiguous weapon-name matches (plasma pistol/gun variants, heavy missile
   launcher krak/frag) need a manual pick during authoring -- check the unit's actual wargear list
   against source before picking, don't assume the standard variant by default.
5. Confirm whether an `Emperors_Children_web.txt` composition pass is needed for the final
   `equipped_parser.py` gap-fill, or whether (as the scope doc's dry run suggests) the
   `--datasheets Datasheets.csv` pass alone covers it -- check directly, per the Grey Knights
   precedent, rather than assuming from the scoping session's dry run.
6. Regenerate `wargear_points.json` via the canonical `FACTION_BY_MFM` insertion-order file list --
   not naive alphabetical (see D236's documented trap). Expect 2 priced items, both Defiler-specific
   (Heavy reaper autocannon 15 pts, Hades lascannon 15 pts, both from v1.1 -- confirm the +5 pt
   increase over v1_0 lands correctly).
7. New structural assertion for the EC build, re-derived from source per the `B101-DATA`/`B106-DATA`
   pattern.

Do not touch detachments this session -- that's its own data turn next (scope doc S9 step 2).

## Also open, at your discretion

- **B109** (XS, engine-only) -- `index.html`'s `renderMyLists()`, one-line label change
  (`'target ' + r.points_target` -> `r.points_target + ' Points'`). Confirmed location, not yet
  changed. Could ride as a standalone engine-only turn before or after the units build -- doesn't
  block or get blocked by anything else open.
- **B110** (XS, data-only) -- `faction_taxonomy.json`'s stale Grey Knights `built: false` flag. Could
  ride with this session's units data turn, or its own tiny turn -- your call, but if folded in, keep
  it as an explicit second diff-guarded change, not silently mixed into the EC units diff.

## Standing reminders

- `./baseline.sh --fetch --data-turn` at open -- this is a data turn, sources must load or the gate
  fails by design.
- All 33 gates should be green at S209 close except `repo_check` (B108, Ryan action) -- confirm
  before starting new work.
- Re-derive from source, don't trust prior-session prose.
- Turn typing: this is data-only. Do not touch `index.html` or any engine logic this session even if
  B109 looks tempting to fold in -- register it as its own turn instead if you don't take it now.

## Close

Produce the four documents, register `SESSION_HANDOFF_210.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
