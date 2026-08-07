# SESSION HANDOFF 210

**Turn type:** data-only (Emperor's Children units, D304). `units.json` + its four merged
lookups, `unit_loadouts.json`, `wargear_points.json`, `datasheet_wargear_abilities.json`,
and `rules_assertions.py` changed. `units_repro_check.py` and `repro_check.py` (the check
harnesses, not the data) also changed to register EC — same class of edit as every prior
faction's units turn. No engine file (`index.html`, `loadout_parser.py`,
`equipped_parser.py`, `mfm_points_parser.py`) touched.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: 33 gates, sources
   loaded, 121/121 assertions, both repro checks byte-identical. `repo_check` red on
   exactly the pre-existing B108 finding (`Thousand_Sons_web.txt` in the public repo),
   unchanged. Public repo confirmed current through S209 via direct clone, not the mount.

2. **Emperor's Children units built (D304).** `EC` registered in `units_repro_check.py`
   (mirrors the Grey Knights/Thousand Sons block) and `merge_factions.py`'s `--in` list.
   Real pipeline run end to end — not a dry run: `wahapedia_transform.py` →
   `mfm_points_parser.py` (`MFM_Emperors_Children_v1.1.txt`, D293) →
   `convert_to_json.py --emit-fourth-plus` → `merge_factions.py` → `add_loadout_groups.py`
   → `add_co_leader.py` → `add_bodyguard_stat_flags.py` → `add_chapter_point_overrides.py`.
   Diff-guarded at unit-id level against the previously committed `units.json`: **23 EC
   units added, 0 removed, 0 changed elsewhere.** `units_repro_check.py` passes
   byte-identical against the promoted file. Merged lookups diff-guarded the same way:
   `abilities.json` +26 (all EC-only), `weapon_abilities.json` +1 (Icon of Excess),
   `rules.json`/`keywords.json` unchanged. 18 army blocks / 410 total units.

3. **Real build needed far less manual authoring than S209's scope doc estimated —
   confirmed by direct demonstration, not by trusting the prior session's prose.** Of the
   "6 manual" wargear groups and 5 "ambiguous" weapon-name matches the transform-stage
   validation flagged, running the real `loadout_parser.py` (not the transform's own
   coarser check) resolved all of them cleanly via existing cross-faction precedent —
   bare weapon names (matching how every other faction already handles the same
   plasma-pistol/plasma-gun/heavy-missile-launcher ambiguity), and existing classifiers
   for Lord Kakophonist's compound swap, both Noise Marines swaps, Maulerfiend, Chaos
   Rhino, and the Chaos Terminators bundled swap (no `bundled_swaps.json` entry needed —
   `classify_n_model_swap` already handles the compound "X and Y replaced with Z" shape).
   EC's own Defiler (`000004208`, a separate datasheet ID from CSM's/DG's/TS's/WE's own
   Defilers) also parsed cleanly, matching its siblings' already-shipped shape exactly.

4. **Only Tormentors and Infractors needed genuine hand-authoring.** Both carry "1
   `<UnitName>` can be equipped with 1 icon of excess." — the generic word "model"
   replaced with the unit's own singular name, a shape none of `loadout_parser.py`'s 19
   `CLASSIFIERS` match (`classify_one_model_add` hard-codes the literal word "model").
   Checked the actual source text before copying the Icon of Despair precedent's
   structure: Icon of Despair's real MFM text carries a gating clause ("equipped with a
   boltgun... this model's boltgun cannot be replaced") that Icon of Excess's text does
   not have, so the two new entries use the plain `add` + `equipment` + `max_total: 1`
   shape only — no `requires_weapon`, no `blocks_swap`. Added to `repro_check.py`'s
   `HAND_AUTHORED` list; `EC` added to `FACTIONS`; no `WEB_PASSES` entry needed, confirmed
   by direct demonstration the same way Grey Knights didn't need one. Regenerated
   `unit_loadouts.json` via the real `loadout_parser.py` + `equipped_parser.py` chain:
   **21 auto-parsed EC units + 2 hand-authored added, 0 removed, 0 changed elsewhere.**
   `repro_check.py` passes byte-identical. The equipped-parser pass correctly enriched
   the two hand-authored entries' per-model-group `default_weapons` and added
   `_defaults_source: "equipped"`, exactly as designed — not a corruption.

