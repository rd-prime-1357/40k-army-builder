# B93 — Enhancement bearer eligibility: scope

**Written S240 (D334), scoping-only turn.** Nothing built. Every number below was re-derived this
session from `detachments.json`, `units.json`, `faction_taxonomy.json`, `index.html`,
`Datasheets_keywords.csv`, `Datasheets.csv`, `Enhancements.csv` and `Army_Muster_Rules.txt`
directly. Nothing is carried forward from the B93 backlog entry, from D332's incidental finding of
six names, or from any prior session's prose. Where this document contradicts an earlier figure,
the figure here is the corrected one.

Baseline at open: `--fetch --data-turn`, **36/36 gates pass**, no tier-B skips. All five S239
handoff hashes verified. `repo_check` green — S238's and S239's files are now pushed.

---

## 1. The rule, from the source

`Army_Muster_Rules.txt` (11e core, Fill Your Army Roster → Select Enhancements) is the authority
and we hold it. It states, under "Unless otherwise stated":

- Only **Character** units can be given enhancements. If such a unit has more than one model,
  one Character model in it is chosen to carry the enhancement.
- **Epic Heroes** cannot have enhancements.
- An army cannot include more than one of the same enhancement.
- **Upgrades** are the exception: they *can* be given to non-Character units, and up to three of
  the same Upgrade may be included.

Three of those four are already enforced correctly in `index.html`. `enhancementTypeEligible()`
refuses `unit_type === 'Epic Hero'` outright, `enhancementMaxCopies()` implements the 1-vs-3 split,
and `canAssignEnhancement()` has an ordered reason list with a `bearer_restriction` slot already
wired in from B113.

The gap is the phrase **"unless otherwise stated."** Almost every enhancement in the game states
otherwise, in its own description, and the engine does not read that statement at all.

---

## 2. Population

All 739 enhancement records in `detachments.json`:

| class | records | note |
|---|--:|---|
| carries a bearer-restriction clause | **641** | 363 distinct names, 173 detachments, 13 armies |
| — of which resolvable against held keyword data | 626 | |
| — of which **not** resolvable | 15 | §5 |
| no restriction clause — description empty | 74 | §6, source gap |
| no restriction clause — Chaos Daemons shorthand | 24 | B122, already open |

**87% of all enhancement records carry a bearer restriction.** B113's curated
`ENHANCEMENT_BEARER_RESTRICTIONS` table holds **7** rows. That table was correctly scoped at the
time — it targeted enhancements carrying a `LEADER:` line in the MFM — but the restriction class is
roughly a hundred times wider than that scope.

### 2.1 What the engine gets wrong today

The current rule is `isUpgrade ? true : unitType === 'Character'`. Measured against every record's
own clause, over every army's real unit pool (union rosters resolved through
`faction_taxonomy.json`):

| | records |
|---|--:|
| **over-admits** — engine offers a bearer the clause forbids | **369** |
| no-op — the clause happens to exclude nobody the Character filter already excluded | 257 |

369 records across **237 distinct names and 13 armies**. Mean over-admission is **9.2 illegal
bearers per record**. This is a live D0 violation on the widest surface in the app: an illegal
state is not merely unflagged, it is the default offering.

Per army:

| army | records | with clause | over-admit | zero-admit (§4) | no text |
|---|--:|--:|--:|--:|--:|
| Space Marines | 87 | 84 | 35 | 4 | 3 |
| Blood Angels | 85 | 76 | 37 | 4 | 9 |
| Dark Angels | 85 | 82 | 46 | 10 | 3 |
| Space Wolves | 81 | 72 | 36 | 4 | 9 |
| Black Templars | 67 | 61 | 27 | 4 | 6 |
| Deathwatch | 63 | 60 | 29 | 4 | 3 |
| Chaos Space Marines | 62 | 57 | 37 | 4 | 5 |
| Emperor's Children | 34 | 28 | 27 | 0 | 6 |
| Death Guard | 30 | 26 | 26 | 0 | 4 |
| Drukhari | 30 | 24 | 15 | 0 | 6 |
| Grey Knights | 30 | 21 | 7 | 0 | 9 |
| Thousand Sons | 30 | 28 | 26 | 1 | 2 |
| Chaos Daemons | 29 | 0 | 0 | 0 | 29 |
| World Eaters | 26 | 22 | 21 | 0 | 4 |
| **total** | **739** | **641** | **369** | **35** | **98** |

