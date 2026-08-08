# SESSION HANDOFF 219

**Turn type:** data-only (World Eaters detachments — per `WORLD_EATERS_BUILD_SCOPE.md` §9 step 2).
`detachments.json`, `detachment_effects.json`, `faction_taxonomy.json` shipped end to end. World
Eaters is now fully built (units + detachments both complete) and selectable.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: 33/34 gates green. The one
   red was the documented, expected pre-existing B108 finding (unchanged, your action). Private
   source repo fetched and verified fresh: 85/85 source files byte-match `source_manifest.json`.

2. **`WE` registered in `detachment_parser.py`'s three maps** (`ARMY_TO_MFM`, `MFM_SOURCE_NAME`,
   `ARMY_TO_WAHA_FACTION`), mirroring the Emperor's Children pattern (D305) exactly.

3. **`detachments.json` built** from `MFM_World_Eaters_v1.1.txt` per D293 (always the newest MFM).
   Diff-guarded: **8 World Eaters detachments added, 0 changed, 0 removed elsewhere.** Verified
   directly against `WORLD_EATERS_BUILD_SCOPE.md` §4's forecast: Brazen Engines' force disposition
   Purge the Foe → Disruption; Butchers of Khorne's Disruption → Take and Hold; zero `UNIQUE:` tags
   remain anywhere in the source file (confirmed by direct text search, not assumed) — Brazen
   Engines and Goretrack Onslaught's shared `UNIQUE: ONSLAUGHT` tag is gone from both;
   Archslaughterer (Vessels of Wrath) re-priced 40 → 30 pts. No DP changes, 8 detachments in both
   MFM versions.

4. **`detachment_effects.json` gained two rows, not the one the scope doc anticipated.** The scope
   doc's instruction was to check directly rather than assume none needed. That check found:
   - **Khorne Daemonkin** — the expected pattern. Rule text: "You can include the Blood Legions
     units in your army," capped 500/1000/1500 pts by battle size, plus "No BLOOD LEGIONS model
     from your army can be your WARLORD." Same shape as Death Guard's Tallyband Summoners,
     Thousand Sons' Changehost of Deceit, Emperor's Children's Carnival of Excess. The five World
     Eaters Blood Legions units already carry `allied_group: "Blood Legions"` in `units.json` (from
     S218's B61 update) — without this row they'd be either unreachable (D0) or offered without
     the points-cap/Warlord gate.
   - **Cult of Blood** — an unflagged second pattern. Rule text's KEYWORDS clause: "JAKHALS and
     GOREMONGERS units from your army have the BATTLELINE keyword." Same shape as Thousand Sons'
     Servants of Change / Warpmeld Pact (Tzaangors). This one wasn't caught by manual scan — it
     surfaced when `rules_assertions.py`'s `e21a_coverage` assertion failed on the full baseline
     re-run after the Khorne Daemonkin row alone, naming `World Eaters|CULT OF BLOOD` directly.
   Both rows diff-guarded: **exactly the two named keys added, 0 changed, 0 removed elsewhere.**

5. **`e21b_check.js`'s battleline-sweep literal updated 7 → 9**, confirmed by the harness's own
   live sweep (not hand-counted): five prior rows (Death Company Marines ×2, Outrider Squad,
   Poxwalkers, Traitor Guardsmen Squad) plus Tzaangors named twice (Servants of Change, Warpmeld
   Pact) plus World Eaters' new Jakhals and Goremongers.

6. **`faction_taxonomy.json`: World Eaters' `built` flag flipped to `true`, `data_army: "World
   Eaters"` added** — same sequencing as D298 (Grey Knights) and D305 (Emperor's Children).

7. **Full baseline re-run** after all five file updates (`detachment_parser.py`, `detachments.json`,
   `detachment_effects.json`, `e21b_check.js`, `faction_taxonomy.json`): every gate green except
   the expected pre-`--write` P3/`pipeline_manifest`/`repo_check` state (resolved by the `--write`
   at the end of this handoff).

## State at close

- `detachments.json`, `detachment_effects.json`, `faction_taxonomy.json`: all updated,
  diff-guarded, byte-verified.
- `detachment_parser.py`: `WE` registered in all three maps.
- `e21b_check.js`: battleline-sweep literal 7 → 9.
- `40K_Decision_Log.md`: D313 appended. `DECISION_INDEX.md`: D313 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: no ticket opened or closed (faction-build turn, not a ticket turn);
  ledger header updated to S219, count unchanged at 23. B113 gains 2 more instances (not a new
  ticket).
- `units.json`, `unit_loadouts.json`, `abilities.json`, `wargear_points.json`,
  `datasheet_wargear_abilities.json`: untouched this session (shipped S218).
- `index.html`: untouched.
- `pipeline_manifest.py`: `SESSION_HANDOFF_219.md` registered in GUARDED before `--write`.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged;
   ideally scrub git history), and push it to the private source repo.
2. Push this session's changed/new files to the public repo (listed below).

## Decisions waiting on Ryan

None. Both construction-effect rows mirror an already-established precedent (D204's allied-unlock/
Warlord shape, D248's BATTLELINE-grant shape) exactly — no new rules-legality call, no lasting
precedent set. World Eaters detachments shipping surfaced zero "how it works" questions.

## Files (SHA-256, first 12)

Verify these at S220 open.

| file | sha256:12 | note |
|------|-----------|------|
| `detachments.json` | `b82e1c38020e` | +8 World Eaters detachments |
| `detachment_effects.json` | `2f067dff1288` | +2 rows (Khorne Daemonkin, Cult of Blood) |
| `faction_taxonomy.json` | `7c670bb72193` | World Eaters `built` → `true`, `data_army` added |
| `detachment_parser.py` | `4e3d4699ab40` | `WE` registered in all three maps |
| `e21b_check.js` | `ffda58de6903` | battleline-sweep literal 7 → 9 |
| `40K_Decision_Log.md` | `1f29c411571b` | D313 appended |
| `DECISION_INDEX.md` | `0ad636618df1` | D313 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `40001bfcfb31` | ledger header S219, count unchanged (23) |
| `pipeline_manifest.py` | (pre-`--write`; re-pinned by `--write`) | `SESSION_HANDOFF_219.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S220 |
| `SESSION_HANDOFF_219.md` | (this file) | |

## Net New Files

None. Every file touched this session is a versioned pipeline output or an existing script/harness/
doc update — no new file role was introduced.

## Backlog

23 open at S218 close; 23 open here (no ticket opened or closed — a faction-build data turn).
Beginning: B113, B110, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2,
P4, E23, B67b, E12, B17, B112 (23). Resolved: none (0). Added: none (0). Ending: B113, B110, B108,
B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17, B112
(23).
