# Next-session prompt — Session 138

Session 137 shipped **E21d pieces 1-2** and **B64/B65/B66** (**D215**): refusal prose, the picker's
forbid gate made visible before the click, and the Battleline indicator are live in `index.html` at
**6.8**. Three UI tickets from a screenshot review — detachment detail moved to a shared modal
(B64), DP-budget refusal no longer rendered red (B65), config-panel eye icon swapped for an info icon
(B66) — shipped in the same UI turn. Read `SESSION_HANDOFF_137.md`, then **D215**, then **D214** (the
piece-3 recommendation this session did not build).

## Turn type

**UI-only**, same as S137, if E21d piece 3 is what's tackled next (see below) — or **product decision
first**, if Ryan's confirmation on piece 3 hasn't arrived yet, in which case start elsewhere in the
backlog (B62, B60, or E23's scoping turn are all available and don't depend on it).

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline) — 23 gates, same set as S137 closed on. Verify the S137
hashes in `SESSION_HANDOFF_137.md`'s Files section before trusting the sync.

## The task: E21d piece 3, if Ryan has confirmed the direction

D214's recommendation: a Plague Legions unit stranded by deselecting or switching away from Tallyband
Summoners renders as a visible roster error — the enhancement over-state treatment (never a silent
trim, never a blocked deselect). The engine already rejects the stranded unit (`offerableUnits`,
`canAddUnitToList`); this is a render-only turn, wiring the existing predicate to a warning on the
roster card, in the mould of `entryHasError`. **Do not build this without Ryan's confirmation in this
conversation** — it sets a precedent for how the tool treats a legal list a later detachment change
makes illegal, and the prompt for S137 held it for exactly this reason.

Once piece 3 ships, **E21 closes**. Update the backlog header and E21's entry accordingly at close.

## If piece 3 has not been confirmed yet

Move to whichever of these is most convenient to open cleanly:

* **B60** — `detachment_parser.py`'s `restrictions` field is populated inconsistently (11 of 25 in
  `restrictions`, 14 of 25 in `rule_text`, zero overlap). Parser fix + `detachments_repro_check.py`
  regeneration. Data-only turn, no engine or UI impact — does not block anything else.
* **B62** — the `FALSE` string-literal quirk in `Is Base Equipment` (Keeper of Secrets, Soul Grinder)
  and the missing presence-and-parse assertion over the nine Chaos Daemons CSVs. Small, self-contained.
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
* **D199's four batched calls remain unreviewed — since S127, now eleven sessions.**
* **Project-area capacity.** No new files added S137 (docs-only volume, negligible). P4 step 2 is the
  next lever, sequenced above.

## Effort

**Mostly mechanical**, whichever branch is taken. Piece 3 is UI plumbing over an existing predicate —
moderate effort is enough once the direction is confirmed. B60/B62/E23-scoping are all mechanical to
low-moderate; E23's scoping calls where the keyword-grant selection state lives is the one part worth
slowing down for, since it's a genuine design decision, not just data cleanup.

## Backlog

**8 open:** B62, P2, P4, E21 (piece 3 only), E23, B60, E12, B17.
