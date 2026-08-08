# NEXT SESSION PROMPT — Session 223

## Recommended turn type: tooling-only (B115 — fix `wahapedia_transform.py`'s Drukhari
faction-selection bug)

Read `SESSION_HANDOFF_222.md` first, then `DRUKHARI_BUILD_SCOPE.md`. S222 scoped Drukhari and found
two things: a real transform bug (B115) and a genuinely new allied-inclusion mechanic with no
built-faction precedent (B116, deferred, awaiting Ryan's call — see "Decisions waiting on Ryan"
below, not blocking this session).

Open with `./baseline.sh --fetch --data-turn`. Confirm clean before starting.

## B115 — the fix

`wahapedia_transform.py --faction DRU` currently selects 37 datasheets against Drukhari's real
23-unit roster. The extra 14 are Harlequins/Aeldari-Corsair units carrying a legacy `faction_id ==
DRU` tag but real `source_id == 000000186` (the Aeldari Faction Pack, current-edition, not
Legends). `select_datasheets`'s existing filter (`source_is_excluded`) only checks
edition/legend-status, not whether the source belongs to the target faction's own pack.

Re-verify this from source before touching code — don't trust S222's numbers without re-running
the dry pass yourself, per standing discipline. Fix `select_datasheets` (or `source_is_excluded`)
so a source outside the target faction's own current Faction Pack is excluded — either a targeted
exclusion of Aeldari's `source_id`, or (preferred if it's a clean generalization) a check that the
source's own name/id maps back to the faction being built. Re-run the dry pass and confirm exactly
23 datasheets select for `--faction DRU`, matching `MFM_Drukhari_v1.1.txt`'s 23-unit list.

Check whether this same gap could affect any other already-built faction sharing a Wahapedia
faction_id with a different current-edition pack (`DRUKHARI_BUILD_SCOPE.md` found no such case in
the 16 already-built factions, but re-confirm rather than trust the prior session's negative
finding, since B115 itself is proof a negative finding can be wrong until actually run per faction).

This is a tooling turn — fix and re-verify only; do not build the Drukhari units data this session
per the standing turn-typing rule. If B115 turns out deeper than a filter fix (e.g. if the general
check breaks an already-built faction), stop and report rather than pushing through.

## Also open, at your discretion

- **Drukhari units data turn** — once B115 is fixed and verified, this is the natural next session:
  run the corrected transform, register Drukhari in `detachment_parser.py`'s three maps, build
  `units.json` for the 23-unit roster. `DRUKHARI_BUILD_SCOPE.md` §§1, 3, 4 have the full source
  read already done.
- **B113** — detachment enhancement `LEADER:` eligibility restriction discarded as parser noise (6
  instances: CSM ×2, TS ×1, EC ×1, World Eaters ×2; Grey Knights, Chaos Daemons, and now Drukhari
  all confirmed to add 0 more). Engine turn, small. Not urgent.
- **B114** — Chaos Daemons' `Shadow Legion` HERETIC ASTARTES unlock (`detachment_effects.json`) is
  recorded `enforced: false` on a stale premise. Needs its own scoping pass.
- **GK §6 / GK §7** — carried unchanged from S222's prompt; still not investigated.
- **Repo push** — `OUTPUT_FORMAT_SPEC_for_project_instructions.md` and `Thousand_Sons_web.txt`
  (B108) both still outstanding, Ryan's action.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including B115's own diagnosis above.
  S220–S222 have all found inherited assumptions wrong on re-check.
- Turn typing: this is a tooling turn. Fix and verify B115 only — the units/detachments build is
  its own, later, data-typed session.

## Decisions waiting on Ryan

**B116** — whether/when to build Drukhari's Harlequins/Anhrathe cross-book allied-inclusion
mechanic (points-capped inclusion of units priced from the unbuilt Aeldari faction). Recommendation
in `DRUKHARI_BUILD_SCOPE.md` §6 is to defer it and ship Drukhari's own roster/detachments first.
Does not block B115 or the Drukhari units build — only relevant once/if Aeldari itself is
prioritized.

## Close

Produce the four documents, register `SESSION_HANDOFF_223.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
