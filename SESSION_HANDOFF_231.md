# SESSION HANDOFF 231

**Turn type:** pipeline/data (B114 build, per NEXT_SESSION_PROMPT.md's recommendation).
B114 shipped and closed. See D325.

## What happened

1. **Open.** `./baseline.sh --fetch --data-turn` — 34/34 gates green. Verified S230's Files
   table hashes against `pipeline_manifest.json`: all four matched.

2. **Re-derived the 21-unit Shadow Legion Thralls set independently**, matching S229/S230
   exactly (14 named datasheets + 7 already-shipped "Damned"-keyword datasheets, all
   CD-faction, `source_id 000000012`, none yet in `units.json`).

3. **Found a correction to S230's reasoning, D131/D132-grounded.** S230 assumed the CD-faction
   datasheet rows were real GW book-variant reprints, the same shape as Rotigus's
   Death-Guard-allied entry (which explicitly names "Plague Legions" in its own ability text,
   unlike its native Chaos Daemons entry). Checked directly: CD-tagged Chaos Lord (`000004036`)
   and CSM's native Chaos Lord (`000000929`) carry byte-identical ability text, stats, and
   wargear. These are Wahapedia mistag duplicates — the exact case D131/D132 already
   documented and the reason `40K_Data_Pipeline_Process.md` Step 4b forbids running
   `wahapedia_transform.py --faction CD` at all. This did not change the recommended build:
   `index.html`'s `resolveUnits`/`setFaction` resolve a faction's roster strictly by `army`
   block, so the 21 units still had to physically exist in the Chaos Daemons block for the
   app to ever offer them there, regardless of whether the source text is flavored or a
   duplicate.

4. **Found neither Chaos Daemons' nor Chaos Space Marines' own MFM file prints a Shadow
   Legion points table** — checked both directly, a real structural difference from the other
   three allied-group precedents (Death Guard's MFM does print a "PLAGUE LEGIONS" units-price
   section; Chaos Daemons' does not print an equivalent "SHADOW LEGION" one — "SHADOW LEGION"
   only appears there as a detachment-DP/enhancements entry). The ability text only caps a
   points pool, so the 21 units correctly price off their Chaos Space Marines native points —
   confirmed unit-by-unit against CSM's shipped roster, not assumed, and pinned as an
   executable cross-check (E21a-7) rather than left as prose.

5. **Built via the real scoped pipeline, not a hand-edit.** Ran `wahapedia_transform.py`
   against `--faction CD`, filtered its output down to exactly the 21 target datasheet IDs
   (discarding the other 53 real-native and remaining mistag rows), hand-built a
   `Unit_Points.csv` fragment sourced directly from CSM's already-shipped, verified prices
   (not retyped from memory), and ran `convert_to_json.py` on the scoped set — clean, zero
   warnings, all 21 points matched.

6. **Made Chaos Daemons stay a genuine reproducible fixed point.** Chaos Daemons is Gen-1
   hand-curated data, converted directly from CSV files sitting at the project root
   (`units_repro_check.py` step 5) — never routed through `wahapedia_transform.py` for its
   real build (D132). A first attempt to splice the 21 units directly into `units.json` broke
   `units_repro_check`/`repro_check`. Fixed properly: appended the 21 units into the actual
   root CSVs (`Unit_Stats.csv`, `Unit_Points.csv`, `Unit_Wargear_Options.csv`,
   `Unit_Other_Options.csv`, `Unit_Weapons.csv`, `Unit_Ability_Details.csv`), adding a
   `Datasheet ID` column and an `Allied_Group` column to the two files whose older schema
   lacked them (needed so `convert_to_json.py` assigns the units their real Wahapedia ids
   instead of falling back to synthesized `local:` slugs, and so the allied_group tag survives
   a from-source rebuild). Also found the full canonical reproduction recipe includes four
   post-processing scripts (`add_loadout_groups.py`, `add_co_leader.py`,
   `add_bodyguard_stat_flags.py`, `add_chapter_point_overrides.py`) that a first, narrower
   convert-only test had skipped — re-ran the complete `units_repro_check.py` recipe and
   adopted its output as the new `units.json`, confirmed byte-identical to the prior committed
   file everywhere except the 21 new entries.

7. **`repro_check.py`'s FACTIONS list gained `CD`** (same precedent as each prior faction
   addition) so the 21 units' loadout defaults regenerate from source via the existing
   B68/B104 cross-army-block propagation mechanism — confirmed the mechanism correctly
   routes `Chaos_Space_Marines_web.txt`'s composition data to both the CSM native units and
   their new Chaos-Daemons-block duplicates, not assumed. Re-ran the full canonical
   loadout+equipped-parser sequence (all 8 factions, all 7 web passes) and confirmed
   byte-identical reproduction of all 411 prior entries plus the 21 new ones.

