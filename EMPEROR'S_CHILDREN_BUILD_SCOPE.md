# Emperor's Children — Build Scope

Scoping-only pass (S209). No committed file changed. All numbers below come from command output
against this session's own baseline open (33 gates, sources loaded via `--fetch --data-turn`,
121/121 assertions, both repro checks byte-identical; `repo_check` red only on the pre-existing
B108 finding, unchanged). Dry-run transforms and parser runs were written only to throwaway temp
dirs; nothing under `units.json`, `unit_loadouts.json`, `detachments.json` or any parser was edited.

Emperor's Children is the **smallest current-edition roster the project has built** — 23 datasheets,
against 25 for Grey Knights, 34 for Thousand Sons, 58 for Chaos Space Marines. It is clean end to
end: no LEGENDS exclusions, no engine gap, no new parser shape. The only real work is ordinary
per-unit loadout authoring, on a par with Grey Knights' four flagged units but smaller still — two.

---

## 1. Roster size: 23, and it matches exactly

`Datasheets.csv` holds exactly 23 rows for `faction_id == EC`, and `MFM_Emperors_Children_v1.1.txt`
lists exactly 23 units. Checked both directions — every MFM unit has a datasheet, every datasheet
has an MFM entry. **Zero LEGENDS exclusions**, unlike Grey Knights' six. Neither MFM file (v1_0 or
v1.1) carries a `LEGENDS` header at all.

The roster includes a "Legions of Excess" sub-block — Daemonettes, Fiends, Keeper of Secrets,
Seekers, Shalaxi Helbane (5 of the 23) — Chaos Daemons units usable within the Emperor's Children
list. This is not a new pattern: Thousand Sons has the identical shape under "Scintillating Legions"
and Death Guard under "Plague Legions," both already built and shipped. `mfm_points_parser.py`
already has both `MFM_Emperors_Children_v1_0.txt` and `MFM_Emperors_Children_v1.1.txt` pre-mapped to
`EC` in `FACTION_BY_MFM` — wired ahead of time, nothing to add.

Roles across the 23: 8 Other, 8 Characters, 5 Battleline (incl. the 2 Legions-of-Excess Battleline
units), 1 Dedicated Transport, 1 (Chaos Terminators, counted separately). Two `LEADER` blocks with
role-word attach lists (Lord Kakophonist → Chaos Terminators/Noise Marines; Sorcerer →
Infractors/Noise Marines/Tormentors), plus Lucius the Eternal and Lord Exultant with single-unit
attach lists. No co-leader pattern — `add_co_leader.py`'s role-word families (Captain/Chapter
Master/Lieutenant/Execrator) are Space-Marine-specific and don't apply here, consistent with Grey
Knights needing no such check.

## 2. One cross-faction wrinkle, already resolved, not a conflict

Chaos Space Marines' own "Noise Marines" cult-troop unit (datasheet `000004099`) is priced from
`MFM_Emperors_Children_v1_0.txt` per `units_repro_check.py`'s `CSM_CULT_TROOP_POINTS` — hardcoded
and already shipped. Emperor's Children's own Noise Marines is a **different datasheet ID**
(`000004088`) — Wahapedia carries two separate rows for the same unit name, one filed under each
faction. Checked both MFM versions price Noise Marines identically (145 pts for 1st–2nd units / 160
pts for 3rd+, in both v1_0 and v1.1), so building Emperor's Children from v1.1 creates no
version-mismatch or price-disagreement with CSM's already-shipped cross-reference. This is the same
class of cross-file sourcing Chaos Space Marines' four cult-troop units already exercise in the
opposite direction (D229/D240) — not new, just confirmed clean rather than assumed.

Confirmed Emperor's Children is **not** part of `add_chapter_point_overrides.py`'s `CHAPTERS` chain
(that list holds only the five Space Marines chapter files) — same conclusion as Grey Knights, for
the same reason: Heretic Astartes, not Space Marine-descended.

## 3. Build from v1.1 — one real points change, not a decision point

Per D293, build from the newest MFM. Comparing v1_0 and v1.1 directly:

- **Wargear pricing changed for Defiler's two options**: Heavy reaper autocannon and Hades lascannon
  each moved from 10 pts (v1_0) to 15 pts (v1.1) — v1.1 marks both with the `▲ (+5)` up-arrow
  annotation, consistent with a routine points increase, not a data problem. Building from v1.1
  picks up the correct current price automatically.
- No other unit or wargear price differs between versions.
- No composition-bracket shape differences (no `esc4`/copy-tier trap like Grey Knights' Brotherhood
  Terminator Squad — Emperor's Children has no unit using the `1ST TO Nth / (N+1)th+` bracket shape
  at all except Chaos Land Raider and Lord Exultant, both of which parse cleanly in both versions).

## 4. Points coverage: complete, no collisions

Dry run of `mfm_points_parser.py` against `MFM_Emperors_Children_v1.1.txt` with the dry-run
`Unit_Stats.csv`:

- 23 unit point rows parsed, all 23 matching datasheets
- **0 datasheets with no MFM points**
- 0 MFM entries with an unparsable cost
- 0 composition-bracket collisions
- 0 dropped attach-list entries
- 4 Leader-eligibility overrides applied from the MFM (4 Leader, 0 Support)
- Wargear pricing: exactly 2 priced items, both Defiler-specific (Heavy reaper autocannon 15 pts,
  Hades lascannon 15 pts). Everything else — including both flagged "icon of excess" items below —
  is a free (0-pt) wargear addition, the same shape as Grey Knights' free Ancient's banner.

## 5. End-to-end dry run: clean

