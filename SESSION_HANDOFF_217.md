# SESSION HANDOFF 217

**Turn type:** scoping-only (World Eaters — next faction in priority order). No committed pipeline
file touched: not `units.json`, not `unit_loadouts.json`, not `wargear_points.json`, not
`detachments.json`. All parser runs were dry runs into throwaway temp directories.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: 33/34 gates green. The one
   red was the documented, expected pre-existing B108 finding (unchanged, your action). Private
   source repo fetched and verified fresh: 85/85 source files byte-match `source_manifest.json`.

2. **World Eaters scoped.** `WORLD_EATERS_BUILD_SCOPE.md` written (net-new), full write-up there.
   Summary:
   - **30 datasheets, matches the MFM exactly.** 28 Legends/Forge World exclusions confirmed both
     directions — manual cross-reference against the MFM text before running anything, then the
     transform's own dry run independently named the identical 28.
   - **"Blood Legions" allied-Daemon block** (Bloodcrushers, Bloodletters, Bloodthirster, Flesh
     Hounds, Skarbrand) confirmed already-wired — `ALLIED_GROUP_HEADERS` (B61) already recognises
     it by name alongside DG/TS/EC's equivalents; Death Guard's own five Nurgle-Daemon units are
     the shipped precedent for building these as native World Eaters entries.
   - **Leader mapping** (5 `LEADER` blocks) cross-checked against `Datasheets_leader.csv`
     independently of the MFM text — exact match, zero discrepancies.
   - **Build from v1.1** per D293: two force-disposition changes (Brazen Engines, Butchers of
     Khorne), two `UNIQUE TAG REMOVED` events (zero unique tags remain in v1.1), one enhancement
     re-price (Archslaughterer 40→30).
   - **Full pipeline dry run clean**: `wahapedia_transform.py` → `mfm_points_parser.py` →
     `convert_to_json.py`, 0 collisions, 0 unmatched datasheets, 5 leader overrides matching
     Section 3 exactly, 3 wargear items priced (all three already exist in the committed
     `wargear_points.json` from sibling Defiler/Forgefiend factions).
   - **`loadout_parser.py --factions WE`** against a merged 19-army `units.json` flagged exactly
     **2 of 30**: Jakhals (a genuinely new two-option composition shape, confirmed unique by direct
     grep across the full composition CSV) and Helbrute (already-solved — the identical sentence
     ships on three sibling factions' Helbrutes today).
   - **No engine work needed for World Eaters.**

3. **Two findings logged, neither touched this session.**
   - **B113 opened** — a detachment enhancement `LEADER:` eligibility restriction (e.g. Cult of
     Blood's Butcher Lord → Goremongers/Jakhals only) is discarded as parser noise by
     `detachment_parser.py`. Confirmed pre-existing and unenforced on 3 already-shipped factions
     (CSM ×2, TS ×1, EC ×1) — not a World Eaters blocker, just newly counted (World Eaters would
     add 2 more instances of the same gap).
   - **B112 unblocked** — a v1.1 Chaos Daemons MFM file now exists in the private repo, absent as
     of S214 when B112 opened. Found incidentally while confirming the private repo's file list for
     World Eaters; not investigated further. Ready for its own data-only turn.

## State at close

- No committed pipeline file changed. `WORLD_EATERS_BUILD_SCOPE.md` is the only substantive new
  artifact.
- `40K_Decision_Log.md`: D311 appended.
- `DECISION_INDEX.md`: D311 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: B113 added to Open Items; B112's body updated (unblocked, not closed);
  ledger header updated, 22 → 23 open.
- `pipeline_manifest.py`: `SESSION_HANDOFF_217.md` registered in GUARDED before `--write`.
- All committed pipeline files untouched: `index.html`, `units.json`, `unit_loadouts.json`,
  `wargear_points.json`, `detachments.json`, `detachment_effects.json`, `rules_assertions.py`,
  `loadout_parser.py`, `equipped_parser.py`, `detachment_parser.py`, `faction_taxonomy.json`,
  `bundled_swaps.json`, `source_manifest.json`, `baseline.sh`, `mfm_points_parser.py`,
  `wahapedia_transform.py`, `convert_to_json.py`, `units_repro_check.py`, `merge_factions.py`.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged;
   ideally scrub git history), and push it to the private source repo.
2. Push this session's changed/new files to the public repo (listed below).

## Decisions waiting on Ryan

None. World Eaters scoping surfaced zero "how it works" questions — every ambiguity resolved from
source (MFM text, `Datasheets_leader.csv`, existing shipped precedent).

## Files (SHA-256, first 12)

Verify these at S218 open.

| file | sha256:12 | note |
|------|-----------|------|
| `WORLD_EATERS_BUILD_SCOPE.md` | `591c54f0869d` | net-new, S217 scoping pass |
| `40K_Decision_Log.md` | `da7843a5e471` | D311 appended |
| `DECISION_INDEX.md` | `e8814f97c66c` | D311 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `fa85e9dcd6b4` | B113 opened, B112 unblocked-not-closed, ledger 22→23 |
| `pipeline_manifest.py` | `543897a674bc` (pre-`--write`; re-pinned by `--write`) | `SESSION_HANDOFF_217.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S218 |
| `SESSION_HANDOFF_217.md` | (this file) | |

## Net New Files

- `WORLD_EATERS_BUILD_SCOPE.md` — no file has previously played this role for World Eaters.

## Backlog

22 open at S216 close; 23 open here (B113 opened, nothing closed; B112 unblocked but stays open
until its own data turn).
Beginning: B110, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4,
E23, B67b, E12, B17, B112 (22). Resolved: none (0). Added: B113 (1). Ending: B113, B110, B108, B99,
B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17, B112 (23).
