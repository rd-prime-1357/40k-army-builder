# SESSION HANDOFF 224

**Turn type:** data-only (Drukhari units — build `units.json` for the 23-unit roster).
`units.json`, `abilities.json`, `weapon_abilities.json`, `datasheet_wargear_abilities.json`,
`faction_taxonomy.json`, `units_repro_check.py` changed. `detachments.json`, `unit_loadouts.json`,
`detachment_parser.py`, `index.html` untouched. Closes no numbered backlog ticket — Drukhari's
build is part of the standing faction-priority-order sequence, not its own item. See D318.

## What happened

1. **Open-time baseline clean.** `./baseline.sh --fetch --data-turn`: 34/34 gates, 85 source files
   verified, B115's `FOREIGN_SOURCE_OWNER` fix confirmed present in the fetched
   `wahapedia_transform.py`.

2. **Real (non-scratch) transform run, re-derived from source, not trusted from S222/S223's
   dry-run numbers.** `wahapedia_transform.py --faction DRU --army-name Drukhari` selects exactly
   23 datasheets (24 stats rows — Incubi splits into INCUBI/KLAIVEX model groups). Matches
   `DRUKHARI_BUILD_SCOPE.md` §1 exactly. `mfm_points_parser.py` against `MFM_Drukhari_v1.1.txt`
   and the real build output: 0 "no MFM points" datasheets, 7 Legends-only MFM entries with no
   datasheet match, 1 attach-list drop (Archon → Court of the Archon, B73/D260 guard) — an exact
   match to S222/S223's numbers, now proven against the real build rather than a scratch dir.