5. **New structural assertion `EC-DATA`**, re-derived from source per the
   `B101-DATA`/`B106-DATA` pattern. Scoped to Emperor's Children specifically (not every
   currently-built faction): the same "N `<UnitName>` can be equipped with N `<item>`"
   sentence shape already exists, unfixed, on several other factions' datasheets
   (Infiltrator Squad's helix gauntlet, Rubric Marines' icon of flame ×2, Incursor
   Squad's haywire mine) as pre-existing `UNMATCHED` residuals — confirmed these are not
   new and are already tracked as backlog debt, not something this session touches.
   122 assertions now registered (was 121).

6. **`datasheet_wargear_abilities.json` regenerated** — a real gap, not previously
   flagged: 5 EC units (`000004079`, `000004080`, `000004095`, `000004097`, `000004098`)
   were missing. Diff-guarded: **5 added, 0 removed, 0 changed.**

7. **`B61-2`/`B61-3` extended for Emperor's Children's Legions of Excess carriers.**
   Confirmed against `units.json` directly: 5 units (Shalaxi Helbane, Daemonettes,
   Fiends, Keeper of Secrets, Seekers) carry `allied_group: "Legions of Excess"`, each
   with a distinct `local:chaos-daemons:*` id on the Chaos Daemons side — same shape as
   Death Guard's Plague Legions and Thousand Sons' Scintillating Legions.
   `ALLIED_CARRIER_GROUPS` extended with the one-line entry the existing comment
   anticipated; both assertions' docstrings updated to name the third carrier army.

8. **`E14-2`'s hardcoded count updated 90/61 → 98/67.** Verified by faction breakdown
   before updating the literal (not assumed): every non-EC faction's count is unchanged;
   EC contributes exactly 8 qualifying free-add options across 6 units — Tormentors' and
   Infractors' Icon of Excess, Chaos Land Raider's and Chaos Rhino's Havoc launcher, and
   Daemonettes' and Seekers' Instrument of Chaos + Daemonic Icon pair.

9. **A real, pre-existing parser gap found and NOT fixed this session (would mix engine
   work into a data-only turn) — opened as B111.** Sourcing EC's Defiler wargear from
   `MFM_Emperors_Children_v1.1.txt` (per the scope doc's expectation) returned zero
   items. Root cause: every v1.1 MFM file dropped the leading bullet character (`•`)
   from `WARGEAR OPTIONS` lines that v1_0 files have (confirmed directly against
   `MFM_Grey_Knights_v1.1.txt`, `MFM_Death_Guard_v1.1.txt`, `MFM_Thousand_Sons_v1.1.txt`,
   `MFM_Chaos_Space_Marines_v1.1.txt` — universal, not EC-specific).
   `mfm_points_parser.py`'s `WARGEAR_RE` regex hard-requires that bullet, so the
   `--wargear` pass has been silently blind to v1.1 pricing for every faction since the
   v1.1 migration. It only surfaces now because EC's Defiler is the first case where the
   v1_0 and v1.1 prices actually differ (10 vs 15 pts) — every other faction's wargear
   item happens to cost the same in both versions, so the stale v1_0 sourcing was
   accidentally still correct. **Shipped EC's Defiler wargear sourced from v1_0 (10 pts
   each item), consistent with its already-shipped siblings (DG/TS/CSM Defilers, all
   currently also stuck at v1_0 pricing for the same reason)** — diff-guarded: **1 unit
   added (`000004208`), 2 items, 0 removed, 0 changed elsewhere.** This is a known-stale
   price, not the v1.1-correct 15 pts; B111 tracks the regex fix.

10. **B110 correction — not executed, flagged for Ryan.** S209's B110 recommends
    flipping Grey Knights' `faction_taxonomy.json` flag to `built: true`. Checked
    `detachments.json` directly: Grey Knights has **zero** detachment entries there.
    `built: true` is exactly what makes a faction selectable in `index.html`
    (`opt.disabled = !f.built`) — flipping it now would let a player select Grey Knights
    and hit an empty detachment picker. Not executed. See "Decisions waiting on Ryan."

11. **Detachments not touched**, per this session's explicit scope (its own data turn
    next). `faction_taxonomy.json` not touched — Emperor's Children's flag stays
    `built: false` until both units and detachments ship, consistent with the B110
    finding above.

## State at close

- `units.json`, `abilities.json`, `weapon_abilities.json`: 23 EC units + merged lookup
  entries added, 0 changed/removed elsewhere. `units_repro_check.py` byte-identical.
- `unit_loadouts.json`: 23 EC entries added (21 auto-parsed, 2 hand-authored), 0
  changed/removed elsewhere. `repro_check.py` byte-identical.
