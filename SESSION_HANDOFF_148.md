# Session Handoff 148

## Baseline at open

S147's substantive hashes matched byte-for-byte (all ten of: units.json, abilities.json, rules.json,
weapon_abilities.json, datasheet_wargear_abilities.json, units_repro_check.py, rules_assertions.py,
pipeline_manifest.json, DECISION_INDEX.md, OPEN_ITEMS_BACKLOG.md). `baseline.sh --no-repo` ran 21/23
gates green; the two failures name exactly the seven B68 unit_ids (`repro_check` and its embedded P1
in `rules_assertions.py`) — the diagnosed, carried-forward state from D230, not a new regression.

One reconciled mismatch, not a bad sync: `NEXT_SESSION_PROMPT.md`'s hash did not match S147's handoff.
The prompt's content post-dates the handoff — it documents Ryan's decision-log removal and drops the
archive-split idea the handoff still recommended. All substantive files matched. This is exactly the
false-alarm case P4 addresses by dropping the prompt from the hash list going forward (see D231).

`40K_Decision_Log_v3_0.md` remains intentionally repo-only (D-log removed from the area at S147's
close for capacity; `DECISION_INDEX.md` stays as the in-area lookup). Confirmed present and current in
the fetched repo copy through D230.

## What happened — D231, P4 scoped (no build)

P4 was this session's assigned work: a scoping/design note for the project area's long-term
architecture. Delivered as `P4_ARCHITECTURE_SCOPE.md`. No app, data, gate, parser, or protocol changed
this session — scoping only. Full reasoning in D231; the shape:

- **Target:** the area's size becomes independent of faction count. Area = per-session working set
  (~450 KB); built data and GW sources become fetch-on-demand into the workspace.
- **Three homes:** public repo (built outputs + all tooling/docs, already true and verified current
  this session), a new private repo `rd-prime-1357/data-sources` (the 71 GW source files), and the
  slimmed area.
- **Open redesigned:** verify area → fetch public repo as one tarball, verify against an extended
  `pipeline_manifest.json` → overlay working set → on data turns fetch the private sources repo with a
  token, verify against a new `source_manifest.json` → gates, tiered.
- **Gates tiered:** Tier A every open (no sources), Tier B when sources load / mandatory at data-turn
  open+close (the three repro rebuilds + source-first assertions). Loud, counted skips; no
  fixed-point protection lost.
- **`repo_check.py` recovered** as a standing tier-A gate (it lives in the repo; the fetch-open brings
  it back after its long `--no-repo` absence).

### Ryan's custody decisions, settled this session

- Accept-risk for the pre-release window: GW text in a *private* repo is OK for now; **public launch
  is the checkpoint to revisit.**
- Private sources repo (created this session, Private, no README/.gitignore/license — all correct for
  a repo holding third-party source material). Zip demoted to offline fallback.
- Read-only single-repo token stored in the area as `SOURCE_REPO_TOKEN.txt` (no per-session paste),
  made safe by a hard `repo_check.py` guard that fails the session if the token filename ever reaches
  a public-repo-bound file list.
- App stays in the public repo; only sources go private.

### Migration order (dev-manager call)

M0 (next session, tooling-only, no eviction) → M1 (Ryan evicts repo-resident set, screenshot-verified)
→ B68 (engine) → CSM turn B as the M2 dress rehearsal → M2 (evict the 71 sources) → CSM turn C. One
added session total (M0). M0 before the remaining CSM turns because the area is at capacity now.

## Decisions needing Ryan (carried into M0)

Both are low-stakes and M0 proceeds on them unless Ryan says otherwise:
1. Bulk-deletion verification amendment (M1/M2): full file-list screenshots before/after each eviction
   batch, in place of per-file cards. (Migration steps only.)
2. The overall shape was approved verbally this session ("go"); M0 is cleared to build.

## Net New Files

- `P4_ARCHITECTURE_SCOPE.md` — the long-term-architecture plan. No prior file plays this role
  (`PROCESS_IMPROVEMENT_PLAN.md` is the superseded S126 tooling plan, not an architecture design).

Not built yet, named here so M0 knows to create them: `source_manifest.json` (new data file, M0),
`SOURCE_REPO_TOKEN.txt` (created by Ryan at M2), `gw_sources.zip` (fallback, built by Ryan at M2).

## Files (SHA-256, first 12 chars)

Changed / delivered this session:
- `P4_ARCHITECTURE_SCOPE.md` — `e94b0d6c402f`
- `40K_Decision_Log_v3_0.md` — reissued with D231 appended; hash recomputed at push (repo-only file)
- `DECISION_INDEX.md` — updated with the D231 one-liner; hash at close below
- `OPEN_ITEMS_BACKLOG.md` — P4 entry updated (scoped; M0–M3 recorded); hash at close below
- `NEXT_SESSION_PROMPT.md` — reissued for S149/M0

Unchanged this session (carried from S147, re-verify at S149 open): units.json `eb370386ccf7`,
abilities.json `051bdd9ceb08`, rules.json `b347222a3bc9`, weapon_abilities.json `ff4379837df4`,
datasheet_wargear_abilities.json `af5be2824e54`, units_repro_check.py `81cb0f825727`,
rules_assertions.py `f793cf479349`, pipeline_manifest.json `fa8073b131eb`.

**Repo custody:** `P4_ARCHITECTURE_SCOPE.md`, the decision log, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, and `NEXT_SESSION_PROMPT.md` are all project-authored prose/config — no
GW-derived text — and belong in the next public-repo batch. No GW source introduced this session.
Excluded as always: the Wahapedia CSV export, the MFM `.txt` files, the faction web/pack files. The
new private repo is the home for those going forward (from M2); nothing GW-derived goes to the public
repo.

**Capacity note (P4):** this session added only `P4_ARCHITECTURE_SCOPE.md` (~19 KB of prose) to the
area — no JSON growth. The area remains at/near capacity; M0→M1 is the structural fix and is now the
top of the queue for exactly this reason.

## Backlog summary

- **Beginning (8 open):** P2, P4, E23, E12, B17, B61, B67b, B68
- **Resolved (0):** none — P4's *scoping* shipped, but P4 stays open (M0–M3 build remains)
- **Added (0):** none
- **Ending (8 open):** P2, P4, E23, E12, B17, B61, B67b, B68
