# SESSION HANDOFF 243

**Turn type:** scoping-only. No code or built-data files changed. `B93_SCOPE.md` (new §12),
`40K_Decision_Log.md` (D340), `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md` and
`pipeline_manifest.py` (handoff registration only) changed. `index.html`, all harnesses, and every
JSON data file are untouched.

## What happened

1. **Open — repo verified clean.** All nine of S242's changed-file hashes matched the pushed
   copies exactly. Baseline ran clean: 29/29 gates (5 tier-B skipped — sources not needed for a
   scoping turn).

2. **B125 closed — the chapter-keyword gap is Dark Angels-only, not general.** Fetched and
   hash-verified `Datasheets_keywords.csv`, `Datasheets.csv` and `Source.csv` directly from the
   private sources repo against `source_manifest.json` (all three matched). Checked every
   non-faction keyword on any Codex Space Marines datasheet for the Deathwing/Ravenwing shape — a
   keyword that should gate on one chapter but lives on a datasheet shared by the generic
   "Adeptus Astartes" pool. Only Deathwing and Ravenwing do this. Death Company (Blood Angels, 8
   source rows) and Wulfen (Space Wolves, 4 rows) — the two other named-formation keywords worth
   checking — both classify cleanly as their own chapter with zero bleed. **Grey Knights is
   structurally exempt**: separate `faction_id` (GK, 31 datasheets), no shared generic pool, so
   the union mechanism that causes this bug cannot apply to it at all.

3. **D338 reconciled — in favor of B93_SCOPE.md's original finding, not the gate's.** Cross-checked
   both keyword strings against the actual built `units.json`, which neither prior side had done.
   `keyword_names` carries Deathwing on 8 Dark Angels units (5 Epic Hero, 3 Infantry — zero
   Characters) and Ravenwing on 7, and none of the generic-pool Characters that should carry them
   when fielded in a Dark Angels list actually do — 5 for Deathwing (Captain/Chaplain/Librarian In
   Terminator Armour, Ancient In Terminator Armour, Bladeguard Ancient), 1 for Ravenwing (Chaplain
   On Bike). Matches B93_SCOPE.md's original 5-and-1 exactly. D338's gate found these "not
   zero-admit" only because its raw-CSV read credits a same-named resolved-pool record without
   checking whether that record's own **built** keyword field carries the restriction — it is more
   permissive than what `units.json` actually contains. The 6 Deathwing-family enhancement records
   belong back on B129's zero-admit exemption list; its docstring currently says the opposite.

4. **B130 and B131 opened — sequenced, not combined (turn typing).** B130: a small per-army
   keyword-restoration map, the mirror of `SUBFACTION_KEYWORD_ARMY`, adding Deathwing/Ravenwing
   back onto the 6 named shared records when the Dark Angels union pool is resolved — 6 units, 1
   chapter, no new mechanism class, data-turn sized. B131: correct B129's exemption list (30 → 36)
   and its D338 docstring paragraph to match today's actual (still-broken) data — tooling-only.
   These are two different turn types and must ship in separate sessions. Recommended order:
   **B131 first** (reflects current reality, quick), **B130 later** (the real fix), then a third
   small tooling pass removing the now-unnecessary exemption once B130 lands.

5. **Close.** No code changed, so no gate re-run was needed beyond the session-open baseline.
   `--write`, then `--freshness-check`, last two commands, in that order.

## Decisions needed

None. B125's finding is grounded in hash-verified source and the actual built JSON, not a product
call — nothing here needs Ryan's input.

## Shipped / changed

- **`B93_SCOPE.md`** — new §12 addendum: full B125 census, the Deathwing/Ravenwing-only finding,
  D338 reconciliation, and the recommended B130 fix shape.
- **`40K_Decision_Log.md`** — D340 added: B125 closed, D338 reconciled, B130/B131 opened.
- **`DECISION_INDEX.md`** — D340 summary appended, matching the full log entry.
- **`OPEN_ITEMS_BACKLOG.md`** — B125 moved from Open Items to Closed/Shipped with a "CLOSED S243"
  addendum; B130 and B131 added to Open Items; S243 ledger appended; 25 → 26.
- **`pipeline_manifest.py`** — `SESSION_HANDOFF_243.md` added to GUARDED (handoff group) before
  `--write` ran. No other entries touched.
- **`NEXT_SESSION_PROMPT.md`** — rewritten for S244.

### Net New Files

None. `B93_SCOPE.md`, `40K_Decision_Log.md`, `DECISION_INDEX.md` and `OPEN_ITEMS_BACKLOG.md` are
all existing rolling/reference documents; this session only added sections to them.

## Files (SHA-256, first 12)

Verify these at S244 open.

| file | sha256:12 | note |
|------|-----------|------|
| `B93_SCOPE.md` | `b452b98bcf4b` | new §12 — B125 census |
| `40K_Decision_Log.md` | `539b55659402` | D340 appended |
| `DECISION_INDEX.md` | `25b3724cb6be` | D340 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `1773bf9bd692` | B125 closed; B130/B131 opened; 25 -> 26 |
| `pipeline_manifest.py` | `e74bfe38cacc` | `SESSION_HANDOFF_243.md` registered |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_243.md` | (this file) | not self-referential; checked by `--freshness-check` |

Hashes taken from the on-disk copies after `--write`/`--freshness-check` both ran clean.

## Ryan action required

- **Push this session's changed files** to the public repo: `B93_SCOPE.md`, `40K_Decision_Log.md`,
  `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `SESSION_HANDOFF_243.md`,
  `NEXT_SESSION_PROMPT.md`. Given D337, please double-check `pipeline_manifest.py` specifically
  lands as edited.

## Decisions resolved this session

D340 (B125 closed, D338 reconciled) — grounded in hash-verified source and the built JSON, not a
product call; nothing here required Ryan's input.

## Decisions waiting on Ryan

- **Next faction after Drukhari** — unchanged since S240. Recommendation stands: clear the engine
  backlog first; B116's Aeldari dependency belongs on a release plan.

## Backlog

25 open at S242 close; **26 open at S243 close** (B125 closed; B130, B131 opened).

Beginning: B125, B126, B127, B128, B116, B120, B122, B124, B97, B103, E28, B93, B90, B94, B85,
B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (25).
Resolved: B125 (1).
Added: B130, B131 (2).
Ending: B126, B127, B128, B116, B120, B122, B124, B97, B103, E28, B93, B90, B94, B85, B86, B69,
B70, B75, P2, P4, E23, B67b, E12, B17, B130, B131 (26).

Nothing is decision-blocked. B130 (the keyword-restore fix, data-sized) paired with B131 (gate
correction, tooling) is the recommended next pick — small, well-scoped, and unblocks B93's
Deathwing-family records specifically. B93 itself remains gated on B127 (source acquisition, 74
records) for its full population regardless.
