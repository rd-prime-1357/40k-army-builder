# 40K Army Builder — Architecture Overview

**Version:** 0.5
**Status:** Current-state reference. Read at session start.
**Scope:** What the system is, how data flows, and what the system of record is for each layer. For *how to run* the pipeline, see `40K_Data_Pipeline_Process`. For the *why* behind individual choices, see the Decision Log. This document sits above both.

---

## 0. Foundational rule

> **Canonical record: Decision Log D0.** This section operationalizes it; D0 is the authoritative statement. Keep the two in sync.

**The app treats as legal exactly what the rules allow and as illegal exactly what they forbid. Legality is the only boundary on validity.**

This governs the whole system. Enforcement is not restriction for its own sake, and permissiveness is not a feature — both are consequences of tracking the actual 11th-Edition Matched Play rules, no more and no less. Every specific design divergence from New Recruit (wargear/option enforcement, strict per-unit leader limits, size-first dropdowns, allied support) is an *instance* of this rule, not an independent principle; when they conflict in the abstract, resolve by asking only "is this legal under 11th-Edition Matched Play?"

**Legality boundary vs. UI mechanism are separate.** This rule defines *what the tool considers legal and flags as illegal* — it does **not** mandate how strictly the UI prevents an action. How the app responds to an illegal state is a distinct, already-made decision: flag-and-warn, not hard-block (D31/D32/D34). The tool still knows and signals every violation; it simply lets the user transiently build past it. "Enforce" means "know and surface what's legal," not "hard-block everything illegal."

**Undetermined-legality default:** where the rules are not yet published, lean **permissive** and revisit when they firm up.

---

## 1. One-paragraph summary

A browser-based Warhammer 40,000 11th-Edition Matched Play army-list builder, deployed as a single `index.html` on GitHub Pages. The app consumes a small set of JSON files produced by a Python pipeline. The pipeline derives each faction's data from three published sources (Wahapedia for structure, the Munitorum Field Manual for points, the faction pack for errata) plus two hand-authored layers: `bundled_swaps.json` for compound-weapon enforcement, and `unit_loadouts.json` for structured per-unit option definitions. The app's defining difference from New Recruit is that it enforces legal 11th-Edition Matched Play construction where NR is permissive.

---

## 2. Data flow

```
SOURCES (per faction)                SCRIPTS                         BUILD ARTIFACTS (app reads)
─────────────────────                ───────                         ───────────────────────────
Wahapedia export (all factions) ──►  wahapedia_transform.py    ──►  8 per-faction CSVs
  Datasheets.csv + siblings            (--faction <ID>                Unit_Stats, Unit_Weapons,
  filtered to one faction;              --army-name "<Name>")         Unit_Wargear_Options,
  Legends/Forge World excluded                                        Unit_Other_Options,
                                                                      Unit_Abilities, Rules,
MFM_<Faction>_v1_0.txt          ──►  mfm_points_parser.py     ──►   Keywords, Weapon_Abilities
  points authority                     (+ Unit_Stats)                 + Unit_Points.csv (3×3 matrix)

(all 9 CSVs)                    ──►  integrity_check.py         ──►  validation reports

9 CSVs + bundled_swaps.json     ──►  convert_to_json.py         ──►  units.json
                                                                      abilities.json
                                                                      rules.json
                                                                      keywords.json
                                                                      weapon_abilities.json

[per-faction outputs]           ──►  merge_factions.py          ──►  merged units.json
                                       (+ faction_taxonomy.json)      (all factions, one file)

units.json + Datasheets_options ──►  loadout_parser.py          ──►  unit_loadouts.json
  + comp/cost CSVs                    (preserves hand-authored         (keyed by unit_id;
  + existing unit_loadouts.json        entries)                         parser_report.md)

<Faction>_web.txt (pasted        ──►  equipped_parser.py         ──►  unit_loadouts.json
  Wahapedia composition)              (per-model defaults from          (per-group default_weapons/
  + units.json + unit_loadouts        "equipped with"; roster-scoped,   default_wargear/counts;
                                       prunes orphans)                  sm/dg_report.md)

faction_taxonomy.json (hand-authored) ─────────────────────────►    deployed as-is alongside JSON
core_glossary.json (hand-authored) ────────────────────────────►    deployed as-is alongside JSON
```

