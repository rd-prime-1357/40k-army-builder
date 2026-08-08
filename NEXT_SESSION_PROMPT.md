# NEXT SESSION PROMPT — Session 224

## Recommended turn type: data-only (Drukhari units — build `units.json` for the 23-unit roster)

Read `SESSION_HANDOFF_223.md` first, then `DRUKHARI_BUILD_SCOPE.md` (still the authoritative
scoping writeup — nothing in it changed this session except that B115 is now fixed). B115 is
closed: `wahapedia_transform.py --faction DRU` now selects exactly 23 datasheets, verified by
direct rerun, zero regression to any other faction.

Open with `./baseline.sh --fetch --data-turn`. Confirm clean before starting. If it fails, reconcile
before starting work — do not carry a failing gate forward in prose (this happened at S223 open;
see D317 for how it was diagnosed and fixed).

## The build

1. Run the fixed `wahapedia_transform.py --faction DRU --army-name Drukhari` for real (not a dry
   run to a scratch dir) and confirm 23 datasheets, matching `DRUKHARI_BUILD_SCOPE.md` §1.
2. Run `mfm_points_parser.py` against `MFM_Drukhari_v1.1.txt` and the new stats output; confirm
   zero "no MFM points" datasheets (S223 already proved this against the same fixed selection in a
   scratch dir — re-verify against the real build output, don't just trust the scratch-dir rerun).
3. Register Drukhari (`DRU`) in `detachment_parser.py`'s three maps (`ARMY_TO_MFM`,
   `MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`) — not yet done, confirmed absent at S222 scoping.
4. Build `units.json` for the 23-unit roster via the normal pipeline path
   (`units_repro_check.py`'s per-faction block, same pattern as every prior faction build).
5. Diff-guard the regenerated `units.json` and any companion regenerations
   (`wargear_points.json`, `datasheet_wargear_abilities.json`) field-by-field against what's
   committed — "ran clean" is not sufficient, per standing discipline.
6. Loadouts are NOT this turn's scope — `DRUKHARI_BUILD_SCOPE.md` §7's 13 wargear-option groups
   are a separate tooling turn per the suggested sequencing, and detachments (§5, 9 detachments)
   are a separate data turn after that. Keep this turn to units only, per the never-mix rule.

## Also open, at your discretion

- **B113** — detachment enhancement `LEADER:` eligibility restriction discarded as parser noise (6
  instances across CSM/TS/EC/World Eaters; GK, CD, and Drukhari all confirmed to add 0 more).
  Engine turn, small, not urgent. Different turn type than this session — do not fold in.
- **B114** — Chaos Daemons' `Shadow Legion` HERETIC ASTARTES unlock (`detachment_effects.json`) is
  recorded `enforced: false` on a now-stale premise (CSM has been built since S212). Needs its own
  scoping pass before it can be flipped. Different turn type — do not fold in.
- **GK §6 / §7** — carried unchanged for several sessions now; still not investigated.
- **Repo push (Ryan's action)** — `OUTPUT_FORMAT_SPEC_for_project_instructions.md` and
  `Thousand_Sons_web.txt` (B108) both still outstanding. This session adds a third:
  `pipeline_manifest.json` needs pushing too — the S223 open-time reconciliation (D317) means the
  repo's copy is currently stale for two entries; `repo_check.py` will show a `DIFFERS` finding on
  `pipeline_manifest.json` until Ryan pushes S223's output. Expected, not a new problem — don't
  re-diagnose it, just confirm the push landed.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's own numbers.
- Turn typing: this is a data turn. Units only. Detachments and loadout-group authoring are
  separate, later turns per `DRUKHARI_BUILD_SCOPE.md` §8's sequencing.

## Decisions waiting on Ryan

**B116** — unchanged. Whether/when to build Drukhari's Harlequins/Anhrathe cross-book
allied-inclusion mechanic (see `DRUKHARI_BUILD_SCOPE.md` §6). Recommendation is still to defer past
the initial Drukhari build. Does not block this session.

## Close

Produce the four documents, register `SESSION_HANDOFF_224.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