- `wargear_points.json`: 1 unit added (EC Defiler, v1_0-sourced pending B111), 0
  changed/removed elsewhere.
- `datasheet_wargear_abilities.json`: 5 EC entries added, 0 changed/removed elsewhere.
- `rules_assertions.py`: `EC-DATA` added (122 total); `E14-2` count updated 90/61→98/67;
  `B61-2`/`B61-3` extended for Emperor's Children.
- `units_repro_check.py`, `repro_check.py`: EC registered (transform block; `FACTIONS`;
  `HAND_AUTHORED` +2).
- `bundled_swaps.json`, `faction_taxonomy.json`, `detachments.json`,
  `detachment_effects.json`, `detachment_parser.py`, `index.html`, `loadout_parser.py`,
  `equipped_parser.py`, `mfm_points_parser.py`: **untouched.**
- 121/122 assertions pass pre-manifest-write (P3 manifest staleness expected until
  `--write`); 122/122 expected after.
- Emperor's Children units are fully built and diff-guard clean. Detachments are the
  next data turn.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding,
   unchanged; ideally scrub git history).
2. Push this session's changed files to the public repo (listed below).

## Decisions waiting on Ryan

1. **B110 correction.** Grey Knights' `faction_taxonomy.json` flag is still `built:
   false`, and per this session's finding it should **stay** that way until Grey Knights
   has detachments — flipping it now would expose a faction with no detachment picker.
   Question: do you want Grey Knights' detachments prioritized ahead of Emperor's
   Children's (both are "next data turn" candidates now), or held until Emperor's
   Children's detachments ship first per the existing sequencing? Either is reversible
   and cheap to change; proceeding on Emperor's Children detachments first (matching the
   existing suggested sequencing) unless you say otherwise.
2. **B111 (new).** A dedicated engine/tooling turn is needed to fix
   `mfm_points_parser.py`'s `WARGEAR_RE` regex so it accepts v1.1's bullet-less
   `WARGEAR OPTIONS` format. Until fixed, every faction's wargear pricing (not just EC's
   Defiler) is sourced from v1_0 text, which happens to still be correct except for
   Defiler. No decision needed from you now — flagging for awareness; this will get
   sequenced as its own tooling turn.

## Files (SHA-256, first 12)

Verify these at S211 open.

| file | sha256:12 | note |
|------|-----------|------|
| `units.json` | `e9be5b2fdc24` | +23 EC units, 0 changed/removed elsewhere |
| `unit_loadouts.json` | `598e3cd5cc46` | +23 EC entries (21 auto + 2 hand-authored) |
| `abilities.json` | `ba50e7e9ec6f` | +26 EC-only entries |
| `weapon_abilities.json` | `1ad0aee35766` | +1 (Icon of Excess) |
| `wargear_points.json` | `2336d1073fea` | +1 unit (EC Defiler), v1_0-sourced, B111 |
| `datasheet_wargear_abilities.json` | `4eeaac7975a0` | +5 EC entries |
| `units_repro_check.py` | `952f71b4e46d` | EC block added |
| `repro_check.py` | `2ede120ab8bd` | EC in FACTIONS; +2 HAND_AUTHORED |
| `rules_assertions.py` | `0bced28d4c91` | EC-DATA added; E14-2 updated; B61-2/3 extended |
| `40K_Decision_Log.md` | (regenerated at close) | D304 full prose entry appended |
| `DECISION_INDEX.md` | (regenerated at close) | D304 entry |
| `OPEN_ITEMS_BACKLOG.md` | (regenerated at close) | B111 opened; B110 corrected, not closed |
| `pipeline_manifest.py` | (regenerated at close) | `SESSION_HANDOFF_210.md` appended to GUARDED |
| `pipeline_manifest.json` | (regenerated at close) | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | (unguarded) | S211 |
| `SESSION_HANDOFF_210.md` | (this file) | |

`index.html`, `bundled_swaps.json`, `faction_taxonomy.json`, `detachments.json`,
`detachment_effects.json`, `detachment_parser.py`, `loadout_parser.py`,
`equipped_parser.py`, `mfm_points_parser.py`, `source_manifest.json`, `baseline.sh`:
**untouched**, no entry needed.

## Backlog

23 open at S209 close; 24 open here (B111 opened, nothing closed; B110 corrected in
place, not closed). Beginning: B110, B109, B108, B99, B98, B97, B103, E28, B93, B90, B94,
B89, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (23). Resolved: none. Added:
B111. Ending: B111, B110, B109, B108, B99, B98, B97, B103, E28, B93, B90, B94, B89, B85,
B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (24).