The faction pack (a **delta document**, not a full datasheet reference) supplies errata applied as recorded override entries during transform — not as hand-edits downstream.

---

## 3. System of record per layer

| Layer | Source of record | Regenerable? | Notes |
|---|---|---|---|
| Unit structure (stats, weapons, abilities, keywords) | Wahapedia export | Yes | Filtered per faction; Legends/FW excluded at transform (by design, temporary) |
| Points | `MFM_<Faction>_v1_0.txt` | Yes | Per-faction MFM text; one file per faction |
| Errata / changes | Faction pack (markdown) | Yes | Delta doc; applied as recorded, re-runnable overrides |
| Compound weapon enforcement | `bundled_swaps.json` | Yes (committed) | The part no GW source contains for bundled swaps |
| Structured option definitions | `unit_loadouts.json` | Yes (parser re-run preserves hand entries) | Parser-generated base + hand-authored overrides. The durable asset for wargear enforcement. |
| Per-model default weapons | `<Faction>_web.txt` (pasted Wahapedia composition) | Yes | Recovers "equipped with" attribution the CSV export drops (D49). Banked as source, edition-stable; Legends included but dropped until onboarded (D53). Feeds `default_weapons`/`default_wargear`/`default_weapon_counts`. |
| App data | The JSON files | No — build artifacts | Never hand-edit; regenerate from sources |

**Rule:** anything a published source provides flows through the pipeline from that source. Hand-authoring is reserved for the enforcement layer. Hand-injecting derived data into a build artifact is prohibited — it is lost on regeneration.

---

## 4. Excel: retired

Early releases maintained all unit data by hand in a single nine-tab Excel workbook. **This approach is retired.** The committed CSVs, JSON override files, and `unit_loadouts.json` are now the system of record for the hand-authored layer; published data comes from the pipeline sources above.

---

## 5. Multi-faction model (master, not per-faction-file)

The app loads **one** `units.json` containing every built faction as a top-level army block, and one merged set of the four lookup JSONs. The two-step selector (group → faction, driven by `faction_taxonomy.json`) switches factions by filtering blocks already in memory.

- **Generic faction** (e.g. Space Marines) resolves to its own army block, no filter.
- **Sub-faction** (e.g. a Space Marine chapter) resolves to the *union* of the generic codex block and the chapter block, with the chapter winning on `unit_name`.

**Merge step now automated** via `merge_factions.py`. Each converter run writes a `units.json` for its faction; `merge_factions.py` combines all faction outputs into the master file. Always re-merge after rebuilding any faction, then deploy the full JSON set together (units + 4 lookups + taxonomy + loadouts) — a partial deploy desyncs tooltips or rosters.

---

### 5.1 Forward scope: allies & agents

Allied units are **in scope** (agents likely too). The master-file model makes allies a filter over an existing block rather than a separate fetch. Saved list entries carry per-entry faction references (D43). Allied-construction *rule enforcement* waits on 11th-Edition rules solidifying.

---

## 6. Faction generations

- **Gen 1 (Daemons, releases 1–4):** hand-built in Excel. Its nine reference CSVs remain in the project and are currently the source of the deployed Daemons block. **Pending:** re-derive Gen-2 using `MFM_Chaos_Daemons_v1_0.txt`.
- **Gen 2 (Space Marines onward):** Wahapedia base + MFM parser + faction-pack errata + hand-authored enforcement layer. The current architecture.

**Built factions as of v5.22:** Space Marines (181 units), Chaos Daemons (53 units), Death Guard (36 units). 270 units total.

---

## 7. App (index.html)

Single self-contained file on GitHub Pages. Fetches `units.json` + four lookup JSONs + `faction_taxonomy.json` + `unit_loadouts.json` + `core_glossary.json` (all from repo root, cache-busted by `VERSION`). Current deployed version: **5.22**.

**Loadout system (D44–D46).** The app's wargear UI is driven by `unit_loadouts.json` where a definition exists. `loRollup()` computes exact weapon counts from composition × default weapons ± user-selected swaps/adds. The UI renders model-group sections with choice selectors, count steppers, count-with-choice steppers, and add-on toggles. The popup shows model make-up and live weapon counts (×N). Units without a definition fall back to the old flat wargear list.

