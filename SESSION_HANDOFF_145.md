# Session Handoff 145

## Baseline at open

Mount check found real drift, not a stale sync: the two files S144 explicitly hashed —
`Space_Marines_web.txt` and `Chaos_Space_Marines_web.txt` — no longer matched that handoff's
recorded hashes, and `Space_Wolves_web.txt` (a `P4_REQUIRED_SOURCES` entry and one of
`repro_check.py`'s five web-passes) was entirely absent. `./baseline.sh --no-repo` failed 2/23
(`repro_check`, `rules_assertions`), both on the missing Space Wolves file. Reconciled before
proceeding, per protocol — see below.

## What happened — D225, data-only (with a large verification component)

**B67 corrected and closed.** D223 recommended `git commit --amend` on the belief the repo was a
single commit. `repo_check.py` is absent from the project mount (as it has been since S141/S142) —
pulled fresh from the repo and, this time, backed by an actual clone rather than the script's own
summary: **249 commits**, not one. `Unit_Weapons.csv` and `wh40k_core_rules.md` were each added in
exactly one commit and never touched again, so the exposure was contained, not smeared. Ryan deleted
both directly from the repo; confirmed gone from HEAD via the GitHub API. B67 closes on that. The two
commits that introduced them remain reachable in history — a real difference from D223's "no earlier
history to preserve" — so a full purge needs a history rewrite and force-push. Filed as **B67b**, low
priority, optional, Ryan's call.

**Three source-file edits verified against the real pipeline, not taken on stated belief.** Ryan
supplied a complete `Dark_Angels_web.txt` (replacing an incomplete prior version) and a complete
`Space_Wolves_web.txt` (built with a script he intends to use for the remaining `_web.txt` files —
LF line endings, unlike the CRLF convention of the hand-sourced files; first uploaded as
`Space-Wolves_web.txt`, renamed to the required underscore form). Ran the real pipeline — first with
Space Wolves still missing to get a partial read, then complete once it arrived — and diffed against
the then-committed `unit_loadouts.json`. Every difference traced to a specific cause: twenty were
Space-Wolves-eligible named characters that had never carried a `_defaults_source` tag (no working
Space Wolves file had ever run before); one was a genuine pre-existing Dark Angels bug on the
Ravenwing Dark Talon (`000000240`) — committed defaults were missing the model's second Hurricane
bolter, confirmed directly against `Dark_Angels_web.txt`'s own text, now fixed. No parser errors, no
unexplained differences. `Space_Marines_web.txt` was separately re-edited by Ryan (via ChatGPT) since
D224's check — re-verified the same way, clean.

**`unit_loadouts.json` regenerated.** 124,652 → 125,329 bytes. Manifest reissued. Full baseline now
**23/23 gates, 104/104 assertions.** `Chaos_Space_Marines_web.txt` untouched — still awaiting its own
scoped data-build turn.

## Decisions needed

None blocking.

- **B67b** (history purge) — optional, not time-sensitive. Ryan's call whether it's worth doing.
- **Capacity reads 96%** (Ryan-reported, after the Chaos Space Marines addition and the Dark Angels
  replacement).
- Ryan plans to regenerate the remaining hand-sourced `_web.txt` files (Black Templars, Death Guard, a
  rerun of Space Marines) with the same script used for Space Wolves. Recommendation: one file at a
  time, each its own verified data-only turn — not a batch. **D226: before starting any of these,
  Claude pauses and explicitly asks Ryan to load that faction's new file, then waits — never assumes
  it's ready.** Expected capacity return from the regeneration alone is modest (line-ending savings
  only); the decision-log archive split flagged since D211/P4 step 1 is very likely the bigger,
  lower-risk lever and hasn't been attempted yet.
- `40K_Data_Pipeline_Process_v0_6.md` differs from its repo copy (project-area copy carries the B56a
  chapter-points scoping steps the repo copy lacks) — pre-existing gap, not from this session, flagged
  for the next repo batch upload.

## Shipped / changed

`unit_loadouts.json` regenerated and re-banked. `pipeline_manifest.json` reissued. `40K_Decision_Log_v3_0.md`
— D225 and D226 appended. `DECISION_INDEX.md` — D225 and D226 indexed. `OPEN_ITEMS_BACKLOG.md` — B67 closed, B67b opened,
P4 updated with the S145 capacity read and the one-at-a-time recommendation, header updated. Verified
(not changed by Claude): `Space_Wolves_web.txt`, `Dark_Angels_web.txt`, `Space_Marines_web.txt` — all
Ryan's edits.

### Net New Files
None.

### Files (SHA-256, first 12 chars)
- `unit_loadouts.json` — `7e66fcf1fcda`
- `pipeline_manifest.json` — `fc90bda51197`
- `40K_Decision_Log_v3_0.md` — `66d60ca1123e`
- `DECISION_INDEX.md` — `5604f444873d`
- `OPEN_ITEMS_BACKLOG.md` — `dac61ab48ae6`
- `NEXT_SESSION_PROMPT.md` — `1289a396b38d`

**Repo custody:** `unit_loadouts.json` and `pipeline_manifest.json` are repo-eligible pipeline
outputs, changed — belong in the next batch upload alongside this handoff and the doc set above.
`Space_Wolves_web.txt`, the updated `Dark_Angels_web.txt`, and `Space_Marines_web.txt` are GW-derived
source, excluded under the existing `.gitignore` pattern — no repo action. `Unit_Weapons.csv` and
`wh40k_core_rules.md` confirmed removed from the repo's HEAD (B67).

## Backlog summary

- **Beginning (7 open):** P2, P4, E23, E12, B17, B61, B67
- **Resolved (1):** B67
- **Added (1):** B67b
- **Ending (7 open):** P2, P4, E23, E12, B17, B61, B67b
