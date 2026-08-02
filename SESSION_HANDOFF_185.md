# SESSION HANDOFF 185 — B90 turn 1 of 3 (ENGINE turn)

## Turn type: ENGINE. No data regeneration, no tooling-only work mixed in.

## What shipped
B90's engine mechanism for the two-tier SM-family chapter model (D276). This turn
built the mechanism only; it changes **no chapter's live behavior**. Details in
D277.

- **`resolveUnits()` (index.html) rewritten** to branch on a per-faction
  `roster_mode`. `'complete'` returns the chapter's own `units.json` block with an
  early return that sits **before** the generic pool is read and before the
  point-override map is applied — so a `'complete'` faction is structurally unable
  to reach `unitsByArmy['Adeptus Astartes']` or `applyChapterPointOverrides()`.
  Anything not exactly `'complete'` (i.e. `'union'` or a missing/garbage value)
  takes the unchanged union path — byte-identical to the pre-B90 behavior.
- **`faction_taxonomy.json`**: `roster_mode` added to all twelve Adeptus Astartes
  records (generic + eleven chapters). Comment rewritten to state the two-tier
  rule. **All eleven chapters flagged `'union'` this turn** (see D277 for why the
  five Tier-2 chapters are NOT `'complete'` yet).
- **`rules_assertions.py` B90-1** (tier A): every `is_subfaction:true` faction
  declares an explicit `roster_mode` of `'union'` or `'complete'` — no silent
  default. Passes.
- **`b90_check.js`** (NET-NEW harness, guarded): drives `resolveUnits` against a
  fixture `'complete'` chapter with a Proxy tripwire on the generic key and a
  call-counter on the override map. Proves complete-mode returns its own block
  only, reads the generic pool zero times, calls the override map zero times, and
  returns a copy; proves union-mode still unions + chapter-wins + one override
  call; proves a missing/unknown `roster_mode` falls safely to union. FAILS 5
  checks on the pre-B90 engine (has teeth), passes on the new one.
- **`baseline.sh`**: `b90_check` wired in as a gate. **`pipeline_manifest.py`**:
  `b90_check.js` and `SESSION_HANDOFF_185.md` added to `GUARDED`.
- **index.html v6.14 → v6.15** (the only version occurrence).

## Key decision this turn — D277 (read it)
The S185 prompt said to flag the five Tier-2 chapters `'complete'` this turn.
Source check contradicted its premise: each Tier-2 block in `units.json` is a
**delta** (BT 18, BA 15, DA 16, DW 10, SW 21), not a baked union — the generic
82-unit block is unioned in at runtime. Flagging the five `'complete'` now would
resolve them to those deltas, stripping the generic units they legitimately field
(Gladiators, Repulsor, Land Raider Crusader, …) — a fresh "legal units
unreachable" bug shipped live between the engine and data turns. So the five stay
`'union'` this turn and flip to `'complete'` in the data turn (S186), atomically
with their MFM-complete rebuild. Live behavior is unchanged — still union-leaked,
unregressed; the D0 gap D276 named persists exactly as before until the data turn
closes it. This is a build-sequencing refinement under development-manager
authority; D276's legality ruling is untouched.

## Integrity findings (flagged, NOT fixed — opened as B91; needs Ryan)
- **Decision log has diverged.** `pipeline_manifest.py` guards the unversioned
  `40K_Decision_Log.md` (and `DECISION_LOG` names it), but S184/S185 append to and
  read `40K_Decision_Log_v3_0.md`. Verified: the guarded unversioned copy has
  **zero** occurrences of D276; the live versioned copy has D276+. The live log is
  unguarded; the guarded log is stale. The manifest can't see this (it verifies
  the stale file's hash, which matches). D277 was appended to the live `_v3_0`.
- Other docs ship as identical-size unversioned + versioned pairs
  (`40K_Architecture_Overview`/`_v0_5`, `40K_Data_Dictionary`/`_v2_0`,
  `40K_Data_Pipeline_Process`/`_v0_6`, `40K_Functional_Spec`/`_v0_7`) — likely
  stale snapshots, each to confirm before removal.
- D276 sits mid-file (line ~243, beside D42), not in session order — pre-existing,
  low priority.

## Baseline
- **Open:** a fresh mount copy lacked the repo-only guarded files (old handoffs,
  `BACKLOG_ARCHIVE.md`, `40K_Decision_Log.md`, `repro_check.py`), so `--no-repo`
  failed 2/26 — both the same guarded-file-presence check, not a regression.
  Reconciled via the documented overlay path (`--fetch --no-repo`): **24/24 green
  (3 tier-B skipped)**. `rules_assertions` reports **76/76** (77/77 after B90-1;
  the older "75" note is stale).
- **Close:** green after `--write`; `--freshness-check` clean as the last command.

## Files — changed this session (SHA-256 first 12)

- `faction_taxonomy.json` — `roster_mode` on all 12 AA records (all `'union'`), comment rewritten — `d2bf67766308`
- `index.html` — `resolveUnits()` two-tier branch; v6.14 → v6.15 — `d503c258109e`
- `rules_assertions.py` — B90-1 roster-mode-presence assertion (tier A) — `93d65a9778f7`
- `baseline.sh` — `b90_check` gate added — `6e516c5d9981`
- `pipeline_manifest.py` — `b90_check.js` + `SESSION_HANDOFF_185.md` added to `GUARDED` — `d1c706803436`
- `b90_check.js` — NET-NEW harness (complete-mode isolation proof) — `de963155d5cf`
- `40K_Decision_Log_v3_0.md` — D277 appended — `f4e0507f0a17`
- `DECISION_INDEX.md` — D277 index entry, open count 15 → 16 — `31df7c696de3`
- `OPEN_ITEMS_BACKLOG.md` — B90 turn-1 progress + turn-plan correction; B91 added; tally 15 → 16 — `5b55ba48d5b8`
- `pipeline_manifest.json` — regenerated by `--write` after all text finalized (hash not listed here: its content includes this handoff's own hash)
- `NEXT_SESSION_PROMPT.md` — overwritten for Session 186 (B90 data turn)
- `SESSION_HANDOFF_185.md` — this file (net-new by number; rolling document, not net-new by role)

**Net New Files:** `b90_check.js` — a harness playing a role the project has not held before (structural proof of the two-tier resolution branch). Everything else in the list is an update to an existing file or a rolling document.

No file in this list is GW-derived; all are safe for the public repo.

## Backlog state at close
- **Beginning:** 15 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, B87, B88, B89, B90.
- **Resolved:** none (B90 turn 1 shipped; B90 stays open — turns 2, 3 remain).
- **Added:** B91 (decision-log integrity reconciliation).
- **Ending:** 16 open — the 15 above plus B91.
