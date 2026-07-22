# 40K Army Builder — Functional Specification
**Version 0.7 — Draft**
**Last Updated: June 2026**

---

## 1. Purpose and Scope

**Governing rule (see Decision Log D0):** The app treats as legal exactly what the 11th Edition Matched Play rules allow and as illegal exactly what they forbid — legality is the only boundary on validity. Enforcement means knowing and surfacing every violation; how strictly the UI blocks an action is a separate mechanism choice (flag-and-warn, not hard-block — see §6.4).

This tool is designed solely to create army lists for Warhammer 40,000 11th Edition Matched Play. It does not teach players how to play the game, provide tactical advice, or serve any purpose beyond full army list creation and output.

The tool displays rules text (ability descriptions, unit special rules, keyword definitions) as reference information to support list building decisions only.

### 1.1 Supported Game Format
- Matched Play only (11th Edition rules)
- Combat Patrol, Crusade, and other formats are explicitly out of scope

### 1.2 Points Limit Support
- User-selectable via banner dropdown: 1,000 / 2,000 / 3,000 points
- Defaults to 2,000 points (standard Matched Play)
- Points limit stored as a live variable — changing it updates error states immediately
- Assumption (unconfirmed): only the cap changes across points levels, not construction rules

---

## 2. UI Layout

The app uses a three-panel layout beneath a fixed top banner.

### 2.1 Top Banner (fixed, full width)
Left to right:
- **Product name:** "40K ARMY BUILDER" in red
- **ARMY:** displays the current list's faction (gold value), positioned at the left edge of the center panel (25%). Faction is set when the list is created (Model 2, D40); it is a list property, not a live "switch my army" control — changing the active army means opening or creating a different list.
- **ARMY POINTS:** dropdown (1,000 / 2,000 / 3,000, gold value), right-aligned with the right edge of the center panel (70%)
- **LIST POINTS:** running points total of the current list (gold value, turns red when over army points cap), far right

### 2.2 Three Panels
Each panel has a fixed sub-header (always visible, does not scroll) and a scrollable body below.

| Panel | Width | Sub-header | Body |
|---|---|---|---|
| Left (Roster) | 25% | "Available Units" | Scrollable unit roster grouped by type |
| Middle (Army List) | 45% | "Army List · N units" | Scrollable army list grouped by type |
| Right (Unit Options) | 30% | "Unit Options · [unit name] · N of N" | Scrollable unit configuration |

