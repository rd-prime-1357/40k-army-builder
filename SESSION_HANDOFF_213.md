# SESSION HANDOFF 213

**Turn type:** data-only (B89 — Space Marines-family group detachment v1.1 fix, D307).
`detachment_parser.py` and `detachments.json` changed. `detachment_effects.json` and
`rules_assertions.py` checked directly and confirmed unaffected — neither touched. No engine file
(`index.html`, `loadout_parser.py`, `equipped_parser.py`, `mfm_points_parser.py`) touched.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: 33/34 gates green, sources
   loaded (85 files verified against `source_manifest.json`), 122/122 assertions, all three repro
   checks byte-identical. `repo_check` red on exactly the pre-existing B108 finding
   (`Thousand_Sons_web.txt` in the public repo), unchanged.

2. **Direct parse-and-diff run on all six registered v1_0 detachment files against their v1.1
   counterparts before touching anything** — per the S213 prompt's instruction not to assume D291's
   prose note was exhaustive. Confirmed the diff was real and materially larger than the three-faction
   CSM/DG/TS turn, as D291 itself warned it might be.

3. **Re-pointed `ARMY_TO_MFM` and `MFM_SOURCE_NAME` for the six-file Space Marines group** (base
   Adeptus Astartes, Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves) from v1_0
   to v1.1 (`MFM_Space_Marines_v1.1.txt`, `MFM_Black_Templars_v1.1.txt`, `MFM_Blood_Angels_v1.1.txt`,
   `MFM_Dark_Angels_v1.1.txt`, `MFM_Death_Watch_v1.1.txt`, `MFM_Space_Wolves_v1.1.txt`), mirroring
   the CSM/DG/TS and Emperor's Children precedent. `source_manifest.json` needed no change — both
   versions of all six files were already hashed and present.

4. **Regenerated `detachments.json`, diff-guarded at record-key level against the committed file.**
   6 keys added, 0 removed, 50 changed — 179 to 185 distinct detachment records, 17 armies
   unchanged.
   - **Added (6):** a new "Vengeful Hosts" detachment (1DP, Take and Hold), one record per source
     file — Space Marines, Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves. No
     faction-pack or Wahapedia prose exists yet for its ability text (`text_source: none`) — checked
     against the pre-existing pattern rather than assumed benign: 14 other committed detachments
     already carry `text_source: none`, so this is not a new gap shape.
   - **Changed (50):** 37 force-disposition corrections, each verified against the raw MFM's own
     explicit "UPDATED — FORCE DISPOSITION(S) CHANGED" marker directly above the affected
     detachment, not inferred from the value change alone. 13 enhancement price changes across five
     enhancement names — Artificer Armour (10→20, six factions), The Flesh Is Weak (10→20, six
     factions), Fusillade (20→25, five factions), Temporal Corridor (15→25, five factions), Armour
     of Antoninus (10→20, Space Marines only), Stalwart Champion (25→15, Dark Angels only). All
     match the raw MFM's ▲/▼ price-change markers. No DP changes and no unique-tag changes surfaced
     in this group.

