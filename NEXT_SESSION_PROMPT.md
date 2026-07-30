# Next-session prompt — Session 164

**Assigned: Thousand Sons tooling turn (tooling-only).** Turn B (loadout defaults) shipped S163
(D252): `unit_loadouts.json` +34 TS entries (309 total, additive-only), `wargear_points.json` +1 entry
(TS Defiler, same class of gap D236 found for CSM), `repro_check.py` registered TS, E14-2 corrected
65/45 -> 75/54. This is the TS build's tooling wrap-up — roster/detachment-count assertions into
`rules_assertions.py`, mirroring `CSM-1`–`CSM-3`, closing `THOUSAND_SONS_BUILD_SCOPE.md` §8.

## Open at session start

Read `SESSION_HANDOFF_163.md` first, then D252 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch --data-turn`. It closed clean at the
end of S163 once the manifest was reissued (see handoff §3/§5); the only expected drift before push is
`repo_check` on exactly S163's changed files. If those have been pushed since, this should be clean; if
`repo_check` fails on a *different* file list, stop and reconcile before proceeding.

**Manifest ordering rule (D251, still standing):** at close, finish the session handoff's text
completely, append its own filename to `pipeline_manifest.py`'s `GUARDED` at creation time (not after),
then issue `pipeline_manifest.json` last, touching nothing after.

## Tooling turn scope

TS already has its detachment census (`TS-1`, `TS-2`, shipped S160/D248). Missing is the roster
census, mirroring `CSM-1`:

1. Add a `TS-3` (or similarly named) assertion confirming `units.json` carries all 34 current Thousand
   Sons units (`THOUSAND_SONS_BUILD_SCOPE.md` §1 for the source-verified count — confirm it still reads
   34, don't assume S161's turn-A number is still current without checking).
2. Check whether a no-prose-detachment assertion (mirroring `CSM-3`) is even needed for TS: `TS-2`
   already states all 9 TS detachments have real text (none are `text_source: none`), so this may
   already be fully covered — verify rather than adding a redundant assertion.
3. Any other TS-specific structural fact currently only true by inspection (not yet an executable
   check) that `THOUSAND_SONS_BUILD_SCOPE.md` §8 calls out — read that section fresh, don't rely on
   a remembered list.
4. Run the full assertion suite and confirm the new count; update `pipeline_manifest.json` last.

This is tooling-only: no `units.json`, `unit_loadouts.json`, or `detachments.json` changes in this
session. If anything looks like it needs a data fix while doing this, stop and flag it rather than
mixing turn types.

## Read before touching the allied units (carried forward, still true)

- **`allied_group` is deliberate and must be retained.** B61 shipped it (S133, D208); its four census
  assertions were generalised at S161 (D250) to a single `ALLIED_CARRIER_GROUPS` dict covering Death
  Guard and Thousand Sons. Extend the dict for a future third army; never fork new assertions.
- **The six Scintillating Legions carriers are not duplicates of Chaos Daemons entries.** Different
  `unit_id`s, different points (Pink Horrors 115 TS vs 150 CD; Blue Horrors 90 vs 125). Never source TS
  allied points from the CD pool.
- **Only one of the four Tzaangor-named datasheets carries the TZAANGORS keyword** (`Tzaangors`,
  `000001034`). The Shaman and both Enlightened datasheets are correctly not elevated.

## Then, in later sessions

- **E25 — Force Disposition selection** — engine-only, designed and filed S162 (D251); full spec in
  the backlog ticket. Target S165, after the TS arc closes. Data side already done (169/169 records
  carry exactly one disposition; `e1a` pins it); no parser or transformer change needed.
- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, never hand-edit output).
  Re-check the ticket's framing against source before starting; it may be stale from before turn A.
- **B75** — Rules Updates column resolution. Awaiting Ryan's flag counts across the pack set.
- **B76** — rolling documents drop version numbers. Stays behind the TS build.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`. But a hardcoded total (like E14-2) is expected to drift as data grows; when it
  does, re-derive and correct the number rather than treating the drift itself as a bug.
- GW-derived material never enters the public repo.
- Diagnoses from prior sessions are re-derived from source before building on them. This has caught
  real regressions five times now (S159, S160, S161, S162's manifest-ordering drift, and S163's
  E14-2 stale count).
