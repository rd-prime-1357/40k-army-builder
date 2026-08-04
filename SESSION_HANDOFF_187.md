# SESSION HANDOFF 187

**Turn type:** data. **Assigned:** neither B90 blocker (D279) nor B91 was answered this session,
so both stayed untouched per the standing prompt; picked up **E23** (data turn) as the only
unblocked, fully-scoped open item. **Outcome:** shipped. Live behaviour unchanged — nothing new
is enforced yet.

## What happened
1. **Baseline opened green.** All 30 gates passed at open (`--fetch --data-turn`); S186's four
   file hashes verified byte-identical. Pulled the live `40K_Decision_Log_v3_0.md` manually from
   the repo (still required — B91's gap, unguarded, the fetch/overlay cannot recover it); hash
   matched S186's record. Read D278/D279 in full before starting.
2. **Neither B90 blocker nor B91 answered.** Per the S187 prompt's own instruction, did not touch
   B90 turn 2 and did not attempt B91 (both need Ryan). Reviewed the full open backlog for the
   next unblocked item: **E23** was the only one — data confirmed S182 (D273), mechanism decided
   S181 (D272), explicitly flagged "build turn next."
3. **E23 data turn shipped (D280).** `detachment_effects.json` gains a fifth kind (`tank_ace`)
   and six rows — one per `HEADHUNTER TASK FORCE` key (Space Marines, Black Templars, Blood
   Angels, Dark Angels, Deathwatch, Space Wolves) — all `enforced: false` pending the separate
   engine turn. Two new assertions (`E23-1` coverage, `E23-2` pool counts); `E21a-3`/`E21a-4`
   extended to validate the new kind. `rules_assertions.py` **114/114 → 116/116**.
4. **Re-derived D273's facts from source rather than trusting them — caught a real bug before
   it shipped.** The first draft set the shared generic key's `army` field to `"Space Marines"`,
   which is a `source_faction` display label, not a resolvable `units.json`/`detachments.json`
   army — `resolved_pool()` returned an empty pool and both new assertions failed loudly (0
   eligible where 16 were expected) instead of silently passing. Root cause: that one key is
   actually owned by **seven** armies per `detachments.json`'s own `armies` index (`Adeptus
   Astartes` + the six vanilla chapters with no dedicated MFM), not the single label on the key.
   Fixed with a new `_owning_armies()` helper that resolves real owners from the armies index —
   a strict generalisation, verified identical for every other existing row. Re-confirmed no
   vanilla chapter carries its own `unit_type: Vehicle` unit, so 16 holds for all seven owners.
   Full re-verification against source matched D273 exactly otherwise: rule text byte-identical
   across all six (`sha256:12 cadd53c18131`), pools 16/16/17/16/16/16 (Blood Angels' Baal
   Predator the only addition), Hammerfall Bunker correctly excluded by `except_unit_types`
   specifically (not just `except_keywords`).
5. **E23 ticket not closed.** The engine turn — `list_store.js` pick-array state,
   `eligibleWarlordEntries()`/`enhancementTypeEligible()` per-entry hooks at three `index.html`
   call sites — is separate work under turn-typing and was not attempted.

## State
- Baseline: green, 30/30 gates at close (verified after the manifest `--write` below).
- `index.html` unchanged, still **v6.15**. No engine or tooling change this session.
- Live behaviour: unchanged. All six `tank_ace` rows carry `enforced: false`, so nothing new is
  reachable or restricted yet.
- `repo_check` will show three files differing from the committed repo until this session's
  changes are pushed: `detachment_effects.json`, `pipeline_manifest.json`, `rules_assertions.py`
  — expected, not a problem.

## Decisions still waiting on Ryan (unchanged from S186)
1. **B90 (D279):** points edition (v1_0 vs adopt v1.1 first, B92) and roster target (confirm
   BT≈90 not 76, and whether Legends/Forge-World datasheets count).
2. **B91:** which decision log is canonical, so the live `_v3_0` gap stops widening.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `detachment_effects.json` | c7ec723c47bd | +tank_ace kind, +6 rows (E23, D280) |
| `rules_assertions.py` | c7383df2498e | +E23-1, +E23-2; E21a-3/E21a-4 extended; 114→116 |
| `DECISION_INDEX.md` | 7b94db7fc570 | D280 index entry |
| `OPEN_ITEMS_BACKLOG.md` | daa3f24e46ec | E23 progress note; still 17 open |
| `40K_Decision_Log_v3_0.md` | d4899d7acc58 | appended D280 (live log; unguarded — B91) |
| `pipeline_manifest.json` | 889415b3f838 | regenerated, `--write` (143 guarded files) |
| `pipeline_manifest.py` | 19f6b662357f | `SESSION_HANDOFF_187.md` appended to GUARDED (close housekeeping) |
| `NEXT_SESSION_PROMPT.md` | (see next file) | S188 (unguarded by design) |
| `SESSION_HANDOFF_187.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
17 open, unchanged. Beginning: B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, B87, B88,
B89, B90, B91, B92. Resolved: none. Added: none. Ending: same 17 — E23 progressed (data turn
shipped) but not closed.
