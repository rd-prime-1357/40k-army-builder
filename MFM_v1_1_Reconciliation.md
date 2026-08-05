# MFM v1.1 Reconciliation — per-faction delta report (B88)

Analysis only. No scripts, data, or config changed. Each faction compares its v1.1 capture against the v1_0 file the app was actually built from. Scope is the 10 distinct MFM files backing the app's currently-built armies (`faction_taxonomy.json` armies with real `units.json` data) — not all 15 v1.1 files banked in `source_manifest.json`; the other 5 factions have no built version to diff against.


## Summary

| Faction | Adopt-mechanically | Investigate-first |
|---|---|---|
| Space Marines | 30 | 14 |
| Black Templars | 22 | 9 |
| Blood Angels | 19 | 8 |
| Dark Angels | 29 | 9 |
| Deathwatch | 19 | 9 |
| Space Wolves | 26 | 11 |
| Chaos Space Marines | 18 | 4 |
| Death Guard | 5 | 2 |
| Chaos Daemons | 9 | 1 |
| Thousand Sons | 12 | 4 |
| **Total** | **189** | **71** |


## Space Marines

`MFM_Space_Marines_v1_0.txt` (179 units, 22 detachments) vs `MFM_Space_Marines_v1.1.txt` (179 units, 23 detachments). **30 adopt-mechanically, 14 investigate-first.**

**Points changed — adopt-mechanically (25)**
- AGGRESSOR SQUAD: `[{"3": 90, "6": 180}, {"3": 100, "6": 190}]` → `[{"3": 80, "6": 165}, {"3": 90, "6": 175}]`
- CAPTAIN TITUS: `[{"1": 90}]` → `[{"1": 100}]`
- CATO SICARIUS: `[{"1": 95}]` → `[{"1": 105}]`
- CHIEF LIBRARIAN TIGURIUS: `[{"1": 95}]` → `[{"1": 85}]`
- DROP POD: `[{"1": 70}]` → `[{"1": 60}, {"1": 70}]` (mode single→esc4)
- ERADICATOR SQUAD WITH HEAVY BOLTERS: `[{"3": 70}, {"3": 80}]` → `[{"3": 80}]` (mode split→single)
- IMPULSOR: `[{"1": 80}]` → `[{"1": 70}, {"1": 80}]` (mode single→esc4)
- INCEPTOR SQUAD: `[{"3": 120, "6": 240}, {"3": 135, "6": 255}]` → `[{"3": 125, "6": 250}, {"3": 140, "6": 265}]`
- INFERNUS SQUAD: `[{"5": 85, "10": 170}]` → `[{"5": 85, "10": 180}]`
- LAND SPEEDER: `[{"1": 95}, {"1": 105}]` → `[{"1": 105}]` (mode split→single)
- LIBRARIAN: `[{"1": 60}]` → `[{"1": 70}, {"1": 80}]` (mode single→split)
- LIEUTENANT WITH COMBI-WEAPON: `[{"1": 85}]` → `[{"1": 95}]`
- MARNEUS CALGAR IN ARMOUR OF ANTILOCHUS: `[{"1": 140}]` → `[{"1": 155}]`
- RAZORBACK: `[{"1": 95}]` → `[{"1": 85}, {"1": 95}]` (mode single→esc4)
- REPULSOR EXECUTIONER: `[{"1": 240}, {"1": 260}]` → `[{"1": 255}, {"1": 275}]`
- RHINO: `[{"1": 75}]` → `[{"1": 65}, {"1": 75}]` (mode single→esc4)
- ROBOUTE GUILLIMAN: `[{"1": 340}]` → `[{"1": 355}]`
- STERNGUARD VETERAN SQUAD: `[{"5": 100, "10": 190}]` → `[{"5": 100, "10": 200}]`
- STORM SPEEDER HAMMERSTRIKE: `[{"1": 130}, {"1": 140}]` → `[{"1": 140}, {"1": 150}]`
- SUBODEN KHAN: `[{"1": 100}]` → `[{"1": 90}]`
- SUPPRESSOR SQUAD: `[{"3": 75}]` → `[{"3": 85}]`
- URIEL VENTRIS: `[{"1": 95}]` → `[{"1": 105}]`
- VANGUARD VETERAN SQUAD WITH JUMP PACKS: `[{"5": 100, "10": 200}, {"5": 110, "10": 210}]` → `[{"5": 105, "10": 210}, {"5": 115, "10": 220}]`
- VICTRIX HONOUR GUARD: `[{"3": 110, "6": 220}, {"3": 130, "6": 240}]` → `[{"3": 110, "6": 230}, {"3": 130, "6": 250}]`
- WARDENS OF ULTRAMAR: `[{"6": 110}]` → `[{"6": 120}]`

