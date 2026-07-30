# Next-session prompt — Session 161

**Assigned: Thousand Sons turn A (units), data-only.** Turn C shipped S160 (D248) — TS now has 9
detachments in `detachments.json`, and the Changehost of Deceit allied unlock exists (enforced:false).
Turn A's gate (E24) is unblocked: the detachment to hang the unlock on now exists.

## Open at session start

Read `SESSION_HANDOFF_160.md` first, then D248/D249 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority.

Run the full baseline before any new work: `./baseline.sh --fetch --data-turn`. It closed **24/24**,
109/109 assertions, at the end of S160.

**Ryan cannot download from the project Files panel.** Any file needed in the repo that lives only in
the project area must be re-delivered by Claude. Build this into close.

## Turn A scope

1. Run the TS block through the pipeline: transform -> mfm-points -> convert -> merge (a per-faction
   block in `units_repro_check.py`, ~26 lines mirroring Death Guard's, verified working dry-run in S159 -
   34 units, 328 -> 362, `abilities.json` +43, `weapon_abilities.json` +2 Brayhorn/Herd Banner). Bank it
   this time; S159 ran it clean but deliberately did not bank because turn C hadn't shipped yet.
2. Extend the B61 census assertions to the six TS allied carriers (Kairos Fateweaver, Lord of Change,
   Flamers, Screamers, Pink Horrors, Blue Horrors) - `b61_plague_legions_census` and its three siblings
   are currently Death-Guard-specific; generalise them to cover both armies' carrier sets, or add TS-
   specific siblings mirroring the four B61-1..4 assertions. Confirm points stay TS-priced, not CD-priced
   (D245's correction: Pink Horrors 115 TS vs 150 CD, Blue Horrors 90 vs 125 - do not source from the CD
   pool).
3. Flip `detachment_effects.json`'s `Thousand Sons|CHANGEHOST OF DECEIT` unlock and warlord-ban entries
   from `enforced: false` to `enforced: true` once the six carriers exist with `allied_group:
   "Scintillating Legions"` set. Verify against `e21a_allied_targets` (E21a-4) - its expected-unenforced
   list will need the two Changehost of Deceit keys removed once this flips.
4. Ship the two Battleline rows B78 has been waiting on: `Thousand Sons|SERVANTS OF CHANGE` and
   `Thousand Sons|WARPMELD PACT`, both granting Tzaangor units BATTLELINE (mirroring the four existing
   `battleline`-kind rows, D204 ruling 2). Once these land, remove `rules_assertions.py`'s `e21a_coverage`
   `known_gap` allowlist (currently tracking exactly these two keys) - its self-check will fail loudly if
   you add a row without also updating the allowlist, so update both in the same edit.
5. Verify `units_repro_check.py` reproduces byte-identical; run the full assertion suite; confirm TS-1/
   TS-2 (detachment count/coverage, S160) still pass unaffected.

## Read before touching the allied units (carried forward from S159/S160, still true)

- **`allied_group` is deliberate and must be retained.** B61 shipped it (S133, D208); four assertions
  (B61-1..4) pin its census. Do not reduce it to a provenance field.
- **The six are not duplicates of Chaos Daemons entries.** Different `unit_id`s, different points (see
  above). Never source TS allied points from the CD pool.
- **`SCINTILLATING LEGIONS` is a keyword, not a detachment** (still true after D248's 9-detachment
  correction - neither of the two newly-added detachments is named Scintillating Legions either).

## Then, in later sessions

- **Turn B** (loadout defaults) - `Thousand_Sons_web.txt` exists now, so `repro_check.py` gains
  `Thousand_Sons` in `WEB_PASSES` and `TS` in `FACTIONS`. Both change `unit_loadouts.json`, so this is
  its own turn, after turn A.
- **B77** - emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, never hand-edit output).
  Untouched this session; still open.
- **B75** - Rules Updates column resolution (pages 1/9 of the TS pack, and Death Guard's equivalent).
  Awaiting Ryan's flag counts across the pack set to size it. Untouched this session; still open.
- **B76** - rolling documents drop version numbers from filenames. Filed S159, sequenced behind the TS
  build; TS build isn't done until turn B closes, so this stays behind it.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold - legality-critical claims go in
  `rules_assertions.py`.
- GW-derived material never enters the public repo. The faction pack PDFs, their converted `.md` files,
  and `Thousand_Sons_web.txt` are GW-derived - private sources repo only.
- Diagnoses from prior sessions are re-derived from source before building on them, not trusted - this
  caught a real regression twice now (S159's repo-push gap; S160's detachment-count regression). Check
  existing scope docs (`THOUSAND_SONS_BUILD_SCOPE.md` etc.) too, not just raw source text - D241 already
  had the right detachment count and a session skipped checking it.
