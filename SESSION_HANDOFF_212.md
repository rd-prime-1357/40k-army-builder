# SESSION HANDOFF 212

**Turn type:** data-only (B89 — CSM/Death Guard/Thousand Sons detachment v1.1 fix, D306).
`detachment_parser.py` and `detachments.json` changed. `detachment_effects.json` and
`rules_assertions.py` checked directly and confirmed unaffected — neither touched. No engine file
(`index.html`, `loadout_parser.py`, `equipped_parser.py`, `mfm_points_parser.py`) touched.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: 33/34 gates green, sources
   loaded (85 files verified against `source_manifest.json`), 122/122 assertions, all three repro
   checks byte-identical. `repo_check` red on exactly the pre-existing B108 finding
   (`Thousand_Sons_web.txt` in the public repo), unchanged. Public repo confirmed current through
   S211 via direct clone and SHA-256 verification against S211's handoff table — all four listed
   hashes (`detachments.json`, `detachment_effects.json`, `detachment_parser.py`,
   `faction_taxonomy.json`) matched exactly, not assumed from the mount.

2. **Re-pointed `ARMY_TO_MFM` and `MFM_SOURCE_NAME` for Chaos Space Marines, Death Guard, and
   Thousand Sons from v1_0 to v1.1** (`MFM_Chaos_Space_Marines_v1.1.txt`, `MFM_Death_Guard_v1.1.txt`,
   `MFM_Thousand_Sons_v1.1.txt`), mirroring how Emperor's Children was registered in D305.
   `source_manifest.json` needed no change — both versions of all three factions' MFM files were
   already hashed and present (v1_0 stays needed by the units-side pipeline, which is untouched by
   this ticket).

3. **Regenerated `detachments.json`, diff-guarded at record-key level against the committed file.**
   Zero keys added or removed — still 179 distinct detachment records across 17 armies. Exactly 7
   records changed, matching the D305 finding's predicted list item for item:
   - Thousand Sons — Hexwarp Thrallband: 2 DP → 3 DP.
   - Thousand Sons — three force-disposition corrections: Ritual of Regeneration (Purge the Foe →
     Take and Hold), Sekhetar Cohort (Priority Assets → Disruption), Warpforged Cabal (Disruption →
     Priority Assets).
   - Chaos Space Marines — Murdertalon Raiders' disposition (Purge the Foe → Reconnaissance).
   - Chaos Space Marines — Soulforged Warpack's disposition (Purge the Foe → Take and Hold) plus its
     Tempting Addendum enhancement price (25 pts → 40 pts).
   - Death Guard — Contagion Engines' disposition (Purge the Foe → Reconnaissance).

   One additional, unpredicted but harmless diff surfaced in the same pass and was investigated
   rather than assumed benign: Death Guard's Contagion Engines carries an enhancement whose v1.1 name
   gained a hyphen ("Parasitic Woe reaper" → "Parasitic Woe-reaper") — a raw MFM text correction, no
   points or legality effect. `detachments_repro_check.py` passes byte-identical against the new
   committed file.

4. **Checked, not assumed: `detachment_effects.json` and `rules_assertions.py` against the 7 changed
   keys directly.** None of the three factions' `detachment_effects.json` entries (Death Guard's
   Shamblerot Vectorium/Tallyband Summoners, Chaos Space Marines' Chaos Cult, Thousand Sons'
   Changehost of Deceit/Servants of Change/Warpmeld Pact) reference any of the 7 changed keys — no
   update needed. `rules_assertions.py`'s CSM-3 and TS-2 pin `text_source` only (for Murdertalon
   Raiders, Ritual of Regeneration, and Sekhetar Cohort) — a field this fix does not touch — so no
   assertion needed reconciling.