**Wargear added/removed — investigate-first (3)**
- REDEMPTOR DREADNOUGHT: removed Macro plasma incinerator
- TERMINATOR ASSAULT SQUAD: removed Thunder Hammer
- VICTRIX HONOUR GUARD: removed Banner of Macragge, Blades of honour

**Attach-list changes — investigate-first (2)**
- MARNEUS CALGAR IN ARMOUR OF ANTILOCHUS LEADER: `AGGRESSOR SQUAD, ASSAULT INTERCESSOR SQUAD, ASSAULT SQUAD, BLADEGUARD VETERAN SQUAD, COMMAND SQUAD, COMPANY HEROES, ERADICATOR SQUAD, HEAVY INTERCESSOR SQUAD, INFERNUS SQUAD, INTERCESSOR SQUAD, RELIC TERMINATOR SQUAD, STERNGUARD VETERAN SQUAD, TACTICAL SQUAD, TERMINATOR ASSAULT SQUAD, TERMINATOR SQUAD, VANGUARD VETERAN SQUAD, VICTRIX HONOUR GUARD` → `AGGRESSOR SQUAD, ASSAULT INTERCESSOR SQUAD, ASSAULT SQUAD, BLADEGUARD VETERAN SQUAD, COMMAND SQUAD, COMPANY HEROES, ERADICATOR SQUAD STERNGUARD VETERAN SQUAD, HEAVY INTERCESSOR SQUAD, INFERNUS SQUAD, INTERCESSOR SQUAD, RELIC TERMINATOR SQUAD, TACTICAL SQUAD, TERMINATOR ASSAULT SQUAD, TERMINATOR SQUAD, VANGUARD VETERAN SQUAD, VICTRIX HONOUR GUARD`
- URIEL VENTRIS LEADER: `ASSAULT INTERCESSOR SQUAD, ASSAULT SQUAD, BLADEGUARD VETERAN SQUAD, COMMAND SQUAD, COMPANY HEROES, INTERCESSOR SQUAD, STERNGUARD VETERAN SQUAD, TACTICAL SQUAD, VANGUARD VETERAN SQUAD` → `ASSAULT INTERCESSOR SQUAD, ASSAULT SQUAD, BLADEGUARD VETERAN SQUAD, COMMAND SQUAD, COMPANY HEROES, INTERCESSOR SQUAD, STERNGUARD VETERAN SQUAD, TACTICAL SQUAD, VANGUARD VETERAN SQUAD, VICTRIX HONOUR GUARD`

**Detachments — investigate-first**
- Added (1): VENGEFUL HOSTS

**Detachment force disposition / unique tag changed — investigate-first (8)**
- 1ST COMPANY TASK FORCE: force_disposition PRIORITY ASSETS→PURGE THE FOE
- EMPEROR'S SHIELD: force_disposition PRIORITY ASSETS→PURGE THE FOE
- FIRESTORM ASSAULT FORCE: force_disposition PURGE THE FOE→PRIORITY ASSETS
- FORGEFATHER'S SEEKERS: force_disposition PURGE THE FOE→PRIORITY ASSETS
- FULGURIS TASK FORCE: force_disposition DISRUPTION→RECONNAISSANCE
- HAMMER OF AVERNII: force_disposition PRIORITY ASSETS→PURGE THE FOE
- IRONSTORM SPEARHEAD: force_disposition PURGE THE FOE→TAKE AND HOLD
- SUBVERSION ASSETS: force_disposition RECONNAISSANCE→DISRUPTION

**Enhancements repriced — adopt-mechanically (5)**
- BLADE OF ULTRAMAR: Armour of Antoninus 10 pts → 20 pts
- GLADIUS TASK FORCE: Artificer Armour 10 pts → 20 pts
- IRONSTORM SPEARHEAD: The Flesh Is Weak 10 pts → 20 pts
- LIBRARIUS CONCLAVE: Fusillade 20 pts → 25 pts
- LIBRARIUS CONCLAVE: Temporal Corridor 15 pts → 25 pts


## Black Templars

`MFM_Black_Templars_v1_0.txt` (90 units, 19 detachments) vs `MFM_Black_Templars_v1.1.txt` (90 units, 20 detachments). **22 adopt-mechanically, 9 investigate-first.**

