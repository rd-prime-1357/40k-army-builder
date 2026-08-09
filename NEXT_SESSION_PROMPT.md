# NEXT SESSION PROMPT — Session 225

## Recommended turn type: tooling-only (Drukhari loadouts — author the 13 flagged wargear-option
groups)

Read `SESSION_HANDOFF_224.md` first, then `DRUKHARI_BUILD_SCOPE.md` §7 (still the authoritative
scoping writeup for this turn — nothing in it changed at S224 except that the 23-unit `units.json`
now exists to author against). Drukhari's units are shipped (D318); this turn does not touch
`units.json`, `wahapedia_transform.py`, or `mfm_points_parser.py` at all.

Open with `./baseline.sh --fetch --data-turn`. Confirm clean before starting. If it fails,
reconcile before starting work — do not carry a failing gate forward in prose.

## The build

1. Run `loadout_parser.py --factions DRU` (or the project's equivalent flagging pass) against the
   now-shipped Drukhari roster and confirm the flagged-unit set matches §7's count before authoring
   anything: 9 units needing manual construction, 13 wargear-option groups, 8 compound
   replacements, 1 bundled two-weapon swap, 4 ambiguous weapon-name matches, 1 equip/add item with
   no weapon profile (Voidraven missiles), 1 multi-model-line split (Incubi). Re-derive this count
   from source — don't trust §7's numbers unchecked, per standing discipline.
2. Author the 13 wargear-option groups directly into `unit_loadouts.json`'s HAND_AUTHORED set
   (same pattern as World Eaters' Jakhals/Helbrute — see `repro_check.py`), covering: Wracks (2
   groups), Hand of the Archon (2 groups), Hellions (2 groups), Talos (2 groups), Razorwing
   Jetfighter, Voidraven Bomber, Scourges with Heavy Weapons, Ravager, Scourges with
   Shardcarbines (1 group each).
3. Resolve the 4 ambiguous weapon-name matches with an explicit pick each: Incubi (demiklaives,
   single vs. dual blade), Wracks ×2 (tools vs. twin tools), Voidraven Bomber (missile variant).
   These are rules-legality/product calls on which reading is correct where the source name is
   genuinely ambiguous — if the correct pick isn't resolvable from `Datasheets.csv` or the MFM
   text alone, batch it as a decision for Ryan rather than guessing silently.
4. Diff-guard `unit_loadouts.json` against committed, field-by-field, via `repro_check.py` — "ran
   clean" is not sufficient.
5. Once loadouts land, rerun `mfm_points_parser.py --wargear` (or the project's `build_wargear_points`
   path) and confirm `wargear_points.json` now DOES pick up Drukhari's 4 wargear items (Ravager's
   Dark lance +5, Scourges with Heavy Weapons' Haywire blaster +5/Dark lance +5, Talos's Twin
   haywire blaster +5) — these were correctly withheld at S224 specifically because the loadout
   groups didn't exist yet; confirm they populate now that they do, don't just assume.
6. Detachments (`DRUKHARI_BUILD_SCOPE.md` §5, 9 detachments) and the deferred
   `detachment_parser.py` three-map registration (see D318 — registering early breaks
   `detachments_repro_check` since Drukhari's `detachments.json` doesn't exist until that turn) are
   NOT this turn's scope. They ship together, in the data turn immediately after this one, per
   §8's sequencing. Keep this turn to loadouts only, per the never-mix rule.

## Also open, at your discretion

- **B113** — detachment enhancement `LEADER:` eligibility restriction discarded as parser noise (6
  instances across CSM/TS/EC/World Eaters; GK, CD, and Drukhari all confirmed to add 0 more).
  Engine turn, small, not urgent. Different turn type — do not fold in.
- **B114** — Chaos Daemons' `Shadow Legion` HERETIC ASTARTES unlock (`detachment_effects.json`) is
  recorded `enforced: false` on a now-stale premise. Needs its own scoping pass. Different turn
  type — do not fold in.
- **GK §6 / §7** — carried unchanged for several sessions now; still not investigated.
- **Repo push (Ryan's action)** — `OUTPUT_FORMAT_SPEC_for_project_instructions.md` and
  `Thousand_Sons_web.txt` (B108) both still outstanding. `pipeline_manifest.json` still outstanding
  from S223. This session adds S224's changed files to the same pending push (see
  `SESSION_HANDOFF_224.md`'s Ryan-action section) — `repo_check.py` will show `DIFFERS` findings
  until pushed; expected, not a new problem.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's own numbers.
- Turn typing: this is a tooling turn. Loadout authoring only. Detachments and the deferred map
  registration are a separate, later data turn per `DRUKHARI_BUILD_SCOPE.md` §8's sequencing.

## Decisions waiting on Ryan

**B116** — unchanged. Whether/when to build Drukhari's Harlequins/Anhrathe cross-book
allied-inclusion mechanic (see `DRUKHARI_BUILD_SCOPE.md` §6). Recommendation is still to defer past
the initial Drukhari build. Does not block this session.

## Close

Produce the four documents, register `SESSION_HANDOFF_225.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
