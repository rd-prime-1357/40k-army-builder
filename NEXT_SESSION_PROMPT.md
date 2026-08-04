# NEXT SESSION PROMPT — Session 188

## Turn type: decided by what's been answered when the session opens (see below).

Read `SESSION_HANDOFF_187.md` first, then this prompt. Read **D280** in
`40K_Decision_Log_v3_0.md` in full for what the E23 data turn actually shipped.

## Session open
1. Data-turn baseline with sources: `./baseline.sh --fetch --data-turn`. Sources are required.
   The live decision log `40K_Decision_Log_v3_0.md` is **unguarded and repo-only** (the B91 gap):
   a fresh mount will not have it and the fetch/overlay will **not** recover it. Pull it manually
   from the public repo — `40K_Decision_Log.md` (the guarded one) is stale and lacks D276-D280.
2. Verify the S187 hashes in the handoff's Files section at open.
3. Baseline should be green at open. `repo_check` will only be clean once S187's three changed
   files (`detachment_effects.json`, `pipeline_manifest.json`, `rules_assertions.py`) are pushed
   to the repo — check whether that's happened; if not, treat the repo-vs-area diff as expected,
   not a failure to chase.

## Three things could be true at open — check in this order

**If Ryan has answered the B90 blockers (D279, both: points edition + roster target) →**
resume B90 turn 2 (DATA turn): new complete-roster pipeline path per D279, rebuild the five
Tier-2 chapters in `units.json`, flip `roster_mode`, update `resolved_pool()`, re-verify
`unit_loadouts.json`/`wargear_points.json`. Do not mix with anything else this session.

**Else if Ryan has answered B91 →** reconcile the canonical decision log (repoint
`GUARDED`/`DECISION_LOG`, remove the stale copy after a file-card check per standing constraints).
Tooling/doc turn.

**Else →** pick up **E23's engine turn** (the only other unblocked, scoped work): wire
`list_store.js`'s new per-entry pick-array state (mirroring `warlord_entry_id`/`force_disposition`
— purely additive, no schema bump) and the three `index.html` call sites
(`eligibleWarlordEntries()`, `enhancementTypeEligible()`'s three sites) to consume the six
`tank_ace` rows `detachment_effects.json` now carries (D280), flipping them to `enforced: true`
once wired. **Flag this at open as an Analysis-tier turn before starting** — it changes Enhancement
and Warlord eligibility live on six built armies, and a wrong per-entry hook is exactly the class
of mistake that ships a bug, not a data typo. Re-derive the eligible-pool predicate and cap from
`detachment_effects.json`'s rows and `E23-2`'s assertion rather than re-deriving from source again
— that part is already pinned.

If none of the three is available (nothing answered and E23's engine turn also looks too deep for
the session), fall back to the next backlog item under the faction priority order rather than
blocking.

## Standing reminders
- Turn-typing strict. Fix parsers, never hand-edit output; merge-passthrough/hand-authored JSON
  (`detachment_effects.json`, `faction_taxonomy.json`, and its four lookup siblings) goes through
  a script/serialiser, never a manual edit — D278's lesson, reapplied this session without
  incident.
- Source-first: re-derive legality claims from source; absence in derived data is not absence in
  rules. S187 is a working example of why — the prior session's confirmed facts (D273) were still
  worth re-checking, and the re-check caught a real bug (`_owning_armies()`, D280).
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `--freshness-check` as the **last** command.
