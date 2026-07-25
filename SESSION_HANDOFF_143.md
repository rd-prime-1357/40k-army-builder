# Session Handoff 143

## Baseline at open

All seven of S142's Files-section hashes verified byte-identical against the mount before any new
work. `./baseline.sh --no-repo` ran clean: 23/23 gates, 102/102 assertions. `repo_check.py` was
absent from the project mount (as S142 flagged) — pulled fresh from the reachable repo and run for
real this session, closing that gap.

## What shipped — B60a closed (D222)

**Turn type: tooling.** `rules_assertions.py` only. Two new assertions pin D221's shape as an
executable fact: exactly 25 detachments carry the chapter-exclusivity sentence in `restrictions` and
zero in `rule_text` (B60a-1); no `restrictions` value contains stratagem/CP debris (B60a-2). Both read
`detachments.json` through the existing `Sources.detachments()` loader. 104/104 assertions pass;
`pipeline_manifest.json` reissued; 23/23 gates hold.

## Also this session — a real repo custody audit (D223), not part of B60a's scope

Running `repo_check.py` for real (rather than continuing to skip it) surfaced two findings that
matter more than B60a:

**Finding 1 — CRITICAL.** `Unit_Weapons.csv` and `wh40k_core_rules.md` are committed to the **public**
repo. Both arrived in a single "Add files via upload" commit dated today, which is also the repo's
entire history — one commit, 99 files. `wh40k_core_rules.md`'s presence directly contradicts D220:
Ryan deleted it from the project area at S142's close specifically because it is GW text and "never
repo-eligible regardless of project-area location," but that deletion never reached the repo — today's
bulk upload re-introduced it from what must have been a stale local backup. Claude has no push
credentials in this environment and could not remediate. Flagged to Ryan as **B67**; recommended fix
is `git commit --amend` to drop both files and force-push, since this is the repo's only commit and
there is no earlier history to preserve.

**Finding 2 — a correction.** D221's closing custody note and `SESSION_HANDOFF_142.md` both stated
`detachments.json` is "not repo-eligible" because it carries GW rule prose. This was checked against
the actual mechanism and found wrong: `pipeline_manifest.json` guards `detachments.json` as an
expected, synced pipeline output; `repo_check.py`'s GW-pattern detection (driven live off
`.gitignore`) does not flag it — no `.gitignore` pattern covers `.json` at all; the file sits in the
repo right now, byte-identical to the project copy; and `index.html` needs it client-side for the
detachment picker to work on the live GitHub Pages site at all. No decision before D221 ever excluded
it. Corrected in the decision log (D223); `detachments.json` continues going to the repo as it always
has.

## Decisions needed

Both carried from the last message, unresolved — "Continue" was taken as authorization to keep
working, not as an answer to either, so I proceeded on my stated recommendations where the action was
mine to take (the `detachments.json` correction — fully reversible, strong mechanical evidence) and
left the one only Ryan can execute open (B67 — I have no push access regardless of which method is
chosen):

1. **B67 remediation method.** Recommended: `git commit --amend` (drop the two files) + force-push —
   complete removal in one step since this is the repo's only commit. Alternative: delete and recreate
   the repo, reconfiguring GitHub Pages after. Ryan's call.
2. **`detachments.json` correction** — proceeded on this one; flagged here in case Ryan wants it
   revisited as a genuine first-time policy call rather than a returned-to-status-quo correction.

## Shipped / changed

`rules_assertions.py` — two new assertions (B60a-1, B60a-2). `pipeline_manifest.json` — reissued.
`40K_Decision_Log_v3_0.md` — D222, D223 appended. `DECISION_INDEX.md` — D222, D223 indexed.
`OPEN_ITEMS_BACKLOG.md` — B60a moved to Closed/Shipped; B67 added to Open Items; P4's capacity note
extended with S143's partial CSM sizing; header counts updated. `NEXT_SESSION_PROMPT.md` — rewritten
for S144.

### Net New Files
None.

### Files (SHA-256, first 12 chars)
- `rules_assertions.py` — `dbc4e975c1ac`
- `pipeline_manifest.json` — `e566d99e0bc4`
- `40K_Decision_Log_v3_0.md` — `d65b70da7207`
- `DECISION_INDEX.md` — `13245da1864f`
- `OPEN_ITEMS_BACKLOG.md` — `071a76fadad7`
- `NEXT_SESSION_PROMPT.md` — `d91023a89e52`

**Repo custody:** `rules_assertions.py` and `pipeline_manifest.json` are repo-eligible, no GW text
touched. The decision log, index, backlog and next-session prompt are repo-eligible docs. Per D223,
`detachments.json` is also repo-eligible (correction — see above) and was **not** touched this
session, so it carries no new hash here. **B67 is still open** — `Unit_Weapons.csv` and
`wh40k_core_rules.md` remain committed to the public repo pending Ryan's remediation; re-run
`repo_check.py` at S144 open to confirm current state before pushing anything new.

## Backlog summary

- **Beginning (7 open):** P2, P4, E23, E12, B17, B61, B60a
- **Resolved (1):** B60a (D222)
- **Added (1):** B67 (repo custody — two GW-derived files on the public repo; Ryan action, D223)
- **Ending (7 open):** P2, P4, E23, E12, B17, B61, B67
