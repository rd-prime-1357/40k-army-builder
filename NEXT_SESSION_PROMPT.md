# NEXT SESSION PROMPT — Session 186 (B90 turn 2 of 3: DATA turn)

## Turn type: DATA. Engine and tooling changes are prohibited this session.

Read `SESSION_HANDOFF_185.md` first, then this prompt. Read D276 and D277 in
`40K_Decision_Log_v3_0.md` in full (D277 corrects the earlier data-shape
assumption — do not skip it).

## Session open
1. Set up the working area, then run the full baseline. This is a data turn, so
   sources are required: `./baseline.sh --fetch --data-turn` (the `--data-turn`
   flag makes it fetch and verify the private GW sources and FAIL rather than
   start tier-A-only). If working `--no-repo`, the guarded files absent from a
   fresh mount copy (old handoffs, `BACKLOG_ARCHIVE.md`, `40K_Decision_Log.md`,
   `repro_check.py`) are recovered by the fetch/overlay path — that is expected
   reconciliation, not a regression. Confirm green before starting.
2. Verify the S185 file hashes in this handoff's Files section at open.

## The work — B90 turn 2 (data): rebuild the five Tier-2 chapters, then flip the flag
The engine mechanism shipped in S185 (D277). This turn does the actual roster fix
and the flag flip **together, atomically**, so no intermediate broken state ships:

1. **Rebuild the five Tier-2 chapters in `units.json` from their own MFM files**
   — Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves — as
   complete self-contained rosters, not override deltas against generic. Today
   their blocks are deltas (BT 18, BA 15, DA 16, DW 10, SW 21 units); after the
   rebuild each block must be its MFM's full roster (BT is 76 per D276). **Fix the
   parser/merge path, do not hand-edit `units.json`.** Each chapter's roster is
   confirmed against its own MFM file at rebuild time (D276 pre-verified only
   Black Templars; the other four are checked fresh, not assumed).
2. **Flip `roster_mode` from `'union'` to `'complete'` for those five** in
   `faction_taxonomy.json`. This is the flag flip D277 deferred from turn 1 — it
   belongs here, atomic with the data rebuild, so the flag never claims a roster
   shape the data doesn't hold. The six vanilla chapters and generic Space Marines
   stay `'union'`.
3. **Update `resolved_pool()` in `rules_assertions.py`** — it is the Python mirror
   of `resolveUnits()` and is still union-only (mirrors the pre-B90 engine). Once
   the five are `'complete'`, the mirror must branch the same way (a `'complete'`
   chapter is its own block only, no generic union), or the mirror silently
   diverges from the engine — the exact failure the project has been bitten by
   before. This is a required part of the data turn, not optional.
4. Re-verify `unit_loadouts.json` / `wargear_points.json` for any unit whose
   leader/support attach list or wargear shape changes once sourced natively.

## Acceptance
- All five Tier-2 chapters' `units.json` rosters match their MFM files exactly,
  unit-for-unit. The six vanilla chapters and generic Space Marines unchanged.
- `b90_check.js` still passes (the mechanism is unchanged; only data + flag move).
- `resolved_pool()` mirrors the new engine; `rules_assertions.py` green including
  any complete-mode roster assertion it feeds.
- `units_repro_check.py` reproduces the rebuilt `units.json` byte-for-byte from
  source (data-turn repro gate).
- Baseline green at close.

## After turn 2: turn 3 (assertion turn, separate session)
Pin the fix: no Tier-2 chapter roster contains a unit absent from its own MFM
file; extend the chapter-exclusivity assertions (D221/D222 pattern) to roster
membership. That is B90's final turn; then B90 closes.

## Recommended near-term priority: B91 (needs Ryan)
Opened S185 (D277). The decision log has diverged: `pipeline_manifest.py` guards
the stale unversioned `40K_Decision_Log.md` (no D276), while the live
`40K_Decision_Log_v3_0.md` that every recent session appends to is unguarded. The
live log is unprotected and the guarded one is stale — the integrity gap widens
every session. Resolving it needs Ryan (pick canonical file, repoint `GUARDED` and
`DECISION_LOG`, remove the stale copy; also triage the other unversioned/versioned
doc pairs). Do not delete anything without a file-card check. Worth doing before
much more log-appending happens.

## Standing reminders
- Turn-typing is strict: this is a data turn. No engine or tooling edits.
- Fix parsers, never hand-edit output. Diff-guard regenerated output against the
  prior committed file before banking.
- Source-first: re-derive any legality claim from source; absence in derived data
  is not absence in rules.
- Close by producing the four documents (decision log, backlog, handoff,
  next-session prompt), regenerating the manifest with `--write`, and running
  `--freshness-check` as the **last** command.
