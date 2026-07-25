# Next-session prompt — Session 140

Session 139 shipped **E21d piece 3** (**D218**), closing the **E21** arc. A unit stranded by a later
change — its unlocking detachment deselected or switched away, its allied group over the sub-cap
after a battle-size drop, or a forbidden unit seated by import — now reads as a visible roster error
(`entryAlliedError`, wired into `entryHasError`), never silently trimmed or blocked. Ryan's ruling:
a quick detachment switch-and-back must leave the list intact, and the same treatment is the tool's
standing answer for the whole "was-legal, a-later-choice-made-it-illegal" class (enhancement
over-states included). Engine-only turn; `index.html` 6.8 -> 6.9. Read `SESSION_HANDOFF_139.md`, then
**D218**.

## Baseline at open

Verify the eight S139 hashes in the handoff's Files section byte-for-byte, then run `./baseline.sh`.
S139 closed at 23/23 gates, 102/102 assertions.

## Turn type and task: P4 step 2 — the capacity lever (data-only, small)

Ryan has flagged project-area capacity (93%) again. P4 step 2 is the sequenced next move and is
small: minify `unit_loadouts.json` alone (77 KB of whitespace) — one writer, one regeneration, one
fixed point re-banked via `repro_check.py`, manifest reissued, then read the percentage. **Decision
rule fixed in D213:** ~0.6 points -> whitespace prices like prose and step 3 minifies `units.json`
(650 KB) and `detachments.json` (70 KB); no movement -> step 3 cancelled. No new files; this is the
lever that reduces capacity without adding to it.

## B60 is ready to build, but it is bigger than the ticket says — take it as a parser turn, higher effort

S139's investigation (diagnosis only, nothing changed) found B60 is **not** the mechanical
field-relabel the ticket describes. Three findings, all needing the source, so budget a stronger
model for the fix:

* In **four** of the eleven `rule_text` cases (Black Templars, Blood Angels, Dark Angels, Space
  Wolves) the literal header word `RESTRICTIONS` is present in the source right before the
  chapter-exclusivity sentence — the parser's header detection is failing to catch it there, so the
  whole block, header text included, falls through into `rule_text`. A real parse bug, not a
  pack-formatting difference.
* Two of the twelve records already in `restrictions` are **corrupted independently**: Dark Angels
  `LION'S BLADE TASK FORCE` has stratagem text bled into the field, and `WRATH OF THE ROCK` has no
  restriction text at all — just fragment text and stray CP tokens. A routing change alone will not
  clean these; root-cause both before fixing.

It's a `detachment_parser.py` fix + `detachments_repro_check.py` regeneration, data-only, and blocks
nothing else — so it can wait behind P4 step 2, but the diagnosis above should save the re-derivation.

## After that, the faction priority order resumes

* **Chaos Space Marines** is next in the priority order and the meaningful unblock — it flips Chaos
  Daemons | SHADOW LEGION's HERETIC ASTARTES unlock from `enforced: false` to live. Large data build;
  scope it as its own turn.
* **B17 remainder** — Sanguinary Guard's max-1 Sanguinary Banner add + confirm the 3/6 size selector.
* **E23** — scoping-only turn (no build). The Tank Ace keyword-grant across six copies; decide where
  the per-list selection state lives (the one genuine design call), and whether the Character-keyword
  grant is a fifth `detachment_effects.json` kind or its own mechanism. Lands on E4 and E9 — scope
  before touching either.

## Standing inputs (unchanged from S138)

* A **local backup folder** for the GW-derived files (the nine Chaos Daemons CSVs, the Wahapedia
  export, the MFM `.txt` files, the faction web/pack files, `Army_Muster_Rules.txt`,
  `wh40k_core_rules.md`). The repo cannot hold them.
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard**.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now thirteen sessions.**

## Effort

**Mostly mechanical.** P4 step 2 is data-only and low effort. B60, when taken, is the exception —
its fix is parser diagnosis worth a stronger model, per the findings above. CSM is a large but
mechanical data build once scoped.

## Backlog

**6 open:** P2, P4, E23, B60, E12, B17.
