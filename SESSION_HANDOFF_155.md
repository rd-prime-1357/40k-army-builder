# Session Handoff 155

## Baseline at open

Read `SESSION_HANDOFF_154.md` and `NEXT_SESSION_PROMPT.md` (S155 header) as instructed.
`40K_Decision_Log_v3_0.md` is still absent from the mounted project area — third session
running (S153 closed with it present, S154 found it absent, S155 finds it absent again).
`D231_entry.md`–`D234_entry.md` and `D237_entry.md` are all still present in the mount.
Read as continued mount staleness per the standing constraint (the mount is a point-in-time
snapshot, not evidence of the repo's real state), not acted on beyond flagging again — this
entry (D238) is banked standalone for the same reason S154's was.

Ran `baseline.sh --fetch --data-turn` in full. Three findings, all named in advance by the
S155 prompt as expected, none surprise drift:

- `rules_assertions.py` FAIL — E4b-3 (29/5 stale, expected 30/6) and E21a-5 (B74, correctly
  failing on Chaos Cult's ungoverned BATTLELINE grant) — both this session's job or explicitly
  deferred.
- `pipeline_manifest.py` FAIL — 5 files not matching (the S154 push-pending set) — resolved by
  this session's `--write`.
- `repo_check.py` FAIL — only `40K_Data_Pipeline_Process_v0_6.md`, the long-standing
  area-ahead-of-repo drift, non-blocking.

Reconciled before starting work per protocol.

## What shipped — D238, CSM tooling turn C

Per `CSM_BUILD_SCOPE.md` §8 step 4 and the S155 prompt.

**Three new assertions in `rules_assertions.py`:**
- `CSM-1` — roster count, pinned at 54 of 58 real current-edition units (the four cult-troop
  units remain unpriced pending their own cross-file data turn, CSM_BUILD_SCOPE.md §4; recorded
  honestly, not rounded up).
- `CSM-2` — detachment count, pinned at 17 (D237).
- `CSM-3` — the two MFM-only detachments (Devotees of Destruction, Murdertalon Raiders) pinned
  as carrying `text_source: none` by design, not a parser gap.

**E4b-3's pinned collision census corrected.** Re-derived fresh from `detachments.json` rather
than trusting D237's handoff prose — confirmed 30 reachable same-army cross-detachment
collisions across 6 distinct names (was 29/5), one still priced differently between its two
detachments. The new sixth colliding name is **Warp-Fuelled Thrusters**, confirmed CSM-internal
(a single Chaos Space Marines collision, not touching any other army). The one differing-price
collision is unchanged and unrelated to CSM (Dark Angels / Deathwing Assault). Both the
assertion statement and the function body's pinned constants and docstring were updated —
neither the design conclusions (name-keyed dedup, detachment-keyed storage) changed.

**Manifest reissued** (`pipeline_manifest.py --write`) — 105 guarded files, all clean.

**Full harness pass:** `baseline.sh --no-repo` — 22/23 gates green. The sole failure is
`rules_assertions.py`'s E21a-5 (B74 — Chaos Cult's BATTLELINE grant has no
`detachment_effects.json` row), which is correctly failing by design and was explicitly out of
scope this session per the prompt. B74 remains open, filed for its own small data turn next.

`index.html` untouched — no engine or UI change this session, matching the tooling-only turn
type. No data file regenerated.

## Decisions needed

None. This was a pure tooling turn with no product or legality judgment calls — the two
findings from S154 were re-derivations against source data (the collision count, the roster
count), not choices.

## Net New Files

- `D238_entry.md` — standalone decision-log entry. Net new only in the sense that no file named
  exactly this exists yet; the *role* (a standalone D-entry awaiting fold-in) has existed before
  (D231–D234, D237).

All other touched files are updates to existing assertion/manifest/index/backlog files.

## Files (SHA-256, first 12 chars)

- `rules_assertions.py` — `df072390a068`
- `pipeline_manifest.json` — `0c3aac290648`
- `DECISION_INDEX.md` — `9d1ac6b661d1`
- `OPEN_ITEMS_BACKLOG.md` — `9d5b4a374b15`
- `D238_entry.md` — `0ccd814855d7` (net new)
- `SESSION_HANDOFF_155.md` — `0c08e1fa1711`
- `NEXT_SESSION_PROMPT.md` — `2a596b5865b4`
