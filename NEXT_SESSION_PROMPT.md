# Next-session prompt — Session 132

Session 131 was a recovery session (**D205**) that turned up a live D0 violation (**D206**). B61 did
not start and is unchanged. `index.html` stays at **6.5**, assertions **80/80**, baseline **21/21**.
Read `SESSION_HANDOFF_131.md`, then **D205** and **D206**.

## Turn type

**Converter-only.** `convert_to_json.py`, the `Unit_Weapons.csv` source edit it consumes, the
`units_repro_check.py` fixed point, and new assertions. No `index.html`, no parser, no engine.

The `Unit_Weapons.csv` edit is a legitimate hand edit, not a violation of the never-hand-edit rule:
the Chaos Daemons CSVs are hand-built source, not parser output. They never route through
`wahapedia_transform.py` — established at D132 and exercised again at S128 (Be'Lakor, Blue Horrors).

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline). Verify the eight S131 hashes in
`SESSION_HANDOFF_131.md`'s Files section before trusting the sync. Three of them are the rebuilt CSVs
— if any fails, stop, because the rebuild is the only copy that exists.

## The task: B63 — Soul Grinder ships all four god weapons at once

**A live D0 violation on a built faction, shipping today.** `index.html` filters god-conditional
weapons at lines 6580 and 6604 on `w.allegiance_condition`. `convert_to_json.py` never reads the
`Allegiance_Condition` column, so it never reaches `units.json` and the app's filter is dead code.
Soul Grinder therefore offers torrent of burning blood, warp gaze, phlegm bombardment and scream of
despair simultaneously, all flagged as base equipment.

**Ryan's ruling (D206), already given — do not re-ask:** exactly one god weapon is added, set by the
allegiance chosen at list-building. The four become allegiance-tagged conditionals, not base
equipment. Base equipment is Harvester cannon, Iron claw and Warpsword. Warpclaw stays the existing
swap against Warpsword. One god weapon is **added** on top and replaces nothing — the reference
wording is "adds", which is why the datasheet lists seven weapons with four conditional.

**The mapping**, verbatim from `chaos_daemons_reference.md`: Khorne adds torrent of burning blood;
Tzeentch adds warp gaze; Nurgle adds phlegm bombardment; Slaanesh adds scream of despair. Soul Grinder
is the column's only user — D25 and D26 confirm the Daemon Princes take stat modifiers instead and are
detected through the app's hardcoded `GOD_UNITS` set.

**The work:**

1. Restore the `Allegiance_Condition` column to `Unit_Weapons.csv` as a sixteenth column, matching
   `wahapedia_transform.py`'s existing header order (it already writes the column at line 983).
2. Populate the four Soul Grinder rows; clear `is_base_equipment` on those same four.
3. Thread the column through `convert_to_json.py` into the weapons objects as `allegiance_condition`,
   the field name `index.html` already reads and D26 already specifies.
4. Regenerate, re-bank the `units_repro_check.py` fixed point.
5. Confirm on the rendered app that picking each god yields exactly one god weapon. **Ryan must eyeball
   this** — the DOM is not visible from here.

**Assertions — the deliverable as much as the fix:**

1. Soul Grinder carries exactly four weapons with a non-empty `allegiance_condition`, one per god.
2. None of those four is base equipment; Harvester cannon, Iron claw and Warpsword all are.
3. No other unit in any built army carries an `allegiance_condition`.
4. Every `allegiance_condition` value is one of the four god names.

**Watch for:** the `FALSE` string literal (B62). Soul Grinder's Warpclaw is one of the two rows
carrying it. Do not normalise it while editing nearby rows — it is load-bearing for the fixed point
until B62 is done deliberately.

## Ground rules

* Converter-only. No parser, no engine, no `index.html`.
* Do not rename anything — project name still unsettled.
* T2 hashes in this session's handoff Files section for S133 to verify.
* Net-new files expected: none.

## After B63

* **S133 — parser-only.** B61, exactly as scoped in S130's prompt: allied-group section recognition,
  `allied_group` on the six Death Guard units, fixed point regenerated, four assertions. Write the
  recognition generally — the same header shape carries SCINTILLATING LEGIONS, BLOOD LEGIONS, LEGIONS
  OF EXCESS and HARLEQUINS / YNNARI.
* **S134 — data-only.** E21a: `detachment_effects.json`, hand-authored, keyed `Army|DETACHMENT`,
  effect kinds `battleline` | `forbid` | `unlock` | `warlord`. Author from the rules, **not** from
  `rule_text` — D203 gives three reasons, D204 a fourth.
* **S135 — engine-only.** E21b.
* **S136 — engine-only.** E21c with E22b.
* **S137 — UI-only.** E21d.

## Backlog

**9 open:** B63 (this session), B62, B61, P2, E21, E22, B60, E12, B17.

## Standing inputs, neither blocking, worth more now than before

* **A local backup folder** for the GW-derived and GW-text-carrying files — the nine Chaos Daemons
  CSVs, the Wahapedia export, the MFM `.txt` files, the faction web and pack files. The repo cannot
  hold them; S131 lost three and rebuilt them only because `units.json` happened to carry enough.
* **File storage.** The project store is at capacity. `Adeptus_Astartes_Unit_Info.txt` (402K, read by
  no script) and `NR_army_selection_windows__detachments.pdf` (173K) are the cleanest removals. Do not
  delete anything else without checking what reads it first — that is what caused S131.
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard** — S134 authors from
  the rules.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
