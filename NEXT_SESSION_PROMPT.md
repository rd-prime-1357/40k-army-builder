# NEXT SESSION PROMPT — Session 187

## Turn type: decided by which of the two blocking decisions Ryan has answered (see below). Do not mix turns.

Read `SESSION_HANDOFF_186.md` first, then this prompt. Read **D278 and D279** in
`40K_Decision_Log_v3_0.md` in full — D279 records why B90 turn 2 was deferred and the two
decisions it waits on.

## Session open
1. Data-turn baseline with sources: `./baseline.sh --fetch --data-turn`. Sources are required.
   The live decision log `40K_Decision_Log_v3_0.md` is **unguarded and repo-only** (the B91 gap):
   a fresh mount will not have it and the fetch/overlay will **not** recover it (it only overlays
   *guarded* absent files). Pull it manually from the public repo if you need D-entries —
   `40K_Decision_Log.md` (the guarded one) is stale and lacks D276-D279.
2. Verify the S186 hashes in this handoff's Files section at open.
3. Baseline should be green at open (D278 reconciled the faction_taxonomy drift). If it is red on
   `faction_taxonomy.json` again, something re-added a trailing newline - re-serialise, don't
   hand-edit.

## B90 turn 2 is BLOCKED - do not attempt until both decisions are answered (D279)
The Tier-2 complete-roster rebuild is a **pipeline build** (no existing path emits a full
per-chapter roster; chapters are deltas + runtime union today), and its target is not well-defined
against source. Two Ryan decisions gate it:

1. **Points edition (B92).** Pipeline pins **v1_0** MFMs; unadopted **v1.1** files carry corrected
   points (rosters identical, only points differ - the tool ships stale points). Adopt v1.1
   faction-wide, or stay v1_0? If current points matter for the rebuilt Tier-2 rosters, settle B92
   **first** so the rebuild is not re-priced immediately after.
2. **Roster target.** Source count is **BT=90**, not the **76** in D276/the old prompt. Confirm the
   rebuild targets the verified source roster (BT ~90; BA/DA/DW/SW counted the same at rebuild
   time), correcting D276's figure, and that Legends/Forge-World datasheets in the MFM (Astraeus,
   Thunderhawk) count as legal roster members before any assertion pins the count.

**If both are answered -> resume B90 turn 2 (DATA turn):** build the new complete-roster pipeline
path (chapter MFM's own curated list -> stats from the Wahapedia SM dump -> priced from the chapter
MFM -> complete chapter block), rebuild the five in `units.json` from source (fix the parser/merge
path, never hand-edit), flip `roster_mode` union->complete for the five in `faction_taxonomy.json`
(write via the serialiser, no trailing newline - D278), update `resolved_pool()` in
`rules_assertions.py` to mirror complete-mode, re-verify `unit_loadouts.json` / `wargear_points.json`
for any changed attach-list/wargear, and confirm `units_repro_check.py` reproduces byte-for-byte.
Then turn 3 (assertion) pins roster membership (D221/D222 pattern).

**If neither is answered -> pick up other open work** rather than blocking: B92 (if Ryan wants the
edition decision teed up), or B91 (decision-log/versioned-doc reconciliation - now more urgent,
see below), or the next backlog item under the faction priority order. Do not start B90 turn 2.

## B91 is more urgent than before
This session had to pull the live decision log manually from the repo because it is unguarded and
the fetch/overlay cannot recover it. Every session that appends to `_v3_0` widens the gap and a
fresh session cannot retrieve it through the normal path. Resolving B91 (pick the canonical log,
repoint `GUARDED`/`DECISION_LOG`, remove the stale copy after a file-card check, triage the other
versioned/unversioned doc pairs) needs Ryan and is worth doing before much more log-appending.

## Standing reminders
- Turn-typing strict. Fix parsers, never hand-edit output; merge-passthrough JSON goes through the
  serialiser (D278). Source-first: re-derive legality claims from source; absence in derived data
  is not absence in rules.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `--freshness-check` as the **last** command.
