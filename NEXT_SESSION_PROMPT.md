# Next-session prompt — Session 162

**Assigned: Thousand Sons turn B (loadout defaults), data-only.** Turn A shipped S161 (D250) — TS now
has 34 units in `units.json` (362 total across all armies), all TS-priced, the six Scintillating
Legions carriers tagged and gated. Turn C (S160, D248) shipped 9 detachments. Turn B is the last data
turn before the TS build's tooling wrap-up.

## Open at session start

Read `SESSION_HANDOFF_161.md` first, then D250 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch --data-turn`. It closed **24/25** at
the end of S161, the sole (expected) failure being `repo_check` — 12 files differing from the pushed
repo, confirmed to be exactly S161's own changes. If S161's files have been pushed since, this should
now be **25/25**; if `repo_check` still fails on a *different* file list than S161's, stop and reconcile
before proceeding — don't assume it's the same known gap without checking.

**Before touching `Thousand_Sons_web.txt`:** per D226's standing process rule, ask Ryan to confirm the
file is current before running the loadout-defaults regeneration turn. Don't assume it's ready without
asking.

## Turn B scope

1. Add `TS` to `repro_check.py`'s `FACTIONS` and `Thousand_Sons` to its `WEB_PASSES`, mirroring the other
   six factions' entries exactly.
2. Dry-run `repro_check.py` against the real pipeline (`equipped_parser.py`/`loadout_parser.py` reading
   `Thousand_Sons_web.txt`) before touching the committed `unit_loadouts.json`. Diff the result:
   `THOUSAND_SONS_BUILD_SCOPE.md` §6 estimates **+~24 KB**, additive only (34 new entries, 0
   changed/removed elsewhere) — confirm this holds, don't assume it.
3. Check whether `wargear_points.json` needs anything new. D236 (CSM turn B) found a real gap here —
   MFM wargear silently never picks up until a loadout entry exists for that faction. Check TS's own MFM
   for wargear entries the same way, don't assume TS is clean just because CSM needed a fix.
4. Bank `unit_loadouts.json` (and `wargear_points.json` if turn 3 finds something) only after the diff is
   traced and clean.
5. Verify `repro_check.py` reproduces byte-identical; run the full assertion suite; confirm nothing
   outside loadout defaults moved.

## Read before touching the allied units (carried forward, still true)

- **`allied_group` is deliberate and must be retained.** B61 shipped it (S133, D208); its four census
  assertions were generalised at S161 (D250) to cover Death Guard *and* Thousand Sons via a single
  `ALLIED_CARRIER_GROUPS` dict. Do not reduce `allied_group` to a provenance field, and if a future
  session adds a third allied-group army, extend that dict rather than forking new assertions.
- **The six Scintillating Legions carriers are not duplicates of Chaos Daemons entries.** Different
  `unit_id`s, different points (Pink Horrors 115 TS vs 150 CD; Blue Horrors 90 vs 125). Never source TS
  allied points from the CD pool. This is now enforced (`Changehost of Deceit`'s unlock is
  `enforced: true`), not just tagged.
- **Only one of the four Tzaangor-named datasheets carries the TZAANGORS keyword.** `Tzaangors` (unit_id
  `000001034`) is BATTLELINE via `Servants of Change`/`Warpmeld Pact`; Tzaangor Shaman and both Tzaangor
  Enlightened datasheets carry their own distinct keywords and are correctly not elevated. If turn B's
  loadout-defaults pass touches any of the four, don't assume they share treatment.

## Then, in later sessions

- **Tooling turn** — TS-specific roster/detachment-count assertions into `rules_assertions.py`
  (mirroring `CSM-1`–`CSM-3`), closing `THOUSAND_SONS_BUILD_SCOPE.md` §8 in full. This is turn B's
  natural successor, not part of turn B itself (turn typing).
- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, never hand-edit output).
  Untouched since S159; still open. Note `keyword_names` per model_group already carries real keywords
  (`Chaos`, `Infantry`, `Mutant`, `Tzaangors`, `Tzeentch`, etc.) — B77 is specifically about the
  `SCINTILLATING LEGIONS` faction-level keyword Rituals/stratagems reference, which is genuinely absent,
  not about the per-unit keyword list being empty (re-check this framing against source before starting;
  it may be stale from when the six carriers still had empty keyword lists pre-turn-A).
- **B75** — Rules Updates column resolution (pages 1/9 of the TS pack, and Death Guard's equivalent).
  Awaiting Ryan's flag counts across the pack set to size it. Untouched this session; still open.
- **B76** — rolling documents drop version numbers from filenames. Filed S159, sequenced behind the TS
  build; TS build isn't done until turn B and the tooling turn both close, so this stays behind them.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold - legality-critical claims go in
  `rules_assertions.py`.
- GW-derived material never enters the public repo. The faction pack PDFs, their converted `.md` files,
  and `Thousand_Sons_web.txt` are GW-derived - private sources repo only.
- Diagnoses from prior sessions are re-derived from source before building on them, not trusted - this
  caught real regressions three times now (S159's repo-push gap; S160's detachment-count regression;
  S161 found two unrelated stale hardcoded counts while touching adjacent code). Check existing scope
  docs (`THOUSAND_SONS_BUILD_SCOPE.md` etc.) too, not just raw source text.
- `DECISION_INDEX.md` was stale from D243 through D250 (last updated at S158) until S161 caught and
  fixed it. Worth a periodic glance at the tail of the index vs. the actual log to catch this early next
  time, rather than letting eight entries' worth of drift accumulate again.