**Points changed — adopt-mechanically (20)**
- AGGRESSOR SQUAD: `[{"3": 90, "6": 180}, {"3": 100, "6": 190}]` → `[{"3": 80, "6": 165}, {"3": 90, "6": 175}]`
- CHAPLAIN GRIMALDUS: `[{"4": 110}]` → `[{"4": 100}]`
- CRUSADE ANCIENT: `[{"1": 45}]` → `[{"1": 40}]`
- DROP POD: `[{"1": 70}]` → `[{"1": 60}, {"1": 70}]` (mode single→esc4)
- EMPEROR’S CHAMPION: `[{"1": 100}]` → `[{"1": 90}]`
- ERADICATOR SQUAD WITH HEAVY BOLTERS: `[{"3": 70}, {"3": 80}]` → `[{"3": 80}]` (mode split→single)
- EXECRATOR: `[{"1": 60}]` → `[{"1": 50}]`
- HIGH MARSHAL HELBRECHT: `[{"1": 120}]` → `[{"1": 110}]`
- IMPULSOR: `[{"1": 85}]` → `[{"1": 75}, {"1": 85}]` (mode single→esc4)
- INCEPTOR SQUAD: `[{"3": 120, "6": 240}, {"3": 135, "6": 255}]` → `[{"3": 125}, {"3": 140}]`
- INFERNUS SQUAD: `[{"5": 85, "10": 170}]` → `[{"5": 85, "10": 180}]`
- LAND SPEEDER: `[{"1": 95}, {"1": 105}]` → `[{"1": 105}]` (mode split→single)
- LIEUTENANT WITH COMBI-WEAPON: `[{"1": 85}]` → `[{"1": 95}]`
- MARSHAL: `[{"1": 80}, {"1": 90}]` → `[{"1": 80}, {"1": 90}]` (mode esc1→split)
- RAZORBACK: `[{"1": 95}]` → `[{"1": 85}, {"1": 95}]` (mode single→esc4)
- REPULSOR EXECUTIONER: `[{"1": 245}, {"1": 265}]` → `[{"1": 255}, {"1": 275}]`
- RHINO: `[{"1": 75}]` → `[{"1": 65}, {"1": 75}]` (mode single→esc4)
- STORM SPEEDER HAMMERSTRIKE: `[{"1": 130}, {"1": 140}]` → `[{"1": 140}, {"1": 150}]`
- SUPPRESSOR SQUAD: `[{"3": 75}]` → `[{"3": 85}]`
- VANGUARD VETERAN SQUAD WITH JUMP PACKS: `[{"5": 100, "10": 200}, {"5": 110, "10": 210}]` → `[{"5": 105, "10": 210}, {"5": 115, "10": 220}]`

**Wargear added/removed — investigate-first (2)**
- REDEMPTOR DREADNOUGHT: removed Macro plasma incinerator
- TERMINATOR ASSAULT SQUAD: removed Thunder Hammer

**Detachments — investigate-first**
- Added (1): VENGEFUL HOSTS

**Detachment force disposition / unique tag changed — investigate-first (6)**
- FIRESTORM ASSAULT FORCE: force_disposition PURGE THE FOE→PRIORITY ASSETS
- FULGURIS TASK FORCE: force_disposition DISRUPTION→RECONNAISSANCE
- GODHAMMER ASSAULT FORCE: force_disposition DISRUPTION→PURGE THE FOE
- IRONSTORM SPEARHEAD: force_disposition PURGE THE FOE→TAKE AND HOLD
- SUBVERSION ASSETS: force_disposition RECONNAISSANCE→DISRUPTION
- THE LIVING MIRACLE: force_disposition PURGE THE FOE→DISRUPTION

**Enhancements repriced — adopt-mechanically (2)**
- GLADIUS TASK FORCE: Artificer Armour 10 pts → 20 pts
- IRONSTORM SPEARHEAD: The Flesh Is Weak 10 pts → 20 pts


## Blood Angels

`MFM_Blood_Angels_v1_0.txt` (109 units, 23 detachments) vs `MFM_Blood_Angels_v1.1.txt` (109 units, 24 detachments). **19 adopt-mechanically, 8 investigate-first.**

**Points changed — adopt-mechanically (15)**
- AGGRESSOR SQUAD: `[{"3": 90, "6": 180}, {"3": 100, "6": 190}]` → `[{"3": 80, "6": 165}, {"3": 90, "6": 175}]`
- DROP POD: `[{"1": 70}]` → `[{"1": 60}, {"1": 70}]` (mode single→esc4)
- ERADICATOR SQUAD WITH HEAVY BOLTERS: `[{"3": 70}, {"3": 80}]` → `[{"3": 80}]` (mode split→single)
- IMPULSOR: `[{"1": 80}]` → `[{"1": 70}, {"1": 80}]` (mode single→esc4)
- INCEPTOR SQUAD: `[{"3": 120, "6": 240}, {"3": 135, "6": 255}]` → `[{"3": 125, "6": 250}, {"3": 140, "6": 265}]`
- INFERNUS SQUAD: `[{"5": 85, "10": 170}]` → `[{"5": 85, "10": 180}]`
- LAND SPEEDER: `[{"1": 95}, {"1": 105}]` → `[{"1": 105}]` (mode split→single)
- LIBRARIAN: `[{"1": 60}]` → `[{"1": 70}, {"1": 80}]` (mode single→split)
- LIEUTENANT WITH COMBI-WEAPON: `[{"1": 85}]` → `[{"1": 95}]`
- RAZORBACK: `[{"1": 95}]` → `[{"1": 85}, {"1": 95}]` (mode single→esc4)
- RHINO: `[{"1": 75}]` → `[{"1": 65}, {"1": 75}]` (mode single→esc4)
- STERNGUARD VETERAN SQUAD: `[{"5": 100, "10": 190}]` → `[{"5": 100, "10": 200}]`
- STORM SPEEDER HAMMERSTRIKE: `[{"1": 130}, {"1": 140}]` → `[{"1": 140}, {"1": 150}]`
- SUPPRESSOR SQUAD: `[{"3": 75}]` → `[{"3": 85}]`
- VANGUARD VETERAN SQUAD WITH JUMP PACKS: `[{"5": 105, "10": 210}, {"5": 115, "10": 220}]` → `[{"5": 110, "10": 220}, {"5": 120, "10": 230}]`

