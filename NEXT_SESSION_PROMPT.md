# Next-session prompt — Session 135

Session 134 shipped **E21a** (**D209**): `detachment_effects.json` is net new and holds seven effects
across five detachments on D204's four-kind schema, with assertions **E21a-1** through **E21a-6** and
the file added to the manifest's guarded set (38 → 39 files). `index.html` stays at **6.5**, assertions
**94/94**, baseline **21/21**. Read `SESSION_HANDOFF_134.md`, then **D209**, then **D210**.

**One new ticket: E23.** Re-deriving E21's survey from source found a seventh construction effect
D203 missed — `HEADHUNTER TASK FORCE`'s Tank Ace → Character keyword grant, live on six built armies,
where the app currently refuses a legal enhancement. Over-restriction, not a D0 violation, so it does
not jump the queue. Not this session's work.

## Turn type

**Engine-only.** `index.html` only. No parser, no converter, no data file, no JSON regeneration.

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline). Verify the S134 hashes in `SESSION_HANDOFF_134.md`'s
Files section before trusting the sync — `detachment_effects.json` is hand-authored and no repro gate
can regenerate it, so its hash is the only thing that catches a bad sync.

## The task: E21b — `effectiveUnitType()`

Load `detachment_effects.json` alongside the other runtime data and add a single helper,
`effectiveUnitType(unit, selectedDetachments)`, returning `'Battleline'` when any selected
detachment's `battleline` effect names that unit and the unit's own `unit_type` otherwise.

**Three call sites, per D204's ruling 2**, all of which must switch to the helper:

1. `instanceLimit()` — the count cap (Battleline doubles it).
2. `groupByType` — the left-panel grouping.
3. The roster's `typeGroups` build.

**Do not overwrite `unit_type` on the record.** The elevation is live against the current detachment
selection: deselecting the detachment must move the unit back to its own group and restore its cap.
D204 reversed D203 here — elevated units render **under Battleline**, not in their own group with a
badge, because that is what New Recruit does and because the status change is legality-relevant.

**Effects from multiple selected detachments union** — a unit elevated by any selected detachment is
elevated (D203, unchanged by D204).

Only the three `battleline` rows are in scope. `forbid`, `unlock` and `warlord` are E21c/E22b.

## Also this session: the chapter-exclusivity structural assertion

The other half of E21b. 25 built detachments say *your army may include this Chapter's units and no
other Chapter's*, and `resolveUnits()` already makes that unreachable by composing a chapter army as
the generic Adeptus Astartes block plus that chapter's own units. Nothing polices it. Add the
assertion: for every faction in the taxonomy, the resolved unit set contains no unit sourced from
another chapter's army block. `Sources.resolved_pool()` in `rules_assertions.py` already mirrors the
composition rule and is the natural place to build from.

Add a harness (`e21b_check.js`) in the mould of `e1b_check.js` / `e4b_check.js` covering the helper
itself: elevation on, elevation off after deselect, union across two selected detachments, and the
doubled cap.

## Ground rules

* Engine-only. `index.html` and a new harness; no data file touched.
* Do not rename anything — project name still unsettled.
* `detachment_effects.json` is a hand-authored **input**. Never edit it to make the engine pass.

## After E21b

* **S136 — engine-only.** E21c with E22b — Shadow Legion's forbid path, Death Guard's Plague Legions
  unlock gate (consuming B61's `allied_group` tag), the points sub-cap, and the Warlord ban.
* **S137 — UI-only.** E21d: refusal prose, roster warnings, Battleline indicator.
* **E23** — scoping turn, unsequenced.

## Backlog

**8 open:** B62, P2, E21 (E21a shipped; b/c/d remain), E22 (E22a done, E22b remains), E23, B60, E12,
B17.

## Standing inputs, neither blocking, worth more now than before

* **A local backup folder** for the GW-derived and GW-text-carrying files — the nine Chaos Daemons
  CSVs, the Wahapedia export, the MFM `.txt` files, the faction web and pack files. The repo cannot
  hold them; S131 lost three and rebuilt them only because `units.json` happened to carry enough.
  D210 sharpens this: the mount cannot be trusted to tell us whether a file is still there.
* **The project file area is near capacity.** E21a cost one 7.6 KB file. E21b costs one harness.
  Beyond that, a plan is needed — see the handoff's note.
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard**.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now eight sessions.**
* **B62** — the `FALSE` string-literal quirk and missing presence-and-parse assertion over the nine
  CD CSVs — still open, untouched since D205.
