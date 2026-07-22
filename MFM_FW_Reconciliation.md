# New-MFM / Forge World Reconciliation

Analysis only. No scripts, data, or config changed. Source of truth for “has a datasheet” is the 181-unit SM transform output; FW/Legends is the datasheet’s Wahapedia source, matching the transform’s own exclusion rule.


## Headline — corrects the prior estimate

The handoff expected the +76 delta to be roughly half core-missing units (bikes, jump packs, command squad, dreadnought variants, named chars) and half Forge World/Legends. **That estimate is wrong.** Those firstborn units were moved to Legends in 10th edition, so they read as Legends in the current Wahapedia data. The delta is almost entirely FW/Legends.

- Old `mfm_sm.txt` prices **103** units; new `MFM_Space_Marines_v1_0.txt` prices **179** (**+76**, **-0** removed).
- Of the **76** new-only priced units:
  - **1 genuine core** — has a datasheet in the 181, currently un-priced → the *only* real unlock from the switch: **VENERABLE DREADNOUGHT**.
  - **74 Forge World / Legends** — priced but excluded at transform; inert (`points_no_stat`) until the transform FW toggle exists.
  - **1 no SM datasheet** — **investigate**: **FERREN AERIOS** (name mismatch or genuinely absent).
- **Net:** switching the SM MFM unlocks **1** core unit and would add **+75** `points_no_stat` orphans. It is **not** the core-coverage upgrade it was thought to be — its value is the FW/Legends pricing layer, which does nothing until the FW toggle ships.

## Core units now priced — safe to adopt (1)

These have a datasheet in the current build; switching the MFM prices them with no orphan.

- VENERABLE DREADNOUGHT

## Forge World / Legends — expected/deferred (74)

Priced by the new MFM but excluded at transform; these are the deferred-FW bucket. They resolve cleanly once the transform FW toggle ships.

- ANCIENT ON BIKE
- APOTHECARY ON BIKE
- ASSAULT SQUAD
- ASSAULT SQUAD WITH JUMP PACKS
- ASTARTES SERVITORS
- ATTACK BIKE SQUAD
- BIKE SQUAD
- CAESTUS ASSAULT RAM
- CAPTAIN ON BIKE
- CARAB CULLN THE RISEN
- CERBERUS
- CHAPLAIN CASSIUS
- CHAPLAIN VENERABLE DREADNOUGHT
- COMMAND SQUAD
- COMPANY CHAMPION ON BIKE
- COMPANY VETERANS ON BIKES
- DEATHSTORM DROP POD
- DEIMOS PREDATOR
- DEREDEO DREADNOUGHT
- DREADNOUGHT DROP POD
- FALCHION
- FELLBLADE
- FIRE RAPTOR GUNSHIP
- HUNTER
- IMPERIAL SPACE MARINE
- IRONCLAD DREADNOUGHT
- JAVELIN ATTACK SPEEDER
- KRATOS
- LAND RAIDER ACHILLES
- LAND RAIDER EXCELSIOR
- LAND RAIDER HELIOS
- LAND RAIDER PROMETHEUS
- LAND RAIDER PROTEUS
- LAND SPEEDER STORM
- LAND SPEEDER TEMPEST
- LAND SPEEDER TORNADO
- LAND SPEEDER TYPHOON
- LEVIATHAN DREADNOUGHT
- LIBRARIAN ON BIKE
- LIBRARIAN WITH JUMP PACK
- MASTODON
- MORTIS DREADNOUGHT
- PRIMARIS COMPANY CHAMPION
- RAPIER CARRIER
- RELIC CONTEMPTOR DREADNOUGHT
- RELIC RAZORBACK
- RELIC TERMINATOR SQUAD
- RHINO PRIMARIS
- SCOUT BIKE SQUAD
- SCOUT SNIPER SQUAD
- SERGEANT CHRONUS
- SERGEANT TELION
- SICARAN ARCUS
- SICARAN BATTLE TANK
- SICARAN OMEGA
- SICARAN PUNISHER
- SICARAN VENATOR
- SOKAR-PATTERN STORMBIRD
- SPARTAN
- STALKER
- STORM EAGLE GUNSHIP
- TARANTULA AIR DEFENCE BATTERY
- TARANTULA SENTRY BATTERY
- TECHMARINE ON BIKE
- TERMINUS ULTRA
- TERRAX-PATTERN TERMITE
- THUNDERFIRE CANNON
- THUNDERHAWK TRANSPORTER
- TYPHON
- TYRANNIC WAR VETERANS
- VANGUARD VETERAN SQUAD
- VINDICATOR LASER DESTROYER
- WHIRLWIND SCORPIUS
- XIPHON INTERCEPTOR

## No SM datasheet — investigate (1)

Priced by the new MFM but no faction_id=SM datasheet matched by name. Likely a name-normalisation mismatch (MFM vs Wahapedia spelling) or a unit genuinely absent from the export. Each needs a name check before adoption.

- FERREN AERIOS

## Black Templars points gap

The 12 BT units that are un-costable in the deployed build, and whether each is priced by the new SM MFM (vs the old).

| Unit | In new SM MFM | In old SM MFM |
|---|---|---|
| Chaplain Grimaldus | no | no |
| Castellan | no | no |
| High Marshal Helbrecht | no | no |
| Emperor’s Champion | no | no |
| Marshal | no | no |
| Sword Brethren Squad | no | no |
| Crusader Squad | no | no |
| Execrator | no | no |
| Crusade Ancient | no | no |
| Sternguard Veteran Squad | yes | yes |
| Terminator Squad | yes | yes |
| Land Raider Crusader | yes | yes |

New SM MFM prices **3/12** of the gap units. A dedicated `MFM_Black_Templars_v1_0.txt` is also present and prices **89** units — the cleaner source for BT-specific points; cross-check before deciding which file owns BT.

## Captain variants

Captain-family entries priced by the new MFM, and whether each has a datasheet in the 181.

| Variant | Has datasheet | In old MFM |
|---|---|---|
| CAPTAIN | yes | yes |
| CAPTAIN IN GRAVIS ARMOUR | yes | yes |
| CAPTAIN IN PHOBOS ARMOUR | yes | yes |
| CAPTAIN IN TERMINATOR ARMOUR | yes | yes |
| CAPTAIN ON BIKE | NO | no |
| CAPTAIN TITUS | yes | yes |
| CAPTAIN WITH JUMP PACK | yes | yes |

## Recommendation

1. **Don’t switch the SM MFM as a “core coverage” move — it isn’t one.** It unlocks a single core unit (Venerable Dreadnought). Price that one unit directly (errata/override) rather than swapping the whole points file and importing 75 orphans.
2. **Treat the new SM MFM as the FW/Legends pricing layer it actually is.** Adopt it *with* the transform FW toggle, not before — switching first just inflates `points_no_stat` by ~75 and makes the blocking count meaningless. The two changes are a pair.
3. **Investigate the no-datasheet name(s)** — FERREN AERIOS — before any switch; resolve as a name mismatch or confirm it’s genuinely out of scope.
4. **Black Templars points come from `MFM_Black_Templars_v1_0.txt` (89 priced), not the SM MFM** (which closes only 3/12). Wire BT points from the dedicated file; don’t double-source.
5. **Net effect on the roadmap:** the new-MFM task is gated on the FW toggle, not a quick win. The FW toggle is the actual high-leverage item; the MFM switch rides on it.

*No files were modified by this analysis.*

