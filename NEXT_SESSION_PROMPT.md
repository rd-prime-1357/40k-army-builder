# Next-session prompt — Session 148

Session 147 was CSM turn A (D229, data-only): 54 self-priced CSM units shipped, diff-traced clean
(54 new, 0 lost, 0 changed among the existing 270). It also opened **B68** (D230): building CSM's
loadout-defaults pass surfaced a real parser bug, deferred. Full detail in the decision log (D229/D230)
and `SESSION_HANDOFF_147.md`.

## Project-area state — READ THIS FIRST

The project area went over 100% at S147's close (CSM's ~367 KB of `units.json` growth was the tipping
point — the P4 risk, now realised). Ryan resolved it by **removing the decision log from the project
area entirely.** As of S148 open, the area holds `units.json`, `index.html`, the prompt, the index,
the backlog, and the source/harness files — but **NOT** `40K_Decision_Log_v3_0.md`.

**Where the decision log lives now:** in the GitHub repo (`rd-prime-1357/40k-army-builder`) and Ryan's
local backup, current through **D230** (Ryan confirmed the save this session; the S147 handoff hash for
it is `774125079221`). It is deliberately kept out of the project area to save capacity. `DECISION_INDEX.md`
stays in the area as the always-present lookup table — use it to find the entry you need, then fetch
that entry's full text from the repo if required (same fetch-from-GitHub pattern D217 established for
`BACKLOG_ARCHIVE.md`). Do not assume the log is missing or lost because it isn't in the mount — it's
intentionally repo-only.

## The long-term architecture problem — scope this session (P4)

Ryan's observation, and it's correct: `units.json` will keep growing as factions are added, and given
the full target scope (SM family + all CSM variants + Chaos Daemons + Drukhari, 20-plus distinct
factions), `units.json` alone is on track to exceed the entire project area within the next several
factions. The area was never going to be the long-term home for built data. Tonight's log removal
stumbled onto the right shape by accident.

**Assigned work: a scoping/design note, no build.** Write up a "project-area long-term architecture"
plan under P4. The direction (Ryan has approved the shape, not the details): stop treating the project
area as the store for built/derived data. Built outputs (`units.json`, `unit_loadouts.json`,
`detachments.json`) and source files live in the repo; each session pulls or regenerates what it needs
into the workspace, runs the gates there, hands results back to Ryan to push. The area keeps only the
small active working set that must be read every session — `index.html`, `DECISION_INDEX.md`, the
backlog, the next-session prompt, the handoff chain.

What the note must work out:
- Exactly what stays in the area vs. what becomes fetch-on-demand.
- How the baseline changes — it currently assumes every file is local; it needs a fetch-then-verify
  open instead (and the reproducibility gates are what make outputs safe to remove: they're derived,
  not authored, and `units_repro_check.py` etc. rebuild them byte-for-byte).
- **GW-source custody is the constraint that makes this non-trivial:** GW-derived source (Wahapedia
  CSV export, MFM `.txt` files, faction web/pack files) must NEVER hit the public repo. So those
  particular files can't use the repo as their fetch-on-demand home the way outputs can. Work out
  where they live and how a session gets them without committing them. This is the crux of the design.
- Migration order — what moves out first, how to verify nothing breaks at each step.

Ryan approves the shape before any of it is built. This is scoping only.

**Effort: Ryan is running Fable for this session** — it's precedent-setting architecture work that
changes how every future session opens, so it's worth the stronger model. Do not rush it into a build.

## B68 — the parser fix (engine/parser turn, after or alongside the P4 scope)

Death Guard and Chaos Space Marines each carry their own datasheet for seven generic Chaos vehicles
(Chaos Rhino, Chaos Land Raider, Chaos Predator Annihilator, Chaos Predator Destructor, Chaos Spawn,
Defiler, Helbrute) — same Unit Name, distinct unit_ids. Something in `loadout_parser.py` and/or
`equipped_parser.py` matches by name rather than army+unit_id, so once a second same-named datasheet
exists, one faction's stored defaults silently pick up the other's. Proven in S147: running the
unmodified production chain (CSM named nowhere in `--factions` or the web passes) against a
CSM-inclusive `units.json` still changed 23 pre-existing units' stored defaults — mere co-presence in
the file triggers it, not any processing of CSM's own data.

