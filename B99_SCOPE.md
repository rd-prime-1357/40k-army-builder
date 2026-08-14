# B99 — Enhancement-conferred weapon modifications: scope

**Written S235 (D329), scoping-only turn.** Nothing built. Every number below was re-derived
this session from `detachments.json`, `units.json` and `index.html` directly; none of it is
carried forward from the original B99 backlog entry or from prior session prose.

---

## 1. What is actually wrong, and how big it is

The original report (Ryan, screenshot, pre-S194) was that Thousand Sons' *Eldritch Vortex of
E'Taph* — "Add 1 to the Strength and Damage characteristics of Psychic weapons equipped by the
bearer" — has no effect on the weapon stats the app displays. That is correct, and it is not a
one-off: **no enhancement of any kind reaches the weapon table.** There is no code path in
`index.html` between an assigned enhancement and a rendered weapon characteristic.

The affected population, censused across all 739 enhancement records in `detachments.json`
(665 of which carry a description; 74 are description-less and are a separate, pre-existing
text-coverage gap, not part of this):

| set | shape | records | distinct names | armies |
|-----|-------|--------:|---------------:|-------:|
| **A** | numeric change to the **bearer's own** weapons, **unconditional** | **57** | 32 | 13 |
| **A2** | weapon-**ability** grant to the bearer's own weapons, unconditional | **23** | 13 | 11 |
| B | bearer's own weapons, **conditional only** (no always-on part) | 5 | 5 | 4 |
| C | bearer's own **statline** (T/W/OC/Sv/Ld/M), unconditional | 10 | 6 | 8 |
| D | weapons of **other models** in the bearer's unit | 19 | 10 | 8 |

**Corrected at D330 (S236), superseding the figures above as first written.** The original
57 / 17 / 72 undercounted Set A2 by *Eye of the Primarch* (6 records): it targets "…equipped
by the bearer **and** Battleline models in the bearer's unit", word-for-word the same shape
as *Blades of Valour*, which this table's first draft put in Set A. Including one and
excluding the other was arbitrary; both are in Set A/A2 for their bearer half. The Set A
figure was unaffected — it was already correct at 57 / 32. The table above carries the
corrected 23 / 13 for Set A2; the union below carries the corrected total.

Sets A and A2 overlap on 2 records (*Cursed Fang*, *Furnace of Plagues*, which do both);
their union is **78 records / 43 names**. Chaos Daemons is the only built army with no
record in either set — its 29 enhancement records carry shorthand summaries rather than
rule text (B122) and cannot be curated from source. A further 11 records modify *an
incoming attack's* characteristics (the *Adamantine Mantle* family) — defensive, per-attack,
and not a profile at all.

**Method.** Descriptions were split into clauses (sentence boundaries plus `, and` / `;`,
because several records join an unconditional clause to a conditional one with a comma —
*Slayer of Champions* and *Radiant Champion* both do, and a sentence-level split
mis-files them). A clause counts as conditional if it carries any of: *once per…*, *each
time*, *while*, *until the end*, *at the start/end of*, *instead*, *when*, *after*, *if*,
*is selected to*, *can use this Enhancement*. This is the same marker vocabulary
`_condMarker` already uses in `index.html` for the wargear statline reader, extended.

## 2. This is not a D0 item

The backlog entry called B99 a "live D0-adjacent gap". That is wrong and should not be carried
forward. An enhancement's stat bonus changes no unit's points, no enhancement's cost, and no
legality test — assignment eligibility (E4b/B113) is already enforced separately and is
untouched by this. No illegal state is reachable because of B99, and fixing it makes none
unreachable. **B99 is a display-fidelity item**: the app shows a number the user's model does
not have. Worth fixing on trust grounds; it should be sized and sequenced as fidelity work, not
as legality work.

## 3. Where it would have to render

Two weapon tables exist, and they are separate code:

