# Next-session prompt — Session 148

Session 147 was CSM turn A (D229, data-only): 54 self-priced CSM units shipped, diff-traced clean
(54 new, 0 lost, 0 changed among the existing 270). It also opened **B68** (D230): building CSM's
loadout-defaults pass surfaced a real parser bug, not a CSM-specific complication — deferred,
`unit_loadouts.json` and `repro_check.py` left untouched. Full detail in the decision log (D229/D230)
and `SESSION_HANDOFF_147.md`.

## Baseline at open

Verify S147's hashes in the handoff's Files section byte-for-byte, then run `./baseline.sh --no-repo`.
**Expect 21/23 gates** — `repro_check` FAILS and `rules_assertions` FAILS on its own embedded P1 check,
both the exact same root cause (B68), both naming the same seven unit_ids
(`000001046,000001047,000001048,000001049,000001050,000002461,000004209`). This is the known,
diagnosed state carried forward from S147 — confirm the failure text matches before doing anything
else; if it doesn't match exactly, treat that as a new problem, not B68 recurring.

## B68 — fix first, before CSM turn B or C

Death Guard and Chaos Space Marines each carry their own datasheet for seven generic Chaos vehicles
(Chaos Rhino, Chaos Land Raider, Chaos Predator Annihilator, Chaos Predator Destructor, Chaos Spawn,
Defiler, Helbrute) — same Unit Name, distinct unit_ids. Something in `loadout_parser.py` and/or
`equipped_parser.py` matches by name rather than army+unit_id, so once a second same-named datasheet
exists, one faction's stored defaults can silently pick up the other's. Proven in S147 by running the
unmodified production chain (CSM named nowhere in `--factions` or the web passes) against a
CSM-inclusive `units.json` and still getting 23 changed pre-existing units — mere co-presence in the
file triggers it, not any processing of CSM's own data.

**This is an engine/parser turn — do not mix with data work.** Suggested approach: grep both scripts
for every dict/lookup keyed on a bare unit or model-group name (not `(army, name)` or `unit_id`) that
feeds `default_weapons`, `_defaults_source`, or any per-unit default-set assignment; rekey to include
army or unit_id. After the fix, re-run the full production chain and diff-trace against the
**currently-committed** `unit_loadouts.json` (not S147's scratch builds) — confirm zero drift outside
what a correct CSM web pass should add. Only then update `repro_check.py` (FACTIONS +CSM, WEB_PASSES
+Chaos_Space_Marines) and regenerate `unit_loadouts.json` for real.

Full ticket: **B68** in `OPEN_ITEMS_BACKLOG.md`.

## Then: CSM turn B — cult-troop cross-file points (data, own turn)

Khorne Berzerkers, Rubric Marines, Plague Marines, Noise Marines — the four units S147 withheld —
need pricing from their god-legion's own MFM (World Eaters / Thousand Sons / Death Guard / Emperor's
Children respectively). The existing `--append --scope-to-army` machinery needs a relabel: those MFM
rows carry the parent legion's Army Name, but the target is CSM's own `Unit_Stats.csv` rows (tagged
"Chaos Space Marines"), so scope-to-army as written won't match them directly. Likely needs a small,
well-scoped `mfm_points_parser.py` flag (e.g. a forced output-army override alongside `--scope-to-army`)
— that makes this a parser change too, so it cannot ride with turn A/C's plain config-line edits;
scope it as its own turn regardless of how small the code change turns out to be.

## Then: CSM turn C — detachments (data, own turn)

`detachment_parser.py` config lines only (§6 of `CSM_BUILD_SCOPE.md`): 17 detachments, 3 dropped as
stale (Champions of Chaos, Infernal Reavers, Underdeck Uprising), 2 MFM-only kept
(Devotees of Destruction, Murdertalon Raiders). **D228 still awaits Ryan's explicit yes/no** — the
recommendation (build the two prose-less ones selectable, prose-incomplete) is what turn C proceeds
on absent a "no."

## Then: tooling turn

CSM-specific assertions (roster 58, detachment count 17, the four cross-sourced points, the two
prose-less detachments recorded as such — plus, per S147, confirm `datasheet_wargear_abilities.json`
and the three merged lookups are covered by whatever pins `units.json`'s fixed point), manifest
reissue, harness pass.

## Also open

* **Ryan's `_web.txt` regeneration plan** — Black Templars, Death Guard, a Space Marines rerun. D226:
  before starting any one, pause and ask Ryan to load that faction's new file, then wait.
* **B67b** — optional git-history purge of the two removed GW files. Ryan's call.
* **B17 remainder** — Sanguinary Guard's max-1 Sanguinary Banner add + confirm the 3/6 size selector.
* **E23** — scoping-only (no build). Tank Ace Character-keyword grant; decide where per-list state
  lives. Lands on E4/E9.
* **B61** — combined attached-unit popup: bodyguard's expand arrow opens the leader's rules. Engine-
  only turn against `index.html`'s combined-popup renderer.
* **P4** — 96% at S145 (Ryan's own read at S147's open). S147 added ~401 KB across `units.json` +
  three merged lookups + `datasheet_wargear_abilities.json`. The decision-log archive split (flagged
  since D211/step 1) is the next lever and still hasn't been attempted — worth doing before CSM's
  remaining three turns add roughly another ~140 KB (detachments.json ~94 KB, unit_loadouts.json
  ~40 KB) on top.
* **D199's four batched calls** remain unreviewed since S127 — now twenty-one sessions; three
  load-bearing in shipped code. Plus D228 above.

## Effort

B68 is the analysis-heavy one — real engine/parser diagnosis with cross-faction risk if the rekey is
wrong; give it a stronger model. CSM turn B (cult-troop pricing) is also analysis-heavy per S146's
original scoping, for the same reason (a parser flag addition). CSM turn C (detachments) and the
tooling turn are closer to mechanical. Baseline verification is mechanical.

## Backlog

**8 open:** P2, P4, E23, E12, B17, B61, B67b, B68.
