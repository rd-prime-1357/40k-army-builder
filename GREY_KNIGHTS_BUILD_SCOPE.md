# Grey Knights — Build Scope

Scoping-only pass (S200, D293). No committed file changed. All numbers below come from command
output against this session's own baseline open (32 gates, 118/118 assertions; `repo_check` red on
exactly the seven files S199 produced and predicted, nothing else). Dry-run transforms and parser
runs were written only to throwaway temp dirs.

Grey Knights is the **smallest faction build the project has done** — 25 current-edition datasheets,
against 58 for Chaos Space Marines and 34 for Thousand Sons. It is fully self-sourced, has no
chapter/sub-faction split, no allied-codex problem, and no cross-file points sourcing. The pipeline
runs it end to end today with no code changes. The real work is four units' loadouts and one engine
gap that Grey Knights makes unavoidable but did not create.

---

## 1. Real roster size: 25, not 31

`Datasheets.csv` holds 31 rows for `faction_id == GK`. Six are excluded by the transform's existing
Legends/Forge-World filter, leaving **25**, which is the correct current-edition count. The dry run
(`wahapedia_transform.py --faction GK --army-name "Grey Knights"`) selected exactly 25 and produced
25 stat rows, 140 weapon rows and 50 auto-built wargear-option rows.

The six exclusions, and why each is right:

| unit | Wahapedia source | in MFM? |
|------|------------------|---------|
| Kaldor Draigo | Grey Knights (Warhammer Legends) | under the MFM's own `LEGENDS` header |
| Brother-Captain Stern | Grey Knights (Warhammer Legends) | under the MFM's own `LEGENDS` header |
| Grey Knights Dreadnought | Grey Knights (Warhammer Legends) | under the MFM's own `LEGENDS` header |
| Grey Knights Relic Razorback | Grey Knights (Warhammer Legends) | under the MFM's own `LEGENDS` header |
| Servitors | Grey Knights (Warhammer Legends) | under the MFM's own `LEGENDS` header |
| Grey Knights Thunderhawk Gunship | Grey Knights (Forge World) | **inline in the main priced list** |

This is worth stating plainly because Draigo is a headline Grey Knights character and his absence
will look like a bug to anyone who doesn't check. It isn't: `MFM_Grey_Knights_v1.1.txt` carries an
explicit `LEGENDS` section header at line 279, and Draigo, Stern, the Dreadnought, the Relic
Razorback and Servitors all sit beneath it. Wahapedia's classification and GW's agree. Excluding
them from a Matched Play builder is correct.

**The Thunderhawk is a different case and should be recorded as a known gap, not a decision.** GW
prices it inline in the main list (805 pts first unit / 855 pts second+), not under `LEGENDS`, so GW
treats it as Matched Play legal. Wahapedia has no current-edition datasheet for it — the Grey Knights
(Forge World) source is edition `0`, so there is no stat line, no weapon profile and no options data
to build from. The unit is therefore unbuildable from our sources, not deliberately excluded on a
rules judgement. This is not Grey Knights-specific: every Forge World source in the export except
Adeptus Titanicus is edition `0`, so the same silent gap already exists for every built faction. It
does not block the Grey Knights build. It is worth a backlog note so nobody re-derives it later.

Roles across the 25: 9 Vehicle, 8 Character, 4 Infantry, 2 Epic Hero, 2 Battleline. Ten `LEADER`
blocks in the MFM; the points parser applied 8 attach-eligibility overrides (8 Leader, 0 Support).

## 2. Build from v1.1, both units and detachments

Per D293 this session: **always build from the newest MFM available**, for units and detachments
alike. Grey Knights is the first faction where this is stated as a rule rather than decided per
migration, and the first whose `detachments.json` records will be current while the other sixteen
armies' remain at v1_0.

For units there is a second, independent reason to prefer v1.1 that is specific to Grey Knights, and
it retires an open concern:

**The B94 copy-tier problem is gone in v1.1.** S194 recorded that Grey Knights' Brotherhood Terminator
Squad was mis-parsed by the same `YOUR 1ST TO 3RD UNITS COST` / `YOUR 4TH + UNIT COSTS` shape that
caused the shipped Rubric Marines overcharge, and noted it was never fixed because Grey Knights was
not a built army. That shape is present in `MFM_Grey_Knights_v1_0.txt` (lines 29–38). In v1.1 it is
gone: the source carries an explicit `REQUISITION THRESHOLDS REMOVED` note and the unit is now a
plain composition-bracket unit (4/175, 5/175, 8/300, 10/360). Building from v1.1 sidesteps the whole
question rather than relying on B87's `esc4` reader to handle it. Two Grey Knights units still emit a
`fourth_plus` tier under `--emit-fourth-plus`; both parse cleanly.