### 2.2 Upgrades

25 of the 48 `is_upgrade` records carry a clause, and **12 of those over-admit** — the engine
applies no restriction whatsoever to Upgrades, so any of them can go on any unit in the army. This
is the half of Ryan's original report described as "live and reachable today," and it is confirmed.

The remaining 23 Upgrade records carry no clause: 5 Chaos Daemons shorthand, 18 description-empty.

---

## 3. Clause grammar

The restriction text is a **closed vocabulary of 117 distinct strings**, listed in full in §9. It is
regular, but not uniformly so. Feature counts (by record):

| feature | records | example |
|---|--:|---|
| `<keywords> model only` | 608 | `ADEPTUS ASTARTES TERMINATOR model only` |
| `<keywords> unit only` | 22 | `SPEEDER unit only` |
| bare unit name + `only` | 11 | `Lord of Poxes only` |
| `(excluding X models)` | 22 | `CHAOS LORD model only (excluding TERMINATOR and JUMP PACK models)` |
| `A or B` alternation | 22 | `Chaplain or Judiciar model only` |
| `A/B` alternation | 4 | `SORCERER/EXALTED SORCERER model only` |
| `with the X ability` qualifier | 5 | `HERETIC ASTARTES model with the Deep Strike ability only` |

### Traps, each confirmed against the real text

1. **The clause is not the first sentence.** Position within the description: sentence 0 for 439
   records, sentence 1 for 183, sentence 2 for 19. `faction_pack`-sourced records lead with a
   sentence of flavour. A first-sentence heuristic misses 202 records — 27% of the population.

2. **Sentence splitting on `.` alone is wrong.** Thousand Sons' *Unravelled Fates* opens with a
   rhetorical question, so its flavour sentence ends in `?`. Splitting on `[.?!]` recovers it; the
   first pass of this census lost it and reported 640 instead of 641.

3. **Case is not consistent and is not a signal.** `ADEPTUS ASTARTES model only` (107 records,
   Wahapedia-sourced) and `Adeptus Astartes model only` (105, faction-pack-sourced) are the same
   restriction. Any matching must be case-insensitive. Likewise `Wolf priest` for the keyword
   `Wolf Priest`, and curly-vs-straight apostrophes in `Emperor's Children`.

4. **The slash distributes over the shared tail.** `INFANTRY/MOUNTED THOUSAND SONS PSYKER model
   only` means (Infantry **or** Mounted) **and** Thousand Sons **and** Psyker — not "Infantry" or
   "Mounted Thousand Sons Psyker". A naive split on `/` yields an unresolvable token and would
   silently drop the restriction.

5. **`excluding` appears on both sides of `only`.** Both
   `HERETIC ASTARTES model only (excluding Damned models)` and
   `Heretic Astartes Infantry model (excluding Damned models) only` occur in the data.

6. **`only` also appears in flavour and effect text.** Requiring the clause to be a *whole sentence
   terminating* in `only` (optionally followed by a parenthetical) and no longer than 110
   characters cleanly separates restrictions from prose such as Death Guard's *Droning Shroud*
   ("…can only be targeted by ranged attacks if…"). No false positive survives that test across the
   117-string vocabulary — each one was read.

---

## 4. Why this is not a table build — four blockers

**These are the reason this document does not recommend building in the next session.** Each is a
prerequisite, and three of them are separate tickets.

### 4.1 The Character gate must be *replaced*, not AND-ed — a legality precedent

24 records read `Adeptus Astartes Vehicle model only` and are **not** tagged Upgrade (Headhunter
Task Force's *Astartes Tank Ace*, *Gunnery Honours*, *Firestorm Coordinators*,
*Redoubtable Machine Spirit*, in six armies). Only two Character-typed units in the entire dataset
carry the Vehicle keyword, both Grey Knights. So:

