# 40K Army Builder — Faction Data Pipeline Process

**Version:** 0.6
**Scope:** How to produce and maintain a faction's data using the pipeline scripts. Written for Space Marines but applies to any faction.

---

## 1. What this pipeline is

Six scripts turn raw source data into the JSON files the app consumes.

- **`wahapedia_transform.py`** — reads the Wahapedia structured export and produces eight CSVs. Requires `--army-name "Faction Name"` for any non-Space-Marines faction (D48); without it, all units default to "Adeptus Astartes" and collide on merge.
- **`mfm_points_parser.py`** — reads the MFM text and produces Unit_Points, then patches Leader Eligible Units into Unit_Stats. Carries a `POINT_NAME_OVERRIDES` dict for name mismatches and Legends suppression — update it when adding a new faction.
- **`integrity_check.py`** — validates the nine CSVs and writes a report. Blocking issues must be resolved before converting. **Important:** "missing_rule" flags for Nurgle's Gift and Pact of Decay are false alarms — they resolve via the abilities lookup in-app and are not blocking.
- **`convert_to_json.py`** — produces `units.json` + four lookup JSONs from the nine CSVs.
- **`merge_factions.py`** — merges per-faction `units.json` outputs into the master file. Always re-merge after rebuilding any faction.
- **`loadout_parser.py`** — reads Datasheets_options.csv + pipeline units.json + composition/cost CSVs and writes `unit_loadouts.json`, preserving hand-authored entries. Run after `merge_factions.py` so the global weapon index covers all factions.
- **`equipped_parser.py`** — reads a pasted Wahapedia composition `.txt` and writes authoritative per-group `default_weapons`/`default_wargear`/`default_weapon_counts` into `unit_loadouts.json`, keyed to the shipped roster (drops non-roster datasheets, prunes orphans). Run after `loadout_parser.py`, once per faction (D49, D52).

The scripts produce a **mechanically complete first draft**, not finished data. Each writes a validation report listing what it could not resolve. **Those reports are your work queue.**

---

## 2. When to run — triggers

| Trigger | What to run | Why |
|---|---|---|
| Starting a new faction | Full sequence, in order | Full build from source |
| MFM points update | Re-pull changed armies' full pages, then re-run for those | D41: full-snapshot parse, no patcher |
| Wahapedia datasheet correction | Full sequence, in order | Re-patch points after |
| Adding a loadout definition by hand | Edit `unit_loadouts.json` directly; re-run `loadout_parser.py` with `--existing` pointing to the current file | Hand entries are preserved; parser fills the rest |
| Found a parsing bug | Fix script, then re-run | Never hand-edit around a systematic bug |

---

## 3. Setup (one-time per run)

1. Put all `.py` files in a working folder (typically `_work/`).
2. In the same folder, place: Wahapedia export CSVs, the faction's MFM text file, seed lookup CSVs from a finished faction (Keywords.csv, Rules.csv, Weapon_Abilities.csv).
3. Python 3 standard library only — no installs needed.

---

## 4. Run sequence (order matters)

```bash
# Step 1: Transform Wahapedia data (--army-name required for non-SM factions)
python wahapedia_transform.py --wahapedia-dir . --seed-dir . --out-dir out --faction SM --army-name "Adeptus Astartes"
python wahapedia_transform.py --wahapedia-dir . --seed-dir . --out-dir dg_out --faction DG --army-name "Death Guard"

# Step 2: Parse MFM points (patches Unit_Stats in place)
python mfm_points_parser.py --mfm MFM_Space_Marines_v1_0.txt --out-dir out --stats out/Unit_Stats.csv
python mfm_points_parser.py --mfm MFM_Death_Guard_v1_0.txt --out-dir dg_out --stats dg_out/Unit_Stats.csv

# Step 3: Integrity check (review reports before proceeding)
python integrity_check.py --dir out
python integrity_check.py --dir dg_out

# Step 4: Convert to JSON (per faction)
python convert_to_json.py --input-dir out --output-dir out --bundles bundled_swaps.json
python convert_to_json.py --input-dir dg_out --output-dir dg_json --bundles bundled_swaps.json

# Step 4b: Chaos Daemons — Gen-1 hand-built, converted DIRECTLY off the project root.
# Do NOT run wahapedia_transform.py --faction CD for this. That pulls the raw Wahapedia
# CD-faction dump (faction_id=CD in Datasheets.csv), which includes ~20 Chaos Space Marine /
# cultist units wrongly tagged CD via the Legiones Daemonica keyword, and its output would
# silently overwrite the real CD source below with the wrong roster (see D132).
# The nine CD source CSVs (Unit_Stats.csv, Unit_Points.csv, Unit_Wargear_Options.csv,
# Unit_Other_Options.csv, Unit_Weapons.csv, Unit_Abilities.csv, Keywords.csv, Rules.csv,
# Weapon_Abilities.csv) already live at the project root — they ARE convert_to_json.py's
# default input filenames.
python convert_to_json.py --input-dir . --output-dir dmn_out --bundles bundled_swaps.json

# Step 5: Merge all factions into master units.json
python merge_factions.py --in out --in dmn_out --in dg_json --taxonomy faction_taxonomy.json --out-dir deploy

# Step 6: Generate/update loadout definitions
python loadout_parser.py \
  --options Datasheets_options.csv \
  --units-dir deploy \
  --comp Datasheets_unit_composition.csv \
  --cost Datasheets_models_cost.csv \
  --datasheets Datasheets.csv \
  --factions SM DG \
  --existing unit_loadouts.json \
  --out unit_loadouts.json \
  --report parser_report.md

# Step 7: Recover per-model defaults from composition text (once per faction, same file in/out)
python equipped_parser.py --composition Space_Marines_web.txt --units deploy/units.json --loadouts unit_loadouts.json --out unit_loadouts.json --report sm_report.md
python equipped_parser.py --composition Death_Guard_web.txt   --units deploy/units.json --loadouts unit_loadouts.json --out unit_loadouts.json --report dg_report.md
# Targeted heterogeneous units in not-yet-onboarded factions (weapons only; factions still un-onboarded):
python equipped_parser.py --composition Black_Templars_web.txt --units deploy/units.json --loadouts unit_loadouts.json --out unit_loadouts.json --report bt_report.md
python equipped_parser.py --composition Dark_Angels_web.txt    --units deploy/units.json --loadouts unit_loadouts.json --out unit_loadouts.json --report da_report.md
python equipped_parser.py --composition Space_Wolves_web.txt   --units deploy/units.json --loadouts unit_loadouts.json --out unit_loadouts.json --report sw_report.md
```