- `buildWeaponTable` (via `buildWeaponSections`) — the per-model-group table.
- `loWeaponTable` (via `loadoutWeaponHtml`) — the rollup table used for loadout-defined units,
  which shows a weapon once with an `×N` count.

Both must be fed, or the same unit will show a modified profile on one surface and the printed
one on the other. That divergence is the failure mode this project has already paid for once.

`buildWeaponSections` is called twice. The **configured** call (right-hand pane) receives
`entry`; the **full/unconfigured** call receives `entry` as absent. That is the correct split
and needs no change: an unconfigured browse view has no list entry and therefore no
enhancement, so modified numbers can only ever appear in the configured pane and the loadout
rollup. `loadoutWeaponHtml` already receives `entry`. **No plumbing work is needed to make the
assignment reachable at either render site** — `entry.enhancement` is `{name, detachment_key}`
and `enhancementRecord(name, key)` already resolves it to the full record.

The Enhancement section itself (`renderEnhancementSectionHtml`) already renders the assigned
enhancement with an eye control that expands its full description text. Anything not
represented numerically is therefore already one click from the user.

## 4. What the data supports, and three traps

**Selectors resolve cleanly.** Set A uses only five weapon selectors: *melee weapons* (53),
*weapons* i.e. all (2), *those weapons* (1, anaphoric — see below), *Psychic weapons* (1),
*melee weapons (excluding Extra Attacks weapons)* (1). Every one is answerable from
`units.json`: `weapon_type` is `Ranged`/`Melee`, and `Psychic`, `Torrent` and `Extra Attacks`
all appear as `weapon_ability_names` entries (194, 146 and 60 rows respectively). Nothing
needs new data.

**Trap 1 — "Improve" has opposite arithmetic on AP.** `AP` is stored as a signed integer
(`0`, `-1`, `-2`, `-3`, `-4`). "Improve the Armour Penetration characteristic by 1" makes it
*more negative*: `-1` → `-2`. On Strength, Attacks and Damage "improve" and "add" both mean
*add*. A single generic "improve = +N" implementation is wrong for exactly the most common
modifier in Set A.

**Trap 2 — variable characteristics.** `A` and `D` are stored as strings and are not always
numeric (`D6`, `D3`, `D6+3`, `2D6`). Across the melee weapons of the 208 Character/Epic Hero
units that can plausibly bear an enhancement, 3 rows have a variable `A` and 43 have a
variable `D`. The correct rendering is string composition — `D6` +1 → `D6+1`, a shape already
present in the data (99 rows) — not arithmetic. `S` and `AP` are always integers.

**Trap 3 — the bearer is one model, the table is not always one model.** Ten Character/Epic
Hero units are loadout-defined with more than one model group (*Dark Apostle* + Dark
Disciples, *Chaplain Grimaldus* + Cenobyte Servitors, *Fabius Bile* + Surgeon Acolyte,
*Wardens of Ultramar*, *Ravenwing Command Squad*, *Dark Commune*, *Traitor Enforcer*, and
their cross-faction duplicates). On these the rollup table shows one row per weapon with a
count spanning models the bearer is not. Writing a modified number into such a row asserts
something false about the other models. This is the same problem D105/D112 already solved for
the statline, and its answer already exists in this codebase: the three-way rule — every
carrier gets the value, *some* carriers get an asterisk to the rules text, no carrier gets
nothing. The build should reuse that idiom rather than invent one.

**Two irregular texts** need explicit handling and are the reason a naive reader is unsafe:
*Ancient Weapons* (Dark Angels) uses anaphora — "…of melee weapons equipped by the bearer by
2, and improve the Armour Penetration and Damage characteristics of **those weapons** by 1";
and *Blades of Valour* (6 chapters) targets "the bearer **and Battleline models in the
bearer's unit**", so it is simultaneously a Set A and a Set D record and only its bearer half
is in scope here.

## 5. Recommended mechanism