- **today**, the engine offers *Astartes Tank Ace* on any Space Marines Character — wrong — and
  refuses it on every tank — also wrong;
- **if the clause is AND-ed onto the Character check**, all 24 become assignable to nobody.

**D334 was decided on that reading, and is REVERSED at D335 — same session.** The reading was
wrong, and the evidence against it was in `detachments.json` all along, in a field this census did
not read.

**D335: the clause NARROWS within the Characters-only default. It does not replace it.** Headhunter
Task Force's own `rule_text` carries a KEYWORDS block: Adeptus Astartes Vehicle units from the army
(excluding Fortifications, Drop Pods, Walkers and units that can Fly) gain the **Tank Ace**
keyword, and **in the Muster Armies step the player may select up to three Tank Ace units to gain
the CHARACTER keyword** — with a Designer's Note stating in as many words that this is what lets
them take Enhancements and be Warlord. The four Vehicle enhancements go to Characters after all.
They are simply Characters the *detachment* creates during mustering, which the app does not model.

The census read enhancement `description` text and the `restrictions` field (null for this
detachment). It did not read `rule_text`. That is the gap that produced D334, and it is the
methodological lesson of this ticket: a bearer-eligibility question cannot be answered from the
enhancement text alone, because the detachment can change who counts as a Character.

The full zero-admit set — records that would have no legal bearer if the clause were enforced
against static data with the Character gate retained:

| clause | army | records | cause |
|---|---|--:|---|
| `Adeptus Astartes Vehicle model only` | 6 SM-family armies | 24 | §4.1 — Tank Ace conferral, B128 |
| `Deathwing model only` | Dark Angels | 4 | §4.2 — chapter keyword stripped |
| `Deathwing model with the Deep Strike ability only` | Dark Angels | 2 | §4.2 |
| `Heretic Astartes Khorne/Tzeentch/Nurgle/Slaanesh model only` | Chaos Space Marines | 4 | §4.3 — mark chosen at mustering |
| `SPAWN unit only` | Thousand Sons | 1 | §4.4 — vocabulary mismatch |

A further **73 records resolve to exactly one legal bearer**. Those are not errors — Drukhari's
`Archon model only` genuinely means one unit — but they are the records where any resolver bug
becomes an unassignable enhancement rather than a mildly wrong list, so they are the right
regression set.

### 4.2 Chapter keywords are stripped from the shared roster — prerequisite, new ticket

Dark Angels' `Deathwing model only` resolves to **zero** eligible Characters. The cause is not the
clause. `Datasheets_keywords.csv` gives Deathwing to `Captain In Terminator Armour`,
`Chaplain In Terminator Armour`, `Librarian In Terminator Armour`, `Ancient In Terminator Armour`
and `Bladeguard Ancient`. Our pipeline strips chapter-specific keywords from the generic
`Adeptus Astartes` block — correctly, because an Ultramarines Captain in Terminator Armour is not
Deathwing — but the Dark Angels block is delta-shaped and never adds them back, and the union
roster serves the stripped generic record.

Measured over the Dark Angels union pool:

| keyword | units carrying it in `units.json` | units the source would give | Characters lost |
|---|--:|--:|--:|
| Deathwing | 8 | 27 | 5 |
| Ravenwing | 7 | 16 | 1 |

This is not confined to B93 — it is wrong for anything that reads keywords in a chapter army — but
B93 is the first consumer that would break visibly. **Banked as B125.** It is very likely the same
shape for the other `complete`-destined chapters and interacts with B90's roster-mode flip; the
B125 scoping turn must census across all chapters rather than assume Dark Angels is the only case.

### 4.3 Marks of Chaos are chosen during list building — prerequisite, new ticket

