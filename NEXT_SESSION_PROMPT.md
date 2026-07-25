# Next-session prompt — Session 142

Session 141 verified S140's baseline (23/23 clean, all hashes matched), then closed out P4's
whitespace line: step 3 is **cancelled** (D220) — step 2's 77 KB removal moved the displayed
percentage by nothing, so minifying `units.json`/`detachments.json` isn't expected to be worth three
re-banked fixed points. In its place, `wh40k_core_rules.md` (139 KB, GW text, referenced by no
script) was removed from the working directory, verified safe by static scan and park-and-rerun
(23/23), and delivered to Ryan as a local-backup file — a direct response to Ryan flagging the
project area's 92% capacity ahead of B60 and the CSM data build, both of which need to add or grow
files. This was a PROCESS turn; no code, data, or engine change.

## Baseline at open

Verify the five S141 hashes in the handoff's Files section byte-for-byte, then run `./baseline.sh`.
S141 closed at 23/23 gates, 102/102 assertions — unchanged from S140, since nothing engine- or
data-side moved this session.

## First: confirm the deletion and read the new percentage

Check whether Ryan deleted `wh40k_core_rules.md` from the project knowledge panel and what the
resulting percentage reads. If it's meaningfully down from 92%, note it in P4 and consider whether
the remaining ~178 KB of identified removable prose, or the decision-log split (see
`OPEN_ITEMS_BACKLOG.md`'s P4 entry), is worth a further turn before B60/CSM start adding volume. If
capacity isn't the live concern anymore, move straight to B60.

## B60 — parser fix, higher effort

S139's investigation (diagnosis only) found B60 is **not** the mechanical field-relabel the ticket
describes. Budget a stronger model — this needs source-text judgment, not just routing:

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
  scope it as its own turn. Mind the capacity picture before adding new large source/output files.
* **B17 remainder** — Sanguinary Guard's max-1 Sanguinary Banner add + confirm the 3/6 size selector.
* **E23** — scoping-only turn (no build). The Tank Ace keyword-grant across six copies; decide where
  the per-list selection state lives (the one genuine design call), and whether the Character-keyword
  grant is a fifth `detachment_effects.json` kind or its own mechanism. Lands on E4 and E9 — scope
  before touching either.

## Standing inputs (unchanged from S138)

* A **local backup folder** for the GW-derived files (the nine Chaos Daemons CSVs, the Wahapedia
  export, the MFM `.txt` files, the faction web/pack files, `Army_Muster_Rules.txt`,
  `wh40k_core_rules.md` as of S141). The repo cannot hold them.
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard**.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now fifteen sessions.**

## Effort

**Mostly mechanical.** The percentage check and any further capacity move are process-tier, low
effort. B60 is the exception — its fix is parser diagnosis worth a stronger model. CSM is a large but
mechanical data build once scoped.

## Backlog

**6 open:** P2, P4, E23, B60, E12, B17.
