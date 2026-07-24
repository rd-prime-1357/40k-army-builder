# Next-session prompt — Session 139

Session 138 shipped **B62** (**D216**): the `Is Base Equipment` boolean fix (a real latent bug on
Keeper of Secrets and Soul Grinder, not the "harmless" quirk D205 assumed), `units.json` re-banked,
and a new presence-and-parse gate (`B62-1`) over the nine Chaos Daemons root CSVs. Data-only turn;
`index.html` untouched. Read `SESSION_HANDOFF_138.md`, then **D216**.

## Turn type

**Product decision first, again** — E21d piece 3 still needs Ryan's confirmation in-conversation
before it's built (D214's recommendation: flag a stranded Plague Legions unit as a visible roster
error, never a silent trim or a blocked deselect). If confirmed at session open, build it — it's
UI-only, wiring an existing predicate to a warning, and E21 closes on landing it. If not yet
confirmed, open elsewhere: **B60** or **E23**'s scoping turn (below).

## Housekeeping resolved: `BACKLOG_ARCHIVE.md` is intentionally repo-only (D217)

Not a mount gap after all — Ryan confirmed it was deliberately moved out of the project area and
committed to the repo, since nothing in the pipeline reads it. B62's full body has already been
fetched from the repo, appended, and handed back for commit. The pointer header in
`OPEN_ITEMS_BACKLOG.md`'s Closed/Shipped section now states this so it isn't re-flagged as missing.
Going forward: fetch from
`https://raw.githubusercontent.com/rd-prime-1357/40k-army-builder/main/BACKLOG_ARCHIVE.md` whenever
a closing ticket needs its full body archived — never re-add it to the project area for this.

## The task: E21d piece 3, if Ryan has confirmed the direction

D214's recommendation: a Plague Legions unit stranded by deselecting or switching away from
Tallyband Summoners renders as a visible roster error — the enhancement over-state treatment
(never a silent trim, never a blocked deselect). The engine already rejects the stranded unit
(`offerableUnits`, `canAddUnitToList`); this is a render-only turn, wiring the existing predicate
to a warning on the roster card, in the mould of `entryHasError`. **Do not build this without
Ryan's confirmation in this conversation** — it sets a precedent for how the tool treats a legal
list a later detachment change makes illegal.

Once piece 3 ships, **E21 closes**. Update the backlog header and E21's entry accordingly at close.

## If piece 3 has not been confirmed yet

* **B60** — `detachment_parser.py`'s `restrictions` field is populated inconsistently (11 of 25 in
  `restrictions`, 14 of 25 in `rule_text`, zero overlap). Parser fix + `detachments_repro_check.py`
  regeneration. Data-only turn, no engine or UI impact — does not block anything else.
* **E23** — scoping-only turn (no build). Confirm the Tank Ace keyword definition against source for
  all six copies (Space Marines, Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves),
  decide where the per-list selection state lives, and decide whether the Character-keyword grant is a
  fifth `detachment_effects.json` kind or its own mechanism. Lands on E4's enhancement eligibility and
  E9's Warlord eligibility — scope carefully before touching either.

## After E21 closes (or in parallel, if a data/tooling turn is picked instead)

* **P4 step 2 — data-only, small.** Minify `unit_loadouts.json` alone (77 KB), re-bank its fixed point,
  reissue the manifest, read the percentage. Decision rule fixed in D213: ~0.6 points → step 3 minifies
  `units.json` and `detachments.json`; no movement → step 3 cancelled.
* **B17 remainder** — Sanguinary Guard's max-1 Sanguinary Banner add + confirm the 3/6 size selector.
* Then the faction priority order resumes: Chaos Space Marines next (it unblocks Shadow Legion's
  HERETIC ASTARTES unlock, still `enforced: false`).

## Standing inputs

* **A local backup folder** for the GW-derived files — the nine Chaos Daemons CSVs, the Wahapedia
  export, the MFM `.txt` files, the faction web and pack files, `Army_Muster_Rules.txt` and
  `wh40k_core_rules.md` (139 KB, opened by nothing). The repo cannot hold them.
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard**.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now twelve sessions.**
* **Project-area capacity.** No new files added S138. P4 step 2 remains the next lever, sequenced
  above; this session's `units.json` change was a two-record content fix, not a volume change.

## Effort

**Mostly mechanical**, whichever branch is taken. Piece 3 is UI plumbing over an existing predicate —
moderate effort is enough once the direction is confirmed. B60/E23-scoping are mechanical to
low-moderate; E23's scoping call on where the keyword-grant selection state lives is the one part
worth slowing down for, since it's a genuine design decision, not just data cleanup.

## Backlog

**7 open:** P2, P4, E21 (piece 3 only), E23, B60, E12, B17.
