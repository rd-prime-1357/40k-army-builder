# Session 130 handoff — analysis/scoping: E21 scoped (D203); Ryan's rulings + the Plague Legions leak (D204)

**Turn type: analysis/scoping.** No `index.html`, data file, parser or harness touched. `index.html`
stays at **6.5**, assertions **80/80**, baseline **21/21**. Authoritative write-up is **D203** and **D204** in
`40K_Decision_Log_v3_0.md`. D204 reverses two of D203's three calls — read in that order.

**Baseline: 21/21 at open and unchanged at close.** All nine S129 hashes verified byte-identical.
`repo_check.py` and `BACKLOG_ARCHIVE.md` were both present in the project area this session — S129's
GitHub recovery did not need repeating, and the third-consecutive-session risk S129 flagged has
cleared.

---

## The findings that mattered

**E21's ticket had the problem wrong in the direction that matters.** It has said since S122 that
"34 detachment abilities across the full dump carry require/forbid language, in free prose with no
common shape." Re-derived from source: the dump-wide figure is ~41 real muster-time effects (57 raw
matches less in-battle false positives — charge targets, Combat Drug/Doctrine re-selection bans,
points-limit consequences); nobody can say where 34 came from. More importantly the dump is the wrong
denominator — what governs the app is our **143 built detachment records**, and the shapes there
reduce to four recurring kinds, not free prose.

**25 of those 143 are already enforced and E21 should build nothing for them.** Chapter exclusivity
is the largest cluster, and `resolveUnits()` already makes it unreachable: a chapter army's pool is
the generic Adeptus Astartes block plus that chapter's own units, so a foreign-chapter unit is never
selectable. D0 satisfied by construction. The correct work is a `rules_assertions.py` check pinning
that guarantee, since it is currently an emergent property of one function that nothing polices —
and E22 (allied units) is exactly the change most likely to break it silently.

This also confirmed the prompt's warning against carrying figures forward: the Wahapedia dump shows
22 chapter-exclusivity detachments, our built data has **25**, because the faction-pack markdown
carries three Dark Angels detachments the 10th-Edition dump does not.

**What is actually left is six detachments, two of which are blocked.** Battleline elevation in
Blood Angels|THE LOST BRETHREN, Dark Angels|COMPANY OF HUNTERS and Death Guard|SHAMBLEROT VECTORIUM;
require/forbid in Chaos Daemons|SHADOW LEGION; and two ally-unlock cases moved out to E22. All
targets were verified present in `units.json`.

**Text parsing is the wrong mechanism, provable three ways.** `rule_text` spans three fidelity tiers
(68 `faction_pack`, 66 `wahapedia_10e`, 9 `none`) and the faction-pack tier is a condensed paraphrase
that *disagrees on rule content* — our stored Shadow Legion text says Be'Lakor must be included, which
the Wahapedia text does not state anywhere. Nine built detachments carry no rule text at all, so a
parser emits nothing for them and reports a clean run. And the unit names in the prose do not match
the data: the text forbids "Daemon Prince" and "Daemon Prince with Wings" where `units.json` holds
**Daemon Prince of Chaos** / **Daemon Prince of Chaos with Wings**, and excludes "Be'lakor" where the
data holds **Be'Lakor**. A name-matching parser forbids nothing here while appearing to work — the
worst failure mode a legality tool has, and E4's D199 name-collision finding arriving from the
opposite direction.

**Two data defects found on the way, filed rather than fixed.** `restrictions` is populated for only
12 of 143 records, and of the 25 chapter-exclusivity detachments, 11 hold the text in `restrictions`
while 14 hold the identical sentence in `rule_text` — zero overlap, split by text tier rather than by
content (**B60**). And nothing in the app can name an allied unit set: "Plague Legions", "Heretic
Astartes", "Legions of Excess", "Blood Legions" and "Scintillating Legions" appear nowhere in
`faction_taxonomy.json`, `units.json` or `chaos_daemons_reference.md` (**E22**).

---

## Ryan's rulings, and the finding they turned up

**Be'Lakor — D203 was wrong, reversed.** He is not required by Shadow Legion. He is optional, and *if
included must be the Warlord*; separately the detachment forbids Daemon Prince, Daemon Prince with
Wings and all other Epic Hero units. The faction-pack paraphrase had compressed a conditional Warlord
constraint into an unconditional inclusion requirement — it did not merely lose fidelity, it inverted
the rule's logical shape. That is a fourth reason not to author from `rule_text`, stronger than the
three D203 already gave. Effect kinds become `battleline` | `forbid` | `unlock` | `warlord`;
`require` is dropped, no built detachment needs it.

**Battleline display — D203 was wrong, reversed.** Elevated units render under the Battleline group.
D203's argument was that moving Outrider Squad out of Mounted makes the roster harder to scan; that
is a convenience claim losing to comprehension of a legality-relevant fact, and New Recruit groups
them under Battleline. Cost checked this session: `unit_type` is read at two grouping sites and one
limit site, so all three take a single `effectiveUnitType(unit, selectedDetachments)` helper, live
against the current selection. Cheaper than D203 implied.

**Allied unit sets from named MFM sections — confirmed, with one exception.** The MFM files define
each group as a plain section header followed by that group's units and their in-context points:
**PLAGUE LEGIONS** (Death Guard, line 140 — the six units, running to `DETACHMENTS`), **SCINTILLATING
LEGIONS** (Thousand Sons), **BLOOD LEGIONS** (World Eaters), **LEGIONS OF EXCESS** (Emperor's
Children), **HARLEQUINS** and **YNNARI** (Aeldari). Every god-legion case in the priority factions
plus two Aeldari-family ones, all found the same way. The exception is Shadow Legion:
`MFM_Chaos_Daemons_v1_0.txt` has no HERETIC ASTARTES section — that unlock is an explicit ~15-name
list in the detachment's own text, every name a Chaos Space Marines datasheet, so it waits on CSM.