**Wargear added/removed — investigate-first (2)**
- REDEMPTOR DREADNOUGHT: removed Macro plasma incinerator
- TERMINATOR ASSAULT SQUAD: removed Thunder Hammer

**Detachments — investigate-first**
- Added (1): VENGEFUL HOSTS

**Detachment force disposition / unique tag changed — investigate-first (5)**
- 1ST COMPANY TASK FORCE: force_disposition PRIORITY ASSETS→PURGE THE FOE
- FIRESTORM ASSAULT FORCE: force_disposition PURGE THE FOE→PRIORITY ASSETS
- FULGURIS TASK FORCE: force_disposition DISRUPTION→RECONNAISSANCE
- IRONSTORM SPEARHEAD: force_disposition PURGE THE FOE→TAKE AND HOLD
- SUBVERSION ASSETS: force_disposition RECONNAISSANCE→DISRUPTION

**Enhancements repriced — adopt-mechanically (4)**
- GLADIUS TASK FORCE: Artificer Armour 10 pts → 20 pts
- IRONSTORM SPEARHEAD: The Flesh Is Weak 10 pts → 20 pts
- LIBRARIUS CONCLAVE: Fusillade 20 pts → 25 pts
- LIBRARIUS CONCLAVE: Temporal Corridor 15 pts → 25 pts


## Dark Angels

`MFM_Dark_Angels_v1_0.txt` (103 units, 23 detachments) vs `MFM_Dark_Angels_v1.1.txt` (103 units, 24 detachments). **29 adopt-mechanically, 9 investigate-first.**

**Points changed — adopt-mechanically (24)**
- AGGRESSOR SQUAD: `[{"3": 90, "6": 180}, {"3": 100, "6": 190}]` → `[{"3": 80, "6": 165}, {"3": 90, "6": 175}]`
- DEATHWING KNIGHTS: `[{"5": 240}, {"5": 260}]` → `[{"5": 240}, {"5": 260}]` (mode esc1→split)
- DROP POD: `[{"1": 70}]` → `[{"1": 60}, {"1": 70}]` (mode single→esc4)
- ERADICATOR SQUAD WITH HEAVY BOLTERS: `[{"3": 70}, {"3": 80}]` → `[{"3": 80}]` (mode split→single)
- IMPULSOR: `[{"1": 80}]` → `[{"1": 70}, {"1": 80}]` (mode single→esc4)
- INCEPTOR SQUAD: `[{"3": 120, "6": 240}, {"3": 135, "6": 255}]` → `[{"3": 125}, {"3": 140}]`
- INFERNUS SQUAD: `[{"5": 85, "10": 170}]` → `[{"5": 85, "10": 180}]`
- INNER CIRCLE COMPANIONS: `[{"3": 80, "6": 170}, {"3": 90, "6": 180}]` → `[{"3": 80, "6": 160}, {"3": 90, "6": 170}]`
- LAND SPEEDER: `[{"1": 95}, {"1": 105}]` → `[{"1": 105}]` (mode split→single)
- LAND SPEEDER VENGEANCE: `[{"1": 120}, {"1": 130}]` → `[{"1": 130}, {"1": 140}]`
- LIBRARIAN: `[{"1": 60}]` → `[{"1": 70}, {"1": 80}]` (mode single→split)
- LIEUTENANT WITH COMBI-WEAPON: `[{"1": 85}]` → `[{"1": 95}]`
- LION EL’JONSON: `[{"1": 285}]` → `[{"1": 265}]`
- NEPHILIM JETFIGHTER: `[{"1": 195}]` → `[{"1": 180}]`
- RAVENWING BLACK KNIGHTS: `[{"3": 75, "6": 150}, {"3": 85, "6": 160}]` → `[{"3": 75, "6": 150}]` (mode split→single)
- RAVENWING COMMAND SQUAD: `[{"3": 115}, {"3": 125}]` → `[{"3": 105}, {"3": 115}]`
- RAVENWING DARKSHROUD: `[{"1": 80}]` → `[{"1": 70}]`
- RAZORBACK: `[{"1": 95}]` → `[{"1": 85}, {"1": 95}]` (mode single→esc4)
- RHINO: `[{"1": 75}]` → `[{"1": 65}, {"1": 75}]` (mode single→esc4)
- SAMMAEL: `[{"1": 105}]` → `[{"1": 95}]`
- STERNGUARD VETERAN SQUAD: `[{"5": 100, "10": 190}]` → `[{"5": 100, "10": 200}]`
- STORM SPEEDER HAMMERSTRIKE: `[{"1": 130}, {"1": 140}]` → `[{"1": 140}, {"1": 150}]`
- SUPPRESSOR SQUAD: `[{"3": 75}]` → `[{"3": 85}]`
- VANGUARD VETERAN SQUAD WITH JUMP PACKS: `[{"5": 100, "10": 200}, {"5": 110, "10": 210}]` → `[{"5": 105, "10": 210}, {"5": 115, "10": 220}]`

