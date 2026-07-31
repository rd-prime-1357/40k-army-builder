# Session handoff — Session 175

**Type: audit-only.** No engine change, no data change, no code change. Decision recorded: **D266**.

## 1. Session open

Cloned the repo before trusting the project area. Newest handoff in both places was 174 — no
staleness gap. One finding: `40K_Decision_Log.md` was absent from the project mount entirely this
session (not even under its old name), despite `DECISION_INDEX.md` and everything else being
present. Verified independently via the repo clone rather than guessing — D264/D265 are there and
match S174's account, so the content is fine; the gap is in what the mount showed this session.
Flagged to Ryan for a file-list screenshot; not treated as data loss.

Ran `./baseline.sh --fetch`: 25/25 gates pass, 3 tier-B skipped (sources not yet loaded). Later in
the session ran `./baseline.sh --fetch --data-turn` to pull GW sources for the B73 re-derivation:
29/29 gates pass, all tier-B included, rules_assertions 110/110. No reconciliation needed either way.

## 2. What was banked

**B70 and B73 — Ryan's decisions taken (D266).**

- **B70:** build the join/Starting-Strength mechanic. New scope, sizing not yet redone (D260
  estimated M/L). Needs its own scoping turn — analysis-typed, since it decides how "join and
  increase Starting Strength" works in general, not just for Wardens.
- **B73:** MFM authoritative wherever both exist, Wahapedia only where the MFM has no `LEADER`
  block for that character — Ryan's exact call, taken as recommended.

**Re-deriving B73 from source before building found the fix is bigger than D260 described.** Per
the standing rule that diagnoses from prior sessions get re-derived, not trusted, I read
`mfm_points_parser.py` directly and checked it against the actual MFM text (`MFM_Space_Marines_v1_0.txt`
— the file `40K_Data_Pipeline_Process.md`'s own documented command names, not `mfm_sm.txt`, a
same-shaped file that also sits in the source set but isn't what the pipeline invokes). Result:
D260's account ("the backfill does not distinguish LEADER and SUPPORT — it copies whichever it
finds") doesn't match the code as it stands. There is exactly one collection trigger in the parser,
the literal string `SUPPORT`; nothing in the file ever matches on `LEADER`. So the parser isn't
choosing the wrong list between the two — it never reads `LEADER` blocks at all. Confirmed against
the real text: Wardens' block is headed `SUPPORT` (matches D260), but Kor'sarro Khan's block, two
entries later, is headed `LEADER` with a six-unit list narrower than his Wahapedia-derived one — and
that block is invisible to today's parser. Counted across `MFM_Space_Marines_v1_0.txt` alone: 34
`LEADER` headers, 16 `SUPPORT` headers.

This means B73's fix needs a new collection path for `LEADER` blocks (parallel to the existing
`SUPPORT` path, but written to its own field — the two headers mean different things, and conflating
them is exactly the bug) before any override logic can run, plus a rule scoping the override to named
Epic Heroes with their own datasheet id while leaving the generic shared datasheets (Captain,
Chaplain, Librarian, Ancient, Apothecary, Lieutenant) on existing behavior — D260 found that broad
list intentional there, and the S170 audit never tested that case. Not a same-session patch.

**Also surfaced, touching B70:** today's blank-fill backfill only ever draws from `SUPPORT`-headed
blocks, and for Wardens (blank Wahapedia cell, no Leader ability) it fills `leader_eligible_units`
from its `SUPPORT` list — mislabeling a join-eligible-units list as leader data. Fixing B73 properly
(capture `LEADER` separately, stop treating `SUPPORT` content as leader data) also cleans up this
mislabeling, which is the data half of what B70's join mechanic will need. Sequencing note for
whoever scopes these: do B73's parser rework before finalizing B70's data needs.

**Ryan also noted MFM source updates will need providing at some point** — logged for future data
turns, no action needed now.

**Nothing shipped.** No parser, engine, or data file was touched this session — only read. B70 and
B73 stay open, now scoped by Ryan's decision rather than blocked on it.

## 3. Decisions still waiting on Ryan

None from B70/B73 — both decided this session. Unchanged from S174:

**B75 + B85 (data access, not a product call).** Still need a local run of `faction_pack_transform.py`
(current version, B85-CONTEXT diagnostic) against 2–3 packs, at minimum Thousand Sons — console
output or the actual pages for p1/p5.

## 4. Candidates that don't need Ryan first

- **E23** — Tank Ace Character grant. Needs a scoping turn — analysis-typed, flag model/effort
  before starting.
- **B70/B73 scoping/build** — both now decided by Ryan; each still needs its own scoping turn before
  code. Flag model/effort before starting either — this session's re-derivation already showed a
  wrong-mechanism assumption would have shipped an incomplete fix.
- **B86** — Chaos Daemons pack p13, image-only, confirm by eye. Blocked on the same PDF-access gap
  as B75/B85.
- **P4** — project-area capacity. Ryan reported 80% again this session (unchanged trend from S172's
  73%). Checked what M0/M2 setup actually exists in the area: `SOURCE_REPO_TOKEN.txt` (93 bytes, real
  token) and `source_manifest.json` (70-file hashes) are both already in place, so the M2 groundwork
  looks done — but the area still holds everything the plan says should already be evicted
  (`units.json`, `detachments.json`, all parsers/checks, and at least one GW source file,
  `Thousand_Sons_web.txt`, still sitting in the area). M1/M2 eviction itself hasn't happened yet
  despite the setup being ready. Worth deciding whether to run the eviction now rather than defer
  again.

## 5. Files

| File | Status |
|---|---|
| `40K_Decision_Log.md` | D266 appended |
| `DECISION_INDEX.md` | D266 index entry added |
| `OPEN_ITEMS_BACKLOG.md` | B70/B73 entries rewritten with Ryan's decisions + corrected mechanism; running count line added for S175 (still 12 open) |
| `SESSION_HANDOFF_175.md` | new (rolling) |
| `NEXT_SESSION_PROMPT.md` | overwritten (S176) |

## 6. Backlog

- **Beginning:** 12 open — B69, B70, B73, B75, B85, B86, P2, P4, E23, B67b, E12, B17
- **Resolved:** none
- **Added:** none
- **Ending:** 12 open — B69, B70, B73, B75, B85, B86, P2, P4, E23, B67b, E12, B17
