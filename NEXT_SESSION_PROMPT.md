# NEXT SESSION PROMPT — Session 216

## Recommended turn type: data-only (B111 data turn — MANDATORY FIRST)

Read `SESSION_HANDOFF_215.md` first. S215 shipped B111's tooling half
(`mfm_points_parser.py` `WARGEAR_RE`, D309) and **deliberately left the baseline with one known-red
gate**: assertion **E14-1** fails (`wargear_points.json does not rebuild from the MFM — it is
stale`). This is not drift and not a gate to work around — it is the tracked, expected consequence of
the parser now being correct while the data has not yet caught up. **Clearing it is this session's
job. Do it before anything else.**

Open with `./baseline.sh --fetch --data-turn` (sources required — this is a data turn). Expect E14-1
red at open; every other gate green (except `repo_check`, B108, Ryan action). Do not start other
work while E14-1 is red.

## B111 data turn — the work

Re-run the wargear pass and regenerate `wargear_points.json`:
`python3 mfm_points_parser.py --wargear MFM_*.txt --units units.json --loadouts unit_loadouts.json
--datasheets Datasheets.csv --wargear-out wargear_points.json` (confirm the exact flag shape against
`main()` before running).

**Diff-guard hard.** The only price changes that should appear:
- Heavy reaper autocannon **10 → 15 pts** and Hades lascannon **10 → 15 pts** on the four Defiler
  factions (Chaos Space Marines, Thousand Sons, Death Guard, Emperor's Children).
- Space Marines' Victrix Honour Guard **Banner of Macragge 10 → 15 pts**.

Anything else changing is a surprise — stop and investigate before banking. Nothing should be
removed. After regeneration, `rules_assertions.py` E14-1 must go green and the three repro rebuilds
must still be byte-identical. Check `datasheet_wargear_abilities.json` and any per-unit point totals
that reference these items are unaffected (they price the item per-instance at build time, so the
unit base points in `units.json` should not move — confirm).

## Also open, at your discretion (only after E14-1 is green)

- **World Eaters** — scoping pass (next faction in priority order; Heretic Astartes CSM/TS/DG/EC all
  built). `CSM_BUILD_SCOPE.md` / `EMPEROR_S_CHILDREN_BUILD_SCOPE.md` pattern. Scoping-only, no
  committed pipeline file touched — so it cannot share a session with the B111 data turn. Its own
  session.
- **B110** — Grey Knights `faction_taxonomy.json` `built: false` until it has detachments
  (`detachments.json` has zero GK entries). No change since S211.
- **B112** — Chaos Daemons LORDS OF THE WARP disposition unverified against v1.1; blocked until GW
  publishes a v1.1 CD detachment file. Just check whether one exists yet.

## Standing reminders

- Re-derive from source, don't trust prior-session prose. S215 caught the B111-not-splittable finding
  exactly this way — the S215 prompt's own tooling/data split was wrong.
- Turn typing: the B111 data turn is data-only. World Eaters scoping is scoping-only. Do not combine.
- One open decision waits on Ryan (reversible, non-blocking): whether B111 should have been one
  combined turn instead of the split-with-known-red that shipped. See S215 handoff. Proceed on the
  data turn regardless.

## Close

Produce the four documents, register `SESSION_HANDOFF_216.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
