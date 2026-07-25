# Next-session prompt — Session 147

Session 146 was tooling-only (D227): Chaos Space Marines build **scoped, not built** — full plan in
`CSM_BUILD_SCOPE.md`. Baseline verified clean at open (S145's six hashes matched byte-for-byte,
`./baseline.sh --no-repo` 23/23 gates, 104/104 assertions). No committed data/engine/parser changed.

## Baseline at open

Verify the S146 hashes in the handoff's Files section byte-for-byte, then run `./baseline.sh`.
Expect 23/23 gates, 104/104 assertions (unchanged from S145 — this was a docs-only turn).

## CSM build — ready, sequenced, one decision pending

Read `CSM_BUILD_SCOPE.md` first. Headline corrections vs the old framing: the real roster is **58
units, not 112** (54 are Legends, correctly excluded); detachments reconcile to **17** under D192;
Marks of Chaos need **no new mechanism**. CSM is a clean Death-Guard-shaped build — no chapter split,
no allied codex, no `index.html` change.

**Build is four turns, strictly separated (scope §8):**
1. Data turn A — the 54 self-priced units (config lines in `units_repro_check.py` / `repro_check.py`,
   regenerate, diff, trace, bank).
2. Data turn B — cult-troop cross-file points append (Khorne Berzerkers/Plague/Rubric/Noise from
   WE/DG/TS/EC MFMs). The one part that may run deep — if it does, keep it its own turn.
3. Data turn C — detachments (`detachment_parser.py` config, regenerate `detachments.json`, verify
   17 / dropped-3 / two prose-less).
4. Tooling turn — CSM assertions, manifest reissue, harness pass.

**Do not fold turns together.** Start with turn A next session.

## Pending decision — D228 (build proceeds on recommendation unless Ryan says otherwise)

The two new 11th-ed detachments (Devotees of Destruction, Murdertalon Raiders) have no held rule/
enhancement/stratagem prose. Recommendation: build them selectable but prose-incomplete, because
suppressing legal detachments breaks the tool's core promise. Reversible (one inclusion flag). Flagged
for an explicit yes/no because it's precedent-setting; turn C proceeds on the recommendation absent a
"no".

## Also open

* **Ryan's `_web.txt` regeneration plan** — Black Templars, Death Guard, a Space Marines rerun. D226:
  before starting any one, pause and ask Ryan to load that faction's new file, then wait. One file
  per verified data-only turn — not a batch.
* **B67b** — optional git-history purge of the two removed GW files. Ryan's call.
* **B17 remainder** — Sanguinary Guard's max-1 Sanguinary Banner add + confirm the 3/6 size selector.
* **E23** — scoping-only (no build). Tank Ace Character-keyword grant; decide where per-list state
  lives. Lands on E4/E9.
* **B61** — combined attached-unit popup: bodyguard's expand arrow opens the leader's rules. Engine-
  only turn against `index.html`'s combined-popup renderer.
* **P4** — 96% at S145. The decision-log archive split (flagged since D211/step 1) is the next lever
  and hasn't been attempted; it's the standing answer if CSM's ~540 KB output growth strains capacity.
* **D199's four batched calls** remain unreviewed since S127 — now twenty sessions; three load-bearing
  in shipped code. Plus D228 above.

## Effort

CSM turn A (build) is data work with a real diff-trace component — moderate. Turn B (cult-troop
cross-file pricing) is the analysis-heavy one; give it a stronger model. Baseline verification is
mechanical.

## Backlog

**7 open:** P2, P4, E23, E12, B17, B61, B67b.