3. **`units_repro_check.py` extended with a Drukhari block**, mirroring the Grey Knights/Emperor's
   Children/World Eaters pattern exactly: transform → mfm points → `convert_to_json.py
   --emit-fourth-plus` (needed for Raider/Venom's 1st-to-3rd/4th+ tier shape), in its own working
   dir, fully self-sourced. `MFM_Drukhari_v1.1.txt` added to `REQUIRED`. `dru_json` wired into the
   `merge_factions.py` call alongside the other seven faction outputs.

4. **`faction_taxonomy.json`** — Drukhari's entry flipped from `built: false` to `built: true` /
   `data_army: "Drukhari"`, matching the Grey Knights/World Eaters entry shape exactly.

5. **Rebuild verified field-by-field against source, not just "ran clean."** All 23 unit names
   match the scope roster; all 6 Leader attach lists match exactly (Archon → Hand of the
   Archon/Incubi/Kabalite Warriors, Drazhar → Incubi, Haemonculus → Wracks, Lady Malys → Hand of
   the Archon/Incubi/Kabalite Warriors, Lelith Hesperax → Wyches, Succubus → Wyches); Raider
   (75/75/75/85), Venom (65/65/65/75), and Ravager (110 flat) points match the v1.1 tier shapes
   exactly.

6. **Diffed against a clean fetch of the public repo, not the project mount** (the mount doesn't
   carry `abilities.json` at all — storage-constraint artifact, not a real absence). `units.json`:
   +23 unit_ids, 0 existing units changed. `abilities.json`: +59, `weapon_abilities.json`: +8,
   `rules.json`/`keywords.json`: +0 (Drukhari's keywords are all already-shared generic ones).
   Zero removals anywhere.

7. **`datasheet_wargear_abilities.json` regenerated** against the new `units.json` (its only real
   input besides `Datasheets_abilities.csv` — independent of `unit_loadouts.json`): +6 datasheet
   entries (Archon, Kabalite Warriors, Incubi, Hellions, Scourges with Shardcarbines, Hand of the
   Archon), purely additive.

8. **`wargear_points.json` checked and correctly left unchanged.** `build_wargear_points()` gates
   every priced item on `reachable_items()` from `unit_loadouts.json`; Drukhari has no loadout
   groups authored yet (that's the next tooling turn per `DRUKHARI_BUILD_SCOPE.md` §7/§8), so its
   4 wargear items (Ravager's Dark lance, Scourges' Haywire blaster/Dark lance, Talos's Twin
   haywire blaster) don't populate yet. Confirmed by rerunning the full price-rebuild path and
   diffing, not assumed from the turn-type boundary alone.

9. **Detachment-map registration — the prompt's own step 3 — deferred, correcting the prompt.**
   Registering Drukhari in `detachment_parser.py`'s three maps was tested directly: it makes
   `detachment_parser.py --root` attempt to build Drukhari's detachments immediately (no
   "registered but not shipped" allowlist exists), and since Drukhari's `detachments.json` content
   doesn't exist yet, the rebuild diverges from committed (1,096,218 vs 1,056,124 bytes) and
   `detachments_repro_check` fails. Left unregistered, this would fail that gate at every session
   open between now and the detachments build turn — not permitted under the standing rule against
   carrying a failing gate forward in prose. Reverted; `detachment_parser.py` is byte-identical to
   the fetched original. Registration will ship together with the detachments build itself.

10. **Full baseline re-run with all changes in place.** `units_repro_check` and
    `detachments_repro_check` both byte-identical to committed; `rules_assertions` 121/122 (the one
    red is the expected P3 manifest-drift for the six edited files, cleared by `--write` below);
    every harness clean — zero regression to any already-built faction.

## Not investigated this session

B113, B114, GK §6/§7 untouched — different turn types (engine/scoping), not mixed with this data
turn per the standing rule. Loadouts (§7) and detachments (§5, including the deferred map
registration) are the next two Drukhari turns, per `DRUKHARI_BUILD_SCOPE.md` §8's sequencing —
not started this session.

## State at close

- `units.json`: +23 units (Drukhari), 0 existing units changed.
- `abilities.json`, `weapon_abilities.json`: purely additive (+59, +8).
- `rules.json`, `keywords.json`: unchanged (0 new entries — Drukhari's keywords are all
  already-shared generic ones).
- `datasheet_wargear_abilities.json`: +6 datasheet entries, purely additive.
- `faction_taxonomy.json`: Drukhari flipped to `built: true` / `data_army: "Drukhari"`.
- `units_repro_check.py`: Drukhari block added, mirrors Grey Knights/Emperor's Children/World
  Eaters pattern.
- `wargear_points.json`, `unit_loadouts.json`, `detachments.json`, `detachment_parser.py`,
  `index.html`: untouched.
- `40K_Decision_Log.md`: D318 appended. `DECISION_INDEX.md`: D318 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: ledger header updated to S224, count unchanged at 23 (no ticket
  closes or opens — Drukhari's build isn't a numbered backlog item).

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged).
2. **Push `OUTPUT_FORMAT_SPEC_for_project_instructions.md` to the public repo** (still outstanding
   from S220).
3. **Push `pipeline_manifest.json`** — still outstanding from S223's open-time reconciliation
   (unchanged; not re-diagnosed here).
4. Push this session's new/changed files to the public repo: `units.json`, `abilities.json`,
   `weapon_abilities.json`, `datasheet_wargear_abilities.json`, `faction_taxonomy.json`,
   `units_repro_check.py`, `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
   `pipeline_manifest.py`/`.json`, this handoff, `NEXT_SESSION_PROMPT.md`.

## Decisions waiting on Ryan

**B116** — unchanged (Drukhari's Harlequins/Anhrathe allied-inclusion mechanic; see
`DRUKHARI_BUILD_SCOPE.md` §6). Not touched this session.

## Files (SHA-256, first 12)

Verify these at S225 open.

| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | (computed by `--write`) | +23 Drukhari units |
| `abilities.json` | (computed by `--write`) | +59 entries, additive |
| `weapon_abilities.json` | (computed by `--write`) | +8 entries, additive |
| `datasheet_wargear_abilities.json` | (computed by `--write`) | +6 entries, additive |
| `faction_taxonomy.json` | (computed by `--write`) | Drukhari built:true |
| `units_repro_check.py` | (computed by `--write`) | Drukhari block added |
| `40K_Decision_Log.md` | (computed by `--write`) | D318 appended |
| `DECISION_INDEX.md` | (computed by `--write`) | D318 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | (computed by `--write`) | ledger header S224, count unchanged (23) |
| `pipeline_manifest.py` | (hash not self-referential — see S223's note) | `SESSION_HANDOFF_224.md` appended to GUARDED |
| `pipeline_manifest.json` | (hash not self-referential) | regenerated by `--write` at close |
| `NEXT_SESSION_PROMPT.md` | (informational only, never guarded) | S225 |
| `SESSION_HANDOFF_224.md` | (this file, hash not self-referential) | |

Per S223's precedent: `pipeline_manifest.py`'s own row is deliberately left uncomputed here — its
final hash is only known once `--write` has run against it. Verify `pipeline_manifest.py` and
`pipeline_manifest.json` directly at S225 open (`python3 pipeline_manifest.py`).

## Net New Files

None this session. `units_repro_check.py`, the four merged lookups, `datasheet_wargear_abilities.json`,
`faction_taxonomy.json`, the decision log, decision index, backlog, `pipeline_manifest.py`/`.json`,
and the next-session prompt are all updates to files the project has held before. `units.json`
itself is an update (new faction data inside an existing, versioned file), not a new file.

## Backlog

23 open at S223 close; **23 open at S224 close** (unchanged — Drukhari's units build advances the
standing faction-priority-order sequence but isn't its own backlog ticket; nothing closed, nothing
opened).

Beginning: B116, B114, B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70,
B75, P2, P4, E23, B67b, E12, B17 (23). Resolved: none (0). Added: none (0). Ending: B116, B114,
B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b,
E12, B17 (23).