**A curated table in `index.html`, keyed `detachment_key + '::' + enhancement_name`, plus a
source-derived census assertion in `rules_assertions.py`.** This is precisely the B113 shape
(`ENHANCEMENT_BEARER_RESTRICTIONS` + `b113_bearer_table_matches_source`), which is already
proven, already understood, and already uses the same key.

Rejected alternatives, with the reason:

- *Parse the description at render time in the engine.* The clause shapes are regular enough
  that this would work for most records, but a parse miss is silent, and traps 1 and 3 plus
  the two irregular texts are exactly where it would miss. The engine's existing text reader
  (`statOverrideFromText`) only handles absolute "characteristic of N" sets, so this is not an
  extension of it in any case — it is a new relative-delta reader.
- *Emit a structured field from `detachment_parser.py`.* Source-derived and regenerable, but
  it moves the same fragile text parsing into the parser and rewrites all 739 enhancement
  records in `detachments.json` for 72 records' worth of benefit.

The census assertion is the part that matters and is the improvement over a bare curated
table: it must re-derive the candidate set from `detachments.json` descriptions and **fail if
any record matches the Set A / A2 shape but has no table row**, so that a faction built later
cannot silently introduce an unhandled enhancement. Without that check a curated table rots the
moment a new faction lands.

## 6. Decisions for Ryan

Recommendations below; the build turn proceeds on them unless Ryan says otherwise. None is
expensive to reverse.

1. **Change the printed numbers at all?** *Recommend yes*, for Set A only, in the configured
   pane and the loadout rollup. A Character with *War-tempered Artifice* really does swing at
   S+3 in every game; showing the printed number is showing something the user does not have.
2. **Display idiom.** *Recommend* the modified value in the cell, the cell marked, and a legend
   line beneath the table naming the enhancement — the existing D89/D112 asterisk-and-legend
   idiom, so the weapon table reads the same way the statline already does. Alternatives
   considered: modified-only with no marker (loses the link to the cause), and `7 (4)`
   base-in-parentheses (heavier in an eight-column table).
3. **Conditional effects (Set B, and the conditional halves of Set A records).**
   *Recommend no marker.* The enhancement's full text already expands from the eye control in
   the Enhancement section, and asterisking every conditional clause would mark most bearers'
   tables without telling the user anything actionable.
4. **Weapon-ability grants (Set A2).** *Recommend folding into the same build* — same 78-record
   union population, same curated table, same render path, different column (Abilities rather
   than a number). Splitting it means touching the same code twice.
5. **How New Recruit handles this** is unknown to me and would usefully inform decision 2. Ryan
   has offered screenshots; worth one before the build turn if he wants the idiom matched.

## 7. Build plan

Two turns, in order. Do not merge them.

1. **Engine turn.** The curated `ENHANCEMENT_WEAPON_EFFECTS` table (78 records, 43 distinct
   names — corrected at D330; see §1's note), the delta applier (with the AP sign rule and
   string composition for variable `A`/`D`), the three-way carrier rule for multi-model-group
   bearers, and both render sites. Plus a new `b99_check.js` harness pinning: the AP sign, a
   variable-`D` composition, a multi-model-group bearer getting an asterisk rather than a
   value, the unconfigured view staying unmodified, and both render surfaces agreeing.
2. **Tooling turn.** The `rules_assertions.py` census assertion described in §5, driven off
   `detachments.json`, pinning the corrected 57 / 23 / 78 figures and failing on an unhandled
   record. Shipped at D331 (S237) as `B99-CENSUS`.

Sets B, C and D are **not** in this build. C and D are banked as their own tickets (B119, B120)
with their populations already censused above.

## 8. Out of scope, checked and stated

Detachment **rule** text carries the same modifier shapes — 31 sentences, of which 7 read as
unconditional. All 7 were read directly and none is an army-construction fact: they are
in-battle grants and player choices (Creations of Bile's surgical enhancements, Spectacle of
Spite's combat drugs, Wrathful Procession's in-battle rite). Detachment rules are correctly
out of scope for B99 and should not be folded in later without re-reading them.
