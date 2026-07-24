# Next-session prompt — Session 133

Session 132 shipped **B63** (**D207**): Soul Grinder's god weapon is now gated at the converter,
`units.json` re-banked, four assertions filed. `index.html` stays at **6.5**, assertions **84/84**,
baseline **21/21**. Read `SESSION_HANDOFF_132.md`, then **D207**.

**The render is still unverified.** Before starting B61, confirm with Ryan whether he's eyeballed
the Soul Grinder god-weapon picker yet. If not, that's a five-minute check worth doing first — it's
the only unverified piece of a converter-only fix.

## Turn type

**Parser-only.** `mfm_points_parser.py`, the `units_repro_check.py` fixed point, and new assertions.
No converter changes beyond what the parser's new output requires downstream, no engine, no
`index.html`.

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline). Verify the sixteen S132 hashes in
`SESSION_HANDOFF_132.md`'s Files section before trusting the sync.

## The task: B61 — Plague Legions units are offered to every Death Guard army, ungated

**A live D0 violation on a built faction.** All six Plague Legions units — Beasts of Nurgle, Great
Unclean One, Nurglings, Plaguebearers, Plague Drones, Rotigus — are already in the Death Guard army
in `units.json` and offered with no gate at all. A Death Guard player can field Great Unclean One and
Rotigus under any detachment or none, with no points sub-cap and with Rotigus eligible as Warlord:
three live illegalities stacked on one faction.

**Cause.** Wahapedia carries these six datasheets twice, under faction `CD` and again under `DG` (the
DG copies exist because the TALLYBAND SUMMONERS detachment makes them includable). `mfm_points_parser.py`
reads a unit header as an ALLCAPS line followed by a tier header; `PLAGUE LEGIONS` is followed by a
unit name, so it is correctly not read as a unit — but is not read as anything else either, and the
six units below it flow into the Death Guard block indistinguishable from Plague Marines.

**The work:**

1. Recognise the allied-group section header in `mfm_points_parser.py`. Write it generally, not
   Death-Guard-specific — the same header shape carries **SCINTILLATING LEGIONS** (Thousand Sons),
   **BLOOD LEGIONS** (World Eaters), **LEGIONS OF EXCESS** (Emperor's Children), and **HARLEQUINS** /
   **YNNARI** (Aeldari), even though only the Death Guard six are in scope today.
2. Tag the units below the header with an `allied_group` field (e.g. `"Plague Legions"`) rather than
   silently absorbing them into the parent army.
3. Regenerate, re-bank the `units_repro_check.py` fixed point — same discipline as B63: run the real
   pipeline, diff old against new, confirm the only substantive change is the six units gaining the
   tag, then copy over the committed files.
4. Assertions pinning the allied set per army: the six named units carry `allied_group: "Plague
   Legions"` in the Death Guard block and nowhere else; no other Death Guard unit carries the field;
   the field is absent (or `enforced: false`, per E22a's needs) everywhere the allied group isn't yet
   gated at selection time.

**Not in scope this session:** the six units are tagged but still selectable without a detachment
gate — that gate is **E22a/E22b**, engine work, sequenced after this parser turn lands the marking.
Tagging without gating is not shipping a partial fix; it's the documented first half of a two-part
ticket (E22a folded into B61 for exactly this reason).

**Checked and clean already, so don't re-derive:** `LEGENDS` sections are handled (explicit skip map
in the parser; no Legends unit is in any pool). Space Marines chapter sub-sections split correctly via
the Wahapedia datasheet blocks. An early S130 scan suggesting five Space Wolves Legends leaks was a
false positive from misreading leader-attachment lists as datasheet names — don't rediscover that one.

## Ground rules

* Parser-only. No converter logic changes beyond passing the new field through, no engine, no
  `index.html`.
* Do not rename anything — project name still unsettled.
* Net-new files expected: none.

## After B61

* **S134 — data-only.** E21a: `detachment_effects.json`, hand-authored, keyed `Army|DETACHMENT`,
  effect kinds `battleline` | `forbid` | `unlock` | `warlord`. Author from the rules, **not** from
  `rule_text` — D203 gives three reasons, D204 a fourth.
* **S135 — engine-only.** E21b.
* **S136 — engine-only.** E21c with E22b — this is where B61's tagging finally gets its gate.
* **S137 — UI-only.** E21d.

## Backlog

**8 open:** B61 (this session), P2, E21, E22, B60, B62, E12, B17.

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
* D199's four batched calls remain unreviewed since S127.
* **B62** — the `FALSE` string-literal quirk and missing presence-and-parse assertion over the nine
  CD CSVs — still open, not touched by B63 or B61.