Chaos Space Marines' Pactbound Zealots detachment rule (`rule_text` in `detachments.json`, read
this session) requires that every non-Epic-Hero Heretic Astartes unit be assigned one of Khorne,
Tzeentch, Nurgle, Slaanesh or Chaos Undivided **when mustering the army**, noted on the roster. The
app does not model this at all. Four enhancements restrict on the resulting keyword.

The mark is a much larger gap than those four records. The same detachment's `restrictions` field
carries two hard legality rules that also depend on it: a Character can only attach to a unit
sharing its mark, and a unit can only embark in a Transport sharing its mark. Neither is enforced,
and neither can be until marks are modelled. **Banked as B126**, sized as a feature (data + engine
+ persistence in the saved list), not as part of B93.

### 4.4 D199 stands directly in the way

`enhancementTypeEligible()` carries an explicit comment (D199) recording that eligibility keys off
`unit_type` and **not** keywords, precisely because keyword lists are unevenly populated —
Rendmaster on Blood Throne carries the single keyword "Deep Strike", and Ravenwing Command Squad's
Character keyword sits on one model group. Re-verified this session: **8 Character-typed units
carry no Character keyword at all**, and **6 Character units have more than one model group**.

B93 has no alternative to reading keywords. So the mechanism must be able to say "this restriction
cannot be evaluated against this unit's data" and fall through to permissive, rather than refusing
— refusing on absent data is how a legal pick gets blocked. Assertion E4b-2 currently holds the
`unit_type` and keyword derivations to agreement wherever keywords *are* populated; that assertion
is the right place to police the fallthrough set, and it must not be allowed to grow silently.

---

## 5. Unresolvable clauses — 15 records

Two tokens cannot be resolved against anything we hold. Both were checked against the raw source,
not inferred:

- **`SPEEDER` — 12 records**, `SPEEDER unit only`, all Upgrades, in six SM-family armies. There is
  **no SPEEDER keyword anywhere in `Datasheets_keywords.csv`** (1,423 distinct keywords; checked
  directly). The ten speeder datasheets each carry only their own name plus Vehicle/Fly/Imperium/
  Ravenwing. Resolution requires a curated unit-name list — of the built roster that is the three
  Storm Speeders plus Land Speeder Vengeance. This is the same "source does not carry the concept"
  shape as B113's Pact of Cursed Pinions, and should be handled the same way: curated, commented,
  and pinned by a census assertion so a future source refresh that *does* add the keyword fails a
  gate rather than passing silently.

- **`Harlequins` — 3 records**, in Drukhari (`Harlequins or Drukhari model only`,
  `Harlequins model only`). Harlequins is not a built faction. Today the clause is harmless
  because no Harlequins unit can be in a list; when Harlequins is built it becomes live. Curate as
  a no-op with a comment, not as an unresolved token.

`SPAWN unit only` (1 record, Thousand Sons) is a third case but a different one: the keyword on the
datasheet is `Chaos Spawn`, and the unit is named `Chaos Spawn Beast`. That is a synonym, resolvable
by a small alias map — but the alias map is itself a hazard, because it is exactly the kind of thing
that quietly grows into an unreviewed translation layer. Recommend one alias entry, commented, with
the census assertion failing on any *new* unresolvable token.

---

## 6. 74 description-empty records — a source gap, not a parser bug

74 records across all 14 armies have `description_source: "none"` and an empty description. Checked,
not assumed:

- **70 of 74 have no name match at all in `Enhancements.csv`**, the Wahapedia enhancement export.
- The 4 that do match (*Swollen with Power*, *Rejuvenating Swarm*, *Periapt of Torments*,
  *Towering Arrogance*) match under a **different detachment name** — the 10th-edition detachment
  that 11th renamed. In each case the *same enhancement name* also appears in this dataset under its
  11th-edition detachment **with** full text, resolved normally. So `detachment_parser.py` is
  behaving correctly by refusing to cross-match on name alone; loosening that would be a mistake.

This is source acquisition — the faction packs and the Wahapedia export between them simply do not
carry rule text for these 74. It caps B93, and it equally caps B99, B119 and B123. **Banked as
B127**, source-acquisition, no build.

---

