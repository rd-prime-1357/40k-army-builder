# Next-session prompt — Session 131

Session 130 scoped **E21** (**D203**), then took three rulings from Ryan and found a live bug
(**D204**). `index.html` unchanged at **6.5**, assertions **80/80**, baseline **21/21**. Read
`SESSION_HANDOFF_130.md`, then **D203** and **D204** — D204 reverses two of D203's three calls, so
read them in that order and let D204 win.

## Turn type

**Parser-only.** `mfm_points_parser.py` plus the `units.json` regeneration it produces, the
`units_repro_check.py` fixed point, and new assertions. No `index.html`, no engine, no hand-edited
data.

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline). Verify the four S130 hashes in
`SESSION_HANDOFF_130.md`'s Files section before trusting the sync.

## The task: B61 — the Plague Legions units are offered ungated

**This is a live D0 violation on a built faction, not an unshipped feature.** All six Plague Legions
units — Beasts of Nurgle, Great Unclean One, Nurglings, Plaguebearers, Plague Drones, Rotigus — sit in
the Death Guard army in `units.json` today with no gate. A Death Guard player can field Great Unclean
One and Rotigus under any detachment or none, with no points sub-cap and with Rotigus eligible as
Warlord. That is why this jumped ahead of E21.

**Cause (traced in D204 — verify it, do not re-derive from scratch):** Wahapedia carries these six
datasheets twice, under faction `CD` and again under `DG`. `mfm_points_parser.py` reads a unit header
as an ALLCAPS line followed by a tier header (`is_real_unit_header`); `PLAGUE LEGIONS` at
`MFM_Death_Guard_v1_0.txt` line 140 is followed by a unit name, not a tier, so it is correctly not
read as a unit — but is not read as anything else either, and the six units below it flow into the
Death Guard block indistinguishable from Plague Marines.

**The fix:** teach the parser to recognise an allied-group section header — an ALLCAPS line that is
*not* followed by a tier header, is not one of the known non-group headers (`SUPPORT`, `LEADER`,
`DETACHMENTS`, `ENHANCEMENTS`, `LEGENDS`, `YOUR …`), and sits between unit blocks — and tag every unit
below it, to the next such header or `DETACHMENTS`, with an `allied_group` field carrying the header
verbatim. Regenerate `units.json`; re-bank the `units_repro_check.py` fixed point.

**Generality matters here.** The same header shape carries **SCINTILLATING LEGIONS** (Thousand Sons,
line 134), **BLOOD LEGIONS** (World Eaters, 117), **LEGIONS OF EXCESS** (Emperor's Children, 83) and
**HARLEQUINS** / **YNNARI** (Aeldari, 233 / 266) — every god-legion case in the priority factions plus
two Aeldari-family ones. Only Death Guard is built today, so only six units change, but write the
recognition generally so the four Chaos factions land correctly when they arrive rather than each
needing a parser turn of its own.

**Assertions — the deliverable as much as the parser change is:**

1. The Death Guard `allied_group: "PLAGUE LEGIONS"` set is exactly those six units, no more and no
   fewer.
2. No unit in any other built army carries an `allied_group`.
3. Every unit carrying an `allied_group` also exists in its home faction's block (all six are in
   Chaos Daemons), so a future merge change cannot orphan them.
4. `LEGENDS` stays excluded: none of Brother Corbulo, Deathwing Command Squad, Canis Wolfborn, Harald
   Deathwolf or Death Guard Chaos Lord appears in any pool.

**Do not gate the units in the engine this session.** Marking is B61; gating is E22b at S134. The
units stay offered after S131, so B61's ticket stays open until E22b lands.

## Ground rules

* Parser-only. Fix the parser and regenerate; never hand-edit `units.json`.
* Do not rename anything — project name still unsettled.
* T2 hashes in this session's handoff Files section for S132 to verify.
* Net-new files expected: none.

## After B61

* **S132 — data-only.** E21a: `detachment_effects.json`, hand-authored, keyed `Army|DETACHMENT`,
  effect kinds `battleline` | `forbid` | `unlock` | `warlord` (D204 dropped `require`). Author from
  the rules, **not** from `rule_text` — D203 gives three reasons and D204 adds a fourth: the
  faction-pack paraphrase inverted the logical shape of Shadow Legion's Be'Lakor rule.
* **S133 — engine-only.** E21b: `effectiveUnitType(unit, selectedDetachments)` feeding
  `instanceLimit()` **and** both grouping sites (`groupByType` and the roster `typeGroups` build), so
  an elevated unit renders under Battleline per Ryan's ruling; plus the chapter-exclusivity structural
  assertion.
* **S134 — engine-only.** E21c (forbid + conditional Warlord) with E22b (allied gating, battle-size
  points sub-cap, Warlord ban).
* **S135 — UI-only.** E21d.

## Backlog

**7 open:** B61 (this session), P2, E21, E22, B60, E12, B17.

## Standing inputs, neither blocking, worth more now than before

* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard** — S132 authors from
  the rules, and D203/D204 rule out authoring from stored `rule_text`.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **File storage.** Duplicate-version CSVs are still sitting in the project's underlying knowledge
  store, invisible to the flat file listing — `Unit_Wargear_Options.csv` (16 rows vs. 13),
  `Unit_Weapons.csv` (140 vs. 142), `Rules.csv` (13 vs. 18). Only Ryan can clear them from the
  project's file manager. S130 produced zero net-new files; S131 should too.