**Wargear added/removed — investigate-first (2)**
- REDEMPTOR DREADNOUGHT: removed Macro plasma incinerator
- TERMINATOR ASSAULT SQUAD: removed Thunder Hammer

**Detachments — investigate-first**
- Added (1): VENGEFUL HOSTS

**Detachment force disposition / unique tag changed — investigate-first (6)**
- 1ST COMPANY TASK FORCE: force_disposition PRIORITY ASSETS→PURGE THE FOE
- FIRESTORM ASSAULT FORCE: force_disposition PURGE THE FOE→PRIORITY ASSETS
- FULGURIS TASK FORCE: force_disposition DISRUPTION→RECONNAISSANCE
- INTERROGATION CONCLAVE: force_disposition PURGE THE FOE→TAKE AND HOLD
- IRONSTORM SPEARHEAD: force_disposition PURGE THE FOE→TAKE AND HOLD
- SUBVERSION ASSETS: force_disposition RECONNAISSANCE→DISRUPTION

**Enhancements repriced — adopt-mechanically (5)**
- GLADIUS TASK FORCE: Artificer Armour 10 pts → 20 pts
- IRONSTORM SPEARHEAD: The Flesh Is Weak 10 pts → 20 pts
- LIBRARIUS CONCLAVE: Fusillade 20 pts → 25 pts
- LIBRARIUS CONCLAVE: Temporal Corridor 15 pts → 25 pts
- LION'S BLADE TASK FORCE: Stalwart Champion 25 pts → 15 pts


## Deathwatch

`MFM_Death_Watch_v1_0.txt` (89 units, 16 detachments) vs `MFM_Death_Watch_v1.1.txt` (89 units, 17 detachments). **19 adopt-mechanically, 9 investigate-first.**

**Points changed — adopt-mechanically (15)**
- AGGRESSOR SQUAD: `[{"3": 90, "6": 180}, {"3": 100, "6": 190}]` → `[{"3": 80, "6": 165}, {"3": 90, "6": 175}]`
- DROP POD: `[{"1": 70}]` → `[{"1": 60}, {"1": 70}]` (mode single→esc4)
- ERADICATOR SQUAD WITH HEAVY BOLTERS: `[{"3": 70}, {"3": 80}]` → `[{"3": 80}]` (mode split→single)
- IMPULSOR: `[{"1": 80}]` → `[{"1": 70}, {"1": 80}]` (mode single→esc4)
- INCEPTOR SQUAD: `[{"3": 120, "6": 240}, {"3": 135, "6": 255}]` → `[{"3": 125}, {"3": 140}]`
- INFERNUS SQUAD: `[{"5": 85, "10": 170}]` → `[{"5": 85, "10": 180}]`
- LAND SPEEDER: `[{"1": 95}, {"1": 105}]` → `[{"1": 105}]` (mode split→single)
- LIBRARIAN: `[{"1": 60}]` → `[{"1": 70}, {"1": 80}]` (mode single→split)
- LIEUTENANT WITH COMBI-WEAPON: `[{"1": 85}]` → `[{"1": 95}]`
- RAZORBACK: `[{"1": 95}]` → `[{"1": 85}, {"1": 95}]` (mode single→esc4)
- RHINO: `[{"1": 75}]` → `[{"1": 65}, {"1": 75}]` (mode single→esc4)
- STERNGUARD VETERAN SQUAD: `[{"5": 100, "10": 190}]` → `[{"5": 100, "10": 200}]`
- STORM SPEEDER HAMMERSTRIKE: `[{"1": 130}, {"1": 140}]` → `[{"1": 140}, {"1": 150}]`
- SUPPRESSOR SQUAD: `[{"3": 75}]` → `[{"3": 85}]`
- VANGUARD VETERAN SQUAD WITH JUMP PACKS: `[{"5": 100, "10": 200}, {"5": 110, "10": 210}]` → `[{"5": 105, "10": 210}, {"5": 115, "10": 220}]`

