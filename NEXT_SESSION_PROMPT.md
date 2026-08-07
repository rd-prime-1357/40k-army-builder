# NEXT SESSION PROMPT — Session 206

## Recommended turn type: data-only (or data+tooling if B105 rides along).

Read `SESSION_HANDOFF_205.md` first, then this prompt. S205 shipped B104 — the
`equipped_parser.py` `scoped_name2id` fix (scope alias + parent-army fallback + propagation).
`unit_loadouts.json` was regenerated with the fixed parser (without GK), capturing 7 AA
improvements. `repro_check` passes byte-identical. GK is still NOT in `repro_check.py`'s
`FACTIONS` — that's this session's job.

## Primary task: B100 loadouts half (Grey Knights)

B104 is closed. The equipped_parser can now handle Grey Knights' shared vehicle names without
corrupting existing entries. The path forward:

1. **Decide whether to fold B105 in (XS).** B105 is the passive single-model swap classifier
   (`"1 Terminator can have its storm bolter replaced with 1 narthecium"`). Two GK units
   (Brotherhood Terminator Squad, Paladin Squad) need this. If folded in, it's a small
   `loadout_parser.py` change (new classifier function, ~10–15 lines) that ships on the same
   turn. If not, those two units remain `UNMATCHED` flagged and get authored by hand or in a
   separate tooling turn.

2. **B106 is NOT foldable.** The Dreadknight distinct-addition engine gap (a fixed-1-group pure
   addition with "up to N, cannot take duplicates") needs its own engine turn to add a new
   `loRollup` branch. Leave both Dreadknights' ranged-weapon options as `UNMATCHED` flags for now.

3. **Add `GK` to `repro_check.py`'s `FACTIONS` list** — this is the load-bearing step. Run the
   full regeneration. Diff-guard at key level: exactly the GK units should be added, and the 7 AA
   improvements from S205 should be unchanged (since the same fixed parser is running).

4. **Author the flagged units** — whichever ones are unblocked after the B105 decision. The four
   flagged units from S204's investigation:
   - Brotherhood Terminator Squad — narthecium swap (B105), banner option (already classified)
   - Paladin Squad — same narthecium swap (B105), same banner option
   - Nemesis Dreadknight — ranged-weapon "up to 2 distinct" (B106, blocked)
   - Dreadknight — same (B106, blocked)

5. **Regenerate `unit_loadouts.json` and diff-guard.** The regeneration now includes all existing
   factions PLUS Grey Knights. Confirm no regressions.

## Standing reminders
- `./baseline.sh --fetch --data-turn` to get GW sources loaded.
- `repro_check` should be **green** at open — S205 left it passing.
- All JS harness checks should pass.
- **Check sources directly, don't trust prior-session prose** — re-derive from
  `loadout_parser.py` and real data before authoring flagged units.

## After this session

Once B100's loadouts half ships: B106 needs its own engine-scoped session (read `loRollup`'s
`add`/`pool_id` mechanism and B101's `distinct` mechanism together before choosing a shape). Then
the Dreadknight options can be authored. After that, Grey Knights is fully built and the project
moves to the remaining Adeptus Astartes factions per the priority order.

## Close
Produce the four documents, register `SESSION_HANDOFF_206.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
