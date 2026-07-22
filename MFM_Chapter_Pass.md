# Cross-Faction MFM Pass — Space Marines (chapters)

Single accumulating report. Baseline = deployed pricing source `mfm_sm.txt`. Chapter datasheet set = that chapter's block in built `units.json`. Two check types: **file-chapters** (own MFM file; conflict + gap-closure) and **generic-chapters** (priced from sections inside `mfm_sm.txt`; coverage + keyword integrity). Conflicts are MFM-vs-MFM and reliable; orphans vs a 10th-ed base may be edition-drift.

> **SUPERSEDED — S101 (D168, B56a).** The closure figures below are no longer the source of
> truth. `rules_assertions.py` B56a-1/B56a-2 now assert the residual null set and the Black
> Templars negative control directly against `units.json`; those are the durable form this
> document warned it needed. This file is kept for the narrative (why the scoping bug existed,
> how it was found) — for current numbers, run `rules_assertions.py`.
>
> **STALE — refreshed S100 (D167).** The figures below were re-derived against current
> `units.json` and the current MFM files. Two of the original findings had drifted inside one
> release: Space Wolves' Venerable Dreadnought has since been costed from the base file, and all
> four vanilla-chapter stragglers (Marneus Calgar in Armour of Antilochus, Wardens of Ultramar,
> Vulkan He'stan, Kor'sarro Khan) are now costed. Chapter files close **77 of 81**, not 78.
> This document has no executable form and will drift again; B56a replaces these numbers with a
> rules assertion.

## Refreshed figures (S100)

| Chapter | Block units | Uncosted today | Closed by chapter MFM | Still open |
|---|---|---|---|---|
| Space Wolves | 21 | 20 | 19 | Wolf Guard Headtakers (B56b) |
| Blood Angels | 15 | 15 | 15 | — |
| Black Templars | 18 | 18 | 17 | Crusader Squad (B56b) |
| Dark Angels | 16 | 16 | 16 | — |
| Deathwatch | 10 | 10 | 10 | — |
| Adeptus Astartes | 82 | 2 | 0 | Judiciar Xacharus, Chaplain Kastiel (B56e — no source) |
| Ultramarines / Iron Hands / Salamanders / Imperial Fists / Raven Guard / White Scars | 19 | 0 | n/a | — |

**Scoping hazard (Black Templars only).** 9 of BT's 18 datasheets share a name with an Adeptus
Astartes datasheet. Parsed unscoped, those rows are written under `Adeptus Astartes` and overwrite
generic base prices while BT stays uncosted — 8 of 18 arm correctly. All other chapters misfile zero.

**Per-chapter overrides on shared generic datasheets (D42):** 11 rows — Blood Angels 8, Space Wolves
1, Dark Angels 1, Deathwatch 1. BT's three price disagreements are *not* overrides; Impulsor,
Repulsor Executioner and Sternguard Veteran Squad are BT-owned datasheets with their own IDs.

**Leader-list side effect:** none. Chapter runs patch 0 `Leader Eligible Units` cells.

---

## Original pass (superseded above)

## Summary
| Chapter | Points source | Block units | Costed | Uncosted | Conflicts |
|---|---|---|---|---|---|
| Space Wolves | own file | 21 | 20 | 1 | 0 |
| Blood Angels | own file | 15 | 15 | 0 | 0 |
| Black Templars | own file | 18 | 17 | 1 | 0 |
| Dark Angels | own file | 16 | 16 | 0 | 0 |
| Deathwatch | own file | 10 | 10 | 0 | 0 |
| Ultramarines | mfm_sm section | 8 | 6 | 2 | n/a |
| Iron Hands | mfm_sm section | 2 | 2 | 0 | n/a |
| Salamanders | mfm_sm section | 2 | 1 | 1 | n/a |
| Imperial Fists | mfm_sm section | 3 | 3 | 0 | n/a |
| Raven Guard | mfm_sm section | 2 | 2 | 0 | n/a |
| White Scars | mfm_sm section | 2 | 1 | 1 | n/a |

## File-chapters (own MFM)

### Space Wolves
- Block units (all uncosted from generic MFM): **21**; chapter MFM closes **20/21**; conflicts **0**.
- Still uncosted (name mismatch / absent): Wolf Guard Headtakers

### Blood Angels
- Block units (all uncosted from generic MFM): **15**; chapter MFM closes **15/15**; conflicts **0**.

### Black Templars
- Block units (all uncosted from generic MFM): **18**; chapter MFM closes **17/18**; conflicts **0**.
- Still uncosted (name mismatch / absent): Crusader Squad

### Dark Angels
- Block units (all uncosted from generic MFM): **16**; chapter MFM closes **16/16**; conflicts **0**.

### Deathwatch
- Block units (all uncosted from generic MFM): **10**; chapter MFM closes **10/10**; conflicts **0**.

## Generic-chapters (priced inside mfm_sm.txt)

### Ultramarines
- Chapter-specific block units (keyword-scoped): **8**; costed from mfm_sm section: **6/8**.
- UNCOSTED (MFM section name vs datasheet name mismatch): Marneus Calgar in Armour of Antilochus, Wardens of Ultramar

### Iron Hands
- Chapter-specific block units (keyword-scoped): **2**; costed from mfm_sm section: **2/2**.
- Clean: all chapter units costed and keyword-scoped correctly.

### Salamanders
- Chapter-specific block units (keyword-scoped): **2**; costed from mfm_sm section: **1/2**.
- UNCOSTED (MFM section name vs datasheet name mismatch): Vulkan He’stan

### Imperial Fists
- Chapter-specific block units (keyword-scoped): **3**; costed from mfm_sm section: **3/3**.
- Clean: all chapter units costed and keyword-scoped correctly.

### Raven Guard
- Chapter-specific block units (keyword-scoped): **2**; costed from mfm_sm section: **2/2**.
- Clean: all chapter units costed and keyword-scoped correctly.

### White Scars
- Chapter-specific block units (keyword-scoped): **2**; costed from mfm_sm section: **1/2**.
- UNCOSTED (MFM section name vs datasheet name mismatch): Kor’sarro Khan