**Wargear added/removed — investigate-first (2)**
- DEATHWATCH TERMINATOR SQUAD: removed Thunder Hammer
- REDEMPTOR DREADNOUGHT: removed Macro plasma incinerator

**Detachments — investigate-first**
- Added (1): VENGEFUL HOSTS

**Detachment force disposition / unique tag changed — investigate-first (6)**
- 1ST COMPANY TASK FORCE: force_disposition PRIORITY ASSETS→PURGE THE FOE
- BLACK SPEAR TASK FORCE: force_disposition PRIORITY ASSETS→PURGE THE FOE
- FIRESTORM ASSAULT FORCE: force_disposition PURGE THE FOE→PRIORITY ASSETS
- FULGURIS TASK FORCE: force_disposition DISRUPTION→RECONNAISSANCE
- IRONSTORM SPEARHEAD: force_disposition PURGE THE FOE→TAKE AND HOLD
- SUBVERSION ASSETS: force_disposition RECONNAISSANCE→DISRUPTION

**Enhancements repriced — adopt-mechanically (4)**
- GLADIUS TASK FORCE: Artificer Armour 10 pts → 20 pts
- IRONSTORM SPEARHEAD: The Flesh Is Weak 10 pts → 20 pts
- LIBRARIUS CONCLAVE: Fusillade 20 pts → 25 pts
- LIBRARIUS CONCLAVE: Temporal Corridor 15 pts → 25 pts


## Space Wolves

`MFM_Space_Wolves_v1_0.txt` (119 units, 22 detachments) vs `MFM_Space_Wolves_v1.1.txt` (119 units, 23 detachments). **26 adopt-mechanically, 11 investigate-first.**

**Points changed — adopt-mechanically (22)**
- AGGRESSOR SQUAD: `[{"3": 90, "6": 180}, {"3": 100, "6": 190}]` → `[{"3": 80, "6": 165}, {"3": 90, "6": 175}]`
- ARJAC ROCKFIST: `[{"1": 105}]` → `[{"1": 95}]`
- DROP POD: `[{"1": 70}]` → `[{"1": 60}, {"1": 70}]` (mode single→esc4)
- ERADICATOR SQUAD WITH HEAVY BOLTERS: `[{"3": 70}, {"3": 80}]` → `[{"3": 80}]` (mode split→single)
- IMPULSOR: `[{"1": 80}]` → `[{"1": 70}, {"1": 80}]` (mode single→esc4)
- INCEPTOR SQUAD: `[{"3": 120, "6": 240}, {"3": 135, "6": 255}]` → `[{"3": 125}, {"3": 140}]`
- INFERNUS SQUAD: `[{"5": 85, "10": 170}]` → `[{"5": 85, "10": 180}]`
- IRON PRIEST: `[{"1": 55}]` → `[{"1": 50}]`
- LAND SPEEDER: `[{"1": 95}, {"1": 105}]` → `[{"1": 105}]` (mode split→single)
- LIBRARIAN: `[{"1": 60}]` → `[{"1": 70}, {"1": 80}]` (mode single→split)
- LIEUTENANT WITH COMBI-WEAPON: `[{"1": 85}]` → `[{"1": 95}]`
- LOGAN GRIMNAR: `[{"1": 110}]` → `[{"1": 100}]`
- NJAL STORMCALLER: `[{"1": 85}]` → `[{"1": 75}]`
- RAGNAR BLACKMANE: `[{"1": 100}]` → `[{"1": 90}]`
- RAZORBACK: `[{"1": 95}]` → `[{"1": 85}, {"1": 95}]` (mode single→esc4)
- RHINO: `[{"1": 75}]` → `[{"1": 65}, {"1": 75}]` (mode single→esc4)
- STERNGUARD VETERAN SQUAD: `[{"5": 100, "10": 190}]` → `[{"5": 100, "10": 200}]`
- STORM SPEEDER HAMMERSTRIKE: `[{"1": 130}, {"1": 140}]` → `[{"1": 140}, {"1": 150}]`
- SUPPRESSOR SQUAD: `[{"3": 75}]` → `[{"3": 85}]`
- VANGUARD VETERAN SQUAD WITH JUMP PACKS: `[{"5": 100, "10": 200}, {"5": 110, "10": 210}]` → `[{"5": 105, "10": 210}, {"5": 115, "10": 220}]`
- WOLF GUARD TERMINATORS: `[{"5": 150, "10": 300}, {"5": 160, "10": 310}]` → `[{"5": 150, "10": 300}, {"5": 165, "10": 315}]` (mode esc1→split)
- WOLF SCOUTS: `[{"6": 95, "12": 190}, {"6": 105, "12": 200}]` → `[{"6": 90, "12": 180}]` (mode split→single)

**Wargear added/removed — investigate-first (4)**
- REDEMPTOR DREADNOUGHT: removed Macro plasma incinerator
- TERMINATOR ASSAULT SQUAD: removed Thunder Hammer
- THUNDERWOLF CAVALRY: removed Storm Shield
- WOLF GUARD TERMINATORS: removed Storm Shield

