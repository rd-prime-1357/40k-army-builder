# Next-session prompt — Session 158

D240 closed (S157): the four CSM cult-troop units (Khorne Berzerkers, Plague Marines, Rubric
Marines, Noise Marines) are now priced via cross-file `--scope-to-army --append` calls against
their own god-legion's MFM, each isolated to a single-row stats scope so it can't touch any of
CSM's other 54 already-priced units. `units.json` and `unit_loadouts.json` both +4, additive only.
`CSM-1` now asserts a clean 58/58; `E14-2`'s literal moved 64/44 → 65/45. This closes
`CSM_BUILD_SCOPE.md` §4 and the CSM build in full — the only thing left for CSM is M2 (Ryan, GW
source eviction, no Claude action, already unblocked since D237).

## Read this first

`SESSION_HANDOFF_157.md` before starting. If the project area is missing guarded files (including
`40K_Decision_Log_v3_0.md` or standalone `D2NN_entry.md` files), that is expected under the
documented 96%-capacity pruning — clone the public repo directly to verify content rather than
re-flagging or asking Ryan.

## Baseline at open

Full `baseline.sh --no-repo` should be clean (20/20, 70/70 tier-A, 37 tier-B skipped in a
no-live-sources sandbox). If sources are loaded (live session with fetch), tier-B should also pass:
`repro_check.py` and `units_repro_check.py` both byte-identical, `detachments_repro_check.py`
likewise. If anything fails against repo-verified content, that's real drift — reconcile before
starting.

## This session — scope the Thousand Sons build (tooling/scoping-only turn)

Per the standing faction priority roadmap, CSM being complete moves the queue to the remaining
Chaos Marine variants: Thousand Sons, Death Guard, Emperor's Children, World Eaters. Thousand Sons
is next.

This session does NOT build Thousand Sons. It produces `THOUSAND_SONS_BUILD_SCOPE.md`, modeled on
`CSM_BUILD_SCOPE.md`'s shape (real current-edition roster count vs. raw source count including
Legends; which units/points/detachments/enhancements/stratagems are self-contained vs. cross-file;
any shared-datasheet units whose points or stats live outside Thousand Sons' own MFM, the mirror
image of what CSM turn B just closed — Thousand Sons prices Rubric Marines in its own MFM, so
check whether Thousand Sons has any reciprocal gaps of its own). Confirm every claim against
`MFM_Thousand_Sons_v1_0.txt`, `Datasheets.csv`, and the other Wahapedia CSVs directly — source-first,
not derived-data-first. Flag anything genuinely ambiguous (a rules-legality call, not a "how it's
built" call) for Ryan; everything else, decide and note in the scope doc.

## After this session

- Thousand Sons build (turns A/B/C, mirroring CSM's arc) — scoped by this session, built next.
- Then Death Guard, Emperor's Children, World Eaters (remaining Chaos Marine variants), then Chaos
  Daemons, then Drukhari, per the standing faction priority order.
- **M2** (Ryan, evict the 71 GW sources) — unblocked since D237; no Claude action, but don't assume
  it's done without confirming.