`mfm_points_parser.py`'s `FACTION_BY_MFM` already maps both filenames to `GK` (added ahead of time
under B87/D275), so nothing needs wiring there.

## 3. Points coverage is complete — no cross-file sourcing, no collisions

Running `mfm_points_parser.py` against the v1.1 file with the dry run's `Unit_Stats.csv`:

- 31 unit point rows parsed, 25 matching datasheets
- **0 datasheets with no MFM points** — every one of the 25 is priced
- 0 MFM entries with an unparsable cost
- 0 composition-bracket collisions (B56b)
- 0 dropped attach-list entries — the B73/D260 guard fired zero times
- 0 escort model groups, 0 escort rate conflicts
- 6 MFM entries with no matching datasheet: exactly the five Legends units plus the Thunderhawk

That last line is the reassuring one. The orphans are precisely the units §1 explains, and
`convert_to_json.py` drops them: the final `units.json` holds 25 units in one army.

Wargear pricing is trivial by comparison with other factions — six `WARGEAR OPTIONS` blocks, three
distinct priced items (Psycannon 5 pts, Heavy psycannon 15 pts, Sublimator 15 pts).

Grey Knights needs **no cross-file points append**. Unlike Chaos Space Marines (whose four cult-troop
units are priced in their god-legions' own MFMs) and unlike the six-file Space Marines group (whose
chapter overrides are derived by comparison against the generic base price), Grey Knights is
self-contained. It mirrors the Death Guard and Thousand Sons blocks in `units_repro_check.py`
exactly, and it is **not** part of the `add_chapter_point_overrides.py` chain — that script's
`CHAPTERS` list holds only the five named Space Marines chapters, so the version-mismatch hazard D291
identified does not apply here.

## 4. End-to-end dry run: clean

`wahapedia_transform.py` → `mfm_points_parser.py` → `convert_to_json.py --emit-fourth-plus` ran with
no errors and produced `units.json` (1 army, 25 units), plus 18 keywords, 6 rules, 34 abilities and
3 weapon abilities. One faction-level ability was correctly identified for army-level placement
rather than per-unit: **Gate of Infinity**.

## 5. Loadouts: four units need authoring, in two shapes

`loadout_parser.py --factions GK` parsed all 25 units, skipped none, and flagged **4**. That is a
very low flag rate — Chaos Space Marines and the Space Marines family both needed substantially more
hand work. The four split into two shapes:

**Shape A — compound "weapon and banner" replacements plus a non-weapon upgrade (2 units).**
Brotherhood Terminator Squad and Paladin Squad each offer four compound replacements of the form
"1 incinerator and 1 Ancient's banner", and each has an unmatched sentence granting one model an
Apothecary's narthecium in place of its storm bolter. Both squads also carry the footnote "That
model's storm bolter cannot be replaced." The banner and narthecium have no weapon profile, so the
parser reports `WEAPON_NOT_FOUND`. **This needs no new schema.** The existing `add` +
`equipment` + `max_total` shape already handles non-weapon upgrade items — Sanguinary Guard's
Sanguinary Banner and Tzaangors' Herd Banner/Brayhorn are shipped precedents, the latter pair even
using `requires_weapon` to bind two items together. The four compound rows are ordinary two-part
authoring of the kind the project has done repeatedly.

**Shape B — "up to two of the following, but cannot take duplicates" (2 units).** Nemesis Dreadknight
(3 choices) and Grand Master in Nemesis Dreadknight (4 choices). This is the one that needs a
decision before authoring, and it is covered in §6.

There is no `Grey_Knights_web.txt`. `repro_check.py` requires one file per entry in its `WEB_PASSES`
list, so adding Grey Knights there would demand one; Chaos Daemons is the precedent for a built
faction that appears in neither `WEB_PASSES` nor `FACTIONS`. The loadout run above produced complete
results for all 25 units without any web pass, so a web file is likely unnecessary — but the web
passes exist to supply *equipped* defaults, and whether the final `--datasheets` pass covers Grey
Knights adequately has not been demonstrated and should be checked in the build turn rather than
assumed. Flagging this as the one open pipeline question, not a finding.

## 6. The one real gap: "cannot take duplicates" is not enforced

Both Nemesis Dreadknights let a player equip up to two items from a list and forbid taking the same
item twice. The engine can express the cap but not the distinctness.

`loMaxCount` in `index.html` handles `max_total_all` with `up_to` by capping the *total* number of
picks across the group. Nothing anywhere in the engine enforces that the picks differ — searching for
duplicate/distinct logic turns up only detachment-selection code (E1b/E1c), which is unrelated.

**This is a pre-existing D0 gap, not one Grey Knights introduces.** Three shipped Chaos Space Marines
units already carry a no-duplicate rule that exists only as a literal string sitting inside the
choices array, where it renders as though it were a selectable option:

