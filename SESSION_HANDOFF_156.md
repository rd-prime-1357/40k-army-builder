# Session Handoff 156

## Baseline at open

Read `SESSION_HANDOFF_155.md`, `D238_entry.md`, and `NEXT_SESSION_PROMPT.md` (S156 header) as
instructed. `40K_Decision_Log_v3_0.md` and 31 other guarded files were absent from the mounted
project area again this session, plus `DECISION_INDEX.md` and `OPEN_ITEMS_BACKLOG.md` failed
`pipeline_manifest.py`'s hash check even though their content matched D238's handoff exactly.

Reconciled by cloning the live public repo directly rather than re-flagging a fourth time: the log,
all 31 session handoffs, and every guarded file are present and intact there. The area mount's
absences are pruning under the project area's 96% capacity, not repo drift — this closes the
three-session D237/D238 flag.

The manifest mismatch was real, not mount staleness: `pipeline_manifest.json`'s stored hashes for
`DECISION_INDEX.md` and `OPEN_ITEMS_BACKLOG.md` matched neither file's actual content, in the area or
the repo, even though both files' content matched D238's stated final hashes. At S155,
`pipeline_manifest.py --write` ran before those two files reached their final edited state and was
never repeated — undetected since because no session since had the full guarded-file set to check
against (a partial area silently narrows what the gate can verify). Fixed by reissuing the manifest
against the complete, repo-verified set — only those two files' entries plus the long-standing,
already-known `40K_Data_Pipeline_Process_v0_6.md` push-pending drift changed. No content lost.

Ran `bash baseline.sh --no-repo` after reconciling: 23/23 gates green, `rules_assertions.py` failing
only `E21a-5` (B74), exactly as the S156 prompt anticipated.

## What shipped — D239, B74 closed

**`detachment_effects.json`** gained a `battleline`-kind row for `Chaos Space Marines|CHAOS CULT`,
elevating Traitor Guardsmen Squad — the sole unit named in the detachment's KEYWORDS clause, confirmed
Chaos Space Marines Infantry in `units.json`, reachable without cross-army resolution, no
`restrictions` text on the detachment. Matches the shape of the five existing battleline rows exactly.

**`e21b_check.js`**'s full-table sweep had a pinned count of 4 named units for elevation; updated to 5
alongside the data row, since the check's fixture is a direct census of this file's battleline rows,
not an engine or parser change.

**Decision-log housekeeping.** D237 and D238 folded into `40K_Decision_Log_v3_0.md` from their
standalone entries (in chronological order, after D236). D231–D234 were already folded at S153 but
their standalone files had never actually been deleted — that omission is why they kept resurfacing
in the mount at S154/S155, not a regression. All six now-redundant `D2NN_entry.md` files deleted.
`DECISION_INDEX.md` gained the D239 line.

**Backlog.** B74's full body moved to `BACKLOG_ARCHIVE.md`, marked closed (S156, D239). Its one-line
pointer replaces the open-item body in `OPEN_ITEMS_BACKLOG.md`; open count 13 → 12.

**Manifest reissued three times** (`pipeline_manifest.py --write`): for the sync-order fix, after the
data row and check update, and after closing a repeated gap in the GUARDED list — `SESSION_HANDOFF_154.md`
and `.155.md` had never been appended (the same append-step miss D234 fixed for `.149.md`/`.150.md` at
S151), so this session's own `.156.md` would have joined them unguarded. All three now added; 108
guarded files, clean.

**Full baseline:** `baseline.sh --no-repo` — 23/23 gates green. `rules_assertions.py` — 107/107.
`index.html` untouched — data-only turn, matching the S156 prompt's scope. This closes the CSM
tooling arc from `CSM_BUILD_SCOPE.md` §8 in full.

## Decisions needed

None. Both findings this session (the mount-vs-repo reconciliation, the manifest sync-order bug) were
re-derivations against the live repo, not product or legality judgment calls.

## Net New Files

None. `detachment_effects.json`, `e21b_check.js`, `pipeline_manifest.py`, `40K_Decision_Log_v3_0.md`,
`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `BACKLOG_ARCHIVE.md`, and `pipeline_manifest.json` are
all updates to existing files. The six deleted `D2NN_entry.md` files are removals, not additions.

## Files (SHA-256, first 12 chars)

- `detachment_effects.json` — `a8b8f376cb5e`
- `e21b_check.js` — `fdbf95474e29`
- `pipeline_manifest.py` — `12ce6e78dde0`
- `pipeline_manifest.json` — `d0dd11ab0227`
- `40K_Decision_Log_v3_0.md` — `13acecae463a`
- `DECISION_INDEX.md` — `7fa06d64a6f4`
- `OPEN_ITEMS_BACKLOG.md` — `ad897103ef03`
- `BACKLOG_ARCHIVE.md` — `0c603e1934f7`
- `NEXT_SESSION_PROMPT.md` — `552cad68ef43`
