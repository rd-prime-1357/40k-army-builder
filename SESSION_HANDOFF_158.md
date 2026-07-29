# Session Handoff 158

## Baseline at open

Read `NEXT_SESSION_PROMPT.md` (S158 header) and `SESSION_HANDOFF_157.md` as instructed. Memory's
picture of this project (S126, index.html v6.3, E1 backlog, a 6-item backlog) was badly stale —
confirmed the real state from the handoff chain and a live clone of the public repo per standing
practice: S157 closed, decision log through D240, 23/23 gates, 107/107 assertions, 12 open backlog
items (P2, P4, E23, E12, B17, B61, B67b, B69, B70, B71, B72, B73).

`baseline.sh --no-repo` at open: 21/23 gates green. The 35-absent-guarded-file failure was the
documented 96%-capacity mount pruning, confirmed via repo clone, not re-flagged. The other failure was
real: `rules_assertions.py`'s B15-9 ("3 missing datasheets"), not the pruning pattern.

## What was found and fixed before scoping began — B15-9 drift from S157

S157 (D240) added 4 units to `units.json` (the CSM cult troops) but never regenerated
`datasheet_wargear_abilities.json` against the new roster. Three of the four carry a wargear-conferred
ability (Khorne Berzerkers' Icon of Khorne, Rubric Marines' Icon of Flame, Plague Marines' Icon of
Despair) that was missing from the file. Re-ran `ds_wargear_abilities_parser.py` (parser rerun, no
code change, per standing practice — never hand-edit): 45 → 48 datasheets, +3 entries, 0 removed,
additive only. `rules_assertions.py`: 106/107 (sole remainder is the documented mount-pruning gap).

Also found mid-fix: the mounted copy of `40K_Decision_Log_v3_0.md` used to draft D241 was itself one
of the pruning-absent files (empty), not a stale duplicate — rebuilt from a live repo clone before
appending, so no prior decisions were at risk. Separately confirmed the mount's copy of
`40K_Data_Pipeline_Process_v0_6.md` differs from both the manifest hash and the repo's copy — read as
a stale second upload sitting in the area, not real content drift (the repo's copy is authoritative
and unaffected); worth a fresh upload from Ryan next time the area is touched, not urgent.

`pipeline_manifest.py --write` reissued once, covering the wargear-abilities fix — 109 guarded files
(this run's manifest generation borrowed the repo-resident guarded files absent from the area,
per standing practice for reissue; nothing here needs re-uploading to the area itself).

## This session — Thousand Sons build scoped (S158, D241), tooling/scoping-only

Per the standing faction priority roadmap (CSM complete except M2), scoped the next Chaos Marine
variant. `THOUSAND_SONS_BUILD_SCOPE.md` written, modeled on `CSM_BUILD_SCOPE.md`'s shape. Every
number confirmed against live dry runs of `wahapedia_transform.py` and `mfm_points_parser.py`, not
assumed from the prior `MFM_Standalone_Pass.md` audit alone (though it agreed).

**Findings:**
- Real roster: **34** current-edition datasheets (60 raw, 26 Legends-FW excluded).
- No new selection mechanism needed — `Cabal of Sorcerers`/`Pact of Sorcery` are passive army-wide
  text, same shape as CSM's `Blessings of Khorne`; zero matching option rows in
  `Datasheets_options.csv`.
- Detachments: **9** current via the same D192 MFM-authoritative pattern CSM used (3 MFM-only new —
  prose-less, same shape as CSM's two — 3 Wahapedia-only dropped, 6 shared).
- **The reciprocal cross-file-points check this session was asked to run comes back clean.** Thousand
  Sons' own MFM prices all 34 of its own units — 34/34, confirmed by a live dry run. No cross-file
  points call needed anywhere in the TS build, unlike CSM's four cult troops.
- **One real gap: no `Thousand_Sons_web.txt` exists anywhere** (project area or repo). Every other
  faction's loadout defaults come from a hand-pasted Wahapedia composition dump; Thousand Sons has
  none yet. This blocks only the loadout-defaults turn; the roster and detachment turns don't depend
  on it. Flagged to Ryan directly — needs him to source and paste the text before that turn can run.

No committed product file changed by the scoping pass itself; the only content changes this session
are the B15-9 reconciliation, the scope doc, and the rolling docs (decision log, decision index,
backlog, manifest).

## Also this session — GW-source bundle handed to Ryan for the M2 migration

Ryan raised the 96%-capacity concern in light of the TS build's coming growth. Confirmed live: the
70-file GW-derived source set (matches the repo's own `.gitignore` exclude patterns exactly) still
totals 7.2 MB of the 13 MB area — the dominant cost, not anything TS will add (~300-400 KB). M2
(`P4_ARCHITECTURE_SCOPE.md` §6) has been unblocked since D237 and not yet done. Zipped the 70-file set
(`gw_sources.zip`, 1.4 MB compressed) and handed it to Ryan so he can push it into a new private
sources repo, generate a read-only fine-grained token, and send it back for `SOURCE_REPO_TOKEN.txt`.
No deletion from the area yet — that only happens after a live session fetches from the token
successfully and confirms outputs match byte-for-byte, per the standing M2 dress-rehearsal rule.

## Decisions needed

1. **Thousand_Sons_web.txt** — Ryan needs to source and paste the Wahapedia composition text for
   Thousand Sons before the TS loadout-defaults turn can run. Nothing else in the TS build depends on
   it.
2. **M2 setup** — Ryan needs to create the private sources repo, push `gw_sources.zip`'s contents, and
   send back a read-only token. Recommended before or alongside the TS build turns, since it frees far
   more room than TS will ever cost.

## Net New Files

`THOUSAND_SONS_BUILD_SCOPE.md` is net new — no prior file served this role. `gw_sources.zip` is a
one-off operational handoff artifact, not a project pipeline file; not tracked in the manifest or
guarded set.

## Files (SHA-256, first 12 chars)

- `datasheet_wargear_abilities.json` — `6d3afcf63051`
- `40K_Decision_Log_v3_0.md` — `1d001f0378ee`
- `DECISION_INDEX.md` — `e260814d0ad0`
- `OPEN_ITEMS_BACKLOG.md` — `308dea4b10f1`
- `THOUSAND_SONS_BUILD_SCOPE.md` — `3e3877d78167`
- `pipeline_manifest.json` — `f718001b8ca5`
