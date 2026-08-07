# NEXT SESSION PROMPT — Session 207

## Recommended turn type: engine-only (B106), unless Ryan's Thousand_Sons_web.txt action is still
## pending, in which case a data-turn open will fail the source-fetch gate — see below.

Read `SESSION_HANDOFF_206.md` first, then this prompt. S206 shipped B105 and B107 (both closed),
added `GK` to `repro_check.py`'s `FACTIONS`, and regenerated both `unit_loadouts.json` and
`wargear_points.json` — 25 and 4 GK units added respectively, 0 changed elsewhere in either. Grey
Knights is substantially complete: the only thing left blocking it is **B106**.

## Before starting: confirm the Ryan action from S206 landed

S206 found `Thousand_Sons_web.txt` missing from the private source repo's `source_manifest.json` —
it has only ever lived in the project mount. If Ryan has pushed it and regenerated
`source_manifest.json`, a `--fetch --data-turn` open will pick it up cleanly. If not, the data-turn
source-fetch gate will fail exactly the way it did at S206 open — pull the file from the project area
again as a stopgap and flag it again; do not treat a second occurrence as a new problem needing
separate diagnosis.

## Primary task: B106 — Dreadknights' distinct-addition engine gap

Both Dreadknights (`000000389` Nemesis Dreadknight, `000001360` Grand Master in Nemesis Dreadknight)
carry "This model can be equipped with up to two of the following, but cannot take duplicates: 1
gatling psilencer / 1 heavy incinerator / 1 heavy psycannon[/1 sublimator]" — a pure addition (no
`replaces`) on a fixed-1 model group. This is currently the **only** residual `_parser_flags` entry
anywhere in Grey Knights, confirmed at S206 close.

Per B106's backlog entry: `loRollup`'s fixed-1-group branch requires a real `o.replaces` matching
something the model carries before it emits anything, so a `count` option with no `replaces` is
silently skipped. The `add` type does support fixed-1 groups and `pool_id`-shared caps, but the
pool-cap mechanism computes the cap as the **largest single member's** `max_total`, not a sum — three
`add` options each capped at 1 would produce a pool cap of 1, not 2. `b101_check.js`'s own fixtures
confirm the shipped, tested `distinct` shape is exclusively the swap case.

This needs a genuine engine-scoped session: read `loRollup`'s `add`/`pool_id` mechanism and B101's
`distinct` mechanism together before choosing a shape, rather than forcing either existing path to fit.
Both Dreadknights currently ship with **no ranged-weapon options at all** — their primary loadout
customization — so this is functionally more significant than a typical residual flag.

## After B106 ships

1. Author both Dreadknights' ranged-weapon options (parser + regeneration, diff-guarded).
2. Grey Knights will then be fully built. Move to the next Adeptus Astartes faction per the priority
   order (check `40K_Decision_Log.md`'s most recent faction-priority note for which one, since the
   standing priority order in project instructions lists the full sequence but doesn't track which
   are already built).

## Standing reminders
- `./baseline.sh --fetch --data-turn` at open (see the Thousand_Sons_web.txt caveat above).
- All 30 gates should be green at S206 close — confirm they still are before starting new work.
- Re-derive from source, don't trust prior-session prose — S206 itself found the backlog's own B105
  entry wrong (claimed the banner option needed no code change; it did — see B107).

## Close
Produce the four documents, register `SESSION_HANDOFF_207.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
