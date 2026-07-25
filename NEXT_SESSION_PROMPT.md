# Next-session prompt — Session 141

Session 140 shipped **P4 step 2** (**D219**): `unit_loadouts.json` minified via `equipped_parser.py`'s
terminal writer, 201,999 -> 124,652 bytes, 77,347 removed — matching D213's 77 KB estimate. Fixed
point re-banked, manifest reissued. Data-only turn; no engine or index.html change.

## Baseline at open

Verify the six S140 hashes in the handoff's Files section byte-for-byte, then run `./baseline.sh`.
S140 closed at 23/23 gates, 102/102 assertions.

## First: read Ryan's percentage report before picking the turn

P4 step 2's decision rule (D213) needs the displayed capacity percentage after the S140 files are
live in the project area — check `SESSION_HANDOFF_140.md`'s "Decisions needed" section and whatever
Ryan reported before this session opened. **If ~0.6 points moved:** whitespace prices like prose;
P4 step 3 minifies `units.json` (650 KB) and `detachments.json` (70 KB) the same way — same
mechanism as step 2, mechanical, data-only. **If it didn't move:** step 3 is cancelled, P4 closes
with step 2 as its final result, and the session goes straight to B60 below.

## B60 — parser fix, higher effort (take this if P4 step 3 doesn't apply, or after it)

S139's investigation (diagnosis only, nothing changed) found B60 is **not** the mechanical
field-relabel the ticket describes. Budget a stronger model — this needs source-text judgment, not
just routing:

* In **four** of eleven `rule_text` cases (Black Templars, Blood Angels, Dark Angels, Space Wolves)
  the literal header word `RESTRICTIONS` is present in the source right before the
  chapter-exclusivity sentence — the parser's header detection is failing to catch it there, so the
  whole block, header text included, falls through into `rule_text`. A real parse bug.
* Two of twelve records already in `restrictions` are **corrupted independently**: Dark Angels
  `LION'S BLADE TASK FORCE` has stratagem text bled into the field, and `WRATH OF THE ROCK` has no
  restriction text at all — just fragment text and stray CP tokens. A routing change alone won't
  clean these; root-cause both before fixing.

It's a `detachment_parser.py` fix + `detachments_repro_check.py` regeneration, data-only, and blocks
nothing else.

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
* **D199's four batched calls remain unreviewed — since S127, now fourteen sessions.**

## Effort

**Mostly mechanical.** P4 step 3, if it applies, is data-only and low effort — identical mechanism
to step 2. B60 is the exception — its fix is parser diagnosis worth a stronger model. CSM is a large
but mechanical data build once scoped.

## Backlog

**6 open:** P2, P4, E23, B60, E12, B17.