8. **`detachment_effects.json` retargeted.** Shadow Legion's `unlock` effect moved from the
   dead `{"keyword": "HERETIC ASTARTES"}, enforced: false` stub to
   `{"allied_group": "Shadow Legion Thralls"}, enforced: true`. Verified zero engine change
   needed — `unlockedAlliedGroups`/`alliedPointsCap`/`canAddUnitToList` are fully generic on
   `allied_group`, already exercised by four other detachments. Did not touch `index.html`,
   including a now-stale comment at ~line 2593-2596 referencing the old unenforced Shadow
   Legion case — left for a future engine-adjacent turn to keep this turn strictly data-only.

9. **Full assertion suite reconciled, 125/125 pass, plus all JS harnesses green.**
   - `E21a-4`: updated the hardcoded unenforced-inventory list and prose (Shadow Legion
     dropped off it).
   - New `E21a-7`: pins the 21-unit census against both `units.json` and CSM's native roster
     (unit_ids and points, cross-checked, not assumed).
   - `E4B_KEYWORD_GAPS` extended by 3 entries: Dark Apostle/Dark Commune/Traitor Enforcer
     duplicate an already-documented, already-shipped Character-keyword gap onto their new
     Chaos Daemons copies (checked against CSM's identical native gap first).
   - `ALLIED_CARRIER_GROUPS` gained a Chaos Daemons entry; added a `NATIVE_ARMY_OVERRIDES`
     map since Shadow Legion Thralls is the first allied-carrier group where Chaos Daemons is
     the carrier rather than the donor — `b61_cd_native_copies_distinct` needed an actual code
     fix (not just a data addition) to check Chaos Space Marines as the donor army instead of
     its hardcoded Chaos Daemons default.
   - `E14-2`'s seeded-add literal moved 109/76 → 113/80, verified by full per-army breakdown
     (exactly +4 options across +4 units, all Shadow Legion Thralls carriers of the same
     Chaos Icon/Chaos Familiar free-add shape already seeded on their CSM counterparts; every
     other army's count unchanged) before updating.
   - `e21c_check.js` S4 rewritten: the prior assertion tested Shadow Legion's dead
     `enforced:false` stub as a convenient real-data example of "nothing unlocks" — replaced
     with a genuine positive test of the now-live unlock (offer-without / offer-with /
     refusal-reason), mirroring Plague Legions' own S4 coverage instead of losing it.
   - `datasheet_wargear_abilities.json` regenerated via `ds_wargear_abilities_parser.py`:
     +5 entries, purely additive, zero existing entries changed.

10. **Diff-guarded throughout.** Every regenerated output was confirmed additive-only against
    its prior committed state before being adopted — `units.json` (21 new Chaos Daemons-block
    entries, zero removals, zero other fields touched anywhere else in the file),
    `unit_loadouts.json` (21 new entries, zero changes to the existing 411),
    `datasheet_wargear_abilities.json` (5 new entries, zero changes to the existing 70).

11. **Close.** Full baseline re-run: all 33 substantive gates pass. `pipeline_manifest.py`
    registered `SESSION_HANDOFF_231.md` in GUARDED before `--write`.

## Shipped / changed

- `units.json`: Chaos Daemons block 53 → 74 units. 21 new entries tagged
  `allied_group: "Shadow Legion Thralls"`, real Wahapedia CD-faction unit_ids, priced
  identically to their Chaos Space Marines native counterparts.
- `unit_loadouts.json`: 21 new entries (per-model equipped defaults propagated from
  `Chaos_Space_Marines_web.txt` via the existing cross-army-block mechanism). Zero changes to
  the prior 411 entries.
- `detachment_effects.json`: Shadow Legion's unlock effect retargeted to the allied_group
  mechanism, `enforced: true`.
- `Unit_Stats.csv`, `Unit_Points.csv`, `Unit_Wargear_Options.csv`, `Unit_Other_Options.csv`,
  `Unit_Weapons.csv`, `Unit_Ability_Details.csv` (project-root Gen-1 Chaos Daemons source
  CSVs): 21 new unit rows appended. `Unit_Stats.csv` gained a `Datasheet ID` column
  (populated for the 21 new rows, blank for the existing 54); `Unit_Points.csv` gained an
  `Allied_Group` column (populated for the 21 new rows, blank for the existing 53).
- `datasheet_wargear_abilities.json`: +5 entries, regenerated via
  `ds_wargear_abilities_parser.py`.
- `repro_check.py`: `CD` added to the `FACTIONS` list, with an explanatory comment matching
  the pattern of each prior faction addition.
- `rules_assertions.py`: `E21a-4` inventory/prose updated; new `E21a-7` assertion + its
  `b114_shadow_legion_census` function added; `E4B_KEYWORD_GAPS` extended by 3 entries;
  `ALLIED_CARRIER_GROUPS` gained a Chaos Daemons entry and a new `NATIVE_ARMY_OVERRIDES` map;
  `b61_cd_native_copies_distinct` fixed to honor the override; `B61-1`/`B61-2`/`B61-3`
  registration prose updated (also corrected pre-existing staleness: World Eaters was already
  missing from B61-1/B61-2's prose before this session); `e14_count`'s literal and comment
  updated.
- `e21c_check.js`: Section 4's dead synthetic assertion replaced with live coverage of
  Shadow Legion's now-real unlock behavior.
- `DECISION_INDEX.md`: D325 appended.
- `OPEN_ITEMS_BACKLOG.md`: B114 moved from Open Items to Closed / Shipped with a summary
  pointer; header count 22 → 21.
- `pipeline_manifest.py`: `SESSION_HANDOFF_231.md` appended to GUARDED (before `--write`).
  `pipeline_manifest.json`: regenerated by `--write` at close.
- `index.html`, `wargear_points.json`, `bundled_swaps.json`: untouched this session (no
  costed wargear options among the 21 new units, so `wargear_points.json` needed no change;
  no new bundled swaps).

### Net New Files

None. Every changed file already existed and played this same role before this session.

## Ryan action required

1. **B108** — remove `Thousand_Sons_web.txt` from the public repo (still outstanding,
   unchanged).
2. Push this session's file set once uploaded.

## Decisions waiting on Ryan

- **B116** — unchanged (Drukhari Harlequins/Anhrathe cross-book allied inclusion; see
  `DRUKHARI_BUILD_SCOPE.md` §6). Own follow-on ticket once Ryan decides; blocks nothing
  shipped.
- **Next faction after Drukhari** — unchanged; priority order fully built, none queued.

## Files (SHA-256, first 12)

Verify these at S232 open.

| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | `ff15575b716b` | 21 new Chaos Daemons-block entries |
| `unit_loadouts.json` | `cc17e8cb60dd` | 21 new entries |
| `detachment_effects.json` | `9d74757684c6` | Shadow Legion unlock retargeted |
| `datasheet_wargear_abilities.json` | `a67326c10030` | +5 entries |
| `repro_check.py` | `27c41e00f879` | CD added to FACTIONS |
| `rules_assertions.py` | `9cf82b34b474` | E21a-4/E21a-7/E4B_KEYWORD_GAPS/ALLIED_CARRIER_GROUPS/B61-1..3/E14-2 |
| `e21c_check.js` | `682fc4f9fda3` | S4 rewritten onto live Shadow Legion behavior |
| `Unit_Stats.csv` | `efb28511498c` | +21 unit rows; new Datasheet ID column |
| `Unit_Points.csv` | `54249500496b` | +21 rows; new Allied_Group column |
| `Unit_Wargear_Options.csv` | `a43bccdcaf83` | +21 units' wargear option rows |
| `Unit_Other_Options.csv` | `6a163e6a3993` | +21 units' other-option rows |
| `Unit_Weapons.csv` | `4ad08a0cc207` | +21 units' weapon rows |
| `Unit_Ability_Details.csv` | `78d7fa534000` | +21 units' ability detail rows |
| `DECISION_INDEX.md` | `d3c5de570cfb` | D325 appended |
| `OPEN_ITEMS_BACKLOG.md` | `dd8b1a875b06` | B114 closed; count 22 → 21 |
| `pipeline_manifest.py` | `46b104778181` | SESSION_HANDOFF_231.md appended to GUARDED |
| `NEXT_SESSION_PROMPT.md` | not guarded | informational only, never guarded — S232 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `SESSION_HANDOFF_231.md` | (this file) | hash not self-referential; checked by `--freshness-check` |

## Backlog

22 open at S230 close; **21 open at S231 close** (B114 closed; nothing else closed, nothing
opened).

Beginning: B116, B114, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75,
P2, P4, E23, B67b, E12, B17 (22).
Resolved: B114 (1).
Added: none (0).
Ending: B116, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4,
E23, B67b, E12, B17 (21).