## 7. Recommended mechanism — for the session *after* the blockers

Not to be built until B125 (chapter keywords) is at least scoped, because enforcement on top of the
current roster data would break legal Dark Angels lists.

**Shape: a resolver, not a curated table.** This is the first population in the project large enough
that curation is the wrong answer — 641 records against B113's 7. The vocabulary is closed at 117
strings and the grammar is small enough to parse completely, so a resolver can be *total*: every
clause either resolves or is named as unresolvable, with nothing in between.

Concretely:

1. **Data turn first.** A post-processor derives, per enhancement record, a structured restriction:
   a list of alternatives (each a conjunctive keyword list), a list of exclusions, an optional
   ability qualifier, and a scope of `model` / `unit` / `bare-name`. It writes into
   `detachments.json` rather than into `index.html`, so the parse is diff-guarded and reproducible
   under `detachments_repro_check.py`. The parser fails loudly on any clause it cannot fully
   tokenise, with a small explicit alias/curation map for the §5 cases.

2. **Engine turn second.** `enhancementBearerEligible()` already exists and is already called from
   the right place in `canAssignEnhancement()` with its own `bearer_restriction` reason. It gains a
   structured-rule branch alongside B113's curated one, and `enhancementTypeEligible()` is changed
   from a gate to a *default*: applied when the record carries no clause, superseded when it does
   (§4.1). Epic Hero stays an unconditional refusal — that one has no "unless otherwise stated."

3. **Assertion, same turn as the data.** `B93-CENSUS`, on the B99-CENSUS / B119-CENSUS pattern:
   re-derive the clause population from `detachments.json` descriptions independently of the parsed
   field, fail on any record whose clause is present but unparsed, and pin the counts in this
   document — 641 / 626 / 15 / 74 / 24. Pin the 35 zero-admit and 73 one-admit records explicitly,
   because those are where a resolver regression turns into an unassignable enhancement.

**Estimated shape:** one scoping turn for B125, then a data turn, then an engine turn, then a
tooling turn. Four sessions, strictly typed. Do not attempt it in fewer.

---

## 8. Decisions

**D334 — REVERSED at D335, same session.** D334 read "unless otherwise stated" as *replacement*:
an enhancement's clause supersedes the Characters-only default. The sole evidence was the 24
Vehicle records, and it does not survive contact with Headhunter Task Force's `rule_text` (§4.1).

**D335 — the clause narrows within the Characters-only default.** Every enhancement still goes to
a Character. Where a clause names something that is not normally a Character, a detachment rule
confers the Character keyword during mustering. Epic Hero remains an unconditional refusal.

