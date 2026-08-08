# World Eaters — Build Scope

Scoping-only pass (S217). No committed file changed. All numbers below come from command output
against this session's own baseline open (34 gates, sources loaded via `--fetch --data-turn`,
122/122 assertions, all three repro checks byte-identical; `repo_check` red only on the
pre-existing B108 finding, unchanged). Dry-run transforms and parser runs were written only to
throwaway temp dirs; nothing under `units.json`, `unit_loadouts.json`, `detachments.json`, or any
parser was edited.

World Eaters is clean and small: 30 datasheets (between Grey Knights' 25 and Thousand Sons' 34),
zero engine gaps, two units needing ordinary manual loadout authoring — on the same order as
Emperor's Children (2 flagged) and Grey Knights (4 flagged) before it.

---

## 1. Roster size: 30, matches exactly, 28 Legends exclusions confirmed both ways

`Datasheets.csv` holds 58 rows for `faction_id == WE`; `MFM_World_Eaters_v1.1.txt` lists exactly
30 units. Checked both directions — every MFM unit has a datasheet, every datasheet-that-should-be
in-scope has an MFM entry. The dry-run `wahapedia_transform.py` pass independently confirms this:
**30 processed, 28 skipped as Legends/Forge World**, and the 28 it names match, unit for unit,
manual cross-reference against the MFM list done before running the transform at all.

The 28 excluded are Horus Heresy-era Forge World datasheets carried in Wahapedia's export but with
no current-edition points entry (Fellblade, Xiphon Interceptor, Sokar-pattern Stormbird, Kratos,
Typhon, Falchion, and 22 others in the same vein) — not a judgment call, a direct absence check
against the MFM text.

## 2. "Blood Legions" — an already-solved allied-Daemon pattern, not a new mechanism

