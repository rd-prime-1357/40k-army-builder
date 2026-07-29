# Next-session prompt — Session 157

B74 closed (S156, D239): `detachment_effects.json` gained the Chaos Cult BATTLELINE row,
`e21b_check.js`'s pinned count updated 4→5. This closes the CSM tooling arc from
`CSM_BUILD_SCOPE.md` §8 in full. 107/107 assertions pass, 23/23 gates green.

Also fixed at S156 open: a real `pipeline_manifest.py` sync-order bug (S155's write ran before
`DECISION_INDEX.md`/`OPEN_ITEMS_BACKLOG.md` reached final edited state, never repeated). Reissued
clean. And: confirmed via a live repo clone that the decision log and all guarded files are intact
in the repo — the project area's repeated absences are pruning under 96% capacity, not repo drift.
D237/D238 folded into the main log; all six standalone `D2NN_entry.md` files deleted.

## Read this first

`SESSION_HANDOFF_156.md` before starting. The decision log and backlog are both current as of D239 —
no standalone `D2NN_entry.md` fallback files remain; if the project area's `40K_Decision_Log_v3_0.md`
is absent again, treat it as area-capacity pruning per S156's finding and pull it from the repo
directly rather than re-flagging or banking standalone again.

## Baseline at open

Full `baseline.sh --no-repo` should be clean (23/23, 107/107). If the project area is missing guarded
files, that's expected under 96% capacity — clone the public repo directly to verify content rather
than treating mount absence as a signal. If anything actually fails against the repo-verified content,
that's real drift; reconcile before starting.

Worth a proactive check this session: run `pipeline_manifest.py` against the full repo-cloned tree (not
just whatever the area happens to hold) at least once per session going forward, since S156 showed a
partial area can silently hide a real manifest mismatch for multiple sessions.

## This session — CSM cult-troop cross-file points (data-only turn)

The last piece of the CSM roster gap (54/58 → 58/58), per `CSM_BUILD_SCOPE.md` §4. Four cult-troop
units — Khorne Berzerkers, Plague Marines, Rubric Marines, Noise Marines — are shared across CSM and
their respective god-legion factions, and need their points sourced cross-file rather than from CSM's
own MFM file alone. Re-read `CSM_BUILD_SCOPE.md` §4 for the exact sourcing rule before starting; this
is a genuine data-sourcing question, not a mechanical regeneration, so confirm the cross-file lookup
logic against source before writing anything to `units.json`.

## After this session

- **M2** (Ryan, evict the 71 GW sources) — unblocked since D237; no Claude action, but don't assume
  it's done without confirming.
- Faction priority roadmap: once CSM's roster gap closes, CSM is essentially complete. Next in
  priority order per the standing faction list: Thousand Sons, Death Guard, Emperor's Children, World
  Eaters (remaining Chaos Marine variants), then Chaos Daemons, then Drukhari.