5. **Checked, not assumed: `detachment_effects.json` and `rules_assertions.py` against the full
   56-key changed-or-added set.** Programmatic set-intersection against `detachment_effects.json`'s
   16 keys (including these six factions' Headhunter Task Force entries, Blood Angels' The Lost
   Brethren, Dark Angels' Company of Hunters) returned zero overlap — no update needed. Text search
   of `rules_assertions.py` for every changed/added detachment name and enhancement name returned
   zero matches — no assertion needed reconciling.

6. **`faction_taxonomy.json`: confirmed directly, not assumed, that all twelve Adeptus Astartes
   chapters are already `built: true`** — no change needed.

7. **B89 CLOSED.** This session closes the detachments-side v1_0-sourcing gap for the entire
   Adeptus Astartes group (S212 closed it for CSM/Death Guard/Thousand Sons; this session closes it
   for the six-file Space Marines group). The only remaining piece of the original gap — Chaos
   Daemons' LORDS OF THE WARP disposition — cannot be confirmed or fixed because GW has not
   published a v1.1 Chaos Daemons detachment file. Rather than leave B89 open indefinitely on an
   externally-blocked item, that piece was split off as **B112** (new, blocked on GW publication).

8. **Backlog housekeeping, in scope of the same rolling-document update:** found and fixed a
   pre-existing duplicate B109 entry in `OPEN_ITEMS_BACKLOG.md` (two separate ticket bodies under
   the same ID, one stale — "not yet scoped" — and one current — render site located at S209). Kept
   the current one, removed the stale duplicate. Verified against the pre-session committed file
   that the duplicate predates this session, not introduced by it.

## State at close

- `detachments.json`: 6 records added, 50 changed, 0 removed elsewhere. 185 total detachment
  records (up from 179), 17 armies. `detachments_repro_check.py` byte-identical against the
  regenerated file.
- `detachment_parser.py`: `ARMY_TO_MFM` and `MFM_SOURCE_NAME` re-pointed for the six-file Space
  Marines group at v1.1. Only Chaos Daemons remains on a v1_0 detachment source (correct — no v1.1
  file exists).
- `detachment_effects.json`: checked, confirmed unaffected, **untouched** (hash unchanged from
  S212).
- `rules_assertions.py`: checked, confirmed unaffected, **untouched**. 122/122 assertions still
  pass (full gate suite re-run after the data change — all pass except `pipeline_manifest`, which
  fails only on the not-yet-rewritten manifest hash, not a real problem).
- `faction_taxonomy.json`: no change needed — all twelve Adeptus Astartes chapters already
  `built: true`.
- `40K_Decision_Log.md`: D307 appended.
- `DECISION_INDEX.md`: D307 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: B89 closed (full body moved to Closed/Shipped, pointer left in place);
  B112 opened (Chaos Daemons detachments blocker); stale duplicate B109 entry removed. 24 open
  (unchanged count — one closed, one opened).
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
remain as carried from prior sessions — no new information on either this session. B112 is a new
ticket but is a dev-manager sequencing/tracking decision (blocked on an external GW publication),
not a decision that needs Ryan's input.

## Files (SHA-256, first 12)

Verify these at S214 open.

| file | sha256:12 | note |
|------|-----------|------|
| `detachments.json` | `7e107c92972a` | 6 added, 50 changed, 0 removed elsewhere |
| `detachment_parser.py` | `df7211dc35bc` | Six-file Space Marines group re-pointed to v1.1 |
| `40K_Decision_Log.md` | (regenerated at close) | D307 full prose entry appended |
| `DECISION_INDEX.md` | (regenerated at close) | D307 entry |
| `OPEN_ITEMS_BACKLOG.md` | (regenerated at close) | B89 closed, B112 opened, duplicate B109 removed |
| `pipeline_manifest.py` | (regenerated at close) | `SESSION_HANDOFF_213.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S214 |
| `SESSION_HANDOFF_213.md` | (this file) | |

`detachment_effects.json` unchanged from S212 (`ad7aae235836`) — checked, not touched.
`units.json`, `unit_loadouts.json`, `abilities.json`, `weapon_abilities.json`,
`wargear_points.json`, `datasheet_wargear_abilities.json`, `rules_assertions.py`, `index.html`,
`loadout_parser.py`, `equipped_parser.py`, `mfm_points_parser.py`, `bundled_swaps.json`,
`source_manifest.json`, `baseline.sh`, `faction_taxonomy.json`: **untouched**, no entry needed.

## Backlog

24 open at S212 close; 24 open here (B89 closed, B112 opened — net unchanged). Beginning: B111,
B110, B109, B108, B99, B98, B97, B103, E28, B93, B90, B94, B89, B85, B86, B69, B70, B75, P2, P4,
E23, B67b, E12, B17 (24). Resolved: B89 (24). Added: B112 (1). Ending: B111, B110, B109, B108, B99,
B98, B97, E28, B93, B90, B94, B112, B103, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (24).