Five of the 30 (Bloodcrushers, Bloodletters, Bloodthirster, Flesh Hounds, Skarbrand) sit under a
`BLOOD LEGIONS` sub-heading in the MFM — Khorne Daemons units usable in a World Eaters list. This
is not new: `mfm_points_parser.py`'s `ALLIED_GROUP_HEADERS` (B61) already recognises `BLOOD
LEGIONS` by name, alongside Death Guard's `PLAGUE LEGIONS`, Thousand Sons' `SCINTILLATING LEGIONS`,
and Emperor's Children's `LEGIONS OF EXCESS` — all four were wired at the same time, ahead of any
of these factions being built. Death Guard's own `units.json` entry already carries its five
Nurgle-Daemon equivalents (Great Unclean One, Plaguebearers, Plague Drones, Beasts of Nurgle,
Nurglings) as native Death Guard units, not references into the Chaos Daemons army — that's the
precedent World Eaters' five Blood Legions units will follow.

## 3. Leader/attachment mapping — confirmed from two independent sources, no conflict

The MFM lists five `LEADER` blocks:

| Leader | Can lead |
|---|---|
| Khârn The Betrayer | Khorne Berzerkers |
| Lord Invocatus | Eightbound, Exalted Eightbound, Khorne Berzerkers |
| Lord on Juggernaut | Eightbound, Exalted Eightbound, Khorne Berzerkers |
| Master of Executions | Khorne Berzerkers |
| Slaughterbound | Eightbound, Exalted Eightbound |

Cross-checked directly against `Datasheets_leader.csv` (the independent Wahapedia source, not
derived from the MFM text) — **exact match, zero discrepancies**. `mfm_points_parser.py`'s dry run
against the World Eaters MFM applied 5 leader-eligibility overrides, 0 support, matching this table
exactly.

Confirmed World Eaters is not part of `add_chapter_point_overrides.py`'s five-chapter Space Marines
list, and needs no `add_co_leader.py` role-word registration (that script's Captain/Chapter
Master/Lieutenant/Execrator families are Space-Marine-specific) — same conclusion as Grey Knights
and Emperor's Children, for the same reason: Heretic Astartes, not Space Marine-descended.

## 4. Build from v1.1 — ordinary points revision, two force-disposition changes, zero unique tags

Per D293, build from the newest MFM. Diffing v1_0 against v1.1 directly:

- Nearly every unit's points dropped modestly (standard-shaped ▼ deltas throughout); Defiler is the
  one exception, moving up (270→270 base unchanged, but 2nd+ unit 300→310, and both wargear options
  10→15 pts each) — the same Defiler wargear increase already banked for the four sibling factions
  in D309/D310. World Eaters' own Defiler entries were confirmed to surface in the parser's raw MFM
  read during that session but stay correctly out of scope until this faction is actually built.
- **Two force-disposition changes**, both carrying v1.1's own `UPDATED / FORCE DISPOSITION(S)
  CHANGED` banner: Brazen Engines (Purge the Foe → Disruption), Butchers of Khorne (Disruption →
  Take and Hold).
- **Two unique tags removed**, both carrying `UNIQUE TAG REMOVED`: Brazen Engines and Goretrack
  Onslaught previously shared a `UNIQUE: ONSLAUGHT` tag (only one of the two could be taken in the
  same list); v1.1 removes it from both. **Zero unique tags remain** in v1.1 — confirmed by direct
  text search, not assumed.
- One enhancement re-price: Archslaughterer (Vessels of Wrath) 40 → 30 pts.
- Two `LEADER:` enhancement-eligibility notes (Cult of Blood's Butcher Lord →
  Goremongers/Jakhals; Khorne Daemonkin's Icon of War → Bloodcrushers/Flesh Hounds) — present in
  both versions, list order swapped only, no semantic change.
- No DP changes, no detachments added or removed (8 in both versions, same names).

Building from v1.1 lands both force-disposition corrections and both tag removals correct on first
build, same payoff already banked for the four other v1.1 Heretic Astartes builds.

**Known, pre-existing gap — not new to World Eaters.** Those two `LEADER:` enhancement-eligibility
notes are currently discarded as parser noise (`detachment_parser.py`'s `MFM_BLOCK_NOISE`) —
nothing enforces that Butcher Lord can only go on a leader attached to Goremongers or Jakhals. This
is not a World Eaters-specific finding: Chaos Space Marines carries 2 of the same shape, Thousand
Sons and Emperor's Children 1 each, both already shipped without enforcement. Logged as **B113**
below rather than treated as a World Eaters blocker.

## 5. Points and structure coverage: complete, no collisions

Dry run of `mfm_points_parser.py` against `MFM_World_Eaters_v1.1.txt` with the dry-run
`Unit_Stats.csv`:

- 30 unit point rows parsed, all 30 matching datasheets
- 0 datasheets with no MFM points, 0 unparsable costs, 0 composition-bracket collisions, 0 dropped
  attach-list entries
- 5 Leader-eligibility overrides applied, 0 Support — matches Section 3 exactly
- Wargear pricing: 3 priced items (Defiler's Hades lascannon and Heavy reaper autocannon at 15 pts
  each, Forgefiend's Ectoplasma cannon at 5 pts) — all three already exist in the committed
  `wargear_points.json` from the four sibling Defiler/Forgefiend factions; nothing new to price at
  the wargear-points level.

## 6. End-to-end dry run: clean

`wahapedia_transform.py` → `mfm_points_parser.py` → `convert_to_json.py` ran with no errors: 30
stat rows, 127 weapon rows, 49 auto-built wargear-option rows, 18 keywords, 10 rules, 54 abilities,
4 weapon abilities. Two faction-level (army-level, not per-unit) abilities correctly identified:
**Blessings of Khorne** and **Pact of Blood**.

## 7. Loadouts: two units flagged, both bounded, one genuinely new shape and one already-solved

`loadout_parser.py --factions WE`, run against a merged `units.json` (committed 18 armies + this
session's World Eaters dry-run output), parsed all 30 units and flagged exactly **2**:

- **Jakhals** (`000002628`) — `COMP_PARSE_FAIL`. The composition source is a genuine two-option
  block joined by a bare `or:` line (`1 Pack Leader, 1 Dishonoured, 8 Jakhals` **or**
  `1 Pack Leader, 2 Dishonoured, 17 Jakhals`), tied to the unit's two size brackets (10/20 models).
  Checked: no other faction's composition data uses this `or:` shape — `grep` across the full
  `Datasheets_unit_composition.csv` finds exactly one instance, this one. This is genuinely new,
  but it's bounded to one unit's composition table and the parser flags it cleanly rather than
  mis-parsing silently — ordinary manual authoring, not an engine gap. If a third size bracket
  ever appears with the same shape elsewhere, that's the point to consider a parser extension; one
  instance doesn't justify one.
- **Helbrute** (`000002632`) — `UNMATCHED`: "For each Helbrute fist this model is equipped with,
  it can be equipped with one of the following: 1 combi-bolter / 1 heavy flamer." Checked: this
  exact sentence (word for word, `datasheet_id`s `000000954`, `000001021`, `000001046`) already
  exists on Death Guard's, Chaos Space Marines', and Thousand Sons' own Helbrutes, all three
  already shipped in `unit_loadouts.json`. **Already-solved shape** — copy the existing pattern,
  no new authoring logic needed.

The transform's own validation report separately flagged 5 ambiguous weapon-name matches (plasma
pistol standard/supercharge, missile launcher frag/krak ×2, great axe of Khorne strike/sweep) and 2
compound two-part replacements (Jakhals' mangler swap, Forgefiend's jaws swap) — both resolved
cleanly by `loadout_parser.py`'s existing matching (neither surfaces in the final 2-unit flagged
list above), the same pattern Emperor's Children's scoping found: transform-level flags often
resolve automatically once the real parser runs.

**No engine work is needed for World Eaters.**

## 8. A finding unrelated to World Eaters, logged separately

A v1.1 Chaos Daemons MFM file (`MFM_Chaos Daemons_v1.1.txt`) now exists in the private source repo
— it did not at S214 when **B112** was opened and blocked on exactly this. Not resolved this
session (would mix Chaos Daemons data into a World Eaters scoping turn); flagged so B112 can be
picked up as its own data turn whenever convenient.

## 9. Suggested sequencing

1. **Data turn — World Eaters units.** Register `WE` in `units_repro_check.py` and
   `merge_factions.py` (mirrors the GK/TS/EC block pattern exactly). Build `units.json` from
   `MFM_World_Eaters_v1.1.txt` and the Wahapedia CSVs. Author the two flagged units: Jakhals'
   two-option composition (new, bounded), Helbrute (copy the already-shipped DG/CSM/TS pattern).
   No `World_Eaters_web.txt` exists in the private repo (checked directly against the repo
   listing, not the mount) — same as Emperor's Children, no composition file needed beyond the
   dry run already run clean.
2. **Data turn — World Eaters detachments.** Register `WE` in `detachment_parser.py`'s three maps,
   build from v1.1, verify both force-disposition changes and both tag removals land correctly.
3. **Small ticket (any time, XS)** — B113, the `LEADER:` enhancement-eligibility enforcement gap
   (4 instances across CSM ×2, TS ×1, EC ×1; World Eaters would add 2 more). Not a World Eaters
   blocker; a cross-faction gap worth its own turn once convenient.

Per project convention, steps 1 and 2 stay separate turns (units.json and detachments.json
migrations never share a turn) — the same discipline kept throughout Grey Knights, Thousand Sons,
and Emperor's Children.
