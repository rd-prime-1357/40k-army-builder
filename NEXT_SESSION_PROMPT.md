# NEXT SESSION PROMPT — Session 189

## Turn type: decided by what's been answered when the session opens (see below).

Read `SESSION_HANDOFF_188.md` first, then this prompt. Read **D281** in
`40K_Decision_Log_v3_0.md` in full for the two tickets opened last session (E28, B93) and the
`pipeline_manifest.json` hash note.

## Session open
1. Data-turn baseline with sources: `./baseline.sh --fetch --data-turn`. Sources are required.
   The live decision log `40K_Decision_Log_v3_0.md` is **unguarded and repo-only** (the B91 gap):
   a fresh mount will not have it and the fetch/overlay will **not** recover it. Pull it manually
   from the public repo — `40K_Decision_Log.md` (the guarded one) is stale and lacks D276-D281.
2. Verify the S188 hashes in the handoff's Files section at open.
3. Baseline should be green at open. `repo_check` will only be clean once S188's four changed
   files (`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.json`,
   `pipeline_manifest.py`) plus the live decision log are pushed to the repo — check whether
   that's happened; if not, treat the repo-vs-area diff as expected, not a failure to chase.

## Four things could be true at open — check in this order

**If Ryan has answered the B90 blockers (D279, both: points edition + roster target) →**
resume B90 turn 2 (DATA turn): new complete-roster pipeline path per D279, rebuild the five
Tier-2 chapters in `units.json`, flip `roster_mode`, update `resolved_pool()`, re-verify
`unit_loadouts.json`/`wargear_points.json`. Do not mix with anything else this session.

**Else if Ryan has answered B91 →** reconcile the canonical decision log (repoint
`GUARDED`/`DECISION_LOG`, remove the stale copy after a file-card check per standing constraints).
Tooling/doc turn.

**Else if picking up E23's engine turn →** the only fully-scoped, unblocked build-turn item:
wire `list_store.js`'s new per-entry pick-array state (mirroring `warlord_entry_id`/
`force_disposition` — purely additive, no schema bump) and the three `index.html` call sites
(`eligibleWarlordEntries()`, `enhancementTypeEligible()`'s three sites) to consume the six
`tank_ace` rows `detachment_effects.json` carries (D280), flipping them to `enforced: true` once
wired. **Flag this at open as an Analysis-tier turn before starting** — it changes Enhancement
and Warlord eligibility live on six built armies, and a wrong per-entry hook is exactly the class
of mistake that ships a bug, not a data typo. Re-derive the eligible-pool predicate and cap from
`detachment_effects.json`'s rows and `E23-2`'s assertion rather than re-deriving from source again
— that part is already pinned.

**Else, two newly opened tickets are available for a scoping turn (not a build turn — neither is
ready to build):**
- **E28** (Detachment UI → right-panel, D281): needs a design/scoping pass on the new selection
  state (distinguishing "a unit is selected" from "the Detachments group is selected") before any
  engine work starts. Ryan already gave the product answer (move it, Force Disposition at the
  group level, not per-row); what's missing is the mechanism, not the decision.
- **B93** (Enhancement/Upgrade eligibility, D281): needs a source pass across all 607 enhancement
  records in `detachments.json` to determine how reliably the qualification clause can be parsed
  (flavour-text-then-qualifier is the common shape, but at least two records have no usable
  qualification text at all — Thousand Sons' Stave Abominus, Chaos Daemons' Leaping Shadows) before
  any parser or engine mechanism is chosen. **Flag as Analysis-tier before starting** — this
  produces the eligibility-gating design for a live D0 gap (Upgrades currently have zero type
  check), and a wrong read of the pattern across 607 records would misscope the whole build.

If none of the above is available (nothing answered, E23's engine turn looks too deep for the
session, and neither E28 nor B93 is picked up for scoping either), fall back to the next backlog
item under the faction priority order rather than blocking.

## Standing reminders
- Turn-typing strict. Fix parsers, never hand-edit output; merge-passthrough/hand-authored JSON
  (`detachment_effects.json`, `faction_taxonomy.json`, and its four lookup siblings) goes through
  a script/serialiser, never a manual edit — D278's lesson.
- Source-first: re-derive legality claims from source; absence in derived data is not absence in
  rules. S188 is a working example of why — Ryan's own report on B93 (qualification clause
  "begins" the description) didn't hold up against a source sample, and the correction was worth
  finding before the ticket was scoped, not after a parser was built against it.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `--freshness-check` as the **last** command — after every other edit, including edits to the
  handoff itself (S188 self-referential-hash note: the handoff's own row in its Files table can't
  meaningfully carry a hash of itself; leave it as "(this file)" per S187's precedent rather than
  computing one, since editing the file to add its own hash invalidates that hash).