Tested against the whole population, not only the Vehicle case. Under the narrowing reading the
**only** non-Upgrade records left with no legal bearer are the 24 Vehicle (explained by Tank Ace,
B128), the 6 Deathwing (B125's data gap) and the 4 Marks of Chaos (B126). Everything else naming a
non-Character-sounding target resolves cleanly: `GREY KNIGHTS WALKER model only` admits 2
(Venerable Dreadnought, Grand Master in Nemesis Dreadknight — genuine Character vehicles) and
`World Eaters Monster model only` admits 2. Narrowing strands nothing that is not already accounted
for by a known gap.

**B123 — decided (Ryan, S240).** Where an Enhancement and equipped wargear both speak to the same
statline cell: show the best **unconditional** value; if a conditional value would be better, show
the unconditional one and mark the cell so the player knows something else is in play. This
generalises past B123 and should be the standing statline rule — print what is always true, flag
what is sometimes better, never print a number the player only sometimes has.

## 9. Full clause vocabulary — 117 strings, 641 records

| records | clause |
|--:|---|
| 107 | ADEPTUS ASTARTES model only |
| 105 | Adeptus Astartes model only |
| 24 | Adeptus Astartes Vehicle model only |
| 18 | PHOBOS model only |
| 17 | Emperor's Children model only |
| 16 | HERETIC ASTARTES model only |
| 14 | GREY KNIGHTS model only |
| 13 | ADEPTUS ASTARTES INFANTRY model only |
| 13 | THOUSAND SONS model only |
| 12 | ADEPTUS ASTARTES MOUNTED model only |
| 12 | CAPTAIN model only |
| 12 | SPEEDER unit only |
| 10 | Adeptus Astartes Psyker model only |
| 10 | ADEPTUS ASTARTES TERMINATOR model only |
| 9 | Adeptus Astartes Terminator model only |
| 8 | DEATH GUARD model only |
| 7 | HERETIC ASTARTES model only (excluding Damned models) |
| 7 | World Eaters model only |
| 6 | Adeptus Astartes Terminator or Gravis model only |
| 6 | Emperor's Children Infantry model only |
| 6 | GRAVIS model only |
| 6 | Gravis model only |
| 6 | INFANTRY PHOBOS unit only |
| 6 | Ravenwing model only |
| 6 | Space Wolves model only |
| 6 | TACTICUS model only |
| 6 | TECHMARINE model only |
| 6 | Techmarine model only |
| 5 | ADEPTUS ASTARTES PSYKER model only |
| 5 | ADEPTUS ASTARTES PSYKER model only (excluding TERMINATOR models) |
| 5 | Archon model only |
| 5 | DRUKHARI model only |
| 5 | Haemonculus model only |
| 5 | Succubus model only |
| 5 | WORLD EATERS model only |
| 4 | Adeptus Astartes Jump Pack model only |
| 4 | Death Company model only |
| 4 | Deathwing model only |
| 4 | HERETIC ASTARTES INFANTRY model only |
| 4 | Malignant Plaguecaster only |
| 4 | Terminator model only |
| 3 | Adeptus Astartes Infantry model only |
| 3 | DARK APOSTLE or DAMNED model only |
| 3 | HERETIC ASTARTES model only (excluding DAMNED models) |
| 3 | HERETIC ASTARTES model with the Deep Strike ability only |
| 3 | Tzaangor Shaman model only |
| 3 | World Eaters Daemon model only |
| 2 | Ancient model only |
| 2 | Chaos Lord Jump Pack model only |
| 2 | Chaos Lord model only |
| 2 | Chaplain model only |
| 2 | CHAPLAIN model only |
| 2 | Chaplain or Judiciar model only |
| 2 | Death Guard Infantry model only |
| 2 | Death Guard model only |
| 2 | Deathwing model with the Deep Strike ability only |
| 2 | EMPEROR'S CHILDREN model only |
| 2 | GREY KNIGHTS INFANTRY model only |
| 2 | Grey Knights Infantry model only |
| 2 | GREY KNIGHTS TERMINATOR model only |
| 2 | Harlequins or Drukhari model only |
| 2 | Heretic Astartes Infantry model (excluding Damned models) only |
| 2 | INFANTRY/MOUNTED THOUSAND SONS PSYKER model only |
| 2 | SORCERER/EXALTED SORCERER model only |
| 2 | Thousand Sons Infantry model only |
| 2 | THOUSAND SONS or Lord of Change model only |
| 2 | World Eaters Monster model only |
| 1 | Adeptus Astartes Ancient model only |
| 1 | Adeptus Astartes Mounted model only |
| 1 | Adeptus Astartes Terminator Captain model only |
| 1 | ADEPTUS ASTARTES unit only |
| 1 | Biologus Putrifier only |
| 1 | Blood Legions or World Eaters model only |
| 1 | Captain, Chaplain or Lieutenant model only |
| 1 | CHAOS LORD model only |
| 1 | CHAOS LORD model only (excluding JUMP PACK models) |
| 1 | CHAOS LORD model only (excluding TERMINATOR and JUMP PACK models) |
| 1 | CHAOS LORD model only (excluding TERMINATOR models) |
| 1 | Crusade Ancient model only |
| 1 | DARK APOSTLE model only |
| 1 | Drukhari model only |
| 1 | Emperor's Children Daemon Prince model only |
| 1 | Emperor's Children or Keeper of Secrets model only |
| 1 | Exalted Sorcerer model only |
| 1 | Great Unclean One only |
| 1 | GREY KNIGHTS WALKER model only |
| 1 | Harlequins model only |
| 1 | HELLBLASTER SQUAD only |
| 1 | Heretic Astartes Khorne model only |
| 1 | HERETIC ASTARTES model (excluding Damned models) only |
| 1 | HERETIC ASTARTES model only (excluding Khorne models) |
| 1 | Heretic Astartes Nurgle model only |
| 1 | Heretic Astartes Slaanesh model only |
| 1 | Heretic Astartes Terminator model only |
| 1 | Heretic Astartes Tzeentch model only |
| 1 | JUMP PACK CHAOS LORD model only |
| 1 | LAND SPEEDER VENGEANCE unit only |
| 1 | Lord Exultant model only |
| 1 | Lord of Poxes only |
| 1 | Lord of Virulence only |
| 1 | Lord on Juggernaut model only |
| 1 | Noxious Blightbringer only |
| 1 | Phobos model only |
| 1 | Plague Surgeon only |
| 1 | RAVENWING FLY unit only |
| 1 | Slaughterbound model only |
| 1 | Sorcerer or Infernal Master model only |
| 1 | SPAWN unit only |
| 1 | TZAANGOR SHAMAN model only |
| 1 | Warpsmith model only |
| 1 | WARPSMITH model only |
| 1 | Watch Master or Captain model only |
| 1 | Watch Master or Techmarine model only |
| 1 | Wolf Guard Battle Leader model only |
| 1 | Wolf priest model only |
| 1 | World Eaters Daemon Prince or World Eaters Mounted model only |
| 1 | World Eaters Infantry model only |

---

## 10. Tickets this document opens

| id | title | type | why it is separate |
|---|---|---|---|
| **B125** | Chapter-specific keywords stripped from union rosters | data; scoping first | Wrong for every keyword consumer, not just B93; prerequisite |
| **B126** | Marks of Chaos not modelled — mark keyword, attachment and Transport restrictions | data + engine; L | A feature in its own right; carries two unenforced D0 rules of its own |
| **B127** | 74 enhancement records with no rule text in any held source | source acquisition | Caps B93, B99, B119 and B123 alike; nothing to build until source exists |
| **B128** | Detachment-conferred keywords at muster time, incl. Tank Ace → Character | data + engine | Found by D335; 28 detachments, 35 conferrals; carries a hard cap of its own |

B93 itself stays open, re-scoped from "engine checks the wrong thing" to the four-turn sequence in
§7, gated on B125.

---

## 11. Addendum (S240, post-D335) — detachment-conferred keywords

Censused after D335 across all 211 detachments' `rule_text`: **28 detachments confer a keyword
during mustering, 35 conferrals in total.** Invisible to the original census because it lives in
`rule_text`, which the census did not read.

| conferred keyword | detachments | shape |
|---|--:|---|
| Character | 1 | Headhunter Task Force — **player selects up to three** Tank Ace units |
| Tank Ace | 6 | automatic, on qualifying Adeptus Astartes Vehicles |
| Heavy Transport | 6 | automatic — Armoured Speartip, Transports with W14+, excluding Fly |
| Entrenched | 6 | Ceramite Sentinels |
| Battleline | 6 | Lost Brethren, Company of Hunters, Shamblerot Vectorium, Chaos Cult, Warpmeld Pact, Cult of Blood — each names specific datasheets |
| Faction keyword | 3 | Tallyband Summoners, Carnival of Excess, and a Thousand Sons equivalent |
| Daemon, Soul Forge | 2 | Cult of the Arkifane |

Headhunter's is the only one that is a **player choice with a hard cap** — "up to three" — and so
the only one that is legality-critical in the D0 sense: a list with four Character Tank Aces is
illegal and must be unreachable. The rest are automatic, and are eligibility or display inputs
rather than choices.

Banked as **B128**. It is a prerequisite for the 24 Vehicle records specifically, not for B93 as a
whole — the other 617 clause-bearing records do not depend on it.