Output after step 6: `deploy/units.json` (master), `unit_loadouts.json` (flat-pool defaults for SM+DG), `parser_report.md` (flag list).
Output after step 7: `unit_loadouts.json` with authoritative per-group `default_weapons`/`default_wargear`/`default_weapon_counts`, orphans pruned to the shipped roster (D49–D52). ~109 units (79 SM + 30 DG) corrected. `sm_report.md`/`dg_report.md` are disposable review artifacts (wargear-routed tokens, quantity>1 weapons, any unmatched/dropped).

---

## 5. Validate before you clean

Pick four units spanning the complexity range and check each end to end against the faction pack or New Recruit:
- A basic squad (e.g. Tactical Squad)
- A wargear-heavy elite (e.g. Bladeguard Veteran Squad)
- A vehicle (e.g. Land Raider)
- A character with leader attachment

If these four are correct, the pipeline logic is sound and the flagged items are just data entry. If one is wrong *systematically*, fix the **script** and re-run.

---

## 6. Work the queue — triage guide

**Integrity report (`integrity_report.md`):**
- `option_unresolved_ref` — weapon name in option text doesn't match any profiled weapon. Either a lowercase family name (fix in loadout definition) or a typo (fix in source or override).
- `points_no_stat` — MFM name doesn't match datasheet name. Add to `POINT_NAME_OVERRIDES` in `mfm_points_parser.py`.
- `missing_rule` — Nurgle's Gift and Pact of Decay flags are **false alarms**; they resolve via the abilities lookup in-app. Ignore them.

**Parser report (`parser_report.md`):**
- `UNMATCHED` — compound/multi-part sentence the parser can't handle. Either extend the parser or hand-author a definition for that unit.
- `REVIEW_MAX_TOTAL` — "any number of models" swap; needs `max_total` set manually in the definition.
- `WEAPON_NOT_FOUND` — weapon name not in any unit's pipeline output. Check for typos; may need a global-index entry or hand override.
- `COMP_PARSE_FAIL` — composition row didn't match expected pattern; hand-author the model_groups for that unit.

**Hand-authoring a loadout definition:** edit `unit_loadouts.json` directly with the unit_id as the key. Follow the schema in Data Dictionary Tab 10. Re-run `loadout_parser.py` with `--existing` pointing to your edited file — it will preserve the hand-authored entry and fill the rest.

---

## 7. Finalize

1. Deploy: `units.json`, `unit_loadouts.json`, `faction_taxonomy.json`, `abilities.json`, `rules.json`, `keywords.json`, `weapon_abilities.json`, `core_glossary.json`, `index.html` — all to GitHub Pages repo root.
2. Hard-refresh the browser (VERSION query string cache-busts on deploy).
3. Smoke-test: load faction, open several configured popups, confirm weapons link and counts are correct.
4. Record any data rules applied by hand in the Decision Log, so the next re-run follows the same rule.

---

## 8. Decisions still open / known gaps

- **Default_weapons per model group** — parser assigns all base weapons to all model groups. Wrong for units where model types have different starting weapons. Hand-author those definitions.
- **"Any number of models" max_total** — 14 definitions carry `max_total_all: true`; these need a numeric `max_total` set manually before the stepper works correctly.
- **Cross-faction sourcing** — units borrowed from other factions (Knights, GSC, Harlequins) don't yet appear. This is a planned feature, not a bug.
- **Comma parser** — `mfm_points_parser` still can't read thousands-separator points (`2,200 pts`). Titans and similar units remain un-costable until fixed.