**The finding: the Plague Legions units are already in the Death Guard pool, ungated.** Checking the
above turned up worse than an unshipped feature. All six sit in the Death Guard army in `units.json`
today with no gate at all — a Death Guard player can field Great Unclean One and Rotigus under any
detachment or none, with no points sub-cap and with Rotigus eligible as Warlord. Three live
illegalities on a built faction. D203 asserted the opposite ("nothing in the app can name an allied
unit set"); the units are there, they are simply unmarked.

Cause: Wahapedia carries these six datasheets twice, under `CD` and again under `DG`.
`mfm_points_parser.py` reads a unit header as an ALLCAPS line followed by a tier header; `PLAGUE
LEGIONS` is followed by a unit name, so it is correctly not read as a unit — and not read as anything
else either, so the six units below it flow into the Death Guard block.

**Not a general leak, and both adjacent worries are clean.** `LEGENDS` is handled — the parser carries
an explicit skip map, and none of Brother Corbulo, Deathwing Command Squad, Canis Wolfborn, Harald
Deathwolf or Death Guard Chaos Lord is in any pool. The Space Marines chapter sub-sections split
correctly via the Wahapedia datasheet blocks: Darnath Lysander is in Imperial Fists and not in the
generic pool, same for Caanok Var, Adrax Agatone and Aethon Shaan. An early crude scan this session
suggested five Space Wolves Legends leaks — a false positive from misreading leader-attachment lists
as datasheet names, recorded so it is not rediscovered as real later.

Filed as **B61**, separate from E22: B61 is *the units are wrongly offered*, E22 is *the unlock,
sub-cap and Warlord ban are enforced*.

---

## Resequenced

B61 is a reachable illegal state on a built faction, which under D0 outranks an enforcement gap that
is merely unshipped, so it goes first. Turn typing forces the rest, since B61's fix is a parser turn.

**S131** parser-only (B61 marking) → **S132** data-only (E21a) → **S133** engine-only (E21b) →
**S134** engine-only (E21c + E22b) → **S135** UI-only (E21d).

E22 is now partly unblocked: its Death Guard half is fully buildable once B61 lands; only Shadow
Legion waits on Chaos Space Marines, already next in the faction priority order.

---

## Decided

**`detachment_effects.json`, hand-authored, keyed on the existing `Army|DETACHMENT` key, guarded by
referential-integrity assertions** — every unit name must resolve against that army's resolved pool,
every detachment key against `detachments.json`. That gate is what makes hand-authoring safe: a typo
fails the baseline by name instead of quietly disabling a restriction. This does not breach *fix
parsers, never hand-edit output files* — that rule protects generated outputs, and this is an input,
in the same class as the two documented `HAND_AUTHORED` exceptions. Recorded in D203 so it is not
re-litigated.

**No separate scope document.** D199 carried E4's whole scope inside the decision log and that
worked; with the file area near capacity a standalone `E21_*_SCOPE.md` costs a file for no benefit.
**Net-new files this session: none** — deliberate.

**The split:** E21a data-only (`detachment_effects.json` + assertions) → E21b engine-only (Battleline
elevation via a predicate consulted by `instanceLimit()`, plus the chapter-exclusivity assertion) →
E21c engine-only (require/forbid) → E21d UI-only (refusal prose, roster warnings, Battleline
indicator). Four turns rather than E4's three because E21 crosses data, engine and UI where E4
crossed two, and turn typing forbids mixing. E21 closes at E21d without waiting on E22.

**Three calls were batched for Ryan; two came back reversed** (see the rulings section above). The
third stands and is reinforced: E22-blocked effects are recorded in data with `enforced: false`
rather than omitted. Had the Plague Legions records existed flagged unenforced, the leak would have
shown up as a contradiction in the data rather than being found by accident.

---

## Still open for Ryan

D199's four batched calls, unreviewed since S127, three now load-bearing in shipped code (D200,
D201). Nothing new is waiting — S130's three calls were all ruled on this session (D204).

---

## Files

**Changed (SHA-256, first 12):**
- `40K_Decision_Log_v3_0.md` — appended D203 and D204 — `9aeebf5ab3f1`
- `DECISION_INDEX.md` — D203 and D204 indexed — `52ab7746196b`
- `OPEN_ITEMS_BACKLOG.md` — E21 rewritten then amended; E22 rewritten; B60 and B61 opened; open count 4→7 — `aabc2003dcee`
- `NEXT_SESSION_PROMPT.md` — S131 (B61, parser-only) — `17674aa80dca`

**Net new:** none.

The handoff does not hash itself. Verify the four above at S131 open per T2.

**Unchanged:** `index.html` (6.5), every `.json` data file, every parser, every harness, `baseline.sh`,
`pipeline_manifest.py`/`.json`.

**Repo custody:** all five files are project-generated prose carrying no GW rules text — short rule
names and unit names only. All repo-eligible; not yet pushed (uploads are batched). Excluded from any
push as always: the Wahapedia CSV export, the MFM `.txt` files, the faction web and pack files,
`Army_Muster_Rules.txt` and `wh40k_core_rules.md`.

---

## Backlog

| | |
|---|---|
| **Beginning** | 4 — P2, E21, E12, B17 |
| **Resolved** | 0 |
| **Added** | 3 — E22, B60, B61 |
| **Ending** | 7 — B61, P2, E21, E22, B60, E12, B17 |