**Construction model (D40).** Faction set at list creation. Autosave on every mutation. Home page (browse/create/open). Ghost rows for unresolved units on load.

---

## 8. Open data tasks

- **Default_weapons per model group** — parser assigns all base weapons to all model groups. Wrong for mixed units where different model types have different starting weapons. Needs per-group attribution; current workaround is hand-authored definitions for affected units.
- **Flagged loadout units (139)** — `_work/parser_report.md` is the work queue. Main types: UNMATCHED (compound sentences), REVIEW_MAX_TOTAL ("any number" swaps needing a max), WEAPON_NOT_FOUND (weapon not in any pipeline output).
- **Cross-faction sourcing** — Knights, GSC, Harlequins borrow units from other factions. Required before those factions can be fully onboarded.
- **Forge World / Legends inclusion** — committed, deferred. Toggle in `wahapedia_transform.py` still needed.
- **Daemons Gen-2 re-derive** — `MFM_Chaos_Daemons_v1_0.txt` exists; pending validation and cutover.
- **`mfm_sm.txt` may be slightly stale** (Repulsor Executioner cheaper in chapter files).

---

## 9. Canonical file / command reference

**Inputs:** Wahapedia export CSVs · `MFM_<Faction>_v1_0.txt` · faction-pack markdown · `bundled_swaps.json` · `faction_taxonomy.json` · `core_glossary.json`

**Scripts:** `wahapedia_transform.py` · `mfm_points_parser.py` · `integrity_check.py` · `convert_to_json.py` · `merge_factions.py` · `loadout_parser.py`

**Artifacts:** `units.json` · `abilities.json` · `rules.json` · `keywords.json` · `weapon_abilities.json` · `unit_loadouts.json` · `faction_taxonomy.json` · `core_glossary.json`

**`units.json` access pattern:** top-level is a list of `{army, units}` blocks. Resolve by `army` name, not positional index.

See `40K_Data_Pipeline_Process` for exact run commands and validation triage.

---

## Session 13 Addendum (July 2026) — Option surfaces

**Two option surfaces (Decision Log D56).** Unit options are presented on two distinct surfaces backed by different sources:
- **Left-panel unconfigured popup** — read-only survey of base equipment plus every option the unit could take. Sourced from the weapon profiles the datasheet references (informational).
- **Right-panel configure pane** — interactive build using the two-control model (steppers for count options, exclusive rows for single-model picks — D54). Sourced from the structured `options` in the loadout def.

Because the sources differ, a unit can look complete in the popup while its configure-pane options are incomplete; a display gap on one surface is not a data gap on the other.

**Configure pane layout:** the leader/champion model's options render as their own visually separated block (D55), identified as the first `model_group` with `count.fixed == 1`.


---

## Session 15 clarifications

**System of record for sizes/points.** The deployed `units.json` carries a per-unit **`points`** object (`points.sizes` + points matrix) built by `mfm_points_parser` from the MFM `.txt` files, run as part of the Claude-run pipeline and committed to the repo. The Excel-workbook path (`Unit_*.csv` → `convert_to_json`) is **retired/vestigial** and is not the source of truth — do not regenerate points from it. Repo: `github.com/rd-prime-1357/40k-army-builder`, branch `main`, files at root; the app is a single `index.html` fetching `units.json`, `unit_loadouts.json`, and the reference JSONs.

**Two-stage units.json.** `wahapedia_transform` emits the structural `units.json` (weapons, model_groups, wargear — no points); `loadout_parser`/`equipped_parser` consume that for weapons/composition; the MFM-points step then enriches the same file with the `points` object. A points-less `units.json` snapshot is a *pre-enrichment* stage, not a corrupted file.

**Configure-pane scope.** The pane renders **option controls and the size selector only** — it does **not** render a model-group composition breakdown. Units with no options (per-bracket units) therefore render near-empty; and the size selector is driven by `unit.points.sizes`, so a points-less unit shows nothing. Composition rendering is a pending feature.