---

## 9. Quick reference — common single commands

```bash
# Points refresh only (datasheets unchanged, new MFM) — per D41, re-pull changed armies only
python mfm_points_parser.py --mfm MFM_Death_Guard_v1_0.txt --out-dir dg_out --stats dg_out/Unit_Stats.csv
python convert_to_json.py --input-dir dg_out --output-dir dg_json --bundles bundled_swaps.json
python merge_factions.py --in out --in dmn_out --in dg_json --taxonomy faction_taxonomy.json --out-dir deploy

# Loadout update only (new hand-authored definitions added, re-run parser to fill rest)
python loadout_parser.py --options Datasheets_options.csv --units-dir deploy \
  --comp Datasheets_unit_composition.csv --cost Datasheets_models_cost.csv \
  --datasheets Datasheets.csv --factions SM DG \
  --existing unit_loadouts.json --out unit_loadouts.json --report parser_report.md
```

---

## Session 13 Addendum (July 2026) — Parser scope + matcher fixes

Two parser correctness fixes landed this session. Both are in the scripts (never hand-injected into output); the pipeline reproduces the prior file byte-for-byte except for the intended corrections.

**`loadout_parser.py` — `resolve_scope` (option scoping).** Replaced substring matching with word-scored matching: singular-normalise words (Veteran ↔ Veterans), prefer the closest group by word count, and break ties by leader/body preference (a body-model hint favours the fills-to-size group, a leader hint favours the fixed-1 group). Substring matching had scoped body options ("for every N models… 1 Veteran…") to the leader group because the leader's name *contains* the body-model name. Corrected 8 units; special weapons now scope to the body.

**`equipped_parser.py` — `match_group` (equipped-line ownership).** The "*X is equipped with:*" subject → model-group matcher tolerates the ways prose and stored group names drift apart, in one consolidated comparison: exact/plural, the group name **before its " - ROLE" suffix** (so "Ancient Gadriel" binds to "Ancient Gadriel - EPIC HERO"), a trailing **"model"/"models"** left after the determiner (so "Each Victrix Honour Guard model" binds to "Victrix Honour Guard"), trailing **footnote markers** on group names (so "Cenobyte Servitors\*" binds), and **irregular -ves plurals** (so "Hunting Wolf" binds to "Hunting Wolves"). A subject of "*every/all/each other model*" targets the **complement of named groups** — all groups no other line in that unit bound by name (D58). These enable heterogeneous named-model units (D57).

**Composition idioms currently parsed:** "*The X is equipped with:*", "*Every X is equipped with:*", "*Each X model is equipped with:*", "*Every other model is equipped with:*". Weapons carry an optional leading count ("1 master-crafted power weapon"); non-weapon tokens (banner, storm shield) route to `default_wargear`. **Latent trap:** if only some groups of a multi-group unit are bound, the unit is still marked `_defaults_source: "equipped"` while unbound groups keep stale flat weapons — verify every group bound after a paste.

**Onboarding a heterogeneous named-model unit (e.g. Wardens, Victrix):** paste the full Wahapedia datasheet composition prose (including the "UNIT COMPOSITION" block and the per-model "*X is equipped with:*" lines) into the faction `_web.txt`, then re-run `equipped_parser`. Verify the unit flips to `_defaults_source: "equipped"` with distinct per-group weapons; cross-check rollup counts against New Recruit.

**New work-queue signature:** for multi-model units, `_defaults_source != "equipped"` **and** identical `default_weapons` on every group = the unit never got per-model weapons (flat placeholder). Audit for this after any regenerate.


---

## Session 15 additions

**Loadout blast-radius reproduction harness (validated byte-perfect).** To isolate a `loadout_parser` change:
1. Extract the hand-authored entries (those with no `_parser_flags` — currently `000001157`, `000001044`) into `existing.json`.
2. `loadout_parser.py --options Datasheets_options.csv --units-dir . --comp Datasheets_unit_composition.csv --cost Datasheets_models_cost.csv --datasheets Datasheets.csv --factions SM DG --existing existing.json --out base.json`
3. Chain `equipped_parser.py` over the banked composition files in order: `Space_Marines_web.txt` (SM) → `Death_Guard_web.txt` (DG) → `Black_Templars_web.txt` (BT) → `Dark_Angels_web.txt` (DA) → `Space_Wolves_web.txt` (SW), each `--loadouts <prev out> --out <next>`.
4. Diff the final JSON against the committed `unit_loadouts.json`; an unmodified run reproduces it exactly (217 entries). All target units are faction code **SM** in `Datasheets.csv` (chapter distinctions are a later layer), so `--factions SM DG` covers every current unit.

**`clean()` now normalises the full Unicode dash family** to ASCII hyphen (U+2010–U+2015, notably the **non-breaking hyphen U+2011**). Range rows like "3‑10 Kill Team Infiltrators" were silently failing the count regex before this.

**Points source reminder.** Sizes/points come from the MFM `.txt` files via `mfm_points_parser`; `Unit_Points.csv` (53 rows) is stale — never regenerate points from the Excel-workbook CSVs.
