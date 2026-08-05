# NEXT SESSION PROMPT — Session 190

## Turn type: decided by what's been answered when the session opens (see below).

Read `SESSION_HANDOFF_189.md` first, then this prompt. Read **D282** in `40K_Decision_Log.md` in
full — the decision log is a single guarded file again as of this session; there is no separate
unguarded live copy to pull manually anymore. If a stray `40K_Decision_Log_v3_0.md` turns up in the
repo or the project area, that is exactly the resurrection pattern D282 diagnosed — do not write to
it, and flag it rather than assuming it's fine.

## Session open
1. Data-turn baseline with sources: `./baseline.sh --fetch --data-turn`.
2. Verify the S189 hashes in the handoff's Files section at open.
3. Confirm Ryan has pushed S189's changes and deleted the five old-named files
   (`40K_Decision_Log_v3_0.md`, `40K_Architecture_Overview_v0_5.md`, `40K_Data_Dictionary_v2_0.md`,
   `40K_Data_Pipeline_Process_v0_6.md`, `40K_Functional_Spec_v0_7.md`). If not yet done, that's
   expected drift, not a failure — proceed, but don't write new content to any old-named file if one
   is still present.

## Two things could be true at open — check in this order

**If Ryan has answered B90's remaining sub-question (do Legends/Forge-World datasheets in a
chapter's own MFM count as legal roster members) →** resume B90 turn 2 (DATA turn): new
complete-roster pipeline path per D276/D282's confirmed mechanism, rebuild the five Tier-2 chapters
in `units.json` directly from their own MFM files, flip `roster_mode` to `'complete'` for those five,
update `resolved_pool()`, re-verify `unit_loadouts.json`/`wargear_points.json`. This is now
unblocked on everything except that one question and B87–B89 clearing first (see below) — do not
start it until both are true. Do not mix with anything else this session.

**Else → B87 (MFM v1.1 parser layout support), the confirmed next unblocked item.** D274/S183's
edition-adoption arc (B87→B88→B89) has been open and untouched since it was opened; D282 confirmed
this session that its underlying decision was never actually in question and Ryan reconfirmed the
same direction independently. Build one parser with a per-file format sniff (v1.1's layout is
self-identifying — new section headers, the "▼" marker) with per-layout readers behind it; v1_0
files must still parse to identical output through the sniff path. Full scope in the B87 backlog
entry. **Tooling turn.** Per D274's own sequencing, this arc runs ahead of B90 turn 2's rebuild —
even if Ryan answers the Legends/Forge-World question this session, B87 still comes first unless
Ryan explicitly says otherwise.

If neither is available, fall back to the next backlog item under the faction priority order rather
than blocking.

## Standing reminders
- Turn-typing strict. Fix parsers, never hand-edit output; merge-passthrough/hand-authored JSON
  (`detachment_effects.json`, `faction_taxonomy.json`, and its four lookup siblings) goes through a
  script/serialiser, never a manual edit.
- Source-first: S189 is a working example of why this matters even for things that feel settled —
  B91 looked like an open naming choice and was actually a five-session-old decision that drifted;
  B92 looked like a new question and was a duplicate of one already answered; B90's mechanism looked
  right from a session's own prior description and turned out to need a direct source read (the
  Black Templars MFM file itself) before it could be confirmed. In each case, checking the primary
  source or the primary decision — not the most recent summary of it — is what caught the gap.
- Close by producing the four documents, regenerating the manifest with `--write`, and running
  `--freshness-check` as the **last** command — after every other edit, including edits to the
  handoff itself (leave the handoff's own row in its Files table as "(this file)" rather than
  computing a hash of itself).
