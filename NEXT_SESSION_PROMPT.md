# Next-session prompt — Session 143

Session 142 closed B60 (D221): `detachment_parser.py` now routes every detachment's
chapter-exclusivity restriction to `restrictions` consistently — 25 chapter-exclusive detachments
populated, zero left in `rule_text`, no stratagem/CP debris. Data-only; `detachments.json` re-banked,
manifest reissued. 23/23 gates, 102/102 assertions. The assertion that would pin this shape was
deliberately not added (turn typing) and is filed as **B60a**.

## Baseline at open

Verify the six S142 hashes in the handoff's Files section byte-for-byte, then run `./baseline.sh`.
S142 closed at 23/23 gates, 102/102 assertions.

Note `detachments.json` is not repo-eligible (it carries GW rule prose in `rule_text`,
`restrictions` and enhancement descriptions). `detachment_parser.py` and `pipeline_manifest.json`
are. `repo_check.py` was not runnable in the S142 sandbox (no clone) — baseline ran `--no-repo`;
run the repo custody check at S143 open if the repo is reachable.

## B60a — pin the fix (tooling, small)

A `rules_assertions.py`-only turn. Assert, against `detachments.json`: every chapter-exclusivity
detachment carries the sentence in `restrictions` and none carries it in `rule_text`; no
`restrictions` value contains stratagem/CP debris (`STRATAGEM`, `WHEN:`, `\bCP\b`). This is cheap
and closes the *facts as executable checks* gap D221 left open. Do it before or after CSM as
convenient — it blocks nothing.

## Faction priority order resumes — Chaos Space Marines is the meaningful unblock

* **Chaos Space Marines** is next in the priority order. Building it flips Chaos Daemons |
  SHADOW LEGION's HERETIC ASTARTES unlock from `enforced: false` to live (E22). Large data build;
  scope it as its own turn. Mind capacity — the project area read **90%** after S141's core-rules
  removal; CSM adds source and output volume. Size CSM's real file footprint first; if it's tight,
  the decision-log archive split (P4, not yet attempted) is the next prose lever.
* **B17 remainder** — Sanguinary Guard's max-1 Sanguinary Banner add + confirm the 3/6 size selector.
* **E23** — scoping-only turn (no build). Tank Ace Character-keyword grant across six copies; decide
  where per-list selection state lives and whether it's a fifth `detachment_effects.json` kind or its
  own mechanism. Lands on E4 and E9 — scope before touching either.
* **B61** — Ryan-reported, not yet scoped by Claude: in the combined attached-unit popup the
  bodyguard's expand arrow opens the leader's rules/abilities. Engine-only turn against
  `index.html`'s combined-popup renderer.

## Standing inputs (unchanged from S138–S141)

* A **local backup folder** for the GW-derived files (the nine Chaos Daemons CSVs, the Wahapedia
  export, the MFM `.txt` files, the faction web/pack files, `Army_Muster_Rules.txt`,
  `wh40k_core_rules.md` as of S141).
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard**.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now sixteen sessions.**

## Effort

B60a is mechanical (low effort). CSM is a large but mechanical data build once scoped. E23 and B61
scoping want a stronger model when reached.

## Backlog

**7 open:** P2, P4, E23, E12, B17, B61, B60a.
