# Next-session prompt — Session 163

**Assigned: Thousand Sons turn B (loadout defaults), data-only.** Reassigned unchanged from the S162
prompt — S162 became a doc-only design turn instead (E25 Force Disposition selection filed, D251).
Turn A shipped S161 (D250): TS has 34 units in `units.json` (362 total), all TS-priced, the six
Scintillating Legions carriers tagged and gated. Turn C (S160, D248) shipped 9 detachments. Turn B is
the last data turn before the TS build's tooling wrap-up.

## Open at session start

Read `SESSION_HANDOFF_162.md` first, then D251 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch --data-turn`. It closed **24/25** at
the end of S162 (tier A; the three repro gates additionally report SKIP without sources), the sole
(expected) failure being `repo_check` on exactly S162's own changed files (7 — listed in the handoff).
If those have been pushed since, this should be clean; if `repo_check` fails on a *different* file
list, stop and reconcile before proceeding.

**Manifest ordering rule (D251):** at close, finish the session handoff's text completely, then issue
`pipeline_manifest.json` last, touching nothing after. S162 opened on exactly this drift from S161.

**Before touching `Thousand_Sons_web.txt`:** per D226's standing process rule, ask Ryan to confirm the
file is current before running the loadout-defaults regeneration turn. Don't assume it's ready.

## Turn B scope

1. Add `TS` to `repro_check.py`'s `FACTIONS` and `Thousand_Sons` to its `WEB_PASSES`, mirroring the
   other six factions' entries exactly.
2. Dry-run `repro_check.py` against the real pipeline (`equipped_parser.py`/`loadout_parser.py` reading
   `Thousand_Sons_web.txt`) before touching the committed `unit_loadouts.json`. Diff the result:
   `THOUSAND_SONS_BUILD_SCOPE.md` §6 estimates **+~24 KB**, additive only (34 new entries, 0
   changed/removed elsewhere) — confirm this holds, don't assume it.
3. Check whether `wargear_points.json` needs anything new. D236 (CSM turn B) found a real gap here —
   MFM wargear silently never picks up until a loadout entry exists for that faction. Check TS's own
   MFM the same way; don't assume TS is clean because CSM needed a fix.
4. Bank `unit_loadouts.json` (and `wargear_points.json` if step 3 finds something) only after the diff
   is traced and clean.
5. Verify `repro_check.py` reproduces byte-identical; run the full assertion suite; confirm nothing
   outside loadout defaults moved.

## Read before touching the allied units (carried forward, still true)

- **`allied_group` is deliberate and must be retained.** B61 shipped it (S133, D208); its four census
  assertions were generalised at S161 (D250) to a single `ALLIED_CARRIER_GROUPS` dict covering Death
  Guard and Thousand Sons. Extend the dict for a future third army; never fork new assertions.
- **The six Scintillating Legions carriers are not duplicates of Chaos Daemons entries.** Different
  `unit_id`s, different points (Pink Horrors 115 TS vs 150 CD; Blue Horrors 90 vs 125). Never source TS
  allied points from the CD pool. Enforced (`Changehost of Deceit` unlock `enforced: true`).
- **Only one of the four Tzaangor-named datasheets carries the TZAANGORS keyword.** `Tzaangors`
  (unit_id `000001034`) is BATTLELINE via `Servants of Change`/`Warpmeld Pact`; the Shaman and both
  Enlightened datasheets carry distinct keywords and are correctly not elevated. If turn B touches any
  of the four, don't assume they share treatment.

## Then, in later sessions

- **TS tooling turn** — TS-specific roster/detachment-count assertions into `rules_assertions.py`
  (mirroring `CSM-1`–`CSM-3`), closing `THOUSAND_SONS_BUILD_SCOPE.md` §8. Turn B's successor, not part
  of turn B (turn typing). Target S164.
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
  `rules_assertions.py`.
- GW-derived material never enters the public repo. The faction pack PDFs, their converted `.md`
  files, and `Thousand_Sons_web.txt` are GW-derived — private sources repo only.
- Diagnoses from prior sessions are re-derived from source before building on them. This has caught
  real regressions four times now (S159, S160, S161, and S162's manifest-ordering drift).
