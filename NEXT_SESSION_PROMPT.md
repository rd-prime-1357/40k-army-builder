# Next-session prompt — Session 159

D241 closed (S158): Thousand Sons build scoped in `THOUSAND_SONS_BUILD_SCOPE.md` — 34 current-edition
units, no new mechanism needed, 9 current detachments (same D192 pattern as CSM), fully self-sourced
points (the reciprocal cross-file-points check comes back clean, no cult-troop-style gap). One real
gap: no `Thousand_Sons_web.txt` exists, blocking only the loadout-defaults turn — flagged to Ryan.
Also this session: found and fixed a real B15-9 drift (S157 added 4 units to `units.json` without
regenerating `datasheet_wargear_abilities.json`; +3 entries, additive). Separately, handed Ryan a
70-file GW-source zip for the M2 capacity migration (unblocked since D237, still not done).

## Read this first

`SESSION_HANDOFF_158.md` before starting. If the project area is missing guarded files (including
`40K_Decision_Log_v3_0.md`, `BACKLOG_ARCHIVE.md`, or any `SESSION_HANDOFF_N.md`), that is expected
under the documented 96%-capacity pruning — clone the public repo directly to verify content rather
than re-flagging or asking Ryan.

**Before anything else, confirm whether Ryan has sent a `SOURCE_REPO_TOKEN.txt` token.** If so, that's
the M2 dress rehearsal — see `P4_ARCHITECTURE_SCOPE.md` §6 for the exact procedure (run the next data
turn against the token-fetched private copy while area copies still exist, byte-compare, only then is
deletion eligible). If not, M2 is still pending Ryan-side; proceed with the TS build regardless, since
it doesn't depend on M2.

## Baseline at open

Full `baseline.sh --no-repo` should be clean (23/23; if sources are loaded, tier-B should also pass:
`repro_check.py`, `units_repro_check.py`, `detachments_repro_check.py` all byte-identical).
`rules_assertions.py` should be 107/107 (up from 106/107 — B15-9 was fixed this session). If anything
fails against repo-verified content, that's real drift — reconcile before starting, the way S158 did
for B15-9.

## This session — Thousand Sons build, turn A (data-only)

Per `THOUSAND_SONS_BUILD_SCOPE.md` §8, run turn A: `wahapedia_transform.py --faction TS` →
`mfm_points_parser.py` against `MFM_Thousand_Sons_v1_0.txt` (self-sourced, no cross-file append step
needed — confirmed 34/34 in scoping) → convert → merge → post-processors. Add TS's config lines to
`units_repro_check.py` (new per-faction block, fifth `--in` to the merge call) and `repro_check.py`
(`FACTIONS`). Regenerate `units.json` (328 → 362), diff-trace every change, confirm 0 changed/removed
elsewhere. Bank before moving to turn C (detachments) — do not mix data turns with the tooling turn.

Turn B (loadout defaults) stays blocked until `Thousand_Sons_web.txt` arrives from Ryan; turns A and C
don't depend on it and can both ship first.

## After this session

- Thousand Sons turn C (detachment build) and the tooling turn (assertions, manifest) — per
  `THOUSAND_SONS_BUILD_SCOPE.md` §8.
- Thousand Sons turn B (loadout defaults) — blocked on Ryan sourcing `Thousand_Sons_web.txt`.
- Then Death Guard, Emperor's Children, World Eaters (remaining Chaos Marine variants), then Chaos
  Daemons, then Drukhari, per the standing faction priority order.
- **M2** — Ryan side, in progress as of S158 (zip handed over); confirm status, don't assume done.
