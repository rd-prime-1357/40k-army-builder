# SESSION HANDOFF 216

**Turn type:** data-only (B111 data half — `wargear_points.json` regenerated from v1.1, D310).
`wargear_points.json` only. No engine file, no other data file, no tooling file touched.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: 32/34 gates green. Both
   reds were the documented, expected ones — `rules_assertions` on **E14-1** (the known-red D309
   deliberately left open) and `repo_check` on the pre-existing B108 finding. Private source repo
   fetched and verified fresh: **85/85 source files byte-match `source_manifest.json`**.

2. **B111 data turn shipped.** Ran `mfm_points_parser.py --wargear MFM_*.txt --units units.json
   --loadouts unit_loadouts.json --datasheets Datasheets.csv --wargear-out wargear_points.json`,
   diff-guarded key-by-key against the pre-turn file before banking.

   **9 price changes, all forecast in D309.** Heavy reaper autocannon and Hades lascannon
   10 → 15 pts on the four Defiler factions (Chaos Space Marines, Thousand Sons, Death Guard,
   Emperor's Children — 8 changes). Space Marines' Victrix Honour Guard "Banner of Macragge"
   10 → 15 pts (1 change). No other existing item's price moved. World Eaters' Defiler entries
   surface in the parser's raw MFM read but stay out of scope — unit not yet in `units.json`,
   faction unbuilt — and do not touch the output.

   **3 new items, not individually forecast (D309 only itemized price conflicts, not new keys).**
   Checked each against both MFM versions before banking; all three are genuine — the v1.1 file
   adds a `WARGEAR OPTIONS` block that did not exist at all in v1_0, on a unit whose base points
   already carry the v1.1 value in `units.json` (confirming the option is additive, not a
   double-count): Black Templars' Repulsor Executioner gains "Heavy laser destroyer" (10 pts);
   Thousand Sons' Forgefiend gains "Ectoplasma cannon" (5 pts); the Centurion Devastator Squad
   (generic Adeptus Astartes, listed in the Black Templars MFM file) gains "Twin lascannon"
   (5 pts). Zero items removed.

3. **Confirmation checks all pass.** `repro_check`, `units_repro_check`, `detachments_repro_check`,
   `b87_check`, `b88_check` all stayed byte-identical after the regen — `units.json` and
   `unit_loadouts.json` did not move, confirming these wargear items price per-instance at build
   time and are not folded into unit base points. `rules_assertions --tier all`: **E14-1 now
   passes**; only remaining fail was P3 (`wargear_points.json` off the manifest hash), the expected
   pre-`--write` state, not a real failure.

4. **B111 fully closed.** Tooling half (D309, S215) + data half (D310, this session). Moved to
   Closed / Shipped in `OPEN_ITEMS_BACKLOG.md` with full history; ledger dropped 23 → 22 open.

## State at close

- `wargear_points.json`: regenerated from v1.1 MFM sources. Only functional change. All three
  repro rebuilds still byte-identical; b87/b88 green; E14-1 green.
- Baseline fully green except `repo_check` (B108, unchanged, your action) and the expected
  pre-`--write` manifest mismatch on `wargear_points.json` itself, cleared by `--write` below.
- `40K_Decision_Log.md`: D310 appended.
- `DECISION_INDEX.md`: D310 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: B111 moved to Closed / Shipped with full tooling+data history; Open
  Items pointer body removed; ledger header updated, 22 open.
- `pipeline_manifest.py`: `SESSION_HANDOFF_216.md` registered in GUARDED before `--write`.
- All other files untouched: `index.html`, `units.json`, `unit_loadouts.json`, `detachments.json`,
  `detachment_effects.json`, `rules_assertions.py`, `loadout_parser.py`, `equipped_parser.py`,
  `detachment_parser.py`, `faction_taxonomy.json`, `bundled_swaps.json`, `source_manifest.json`,
  `baseline.sh`, `mfm_points_parser.py`.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged;
   ideally scrub git history), and push it to the private source repo.
2. Push this session's changed files to the public repo (listed below).

## Decisions waiting on Ryan

None new. The one from S215 (B111 sequencing — split vs. combined turn) is now moot; B111 is
closed either way.

## Files (SHA-256, first 12)

Verify these at S217 open.

| file | sha256:12 | note |
|------|-----------|------|
| `wargear_points.json` | `2a9882e1d3ca` (pre-`--write`; re-pinned by `pipeline_manifest --write`) | regenerated from v1.1 (B111 data half, D310) |
| `40K_Decision_Log.md` | `d50d852ae98a` (pre-`--write`) | D310 appended |
| `DECISION_INDEX.md` | `aa7f4248355e` (pre-`--write`) | D310 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `3c17c86c45d3` (pre-`--write`) | B111 closed, moved to Closed/Shipped; ledger 23→22 |
| `pipeline_manifest.py` | `16aeeb4f5b4f` (pre-`--write`) | `SESSION_HANDOFF_216.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S217 |
| `SESSION_HANDOFF_216.md` | (this file) | |

`index.html`, `units.json`, `unit_loadouts.json`, `abilities.json`, `weapon_abilities.json`,
`datasheet_wargear_abilities.json`, `rules_assertions.py`, `loadout_parser.py`,
`equipped_parser.py`, `detachment_parser.py`, `detachments.json`, `detachment_effects.json`,
`bundled_swaps.json`, `source_manifest.json`, `baseline.sh`, `faction_taxonomy.json`,
`mfm_points_parser.py`: **untouched**, no entry needed.

## Backlog

23 open at S215 close; 22 open here (B111 closed on its data half, nothing else opened).
Beginning: B111, B110, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2,
P4, E23, B67b, E12, B17, B112 (23). Resolved: B111 (1). Added: none (0). Ending: B110, B108, B99,
B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17, B112 (22).