**Engine/parser turn — do not mix with data work.** Grep both scripts for every dict/lookup keyed on a
bare unit or model-group name (not `(army, name)` or `unit_id`) that feeds `default_weapons`,
`_defaults_source`, or any per-unit default-set assignment; rekey to include army or unit_id. Then
re-run the full production chain and diff-trace against the currently-committed `unit_loadouts.json` —
confirm zero drift outside what a correct CSM web pass should add. Only then update `repro_check.py`
(FACTIONS +CSM, WEB_PASSES +Chaos_Space_Marines) and regenerate `unit_loadouts.json` for real. B68
blocks CSM_BUILD_SCOPE.md §5 (CSM's own loadout-defaults pass). Full ticket: **B68** in the backlog.

## Baseline at open

Verify S147's hashes in the handoff's Files section byte-for-byte, then run `./baseline.sh --no-repo`.
**Expect 21/23 gates** — `repro_check` FAILS and `rules_assertions` FAILS on its own embedded P1 check,
both the exact same root cause (B68), both naming the same seven unit_ids
(`000001046,000001047,000001048,000001049,000001050,000002461,000004209`). This is the known,
diagnosed state carried forward from S147 — confirm the failure text matches before doing anything
else; if it doesn't match exactly, treat that as a new problem, not B68 recurring. Note the decision
log is no longer in the area (see above) — that is expected, not a missing-file failure.

## Then, once B68 is fixed: CSM turn B — cult-troop cross-file points (data, own turn)

Khorne Berzerkers, Rubric Marines, Plague Marines, Noise Marines — the four units S147 withheld —
need pricing from their god-legion's own MFM (World Eaters / Thousand Sons / Death Guard / Emperor's
Children respectively). The existing `--append --scope-to-army` machinery needs a relabel: those MFM
rows carry the parent legion's Army Name, but the target is CSM's own `Unit_Stats.csv` rows (tagged
"Chaos Space Marines"). Likely a small `mfm_points_parser.py` flag (a forced output-army override
alongside `--scope-to-army`) — a parser change, so its own turn regardless of size.

## Then: CSM turn C — detachments (data, own turn)

`detachment_parser.py` config lines only (§6 of `CSM_BUILD_SCOPE.md`): 17 detachments, 3 dropped as
stale (Champions of Chaos, Infernal Reavers, Underdeck Uprising), 2 MFM-only kept
(Devotees of Destruction, Murdertalon Raiders). **D228 still awaits Ryan's explicit yes/no** — the
recommendation (build the two prose-less ones selectable, prose-incomplete) is what turn C proceeds
on absent a "no."

## Then: tooling turn

CSM-specific assertions (roster 58, detachment count 17, the four cross-sourced points, the two
prose-less detachments recorded as such — plus confirm `datasheet_wargear_abilities.json` and the
three merged lookups are covered by whatever pins `units.json`'s fixed point), manifest reissue,
harness pass.

## Also open

* **Ryan's `_web.txt` regeneration plan** — Black Templars, Death Guard, a Space Marines rerun. D226:
  before starting any one, pause and ask Ryan to load that faction's new file, then wait.
* **B67b** — optional git-history purge of the two removed GW files. Ryan's call.
* **B17 remainder** — Sanguinary Guard's max-1 Sanguinary Banner add + confirm the 3/6 size selector.
* **E23** — scoping-only (no build). Tank Ace Character-keyword grant; decide where per-list state
  lives. Lands on E4/E9.
* **B61** — combined attached-unit popup: bodyguard's expand arrow opens the leader's rules. Engine-
  only turn against `index.html`'s combined-popup renderer.
* **P4** — capacity. Now the home of the long-term architecture scope above, not just incremental
  trimming. The archive-split idea floated at S147 is DROPPED — Ryan solved tonight's crunch by
  moving the whole decision log out of the area, which is the better pattern and the seed of the
  architecture plan.
* **D199's four batched calls** remain unreviewed since S127 — now twenty-one sessions; three
  load-bearing in shipped code. Plus D228 above.

## Backlog

**8 open:** P2, P4, E23, E12, B17, B61, B67b, B68.
