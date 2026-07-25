# Next-session prompt — Session 145

Session 144 shipped no pipeline changes — a verification/process session (D224). Ryan replaced
`Space_Marines_web.txt` (stratagem sections stripped, 11,364 → 7,906 lines) and supplied
`Chaos_Space_Marines_web.txt` (8,337 lines). Both checked against source and mechanically before
being trusted: no parser reads stratagem content from any `_web.txt` file, `repro_check.py`
reproduces `unit_loadouts.json` byte-for-byte with the smaller file, 104/104 assertions and 23/23
gates hold. CSM's build blocker is cleared.

## Baseline at open

Verify the S144 hashes in the handoff's Files section byte-for-byte, then run `./baseline.sh`.
S144 closed at 23/23 gates, 104/104 assertions (unchanged from S143 — no assertion or pipeline file
touched this session). Re-pull `repo_check.py` from the repo and check whether **B67** has been
remediated (see below) before doing anything else.

## Still open from S143 — check before proceeding

* **B67, CRITICAL.** `Unit_Weapons.csv` and `wh40k_core_rules.md` were found committed to the public
  repo (S143, D223) — its entire history is one commit. Claude has no push credentials. Confirm with
  Ryan whether this has been remediated; if not, it is still the first thing to raise.
* **`detachments.json` is repo-eligible** (D223 correction) — do not exclude it from any push.

## Chaos Space Marines — ready to build

Fully unblocked: 112 datasheets, 18 detachments, `MFM_Chaos_Space_Marines_v1_0.txt` (499 lines),
`Chaos_Space_Marines_web.txt` (8,337 lines, 58 `UNIT COMPOSITION` anchors — structure checked, not
yet run through `equipped_parser.py`). This is a **large data build** — scope it as its own turn
before running the pipeline for real; do not fold scoping and building into one turn. Get a fresh
capacity percentage from Ryan first — S144 removed ~3,458 lines from one source file and added
~8,337 in another, and the net direction isn't known yet.

## Also open

* **B17 remainder** — Sanguinary Guard's max-1 Sanguinary Banner add + confirm the 3/6 size selector.
* **E23** — scoping-only turn (no build). Tank Ace Character-keyword grant across six copies; decide
  where per-list selection state lives and whether it's a fifth `detachment_effects.json` kind or its
  own mechanism. Lands on E4 and E9 — scope before touching either.
* **B61** — Ryan-reported, not yet scoped by Claude: in the combined attached-unit popup the
  bodyguard's expand arrow opens the leader's rules/abilities. Engine-only turn against
  `index.html`'s combined-popup renderer.
* **P4** — capacity direction unknown pending a fresh read (see above); decision-log archive split
  (not yet attempted) remains the next prose lever if still needed once CSM's real cost is known.

## Standing inputs (unchanged from S138–S141)

* A **local backup folder** for the GW-derived files (the nine Chaos Daemons CSVs, the Wahapedia
  export, the MFM `.txt` files, the faction web/pack files, `Army_Muster_Rules.txt`,
  `wh40k_core_rules.md` as of S141).
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard**.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now eighteen sessions.**

## Effort

B67 confirmation is mechanical (low effort). CSM's build-turn scoping wants a stronger model —
112 datasheets across 18 detachments is the largest single faction build since Space Marines itself.

## Backlog

**7 open:** P2, P4, E23, E12, B17, B61, B67.