**Detachments — investigate-first**
- Added (1): VENGEFUL HOSTS

**Detachment force disposition / unique tag changed — investigate-first (6)**
- 1ST COMPANY TASK FORCE: force_disposition PRIORITY ASSETS→PURGE THE FOE
- CHAMPIONS OF FENRIS: force_disposition PURGE THE FOE→PRIORITY ASSETS
- FIRESTORM ASSAULT FORCE: force_disposition PURGE THE FOE→PRIORITY ASSETS
- FULGURIS TASK FORCE: force_disposition DISRUPTION→RECONNAISSANCE
- IRONSTORM SPEARHEAD: force_disposition PURGE THE FOE→TAKE AND HOLD
- SUBVERSION ASSETS: force_disposition RECONNAISSANCE→DISRUPTION

**Enhancements repriced — adopt-mechanically (4)**
- GLADIUS TASK FORCE: Artificer Armour 10 pts → 20 pts
- IRONSTORM SPEARHEAD: The Flesh Is Weak 10 pts → 20 pts
- LIBRARIUS CONCLAVE: Fusillade 20 pts → 25 pts
- LIBRARIUS CONCLAVE: Temporal Corridor 15 pts → 25 pts


## Chaos Space Marines

`MFM_Chaos_Space_Marines_v1_0.txt` (85 units, 17 detachments) vs `MFM_Chaos_Space_Marines_v1.1.txt` (85 units, 17 detachments). **18 adopt-mechanically, 4 investigate-first.**

**Points changed — adopt-mechanically (17)**
- ABADDON THE DESPOILER: `[{"1": 285}]` → `[{"1": 295}]`
- ACCURSED CULTISTS: `[{"8": 90, "16": 195}, {"8": 110, "16": 215}]` → `[{"8": 90, "16": 195}, {"8": 110, "16": 215}]` (mode esc1→split)
- CHAOS LORD WITH JUMP PACK: `[{"1": 90}]` → `[{"1": 80}]`
- CHAOS PREDATOR ANNIHILATOR: `[{"1": 135}, {"1": 145}]` → `[{"1": 145}, {"1": 155}]`
- CHAOS PREDATOR DESTRUCTOR: `[{"1": 140}, {"1": 150}]` → `[{"1": 150}, {"1": 160}]`
- CHAOS RHINO: `[{"1": 75}]` → `[{"1": 65}, {"1": 75}]` (mode single→esc4)
- CHAOS TERMINATOR SQUAD: `[{"5": 180, "10": 360}]` → `[{"5": 175, "10": 350}]`
- CHOSEN: `[{"5": 125, "10": 250}, {"5": 135, "10": 260}]` → `[{"5": 135, "10": 270}, {"5": 145, "10": 280}]` (mode esc1→split)
- DARK COMMUNE: `[{"5": 90}, {"5": 100}]` → `[{"5": 90}, {"5": 100}]` (mode esc1→split)
- DEFILER: `[{"1": 300}, {"1": 330}]` → `[{"1": 300}, {"1": 340}]`
- HURON BLACKHEART: `[{"1": 120}]` → `[{"1": 130}]`
- MASTERS OF THE MAELSTROM: `[{"5": 135}]` → `[{"5": 145}]`
- MUTILATORS: `[{"3": 180}, {"3": 190}]` → `[{"3": 165}, {"3": 175}]`
- NEMESIS CLAW: `[{"5": 110, "10": 190}]` → `[{"5": 100, "10": 180}]`
- RED CORSAIRS REAVE-CAPTAIN: `[{"1": 70}]` → `[{"1": 60}]`
- VASHTORR THE ARKIFANE: `[{"1": 205}]` → `[{"1": 220}]`
- VENOMCRAWLER: `[{"1": 110}, {"1": 120}]` → `[{"1": 120}, {"1": 130}]`

**Wargear added/removed — investigate-first (2)**
- DEFILER: removed Hades lascannon, Heavy reaper autocannon
- FORGEFIEND: removed Ectoplasma cannon

**Detachment force disposition / unique tag changed — investigate-first (2)**
- MURDERTALON RAIDERS: force_disposition PURGE THE FOE→RECONNAISSANCE
- SOULFORGED WARPACK: force_disposition PURGE THE FOE→TAKE AND HOLD

**Enhancements repriced — adopt-mechanically (1)**
- SOULFORGED WARPACK: Tempting Addendum 25 pts → 40 pts


## Death Guard

`MFM_Death_Guard_v1_0.txt` (41 units, 9 detachments) vs `MFM_Death_Guard_v1.1.txt` (41 units, 9 detachments). **5 adopt-mechanically, 2 investigate-first.**