| army | unit | `up_to` | real choices |
|------|------|---------|--------------|
| Chaos Space Marines | Raptors | 2 | 3 |
| Chaos Space Marines | Legionaries | — | 9 |
| Chaos Space Marines | Traitor Guardsmen Squad | 3 | 5 |

So today an illegal duplicate selection is reachable in three shipped units, and the rule text is
being shown to the player as a fake menu entry. Under D0 the illegal state should be unreachable.
Grey Knights makes this unavoidable because both Dreadknights depend on it, and unlike the Chaos
Space Marines cases there is no sensible way to author around it.

Recommend opening this as its own engine ticket rather than folding it into the Grey Knights build:
it is an engine turn (a `distinct: true` flag on the option plus selection-side enforcement), it
fixes three already-shipped units, and mixing it into a data build turn would violate turn typing.
The Grey Knights build can proceed and author the two Dreadknights against the new flag once it
exists, or ship them capped-but-not-distinct with the gap recorded — my recommendation is to
sequence the engine ticket first, since Grey Knights is small enough that the wait costs little.

## 7. A second, smaller defect found: `detachment_parser.py --report` crashes

The parser builds gap records with keys `key`, `source_faction`, `detachment`, `dp`, but the report
writer reads `g["army"]`. Any run with `--report` that produces at least one gap dies with a
`KeyError` after the JSON has been written. It has never fired in a gate because
`detachments_repro_check.py` never passes `--report` — but a build or scoping session does, which is
how it surfaced here.

There are already **11 gaps across built factions** (Black Templars 2, Blood Angels 3, Space Wolves
2, Death Guard 2, Chaos Space Marines 2 — all 1DP detachments with no rule text in either source).
Grey Knights adds 3 more (Argent Assault, Fires of Purgation, Immaterial Interdiction). So the crash
is latent today and would fire the moment anyone runs the parser with a report. One-line fix, XS,
tooling turn.

## 8. Detachments: 9, and almost identical between versions

Running the real `detachment_parser.py` against both Grey Knights MFM files (via a throwaway copy
with Grey Knights added to `FACTION_FILES`, `MFM_SOURCE_NAME` and `ARMY_TO_WAHA_FACTION` — the three
places a new faction must be registered) produced 9 detachments from each, with identical keys.

The only differences are **three force-disposition changes**, matching the three
`FORCE DISPOSITION(S) CHANGED` banners in the v1.1 text exactly:

| detachment | v1_0 | v1.1 |
|------------|------|------|
| Argent Assault | Purge The Foe | Priority Assets |
| Immaterial Interdiction | Priority Assets | Reconnaissance |
| Warpbane Task Force | Purge The Foe | Take And Hold |

No DP changes, no enhancement re-prices, no detachments added or removed, no unique tags anywhere in
the faction. The nine are Argent Assault, Augurium Task Force, Banishers, Brotherhood Strike, Fires
of Purgation, Hallowed Conclave, Immaterial Interdiction, Sanctic Spearhead and Warpbane Task Force;
DP costs run 1–3; 28 enhancements total, four of them Upgrades.

Because D293 sets v1.1 as the rule, the three changed dispositions land correct on first build rather
than needing a later migration turn — which is the concrete payoff of the decision.

## 9. One data-currency caveat

Wahapedia's Grey Knights faction pack is version 1.0 with an errata date of 22 Oct 2025 — the oldest
current-edition pack among the priority factions (Chaos Space Marines is at 1.6 / May 2026, Space
Marines at 1.8 / May 2026). The MFM is the authority for points and detachments regardless, so this
does not affect legality or costing. It does mean the datasheet layer — abilities text, weapon
profiles, options wording — may lag any GW change made since October 2025. Worth knowing if
something in the built faction later looks stale.

## 10. Suggested sequencing

1. **Engine turn** — the `distinct` flag and its enforcement (§6). Fixes three shipped Chaos Space
   Marines units; unblocks both Grey Knights Dreadknights.
2. **Tooling turn** — the `--report` `KeyError` (§7). XS; can ride with any other tooling work.
3. **Data turn — Grey Knights units.** Register Grey Knights in `units_repro_check.py` mirroring the
   Thousand Sons block, build from `MFM_Grey_Knights_v1.1.txt`, author the four flagged units'
   loadouts, resolve the web-pass question in §5.
4. **Data turn — Grey Knights detachments.** Register Grey Knights in `detachment_parser.py`'s three
   maps, build from v1.1.

Steps 3 and 4 could plausibly be one turn given the size, but they touch different outputs and
different parsers, and the project's convention has kept `units.json` and `detachments.json`
migrations separate throughout the B89 arc. Keep them separate.
