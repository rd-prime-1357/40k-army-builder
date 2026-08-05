# NEXT SESSION PROMPT — Session 193

## Turn type: engine-only. No exceptions.

Read `SESSION_HANDOFF_192.md` first, then this prompt. Read **D285** in `40K_Decision_Log.md` in
full before starting — it carries B95's close and B94's decision, and this session's work is B94's
engine turn.

## Session open
1. Baseline: `./baseline.sh --fetch --data-turn`.
2. Verify the S192 hashes in the handoff's Files section at open.
3. Confirm Ryan has pushed S192's changes.
4. Check whether Ryan confirmed `40K_Decision_Log.md`'s presence/absence in the `/mnt/project`
   mount (flagged in S192, unresolved) — if he reports it present, treat S192's mount-vs-repo
   finding as a one-session mount staleness, not a live gap.
5. If Ryan spot-checked CSM/Thousand Sons in the running app per S192's action item, note the
   result; if not, a quick visual check that both factions resolve their real rosters (not the
   generic Adeptus Astartes pool) is worth doing before building on top of B95's fix.

## This session's work — B94 engine turn (Ryan decided S192/D285: add the real 4th copy-tier)

**Engine only — schema, `resolveUnits`/points lookup in `index.html`, and the `resolved_pool`/points
mirror in `rules_assertions.py`. Do NOT touch `units.json` or regenerate any data this session.**

Full scope from D283/B94's backlog entry:
- The MFM tier shape `YOUR 1ST TO 3RD UNITS COST` / `YOUR 4TH + UNIT COSTS` needs a real 4th
  copy-tier in the points schema (`units.json` `points.sizes[*]` currently has only `first_unit` /
  `second_unit` / `third_plus`).
- B87 already captures the un-representable 4th+ tier as `_esc4_fourth_plus` on the 34 affected
  units' parsed output (not yet regenerated into committed `units.json` — that's the data turn,
  separate and later).
- This turn: design and land the schema's 4th tier, wire `index.html`'s points-lookup path to use
  it when a unit's copy count reaches 4, and update `rules_assertions.py`'s Python mirror of the
  same lookup so the two never diverge (same discipline as B90's `resolved_pool()` mirror).
- Do not regenerate `units.json` this session — the schema and lookup must be correct and pass their
  own harness/assertion checks against synthetic or the currently-committed (3-tier) data first. The
  data turn (regenerating the 34 affected units through the real pipeline) and the assertion turn
  (pinning the new tier's presence) are separate, later turns per D283, sequenced with B89's
  adoption arc so the affected units migrate once.
- 34 units affected across 15 v1.1 files: Rhino, Razorback, Drop Pod, Impulsor, Chaos Rhino, Raider,
  Venom, Rubric Marines.

## Standing reminders
- Turn-typing strict: engine only this session. If the engine change turns out to need a coupled
  data correction the way B87 did, stop and scope it as its own turn rather than mixing — B87's
  exception was justified by a shipped live bug forcing the pipeline's hand; B94's schema addition
  starts from a clean baseline and has no equivalent forcing reason to mix.
- Fix parsers/schema, never hand-edit output.
- Source-first: two real findings this session (S192) — the missing `40K_Decision_Log.md` in the
  mount, resolved by cloning the repo rather than assuming; and the missing `data_army` field found
  by reading `index.html`'s actual consumers of the flag before flipping it, not from the ticket's
  own framing — were both caught by checking, not assuming. Same discipline applies to the schema
  design: read `mfm_points_parser.py`'s `esc4` output shape directly before designing the 4th tier,
  don't design from the ticket's prose description alone.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `pipeline_manifest.py --freshness-check` as the **last** command — after every other edit,
  including edits to the handoff itself (leave the handoff's own row in its Files table as
  "(this file)").