### 2.3 Color System
- **Red:** Error and warning states only (never used for section labels or decorative UI)
- **Gold (#cc9900):** Points values, selected options, banner values
- **Grey (#666):** Section type labels, banner labels, secondary text
- **Amber:** Roster card when unit is at or over instance limit (warning, not error)

---

## 3. Army Construction Flow

### 3.1 Interaction Model (Immediate-Add, Live-Edit)
1. User clicks a unit card in the roster (left panel) — unit is immediately added to the army list with default selections and opened in the right panel
2. User configures the unit in the right panel — all changes take effect immediately on the list entry
3. User clicks any list entry in the middle panel — opens that entry in the right panel for editing
4. No "Add to Army" button — no staging or commit step
5. The active list **autosaves on every mutation** (D40); there is no manual Save step and no anonymous in-progress list to lose

### 3.2 Construction Steps
1. **Open or create a list** — from the home/landing page (browse saved / create new / open existing). Creating a list opens a modal that sets **name + faction** (Model 2, D40). Faction is a property of the list set at creation; there is no faction-switch on an open list. Starting over is an explicit "New List" action (with an unsaved-changes confirm), not a side effect of the faction control.
2. **Select Army Points** — via banner dropdown (1,000 / 2,000 / 3,000)
3. **Select Detachment(s)** — future release
4. **Select Units** — immediate-add from roster, configure in right panel
   - 4a. Unit size (number of models)
   - 4b. Daemonic Allegiance (for applicable units)
   - 4c. Equipment (weapon substitutions)
   - 4d. Other options (icons, instruments, etc.)
   - 4e. Leader assignment
   - 4f. Allied units — added via a separate "add ally" path, each carrying its own per-entry faction reference (capability now, allied-construction enforcement later)
5. **Select Enhancements** — future release
6. **Assign Warlord** — future release

---

## 4. Army Selection

- An army always belongs to a single faction
- Allies permitted where specified by army rules (predefined units from other factions, max 3)
- Additional units may be conditionally unlocked by detachment selection
- Current implementation: Chaos Daemons only; additional factions added via ARMY dropdown

---

## 5. Detachment Selection (future release)

- 11th Edition: each detachment costs 1–3 detachment points; 2,000 point game provides 3 detachment points
- Player may take 1–3 detachments depending on costs
- Detachments are faction-constrained
- Each detachment provides: rules, optional enhancements, and potentially conditional unit unlocks
- Some detachments elevate non-Battleline units to Battleline status, affecting count caps
- config.json has all 9 Chaos Daemons detachments complete and validated

---

## 6. Unit Selection

### 6.1 Unit Types (display order)
Epic Hero, Character, Battleline, Infantry, Mounted, Beast, Monster, Vehicle, Dedicated Transport, Fortification, Allied

### 6.2 Unit Instance Limits

| Unit Type | Maximum | Notes |
|---|---|---|
| Epic Hero | 1 | One of each named character maximum |
| Battleline | 6 | Some detachments may elevate other types to Battleline |
| Dedicated Transport | 6 | |
| All others | 3 | Per-unit overrides stored in data for exceptions |

Limits are informational — exceeding them shows visual error flags but does not block adding units. This supports list exploration and construction workflows.

### 6.3 Unit Options (right panel)

**Daemonic Allegiance** (Soul Grinder, Daemon Prince of Chaos, Daemon Prince of Chaos with Wings):
- Four god choices: Khorne, Tzeentch, Nurgle, Slaanesh
- Must be chosen before list is considered complete (shown as error flag if missing)
- God selection determines conditional weapons (Soul Grinder) and stat modifiers (Daemon Princes — not yet enforced)
- Copy-tier pricing counts all god variants of a unit together

**Unit Size:**
- Selectable from valid size brackets defined per unit
- Points update immediately on selection
- Copy-tier pricing: 1st unit uses first_unit price, 2nd unit uses second_unit price, 3rd+ uses third_plus price
- Pricing recalculates across all list entries when any entry is added, removed, or resized

**Wargear Options (weapon substitutions):**
- Grouped choices (mutually exclusive within group) render as radio-style selectors
- Independent swaps render as checkboxes
- No points cost for any Chaos Daemons wargear options currently

**Other Options (icons, instruments, non-weapon upgrades):**
- Render as independent checkboxes
- Icon and Instrument of Chaos are independent — a unit can have both (on different models)
- Carrier notes displayed as subtext

### 6.4 Error States

A list entry shows a red "!" flag when:
- Required selection is missing (Daemonic Allegiance not chosen)
- Unit count exceeds instance limit

The detail panel shows descriptive warning text for each error condition. The roster card turns amber when a unit is at or over its instance limit.

---

## 7. Leader Assignment

- Leader assignment is optional
- Eligibility rules defined on the leader unit's datasheet (leader_eligible_units field)
- Standard rule: one leader per bodyguard unit
- Co-leader exception: a second leader may join if that leader's co_leader_eligible_with field lists the already-assigned leader (or vice versa). Many armies have co-leader cases — the code checks this field rather than hardcoding a flat limit of 1.
- Assignment UI: dropdown in the right panel detail view showing eligible bodyguard units currently in the list
- Army list display: attached leader appears above its bodyguard with bodyguard name in parentheses — "Bloodmaster (Bloodletters)". Bodyguard block gets a subtle amber left border.
- Removing a bodyguard automatically detaches any leaders attached to it
- Leader assignment does not affect points cost (confirmed)

---

## 8. Unit Detail Modal (next major feature)

Clicking a unit name in the roster or army list opens a modal popup showing full unit details.

**Two modes:**
- **Roster click (full view):** All model groups with stat lines (M/T/SV/INV/FNP/W/LD/OC), all weapon profiles (ranged and melee), all abilities, rules, keywords. Optional weapons marked as such.
- **List entry click (configured view):** Selected weapons shown normally; non-selected weapons greyed (not hidden — context is useful). Current selections reflected. This is the foundation for print output.

The configured view is mandatory — it is the precursor to print output and must be built correctly.

---

## 9. Enhancements (future release)

- Optional additions purchasable for eligible units, costing points
- Each detachment defines its own enhancement set
- Maximum 4 enhancement purchases per army
- Upgrade enhancements: apply to up to 3 units at per-unit cost, count as 1 purchase
- Standard enhancements: Characters only, count as 1 purchase each
- TBD: Confirm duplicate enhancement rules; confirm Epic Hero eligibility

---

## 10. Warlord Selection (future release)

- Must be a Character or Epic Hero
- Some Epic Heroes require mandatory warlord designation if included
- Some Epic Heroes restrict which other characters may be included

---

## 11. Output

- **Unit detail modal:** On-screen display of full unit stats and configured loadout (next release)
- **Print:** Rendered in designed format, sent to browser print. Modeled on NR unit card layout: stats, weapon tables, abilities, rules, keywords per unit. Configured view (selected options only shown prominently).
- **Export/share:** JSON export/import of saved lists (D38) — the portability and sharing path. See §11.1.

### 11.1 List Management (D38–D40)

- **Home / landing page** — the app's front door: browse saved lists (grouped by primary faction, with name / points / last-modified), create a new list, or open an existing one. The builder is entered *from* here.
- **Storage** — saved lists persist in browser localStorage behind a swappable async store; cloud sync is a future drop-in. JSON export/import provides backup, portability, and sharing (export on one device, import on another).
- **Reference model** — a saved list stores unit references (`unit_id`) and selections, not frozen points. On load it re-resolves, re-prices, and re-validates against current data, so a list always reflects current points and legality.
- **Flag-don't-drop** — a unit that no longer resolves (removed/renamed without id) renders as a flagged ghost row carrying its saved name/points; it is never silently deleted. A unit that resolves but is now illegal (e.g. lost leader eligibility, new limit) renders as a normal entry with an error flag (same surface as §6.4).
- **Schema version** — every saved list is stamped for forward migration.

---

## 12. Open Questions / TBD

- Confirm whether any construction rules (beyond points cap) change at different points levels
- Confirm maximum enhancements per army (believed to be 4)
- Confirm whether duplicate enhancements are permitted
- Confirm enhancement eligibility for Epic Heroes
- Confirm Dedicated Transport and Fortification special construction rules if any
- Confirm Allied Units: formal GW unit type designation or organizational category?
- Daemon Prince stat modifiers for god selection not yet enforced (Khorne +2S hellforged, Tzeentch +3A infernal cannon, Nurgle +1T, Slaanesh +2"M) — implement when stat display added
- Define initial faction list beyond Chaos Daemons

*Resolved this session (now in Decision Log):* list construction model (Model 2, D40), storage/saved-list model (D38/D39), clear-on-faction-switch (retired, replaced by explicit "New List").

---

## 13. Unit Options Panel — Loadout System (implemented v5.18–v5.22)

The right panel ("Unit Options") renders differently depending on whether the unit has a structured loadout definition in `unit_loadouts.json`.

### 13.1 Units with a loadout definition

Options are rendered in model-group sections, each labeled with the group name in gold (e.g. "INTERCESSOR SERGEANT", "PLAGUE MARINE"). Within each section:

- **Choice swap** (`choice` type): radio-style list. One row per option including "Keep [weapon]" as the default. Selected row highlighted in gold. Only one choice active at a time per option.
- **Count swap** (`count` type): +/− stepper with current value, label, and "(max N)" where N is computed from the unit's current size. Separate steppers for each count option in the same group share one header.
- **Count-with-choice** (`count` type with `replacement_choices`): one stepper per replacement weapon, all under a shared group header showing the combined max.
- **Add-on** (`add` type, `max_total: 1`): single radio-style toggle. Add-ons that scale with size use a stepper.
- **Pool status line** (body groups with count swaps only): "Special weapons: X of Y models" shown between the scope label and the first option. Turns red when X > Y (over-allocation flagged, not blocked — D34).

One category header is shown per unique `group` value within a scope; options sharing a group value are listed together under a single header.

### 13.2 Units without a loadout definition

Existing wargear option UI (flat list of wargear rows, no model-group grouping). This path is now rare for SM and DG; it remains for any future faction before its parser run.

### 13.3 Weapon counts in the configured popup

When a unit has a loadout definition and the popup is opened in configured mode:
- **Model make-up** line: "Group Name ×N, Group Name ×N" (above the weapon tables).
- **Weapon tables** (Ranged / Melee / Other wargear): generated from the rollup result, not the flat weapon list. Each row shows the weapon name followed by "×N" in gold. Only weapons with a count > 0 are shown. Profile-suffixed weapons (e.g. "Plasma pistol – standard", "Plasma pistol – supercharge") both receive the count of their base-name match in the rollup.
- **Per-model defaults are authoritative (D49):** a group's `default_weapons` now come from the datasheet "equipped with" wording via `equipped_parser.py`, so mixed-model units (command squads, bikes + attack bike, etc.) show each model's correct weapons rather than a shared flat pool. Vehicles that mount multiples of a weapon carry a `default_weapon_counts` map so the rollup shows the true quantity — a Land Raider shows 2× Godhammer lascannon, a Whirlwind 4× Twin heavy bolter (D51).
- **Other wargear section**: shown when `add` options produce equipment (e.g. "Icon of despair ×1"). Note: per-model non-weapon defaults captured in `default_wargear` (Astartes shield, jump packs) are stored but not yet rendered here (D50).
- **Over-allocation warning**: shown if `overAllocated` is true from the rollup.

### 13.4 Weapon count rollup logic (D45)

`loRollup(def, size, selections)` computes:
1. Model counts per group from `size_brackets` + `model_groups` (fixed counts sum first; fills-to-size group gets the remainder).
2. For single-model groups (fixed: 1): apply choice swaps directly. Replaced weapon removed, chosen weapon added. Each default weapon is added ×(its `default_weapon_counts` value, default 1), so multi-mount vehicles show correct quantities (D51).
3. For body groups: process add-ons first (add weapons, reserve pool slots if `blocks_swap`). Then process count swaps against the pool (remaining models). Total swapped across all count options is capped at pool size; over-pool is flagged.
4. Output: `{weapons: Map<name, count>, equipment: Map<name, count>, overAllocated: bool, pools: {groupName: {pool, used}}}`.

All wargear is free in 10th/11th edition; the rollup does not affect points. Points come from size only.

---

## 14. Configured Popup (implemented)

Opens on "Configure" button click on any list entry, or on any unit row's eye icon. Shows the unit in its configured state, not its default state.

### 14.1 Sections (in order)

1. **Stat block** — full stat line (M/T/SV/INV/FNP/W/LD/OC).
2. **Model make-up** (loadout units only) — "Group ×N, Group ×N".
3. **Ranged Weapons table** — active weapons only, with ×N counts for loadout units.
4. **Melee Weapons table** — active weapons only, with ×N counts for loadout units.
5. **Other wargear** (loadout units with add-on equipment only).
6. **Abilities bar** — collapsed by default; shows ability names. Expands to show descriptions from abilities lookup.
7. **Rules bar** — collapsed by default; shows rule names + weapon ability names from active weapons. Expands to show descriptions. Weapon abilities resolved via `glossaryDesc()` which checks rulesLookup → abilitiesLookup → weaponAbilitiesLookup → coreGlossaryLookup (exact) → coreGlossaryLookup (base name).
8. **Keywords bar** — collapsed by default; shows keyword tags.

### 14.2 Description resolution (glossaryDesc)

Priority chain for any rule/ability name:
1. `rulesLookup` (faction rules from pipeline)
2. `abilitiesLookup` (unit abilities from pipeline)
3. `weaponAbilitiesLookup` (weapon abilities from pipeline)
4. `coreGlossaryLookup[name]` (exact match in core_glossary.json)
5. `coreGlossaryLookup[baseAbilityName(name)]` (base-name match, strips parameter)

`baseAbilityName()` strips trailing parameters: "Rapid Fire 1" → "Rapid Fire", "Anti-Vehicle 4+" → "Anti", "Feel No Pain 5+" → "Feel No Pain", "Scouts 8\"" → "Scouts".

---

## Session 13 Addendum (July 2026) — Option surfaces and configure-pane controls

**Two option surfaces (Decision Log D56).**
- *Unconfigured popup (left panel):* read-only survey — base equipment plus every option the unit could take. For browsing "what can this unit be."
- *Configure pane (right panel):* interactive build — "what am I actually choosing."

**Configure-pane controls — two-control model (D54):**
- *Count options* (size-scaled: "for every N models…", "any number of…") render as a **count stepper**.
- *Single-model exclusive choices* (a champion's "replace weapon with one of…") render as an **exclusive choice row** (select one, the rest clear). A stepper is not used here because it cannot enforce "pick exactly one," which would permit an illegal loadout.

**Configure-pane layout:**
- The leader/champion model's options render in their own **visually separated block** (D55), identified as the first model group with a fixed count of 1.
- Within a block, distinct option groups are separated by a **divider line**.
- Colour discipline holds: red = error only, gold = unsaved only; the separators use neutral gray.


---

## Session 15 additions

**Size-varying units (D62).** A unit with two alternative legal builds ("OR" composition) is presented via the size selector: choosing a size shows that bracket's exact composition. Counts that differ by bracket are fixed and non-editable at each size; a stepper appears only where the count is the player's choice.

**Optional groups & compound choices.** Optional model groups (composition `0-N`) become include/exclude controls (toggle at max 1). A weapon-swap choice may be **compound** ("Weapon A + Weapon B") — one pick granting two weapons (D63). All *legal* options are shown regardless of competitiveness (D0); the tool guides via defaults, never by removing legal choices.

**Un-onboarded units (D61).** Units without points data are shown with an "unverified" badge and, in the configure pane, an explicit "not yet onboarded — points and options pending" empty-state rather than a blank panel. The badge is derived from points-presence and clears automatically as units are onboarded.
