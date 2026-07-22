# Standalone-Faction MFM Pass

Standalone factions: one faction, one MFM, no generic/chapter split → no conflict surface. Checks: **orphans** (MFM-priced, no datasheet), **uncosted** (non-Legends datasheet, no MFM price), and **name-normalization recurrence** (orphan/uncosted that match by punctuation/suffix-stripped name — the SM-family defect, tested for recurrence). Orphans vs a 10th-ed base may be edition-drift.


## Drukhari
- Datasheets (faction_id DRU): **47** (37 current / 10 Legends-FW).
- MFM `MFM_Drukhari_v1_0.txt` prices **30** units.
- **Uncosted current datasheets: 14**: Corsair Skyreavers, Corsair Voidreavers, Corsair Voidscarred, Death Jester, Kharseth, Prince Yriel, Shadowseer, Skyweavers, Solitaire, Starfangs, Starweaver, Troupe, Troupe Master, Voidweaver
- **Orphans (priced, no datasheet): 0** — none.


---
# Standalone batch 2 — remaining factions

Auto-mapped each MFM to its faction_id by datasheet-name overlap. Checks: uncosted current datasheets, orphans (priced/no datasheet), name-normalization recurrence, and **cross-faction sourcing** (uncosted unit priced in another faction's MFM — the Harlequin/Aeldari pattern).


## Adepta Sororitas  (faction_id AS, name-overlap 38)
- Datasheets: **38** (33 current / 5 Legends-FW); MFM prices **38**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

## Adeptus Custodes  (faction_id AC, name-overlap 31)
- Datasheets: **31** (18 current / 13 Legends-FW); MFM prices **31**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

## Adeptus Mechanicus  (faction_id AdM, name-overlap 38)
- Datasheets: **39** (34 current / 5 Legends-FW); MFM prices **38**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

## Aeldari  (faction_id AE, name-overlap 92)
- Datasheets: **97** (70 current / 27 Legends-FW); MFM prices **93**.
- Uncosted current datasheets: **1**: Vypers
- Orphans (priced, no datasheet): **1**: VYPER

## Astra Militarum  (faction_id AM, name-overlap 132)
- Datasheets: **134** (70 current / 64 Legends-FW); MFM prices **133**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **1**: HELL'S LAST

## Chaos Knights  (faction_id QT, name-overlap 20)
- Datasheets: **37** (18 current / 19 Legends-FW); MFM prices **20**.
- Uncosted current datasheets: **7**: Accursed Cultists, Cultist Firebrand, Cultist Mob, Dark Commune, Fellgor Beastmen, Traitor Enforcer, Traitor Guardsmen Squad
- Orphans (priced, no datasheet): **0** — none.
- **CROSS-FACTION sourcing (7)** — uncosted here, priced in another faction's MFM:
  - 'Cultist Firebrand' → MFM_Chaos_Space_Marines_v1_0.txt
  - 'Dark Commune' → MFM_Chaos_Space_Marines_v1_0.txt
  - 'Traitor Enforcer' → MFM_Chaos_Space_Marines_v1_0.txt
  - 'Cultist Mob' → MFM_Chaos_Space_Marines_v1_0.txt
  - 'Accursed Cultists' → MFM_Chaos_Space_Marines_v1_0.txt
  - 'Fellgor Beastmen' → MFM_Chaos_Space_Marines_v1_0.txt
  - 'Traitor Guardsmen Squad' → MFM_Chaos_Space_Marines_v1_0.txt

## Chaos Space Marines  (faction_id CSM, name-overlap 85)
- Datasheets: **112** (58 current / 54 Legends-FW); MFM prices **85**.
- Uncosted current datasheets: **4**: Khorne Berzerkers, Noise Marines, Plague Marines, Rubric Marines
- Orphans (priced, no datasheet): **0** — none.
- **CROSS-FACTION sourcing (3)** — uncosted here, priced in another faction's MFM:
  - 'Rubric Marines' → MFM_Thousand_Sons_v1_0.txt
  - 'Plague Marines' → MFM_Death_Guard_v1_0.txt
  - 'Noise Marines' → MFM_Emperors_Children_v1_0.txt

## Chaos Titan Legions  (faction_id AC, name-overlap 0)
- Datasheets: **31** (18 current / 13 Legends-FW); MFM prices **0**.
- Uncosted current datasheets: **18**: Aleya, Allarus Custodians, Anathema Psykana Rhino, Blade Champion, Custodian Guard, Custodian Wardens, Knight-centura, Prosecutors, Shield-captain, Shield-captain In Allarus Terminator Armour, Shield-captain On Dawneagle Jetbike, Trajann Valoris, Valerian, Venerable Contemptor Dreadnought, Venerable Land Raider, Vertus Praetors, Vigilators, Witchseekers
- Orphans (priced, no datasheet): **0** — none.
- **CROSS-FACTION sourcing (18)** — uncosted here, priced in another faction's MFM:
  - 'Custodian Guard' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Venerable Contemptor Dreadnought' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Venerable Land Raider' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Trajann Valoris' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Shield-captain' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Shield-captain In Allarus Terminator Armour' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Shield-captain On Dawneagle Jetbike' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Custodian Wardens' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Allarus Custodians' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Vertus Praetors' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Aleya' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Blade Champion' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Valerian' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Knight-centura' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Prosecutors' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Vigilators' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Witchseekers' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Anathema Psykana Rhino' → MFM_Adeptus_Custodes_v1_0.txt

## Death Guard  (faction_id DG, name-overlap 40)
- Datasheets: **71** (36 current / 35 Legends-FW); MFM prices **41**.
- Uncosted current datasheets: **1**: Myphitic Blight-hauler
- Orphans (priced, no datasheet): **1**: MYPHITIC BLIGHT-HAULERS

## Emperors Children  (faction_id EC, name-overlap 23)
- Datasheets: **23** (23 current / 0 Legends-FW); MFM prices **23**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

## Genestealer Cults  (faction_id GC, name-overlap 25)
- Datasheets: **139** (87 current / 52 Legends-FW); MFM prices **25**.
- Uncosted current datasheets: **63**: Aegis Defence Line, Armoured Sentinels, Artillery Team, Attilan Rough Riders, Baneblade, Banehammer, Banesword, Basilisk, Cadian Castellan, Cadian Command Squad, Cadian Heavy Weapons Squad, Cadian Shock Troops, Catachan Command Squad, Catachan Heavy Weapons Squad, Catachan Jungle Fighters, Centaur RSV, Chimera, Death Korps Of Krieg, Death Riders, Deathleaper, Deathstrike, Doomhammer, Field Ordnance Battery, Gargoyles, Hellhammer, Hellhound, Hippogriff AFV, Hydra, Hyperadapted Raveners, Kasrkin, Krieg Combat Engineers, Krieg Command Squad, Krieg Heavy Weapons Squad, Leman Russ Battle Tank, Leman Russ Commander, Leman Russ Demolisher, Leman Russ Eradicator, Leman Russ Executioner, Leman Russ Exterminator, Leman Russ Punisher, Leman Russ Vanquisher, Lictor, Manticore, Mawloc, Neurolictor, Parasite Of Mortrex, Primaris Psyker, Raveners, Rogal Dorn Battle Tank, Rogal Dorn Commander, Scout Sentinels, Shadowsword, Stormlord, Stormsword, Taurox, Taurox Prime, The Red Terror, Trygon, Tyrannocyte, Von Ryan’s Leapers, Winged Hive Tyrant, Winged Tyranid Prime, Wyvern
- Orphans (priced, no datasheet): **0** — none.
- **CROSS-FACTION sourcing (63)** — uncosted here, priced in another faction's MFM:
  - 'Deathleaper' → MFM_Tyranids_v1_0.txt
  - 'Parasite Of Mortrex' → MFM_Tyranids_v1_0.txt
  - 'Winged Hive Tyrant' → MFM_Tyranids_v1_0.txt
  - 'Winged Tyranid Prime' → MFM_Tyranids_v1_0.txt
  - 'Gargoyles' → MFM_Tyranids_v1_0.txt
  - 'Tyrannocyte' → MFM_Tyranids_v1_0.txt
  - 'Lictor' → MFM_Tyranids_v1_0.txt
  - 'Mawloc' → MFM_Tyranids_v1_0.txt
  - 'Neurolictor' → MFM_Tyranids_v1_0.txt
  - 'Raveners' → MFM_Tyranids_v1_0.txt
  - 'Trygon' → MFM_Tyranids_v1_0.txt
  - 'Von Ryan’s Leapers' → MFM_Tyranids_v1_0.txt
  - 'Cadian Castellan' → MFM_Astra_Militarum_v1_0.txt
  - 'Cadian Command Squad' → MFM_Astra_Militarum_v1_0.txt
  - 'Catachan Command Squad' → MFM_Astra_Militarum_v1_0.txt
  - 'Krieg Command Squad' → MFM_Astra_Militarum_v1_0.txt
  - 'Leman Russ Commander' → MFM_Astra_Militarum_v1_0.txt
  - 'Primaris Psyker' → MFM_Astra_Militarum_v1_0.txt
  - 'Rogal Dorn Commander' → MFM_Astra_Militarum_v1_0.txt
  - 'Cadian Shock Troops' → MFM_Astra_Militarum_v1_0.txt
  - 'Catachan Jungle Fighters' → MFM_Astra_Militarum_v1_0.txt
  - 'Death Korps Of Krieg' → MFM_Astra_Militarum_v1_0.txt
  - 'Chimera' → MFM_Astra_Militarum_v1_0.txt
  - 'Taurox' → MFM_Astra_Militarum_v1_0.txt
  - 'Taurox Prime' → MFM_Astra_Militarum_v1_0.txt
  - 'Aegis Defence Line' → MFM_Astra_Militarum_v1_0.txt
  - 'Armoured Sentinels' → MFM_Astra_Militarum_v1_0.txt
  - 'Artillery Team' → MFM_Astra_Militarum_v1_0.txt
  - 'Attilan Rough Riders' → MFM_Astra_Militarum_v1_0.txt
  - 'Baneblade' → MFM_Astra_Militarum_v1_0.txt
  - 'Banehammer' → MFM_Astra_Militarum_v1_0.txt
  - 'Banesword' → MFM_Astra_Militarum_v1_0.txt
  - 'Basilisk' → MFM_Astra_Militarum_v1_0.txt
  - 'Cadian Heavy Weapons Squad' → MFM_Astra_Militarum_v1_0.txt
  - 'Catachan Heavy Weapons Squad' → MFM_Astra_Militarum_v1_0.txt
  - 'Death Riders' → MFM_Astra_Militarum_v1_0.txt
  - 'Deathstrike' → MFM_Astra_Militarum_v1_0.txt
  - 'Doomhammer' → MFM_Astra_Militarum_v1_0.txt
  - 'Field Ordnance Battery' → MFM_Astra_Militarum_v1_0.txt
  - 'Hellhammer' → MFM_Astra_Militarum_v1_0.txt
  - 'Hellhound' → MFM_Astra_Militarum_v1_0.txt
  - 'Hydra' → MFM_Astra_Militarum_v1_0.txt
  - 'Kasrkin' → MFM_Astra_Militarum_v1_0.txt
  - 'Krieg Combat Engineers' → MFM_Astra_Militarum_v1_0.txt
  - 'Krieg Heavy Weapons Squad' → MFM_Astra_Militarum_v1_0.txt
  - 'Leman Russ Battle Tank' → MFM_Astra_Militarum_v1_0.txt
  - 'Leman Russ Demolisher' → MFM_Astra_Militarum_v1_0.txt
  - 'Leman Russ Eradicator' → MFM_Astra_Militarum_v1_0.txt
  - 'Leman Russ Executioner' → MFM_Astra_Militarum_v1_0.txt
  - 'Leman Russ Exterminator' → MFM_Astra_Militarum_v1_0.txt
  - 'Leman Russ Punisher' → MFM_Astra_Militarum_v1_0.txt
  - 'Leman Russ Vanquisher' → MFM_Astra_Militarum_v1_0.txt
  - 'Manticore' → MFM_Astra_Militarum_v1_0.txt
  - 'Rogal Dorn Battle Tank' → MFM_Astra_Militarum_v1_0.txt
  - 'Scout Sentinels' → MFM_Astra_Militarum_v1_0.txt
  - 'Shadowsword' → MFM_Astra_Militarum_v1_0.txt
  - 'Stormlord' → MFM_Astra_Militarum_v1_0.txt
  - 'Stormsword' → MFM_Astra_Militarum_v1_0.txt
  - 'Wyvern' → MFM_Astra_Militarum_v1_0.txt
  - 'Hyperadapted Raveners' → MFM_Tyranids_v1_0.txt
  - 'Centaur RSV' → MFM_Astra_Militarum_v1_0.txt
  - 'Hippogriff AFV' → MFM_Astra_Militarum_v1_0.txt
  - 'The Red Terror' → MFM_Tyranids_v1_0.txt

## Grey Knights  (faction_id GK, name-overlap 31)
- Datasheets: **31** (25 current / 6 Legends-FW); MFM prices **31**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

## Imperial Agents  (faction_id AoI, name-overlap 46)
- Datasheets: **46** (29 current / 17 Legends-FW); MFM prices **46**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

## Imperial Knights  (faction_id QI, name-overlap 22)
- Datasheets: **28** (19 current / 9 Legends-FW); MFM prices **22**.
- Uncosted current datasheets: **6**: Sir Hekhtur, Skitarii Marshal, Skitarii Rangers, Skitarii Vanguard, Tech-priest Dominus, Tech-priest Manipulus
- Orphans (priced, no datasheet): **0** — none.
- **CROSS-FACTION sourcing (5)** — uncosted here, priced in another faction's MFM:
  - 'Tech-priest Dominus' → MFM_Adeptus_Mechanicus_v1_0.txt
  - 'Tech-priest Manipulus' → MFM_Adeptus_Mechanicus_v1_0.txt
  - 'Skitarii Marshal' → MFM_Adeptus_Mechanicus_v1_0.txt
  - 'Skitarii Rangers' → MFM_Adeptus_Mechanicus_v1_0.txt
  - 'Skitarii Vanguard' → MFM_Adeptus_Mechanicus_v1_0.txt

## Leagues of Votann  (faction_id LoV, name-overlap 22)
- Datasheets: **22** (22 current / 0 Legends-FW); MFM prices **22**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

## Necrons  (faction_id NEC, name-overlap 63)
- Datasheets: **64** (51 current / 13 Legends-FW); MFM prices **64**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **1**: SENTRY PYLONS

## Orks  (faction_id ORK, name-overlap 84)
- Datasheets: **87** (53 current / 34 Legends-FW); MFM prices **88**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **4**: BANNERNOB, BIG MEK DAKKARIG, BIGBOSS, WARTRAKK

## Tau Empire  (faction_id TAU, name-overlap 61)
- Datasheets: **63** (39 current / 24 Legends-FW); MFM prices **61**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

## Thousand Sons  (faction_id TS, name-overlap 34)
- Datasheets: **60** (34 current / 26 Legends-FW); MFM prices **34**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

## Titan Legions  (faction_id AC, name-overlap 0)
- Datasheets: **31** (18 current / 13 Legends-FW); MFM prices **0**.
- Uncosted current datasheets: **18**: Aleya, Allarus Custodians, Anathema Psykana Rhino, Blade Champion, Custodian Guard, Custodian Wardens, Knight-centura, Prosecutors, Shield-captain, Shield-captain In Allarus Terminator Armour, Shield-captain On Dawneagle Jetbike, Trajann Valoris, Valerian, Venerable Contemptor Dreadnought, Venerable Land Raider, Vertus Praetors, Vigilators, Witchseekers
- Orphans (priced, no datasheet): **0** — none.
- **CROSS-FACTION sourcing (18)** — uncosted here, priced in another faction's MFM:
  - 'Custodian Guard' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Venerable Contemptor Dreadnought' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Venerable Land Raider' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Trajann Valoris' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Shield-captain' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Shield-captain In Allarus Terminator Armour' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Shield-captain On Dawneagle Jetbike' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Custodian Wardens' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Allarus Custodians' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Vertus Praetors' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Aleya' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Blade Champion' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Valerian' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Knight-centura' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Prosecutors' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Vigilators' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Witchseekers' → MFM_Adeptus_Custodes_v1_0.txt
  - 'Anathema Psykana Rhino' → MFM_Adeptus_Custodes_v1_0.txt

## Tyranids  (faction_id TYR, name-overlap 57)
- Datasheets: **57** (50 current / 7 Legends-FW); MFM prices **57**.
- Uncosted current datasheets: **0** — none.
- Orphans (priced, no datasheet): **0** — none.

---
## Batch 2 conclusions

1. **PARSER BUG — thousands-separator comma.** `mfm_points_parser` fails to read points written with a comma (e.g. `2,200 pts`), so every unit priced ≥1,000 pts parses as un-costable. Surfaced via Titan Legions / Chaos Titan Legions (files have content — Reaver 2,200, Warbringer 2,600 — but 0 parsed). Affects any ≥1,000-pt unit across all factions, not just Titans. Highest-value fix from this pass. (The AC faction-mapping on those two rows is an auto-mapper fallback from the 0-parse; it resolves once the comma is handled.)

2. **Name-normalization is SM-chapter-specific.** Zero recurrence across all 20 standalone factions, including punctuation-heavy Necrons/Tyranids/Orks. The apostrophe/suffix mismatch fix stays scoped to the SM-family named-character MFM sections; no global matcher change needed.

3. **Cross-faction sourcing is the recurring structural pattern.** Datasheet tagged to faction X, points owned by faction Y's MFM. Concentrated in: Imperial Knights ↔ Chaos Knights (the Knights pair), Chaos Space Marines cult/traitor units, Thousand Sons, and most heavily Genestealer Cults (63 units priced in the CSM MFM). Same shape as the SM chapters and the Harlequin/Aeldari case. The points-sourcing model must let a faction draw unit points from sibling/parent MFMs, not only its own file.

4. **Clean factions** (no uncosted, no orphans, no cross-faction): Adepta Sororitas, Adeptus Custodes, Adeptus Mechanicus, Emperor's Children, Grey Knights, Imperial Agents, Leagues of Votann, T'au Empire, Thousand Sons (self-sourced), Tyranids. Small orphan counts (1–4) on Aeldari, Astra Militarum, Death Guard, Necrons, Orks are noted per-faction above — likely loadout-variant lines or edition-drift, not defects.

5. **Scope flag (verify, not tonight):** Genestealer Cults faction_id (GC) returns 139 datasheets — anomalously large. Its cross-faction hits suggest the faction_id tag pulls in shared cult/traitor/allied units broadly. Confirm the intended GSC scope before relying on a raw faction_id filter.

**No MFM file present for World Eaters** (faction_id WE, 58 datasheets) — its MFM was not in the project file set. Flagged as a data gap.

## World Eaters  (faction_id WE) — added after file provided
- Datasheets: **58** (30 current / 28 Legends-FW); MFM prices **30**.
- Uncosted current datasheets: **0** — none.
- Orphans: **0** — none.

---
## Genestealer Cults scope flag — RESOLVED

The anomalous GC count (139) is explained, not a defect. Breakdown of the `GC` faction_id datasheets by source:

- **24** — Genestealer Cults codex (the faction's own units; matches NR and the MFM)
- **1** — Genestealer Cults (Warhammer Legends)
- **49** — Astra Militarum codex + **50** Astra Militarum (Legends) + **1** AM (Forge World) — Brood Brothers / allied-Guard units a GSC army can field
- **14** — Tyranids codex — shared Genestealer/biomorph datasheets

So `faction_id == GC` means "everything a GSC army can include," not "the GSC codex." The ~100 Guard and 14 Tyranid units are correctly priced in the **Astra Militarum** and **Tyranids** MFMs, which is why the pass reported 63 cross-faction-sourced units — the pattern working as intended, at scale, because GSC borrows an entire allied codex.

**Implication:** building "Genestealer Cults" as a clean faction requires scoping its *own* units to the GSC codex source (000000053), then treating the Brood Brothers Guard units as allied inclusions — i.e. GSC is an early concrete instance of the **allies** problem, not merely a points-sourcing quirk. Do not filter GSC by raw faction_id alone.

Confirmed target counts: **24 GSC codex units + 1 Legends + 9 detachments.**
