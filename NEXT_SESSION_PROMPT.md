# Next-session prompt — Session 146

Session 145 was data-only (D225): the S144→S145 gap turned out to be real drift, not a stale sync —
`Space_Marines_web.txt` and `Chaos_Space_Marines_web.txt` had both been edited further, and
`Space_Wolves_web.txt` was entirely missing. Reconciled: B67 corrected and closed (repo has 249
commits, not one — D223 was wrong; both GW-derived files confirmed removed from HEAD; full history
purge filed as B67b, optional), a complete Dark Angels file and a new Space Wolves file verified
against the real pipeline (one genuine Dark Angels data bug found and fixed — Ravenwing Dark Talon's
missing second Hurricane bolter), and `unit_loadouts.json` regenerated. Baseline is clean.

## Baseline at open

Verify the S145 hashes in the handoff's Files section byte-for-byte, then run `./baseline.sh`.
S145 closed at **23/23 gates, 104/104 assertions** — the first fully clean baseline since S143.

## Chaos Space Marines — still ready to build, still not started

Fully unblocked since S144: 112 datasheets, 18 detachments, `MFM_Chaos_Space_Marines_v1_0.txt` (499
lines), `Chaos_Space_Marines_web.txt` (structure checked, not yet run through `equipped_parser.py`).
This is the largest single faction build since Space Marines itself — **scope it as its own turn
before running the pipeline for real; do not fold scoping and building into one turn.** Get a fresh
capacity percentage from Ryan first (96% as of S145) — CSM's real build will add further volume on
top (`detachments.json`/`units.json`/`unit_loadouts.json` growth from 112 new datasheets and 18 new
detachments), and that's the actual number that matters for whether this fits.

## Also open

* **Ryan's `_web.txt` regeneration plan** — Ryan has a script (used for the new Space Wolves file) he
  intends to use on Black Templars, Death Guard, and a rerun of Space Marines, for consistency and
  some capacity relief. S145's recommendation: **one file at a time, each its own verified data-only
  turn** — not a batch — the same way Dark Angels and Space Wolves were handled. **Before starting any
  one of these (D226): pause, explicitly ask Ryan to load that faction's new file, and wait — do not
  assume it's already loaded or proceed against the existing file.** Once it's supplied, treat it
  exactly like S145 treated Dark Angels/Space Wolves: run the real pipeline, diff against committed
  `unit_loadouts.json`, trace every difference to a cause before trusting it.
* **B67b** — optional, not time-sensitive. Purge `Unit_Weapons.csv`/`wh40k_core_rules.md` from git
  history via `git filter-repo` or BFG + force-push. Ryan's call whether it's worth doing at all.
* **B17 remainder** — Sanguinary Guard's max-1 Sanguinary Banner add + confirm the 3/6 size selector.
* **E23** — scoping-only turn (no build). Tank Ace Character-keyword grant across six copies; decide
  where per-list selection state lives and whether it's a fifth `detachment_effects.json` kind or its
  own mechanism. Lands on E4 and E9 — scope before touching either.
* **B61** — Ryan-reported, not yet scoped by Claude: in the combined attached-unit popup the
  bodyguard's expand arrow opens the leader's rules/abilities. Engine-only turn against
  `index.html`'s combined-popup renderer.
* **P4** — 96% as of S145. The decision-log archive split (flagged since D211/step 1 — move the log's
  archive half to a repo-only file, `DECISION_INDEX.md` covering lookup, same treatment
  `BACKLOG_ARCHIVE.md` got) is the next lever if still needed; hasn't been attempted.

## Standing inputs (unchanged from S138–S141)

* A **local backup folder** for the GW-derived files (the nine Chaos Daemons CSVs, the Wahapedia
  export, the MFM `.txt` files, the faction web/pack files, `Army_Muster_Rules.txt`,
  `wh40k_core_rules.md` as of S141).
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard**.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now nineteen sessions.**

## Effort

Baseline verification is mechanical (low effort). CSM's build-turn scoping wants a stronger model —
112 datasheets across 18 detachments is the largest single faction build since Space Marines itself.

## Backlog

**7 open:** P2, P4, E23, E12, B17, B61, B67b.
