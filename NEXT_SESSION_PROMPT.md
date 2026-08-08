# NEXT SESSION PROMPT — Session 219

## Recommended turn type: data-only (World Eaters detachments)

Read `SESSION_HANDOFF_218.md` and `WORLD_EATERS_BUILD_SCOPE.md` first. S218 shipped World Eaters
units clean: 30 units, 30 loadout entries, all diff-guarded, full baseline green. This session is
`WORLD_EATERS_BUILD_SCOPE.md` §9 step 2.

Open with `./baseline.sh --fetch --data-turn`. Confirm clean before starting — should be fully
green except the pre-existing B108 finding (unchanged, Ryan's action).

## World Eaters detachments — the work

Per `WORLD_EATERS_BUILD_SCOPE.md` §4, build from `MFM_World_Eaters_v1.1.txt` (D293: always the
newest MFM). Register `WE` in `detachment_parser.py`'s three maps (`ARMY_TO_MFM`,
`MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`), mirroring the Emperor's Children pattern (D305) exactly.

Two things the scope doc already flagged as landing correctly on first build if sourced from v1.1:
- **Two force-disposition changes**, both carrying v1.1's own `UPDATED` banner: Brazen Engines
  (Purge the Foe → Disruption), Butchers of Khorne (Disruption → Take and Hold).
- **Two `UNIQUE TAG REMOVED` events**: Brazen Engines and Goretrack Onslaught previously shared a
  `UNIQUE: ONSLAUGHT` tag; v1.1 removes it from both. Confirm zero unique tags remain in the parsed
  output — the scope doc found zero by direct text search, not assumed.
- One enhancement re-price: Archslaughterer (Vessels of Wrath) 40 → 30 pts.
- No DP changes; 8 detachments in both MFM versions, same names.

Diff-guard `detachments.json` before banking: confirm exactly World Eaters' detachments added
(8, per the scope doc), 0 changed/removed elsewhere. Check `detachment_effects.json` directly for
whether any World Eaters detachment needs a construction-effect row (scan all 8 for an
allied-unlock or similar pattern, the way EC's Carnival of Excess was found at D305 — don't assume
none needed without checking).

**Once detachments ship clean:** flip `faction_taxonomy.json`'s World Eaters `built` flag to `true`
and set `data_army: "World Eaters"` — this is the point where both units and detachments are
complete and the faction becomes selectable (same sequencing as D298 Grey Knights, D305 Emperor's
Children).

## Also open, at your discretion

- **B112** — Chaos Daemons LORDS OF THE WARP disposition, now unblocked (a v1.1 CD MFM file exists
  in the private repo as of S217). Same-pattern data-only fix mirroring D306/D307. Not a World
  Eaters-session fit; its own turn.
- **B113** — detachment enhancement `LEADER:` eligibility restriction discarded as parser noise
  (4 instances across CSM/TS/EC today, 2 more once World Eaters' detachments ship this session —
  Cult of Blood's Butcher Lord, Khorne Daemonkin's Icon of War). Engine turn, small. Not urgent —
  pre-existing and unenforced on shipped factions already.

## Standing reminders

- Re-derive from source, don't trust prior-session prose.
- Turn typing: World Eaters detachments is data-only. If it surfaces an engine or tooling need,
  note it for a future typed session — don't fold it into this one.
- No decisions currently waiting on Ryan from S218.
- Seed files for diagnostic/dry-run work: if constructing an `--existing`/seed file by hand, copy
  only the true hand-authored keys, never the whole committed file — S218 lost time to exactly this
  mistake (see D312's "test-harness false alarm" note) before catching it via full byte-diff.

## Close

Produce the four documents, register `SESSION_HANDOFF_219.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
