# SESSION HANDOFF 189

**Turn type:** tooling/doc. Ryan answered both B90 sub-questions in conversation (roster mechanism
direction, edition policy direction) and handed B91's naming call to dev-manager authority, asking
for pros/cons first. Checked both against primary sources before acting on either — a session
transcript is not a source. **Outcome:** shipped. B91 and B92 closed; B90 narrowed to one remaining
sub-question. No engine, data, parser, or assertion touched.

## What happened
1. **Baseline opened green.** `./baseline.sh --fetch --data-turn`, 30/30 (28 gated + repo_check
   expected-fail on doc drift not yet pushed, matching S188's own note). Verified S188's Files-section
   hashes: all matched.
2. **B91 — the two decision-log files were not two competing conventions, they were one settled
   decision (D265/S174) that drifted.** Diffed both files byte-for-byte rather than trusting either's
   self-description or the ticket's own framing. Result: `40K_Decision_Log.md` and
   `40K_Decision_Log_v3_0.md` agree on every line except two spots — `40K_Decision_Log.md` alone
   carries D264–D275, `40K_Decision_Log_v3_0.md` alone carries D276–D281, and D276 was additionally
   inserted out of session order next to D42 rather than appended at the end. No conflicting content
   anywhere — every decision from D0 through D281 exists in exactly one file. Root cause: D265/S174
   already renamed the log off its version suffix and updated every tool reference
   (`pipeline_manifest.py`'s `GUARDED`/`DECISION_LOG`, `repo_check.py`'s `DOC_FILES`, both confirmed
   still correct this session, no changes needed) — but a `_v3_0`-named file reappeared in the repo
   at some later point and sessions kept writing to it instead, undetected because the manifest only
   verifies that its guarded target hasn't changed, not that it's the file actually being edited.
   Merged both into one `40K_Decision_Log.md`: D0–D275 kept as-is, D276 relocated to its correct
   position after D275, D277–D281 appended. Verified programmatically — every D-number 0–281 present
   exactly once, no gaps, no new duplicates introduced by the merge (two pre-existing, already-documented
   quirks — D158/D159 appearing twice, six entries with no heading-line title — carried through
   unchanged, confirmed present in the original file before touching it, not something this session
   caused). New entry **D282** records the reconciliation in the merged file itself.
3. **B91's "secondary" doc-pairs triage turned out trivial, done in the same turn.** The four other
   version-suffixed docs D265 flagged for eventual deletion — `40K_Architecture_Overview_v0_5.md`,
   `40K_Data_Dictionary_v2_0.md`, `40K_Data_Pipeline_Process_v0_6.md`,
   `40K_Functional_Spec_v0_7.md` — were fetched directly from the repo and diffed against their
   renamed counterparts: all four byte-identical. No merge needed, safe to delete outright. B91
   closed in full.
4. **B90's roster mechanism checked against the actual Black Templars MFM file, not against
   recollection.** `MFM_Black_Templars_v1.1.txt` lists no Librarian entry anywhere — confirms the
   already-scoped turn-2 plan (native per-chapter build from each chapter's own MFM, no reference to
   the generic pool) is correct, and rules out a "union the generic list, override named duplicates"
   shortcut, which would still leak the generic Librarian since BT's file has nothing to override it
   with. Ryan confirmed the roster-size target (source count, not the superseded 76) and the
   never-lock-to-one-edition direction; both match what's already decided. One sub-question remains
   open: whether Legends/Forge-World datasheets present in a chapter's MFM (Astraeus, Thunderhawk for
   BT) count as legal roster members.
5. **B92 closed as a duplicate.** Its question — adopt v1.1 or not — was already answered at
   D274/S183, which opened B87/B88/B89 to execute exactly that. B92 restated the same question three
   sessions later without being checked against the earlier decision. Ryan's answer in conversation
   this session matches D274 exactly. B87 (parser support for the v1.1 layout) is the real next
   unblocked step, confirmed by this session, not newly decided.
6. **No engine, data, parser, or assertion touched.** `index.html` unchanged, still v6.15.
   `rules_assertions.py` unchanged, still 116/116.

## State
- Baseline: green at close (verified after the manifest `--write` below).
- `index.html` unchanged, still **v6.15**.
- Live behaviour: unchanged.
- `40K_Decision_Log.md` is a single guarded file again — the "pull the live log manually, it's
  unguarded" step that's been in recent next-session prompts is retired as of this session.
- `repo_check` will show real drift until pushed: the merged `40K_Decision_Log.md`, plus
  `OPEN_ITEMS_BACKLOG.md`, `DECISION_INDEX.md`, `BACKLOG_ARCHIVE.md`, `pipeline_manifest.json`,
  `pipeline_manifest.py` all differ from committed. `40K_Decision_Log_v3_0.md` will show as
  repo-only (net-new — it needs deleting, not adding). Expected, not a problem.

## Ryan action required — repo cleanup, cannot be pushed by this session
After uploading this session's `40K_Decision_Log.md`, delete five old-named files from the repo:
`40K_Decision_Log_v3_0.md`, `40K_Architecture_Overview_v0_5.md`, `40K_Data_Dictionary_v2_0.md`,
`40K_Data_Pipeline_Process_v0_6.md`, `40K_Functional_Spec_v0_7.md`. All five confirmed safe —
either fully merged (the decision log) or byte-identical to their replacement (the other four).

## Decisions still waiting on Ryan
1. **B90, narrowed to one question:** do Legends/Forge-World datasheets present in a chapter's own
   MFM (e.g. Astraeus, Thunderhawk for Black Templars) count as legal matched-play roster members?
   Everything else about B90 turn 2 is now settled.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `40K_Decision_Log.md` | aa096cc6cbe5 | merged; D0–D281 + new D282; replaces both prior copies |
| `OPEN_ITEMS_BACKLOG.md` | 5051c9fd461f | B91, B92 closed; B90 narrowed; 19→17 open |
| `DECISION_INDEX.md` | 7223cf65886b | D282 index entry |
| `BACKLOG_ARCHIVE.md` | b1b87709438d | full B91/B92 closing bodies appended |
| `pipeline_manifest.py` | efca28aca6b8 | `SESSION_HANDOFF_189.md` appended to GUARDED |
| `pipeline_manifest.json` | ca199fb24c4c | regenerated, `--write` |
| `NEXT_SESSION_PROMPT.md` | (see next file) | S190 (unguarded by design) |
| `SESSION_HANDOFF_189.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
17 open, down from 19. Beginning: B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, B87, B88,
B89, B90, B91, B92, E28, B93. Resolved: B91, B92 (closed, D282). Added: none. Ending: B69, B70, B75,
B85, B86, P2, P4, E23, B67b, E12, B17, B87, B88, B89, B90, E28, B93.
