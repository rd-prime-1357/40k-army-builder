# Session handoff — Session 174

**Type: tooling.** No engine change, no data change. Decisions recorded: **D264, D265**.

## 1. Session open

Cloned the repo before trusting the project area. Newest handoff in both places was 173 — no
staleness gap. Diffed the four files S173 flagged as expected push-lag
(`SESSION_HANDOFF_173.md`, `NEXT_SESSION_PROMPT.md`, `pipeline_manifest.py`,
`pipeline_manifest.json`) against the repo: all four matched. That lag had already cleared.

Ran `./baseline.sh --fetch`: failed at `fetch-verify` — `pipeline_manifest.json`'s recorded hash
for `SESSION_HANDOFF_172.md` (`02c6632e...`) did not match the file actually committed to the repo
(`dbaecf1...`). Confirmed two independent ways (`git clone` and the same `codeload` tarball
`baseline.sh` itself fetches) — identical content both times, ruling out a fetch fluke. Git history
shows the handoff committed at 06:37 and the manifest entry that names it committed 38 minutes
later, same session (S173) — the manifest was written from a copy of the file that was not the one
already in the repo. Diff-checked all 128 guarded entries against the verified clone; this was the
only one affected. Root cause unconfirmed — the local copy S173 hashed no longer exists to inspect
— most likely a stale-mount or duplicate-upload artifact, the failure class the standing constraints
already name. Regenerated the manifest against the verified clone rather than guess at the correct
hash (**D264**).

## 2. What was banked

**Manifest reconciled (D264).** Corrected `pipeline_manifest.json` delivered this session. Until
Ryan pushes it, `repo_check` will keep showing this one entry as differing — expected, not a new
problem.

**B76 shipped (D265).** Dropped the frozen version suffixes from the five versioned docs — content
unchanged in every case:

- `40K_Decision_Log_v3_0.md` → `40K_Decision_Log.md`
- `40K_Data_Pipeline_Process_v0_6.md` → `40K_Data_Pipeline_Process.md`
- `40K_Functional_Spec_v0_7.md` → `40K_Functional_Spec.md`
- `40K_Architecture_Overview_v0_5.md` → `40K_Architecture_Overview.md`
- `40K_Data_Dictionary_v2_0.md` → `40K_Data_Dictionary.md`

Updated the two live scripts that name these files (`pipeline_manifest.py`'s `GUARDED` list and
`DECISION_LOG` constant; `repo_check.py`'s `DOC_FILES` list) and the two live cross-references
(`DECISION_INDEX.md`'s header; the P4 entry in `OPEN_ITEMS_BACKLOG.md`). Left every historical
decision-log entry, the closed-backlog archive, `PROCESS_IMPROVEMENT_PLAN.md`'s old S126 file list,
and every session handoff untouched — those are the record of what was true when written, per B76's
own scoping note.

**Action needed from Ryan:** the web uploader can't rename in one step. Upload the five newly-named
files (delivered this session), then delete the five old-named files from the repo:
`40K_Decision_Log_v3_0.md`, `40K_Data_Pipeline_Process_v0_6.md`, `40K_Functional_Spec_v0_7.md`,
`40K_Architecture_Overview_v0_5.md`, `40K_Data_Dictionary_v2_0.md`. Also push the corrected
`pipeline_manifest.py`, `pipeline_manifest.json`, `repo_check.py`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `40K_Decision_Log.md`, and `BACKLOG_ARCHIVE.md`.

Baseline after both fixes: 26/26 gated pass, 2 tier-B skipped (sources not loaded) — clean.

## 3. Decisions still waiting on Ryan (unchanged from S170/S173)

- **B70** — close as not-a-bug, or build the "join another unit, increase Starting Strength"
  mechanic as new scope (M/L)?
- **B73** — should the MFM's own `LEADER` list be authoritative over Wahapedia's broader one,
  roster-wide, wherever both exist?

## 4. Action needed from Ryan (data access, not a product call — unchanged from S173)

B75 (faction pack column resolution) and B85 (keyword-detector false positives) still need a local
run of `faction_pack_transform.py` (current version, with the B85 `B85-CONTEXT` diagnostic) against
2–3 representative packs, at minimum Thousand Sons — console output or the actual pages for p1/p5.

## 5. Files

| File | Status |
|---|---|
| `40K_Decision_Log.md` | renamed (was `40K_Decision_Log_v3_0.md`) + D264/D265 appended |
| `40K_Data_Pipeline_Process.md` | renamed (was `40K_Data_Pipeline_Process_v0_6.md`), content unchanged |
| `40K_Functional_Spec.md` | renamed (was `40K_Functional_Spec_v0_7.md`), content unchanged |
| `40K_Architecture_Overview.md` | renamed (was `40K_Architecture_Overview_v0_5.md`), content unchanged |
| `40K_Data_Dictionary.md` | renamed (was `40K_Data_Dictionary_v2_0.md`), content unchanged |
| `pipeline_manifest.py` | updated — `SESSION_HANDOFF_172.md` hash source no longer relevant; `GUARDED`/`DECISION_LOG` renamed for B76 |
| `pipeline_manifest.json` | reissued (128 guarded files) — corrects the S173 hash defect and reflects the B76 renames |
| `repo_check.py` | updated — `DOC_FILES` renamed for B76 |
| `DECISION_INDEX.md` | updated — D264/D265 added; header cross-reference renamed |
| `OPEN_ITEMS_BACKLOG.md` | updated — B76 closed and moved; P4 cross-reference renamed; running count refreshed |
| `BACKLOG_ARCHIVE.md` | updated — B76's full history appended |
| `SESSION_HANDOFF_174.md` | new (rolling) |
| `NEXT_SESSION_PROMPT.md` | overwritten (S175) |

Exact hashes are in the freshly-reissued `pipeline_manifest.json`, delivered alongside this handoff.

## 6. Backlog

- **Beginning:** 13 open — B69, B70, B73, B75, B76, B85, B86, P2, P4, E23, B67b, E12, B17
- **Resolved:** 1 — B76
- **Added:** none
- **Ending:** 12 open — B69, B70, B73, B75, B85, B86, P2, P4, E23, B67b, E12, B17
