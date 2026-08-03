# SESSION HANDOFF 186

**Turn type:** data. **Assigned:** B90 turn 2 (Tier-2 SM chapter complete-roster rebuild).
**Outcome:** assigned work **deferred** after source verification (D279); a red-baseline
**open reconciliation** banked instead (D278). Live app behaviour unchanged.

## What happened
1. **Baseline opened RED.** `units_repro_check` and `rules_assertions` both failed on
   `faction_taxonomy.json: differs (5642 vs 5643 bytes)`. Root cause: S185 (engine turn)
   hand-edited `faction_taxonomy.json` to add `roster_mode` and left a **stray trailing
   newline**; that turn ran tier-A-only and skipped the repro gates, so it shipped uncaught.
   The committed file equalled the pipeline's serialiser output **plus one `\n`**; its four
   sibling merge-passthrough lookups all end at `]`, confirming the newline was an anomaly.
   **Reconciled** by re-serialising to canonical no-trailing-newline form — content
   byte-identical, only the newline removed. Both gates green. (**D278**.)
2. **B90 turn 2 verified against source → deferred (D279).** Turn 2 was scoped as a
   mechanical data rebuild; it is not. Findings:
   - **No pipeline path builds a complete per-chapter roster.** Chapters are deltas today
     (BT 18, BA 15, DA 16, DW 10, SW 21) + a runtime union of the generic 82-unit block.
     A complete-roster rebuild needs a **new build path** (chapter MFM curated list → stats
     from the Wahapedia SM dump → priced from the chapter MFM → complete block), for
     ~90–119 units/chapter, byte-reproducible. Parser/merge architecture work, D0 stakes.
   - **D276's legality model confirmed by source:** BT lists **0** Librarian entries (BT
     fields no Psykers); the other four carry Librarians; chapter rosters genuinely differ
     (BT: Grimaldus/Emperor's Champion/Sword Brethren; BA: Dante/Mephiston/Death Company).
   - **Blocker 1 — points edition (→ B92).** Pipeline pins **v1_0** MFMs; unadopted **v1.1**
     files carry corrected points (rosters identical across versions; only points differ,
     e.g. Grimaldus 110→100, Emperor's Champion 100→90). Tool ships stale points. Adopting
     v1.1 is a faction-wide refresh with a manifest re-hash and a points-legality precedent.
   - **Blocker 2 — roster target.** Direct source count is **BT=90** (18 chapter-specific +
     72 curated-generic), **not** the **76** in D276/the prompt. The acceptance figure is
     contradicted by source; the target must be corrected before an assertion pins it.
   Both blockers are points-legality precedent → Ryan. B90 stays open; turn 2 resumes once
   both are settled.

## State
- Baseline: green after reconciliation + manifest `--write`; `--freshness-check` clean.
- `index.html` unchanged (v6.15). No engine or tooling behaviour change; the only
  `pipeline_manifest.py` edit is this handoff added to `GUARDED` (standard close housekeeping).
- Live behaviour: five Tier-2 chapters still `'union'`, still union-leaked — the D276 D0 gap
  persists, unregressed.

## Decisions waiting on Ryan (see D279 / B90 / B92)
1. **Points edition:** stay v1_0 for the rebuild (status-quo, stale points) or adopt v1.1
   first (faction-wide, current points). Recommend settling B92 first if current points matter.
2. **Roster target:** confirm rebuild targets the verified source roster (BT ≈90), correcting
   D276's 76, and that Legends/Forge-World datasheets in the MFM (Astraeus, Thunderhawk) count.

## B91 more urgent
Had to pull the live `40K_Decision_Log_v3_0.md` manually from the public repo — it is
unguarded and the fetch/overlay cannot recover it (guarded-absent files only). The guarded
`40K_Decision_Log.md` is stale (no D276–D279). Every append widens the gap. Resolve B91
(canonical log, repoint guard, remove stale copy after a file-card check) before much more
log-appending. Ryan decision.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `faction_taxonomy.json` | cdf229023b11 | re-serialised canonical (D278); content unchanged |
| `40K_Decision_Log_v3_0.md` | 6301db986ac8 | appended D278, D279 (live log; unguarded — B91) |
| `DECISION_INDEX.md` | 2e5b30a5468b | D278, D279 index entries |
| `OPEN_ITEMS_BACKLOG.md` | 395d39225104 | B90 turn-2 deferral note; B92 opened; 16→17 open |
| `NEXT_SESSION_PROMPT.md` | 9767c5336498 | S187 (unguarded by design) |
| `pipeline_manifest.py` | cd9a3432e0c4 | this handoff added to GUARDED (close housekeeping) |
| `SESSION_HANDOFF_186.md` | (this file) | net-new; hash banked in the manifest by `--write` |
| `pipeline_manifest.json` | (regenerated) | not self-guarded; rebuilt by `--write` |

## Backlog
16 → 17 open. Beginning: B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, B87, B88,
B89, B90, B91. Added: B92 (MFM v1.1 edition adoption / points currency). Resolved: none.
Ending: the 16 above + B92.
