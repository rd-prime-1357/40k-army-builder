# Session Handoff 151

## Baseline at open

`NEXT_SESSION_PROMPT.md`'s mount copy still showed S149's stale M0 prompt at the very start of this
turn (Ryan confirmed he'd already deleted and replaced it; the real S151 prompt was pasted in-chat).
Same reconciliation category S150 already hit once — mount lag, not a regression.

Ran `baseline.sh --fetch`: 5/25 gates failed. Diagnosed rather than routed around:

- **M1 has already run.** 27 guarded files (the repo-resident set: `40K_Decision_Log_v3_0.md`,
  `BACKLOG_ARCHIVE.md`, `repro_check.py`, `SESSION_HANDOFF_125.md`–`148.md`) were absent from the
  project area — confirmed against the actual mount, not assumed. This matches exactly what the S151
  prompt itself said to watch for.
- **The fetch-overlay's own verify step was blocking its recovery.** `pipeline_manifest.py --dir
  $FETCHED_DIR` checked the *entire* fetched tree unconditionally. Three files failed that check —
  the one already-known drift (`40K_Data_Pipeline_Process_v0_6.md`) plus two new ones
  (`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`) that S150 edited (adding D233) without re-running
  `pipeline_manifest.py --write` afterward. Because the check is all-or-nothing, that one stale
  manifest entry blocked the *entire* overlay — including the 27 files that had nothing to do with
  the mismatch and were the only reason the fetch ran at all.

This is a real gap in M0's design, not a one-off: the stated authority rule is "area copy wins," but
the old fetch-verify checked every file unconditionally, so ordinary area-ahead-of-repo drift on an
unrelated file could permanently block recovering genuinely evicted ones, every session, until a push
happened to clear it.

## What shipped — D234, fetch-verify scoped to the overlay set

`pipeline_manifest.py` gained `check_overlay()` / `--overlay-check`: verifies only the guarded files
*absent from the local workspace* against the fetched copy. Files already resident locally are never
checked here — consistent with "area copy wins," their content was never going to come from the fetch
regardless of whether the fetched copy matches. `baseline.sh`'s fetch-verify step now calls this mode
and overlays exactly the verified list, rather than walking the whole fetched tree.

Re-ran `baseline.sh --fetch` after the fix: fetch-verify passed (27 overlay-needed files verified, 74
already-local skipped), all 27 evicted files restored. Remaining state, all expected:

- `repro_check` — fails naming the same seven B68 unit_ids as S148 named. Carried-forward, diagnosed,
  not a regression.
- `repo_check` — three files differ from the live repo: the pre-existing `40K_Data_Pipeline_Process_v0_6.md`
  drift, plus `baseline.sh` and `pipeline_manifest.py` (this session's own edits, not yet pushed).
  `SESSION_HANDOFF_149.md` flagged repo-only (informational) — see manifest gap below.

## Manifest housekeeping

`SESSION_HANDOFF_149.md` and `SESSION_HANDOFF_150.md` were never appended to `GUARDED` — S149 missed
its own append-at-close step. Added both, plus `SESSION_HANDOFF_151.md` (this file), to the guarded
set. Regenerated `pipeline_manifest.json` (`--write`) to bless the current state: S150's
`DECISION_INDEX.md`/`OPEN_ITEMS_BACKLOG.md` edits, this session's `baseline.sh`/`pipeline_manifest.py`
changes, and the three newly-guarded handoffs. Full baseline re-run after regeneration: clean except
the carried-forward B68 `repro_check` failure and the three known push-pending files — no other gate
affected.

Turn type: **tooling-only.** No engine, data, or parser change; `loadout_parser.py`/`equipped_parser.py`
untouched, B68 unaddressed by design.

## Decisions needed

- **Push `baseline.sh`, `pipeline_manifest.py`, and `40K_Data_Pipeline_Process_v0_6.md`** in the next
  upload batch — closes all three live drifts `repo_check.py` currently names. Recommend yes; low-cost,
  reversible. Proceeding on this unless you object.
- The CSV batch you re-sent this session is confirmed the same file set flagged at S150 (identical
  names/schemas to files already resident) — not added, per the standing recommendation from S150 that
  I not treat a re-send as a replacement without confirmation of what it's meant to replace.

## Net New Files

None. `D234_entry.md` follows the same standalone-decision pattern as D231–D233 (full log stays
repo-only); it is a new file on disk this turn but plays a role (a decision-log entry) the project has
held before, same as its predecessors.

## Files (SHA-256, first 12 chars)

- `pipeline_manifest.py` — `4cfb1f4e71df`
- `baseline.sh` — `d0d765763d89`
- `pipeline_manifest.json` — `1c47d2af4faf`
- `DECISION_INDEX.md` — `989d081f32e0`
- `OPEN_ITEMS_BACKLOG.md` — `18478d4325e2`
- `D234_entry.md` — `a18d81a7cdca`

`NEXT_SESSION_PROMPT.md` not hashed, per D231/M0.

Unchanged this session (re-verify at S152 open): `index.html`, `units.json`, `unit_loadouts.json`,
`detachments.json`, and everything else in the guarded set not named above.

**Repo custody:** `pipeline_manifest.py`, `baseline.sh`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
`D234_entry.md` — project-authored code/prose, no GW-derived text, public-repo-eligible next batch.
`pipeline_manifest.json` likewise (hashes only).

**Capacity note:** M1 confirmed already run by Ryan; area holds only the per-session working set now.
M2 (evict the 71 GW sources) still gated behind CSM turn B as its dress rehearsal, per D231/P4 — not
this session's task.

## Backlog summary

- **Beginning (8 open):** P2, P4, E23, E12, B17, B61, B67b, B68
- **Resolved (0):** none — the fetch-verify fix is process/tooling under P4, not a ticket of its own
- **Added (0):** none
- **Ending (8 open):** P2, P4, E23, E12, B17, B61, B67b, B68