**Points changed — adopt-mechanically (5)**
- CHAOS RHINO: `[{"1": 85}]` → `[{"1": 75}, {"1": 85}]` (mode single→esc4)
- DEATHSHROUD TERMINATORS: `[{"3": 160, "6": 320}, {"3": 170, "6": 330}]` → `[{"3": 160, "6": 305}, {"3": 170, "6": 315}]`
- DEFILER: `[{"1": 290}, {"1": 320}]` → `[{"1": 300}, {"1": 340}]`
- MORTARION: `[{"1": 400}]` → `[{"1": 390}]`
- PLAGUE MARINES: `[{"5": 90, "7": 125, "10": 190}]` → `[{"5": 90, "7": 125, "10": 180}]`

**Wargear added/removed — investigate-first (1)**
- DEFILER: removed Hades lascannon, Heavy reaper autocannon

**Detachment force disposition / unique tag changed — investigate-first (1)**
- CONTAGION ENGINES: force_disposition PURGE THE FOE→RECONNAISSANCE


## Chaos Daemons

`MFM_Chaos_Daemons_v1_0.txt` (63 units, 9 detachments) vs `MFM_Chaos Daemons_v1.1.txt` (63 units, 9 detachments). **9 adopt-mechanically, 1 investigate-first.**

**Points changed — adopt-mechanically (6)**
- BEASTS OF NURGLE: `[{"1": 70, "2": 140}]` → `[{"1": 75, "2": 140}]`
- BLOODCRUSHERS: `[{"3": 95, "6": 180}, {"3": 105, "6": 190}]` → `[{"3": 95, "6": 190}, {"3": 115, "6": 210}]`
- FLUXMASTER: `[{"1": 80}]` → `[{"1": 70}]`
- KAIROS FATEWEAVER: `[{"1": 295}]` → `[{"1": 305}]`
- LORD OF CHANGE: `[{"1": 300}, {"1": 315}]` → `[{"1": 320}, {"1": 340}]`
- SHALAXI HELBANE: `[{"1": 340}]` → `[{"1": 315}]`

**Detachment force disposition / unique tag changed — investigate-first (1)**
- LORDS OF THE WARP: force_disposition PURGE THE FOE→TAKE AND HOLD

**Enhancements repriced — adopt-mechanically (3)**
- SCINTILLATING LEGION: Inescapable Eye 10 pts → 15 pts
- SCINTILLATING LEGION: Infernal Puppeteer 25 pts → 20 pts
- SCINTILLATING LEGION: Neverblade 20 pts → 25 pts


## Thousand Sons

`MFM_Thousand_Sons_v1_0.txt` (34 units, 9 detachments) vs `MFM_Thousand_Sons_v1.1.txt` (34 units, 9 detachments). **12 adopt-mechanically, 4 investigate-first.**

**Points changed — adopt-mechanically (11)**
- CHAOS PREDATOR ANNIHILATOR: `[{"1": 130}, {"1": 140}]` → `[{"1": 140}, {"1": 150}]`
- CHAOS PREDATOR DESTRUCTOR: `[{"1": 130}, {"1": 140}]` → `[{"1": 140}, {"1": 150}]`
- CHAOS RHINO: `[{"1": 90}]` → `[{"1": 80}, {"1": 90}]` (mode single→esc4)
- DEFILER: `[{"1": 290}, {"1": 320}]` → `[{"1": 300}, {"1": 340}]`
- KAIROS FATEWEAVER: `[{"1": 295}]` → `[{"1": 305}]`
- LORD OF CHANGE: `[{"1": 300}, {"1": 315}]` → `[{"1": 320}, {"1": 340}]`
- SCARAB OCCULT TERMINATORS: `[{"5": 180, "10": 370}, {"5": 195, "10": 385}]` → `[{"5": 180, "10": 385}, {"5": 195, "10": 400}]`
- SEKHETAR ROBOTS: `[{"2": 80, "4": 160}]` → `[{"2": 85, "4": 175}, {"2": 100, "4": 190}]` (mode single→split)
- SORCERER: `[{"1": 85}]` → `[{"1": 85}, {"1": 95}]` (mode single→split)
- TZAANGOR ENLIGHTENED: `[{"3": 45, "6": 90}]` → `[{"3": 50, "6": 90}]`
- TZAANGOR SHAMAN: `[{"1": 60}]` → `[{"1": 65}]`

**Wargear added/removed — investigate-first (1)**
- DEFILER: removed Hades lascannon, Heavy reaper autocannon

**Detachment DP changed — adopt-mechanically (1)**
- HEXWARP THRALLBAND: 2DP → 3DP

**Detachment force disposition / unique tag changed — investigate-first (3)**
- RITUAL OF REGENERATION: force_disposition PURGE THE FOE→TAKE AND HOLD
- SEKHETAR COHORT: force_disposition PRIORITY ASSETS→DISRUPTION
- WARPFORGED CABAL: force_disposition DISRUPTION→PRIORITY ASSETS