`wahapedia_transform.py` → `mfm_points_parser.py` → `convert_to_json.py --emit-fourth-plus` ran with
no errors: 23 stat rows, 104 weapon rows, 31 auto-built wargear-option rows, 19 keywords, 11 rules,
43 abilities, 4 weapon abilities. Two faction-level (army-level, not per-unit) abilities correctly
identified: **Thrill Seekers** and **Pact of Excess**.

## 6. Loadouts: two units flagged, both the same known shape

`loadout_parser.py --factions EC`, run against a merged `units.json` (committed 17 armies + this
session's EC dry-run output), parsed all 23 units and flagged exactly **2**:

- **Tormentors** (`000004079`) — `UNMATCHED: 1 Tormentor can be equipped with 1 icon of excess.`
- **Infractors** (`000004080`) — the identical sentence, same item.

"Icon of excess" has no weapon profile and no MFM price — a free equip-only wargear item. This is
the exact shape already solved by Grey Knights' Ancient's banner and Sanguinary Guard's Sanguinary
Banner: the existing `add` + `equipment` + `max_total` schema handles it with no engine change.
**This needs no new schema and no engine ticket** — unlike Grey Knights, which needed the B106
distinct-addition engine fix before its two Dreadknights could be authored.

The transform's own validation report additionally flagged six items as "not auto-parsed, build
manually" and two as "compound replacements" — all recognized shapes with shipped precedent, not new
work:

- Compound two-part replacements (Lord Kakophonist's power sword → screamer pistol + close combat
  weapon; Noise Marines' Disharmonist sonic blaster → screamer pistol + power sword) — ordinary
  two-part authoring, same as Grey Knights' Brotherhood Terminator Squad/Paladin Squad banner swaps.
- A bundled two-weapon swap (Chaos Terminators: combi-bolter + accursed weapon → paired accursed
  weapons) — the same `bundled_swaps.json` shape already used for four other units (Captain,
  Bloodthirster, Lieutenant, Wulfen Dreadnought); needs one new entry, not new mechanism.
  "Up to 2 Noise Marines can each replace their sonic blaster with 1 blastmaster" is a plain
  per-model-count swap (single target item, no distinctness question) — not the B106 shape, ordinary
  authoring.
- Five ambiguous weapon-name matches (plasma pistol/plasma gun standard-vs-supercharge variants,
  heavy missile launcher krak-vs-frag) — routine manual disambiguation during authoring, the same
  kind of pick every prior faction has needed.
- One equip-only item with no weapon profile (Keeper of Secrets' "shining aegis") — same free-item
  shape as the two flagged units above.

**No engine work is needed for Emperor's Children.** This is the first faction since the project
started this arc where scoping surfaces zero engine tickets.

## 7. Detachments: 10, four force-disposition changes between versions, no unique tags

Comparing both MFM files directly (not yet run through `detachment_parser.py` against a registered
copy — that requires adding EC to `FACTION_FILES`/`MFM_SOURCE_NAME`/`ARMY_TO_WAHA_FACTION`, deferred
to the detachments build turn per the Grey Knights precedent):

10 detachments, DP costs 1–3, identical names and enhancement lists (same enhancements, same costs)
between v1_0 and v1.1. **Zero unique tags** in either version — confirmed by direct text search, not
assumed. Four force-disposition changes, all carrying the source's own `UPDATED / FORCE
DISPOSITION(S) CHANGED` banner in v1.1:

| detachment | v1_0 | v1.1 |
|------------|------|------|
| Carnival of Excess | Priority Assets | Disruption |
| Coterie of the Conceited | Purge the Foe | Priority Assets |
| Frenzied Host | Disruption | Reconnaissance |
| Spectacle of Slaughter | Purge the Foe | Disruption |

The other six (Court of the Phoenician, Elegant Brutes, Mercurial Host, Peerless Bladesmen, Rapid
Evisceration, Slaanesh's Chosen) are unchanged between versions. No DP changes, no enhancement
re-prices, no detachments added or removed. Building from v1.1 lands all four changed dispositions
correct on first build, same payoff D293 already banked for Grey Knights.

## 8. A finding unrelated to Emperor's Children, logged separately

`faction_taxonomy.json` still lists Grey Knights as `built: false` under the Imperium group, even
though `units.json` confirms 25/25 units and B100 closed at S208. Nobody flipped the taxonomy flag
when Grey Knights shipped. Not a blocker for anything, but worth a data fix before it causes a
false-negative in some future census. Logged as **B110** below rather than fixed this session — this
turn is scoping-only and taxonomy is a data file.

## 9. Suggested sequencing

1. **Data turn — Emperor's Children units.** Register `EC` in `units_repro_check.py` (mirroring the
   Grey Knights/Thousand Sons block pattern), build `units.json` from `MFM_Emperors_Children_v1.1.txt`
   and the Wahapedia CSVs, author the two flagged units' loadouts (Tormentors, Infractors — the
   "icon of excess" free-item pattern), plus the six manually-built option groups and one
   `bundled_swaps.json` entry (Chaos Terminators). No `Emperors_Children_web.txt` exists and none of
   the flagged units suggest one is needed — the loadout run above produced complete results without
   one, but per the Grey Knights precedent, confirm the final `--datasheets` pass covers Emperor's
   Children adequately during the build turn rather than assuming.
2. **Data turn — Emperor's Children detachments.** Register `EC` in `detachment_parser.py`'s three
   maps, build from v1.1, verify the four force-disposition changes land correctly.
3. **Small data fix (any time, XS)** — B110, `faction_taxonomy.json` Grey Knights `built` flag.

Steps 1 and 2 could be combined given the roster's size, but per project convention (kept separate
throughout Grey Knights, Thousand Sons, and every faction before them), keep `units.json` and
`detachments.json` migrations in separate turns.