5. **B89 stays open, not closed.** This session fixed the CSM/Death Guard/Thousand Sons portion of
   the detachments-side v1_0-sourcing gap. The same pattern applies to the six-file Space Marines
   group (base Adeptus Astartes, Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves)
   — already noted at D291 (Black Templars gains a new Vengeful Hosts detachment in v1.1, several
   enhancement re-prices) but never confirmed/quantified by a direct parse-and-diff the way this
   session did for CSM/DG/TS. Recommended as B89's next data turn. Chaos Daemons remains blocked — no
   v1.1 detachment file exists to compare against.

## State at close

- `detachments.json`: 7 records changed, 0 added/removed. `detachments_repro_check.py`
  byte-identical. Still 179 total detachment records, 17 armies.
- `detachment_parser.py`: `ARMY_TO_MFM` and `MFM_SOURCE_NAME` re-pointed for CSM/DG/TS at v1.1.
- `detachment_effects.json`: checked, confirmed unaffected, **untouched** (hash unchanged from
  S211).
- `rules_assertions.py`: checked, confirmed unaffected, **untouched**. 122/122 assertions still pass.
- `faction_taxonomy.json`: no change needed — all three factions already `built: true`.
- `40K_Decision_Log.md`: D306 appended.
- `DECISION_INDEX.md`: D306 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: top summary updated (24 open, unchanged count — nothing closed, nothing
  new opened); B89's body gained the S212 fix confirmation and the SM-family group recommendation
  for next.
- `units.json`, `unit_loadouts.json`, `abilities.json`, `weapon_abilities.json`,
  `wargear_points.json`, `datasheet_wargear_abilities.json`, `index.html`, `loadout_parser.py`,
  `equipped_parser.py`, `mfm_points_parser.py`, `bundled_swaps.json`: **untouched.**
- `units_repro_check.py`, `repro_check.py`, `detachments_repro_check.py`: all byte-identical.
- All JS harness gates re-run and pass.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged;
   ideally scrub git history).
2. Push this session's changed files to the public repo (listed below).

## Decisions waiting on Ryan

None new this session. B110 (Grey Knights detachments sequencing) and B111 (`WARGEAR_RE` regex gap)
remain as carried from S211/prior — no new information on either this session.

## Files (SHA-256, first 12)

Verify these at S213 open.

| file | sha256:12 | note |
|------|-----------|------|
| `detachments.json` | `03fbde98ba2f` | 7 CSM/DG/TS records changed, 0 added/removed elsewhere |
| `detachment_parser.py` | `1236a6449eae` | CSM/DG/TS re-pointed to v1.1 in two maps |
| `40K_Decision_Log.md` | (regenerated at close) | D306 full prose entry appended |
| `DECISION_INDEX.md` | (regenerated at close) | D306 entry |
| `OPEN_ITEMS_BACKLOG.md` | (regenerated at close) | B89 gained S212 fix confirmation, stays open |
| `pipeline_manifest.py` | (regenerated at close) | `SESSION_HANDOFF_212.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S213 |
| `SESSION_HANDOFF_212.md` | (this file) | |

`detachment_effects.json` unchanged from S211 (`ad7aae235836`) — checked, not touched.
`units.json`, `unit_loadouts.json`, `abilities.json`, `weapon_abilities.json`,
`wargear_points.json`, `datasheet_wargear_abilities.json`, `rules_assertions.py`, `index.html`,
`loadout_parser.py`, `equipped_parser.py`, `mfm_points_parser.py`, `bundled_swaps.json`,
`source_manifest.json`, `baseline.sh`, `faction_taxonomy.json`: **untouched**, no entry needed.

## Backlog

24 open at S211 close; 24 open here (nothing closed, nothing new opened — B89 advanced, did not
close). Beginning: B111, B110, B109, B108, B99, B98, B97, B103, E28, B93, B90, B94, B89, B85, B86,
B69, B70, B75, P2, P4, E23, B67b, E12, B17 (24). Resolved: none. Added: none. Ending: B111, B110,
B109, B108, B99, B98, B97, B103, E28, B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4, E23,
B67b, E12, B17 (24).
