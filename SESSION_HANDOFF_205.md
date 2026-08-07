# SESSION HANDOFF 205

**Turn type:** tooling-only. `equipped_parser.py` and `rules_assertions.py` changed.
`unit_loadouts.json` regenerated (mechanical consequence of the parser fix, not new faction data).
`pipeline_manifest.py` updated (GUARDED list). No engine, no new data sources.

## What happened

1. **Baseline reconciled at open.** All JS harness checks pass. `units_repro_check` and
   `detachments_repro` pass. `repro_check` fails on exactly the 8 units documented in S204 (the
   B104 bug) — expected and confirmed. Manifest/rules_assertions fail on absent old handoffs
   (routine housekeeping).

2. **B104 fixed (D298).** Root cause re-derived from source (not trusted from S204's prose).
   `equipped_parser.py`'s `scoped_name2id` had an insertion-order-dependent `cands[-1]` fallback
   that silently corrupted shared-name vehicles whenever a new faction was appended to `units.json`.
   Two problems confirmed against real data:
   - **Scope alias gap:** `Space_Marines_web.txt` derived scope `Space Marines`, which didn't match
     the army block name `Adeptus Astartes`, so scope fell to None and ALL multi-candidate names
     resolved to `cands[-1]`.
   - **Chapter fallback gap:** `Dark_Angels_web.txt` and `Space_Wolves_web.txt` correctly resolved
     scope to their block names, but for shared vehicles (candidates: AA, BT, GK) no candidate
     matched the chapter scope, so they also fell to `cands[-1]`.

   **The fix** — three mechanisms:
   - `load_scope_maps()` reads `faction_taxonomy.json` and builds two maps: `scope_aliases`
     (`Space Marines` → `Adeptus Astartes`) and `parent_armies` (all Astartes chapters → `Adeptus
     Astartes`). Degrades gracefully if the taxonomy file is absent.
   - `scoped_name2id` now resolves in order: exact scope match → parent-army fallback → `cands[-1]`
     (only for unresolvable cases). This is deterministic and insertion-order-stable.
   - **Propagation:** `scoped_name2id` returns a second value: a propagation map
     (`{primary_uid: [other_uids]}`). After `segment()` attributes composition text to a primary uid,
     the caller copies it to all other candidates sharing the same name — because a "Gladiator Lancer"
     in `Space_Marines_web.txt` describes the same physical loadout whether the unit belongs to Adeptus
     Astartes or Black Templars. This prevents a regression where BT entries would lose their equipped
     data (they had it via the buggy fallback before).

3. **Verification — two regeneration runs, both confirmed.**
   - **Without GK in FACTIONS:** 7 Adeptus Astartes entries gain correct `_defaults_source=equipped`
     and `default_weapon_counts` they were previously missing. All 8 S204 critical units match
     committed file. All BT entries byte-identical to committed. All Chaos entries byte-identical.
   - **With GK added to FACTIONS:** 25 new GK entries, zero existing entries changed vs the no-GK
     run. All 8 critical units identical whether GK is present or not. The B104 bug is dead.
   - Both verified at field level (default_weapons, default_weapon_counts, _defaults_source) for
     the 8 critical units plus unrelated samples from CSM, DG, and hand-authored entries.

4. **`unit_loadouts.json` regenerated (without GK in FACTIONS).** The 7 AA improvements are a
   mechanical consequence of the parser fix, not new faction data. Repro_check confirmed
   byte-identical reproduction. GK not added to `repro_check.py`'s FACTIONS — that's the loadouts
   data turn, not this one.

5. **B104 assertion added to `rules_assertions.py`.** Synthetic fixture testing 6 sub-checks:
   direct scope match, alias match, parent fallback, insertion-order stability (adding a new
   candidate doesn't change results), single-candidate stability, and propagation-map correctness.
   Passes against the fixed parser; fails against the old one.

## The 7 AA improvements (pre-existing gap, now corrected)

These units previously had `_defaults_source=None` because the SM web pass fell through to
scope=None and routed their composition text to BT entries instead of AA entries. Now corrected:

| unit_id | unit_name | change |
|---------|-----------|--------|
| 000000066 | Land Raider Crusader | gained `Hurricane bolter: 2` |
| 000001667 | Gladiator Reaper | gained `Tempest bolter: 2` |
| 000001825 | Gladiator Valiant | gained `Multi-melta: 2` |
| 000002568 | Impulsor | gained `Storm bolter: 2` |
| 000002705 | Gladiator Lancer | gained `Storm bolter: 2` |
| 000002721 | Repulsor | gained `_defaults_source=equipped` (weapons unchanged) |
| 000002722 | Repulsor Executioner | gained `_defaults_source=equipped`; lost `Ironhail heavy stubber` from defaults (confirmed: it is an add-on option, not a default weapon per the composition text) |

## State at close

- `equipped_parser.py`: B104 fix shipped. New `--taxonomy` argument (optional, default
  `faction_taxonomy.json`). `scoped_name2id` returns `(name2id, propagation_map)`.
- `rules_assertions.py`: B104 assertion added. Count now 120 (was 119).
- `unit_loadouts.json`: regenerated with fixed parser; 7 AA entries improved; all other entries
  byte-identical. `repro_check` passes.
- `pipeline_manifest.py`: `SESSION_HANDOFF_205.md` appended to GUARDED list.
- `repro_check.py`: `FACTIONS` unchanged (GK not added — that's the loadouts data turn).
- `index.html`, `loadout_parser.py`, `detachment_parser.py`, `units.json`: untouched.
- `OPEN_ITEMS_BACKLOG.md`: **23 open** (down from 24 — B104 closed).

## Ryan action required

1. Push this session's changed files to the repo (listed below).
2. No product decision waiting.

## Decisions waiting on Ryan

None blocking.

## Files (SHA-256, first 12)

Verify these at S206 open.

| file | sha256:12 | note |
|------|-----------|------|
| `equipped_parser.py` | `8cc4cdc2685b` | B104 fix: scope alias + parent fallback + propagation |
| `rules_assertions.py` | `f767cdb962df` | B104 assertion added; 120 total |
| `unit_loadouts.json` | `42f3ad99ebb7` | 7 AA entries improved; all else byte-identical |
| `pipeline_manifest.py` | `e3880603027b` | S205 handoff appended to GUARDED |
| `40K_Decision_Log.md` | `68375fc125af` | D298 full prose entry appended |
| `DECISION_INDEX.md` | `2997f05243d6` | D298 entry |
| `OPEN_ITEMS_BACKLOG.md` | `1d4fe5b95154` | B104 closed; 23 open |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S206 |
| `SESSION_HANDOFF_205.md` | (this file) | hash banked by `--write` once S203 gap is resolved |
| `pipeline_manifest.json` | (not regenerated) | `--write` blocked by absent `SESSION_HANDOFF_203.md` — see note |

**Manifest gap:** `pipeline_manifest.py --write` cannot run because `SESSION_HANDOFF_203.md` is
absent from both the repo and the project area. It was apparently never pushed (first visible in
S204's baseline `fetch-verify` failure, confirmed this session against a fresh clone). Ryan action:
either locate and push S203's content, or remove it from GUARDED in `pipeline_manifest.py`, then
run `--write` and `--freshness-check` before starting S206.

`units.json`, `index.html`, `loadout_parser.py`, `detachment_parser.py`, `repro_check.py`,
`detachments.json`, `abilities.json`, `weapon_abilities.json`, `datasheet_wargear_abilities.json`:
**untouched**, no entry needed.

## Backlog

24 open at S204 close, down to 23 here (B104 closed, none added). Beginning: B104, B105, B106,
B99, B98, B97, B103, E28, B93, B90, B94, B89, B100, B85, B86, B69, B70, B75, P2, P4, E23, B67b,
E12, B17 (24 — matches S204's ending count). Resolved: B104. Added: none. Ending: B105, B106, B99,
B98, B97, B103, E28, B93, B90, B94, B89, B100, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12,
B17 (23).
