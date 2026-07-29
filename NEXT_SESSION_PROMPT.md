# Next-session prompt — Session 159

D241/D242 closed (S158): Thousand Sons build scoped (`THOUSAND_SONS_BUILD_SCOPE.md` — 34
current-edition units, 9 detachments, fully self-sourced, one gap: no `Thousand_Sons_web.txt`
exists yet). Separately, the M2 dress rehearsal shipped clean: Ryan's private sources repo
(`rd-prime-1357/rd-prime-1357-data-sources`) and read-only token were verified live — a full
fetch/unpack/byte-compare of all 70 files against `source_manifest.json` passed, 0 missing/mismatched.
Found and fixed a real bug in the process: `baseline.sh`'s private-fetch URL was hardcoded to a
nonexistent repo name. `SOURCE_REPO_TOKEN.txt` was handed to Ryan to upload.

**Since then, outside this session:** Ryan worked through the 70-file GW-source deletion checklist by
hand in the project area (no sort/search tool there, so it was a manual one-by-one process). He
reports some `MFM_*.txt` files are still present afterward. The prior session's own mount view showed
*zero* `MFM_*.txt` files remaining — a direct conflict. Per standing practice, the mount is known to
go stale and not always reflect recent edits within a session, so neither view was trusted over the
other; Ryan and Claude agreed to reconcile in a fresh conversation instead of continuing to argue two
different pictures of the same area.

## This session's actual task: reconcile the file-area state — do this before anything else

Do not run `baseline.sh` or start any build work until this is done, since `baseline.sh`'s own
behavior (whether it can find sources locally or needs the token fetch path) depends on the answer.

1. **Ask Ryan for a current, complete screenshot (or screenshots) of the project file list.** The
   list may need to scroll or paginate to see everything — ask for enough screenshots to cover the
   whole list, not just the top.
2. **Cross-check every filename shown against the 70-item GW-source checklist** (the list is:
   `Abilities.csv`, `Army_Muster_Rules.txt`, `Black_Templars_web.txt`, `Chaos_Space_Marines_web.txt`,
   `Dark_Angels_Faction_Pack_June_2026.md`, `Dark_Angels_web.txt`, `Datasheets.csv`,
   `Datasheets_abilities.csv`, `Datasheets_keywords.csv`, `Datasheets_leader.csv`,
   `Datasheets_models.csv`, `Datasheets_models_cost.csv`, `Datasheets_options.csv`,
   `Datasheets_unit_composition.csv`, `Datasheets_wargear.csv`, `Death_Guard_web.txt`,
   `Detachment_abilities.csv`, `Detachments.csv`, `Enhancements.csv`, `Export_Data_Specs.csv`,
   `Factions.csv`, `Keywords.csv`, `Last_update.csv`, all 31 `MFM_*.txt` files (one per faction, plus
   `MFM_Instructions.txt`), `Rules.csv`, `Source.csv`, `Space_Marines_Faction_Pack_v1_0.md`,
   `Space_Marines_web.txt`, `Space_Wolves_web.txt`, `Stratagems.csv`, `Unit_Abilities.csv`,
   `Unit_Ability_Details.csv`, `Unit_Other_Options.csv`, `Unit_Points.csv`, `Unit_Stats.csv`,
   `Unit_Wargear_Options.csv`, `Unit_Weapons.csv`, `Weapon_Abilities.csv`, `chaos_daemons_reference.md`,
   `mfm_sm.txt` — cross-verify the exact count and names against a live clone of the public repo's
   `.gitignore` patterns rather than trusting this list from memory alone, since it's being retyped
   from a prior session's summary).
3. **Report exactly three things back to Ryan:** (a) which of the 70 are still present and need
   deleting, (b) confirm nothing outside that list was accidentally deleted (the permanent working
   set — `units.json`, `index.html`, `detachments.json`, all parsers/harnesses/JSONs, the decision
   log, the backlog, `pipeline_manifest.json`, etc. — should all still be there untouched), (c) whether
   `SOURCE_REPO_TOKEN.txt` made it into the area (check for its presence, never its contents, in any
   screenshot).
4. **Only after Ryan confirms the area matches expectations** (whether that means he deletes a few
   more files, or it turns out already correct and the earlier mount read was just stale) does this
   session move on to baseline and build work below.

## Baseline at open (once reconciliation above is done)

Full `baseline.sh --no-repo` should be clean (23/23). If the GW sources are no longer locally present
in the area (expected, post-M2), this is where the token-fetch path (fixed in S158) does its job —
confirm it actually engages and pulls sources rather than the session silently treating a data turn
as tier-A-only. If sources are loaded via fetch, tier-B should also pass: `repro_check.py`,
`units_repro_check.py`, `detachments_repro_check.py` all byte-identical. `rules_assertions.py` should
be 107/107 (up from 106/107 — B15-9 was fixed in S158). Any failure against repo-verified content is
real drift — reconcile before starting, the way S158 did for B15-9.

## After reconciliation and a clean baseline — Thousand Sons build, turn A (data-only)

Per `THOUSAND_SONS_BUILD_SCOPE.md` §8, run turn A: `wahapedia_transform.py --faction TS` →
`mfm_points_parser.py` against `MFM_Thousand_Sons_v1_0.txt` (self-sourced, no cross-file append step
needed — confirmed 34/34 in scoping) → convert → merge → post-processors. Add TS's config lines to
`units_repro_check.py` (new per-faction block, fifth `--in` to the merge call) and `repro_check.py`
(`FACTIONS`). Regenerate `units.json` (328 → 362), diff-trace every change, confirm 0 changed/removed
elsewhere. Bank before moving to turn C (detachments) — do not mix data turns with the tooling turn.

If the reconciliation step above turns out to need real cleanup work (re-deleting several files,
restoring something wrongly deleted), treat that as this session's whole turn and defer the TS build
to the session after — a clean reconciliation banked on its own beats a rushed one bleeding into a
data turn.

Turn B (loadout defaults) stays blocked until `Thousand_Sons_web.txt` arrives from Ryan; turns A and C
don't depend on it and can both ship first.

## After this session

- Thousand Sons turn C (detachment build) and the tooling turn (assertions, manifest) — per
  `THOUSAND_SONS_BUILD_SCOPE.md` §8.
- Thousand Sons turn B (loadout defaults) — blocked on Ryan sourcing `Thousand_Sons_web.txt`.
- Then Death Guard, Emperor's Children, World Eaters (remaining Chaos Marine variants), then Chaos
  Daemons, then Drukhari, per the standing faction priority order.
