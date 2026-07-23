# 40K Army Builder — Decision Log
**Version 3.0 — July 2026**

This document records key product and architectural decisions, with rationale, so that context is not lost between working sessions.

---

## D0 — Foundational Rule: Legality Is the Only Boundary
**Decision:** The app treats as legal exactly what the rules allow and as illegal exactly what they forbid. Legality is the only boundary on validity. Every divergence from New Recruit and every enforcement decision below is an *instance* of this rule, not an independent principle; resolve abstract conflicts by asking only "is this legal under 11th Edition Matched Play?"

**Boundary vs. mechanism (critical):** This rule defines *what the tool considers legal and flags as illegal*. It does NOT mandate how strictly the UI prevents an action. How the app responds to an illegal state is a separate decision — flag-and-warn, not hard-block (D31, D32, D34). The tool still knows and signals every violation, so the legality boundary is intact; it simply lets the user transiently build past it. "Enforce" means "know and surface what's legal," not "hard-block everything illegal."

**Undetermined-legality default:** Where 11th Edition construction rules are not yet published, lean permissive and revisit when they firm up. Inventing a restriction the rules don't impose blocks legal lists on rules that don't exist — the one failure the differentiator cannot afford.

**Rationale:** The tool's entire reason to exist over New Recruit is enforcing legal construction where NR is permissive. Making that the explicit governing rule keeps later decisions from drifting into either over-restriction or freeform permissiveness, and gives every specific divergence a single principle to cite.

---

## D1 — Tool Purpose
**Decision:** The tool's sole purpose is Warhammer 40K 11th Edition Matched Play army list creation and output. No gameplay instruction, no tactical advice. The tool displays rules text as reference information to support list building decisions.

**Rationale:** Clear scope boundary prevents feature creep and keeps the tool focused on a well-defined, completable goal.

---

## D2 — Game Format
**Decision:** Matched Play only. Combat Patrol, Crusade, and other formats explicitly excluded.

**Rationale:** Matched Play is the competitive/tournament standard with well-defined, stable construction rules.

---

## D3 — Points Limit
**Decision:** Points limit is user-selectable in the app via a banner dropdown (1,000 / 2,000 / 3,000). Defaults to 2,000. POINTS_CAP is a live JS variable; changing it updates error states immediately. No construction rules are believed to change across points levels — only the cap changes — but this is noted as unconfirmed.

**Rationale:** 2,000 points is the standard competitive format. Variable points support was trivial to add once the cap was a variable rather than a constant.

*Updated from original: variable points now implemented in R5.4.*

---

## D4 — Technology Stack
**Decision:** Browser-based web app hosted on GitHub Pages. Claude Code (web interface at claude.ai) used for development. No local installation on developer machine.

**Rationale:** Developer (non-coder) has security concerns about local installs. GitHub Pages is free, requires no server infrastructure, and is sufficient for a static web app at this stage.

---

## D5 — Data Maintenance Approach
**Decision:** Unit data maintained manually by the product owner in Excel, converted to JSON for the app. GW's Munitorum Field Manual (PDF) and faction pack PDFs used as the authoritative data source. No automated scraping or third-party data feeds.

**Rationale:** GW publishes points updates ~12-13 times per year, most with only a few changes. Manual update is manageable. Going direct to GW source avoids third-party latency.

---

## D6 — JSON File Structure
**Decision:** Unit and lookup data split across four JSON files: (1) units.json — stats, weapons, wargear options, points, embedded abilities per unit; (2) keywords.json — keyword name and description lookup; (3) rules.json — rule name and description lookup; (4) config.json — detachment rules, faction lists, army-wide rules, points caps.

**Rationale:** Configuration data changes on a different cadence from unit data. Keywords and rules are shared across many units — storing descriptions once avoids duplication.

---

## D7 — Excel as Data Maintenance Tool
**Decision:** Unit data maintained in Excel, converted to JSON via a Python script (convert_to_json.py). CSV UTF-8 format used for file exchange.

**Rationale:** Unit data is inherently tabular. Product owner has 20+ years Excel experience.

---

## D8 — Weapon Options Enforced
**Decision:** The app enforces wargear options — base loadouts, substitutions, size-dependent options, and conditional restrictions. Display-only was rejected.

**Rationale:** If the app only displays wargear options without enforcing them, New Recruit already provides this capability. Enforcement is what differentiates the tool. *(Instance of D0.)*

---

## D9 — Release Philosophy
**Decision:** Early releases are not required to be independently useable. Each release makes progress toward a complete tool.

**Rationale:** Attempting to make each release independently valuable forces premature decisions and risks building the wrong foundation.

---

## D10 — Browser Caching
**Decision:** Three-layer caching fix: (1) _headers file at repo root with Cache-Control: no-cache; (2) no-cache meta tags in index.html; (3) VERSION constant in JS used as ?v= query string on units.json fetch. VERSION is bumped on every deploy.

**Rationale:** GitHub Pages aggressive caching caused repeated false failures during development. This combination eliminates the problem across all browsers without per-deploy manual steps.

*Updated from D30: added meta tags and version query string after _headers alone insufficient for Chrome.*

---

## D15 — Abilities Embedded Per Unit
**Decision:** Ability descriptions are embedded directly in unit records in units.json rather than stored in a shared lookup file. Keywords and rules remain in shared lookup files referenced by name.

**Rationale:** Abilities are unit-unique — the same ability name may have different parameters across units (e.g. "Deadly Demise 1" vs "Deadly Demise D3"). Embedding them avoids a parameterized lookup problem. Keywords and rules are genuinely shared and identical across units.

---

## D22 — INV and FNP Storage
**Decision:** INV and FNP stored as integers with companion condition fields (INV_Condition, FNP_Condition), not buried in ability text.

**Rationale:** These are commonly referenced stats that need to be queryable and displayable as structured data.

---

## D23 — Two-Level Parameterized Ability Naming
**Decision:** Lookup tables store generic ability names; unit/weapon records store full parameterized instances (e.g. "MELTA 2", "Deadly Demise 1").

**Rationale:** Allows abilities to be referenced by their exact instance while the lookup provides the generic description template.

---

## D25 — Daemonic Allegiance Units: Single Datasheets, God Selection at List-Build Time
**Decision:** Units with Daemonic Allegiance (Soul Grinder, Daemon Prince of Chaos, Daemon Prince of Chaos with Wings) are stored as single datasheets. God selection (Khorne/Tzeentch/Nurgle/Slaanesh) is made at list-building time in the app detail panel and stored on the army list entry. Copy-tier pricing is correctly enforced across all god variants since they share a single unit entry.

For Soul Grinder, god selection determines which conditional ranged weapon is equipped (tagged with Allegiance_Condition in Unit_Weapons). For Daemon Prince variants, god selection applies stat modifiers (Khorne: +2S hellforged; Tzeentch: +3A infernal cannon; Nurgle: +1T; Slaanesh: +2"M) — these modifiers are not yet enforced in the app.

The app identifies god-selection units via a hardcoded GOD_UNITS set in JS.

**Rationale:** Original D25 expanded these to four god-variant entries, which broke copy-tier pricing (each god counted independently, allowing 12 Soul Grinders with no premium). Single datasheets mirror GW's own representation and correctly enforce pricing.

*Supersedes original D25.*

---

## D26 — units.json Nested Structure
**Decision:** Each unit object in units.json contains: unit_name and unit_type at unit level; model_groups array with all stats, leader fields, and name arrays (unit_ability_names, rule_names, keyword_names); weapons array with model_group and allegiance_condition fields; wargear_options array; other_options array; points object (flat); abilities array with embedded descriptions.

**Rationale:** Pink Horrors confirmed the need for model_group-level differentiation — Pink Horror and Blue/Brimstone Horror groups within one unit have different keywords and stat lines.

---

## D27 — Unit Size: Ordered Slots with Trailing Blanks
**Decision:** Unit sizes stored as ordered numbered slots (Size_1, Size_2, Size_3). Size_1 always populated. Additional valid sizes fill Size_2 then Size_3. Blank values appear only as trailing blanks.

**Rationale:** Avoids blank-as-meaningful ambiguity that caused the Release 2 points-display failure.

---

## D28 — Points Pricing: Fully-Populated 3×3 Lookup Matrix
**Decision:** Points stored as a fully-populated 3×3 matrix crossing size slot (Size_1/2/3) with copy tier (1st/2nd/3rd+ unit). Column naming: Points_N-C (e.g. Points_1-1 through Points_3-3). Every valid cell populated with exact GW-published value.

**Rationale:** Pure lookup at [size, copy] with zero inference. Robust to irregular GW pricing patterns. Maintainer fills duplicate cells via Excel copy/fill.

---

## D29 — Army-Level Unit Instance Limit: Derived from Type with Override
**Decision:** Instance limits derived in code from unit type: Epic Hero = 1; Battleline and Dedicated Transport = 6; all others = 3. Optional override field in data for genuine exceptions. Limit is not a hard block — over-limit units show visual error flags but can still be added (D32).

**Rationale:** Limits are rule-derivable from unit_type for nearly all units. Hard blocks removed in D32 after confirming the construction mechanic use case.

---

## D31 — Immediate-Add Interaction Model
**Decision:** Clicking a roster card immediately adds the unit to the army list with default selections and opens it in the right panel for configuration. No "Add to Army" button. All option selections in the right panel write directly to the list entry and take effect immediately. Clicking any list entry in the middle panel opens it in the right panel for live editing.

**Rationale:** Reduces clicks, eliminates the staging/commit step, and matches New Recruit's proven UX pattern. Left-to-right flow: add from roster → configure in right panel. Editing existing entries follows the same flow starting from the middle panel.

---

## D32 — No Hard Enforcement of Instance Limits
**Decision:** Over-limit units can be added to the list. The app shows visual error flags (red "!" on list entry, warning in detail panel, amber roster card) but does not block the action. Points cap similarly non-blocking — list points turn red when over cap but no units are prevented from being added.

**Rationale:** List building is a construction and exploration activity. Users need to sketch different configurations, compare options, and temporarily exceed limits while making decisions. Hard blocks interrupt this workflow. Informational error states communicate violations clearly without forcing a specific resolution order. This is a UI-mechanism choice and does not relax the D0 legality boundary: every violation is still detected and flagged, so the tool's notion of what is legal is unchanged — only the prevention strictness differs.

---

## D33 — Leader Display in Army List
**Decision:** Attached leaders display above their bodyguard unit in the army list, not below or indented. Leader row shows at full size with the bodyguard name in parentheses: "Bloodmaster (Bloodletters)". The bodyguard block (leader + bodyguard) gets a subtle amber left border. No assignment dropdown in the middle panel — leader assignment is in the right panel detail view only.

**Rationale:** Above-bodyguard placement reads as a command hierarchy (leader first, then the unit they lead) which is tactically intuitive. Full-size text treats the leader as a peer entry, not a sub-item. Parenthetical bodyguard name gives assignment context at a glance without adding UI controls to the list panel. The dropdown in the right panel is sufficient for assignment changes and keeps the middle panel clean.

---

## D34 — Error Flag System
**Decision:** Three-layer visual error system: (1) roster card turns amber and shows over-limit X/Y badge in red when unit count meets or exceeds limit; (2) list entry shows red "!" flag next to unit name for any unresolved issue (over limit, missing god allegiance); (3) detail panel shows descriptive warning text at the top (over-limit warning in orange, incomplete flag in red). Nothing is blocked.

**Rationale:** Multiple signal layers ensure errors are visible at every level of the UI without requiring the user to open the detail panel to discover problems. Amber (limit warning) and red (error/incomplete) are distinct states. Red is reserved exclusively for errors — section headers and other non-error UI elements use grey.

---

## D35 — Banner Layout and Color System
**Decision:** Top banner contains: product name (red, left), separator, ARMY dropdown (grey label / gold value, positioned at 25% mark aligned with center panel left edge), ARMY POINTS dropdown (grey label / gold value, right-aligned at 70% mark aligned with center panel right edge), LIST POINTS (grey label / gold value, far right — turns red when over army points cap). Section type labels in both roster and army list panels are grey (#666), not red. Red is reserved exclusively for error and warning states.

**Rationale:** Consistent label/value pattern in the banner creates visual rhythm. ARMY and ARMY POINTS positioned to align with panel boundaries provides spatial context. Reserving red for errors makes error states more readable for older users and clearer in meaning — a red element always means something is wrong.

---

## D36 — Bundled / Compound Weapon Swaps
**Decision:** Weapon swaps where a single choice removes one weapon family and adds two or more families together (e.g. the Bloodthirster's "replace great axe with axe of Khorne **and** one of {bloodflail, lash of Khorne}") are represented as a New-Recruit-style single mutually-exclusive radio group with an explicit, selectable default line. The Bloodthirster group is three lines: "Great axe of Khorne" (the default), "Axe of Khorne + Bloodflail", and "Axe of Khorne + Lash of Khorne". Each line is self-contained — selecting it applies that line's full add-set and remove-set together. There is no show/hide or dependency logic between lines.

This is stored in a dedicated `bundled_swaps` array on the unit, **separate from** `wargear_options`. Each element is one group: a `group_label` plus an `options` list, where every line carries `label`, `adds` (weapon family base names to equip), `removes` (base names to unequip), and `is_default` (exactly one true per group). Add/remove use family **base names**; the app fans out to all profile rows of that family (consistent with D-base-name-fan-out). When a unit uses `bundled_swaps`, its conflicting `wargear_options` rows are removed.

**Rationale:** The legacy `wargear_options` row is a replacement *pair* (one replaced → one replacement) and cannot express a line that adds two weapons without inventing no-op or phantom-replaced rows that would pollute every consumer of that structure. A dedicated, self-contained array mirrors the locked UX directly, keeps the already-deployed simple-swap path untouched (lower regression risk), and is self-documenting for the Space Marines bundle queue (27 bundled swaps + 17 compound replacements). The explicit default radio replaces the earlier backwards modeling (data said "replace lash with bloodflail", which made lash appear default-equipped when the true base loadout is the great axe). Null/unset state resolves to the default line, so the base loadout needs no stored state.

**App behaviour:** Unset state ⇒ default line. The configured view computes active families from the chosen line's `adds` and replaced families from its `removes`; the union of every line's `adds` is recorded so unchosen replacement families drop out of the loadout. Validated against the real deployed `units.json` (Bloodthirster, all four states + invalid-label fallback) with the Lord of Change genuine two-weapon choice unaffected. Shipped in app VERSION 5.9 (two-file deploy: `index.html` + `units.json`).

---

## D37 — Stable Unit Reference: Wahapedia datasheet_id carried through pipeline
**Decision:** Every unit in `units.json` carries a `unit_id` field. Its value is the Wahapedia `datasheet_id` (carried through the transform via a new `Datasheet ID` column on `Unit_Stats`) where the source provides one, else a deterministic `local:<army-slug>:<unit-slug>` fallback for Gen-1 sources with no Wahapedia id (currently Chaos Daemons). Saved-list entries reference `unit_id`, not unit name.

**Rationale:** A reference-based saved-list model needs a stable key. `(army, unit_name)` is fragile to renames; the Wahapedia id survives renames. Same logic as the per-entry faction reference — costs nothing now, retrofitting ids onto already-saved lists later is real user-data migration. Verified: 234/234 units carry a `unit_id` (181 Wahapedia, 53 local-slug), unique within each army block. Critically disambiguates same-named-but-distinct datasheets (e.g. generic Impulsor id `000002568` vs Black Templars Impulsor id `000002786`). Implemented in `wahapedia_transform.py` (+ `Datasheet ID` column) and `convert_to_json.py` (emits `unit_id`); baseline counts unchanged.

---

## D38 — List Management: Storage Mechanism
**Decision:** Saved lists persist in browser **localStorage** as the primary store, with **JSON export/import** shipped alongside as core (not a backup nicety) — it is the only portability/sharing path in a backend-less app. All persistence goes through a thin **swappable list-store interface** (`get` / `put` / `list` / `delete`), made **async** (Promise-returning) even over synchronous localStorage so a future Drive/OneDrive backend is a one-module swap, not a sync→async refactor of every caller. URL-hash sharing and any server/cloud backend are deferred behind this seam.

**Rationale:** GitHub Pages is static — no server option without new infrastructure. localStorage holds hundreds of KB-sized lists comfortably. NR was confirmed server-backed with a local IndexedDB mirror; our inverse (local source-of-truth, optional cloud later) is sound. Built and headlessly tested in `list_store.js` (34 checks).

---

## D39 — Saved-List Data Model: Reference, Versioned, Flag-Don't-Drop
**Decision:** A saved list stores: `schema_version`, `id`, `name`, `points_target`, `primary_faction`, `created`/`modified`, and an `entries` array. Each entry carries `faction_ref`, `unit_id` (D37), cached `unit_name`/`unit_type`, `size_idx`, `god`, `wargear`, `other_options`, `attached_to`, and a display-only `points_cache`. Points are **never authoritative in the blob** — they are recomputed on load (reference model, not frozen snapshot), correct for Matched Play where MFM/dataslate points change. On load, entries **re-resolve (id-first, name-fallback) and re-validate**; an unresolved unit renders as a **flagged ghost row** carrying saved name/points, never silently dropped. `schema_version` drives forward migration of older saved blobs.

**Rationale:** Matched Play requires current points and current legality; a frozen list silently fields a mispriced/illegal army. Id-first resolution lets a renamed unit load under its current name. Two failure render-states: soft-illegal (unit resolves, config now illegal → live flag, same surface as D34) vs hard-unresolve (unit gone → ghost row). Build-side `integrity_check` id-diff (future) catches dropped ids before users hit them.

---

## D40 — List Construction Model: Model 2 (faction-on-list, autosave, home page)
**Decision:** Adopt the New-Recruit-style model. **Faction is a property of a named list, set at creation** via a create-list modal (name + faction); there is **no faction-switch on an open list**. The active list **autosaves on every mutation**. Clearing is **decoupled from the faction selector** and becomes an explicit "New List" action with an unsaved-changes confirm (supersedes the prior clear-on-faction-switch behavior). The list builder is entered *from* a **home/landing page** (browse saved lists / create new / open existing) — the home page is the front door of the list-management build, built as part of it, not a separate step. The roster is **faction-agnostic / allies-ready**: `primary_faction` drives identity and grouping; allied units are added through a separate path with their own per-entry `faction_ref`.

**Rationale:** Model 2 removes the clear-on-switch tension entirely rather than patching it, is allies-compatible by construction, and is validated by NR's UX. Autosave + required name/faction at creation means there is no anonymous in-progress list to lose. Clear-on-switch was a destructive, hard-block-style action sitting against D0/flag-not-block; an explicit "New List" is non-destructive.

---

## D41 — MFM Update Strategy: Full Re-Pull of Changed Armies, No Patcher
**Decision:** When GW publishes MFM updates, re-pull the **complete current page for only the armies that changed** (usually 1–4) and run them through the existing parser; never build a surgical points-patcher or a persistent changes/delta file. Points are a single current value updated in place (no history/replay). A small re-pull of one army is the lightweight path for a 1–4 unit hotfix. "Full" = the changed armies' whole pages, **not** all 30 factions.

**Rationale:** GW publishes full per-army snapshots, not diffs (confirmed). One ingestion path (full-snapshot parse) beats two; re-pull always matches GW's current snapshot, a patch is only as correct as the changelog reading. Eliminates the points-only-vs-structural routing judgment a patcher would force every release. Optional `mfm_diff.py` (re-pull vs committed) gives derived "what changed" visibility without a changes file. The override layers (faction-pack errata, bundled_swaps) re-apply on the fresh pull by design.

---

## D42 — SM-Family Chapter Points Sourcing: Base + Build-Time-Derived Override
**Decision:** Within the Space Marine family only, chapter points = `mfm_sm.txt` **base** prices for the shared generic roster **plus a build-time-derived per-chapter override** (the delta wherever a chapter's own complete MFM file prices a shared unit differently). The override is **derived every build** by diffing the chapter file against base — never hand-maintained, so it cannot drift. Shared generic datasheets stay single (one Intercessor datasheet, unioned into chapter views) and keep base price unless a chapter override applies. Chapter-exclusive units price from the chapter file. **Black Templars' re-printed units are distinct datasheet IDs** carrying their own BT-file prices natively — not overrides. **Vanilla chapters** (Ultramarines, Iron Hands, Salamanders, Imperial Fists, Raven Guard, White Scars) source from their sections inside `mfm_sm.txt` and have no shared-unit re-pricing.

**Rationale:** Each chapter MFM is a complete authoritative faction file that re-prices some shared units (Blood Angels re-prices 8 assault units, e.g. Assault Intercessors 75→80; Space Wolves/Dark Angels 1 each). The shared-datasheet structure makes self-contained per-chapter duplication wasteful; a derived override keeps one datasheet and a tiny delta map, with no drift because it is recomputed each build. Mechanism is **SM-family-only** — there is no parent base to override against elsewhere.

---

## D43 — Cross-Faction / Allied Points Sourcing (Pattern Catalog)
**Decision:** Two structurally distinct sourcing relationships, handled by two mechanisms. **Pattern 1 — parent base + child extension (SM chapters):** handled by D42 (base + derived override). **Pattern 2 — allied borrowing (Genestealer Cults borrowing Astra Militarum/Tyranids; Imperial↔Chaos Knights; Drukhari/Aeldari Harlequins):** the borrowed unit belongs to its home faction, is a distinct datasheet, and carries its **home faction's points sourced from that faction's MFM**, added via a separate "add ally" path with its own per-entry `faction_ref` (already locked). A faction_id filter alone does **not** equal a faction's own codex roster (GC `faction_id` returns 139 datasheets = 24 GSC codex + ~100 allied Guard + 14 Tyranid); scope a faction's *own* units to its codex source, treat the rest as allied inclusions. The build must ingest allied factions' data so their points are available to look up.

**Rationale:** Confirmed across the full cross-faction MFM analysis (`MFM_Chapter_Pass.md`, `MFM_Standalone_Pass.md`). Pattern 2 is the allies problem already in scope; GSC is its largest concrete instance. Keeping the two mechanisms separate prevents the override logic from leaking outside the SM family.

## D44 — Structured Loadout Definition Schema (unit_loadouts.json)
**Decision:** Structured loadout definitions are stored in `unit_loadouts.json`, keyed by `unit_id` (Wahapedia datasheet id). Each entry has `size_brackets`, `model_groups` (name, count fixed/fills_to_size, default_weapons), and `options`. Option types: `choice` (1-for-1 within single-model scope), `count` (size-scaled swap with per_n_models/max_per_n; may carry `replacement_choices` for count-with-choice), `add` (keeps base weapon, adds new one; may `blocks_swap` to reserve pool slot). Hand-authored entries carry no `_parser_flags`; parser-generated entries carry the flag list. The parser preserves hand-authored entries on re-run.

**Rationale:** Flat wargear options from the Wahapedia export cannot represent model-group scope, shared pool caps, or add-vs-swap distinctions. A structured per-unit definition, generated by a parser with hand-authored overrides, enables exact weapon count rollup and correct legality checking. Same parser + override pattern as MFM processing.

---

## D45 — Weapon Count Rollup: Exact, Not Heuristic
**Decision:** Weapon counts in the popup are computed exactly from composition (model counts per group) × default weapons ± user-selected swaps and adds. The rollup is not an estimate — it is exact once the option model is complete. Count stepper controls in the UI are the mechanism: the user's input is the count, which flows into the rollup. Over-allocation is flagged (not blocked) via the shared-pool cap (D34 applies).

**Rationale:** Correct weapon counts are required for gameplay. A heuristic approach (assuming uniform loadouts) would produce wrong counts on units with non-uniform defaults or mixed swaps. The structured option model makes exact counts derivable from first principles.

---

## D46 — Add vs. Swap Distinction (Critical for Correct Counts)
**Decision:** "Equipped with" in GW datasheet prose = `add` option type (model keeps its original weapon AND gains the new one). "Replaced with" = `choice` or `count` swap (original weapon removed). The parser and all hand-authored definitions must honour this distinction. Reference case: Intercessor Squad grenade launcher is an `add` (bolt rifle ×5 + grenade launcher ×1, not bolt rifle ×4 + grenade launcher ×1).

**Rationale:** Getting this wrong silently produces incorrect weapon counts — exactly the kind of error the loadout system exists to prevent. The distinction is clear in the rules text; it must be preserved through the data model.

---

## D47 — Parser + Override Layer Pattern for Loadouts
**Decision:** `loadout_parser.py` generates the base definitions for all units; hand-authored entries in `unit_loadouts.json` are the override layer and are never overwritten by the parser. The `_parser_flags` list on each parser-generated entry is the work queue for manual review. Units with flags render with whatever options the parser did extract; they don't crash or block.

**Rationale:** Same pattern as MFM processing (machine-generated base + hand-curated exceptions). Prevents the need to hand-author all 370+ definitions while still allowing precise overrides where the parser can't handle the prose.

---

## D48 — army-name Flag Required for Non-SM Factions
**Decision:** `wahapedia_transform.py` must be called with `--army-name "Faction Name"` for every non-Space-Marines faction. Without it, all units default to "Adeptus Astartes" and silently collide with the SM block on merge. This is a required argument for every new faction onboarding, not optional.

**Rationale:** The original script hardcoded the generic army name for the SM use case. The `--army-name` flag generalises this without changing SM behaviour. Death Guard was the first faction to hit this; the fix was the flag.

---

## D49 — Equipped-With Composition Parser (New Source + Parser Layer)
**Decision:** Per-model weapon attribution is recovered from the datasheet UNIT COMPOSITION "... is equipped with:" wording, which the Wahapedia CSV export drops. A pasted Wahapedia composition text file (one per faction, e.g. `Space_Marines_web.txt`, `Death_Guard_web.txt`) is a recorded source, in the same class as the MFM `.txt` files. A new pipeline tool, `equipped_parser.py`, reads it and writes authoritative per-group `default_weapons` into `unit_loadouts.json`, layering over the flat-pool baseline that `loadout_parser.py` produced. Subject grammar: "Every/This/All/Each model" → all model groups; "The X and every Y is equipped with" → groups X and Y; "The X is equipped with" / "Each Y" → that group. Weapon-list tokens split on both `;` and `,`. Weapon names resolve via case/apostrophe normalisation, base-name matching (variant weapons like "Plasma incinerator – standard/supercharge" both returned), plural tolerance, and a global cross-unit fallback.

**Rationale:** The flat weapon pool assigned every base weapon to every model group, which is wrong for any unit whose groups carry different weapons (command squads, bikes + attack bike, Techmarine + Thunderfire, etc.) — the popup is the play surface, so this made those units unplayable from the tool. The "equipped with" prose is the authoritative per-model source and is stable within an edition. A pasted text file (not a live scrape) avoids fragility, avoids scraping-legitimacy concerns, and survives edition changes; only new/re-cut datasheets need a re-paste. 109 units (79 SM + 30 DG) corrected.

---

## D50 — default_wargear Schema Field
**Decision:** Non-weapon items appearing in "equipped with" text (e.g. Astartes shield, jump pack) are stored in a per-group `default_wargear` list, separate from `default_weapons`. Any token that does not resolve to a weapon profile is routed here and flagged in the parser report for human verification (real wargear vs a weapon missing from our data). Display of `default_wargear` in the popup is a separate, still-pending UI task.

**Rationale:** These items affect play (an Astartes shield grants a 4+ invulnerable save) and the popup is the play surface, so they must be captured. They are not weapons, so mixing them into `default_weapons` would corrupt weapon rollups. A separate field keeps the two clean while preserving the information.

---

## D51 — default_weapon_counts Schema Field
**Decision:** A per-group `default_weapon_counts` map (weapon name → integer count) records quantities greater than 1, for single-model vehicles that mount multiple of a weapon (Land Raider 2× Godhammer lascannon, Whirlwind 4× Twin heavy bolter + 2× Lascannon, etc.). The field is sparse — only weapons with count > 1 appear. The popup rollup (`loRollup` in `index.html`, v5.23) multiplies each default weapon's contribution by its count, defaulting to 1 when absent. The parser reads the leading quantity prefix in composition tokens ("2 fragstorm grenade launchers") and records it.

**Rationale:** Without this, the popup showed one weapon where the model has several — a Land Raider firing one lascannon instead of two — the same "wrong at the table" error the loadout system exists to prevent, applied to vehicles. The sparse-map approach is non-breaking (weapons with no count behave exactly as before) and mirrors the additive pattern of `default_wargear`.

---

## D52 — Curated-Roster Scoping + Orphan Pruning
**Decision:** Loadout parsers key off the curated roster (`units.json` unit_ids), not the full raw Wahapedia datasheet list. Any datasheet in a paste whose name does not match a shipped unit is dropped, and pre-existing loadout entries with no backing unit are pruned from `unit_loadouts.json`. Ownership of composition blocks is resolved by datasheet TITLE (a roster-name line followed by the stat header), so roster names appearing inside "can be attached to the following units" lists or as model-profile rows are ignored. This removed 151 orphan entries (Legends/FW/excluded) that were inflating the file and the review queue.

**Rationale:** `loadout_parser.py` had run against the full datasheet list and generated definitions for units we don't ship, unreferenced by the app but bloating the file and overstating the flagged-review count. Scoping to the roster makes the flag queue reflect only real work.

---

## D53 — Legends: Keep in Source, Defer Processing
**Decision:** Full composition pastes include Legends (and Forge World) units — the source is banked — but the parser drops them now because they are not in the shipped roster. When Legends/FW is onboarded later (entering `units.json`), the same parser picks up their per-model defaults automatically with no re-paste and no parser change. Getting Legends "right now" would mean doing the deferred Legends onboarding early, which is not warranted for the initial release.

**Rationale:** The durable asset is the source files, not the generated JSON. Parsing Legends later gives identical results to parsing now (composition wording is edition-stable), so there is zero accuracy cost to deferring — only a cheap future re-run. This keeps the initial release scope tight while foreclosing nothing.

---

## D54 — Wargear-Option Controls: Two-Control Model
**Decision:** The configure pane renders wargear options with two controls chosen by option type. **Count** options (size-scaled — "for every N models…", "any number of…") use a **count stepper**. **Single-model exclusive** choices (a champion's "replace weapon with one of the following") use an **exclusive choice row** (radio behaviour: selecting one clears the others). Ratified this session as intentional; it was already live in the build.

**Rationale:** A stepper cannot enforce "pick exactly one," so a per-option stepper on a mutually-exclusive choice would let a user set two exclusive weapons to 1 at once — an illegal loadout (D0). The two-control split is the mechanism that keeps single-model choices legal while letting count options scale with unit size.

---

## D55 — Leader/Champion Block Visually Separated (Configure Pane)
**Decision:** In the configure pane, the leader/champion model's options render in their own visually distinct block (bordered card, slightly raised fill, neutral gray only — no red/gold semantics). The leader model is identified **structurally** as the first `model_group` with `count.fixed == 1`, not by name.

**Rationale:** Champion names vary too much across factions to keyword-match (Sergeant, Champion, Sword Brother, Plagueridden, Ancient…). The fixed-1 signal is faction-agnostic and correctly separates 49 of 53 multi-group units; the misses are genuinely leaderless units (correctly separated: none) or parser artifacts, not false negatives.

---

## D56 — Two Option Surfaces: Unconfigured Popup vs Configure Pane
**Decision:** Options appear on two distinct surfaces with different jobs. The **left-panel unconfigured popup** is a read-only survey — base equipment plus every option the unit *could* take, for browsing. The **right-panel configure pane** is the interactive build using the two-control model (D54). They read from **different sources**: the popup surveys all weapon profiles the datasheet references (informational); the configure pane reads structured `options` from the loadout def. A unit can therefore look complete in the popup while its configure-pane options are incomplete.

**Rationale:** Separating "everything this unit can be" from "what you are actually choosing" matches how a builder is used, and explains why a display gap on one surface is not a data gap on the other.

---

## D57 — Heterogeneous Named-Model Units Require Composition Prose
**Decision:** Units whose models carry *different* weapons (named epic-hero squads — Wardens of Ultramar, Victrix Honour Guard — and mixed kill teams / command squads) require the pasted Wahapedia composition **prose** ("*X is equipped with:*" lines) to produce correct per-model weapons. The Wahapedia CSV export carries only a flat, datasheet-level weapon list with no per-model mapping and is insufficient. Until the prose is pasted and parsed, such a unit falls back to `loadout_parser`'s placeholder — every model gets the full weapon union — which is **known-wrong and detectable**: `_defaults_source != "equipped"` **and** identical `default_weapons` across multiple model groups. That combination inflates every weapon to ×(unit size) on the play surface.

**Rationale:** The CSV drops the "equipped with" ownership; the composition page is the only authoritative per-model source. Naming the fallback signature makes the affected units auditable instead of silently shipping wrong counts.

---

## D58 — "Every Other Model" Resolves to the Complement of Named Groups
**Decision:** In composition prose, an equipped line whose subject is "*every/all/each other model*" targets **all model groups not explicitly named by another equipped line in the same unit**. The parser makes two passes per unit: first it records which groups are bound by name (e.g. "The Ravenwing Champion is equipped with…"), then it applies each "other model" line to the remaining groups.

**Rationale:** This is a standard Wahapedia idiom for "the rest of the squad" (Ravenwing Command Squad: Champion is named, so "every other model" = Apothecary + Ancient). Without complement logic the line matches no group and drops, leaving those models on wrong flat weapons. Resolving by *complement of named groups* is faction-agnostic and needs no per-unit configuration.

---

## D59 — Tolerant Group-Name Matching (Footnotes, Irregular Plurals, "model" Suffix)
**Decision:** The equipped-line subject → model-group matcher is normalised to tolerate the ways datasheet prose and stored group names drift apart. It (a) strips a trailing "model"/"models" left after the determiner (so "Each Victrix Honour Guard model" binds to group "Victrix Honour Guard"), (b) strips trailing footnote markers from group names (so "Cenobyte Servitors\*" binds), and (c) matches across regular **and** irregular -ves plurals (so prose "Hunting Wolf" binds to group "Hunting Wolves"). The three former match passes (exact, plural, role-suffix-stripped) are consolidated into one keyed comparison.

**Rationale:** Each of these is a whole *class* of phrasing, not a one-off. Handling them generally means future units using the same idioms parse with no new work. Verified against the full Space Marines + Death Guard equipped layer: the rewrite reproduces every previously-correct unit byte-for-byte and changed only the five intended units.

**Note on scope of the fix vs. a latent trap:** when a unit has multiple groups and only some are bound by an equipped line, the parser still marks the whole unit `_defaults_source: "equipped"` while any unbound group silently retains its earlier flat weapons. Not triggered by the units fixed this session (all groups bound), but tracked below as a latent correctness trap.

---

## D60 — Victrix Honour Guard Count Model + Army-Wide Character Cap
**Decision:** Victrix is size-first (brackets 3 / 6). The two character groups (Chapter Ancient, Chapter Champion) are optional **0-1 toggles** that each consume one slot from the chosen size; the body (Victrix Honour Guard) fills the remainder. Army-wide across all Victrix units (up to 3 per army): at most **one** Victrix Ancient and **one** Victrix Champion; both may sit in the same unit. The cap is scoped to the **in-datasheet** Victrix Ancient/Champion only — not the standalone Chapter Ancient / Chapter Champion characters that share the name.
**Status:** Per-unit count model implemented in `loadout_parser` (`0-N` composition rows now parse to an *optional* group, not fills-to-size). The army-wide ≤1 cap is the project's **first cross-unit, within-datasheet legality rule** — no home in the current per-unit enforcement model; deferred to the enforcement-engine buildout as a flagged requirement. The character toggles also need a points source + toggle UI (see D-priced-optional item in the queue).

---

## D61 — Un-onboarded Units: Points-Driven "Unverified" Badge, Not Hide (resolves old Item 8)
**Decision:** Do **not** hide un-onboarded units. Show them and badge "unverified," driving the badge off the **data** — a unit is unverified iff it lacks a `points` object — rather than a hand-maintained faction allowlist. Pair with an explicit configure-pane empty-state ("not yet onboarded — points and options pending") replacing the current blank render.
**Rationale:** Test-mode tool; hiding costs coverage on the units that most need eyes. Points-presence is self-maintaining, finer-grained than faction-level (the ~97 missing units are scattered inside already-onboarded armies), and honest during onboarding. Badges clear automatically as points attach; the badged set doubles as the onboarding worklist. Onboarding remains the real fix; badging shrinks to nothing as it proceeds.

---

## D62 — "OR" Alternative-Profile Units → Size Brackets + Per-Bracket Counts
**Decision:** A composition containing a bare **"OR"** separator (two alternative legal builds — Wolf Scouts 6 vs 12 models, Decimus 5 vs 10) maps onto the existing **size brackets**: profile *i* → bracket *i*. Groups whose count is constant across profiles emit a fixed count; groups whose count **varies** emit an explicit `per_bracket` count keyed by bracket size (e.g. `{"6":1,"12":2}`). No fills-inference inside OR units — each bracket is one exact legal composition. Bracket-fixed counts render **non-editable with no stepper** (a counter appears only where the count is the player's to change).
**Rationale:** Reuses the size-first control; faithful to the rule (you cannot take 5 scouts at size 6). Also dissolves the earlier "duplicate group" symptom — the parser emits 3 aligned groups, not 6. Cross-profile group alignment reuses the singular/plural idiom (Hunting Wolf ↔ Hunting Wolves).

---

## D63 — Compound "A and B" Replacement Choices Are One Pick (D0 held)
**Decision:** A replacement-list item written "X and 1 Y" is a single **compound** choice (two weapons at once), kept together and rendered "X + Y" — not split into two entries. The rollup splits a selected compound on " + " and tallies each weapon. **D0 held:** all *legal* options remain, including strictly sub-optimal picks (chainsword-only / power-weapon-only sergeant); the tool enforces **legality, not optimality** — guide via sensible defaults, don't curate the option list.
**Rationale:** The old list-splitter broke compounds at "and," producing fake duplicates (the "Sternguard duplicate rows" artifact was actually this). General fix across **33** SM/DG datasheets (10 in the deployed roster). **Known limitation:** a compound whose second item is a **shield** (relic / terminator storm / blizzard) displays correctly but tallies the shield in the *weapons* bucket, not equipment (4 units, flagged).

---

## D64 — Coupled-Control Hard Interlock (Local Exception to D0 Flag-and-Warn)
**Decision:** When two option controls are legally coupled — one option's eligibility depends on a weapon another option can remove — the dependent control is a **hard interlock**, not a flag. It disables (greyed, non-clickable, "needs &lt;weapon&gt;") and auto-clears (freeing any shared-pool slot) the moment its prerequisite weapon is swapped away, rather than staying pickable with a warning. This is a deliberate **local exception to D0's flag-and-warn default**: prevent the illegal combination at the coupled control instead of allowing-and-flagging. First instance (shipped v5.29): the Intercessor Sergeant grenade-launcher toggle, coupled to the Sergeant's bolt-rifle ranged choice (the rule requires "a model equipped with a bolt rifle"). Enforced in **both** the renderer and the rollup engine, and expressed in data as a `requires_weapon` field on the option.
**Rationale:** For a two-control dependency, letting the user build the illegal combo and then flagging it is more confusing than removing the option — cause (the ranged swap) and effect (grenade launcher now illegal) sit in different blocks. Disabling shows the dependency directly. Flag-and-warn stays the default for soft constraints (pool over-allocation, etc.); this exception is scoped to explicit weapon-prerequisite couplings.

---
## D65 — Leader Inclusion in a Per-N Carrier Pool Follows the Datasheet Wording
**Decision:** Whether a unit's leader (Sergeant/Champion) is an eligible carrier for a per-N "special weapon" pool is read from the rule's wording, not assumed. Generic "1 **model** equipped with X" **includes** the leader; a rule naming the **body model** ("1 **Sternguard Veteran**'s X", "1 **Heavy Intercessor**'s X") **excludes** it. Consequences: **Intercessor** grenade launcher — "1 model equipped with a bolt rifle" → the Sergeant is a legal carrier sharing the unit-wide per-5 pool (shipped v5.29, via a `pool_id` spanning the Sergeant toggle and the body stepper). **Sternguard** pyrecannon / heavy bolter — "1 Sternguard Veteran's…" names the body → the Sergeant is **excluded**, so the previously-queued "Sternguard Sgt special-weapon eligibility" item (old queue item 4) is **dropped** — building it would have added an illegal option. **D0 held:** model exactly what the rules allow.
**Rationale:** The datasheet distinguishes these two carrier scopes explicitly; treating them uniformly would either wrongly bar the Intercessor Sergeant or wrongly permit the Sternguard Sergeant. The same wording is the parser's future signal for auto-scoping leader eligibility. Shipped capability: `pool_id` (unit-wide shared cap that may span model groups) + `requires_weapon` (see D64) generalise this without new per-unit code.

---

## Session 15 — Queue Items Resolved
- **Sternguard "duplicate choice rows"** — root cause was compound-choice mis-split, not fan-out. Fixed (D63).
- **Kill Team phantom "MODELS MAXIMUM" group** (Fortis, Talonstrike, + Spectrus, Indomitor) — fixed by skipping `N MODELS MAXIMUM` annotation lines **and** normalising the non-breaking hyphen (U+2011) that had been silently failing their range rows in `clean()`.
- **Decimus / Wolf Scouts duplicated model groups** — were "OR" alternative profiles, not duplicates. Fixed (D62).
- **Victrix count model** — per-unit part fixed (D60); army-wide cap deferred to enforcement engine.

---

## Parser Review Queue / Known Data Issues (not decisions — tracked items)
- **Forge World weapon gap:** unit `000002727` references weapons absent from our data (Astraeus las-rippers, Thunderhawk cannons, twin macro-accelerator cannon). Routed to `default_wargear` and flagged. Resolves when FW weapon data is added or the unit is hand-authored; consistent with FW being deferred.
- **Duplicate unit-names in `units.json`:** several names map to two unit_ids — Terminator Squad, Repulsor, Impulsor, Gladiator Reaper/Valiant/Lancer, Land Raider Crusader, Sternguard Veteran Squad, Repulsor Executioner (plus Daemons duplicated with numeric ids). Because `name2id` collides, only one id of each pair receives equipped-with defaults. Roster data-cleanup item, independent of the parser. Minor related item: weapon-name casing drift ("Bolt Pistol" vs "Bolt pistol") across units.

- **Option scope resolution fixed (`resolve_scope`, this session):** was substring-matching, which mis-scoped body options ("for every N models… 1 Veteran…") to the leader group. Now word-scored (singular-normalised, closest match, leader/body preference). Corrected 8 units (Sternguard, Terminator Squad, Eradicators, and 5 others) — special weapons now scope to the body group.
- **Named-hero equipped-line matching fixed (`match_group`, this session):** matched the "*X is equipped with:*" subject only on exact/plural name, so a model whose group carries a "` - EPIC HERO`" role suffix never bound. Now also matches on the group name before the " - " suffix. Wardens of Ultramar onboarded correctly (laspistol ×3, power weapon ×2, ccw ×2; storm shield + refractor field to `default_wargear`).
- **Victrix Honour Guard (`000004185`) — DONE this session.** Composition prose pasted; parser fix D59 ("Each X model") applied. Per-model weapons now correct (Ancient: mc power weapon + banner of Macragge→wargear; Champion: blades of honour; each Guard: mc bolt carbine + mc power weapon). **Still open:** its *count model* — the three groups (0-1 Chapter Ancient, 0-1 Chapter Champion, 1-6 Victrix Honour Guard) all read `count.fills_to_size == true`, which is wrong for a build-choice unit that must sum to the bracket (3 or 6). Weapons are right; totals are not until the count model is fixed. Blocked on the NR-handling answer for optional-character-plus-variable-body units. Comes from `loadout_parser` (first stage), not the equipped parser.
- **Four heterogeneous units onboarded this session (D58/D59).** Chaplain Grimaldus (BT), Crusader Squad (BT), Ravenwing Command Squad (DA), Wolf Guard Headtakers (SW) moved from flat-fallback to correct equipped weapons via three new banked composition files (`Black_Templars_web.txt`, `Dark_Angels_web.txt`, `Space_Wolves_web.txt`). These fix *weapons only* — the factions themselves (BT/DA/SW) remain un-onboarded (points, detachments, rules unverified). `unit_loadouts.json` equipped count 110 → 115.
- **Flat-fallback triage (supersedes the old blanket item 8).** The 21 multi-model flat-fallback units are **not uniformly wrong.** They split into: (1) 4 already-onboarded-faction units needing a *different* fix, not prose — Sternguard, Terminator Squad (SM), Plaguebearers, Plague Drones (DG); (2) 4 genuinely heterogeneous — **fixed this session**; (3) 3 Deathwatch kill teams blocked on parser junk (see below); (4) ~10 homogeneous leader-plus-body squads where a flat *default* weapon list is **likely already correct** and the real gap is unmodeled wargear *options*, which is faction-onboarding work, not a paste. Verify-caveat: the "likely correct" call is inferred from unit knowledge, not parsed data, since those factions aren't onboarded.
- **Item 8 product question (still open, now reframed):** whether un-onboarded-faction units (BT/DA/SW/Deathwatch) belong in the roster at all. Now clearly a *scope* decision (depth-on-a-subset vs. breadth) rather than a loadout one. Options: hide until onboarded / mark "unverified" / commit to full onboarding.
- **Stale-group trap (latent, from D59 note):** a partially-bound multi-group unit is marked `equipped` while unbound groups keep stale flat weapons. Add a guard so a unit is only marked `equipped` if every group bound, or flag unbound groups explicitly.
- **Kill Team parser junk (blocks the 3 kill teams):** `000002780` / `000003874` carry a phantom "MODELS MAXIMUM" group (fixed 10); `000004175` (Decimus) and `000004182` (Wolf Scouts) carry *duplicated* model groups (same fan-out family as the Sternguard duplicate-choice artifact). Composition prose won't stick until the group structure is cleaned. Fix parser first, then paste.
- **Footnote asterisk in stored group names:** matching now *tolerates* "Cenobyte Servitors\*", but the stored/display name still carries the asterisk and will show in the popup as a stray mark. Strip trailing footnote markers at group-derivation time in `loadout_parser`.
- **Sternguard duplicate choice rows:** the Sergeant "bolt rifle options" choice contains duplicate entries (chainsword ×2, power weapon ×2, bolt rifle ×3) — parser fan-out artifact, unresolved.
- **UNMATCHED body swaps still dropped:** Sternguard combi-weapon; Terminator Assault Squad thunder-hammer+storm-shield → twin lightning claws (a bundled two-for-one swap). Part of the 139-unit flag queue. Terminator Assault Squad shows no configurable options until authored.
- **`loadoutFor` name-lookup fragility:** resolves a unit by `unit_name` first-match rather than the entry's own `unit_id`; latent robustness issue tied to duplicate unit-names. Not misfiring in current deployed data, but should resolve by `unit_id`.
- **`default_wargear` now populated but unconsumed:** Wardens (storm shield, refractor field), plus this session Wolf Guard Headtakers (storm shield). The popup still has no UI reader for `default_wargear`.
- **Duplicate unit-names in `units.json`:** several names map to two unit_ids — Terminator Squad, Repulsor, Impulsor, Gladiator Reaper/Valiant/Lancer, Land Raider Crusader, Sternguard Veteran Squad, Repulsor Executioner (plus Daemons duplicated with numeric ids). Roster data-cleanup item.
- **Forge World weapon gap:** unit `000002727` references weapons absent from our data. Routed to `default_wargear` and flagged; resolves when FW data is added. Consistent with FW being deferred.


## Session 15 — New / Updated Open Items
- **Configure pane renders options only, not model-group composition.** Units whose groups have no options (per-bracket units — Wolf Scouts, Decimus) render a near-empty pane: no NR-style "leader / body / extras" breakdown. **HIGH priority — unblocks visibly testing per-bracket units.** Needs a composition-rendering feature.
- **Priced optional groups (blocked on points source + toggle UI):** Victrix Ancient/Champion toggles (D60) and Wolf Guard Headtakers' matched Hunting-Wolf pack. The wolves are a *matched pack* (0 or bracket-count: 3-at-6, 6-at-12), **additive** (do not consume Headtaker size), priced from the MFM combos 85/115/170/230. The current size-bracket points model does not capture optional-group pricing. Same shape for both.
- **Sternguard Sergeant special-weapon eligibility:** the Sgt should be eligible for the per-5 pyrecannon / Sternguard heavy bolter, currently body-scoped only (Sgt is a Veteran).
- **Captain:** (a) missing master-crafted bolter in base equipment (units.json weapons layer); (b) two-section **either/or** swap not modeled — "replace all base with pistol+melee combo" vs "replace close-combat weapon only," mutually exclusive; the compound rows show but cross-section exclusivity isn't enforced.
- **Terminator Squad options wrong** — investigate.
- **Shield-in-weapons-tally (D63 limitation):** route equipment-type compound parts (shields) to the equipment tally instead of weapons (4 units).
- **Single-form "replaced with A and B" compound** (e.g. Decimus thunder-hammer → power weapon + Astartes shield): same pattern as D63 but outside the "one of the following" list — a different classifier path, not yet handled.
- **Victrix group-name cosmetic:** stored group names carry the "` - EPIC HERO`" epithet ("Chapter Ancient - EPIC HERO").
- **Per-chapter MFM points pipeline** — the real onboarding mechanism for the ~97 points-less units. Large phase; the D61 badge is the interim.

## Session 15 — Data / Pipeline Facts Confirmed
- **units.json is current** (project copy == repo HEAD, branch `main`). Sizes and points live under a per-unit **`points`** object (`points.sizes`, points matrix), **not** a top-level `sizes` field. **173 / 270** units have points; ~97 do not (onboarding in progress). The app derives the size selector from `unit.points.sizes` — no points ⇒ no selector ⇒ blank pane.
- **Points come from the MFM `.txt` files via the Claude-run pipeline** (`mfm_points_parser`). `Unit_Points.csv` / `convert_to_json` (the Excel-workbook path) is **stale/vestigial** — 53 rows, does not cover current units. **Do not regenerate units.json from the Excel CSVs.** Source of truth = the Claude-run versions committed to the repo.
- **Duplicate-name datasheets, use `unit_id`:** Sternguard has two entries — Adeptus Astartes `000002255` (onboarded, has points) and Black Templars `000004137` (re-print, no points). Name-first lookups collide (confirms the `loadoutFor` fragility item).


## Session 16 — Queue Corrections & Banked Work
- **Old queue item 4 (Sternguard Sgt special-weapon eligibility) — DROPPED.** See D65: the rule names the body model, so the Sergeant is correctly excluded; the current body-only scoping is right.
- **"Sternguard duplicate choice rows" — mislabeled, closed.** No duplicates exist in the current data (the Sergeant choice is 7 clean entries). The real gap was the missing combi-weapon body swap, which is one instance of the any-number-family parser bug below.
- **BANKED — any-number-family single-replacement parser bug (needs a dedicated session).** A one-character bug (missing space after `replaced with`) in the **shared tail** of the "Any number / All models / Up to N" matcher makes **all single-replacement lines of these three forms** fall to `UNMATCHED` (only the "one of the following" list variant matched). Fixing the space alone cascades to **21 SM/DG units**. Three sub-problems must be handled together, or the fix trades one flaw for another:
  1. **Trailing-period weapon names** — e.g. `storm shield.` fails normalisation (`WEAPON_NOT_FOUND`).
  2. **Compound replacements** — `replaced with 1 A and 1 B` (e.g. Indomitor, Crusader) emit a swap to an unmatchable single name; needs the D63-style `" + "` split applied to this option type.
  3. **Compound sources** — `A and B replaced with …` (e.g. Deathwatch Terminator Squad `000003873`) must be handled without regressing units the "one of the following" path already matches; a naive `" and "` source guard **dropped** `000003873` from 1 option to 0.
  Validate with the full prune-correct reproduction chain. Note (confirmed this session): `equipped_parser` only sets per-group `default_weapons`; it never touches `options` or `_parser_flags`. So a parser-only change can be blast-radius-checked by regenerating `loadout_parser` output and diffing **options + flags** against committed, without re-running the equipped chain. `loadout_parser` emits **368** entries pre-prune vs the **217** committed post-prune — expected, not a discrepancy.

## Session 16 — Shipped
- **index.html v5.29 + `unit_loadouts.json` (Intercessor `000001157` only).** Intercessor Sergeant grenade-launcher toggle in its own block, sharing one unit-wide per-5 pool with the body stepper (max 1 @ size 5, 2 @ size 10; Sergeant draws first, body ceiling shrinks accordingly). Bolt-rifle prerequisite coupling per D64. New general renderer primitives `pool_id` + `requires_weapon` (see D64/D65). Engine math and prereq coupling verified against real data; render behaviour confirmed by Ryan in the live app (all cases pass). `000001157` is hand-authored, so this was a hand-edit + the general renderer capability — no parser rule was needed (Intercessor is the only onboarded unit with the generic-"model" wording).

## D66 — Any-number-family parser: named-model scope + compound weapons

**Context.** The banked "any number / all models / up to N" bug turned out to be four issues, not one. Investigation with the full prune-correct chain (which reproduces committed exactly) confirmed the shape before any change.

**Decisions.**
1. **Tail fix.** The shared "replaced with" tail now consumes the space (`\s+`) and tolerates a trailing period, matching the sibling classifiers. This is the one-char bug the item was banked for.
2. **Named-model scope (new, not in the original banked note).** The scope regex previously required the literal word *models*/*units*, so "Any number of **Sternguard Veterans**…" never matched — including the marquee combi-weapon case. The classifier now captures whatever sits between the lead-in and "can … have their" and resolves it as a model group by word-overlap. "models"/"units"/"the models" still map to the body group. This is what actually clears Sternguard and ~16 other named-model SM/DG units.
3. **Compound replacement** ("replaced with 1 A and 1 B") splits on count-led " and " into a `" + "` name; the engine already splits replacements on `" + "` (adds each weapon).
4. **Compound source** ("A and B replaced with …") splits on " and " **guarded by an exact whole-name check first**, so genuine "and"-named weapons ("Teeth and claws", "Crozius arcanum and power weapon") are kept whole and are **not** shattered — this is the guard that prevents the earlier regression that dropped `000003873` to 0. Compound sources are stored as a `" + "` source string.
5. **Engine (index.html) — compound source removal.** The rollup now splits `replaces` on `" + "` so every named source weapon is decremented on each swapped model, while the swap still counts **once** per model against the model-group pool (a compound source is one swap, not two). Single-source behaviour is unchanged. Verified with an isolated math harness (compound src+repl, single-source regression, choice-replacement that re-adds a source weapon, and over-allocation counting once).

**Scope / results.** 27 SM/DG units gain correct options; deep-diff vs committed shows only those 27 changed, **zero units lost options**, zero units added/removed. `000003873` stays at 2 options with its compound source intact.

**Still deferred (surfaced, visible flags — not silent corruption).**
- **Shields / totems as swap parts** (storm shield ×4, death totem ×2) — the D63 equipment-in-weapons limitation (queue item 5). The weapon side of each swap resolves; the equipment side is flagged, not removed.
- **"Centurion assault launcher"** — the replacement weapon is genuinely absent from `units.json` for that datasheet (a missing-weapon data gap, not a parser fault). Title-cased + flagged.
- **Verb/format variants** still UNMATCHED: "replace their X with Y" (Kill Teams), possessive "…bolt pistols can each be replaced", "**1** of the following" (vs "one"), "replaced one of the following" (missing "with"), the "one 1" source typo. These are a separate parser track.
- The pre-existing "1 of the following" leader mis-parse on Wolf Guard Terminators `000000318` (garbage choice string) is unchanged by this work and belongs to the variant track above.

**Ships as:** `loadout_parser.py` (classifier + build_loadout), `index.html` **v5.30** (rollup), regenerated `unit_loadouts.json`. Configure-pane render of the new compound options needs Ryan's live eyeball (the compound labels render as "A + B" text).

## D67 — Any-number swap caps + per-source-weapon pool

**Problem.** After D66 the any-number swaps matched and rendered, but every stepper showed **max 0** — unusable. `loMaxCount` returned 0 for `max_total_all` options because they carry no `max_total`.

**Decisions.**
1. **Cap is rules-derived, not a product choice.** "Any number"/"All" → the swap ceiling is the scoped model group's count (all eligible models). "Up to N" → `min(N, group count)`. The parser now captures the N from "Up to N" (`up_to`), previously discarded. `loMaxCount(opt, size, groupN)` resolves `max_total_all` to `groupN`, or `min(up_to, groupN)` when `up_to` is set. Two SM/DG units needed the N enforced: Devastator (4) and Deathwatch Terminator (3).
2. **Pool is per source weapon, not a summed total.** Wiring the caps exposed that the group pool summed *all* body swaps, so a unit with two independent swaps (e.g. Sanguinary Guard: blade→spear and boltgun→pistol on the same models) would falsely warn "too many." A model may swap each weapon it carries once, so the binding limit is per source weapon. The rollup now flags over-allocation when any single source weapon is swapped more than the group has models, and reports the most-consumed source as "X of N models." This also correctly couples swaps that share a source (e.g. a compound special weapon and a chainfist swap both consuming the power fist). Weapon-count output is unchanged; only the indicator and over-flag were corrected.
3. **Stale flag removed.** `REVIEW_MAX_TOTAL` is dropped — the cap is now resolved, so the flag was misleading.

**Verified.** 8 cap cases + 4 rollup cases (independent dual swap not over, competing same-source over, up-to clamp, single-swap regression) pass in an isolated harness. Loadout regen: 217 units, none lost; only the 2 Up-to-N units change (gain `up_to`).

**Separately surfaced (not a cap issue).** Crusader Squad shows "0 of 0" because it has **no points object → no size selector → size defaults to 1**, and its fixed Sword Brother consumes that one model. This is the missing-points onboarding gap (D61 track); caps can't help until it's sized. Same class as the Black Templars Sternguard re-print.

**Ships as:** `loadout_parser.py` (`up_to` capture), `index.html` **v5.31** (`loMaxCount` + per-source-weapon pool), regenerated `unit_loadouts.json`. Configure-pane behaviour needs Ryan's live check.

## D68 — Any-number swaps get their own heading; live-test gaps banked

**Change (shipped).** Any-number/up-to-N swaps were all labelled "Special Weapon", so distinct swaps stacked under one heading. They now take a source-derived heading (e.g. "Power Fist Options", "Storm Bolter Options"); per-N replacements keep "Special Weapon" (that IS the datasheet's special-weapon slot). This separates Terminator's chainfist from the special-weapon list, and renders Deathwatch Terminator's two rule groups (storm-bolter→heavy weapons up-to-3; power-fist+storm-bolter→melee any-number) as two distinct groups. Cosmetic only — `group` drives just the sub-heading; no rollup/keying logic uses it. Regen: 217 units, none lost; the only non-label delta from the prior state is the two up-to-N units' `up_to`. Ships as `loadout_parser.py` + regenerated `unit_loadouts.json`, `index.html` bumped to **v5.32** (version constant only, to cache-bust the new JSON).

**Banked from live testing (not fixed here).**
- **Devastator Sergeant options** — the datasheet line is "…can be replaced with two different weapons from the following list." This "pick two DIFFERENT from a list" combinatorial form is unmodelled (distinct from the any-number family). The Sergeant model group exists; it just has no parsed options. Separate parser track.
- **Sanguinary banner** — "One model can be equipped with 1 Sanguinary banner." The add classifier only matches "This model/unit…", not "One model…", and the banner is equipment, not a weapon, so it also needs the weapon-vs-equipment add path. Banked.
- **Sanguinary Guard / Crusader points + size selector** — no points object ⇒ no size bracket selector (Sanguinary should offer 3/6). Missing-points onboarding gap (D61 track), not a loadout bug.

## D69 — Points join normalized; units.json reproduction chain established

**Problem.** 8 Death Guard units (active faction) and 7 Space Marines units had no
points despite the values existing in the MFM source. Root cause: the MFM parser
title-cases ALL-CAPS names, producing "Daemon Prince **Of** Nurgle" and
"Foetid Bloat-**Drone**", which never match Wahapedia's casing on the exact-string
points join in `convert_to_json`. Names with "of"/"with"/hyphens broke; others didn't,
which made the gap look random.

**Decision.** Normalize the points-join key (casefold + collapse whitespace) as a
fallback after the exact match — fixes the whole casing class at once. Chosen over
fixing the parser's casing because Wahapedia's casing (lowercase "Bloat-drone") can't
be derived by any title-case rule; the display name comes from units.json, so
normalizing the *match* loses nothing. 15 units recovered correct points; strict diff
showed only those 15 changed.

**Reproduction chain (new).** Verified for the first time that
`wahapedia_transform` (per faction) + MFM points + `convert_to_json` + `merge_factions`
reproduces the committed SM (181) and DG (36) blocks exactly — no hidden manual edits.
Chaos Daemons is the Gen-1 hand-built block, carried through merge unchanged (not
regenerable by the Gen-2 pipeline, by design). This is the durable outcome: units.json
data fixes can now be shipped the way loadout fixes already are.

**Ships as:** `convert_to_json.py`, regenerated `units.json`, `index.html` v5.34.

## D70 — Per-model keyword split, wargear abilities, per-datasheet ability text

**Change 1 — keywords split three ways.** The keyword builder read only the keyword
text, dropping the source `model` and `is_faction_keyword` columns, so faction and
model-specific keywords were smeared unit-wide. Now: all-models keywords → pills
(`Keyword Names`); faction keywords → `Faction Keyword Names` (rendered "Faction: X");
model-specific → `Model Keyword Names`, encoded "MODEL: kwA, kwB | MODEL2: kwC". Model
scope reaches ~148 datasheets, faction all of them. Faction kept distinct for the
legality tie-in (D0).

**Change 2 — wargear abilities.** Default (non-optional) gear that confers an ability
(Refractor Field 5+, Storm Shield 4+) was routed to the glossary but never attached to
the unit. `type=Wargear` abilities are now recorded per datasheet and rendered in a
Wargear Abilities section. Reaches ~297 datasheets.

**Change 3 — per-datasheet ability text (B1).** The ability-description lookup was
keyed by name alone, so 198 ability names that carry different text across datasheets
(Narthecium, Honour or Death, …) showed one arbitrary version everywhere — the
Ravenwing variants leaked onto Sicarius and the Apothecary. Fix: `wahapedia_transform`
emits `Unit_Ability_Details.csv` (datasheet_id, name, description) with each
datasheet's own text; `convert_to_json` attaches `unit_ability_details` (name→text) to
each unit; both popups resolve an ability's description from the unit's own text first,
falling back to the global glossary.

**Render (index.html).** v5.34 added the three keyword blocks + Wargear Abilities to
`buildModalFull`; v5.35 ported them to `buildModalConfigured` and fixed the doubled
`++` on SV/LD in the shared stat table; v5.36 wired per-unit ability text into both.

**Verified.** Strict diff vs live after each change: only the intended fields changed,
zero regressions, CD untouched.

**Ships as:** `wahapedia_transform.py`, `convert_to_json.py`, regenerated `units.json`,
`index.html` v5.34→v5.36. New intermediate file: `Unit_Ability_Details.csv`.


## D71 — Unit classification from shared + namesake keywords; Leader/Character promotion (B8)

The left-panel `unit_type` classifier flattened every keyword row for a datasheet
into one set, ignoring each keyword's `model` column, so a keyword carried by only
one model in a multi-model unit promoted the whole unit. Victrix Honour Guard read as
Epic Hero (that keyword sits on its Chapter Ancient / Chapter Champion models, not the
unit body); Ravenwing Command Squad's model-specific Character was masked by its
unit-wide Mounted.

**Fix (`wahapedia_transform`, `unit_type`).** Classify from the union of the unit's
all-models keywords and the keywords of its *namesake* model — a model whose name
matches the unit name, either direction (e.g. "Grimaldus" ⊂ "Chaplain Grimaldus",
"Wolf Guard Headtakers" = "Wolf Guard Headtakers"). Faction keywords are excluded.
Priority: Epic Hero → Character → (Fortification, Vehicle, Monster, Beast, Mounted) →
Battleline (role) → Infantry → role fallback.

**Character promotion, two sources, both above the body keywords.** (a) A whole-body
Character keyword — a single-model unit, or a keyword on the all-models line — so a
Daemon Prince / Great Unclean One is a Character that *also* happens to be a Monster
(monster rules still apply; it just lives under Characters). (b) The Leader ability,
which catches multi-model attach-characters whose Character keyword sits on only one
model (Ravenwing Command Squad, Chaplain on Bike). A model-specific Character keyword
on a *subset* of a multi-model unit does **not** promote — that was the original bug.

**Net effect** (strict diff vs live: only `unit_type` changed, zero collateral, CD
untouched): Victrix Honour Guard Epic Hero → Infantry; Ravenwing Command Squad &
Chaplain on Bike Mounted → Character (Leader); Daemon Prince of Nurgle (both forms) &
Great Unclean One Monster → Character (whole-body Character keyword). Grimaldus stays
Epic Hero and Wolf Guard Headtakers stays Infantry (both via namesake model); Wardens
of Ultramar stays Epic Hero (all-models).

**No override table.** The namesake rule plus the Leader signal cover every current
SM+DG multi-model case; a curated override is deferred until a real unit forces one.

**Ships as:** `wahapedia_transform.py`, regenerated `units.json`, `index.html`
v5.36→v5.37.


## D72 — Heterogeneous fixed-group split (B9)

A model group of N is assumed uniform — every model carries the group's
`default_weapons`, and the rollup emits each weapon × N. That breaks when a
datasheet gives *different* weapons to individual models via repeated singular
composition lines ("One Company Veteran is equipped with … master-crafted heavy
bolter" / "One … master-crafted bolt rifle"). Unioned into one 2-model group, both
master-crafted weapons doubled to ×2.

**Fix (`equipped_parser`).** When a fixed-N group receives exactly N singular
("One <model>…") equip lines and has no options scoped to it, split it into N
one-model sub-groups, each carrying only its own line's weapons, named
"<singular base> (<distinguishing weapon>)" — e.g. "Company Veteran (Master-crafted
heavy bolter)". Shared weapons (bolt pistol, close combat weapon) then sum back to
×2 across the two sub-groups while each distinct weapon stays ×1.

**Display.** Make-up now shows one line per distinct model loadout instead of a
single "×N" line — accepted trade-off (the "×2" line was hiding the difference).

**Guard / blast radius.** Fires only when the singular-line count equals the group's
fixed N and the group carries no scoped options, so option-bearing or partially
specified groups are left alone. The "One X is equipped with…" pattern appears
exactly twice across all of SM+DG — both on Company Heroes' Veterans — so this is
the only unit affected. Strict diff vs committed: 1 of 217 loadout entries changed.

**Ships as:** `equipped_parser.py`, regenerated `unit_loadouts.json`, `index.html`
v5.37→v5.38.


## D73 — Bundle / loadout integration and the compound-swap control model (B5, B6)

Two option systems coexist: hand-authored **bundled_swaps** (in units.json, for
compound/atomic mutually-exclusive swaps and the only carrier of grants such as a
relic shield's stat override) and parser-generated **loadout options** (in
unit_loadouts.json, for simple single-weapon swaps). They did not compose. The
detail panel rendered *either* a unit's loadout options *or* its bundle, never both,
so a loadout-defined unit that also owned a bundle (the Captain) never showed the
bundle at all — the user only saw the parser's broken duplicate options, and the
bundle's relic-shield grant (and its `{W:'7'}`) was dead code. On top of that, the
loadout weapon rollup ignored bundle add/remove, and the stat override was only
reachable through the un-rendered bundle UI.

**Integration (index.html).**
- The loadout weapon display now folds in the chosen bundle endpoint's add/remove,
  so a bundle choice actually changes the weapons shown on a loadout-defined unit.
- A loadout-defined unit that owns a bundle now renders the bundle picker + grants
  alongside its loadout options.
- Loadout options whose weapon slot the bundle owns are suppressed (and any stale
  selection cleared) so there is a single control per slot.

**Control model — `loadout_relation` on each bundle.** `owns` (Captain): the bundle
is the sole control for its slots; those loadout options are always hidden. `alternative`
(Lieutenant's atomic 3-for-3): the per-slot loadout swaps stay available, and the
bundle's non-default endpoint hides them only while it is selected. That single flag
delivers cross-exclusivity for free — picking the atomic swap hides and clears the
three per-slot swaps; clearing it restores them — with no separate reverse-lock,
since selecting the atomic always wins and the per-slot controls simply aren't shown
while it is active. `convert_to_json` passes `loadout_relation` through into units.json
(default `owns`, preserving prior bundle behaviour).

**Broken-compound drop.** A loadout choice whose replacements resolve to no real
weapon profile is a compound the parser couldn't express; it is dropped. This removes
the Lieutenant's mangled `sng_2` ("neo-volkite + power weapon + storm shield" crammed
into a bolt-pistol swap) now that the bundle owns that swap.

**Units.** *Captain* — the ten-endpoint bundle is the single control; choosing the
relic-shield endpoint swaps the three base weapons for heavy bolt pistol + master-
crafted power weapon, surfaces the Relic Shield ability, and drives Wounds to 7. This
also closes the B12 relic-shield case. *Lieutenant* — authored an `alternative`
bundle: default plus the atomic that removes bolt pistol / master-crafted bolter /
close combat weapon, adds neo-volkite pistol + master-crafted power weapon, and grants
a storm shield (INV → 4+).

Regen diff: only the Lieutenant changed in units.json (gained `bundled_swaps`).

## D74 — Stat-line INV/FNP overrides; configured popup made selection-aware

**INV/FNP overrides.** The shared stat table honored overrides only on SV and W. It
now applies them to INV and FNP as well, so the storm-shield grant drives INV to 4+
the way the relic shield drives Wounds. An override replaces the cell and its
condition text; the value is stored bare and rendered with a trailing `+`.

**Configured popup Wargear Abilities — selection-aware.** The configured popup listed
every *possible* wargear ability on the datasheet, regardless of what the built unit
actually had (so the Captain showed "Relic Shield" even on the default loadout). It
now shows only abilities the build actually confers: always-on gear abilities, plus
grant-conferred ones whose grant is currently chosen. Abilities tied to a bundle
grant are treated as optional and hidden unless active. The left-panel
(available-unit) popup is unchanged and still lists all possibilities — that view is
the datasheet reference. Side effect: authoring the Lieutenant's storm-shield grant
made its "Storm Shield" ability selection-aware too (it previously showed always).

## D75 — Captain relic-shield W correction; general characteristic-from-text reader; Shining Aegis de-hardcoded (B12 remainder)

**Captain relic shield: W 7 → W 6 (bug fix).** Last session the foot Captain's
(datasheet `000000073`) relic-shield grant was authored with a Wounds override to 7.
The authoritative Wahapedia ability text and the SM faction pack both set that shield
to **Wounds characteristic of 6** (base 5 → 6). W 7 belongs only to the *Wolf Lord on
Thunderwolf* (`000000284`) and *Captain on Bike* (`000002702`), both base W 6 → 7 —
the wrong variant's value was picked up. Corrected at source in `bundled_swaps.json`
(`carrier_notes` and `stat_override`), regenerated the SM block, diffed: only the two
Captain lines changed across the whole `units.json`.

**General characteristic-from-text reader (B12 remainder, the "b" of the c-then-b
plan).** Replaced per-effect hardcoding with a reader that parses a wargear/ability's
rules text into a stat override: `N+ invulnerable save` → INV, `Wounds characteristic
of N` → W, `Save characteristic of N+` → SV, `Feel No Pain N+` → FNP. Wired into two
active sources: bundle-grant `carrier_notes` (an authored `stat_override` still wins,
as an escape hatch), and active weapon/wargear abilities via the weapon-ability
glossary. Validated against the full SM+DG+CD corpus: reader parses every real
characteristic text correctly; on the wired cases reader-derived equals authored
(Captain W 6, Lieutenant INV 4).

**Shining Aegis de-hardcoded.** The former JS special-case (`if shiningAegisActive
overrides.SV = 3`) is gone; the Keeper of Secrets' Shining aegis shield now drives
Sv 3+ through the reader like any other characteristic wargear.

**Scope guard — the weapon/wargear path skips the broad surface.** The active-wargear
reader deliberately ignores any ability already surfaced via `wargear_ability_names`
(Storm Shield, Shield Dome, Watcher in the Dark, Helix Gauntlet, …). Those conferred
always-on abilities are the "broad" pass, deferred to its own item with an E17
asterisk for the bearer-only/conditional cases — applying them here would double-apply
or mis-apply a per-model or once-per-battle effect to the whole-group statline.
Finding that motivates the guard: the reader matches the phrase even inside a
conditional clause (e.g. the Lion Helm and Watcher in the Dark both contain a summoned
"Feel No Pain 4+"), so the broad pass must add a *conditional/bearer* guard before it
can safely write those to the statline.

---

## D76 — B14: optional per-model wargear items routed to Other Options

**The problem.** "1 X can be equipped with 1 Y" adds (e.g. the Infiltrators' helix
gauntlet) were landing in Wargear Options shaped like weapon swaps — `weapon_replaced`
null, the item name carrying a footnote asterisk (`helix gauntlet.*`), no toggle the
UI could render meaningfully. Separately, the item's ability was pinned to the unit's
always-on `wargear_ability_names` surface, so an *optional* item read as if the unit
always had it.

**The fix (transform).** `parse_options` now discriminates a wargear ITEM from a
weapon add: an add that resolves to no weapon profile but matches a type=Wargear
ability name is routed to Unit_Other_Options (option name = the proper ability name,
asterisk stripped, max-per-unit from the "1 Y" count) and its ability name is
subtracted from that unit's always-on wargear surface — it now confers only when the
option is checked. Weapon adds (Hunter-killer missile, Storm bolter, …) are untouched.

**Exclusion groups.** An item-only "one of the following" list (Corvus Blackstar's
auspex array / infernum halo-launcher; Spectrus' helix / comms) emits as a
mutually-exclusive Other-Options group. Two independent single adds on one unit
(Infiltrators' helix + comms) stay independent checkboxes.

**Stat conferral, guarded.** The transform copies the item's ability text into
`carrier_notes` only when it is an *unconditional* set-value phrase; a set-value that
sits inside a conditional/summon clause is blanked. So a checked Helix Gauntlet drives
Feel No Pain 6+ through the existing reader, while Watcher in the Dark (summoned FNP
4+) carries no reader text and confers nothing here. This is a narrow guard on the
option path only; the broad always-on surface still awaits B15's full guard.

**App (v5.43).** Checked Other Options feed the statline reader via their
`carrier_notes` (`activeOtherOptionOverrides`); options sharing an `exclusion_group`
behave as a radio (turning one on clears its group-mates).

**Scope this pass.** SM faction only. Regenerated SM block; diff = exactly 8 units
(Infiltrator Squad, Incursor Squad, Reiver Squad, Sanguinary Guard, Corvus Blackstar,
Deathwing Terminator Squad, Deathwing Knights, Spectrus Kill Team), each moving its
item(s) to Other Options and shedding them from the always-on surface; no stats,
weapons, points, or bundles changed. DG (Deathshroud's icon of despair) and CD
(Plaguebearers/Plague Drones icons) will convert when those factions are next
regenerated — CD is Gen-1 hand-built and won't, so its icons stay as-is by design.

**Carved out — B14b.** A wargear-item add inside a group that *also* contains weapon
systems (Impulsor's group C: shield dome + orbital comms array alongside two weapon
arrays) needs cross-channel mutual-exclusion between Wargear Options and Other
Options, which we don't model yet. The whole group is left in Wargear Options
untouched rather than emit half an exclusive set.

## D77 — B14 render wiring corrected; other-option / loadout de-dup; weapon-count root cause found

**The B14 gap.** B14 (D76) added optional wargear items to `other_options` in the data,
but the app never surfaced them for loadout-defined units. The config-pane dispatch
rendered Other Options for a loadout unit *only if that unit also owned a bundle*, so
loadout units whose only extras were `other_options` (no bundle) silently dropped them.
Infiltrator Squad showed nothing but unit size; Corvus Blackstar showed its weapon
swaps but not Auspex/Infernum. Data was correct; the render path was the fault.

**Fix (v5.44).** Pulled the `buildOtherOptionsHtml` call out of the bundle guard in the
loadout branch: loadout-defined units now render Other Options whenever they have any
(or have active bundle grants). The bundle picker stays gated on bundle presence, so the
Captain path (loadout + bundle + relic-shield grant) is unchanged. App-only; restored
Other Options for the 8 B14 units.

**De-dup (v5.45).** v5.44 exposed a double-sourcing: Watcher in the Dark exists both as a
loadout option group *and* as a B14 `other_option` on Deathwing Terminator Squad and
Deathwing Knights, so it rendered twice. The loadout group is canonical, so
`buildOtherOptionsHtml` now suppresses any `other_option` whose name matches a loadout
group label (normalized). Contained to those 2 units; the other 6 B14 units are
untouched. The deeper cleanup — stopping the B14 transform from emitting an other-option
that duplicates a loadout group — is banked for the next relevant regen.

**Weapon-count root cause (diagnosed, fix banked as B16).** The configured popup showed
impossible weapon counts (Deathwing Knights: Great weapon ×5 + Mace ×3 + Power weapon ×2
= 10 on a 5-model unit). The rollup engine is correct; the inputs are wrong.
`loadout_parser.py` assigns the *full* base-weapon set to *every* model group
(`g['default_weapons'] = base_ws`, a documented shortcut ~line 521/785), so a unit whose
groups carry different weapons (Knight Master's Great weapon vs the Knights' Mace) gets
every model credited with every weapon. The per-model assignment exists in the source —
the datasheet `loadout` prose ("The Knight Master is equipped with: X. Every Deathwing
Knight is equipped with: Y.") — so the fix is to parse that prose and partition base
weapons per model group. This also clears the false-positive noise (Sergeant pistol +
primary, vehicle multi-guns, weapon profile-variants), because the prose is authoritative
per group. Requires a loadout regen scoped to all 13 loadout-defined factions (CD has 0
loadout-defined units and is unaffected) plus validation across all multi-group units.
Fix parser, not output.

## D78 — B16 shipped: per-model-group default weapons (weapon-count fix)

**Where the fix actually landed.** The Session-22 diagnosis pinned the weapon-count bug
on `loadout_parser.py` and proposed teaching it to read the datasheet `loadout` prose.
On inspection that partition already exists — in `equipped_parser.py`, which reads
"... is equipped with:" prose and writes per-group `default_weapons` as an override over
loadout_parser's flat baseline. The real defect was its **input**: the source is the
hand-pasted `*_web.txt` composition dumps, and those are incomplete. `Dark_Angels_web.txt`
is 72 lines and contains no Deathwing units at all, so 19 multi-group units never got
partitioned and kept the flat all-groups defaults (the Deathwing Knights "10 weapons on 5
models" symptom). So B16 became a source fix, not a new parser.

**The fix.** Added a Datasheets.csv `loadout`-column adapter to `equipped_parser.py`
(`loadout_lines_from_datasheets`, `--datasheets` flag). It turns each
`<b>Subject is equipped with:</b> weapons` clause into the same per-clause equipped line
`segment()` would have produced, then feeds the existing partition machinery unchanged.
It is a **gap-filler only**: it skips any unit already covered by a web.txt pass
(`_defaults_source == 'equipped'`) or present in the current pass's `owner_lines`, and only
touches multi-group units (single-group units are already correct — flat == the one group).
Web.txt therefore takes precedence and nothing that was already partitioned moves.

**Result.** Exactly 19 units changed vs the committed file; the 115 web.txt-covered units
diff zero. Eight units got real per-group trims (Deathwing Terminator Squad, Deathwing
Knights, Wolf Scouts, and partial fixes on Spectrus / Fortis / Indomitor / Talonstrike /
Decimus Kill Teams). No group's weapon count increased anywhere (regression-checked
per group). Deathwing Knights now reads Great weapon of the Unforgiven on the Knight Master
alone and Mace of absolution on the four Knights.

**Known partials (banked to B17).** The Deathwatch Kill Teams model each weapon variant as
its own optional `0-N` model group. The base groups now partition correctly, but the
`"...with <weapon>"` variant sub-groups don't match a plain group name, so they retain the
flat baseline (unchanged from before, not a regression). Talonstrike (all clauses carry a
"with Jump Pack" qualifier) and Decimus (per-N "For every 5 models" clauses) are partials
for the same reason. These need a variant-group / per-N default rule — out of B16 scope.

**Reproduction change.** The final `equipped_parser.py` pass now takes
`--datasheets Datasheets.csv`. Run the five web.txt passes first (no `--datasheets`),
feeding each output into the next `--loadouts`, then a final pass with `--datasheets` to
gap-fill. CD carries verbatim (0 loadout-defined units, never entered the file).

**App unchanged.** Data-only fix; the rollup engine was already correct. `index.html` stays
v5.45. The configured-popup render still needs Ryan's eyeball on Deathwing Knights (DOM not
visible in build env), but per-group inputs are now correct.

---

## D79 — B17 (part 1): loadout option-parser gaps closed for the Deathwatch/Deathwing partials

**Decision.** Widen `loadout_parser.py` to recognise three option-sentence shapes it
previously left UNMATCHED, and route non-weapon wargear items added by name as equipment
rather than flagging them as missing weapons. Data-only against existing app support;
`index.html` stays v5.45.

**What changed in the parser.**
1. **Per-N clauses generalised.** `classify_per_n` now accepts "in **the** unit" as well
   as "in **this** unit", an optional "up to N" lead-in, and **active voice**
   ("… N model can replace its X with …") alongside the existing passive
   ("… X can be replaced with …"). This closes Decimus (four "For every 5 models in the
   unit, up to 1 model's X can be replaced with …" clauses), Talonstrike's per-N
   heavy-bolt-pistol swap, and the Deathwing Terminators' per-5 storm-bolter swap.
2. **Active-voice definite swap.** New `classify_active_swap` handles
   "The/This `<model>` can replace its X with one of the following: `<list>`" (and the
   single-replacement form). It is deliberately limited to the **definite** lead-in
   (The/This), which scopes to a named single model — the sergeant/leader group — where a
   plain choice is exactly right. This closes the Talonstrike and Fortis sergeant swaps
   (the "…with Jump Pack" qualifier resolves correctly via word-overlap scoring).
3. **Active-voice "any number / all".** `classify_any_number` now also matches the active
   "… can each replace their X with …", mirroring the passive "have their X replaced with".
   This closes the Talonstrike plasma-exterminator, Fortis superkrak, and Spectrus
   las-fusil / combat-knife clauses.
4. **Equipment add.** A by-name add that fails weapon lookup but matches a known
   wargear-ability item (allowlist built from `weapon_abilities.json`) is emitted as an
   `equipment` add with no flag. This clears the Deathwing Terminators' "This unit can be
   equipped with 1 Watcher in the Dark" WEAPON_NOT_FOUND.

**Choice-list hygiene.** A trailing rules note in parentheses is stripped before a
"one of the following" list is split (so "… 1 cyclone missile launcher (this model's storm
bolter cannot be replaced)" yields the compound "storm bolter + cyclone missile launcher"
choice cleanly), and stray list punctuation ("frag cannon.") is trimmed in `qty_name`.

**Explicitly banked (not shipped) — deeper shapes, surfaced not half-done.**
- **Indefinite single-model swap.** "One model / 1 model can replace its X with 1 Y"
  (Fortis vengor, Spectrus instigator) needs a **1-model cap**; emitting it as a plain
  choice would wrongly let the whole body swap. Left flagged pending a bounded shape.
- **Conditional per-model scope.** "One model equipped with a `<weapon>` can …" (Fortis,
  Spectrus) is a requires-weapon-gated swap — a distinct shape reusing the existing
  `requires_weapon` machinery. Left flagged.
- **Variant sub-group DEFAULT weapons (true 1b).** The Deathwatch "…with `<weapon>`"
  optional model groups still carry the merged weapon list as their default. That fix lives
  in the default-partition path (`equipped_parser.py`), not the option classifier, and is
  entangled with how those variants are modelled from composition — its own scoped pass.
- **Sanguinary banner + 3/6 selector** (D-queue), untouched this session.

**Scope of the shipped change.** Exactly five units changed vs the committed file —
Talonstrike (3→0 flags), Decimus (4→0), Deathwing Terminator Squad (2→0), Fortis (5→3),
Spectrus (4→2) — and only their `options` / `_parser_flags`. Every unit's `model_groups`
(including the B16 per-group `default_weapons`) is byte-identical to the committed file;
the equipped-pass chain reproduces the new file with zero diff (still a fixed point); CD
carried verbatim. All three new option shapes already exist in the committed data and are
rendered by the app, so no `index.html` change was needed.

**How the fix was applied to the preserved file.** `loadout_parser.py` preserves existing
entries, so the five targets were stripped from the `--existing` input, re-parsed with the
widened classifiers, and their fresh `options` / `_parser_flags` spliced back over the
committed entries — `model_groups`/`default_weapons` kept from the committed (B16) file so
no default drift. Fix parsers, not output: the classifier changes are the durable artifact;
the splice is just how they reach the already-bootstrapped file.

## D80 — B17 (part 2): the banked single-model / conditional-swap shapes

**Context.** Part 1 (D79) cleared the bulk of the Deathwatch kill-team option gaps but
banked two shape families that needed bounded handling: the **indefinite single-model
swap** ("One model / 1 model can replace its X with 1 Y" — a plain choice would let the
whole body swap) and the **conditional per-model scope** ("One model equipped with a
`<weapon>` can …" — a requires-weapon gate). Five flags remained: Fortis ×3, Spectrus ×2.

**Decision.** Widen `loadout_parser.py` to emit both families with existing option
fields — no new schema, no `index.html` change:
- **Indefinite single-model swap → `count` + `max_total: 1`.** A new `classify_one_model_swap`
  matches the bare "One/1 model can replace its X with N Y" form and caps it at exactly one
  model. `max_total` was already returned by the render/rollup cap function and enforced, so
  the shape rides existing machinery. Chosen over a new cap field or reusing `up_to`
  (`up_to` pairs with `max_total_all` for *group-eligible* caps — wrong semantics here).
- **Conditional per-model scope → existing `requires_weapon`.** The per-5 add form
  ("For every 5 models… 1 model equipped with a `<weapon>` can be equipped with …") is now
  handled inside `classify_per_n` (previously bailed on "equipped with a"); the conditional
  single-model replace form is handled by `classify_one_model_swap`. Both carry
  `requires_weapon`. The gate is **live on the add path** and **dormant on the count path**
  (the count rollup does not yet consult `requires_weapon`) — the count-gate activation is
  the banked engine turn. It is encoded now as faithful intent; in both flagged cases the
  gate has no same-scope choice that could disable it, so nothing is falsely blocked.

**Sequencing (dev-manager call).** Four of the five flags are tractable as a data-only pass
that stays a verified fixed point; the fifth — Spectrus "one of the following" helix/comms —
is an **exclusive choice between two equipment adds on one model**, which the current
shared-pool cap (seeded only from `per_n_models` members) would not bound, and which needs a
render-side pool-remaining check plus count-gate activation. That is deliberately isolated
into its own **engine turn** (next), so a risky change to the tested rollup hot path lands
without a data change muddying the bisect. This pass ships the four; Spectrus keeps one
banked flag, explicitly scoped.

**Real-data catch.** The grenade-launcher add first normalised to the `– frag` firing
profile (multi-profile weapon; the index returns the first profile row), which would confer
only frag and drop krak. Corrected with a `base_display` helper that strips the ` – profile`
suffix for option-facing weapon names, matching the hand-authored reference (Intercessor
Squad's grenade launcher uses the base name). Applied to `adds_weapon` and to
`requires_weapon` (so the dormant gate names the base weapon, not a profile).

**Scope of the shipped change.** Exactly two units changed vs the committed file — Fortis
(3→0 flags) and Spectrus (2→1) — and only their `options` / `_parser_flags`. Both units'
`model_groups` (incl. B16 per-group `default_weapons`) are byte-identical to committed; the
equipped-pass chain reproduces the new file with zero diff (still a fixed point); CD carried
verbatim. `index.html` unchanged (still v5.45). Applied via strip-from-`--existing` →
re-parse with widened classifiers → splice fresh `options`/`_parser_flags` over committed.

## D81 — B17 (engine turn): count `requires_weapon` gate + `max_total` pool cap; Spectrus helix/comms

**What.** The tested `loRollup` hot path (`index.html`) gains two mechanisms and Spectrus's
last banked flag is cleared. `index.html` bumped **5.45 → 5.46** (engine edit). No data change
landed alongside the engine edit except the Spectrus splice, which is its own verified fixed
point — so a regression here bisects cleanly to one file at a time.

**1. Count `requires_weapon` gate activated.** The `add` path already consulted `reqOk`
(engine) and `reqOkUI` (render); the `count` path did not. The count rollup loop now skips a
gated-off `count` (emits nothing, charges no source weapon), the render clears any stored
count when its bearer weapon is gone, and a gated-off count shows a disabled
"`<replacement>` — needs `<weapon>`" row (mirroring the add radio). This makes the Fortis
plasma-pistol gate (`requires_weapon` "Plasma incinerator", encoded in part 2) live. It stays
harmless in-app today: no same-scope choice removes the Plasma incinerator, so nothing is
falsely blocked — the wiring is what changed, not any current selection outcome.

**2. Shared-pool cap seeded from `max_total`.** `poolCap` was seeded only from `per_n_models`
members, so a pool whose members all use `max_total` got no cap and couldn't lock its members
against each other. It is now also seeded from `max_total` members — bounded by the largest
member `max_total`, with `per_n_models` members keeping precedence when a pool mixes both.

**3. Spectrus helix/comms — exclusive one-model equipment choice.** New `loadout_parser.py`
classifier `classify_conditional_add_choice` handles "One model equipped with a `<weapon>` can
be equipped with one of the following: …". It emits one capped `add` per list item
(`max_total:1`), all sharing one `pool_id` (assigned per sentence in `build_loadout`) and each
carrying `requires_weapon`. On Spectrus this yields Helix Gauntlet + Infiltrator Comms Array as
two equipment adds, shared pool (cap 1) → picking one locks out the other; both vanish if the
Deathwatch marksman bolt carbine is swapped away. Spectrus now carries **0 flags**.

**Shape choices made (mechanism, dev-manager call).**
- Pool-cap aggregation for a `max_total`-only pool = **max of members**, not sum — an exclusive
  "one of the following" choice on one model is cap 1, not 2. `per_n_models` precedence
  preserved so mixed pools keep their defining-member semantics.
- Gated-off count **renders a disabled "needs `<weapon>`" row** (not a live stepper capped at
  0) — consistent with the existing add gate and clearer than a dead stepper.
- Conditional-add scope = **body group** (`_scope_hint:'body'` → Kill Team Infiltrators, the
  bearer of the marksman bolt carbine), not a synthetic single-model group.

**Validation.** Engine behaviors checked on real + synthetic defs: the Spectrus pool caps at 1
(second add locked out); a synthetic count gate suppresses its swap when a same-scope choice
removes the required weapon and restores it when kept. Splice is exactly one unit (Spectrus,
`options`/`_parser_flags` only); its `model_groups` byte-identical to committed; equipped-pass
chain reproduces the new file with zero diff (fixed point); CD carried verbatim. Render states
(disabled "needs" row, pool lock-out radio) are unverified in-DOM — flagged for Ryan's eyeball.

---

## D82 — JSON export / import wired into the UI (data-loss recovery)

**Context.** Saved lists live only in browser `localStorage`; clearing site data wipes them,
which Ryan has already hit. The storage module already carried `exportRecords` /
`importRecords` and the `migrate` hook, but nothing in the UI reached them. This turn wires
them up. No engine or parser change; `index.html` only (v5.46 → v5.47).

**Sequencing note.** These were mechanism/priority calls, not product calls, so they were
decided at the dev-manager level rather than referred to Ryan. All six scoped choices below
were taken as recommended.

**Decisions.**
1. **File shape.** The module envelope (`format: "40kab-lists"`, `schema_version`, `lists: [...]`)
   plus an added `app_version` diagnostic stamp. `schema_version` is what guards import;
   `app_version` is informational only. Export always emits the `lists` array (stable shape),
   even for a single list.
2. **Version mismatch.** Reuse the existing `migrate` hook — older upgrades in place, a
   newer-than-this-build record is refused, not guessed. The UI compares incoming vs surviving
   record counts so a dropped newer-schema list is **surfaced** ("saved by a newer version —
   update the app"), never silently swallowed.
3. **Unknown `unit_id`.** No special import path — persisted as-is; the existing `openList`
   id-first resolve + flag-don't-drop ghost rows handle unresolved units when the list is opened.
4. **Import target.** Every imported record gets a **fresh id** (`newListId`) and `modified: now`
   before `put`, so import can never overwrite a surviving list. Lands as a new home-page row.
5. **Channels.** Both, file-first. Export downloads a `.json` (survives cache-clearing — the
   actual failure) and offers clipboard copy; import takes a file picker and a paste box.
6. **Unit of work.** v1 exports one list per action (current open list from the builder, or a
   single row from home). The envelope already supports many lists, so a "back up everything"
   export is a clean fast-follow without a format change.

**UI.** Builder chrome gains **Export** / **Copy**; each home row gains an export glyph; the
home header gains **Import** (opens a modal with file picker + paste box, error + success lines).

**Validation.** Logic checked in isolation: envelope round-trips (export → import → same
entries), a bare record imports, a newer-`schema_version` record is detected and reported as
dropped, malformed JSON is caught. Concatenated page scripts pass `node --check`. Modal render
and the download/clipboard actions are browser-only — flagged for Ryan's eyeball.

---

## D83 — B17 (true-1b): variant sub-group default weapons (Deathwatch Kill Teams)

**Finding (reframes the banked item).** The Deathwatch "…with `<weapon>`" variant model groups
(Spectrus 3, Fortis 4, Heavy-Intercessor team `000002781` 2 — ten groups total) defaulted to the
whole merged weapon pool instead of their own loadout. Root cause is *not* missing data: the
composition prose already carries a complete per-variant "Every … with `<weapon>` is equipped
with: …" line for every one of these groups. They failed to bind because `match_group`'s
singularizer (`sing_forms`) only normalizes the *trailing* word, while the plural difference here
sits **mid-phrase** ("Intercessor with plasma incinerator" line vs "Intercessors with plasma
incinerators" group). Base groups bound (trailing-word plural), variants didn't. So the fix is a
matcher gap, not merged-list synthesis — the three surfaced design questions (detect variant vs
plain; partition merged list; weapon-not-in-pool) all dissolve: bind the authoritative line and
the existing partition machinery does the rest; an unresolvable weapon still takes the existing
report path.

**Fix (`equipped_parser.py`).** Added `loose_key` (whole-phrase key with every word singularized
via a conservative `_sing_word`: strip one trailing `s`, map `-ves`/`-ies`, leave `-ss`) and a
fallback branch in `match_group`: when the strict matcher returns None, accept a per-word-
singularized whole-phrase equality **only if exactly one group matches** (ambiguity → no match).
Applied to both sides, so non-plural `-s` words (e.g. "occulus") collapse identically and remain
safe. Blast radius is one unit's group set per call.

**Re-derivation (one-time migration).** The affected units were already `_defaults_source:
equipped`, so the standard chain skips them and a plain re-run wouldn't re-touch them. Migration:
strip `_defaults_source` from the three uids in the committed file, run one `equipped_parser`
`--datasheets Datasheets.csv` pass (any composition; gap-fill drives it), which re-partitions all
their groups from prose with the corrected matcher. Result verified: **only** those three units
changed, **only** their ten variant groups' `default_weapons` (base groups, options, flags,
counts byte-identical), every new loadout matches the prose, no stale `default_weapon_counts`.

**Fixed point re-established.** The corrected parser is inert on the *old* committed file (0
diff), and the *new* committed file reproduces under the full standard chain with 0 diff — the
units are `equipped` again and skip cleanly. CD carried verbatim (0 CD units in the file). 218
keys unchanged (217 + `_schema`).

**App / schema unchanged.** Data-only; `index.html` stays v5.47, Data Dictionary v1.5,
`SCHEMA_VERSION` 1. The variant-group config popup render is browser-only — Ryan's eyeball.

---

## D84 — Reiver Squad parser gap: conditional add + unit-wide per-model item adds (S29)

**Context.** Reiver Squad (`000002718`) carried three UNMATCHED parser flags — the only
three across the whole file matching these shapes. All three now classify cleanly;
data-only, `index.html` stays v5.47.

**Two new classifiers (`loadout_parser.py`), placed first in `CLASSIFIERS` so they win, but
non-shadowing by construction: both shapes were UNMATCHED everywhere (nothing else matches
an "If the … is equipped with …" or "All models in this unit can each be equipped with …"
lead), so they only convert UNMATCHED → matched — zero regression risk.**

- **`classify_conditional_add`** — "If the `<model>` is equipped with `<req>`, it can be
  equipped with `<what>`." Emits one capped add (`max_total` 1) scoped to `<model>`, carrying
  `requires_weapon` (quantity stripped via `qty_name` so it normalises to the bare weapon name
  — the gate must equal the token the engine sees). Reuses the existing `requires_weapon` gate,
  which the current engine **honours** (dims/zeros the add when the weapon is absent). Reiver
  Sergeant keeps a combat knife only while holding the bolt carbine.
- **`classify_all_models_add`** — "All models in this unit can each be equipped with 1 `<item>`."
  Emits an `_all_groups` marker op, fanned out in `build_loadout` to one per-model add **per
  model group** (`per_n_models` 1 / `max_per_n` 1), so each group's cap follows its own size
  (Sergeant → 1, Reivers → group size). grav-chute and grapnel are separate rule lines →
  **independent, not mutually exclusive** (a model may take both). Both resolve to known
  equipment in `weapon_abilities.json` → emitted as `equipment` adds, not weapons.

**Decisions made (all reversible/data-only; recommendations taken, noted for veto):**
- **Per-model item add, not pooled** — the rule says "each model can," no unit-wide cap. Fan
  out per group; cap = group size.
- **grav-chute / grapnel independent** — separate lines, no "or" → not exclusive. (Legality
  precedent for unit-wide equipment adds: two independent lines = independent toggles.)
- **Sergeant conditional reuses `requires_weapon`** — exact fit; no new mechanism.
- **"All models" equipment add covers every model group** (incl. the Sergeant). New pattern,
  no prior convention; faithful to "all models."

**Data reached the preserved file via strip-from-existing → re-parse (SM) → splice options,
keeping committed `model_groups`/`default_weapons`/`_defaults_source` byte-identical.** Result:
only `000002718` changed; six options (`cnt_1` unchanged + five new); flags cleared; groups and
defaults intact; full equipped chain reproduces at **0 diff** (fixed point); CD verbatim; 218
keys.

**Finding — systemic, banked (not a Reiver bug).** The scope resolver maps a "body"/"all
models" hint to the **fills-to-size group only**, excluding leader/fixed groups. This is an
established convention across ~30 units' weapon-swap options (e.g. cnt_1's knife→carbine swap
scopes "Reivers", not "Reiver Sergeant"). Consequence for Reiver: the Sergeant cannot currently
*take* the bolt carbine, so the new conditional combat-knife add stays correctly gated-off until
that broader fix lands — safe, not illegal, just dormant-by-data. Fixing "all models → all
groups" generally ripples across all ~30 units and changes their legality; it needs per-unit
rules verification and full re-validation. Banked as its own item (see backlog).

## D85 — Sanguinary Guard banner: one-model item add (S30)

**Context.** Sanguinary Guard (`000000165`) carried one UNMATCHED flag — "One model can be
equipped with 1 Sanguinary banner." — the only shipped-unit instance of the "one/1 model can be
equipped with N …" shape. Now classifies cleanly. Data-only; `index.html` stays v5.47.

**New classifier (`loadout_parser.py`), `classify_one_model_add`.** Matches "One model / 1 model
can be equipped with N `<item>`." → a body-scoped add capped at one model (`max_total` 1), same
emission path as `classify_add`; `build_loadout` resolves `<item>` to an **equipment** add when
it's a known wargear item, or a weapon add otherwise. Distinct from `classify_one_model_swap`
(verb "replace", not "be equipped with"), so no collision. Registered in `CLASSIFIERS` with the
add family at the top; UNMATCHED-everywhere by construction → converts UNMATCHED → matched only,
zero regression on the clean set (verified by diffing parser output with vs without the
classifier).

**Build-shape decisions (both reversible/data-only; recommendations taken):**
- **Banner is an equipment add, not a weapon.** "Sanguinary Banner" is a Wargear ability (+1 OC
  to the bearer's unit) with no weapon profile in `Datasheets_wargear.csv`; it's already in the
  `weapon_abilities.json` equipment allowlist, so it emits as `equipment` — same resolution path
  as the Reiver grav-chute/grapnel and Watcher-in-the-Dark items.
- **"One model" scope → the single Sanguinary Guard body group, `max_total` 1.** One group; the
  fills-to-size body group is the correct target; cap of exactly one model matches the rule.
- **3/6 size selector** surfaces from `size_brackets [3,6]` (present in data; shared mechanism —
  render is Ryan's eyeball but low-risk).

**Second real instance found + fixed (out-of-roster, latent).** The classifier also matches
Death Guard Possessed (`000001045`): "1 model can be equipped with 1 diseased icon." "Diseased
Icon" is likewise a Wargear ability (grants [LETHAL HITS] to the unit's melee weapons) but was
**missing from the equipment allowlist**, so it would have resolved as a mis-typed weapon with a
WEAPON_NOT_FOUND flag. Added **Diseased Icon** to `weapon_abilities.json`; it now resolves as an
`equipment` add. Possessed is **not in the shipped roster** (`units.json`) and is pruned by the
equipped pass, so this changes **no shipped data** — it's correct-if-ever-onboarded hygiene only.

**Data reached the preserved file via re-parse → splice.** Ran the edited parser, confirmed the
two existing count options for `000000165` reproduce byte-identically, then spliced only the new
`add_3` banner option and cleared the flag. `model_groups`/`default_weapons`/`size_brackets`/
`_defaults_source` byte-identical. Only `000000165` changed; 218 keys; full equipped chain
reproduces at **0 diff** (fixed point); CD verbatim.

## D86 — "Back up all lists" multi-list export (S31)

**Context.** The export/import module already emitted and accepted a multi-list envelope
(`{format:'40kab-lists', schema_version, lists:[...]}`); only single-list export was wired to the
UI. This session added the home-page "Back up all" button that packs every saved list into one
re-importable file. UI/version change only — no schema, parser, or data change; storage/export
layer untouched.

**What shipped (`index.html`, v5.47 → v5.48).**
- **"Back up all" button** in the home actions bar, shown only when at least one list exists
  (toggled in `renderMyLists` off `store.list()` row count). Downloads
  `40k-army-lists-backup-YYYY-MM-DD.json` via the existing `serialiseForExport` +
  `downloadText` path — the same envelope shape as single-list export, so it round-trips through
  the existing import modal with no import-side change.
- **`exportAllLists()`** gathers ids from `store.list()`, fetches each full record with
  `store.get()` (which runs `migrate`), keeps only valid records, and skips any flagged
  `__corrupt`/`__incompatible` — surfacing a skipped count (surface-don't-drop, per D82).
- **`homeFlash()` + `#home-flash` span.** `flashBanner` targets `#banner-changed`, which lives
  inside `builder-chrome` and is hidden on the home screen; a home-scoped flash element was added
  so backup feedback is visible where the button is.

**Skipped-count semantics (decision, reversible).** Corrupt records are already dropped by
`store.list()` before the user ever sees them (existing behavior, console-warned) and so are NOT
counted in the backup's "skipped" total. The skipped count reflects only newer-schema
(`__incompatible`) records caught at `store.get()` — the D82 case that matters for a user moving
between app versions. Rationale: a corrupt blob is unreadable and never surfaced in the UI;
counting it would imply the user lost a list they could see, which isn't the case.

**Verification (one line).** Node harness against `list_store.js`: multi-list export→import
round-trips all records; a mixed envelope with a newer-schema record drops+counts exactly one;
bare-array and single-record legacy files still import. Full-flow sim (2 valid + 1 corrupt + 1
newer-schema in a fake store) → `list()` yields 3 rows, 2 valid exported, 1 skipped, re-import
restores 2. App script passes syntax check. DOM render (button visibility toggle, flash text) is
Ryan's eyeball.

---

## D87 — E16: sort control on "My Army Lists" home page

**Context.** The home page listed saved lists in whatever order `store.list()` returned. With
several lists, that's hard to scan. E16 adds a user-facing sort. Pure UI over existing row data —
no schema, parser, storage, or data change.

**What shipped (`index.html`, v5.48 → v5.49).**
- **Sort `<select>`** in the home actions bar, left of "Back up all". Three options: **Recent**
  (default), **Name A–Z**, **Faction**. Shown only when at least one list exists (same
  row-count toggle as the backup button), so the empty state stays clean.
- **`sortMyListRows()`** sorts a copy (non-mutating) of the `store.list()` rows:
  - *Recent* — `modified` descending; rows missing a `modified` timestamp sink to the bottom.
  - *Name* — `localeCompare`, case-insensitive (`sensitivity: 'base'`).
  - *Faction* — `primary_faction` `localeCompare`, then name as tiebreak. Rows with no
    `primary_faction` float to the top (rare; created lists always set one).
- **`setMyListsSort(v)`** guards the value (anything other than `name`/`faction` falls back to
  `recent`) and re-renders. Selection is held in module state `_myListsSort` and re-applied to the
  select on each render so it survives re-renders (open/delete/import).

**Decision (reversible).** Default sort is **Recent**, not alphabetical — the most common home-page
action is reopening the list you were last working on, which is the newest `modified`. Options were
kept to three; points-target sort was dropped as low-value for saved-list scanning.

**Verification (one line).** Sort logic exercised in a Node harness on sample rows (recent/name/
faction all order correctly; case-insensitive; empty faction/date handled; source array not
mutated). App script passes syntax check. DOM render (select visibility toggle, live re-sort) is
Ryan's eyeball.

---

## D88 — B15 (safe subset): broad conferred always-on wargear characteristics → statline

**Context.** ~a dozen SM/DG units carry an always-on invuln/wounds in `wargear_ability_names`
(default, non-optional gear) that the statline didn't show, while the Wargear Abilities section
did — the statline read as base stats. The v5.42 reader (`statOverrideFromText`) was wired only to
bundle grants and active weapon/wargear abilities, not to this broad surface. B15 applies it there.

**What building it surfaced (two traps the backlog didn't call out).**
1. **Shared glossary text hardcodes a datasheet-specific value.** "Storm Shield" resolves to "The
   bearer has a Wounds characteristic of 4." Applied broadly, that would *drop* a Wolf Guard Battle
   Leader from its base **W5 to W4** — a regression. The Wounds/Save-characteristic *override* style
   is only correct for the datasheet the text was written for; it is not safe to apply from a
   shared ability name across all carriers.
2. **Static `wargear_ability_names` overlaps with grant-gated bundle options.** The foot Captain and
   Lieutenant list their shield in `wargear_ability_names` *and* confer it via an optional bundle
   endpoint. Applying it unconditionally would show the value even on loadouts without the shield.

**Decision (dev-manager; reversible).** Ship the **safe subset** and hold the rest:
- **Written now:** only **INV** and **FNP** overrides. These *confer* a protective stat the cell
  otherwise can't show (the model either has that invuln/FNP or not) — additive, not an override of
  a core characteristic, so no regression risk.
- **Held for Ryan (rules call):** **W** and **SV** overrides from this surface. The shared text
  carries a per-datasheet number; each affected carrier (Storm/Relic/Terminator Storm Shield →
  W; any Save-characteristic gear) needs a per-carrier verification or a data fix before broad
  application. See NEXT_SESSION decision block.
- **Grant-gated abilities skipped:** any ability that is also an optional bundle/other-option grant
  on the unit — the active-grant path (D73/D74) owns those.
- **Uniform vs bearer:** "models in the unit have…" → uniform, write the value. "the bearer has…"
  on a **single-model** group (Vehicle/Monster, or a lone Character/Epic Hero) → the bearer is the
  only model, write. "the bearer has…" on a **multi-model** group → only one model gets it; **not**
  a whole-group value → left for the **E17 asterisk** (writes nothing).
- **Conditional/summon guard:** the reader now runs sentence-by-sentence and drops any sentence
  with a conditional/summon marker (once per battle, in addition, against, summon, when it does,
  until the end of…). This keeps the Lion Helm's unit-wide invuln while rejecting its
  once-per-battle summoned Feel No Pain 4+.

**Net effect (verified on real data).** 5 groups now carry a broad INV write, all correct, zero W/SV
writes, nothing on multi-model bearer groups, grant-gated units skipped:
- Impulsor (AA) and Impulsor (BT): Shield Dome → **INV 5** (base had none).
- Venerable Dreadnought and Wulfen Dreadnought (SW): Blizzard Shield → **INV 4** (base had none).
- Azrael (DA): Lion Helm → INV 4 (base already 4 — no-op, confirms the guard keeps the invuln and
  drops the summoned FNP).

**Where it's wired.** `broadWargearStatOverrides(raw, mg)` feeds both the reference full view
(`buildModalFull` → `buildStatTable(mg, …)`) and the configured view, where it sits **first** in the
override merge (lowest priority) so any active weapon/bundle/other-option override wins. Helpers:
`unconditionalStatOverride`, `unitMaxModels`, `isSingleModelGroup`.

**Verification (one line).** Node harness mirroring the reader over all 270 units: exactly the 5 INV
groups above, 0 W/SV writes; conditional guard strips the Lion Helm FNP. App script passes syntax
check. Statline DOM render is Ryan's eyeball. `index.html` v5.49 → v5.50; no data/schema change.

## D89 — E17: asterisk on statline cells with a per-model (bearer-only) INV/FNP

**Context.** B15 (D88) deliberately writes nothing when a default wargear ability confers a per-model
invuln/FNP ("the bearer has a 4+ invulnerable save") on a **multi-model** group — one model gets the
value, so it can't be shown as a whole-group statline number. That left those cells reading as base
(an em dash for INV), silently hiding a real protective stat that the Wargear Abilities section does
list. E17 marks those cells so the two surfaces agree.

**What building it surfaced.** The set is smaller than the backlog anticipated. The backlog named
Terminator Assault Squad, Wolf Guard Terminators/Headtakers, Thunderwolf Cavalry, Deathwatch
Terminator Squad among the candidates, but those carry their invuln via an **optional storm-shield
swap** (a weapon/option surface), not a default `wargear_ability_names` entry — so they never reach
the B15 bearer path and E17 (as scoped to the default-gear surface) does not touch them. Marking the
option-swap invuln case is a separate, larger pass (it depends on the active loadout, not a default
ability) and was intentionally not widened into here.

**Decision (dev-manager; reversible).** Asterisk exactly the B15-rejected case: a multi-model group
whose default (non-optional) `wargear_ability_names` includes an **unconditional** "the bearer has…"
INV/FNP value. Guards mirror B15 — grant-gated abilities skipped; single-model groups excluded (B15
already writes those); "models in the unit have…" (uniform) excluded (B15 writes those too);
conditional/summon auras yield nothing after the sentence filter, so they are never asterisked. The
asterisk is suppressed if the cell already carries a real override value.

**Net effect (verified on real data).** 5 groups across 3 units get an INV asterisk; 0 FNP asterisks:
- Wardens of Ultramar (Ultramarines) — both named model groups (Refractor Field → per-model 5+).
- Deathwatch Veterans (Deathwatch) — the "All" group (Astartes Shield → per-model 4+).
- Decimus Kill Team (Deathwatch) — Sergeant/Veteran group and Gravis Veteran group (Astartes Shield).

Each asterisked table renders a right-aligned "* see Wargear Abilities" legend beneath it; that
section is present on all three units and lists the conferring ability by name.

**Where it's wired.** `bearerOnlyStatFlags(raw, mg)` (counterpart to `broadWargearStatOverrides`)
returns `{INV?, FNP?}` and is passed as a third arg to `buildStatTable(mg, overrides, flags)` at both
render call sites (reference full view and configured view). The asterisk is appended to the INV/FNP
cell only when that stat isn't overridden; the legend renders once per flagged table. CSS:
`.stat-asterisk`, `.stat-asterisk-legend`.

**Verification (one line).** Node harness mirroring the reader over all 270 units: exactly the 5 INV
groups above, 0 FNP; 0 B15 multi-model writes (confirms E17 and B15 partition cleanly). App script
passes syntax check. Statline DOM render is Ryan's eyeball. `index.html` v5.50 → v5.51; engine/render
change only, no schema/parser/storage/data change.

## D90 — B14b/B14c investigation: rescope, and the `requires_weapon` gate is dormant (S35)

**Context.** Handoff 34 recommended B14b/B14c as the "cleanest small build — small parser
items, self-contained, no product call." S35 opened them for build and found the framing
wrong on both.

**Finding 1 — the shipped `requires_weapon` gates don't fire.** `reqOk` and `reqOkUI` in
`index.html` disqualify a gated add/count only when a **same-scope `choice`-type** option
replaces the required weapon. Every in-roster unit that carries a `requires_weapon` value
loses that weapon through **`count`-type** swaps instead. So the gates shipped in D81
(Spectrus `000002779`) and S28 (Fortis `000002780`) are present but inert — they never
disqualify anything. The earlier "harmless today" notes were correct; this is the reason.
Consequence: adding more `requires_weapon` values (the B14c "clean" slices) writes dormant
data with no user-visible effect until the engine is fixed.

**Finding 2 — B14b is two-part, not one.** Both Impulsors (`000002568`, `000002786`) drop
two of the four "group C" options — *orbital comms array* and *shield dome* — with
`WEAPON_NOT_FOUND` flags, because they're equipment items that fail the weapon-index
lookup. B14b therefore needs (1) an equipment-allowlist parse of the two items and only
then (2) the cross-channel exclusion (parser key + engine enforcement).

**Finding 3 — three bearer-gated adds are entirely UNMATCHED** (Captain w/ Jump Pack relic
shield on a two-weapon combo, Execrator MC power weapon, Wolf Scouts haywire mine) — new-
classifier work, not covered by the existing add matchers.

**Decision (dev-manager; reversible).** Do not ship a dormant `requires_weapon` data change
this session. Rescope: promote the engine gap to **B19** (make `reqOk`/`reqOkUI` honour
`count`-type swaps via a remaining-carriers count) as the item that unblocks B14c and
activates the already-shipped Spectrus/Fortis gates; re-file B14c(b) data fixes and B14c(c)
UNMATCHED adds behind it; note B14b's two parts. **Recommended next headline: B19.** No
code/data changed this session — backlog and log only.

**Product calls still owed by Ryan** (surfaced, not blocking): B15 W/SV subset (held since
B15 — see below); B18 "all models" leader-scope; plus the standing E1 / Devastator swap /
E9 (E9). B19 itself is a build call (rule text is explicit), but its partial-swap
threshold edge cases may warrant a sanity check with Ryan at build time.


---

## D91 — B19: the `requires_weapon` gate becomes a carrier count (S36, v5.52)

**Context.** S35 filed B19 on the theory that the gates were inert because the in-roster
units removed the required weapon via `count` swaps that `reqOk` ignored. Building it showed
that theory was only half right, and the narrow fix in the brief would have shipped a no-op.

**What the data actually says.**
- **Spectrus (`000002779`)** and **Fortis (`000002780`) `add_3`** gate on a weapon
  (Deathwatch marksman bolt carbine / Deathwatch bolt rifle) that **no in-scope swap ever
  removes** — a literal "subtract matching count-swaps" fix leaves both gates exactly as
  inert as before.
- The real hole was elsewhere: `loRollup` **never called `reqOk` on `add` options outside the
  leader group at all**, so those two units' gates were unenforced by construction.
- Two other gates point at a weapon that is **not** a default of their scope group — the
  gate can only be satisfied by *gaining* the weapon, not by keeping it: Reivers
  (`000002718 add_2`, "if the Reiver Sergeant is equipped with 1 bolt carbine…") and Fortis
  `cnt_4` ("one model equipped with a plasma incinerator…"). The old choice-only test treated
  both as satisfied and offered illegal options.

**Decision (dev-manager).** Generalise the gate to a **carrier count** rather than a boolean:
carriers of weapon *W* in scope group *G* = models holding *W* as default gear, **minus**
models that swapped it away (choice or count), **plus** models that gained it (swap
replacement, replacement-choice tally, or an `adds_weapon` add). Matching is on the base
weapon name (profile suffixes collapse) and compound "A + B" replacements are split. Gated
options are then **capped** by the carrier count (so "1 model equipped with a bolt rifle per
5 models" can never exceed the bolt-rifle models), and disqualified only at zero carriers.
`reqOk`/`reqOkUI` are thin wrappers over the same function, so engine and UI cannot drift.

**Why.** One count handles all four gate shapes in the data — removal-by-choice,
removal-by-count, gain-by-swap, and required-weapon-not-in-defaults — where the boolean test
handled only the first. It is also forward-compatible: when B18 attaches the "all models"
carbine swap to the Reiver Sergeant group, that gate lights up with no further engine work
(verified in the harness against a simulated B18 loadout).

**Legality effect (2 units, both tightenings, both rules-correct today).**
- Fortis `cnt_4` (plasma pistol) is now unavailable: no selectable model carries a plasma
  incinerator. Reappears when variant groups are selectable (→ B21).
- Reivers `add_2` (sergeant's extra combat knife) is now unavailable: the sergeant cannot get
  a bolt carbine until B18 attaches the swap to its group.
Differential sweep, 54,800 random selections across all 217 loadout units: exactly these two
units change; **zero** ungated units affected.

**Filed while building:** **B20** (count swaps scoped to a single-model group are silently
dropped by the rollup — Helbrute, Ravenwing Ancient; also blocks B18) and **B21** (options
mis-scoped to the base group when the required weapon lives in a variant group).

**Still owed by Ryan:** B15 W/SV subset; B18 scope call. Unchanged.

## D92 — B14c(b): the three bearer-gated adds go live (S37, data-only)

**Context.** B19 (D91) made `requires_weapon` actually enforceable. B14c(b) was the data
half held behind it: three units whose bearer-gated adds were either un-gated or stale.

**Shipped (data only, no engine change).**
- **Death Company Marines w/ Bolt Rifles (`000002285`)** — parser-generated, stale. Stripped,
  re-parsed, spliced back with `model_groups`/`default_weapons` preserved from the committed
  file. `add_3` gains `requires_weapon: 'Bolt rifle'`; its `adds_weapon` also corrects from
  the single profile `Astartes grenade launcher - frag` to the base name `Astartes grenade
  launcher`, which is the hand-authored convention (the app base-matches, so both frag and
  krak profiles now resolve — previously only frag did).
- **Intercessor Squad (`000001157`)** — hand-authored; the body-group grenade-launcher add
  gains `requires_weapon: 'Bolt rifle'`. Correct but inert: nothing in the Intercessor body
  group can swap a bolt rifle away.
- **Plague Marines (`000001044`)** — hand-authored; the icon-of-despair add gains
  `requires_weapon: 'Boltgun'`. **This is the only live tightening of the three.** The body
  group's boltguns *are* removable (blight launcher / plague spewer / meltagun-belcher-plasma
  / bubotic / heavy plague weapon, all `count` swaps), so a list that swaps every boltgun away
  now correctly loses access to the icon. `blocks_swap` already reserved the icon-bearer's
  boltgun; the gate closes the other direction.

**Validation.** Equipped chain still reaches its fixed point at zero diff (five web.txt passes
+ `--datasheets`); 218 raw keys; whole-file diff vs the committed loadouts is exactly the three
intended edits and nothing else. Gate behaviour checked in the node harness against the v5.52
carrier-count engine: Plague Marines icon shows 4 carriers at size 5, drops with each boltgun
swap, and blocks at zero; DCM/Intercessor gates behave and never spuriously block.

**Filed while building (both real over-permissiveness — the app currently allows illegal lists).**
- **B22 — "1 model's X can be replaced" is parsed as "for every 5 models".** The classifier
  hardcodes `per_n_models: 5, max_per_n: 1` for a sentence that means *exactly one model in the
  unit*. In a 10-model squad the app therefore offers two of a single-model upgrade. 7 units,
  all parser-generated. Same classifier as B20's parser half — fix them together.
- **B23 — compound "A and B can be replaced with C" drops the second weapon.** DCM `cnt_2`
  (eviscerator replaces bolt rifle *and* close combat weapon) removes only the bolt rifle, so
  the model keeps a close combat weapon it should not have. The engine already understands
  compound `A + B` replaces (4 options in the file use it); the parser path for the "for every
  5 models…" shape does not emit it. ~25 candidate option lines to audit.

## D93
**B20 — engine half: single-model groups now honour `count` options, and every per-N cap is
bounded by its own model group (v5.53, engine-only).**

Two defects in one family: an option's cap is written against the *unit*, but the option is
scoped to a *model group*, and the engine never reconciled the two.

1. **`loMaxCount` ignored the scope group.** `per_n_models` ("1 per 5 models") was evaluated
   against unit size alone. Where the scope group is smaller than the unit, the cap ran past the
   models that exist. Live case: Reiver Squad (`000002718`) — the Sergeant's grav-chute and
   grapnel launcher (`per_n_models: 1`) were capped at *unit size*, so one Sergeant could be given
   5 or 10 grav-chutes, and the 9-model body could be given 10. The engine emitted them and the
   points/roster followed. Fix: when `per_n_models` is used and no `max_total` is authored, the cap
   is `min(floor(size / per_n) × max_per_n, models in the scope group)`. An authored `max_total` is
   still trusted as written — it is a deliberate statement, the per-N form is an inference.
2. **The rollup's `fixed: 1` branch processed only `choice` and `add`.** A `count` option scoped to
   a single-model group emitted nothing and charged nothing. Live case: Ravenwing Black Knights
   (`000002748`) — `cnt_1` on the Ravenwing Ancient rendered a working stepper that changed no
   weapons. Fix: the branch now applies counts. A picked *choice* still takes the model's whole
   slot (every copy it carries, preserving `default_weapon_counts` behaviour); a *count* takes
   exactly the number selected and leaves the remainder on the model. A source weapon consumed
   past the copies the model actually has flags `overAllocated`.

**Deliberately not changed.** Helbrute (`000001046` `cc_2`) is in the same branch but stays inert:
its cap is `per_n_models: 5` on a 1-model unit, so it still computes 0. That is B22's parser bug,
not an engine bug — the data must say `max_total: 1` before the engine has anything to apply. The
engine change is the prerequisite; the data change makes it bite.

**Validation.** Differential sweep of both engines across all 217 loadout units × every size
bracket × (nothing selected, everything maxed, each option alone): exactly 2 units differ,
`000002718` and `000002748`, both intended. No other unit's weapons, equipment, pools, or caps move.

**Filed while building.**
- **B25 — two `choice` options in one single-model group replacing the same weapon.** Three units
  (`000000083` Captain w/ Jump Pack, `000001346` Lieutenant, `000002801` Venerable Dreadnought).
  They are separate radio groups in the UI, so the user can pick both; the engine keeps whichever
  is written last and silently drops the other. Deliberately left alone here — emitting both would
  hand the user a weapon the model cannot legally have, so the real fix is mutual exclusion, not a
  rollup tweak, and it is out of B20's scope.
- **B24 — profile-pinned `replaces` / `replacement`.** 14 options name a single profile
  ("Plasma talon – standard") where the model carries the whole family. The rollup keys default
  weapons on the exact string, so swapping the pinned profile away leaves its sibling on the model
  (Ravenwing `cnt_1` removes "– standard" and keeps "– supercharge"). Same class as D92's DCM
  `adds_weapon` fix; the convention is the base name.

---

## D94 — "N model's X can be replaced with…" is N models in the unit, not N per 5 models (parser + data)
**Session 39. Data-only; `index.html` unchanged at v5.53.**

**Decision.** `classify_n_model_swap` in `loadout_parser.py` no longer hardcodes
`per_n_models: 5 / max_per_n: 1`. It reads the leading number as a fixed cap on models **in the
unit** and emits `max_total: N`. This closes **B22** and the **parser half of B20** (they were the
same classifier).

**Why.** The sentence "1 Tactical Marine's boltgun can be replaced with one of the following: …" is
the datasheet's single special-weapon slot; it does not scale with unit size. The old form offered
two of every such slot at size 10 (an illegal list the tool is supposed to refuse) and computed
**zero** on a one-model unit, because `floor(1 / 5) = 0` — which is why Helbrute `cc_2` was inert.

**Two further parser corrections in the same classifier.**
- The single-replacement branch of the regex was missing the space after "replaced with", so
  "1 Wolf Scout's plasma pistol can be replaced with 1 plasma gun." never matched at all and landed
  in `_parser_flags` as UNMATCHED. Fixed. Also handles the "N **of** this model's X" wording
  (Helbrute) and scopes "this model" to the fixed-1 group.
- A **compound source** ("X **and** Y can be replaced with…") now returns no match deliberately,
  rather than matching and silently dropping the second replaced weapon. Those lines stay UNMATCHED
  until B23. This is why `000002783` Deathwatch Veterans is untouched by this pass.

**The `Special Weapon` group heading is preserved** for these slots (an internal `_special_slot`
marker), so the UI grouping does not move.

**Blast radius.** 7 units carried the pattern in the committed file; 6 changed, `000002783` held for
B23. `000000070` Tactical Squad, `000001997` / `000002285` / `000002737` Death Company (all three
variants), `000001046` Helbrute, `000004182` Wolf Scouts. Caps at size 10 drop from 2 to 1 on every
affected slot; Helbrute's two fist swaps go from 0 to 1 and become usable; Wolf Scouts gains its
plasma-gun swap (previously no option at all).

**Validation.** Strip-from-existing → re-parse → splice, preserving committed `model_groups`,
`default_weapons` and `_defaults_source`. Equipped chain (five web.txt passes + `--datasheets`)
reaches its fixed point at zero diff. `integrity_check.py`: 0 blocking issues. Node harness over all
217 loadout units × every bracket × (nothing / everything selected): no throws, and no cap moves
outside the 6 units above.

**Known wart carried forward (B24).** The two newly-matched options are profile-pinned: Helbrute
`cnt_2` adds only "Missile launcher – frag" (not the krak profile), and Wolf Scouts `cnt_1` removes
only "Plasma pistol – standard" (leaving "– supercharge") and adds only "Plasma gun – standard".
Same class as the known Ravenwing wart. B24's blast radius grows from 14 options to 16; it is the
next turn, so this was not fixed here rather than widening the scope of a data-only pass.

---

## D95 — Weapon names in `unit_loadouts.json` are family names, and a swap source can be compound (parser + data)

**Session 40. Parser + data; `index.html` unchanged at v5.53.** Closes **B24**; closes **B23** for
the `count` family and spins the remainder out as **B23b**.

**Decision 1 — the family, not the profile, is the stored name (B24).** Every weapon name held in
`unit_loadouts.json` — `default_weapons`, `default_weapon_counts` keys, `default_wargear`, and the
option `replaces` / `replacement` / `choices` / `replacement_choices` / `adds_weapon` /
`requires_weapon` fields — is now the base weapon name with any profile suffix stripped
("Plasma pistol – standard" → "Plasma pistol"). `loadout_parser.py` emits base names; a new
`normalise_profiles` pass in `equipped_parser.py` folds the whole file on every run, so the
invariant holds for every entry regardless of when it was parsed.

**Why.** `index.html` already treats the family as the unit of selection, replacement and display —
every consumer of the loadout rollup looks weapons up by base name (`weaponBase`) — but the data was
storing per-profile names. Two consequences, both live in v5.53:
- A swap whose `replaces` was profile-pinned consumed only that one profile, so the sibling profile
  stayed on the model (Wolf Scouts kept a "Plasma pistol – supercharge" after swapping the pistol
  away). 19 options across 17 units.
- Worse and previously unlogged: **any multi-profile weapon was missing entirely from the unit's
  weapon table** (and from the weapon-abilities roll-up), because the rollup keyed the weapon by its
  full profile name and the table looked it up by base name. **45 of 217 units** were affected —
  Wolf Scouts showed no plasma pistols at all.

Base names make both correct at once with no engine change: the rollup now keys by family, the table
finds it, and every profile row of the family shows the family's count.

**Decision 2 — compound swap sources on `count` options (B23).** "1 model's bolt rifle **and** close
combat weapon can be replaced with 1 eviscerator" now emits `replaces: "Bolt rifle + Close combat
weapon"`, the compound form the engine's multi-model path already splits and charges per weapon.
Applies to `classify_per_n` and `classify_n_model_swap`; the D94 guard that left these UNMATCHED is
removed. The replacement side is compound-aware too, including comma lists ("1 bolt pistol, 1
Thunderclap and 1 runic stave").

**Decision 3 — compound sources on `choice` options are NOT emitted (B23b).** The engine keys a
choice's source by exact weapon name (`replaced[o.replaces]`, `cUsed[src]`), so a `'A + B'` source
on a choice — or on a `count` scoped to a single-model group — would consume nothing. Those lines
keep their first-weapon-only behaviour and now carry a `COMPOUND_SOURCE_UNSUPPORTED` /
`COMPOUND_SOURCE_ON_SINGLE_GROUP` flag so they are enumerable. **B23b** is the engine turn that
teaches the two single-model consumption paths to split `' + '`. ~13 characters are affected
(Captain, Dreadnought, Ancient, Lieutenant, Wolf Guard Terminator Pack Leader, …): today they keep
the second weapon they should have given up.

**Three smaller parser corrections in the same pass.**
- `"1 of the following"` is now accepted alongside `"one of the following"`. One roster unit
  (Wolf Guard Terminators) had been turning that list into a bogus single "weapon" named
  *"Of The Following: 1 Relic Greataxe 1 Twin Lightning Claws"*.
- A choice item written `"1 boltgun, 1 Astartes shield and 1 close combat weapon"` is one pick of
  three weapons, not a pick of "boltgun" plus junk; `_choices_from_list` now merges on a trailing
  comma as well as a trailing "and".
- `normalise_weapon` gained a squashed-alphanumeric fallback, so the datasheet's "powerfist" (no
  space) resolves to "Power fist" instead of inventing a weapon.

**Data.** 11 units re-parsed and spliced (`000000231`, `000000241`, `000000318`, `000001372`,
`000002285`, `000002737`, `000002781`, `000002783`, `000002798`, `000003874`, `000004182`); the
base-name fold touched 91 units in all. Options 268 → 274; parser flags 63 → 56. The equipped chain
reaches its fixed point at zero diff; `integrity_check.py` reports 0 blocking issues.

**Five units were stale against the parser.** A full re-parse of the committed file (not just the
target units) showed `000000231`, `000000241`, `000000318`, `000002781`, `000003874` had never been
re-spliced after earlier classifier work and were missing options they now parse cleanly (Deathwing
Knights' Watcher in the Dark as equipment rather than a phantom weapon; Ravenwing Black Knights'
grenade-launcher swap; Wolf Guard Terminators' assault-cannon swap; two Kill Team swaps). All five
are in this session's re-parse set. **Process note:** a targeted splice leaves the rest of the file
behind whenever a classifier widens. A full re-parse diff should be run at the end of any parser
session, and the units it turns up folded into the same splice.

---

## D96 — Session 41: the per-N passive-possessive shape (B26), the Whirlwind bleed (B27), and a 23-unit staleness fold

**Decision.** `classify_per_n` now handles the passive-possessive form of a per-bracket swap, and
`equipped_parser.segment` no longer lets an off-roster datasheet's composition bleed into the
previous roster unit. Both are parser fixes; the data file was regenerated from the parsers, not
hand-edited.

### B26 — "up to N models can each have their X replaced with Y"
The datasheets write a per-bracket swap in four interchangeable ways. `classify_per_n` recognised
the two *active* forms ("… can replace its X with Y") and the singular possessive ("1 model's X can
be replaced with Y"), but not the **passive-possessive plural** — "For every 5 models in this unit,
up to 2 models can each have their boltgun and power weapon replaced with one of the following: …".
Those sentences fell through to UNMATCHED, so the options did not exist in the tool at all.

Three changes to the classifier:
- a new branch for `can [each] have their|its <source> replaced with <single | one of the following>`,
  compound-source aware and choice-list aware;
- the per-bracket **cap is now read from the sentence** ("up to 3 models" → `max_per_n: 3`) instead of
  being hardcoded to 1 — this also corrects the possessive-plural form ("up to 3 models' combi-bolters
  can each be replaced with 1 combi-weapon", Blightlord Terminators);
- the passive branch tolerates "can **each** be replaced", and a source-data typo in the Death Company
  Marines datasheet ("replaced with **equipped with** 1 eviscerator") is normalised away.

Every "For every N models…" line in the SM/DG datasheet set (58 of them) now classifies; there are
zero UNMATCHED per-N lines left. Five roster units gained options: **Deathwatch Veterans**
`000002783` (+6 body options — every Deathwatch-specific weapon, including the six-weapon "one of the
following" list), **Blightlord Terminators** `000001372` (combi-weapon, cap 3 per 5),
**Sword Brethren** `000002798` (pyre pistol, cap 2 per 5), **Crusader Squad** `000002799`
(the Initiates' two-way choice, cap 2 per 10), **Death Company Marines** `000001997` (eviscerator).
Plague Marines `000001044` carries the same shape but is hand-authored and was left untouched.

No engine change was needed: the multi-model consumption path already splits a compound `' + '`
source for both `count` and `count`-with-`replacement_choices`, so Deathwatch Veterans' "boltgun **and**
power weapon" source charges both weapons correctly. Verified in the node harness.

### B27 — the Whirlwind's borrowed weapons
`equipped_parser.segment` attributed each UNIT COMPOSITION block to the nearest preceding *roster*
title. A datasheet that is **not** on the roster (Legends / Forge World — the Astraeus and the
Thunderhawk sit right after the Whirlwind in the Space Marines composition dump) had no title of its
own, so its "This model is equipped with:" line was credited to the previous roster unit. The
Whirlwind carried four weapons it does not own (ironhail heavy stubber, twin heavy bolter ×4,
lascannon ×2, armoured hull) plus four wargear tokens from two different aircraft.

`find_titles` now recognises **every** datasheet block — a name line followed by the stat header `M`,
past an optional base-size line — and returns `None` for one that isn't on the roster. An anchor owned
by a `None` title is dropped rather than reassigned. The base-size "(⌀…)" line is explicitly excluded
from title candidacy (it also sits directly above an `M` and would otherwise shadow the real title).
A group the parser rewrites now has its `default_wargear` and `default_weapon_counts` cleared first,
so stale bleed can't survive a re-run. Exactly one unit changes: the Whirlwind, down to its true
loadout (Whirlwind vengeance launcher, armoured tracks) with the hunter-killer missile and storm
bolter still available as adds. Two composition blocks are now correctly dropped as off-roster.

### The staleness fold (S40's new standing check, first run)
The full-file re-parse turned up **23 more stale units** — options that had never been re-spliced
after earlier classifier work. All are folded into this session's splice:
- **Two real legality fixes.** The **Captain** `000000073` had one datasheet choice split into two
  bogus picks ("heavy bolt pistol" alone, and a three-weapon combo missing the pistol); it is now the
  single correct pick. The **Venerable Dreadnought** `000002801` had a duplicated, half-formed pair of
  choices; it is now two proper compound picks.
- **Eight group headings** carried a weapon *profile* suffix ("Bilesword – Strike Options") or a
  compound label. D95's fold normalised weapon names but not the option's display heading; the parser
  now emits headings from the base name.
- **Ten units** gained a `COMPOUND_SOURCE_UNSUPPORTED` flag they should already have carried since
  D95. No behaviour change — the flag makes the B23b population enumerable (Tactical Squad, Captain,
  Captain with Jump Pack, Dreadnought, Brutalis, Death Company Dreadnought, Ancient in Terminator
  Armour, Ancient, Venerable Dreadnought, Wulfen Dreadnought).

`model_groups` / `default_weapons` / `_defaults_source` were preserved from the committed file
throughout the splice; the re-parse would have regressed the Decimus Jump Kill Team `000003874`'s
body-group weapons if taken wholesale.

**Data.** 28 units changed. Options 274 → 284; parser flags 56 → 60 (the eight new
`COMPOUND_SOURCE_UNSUPPORTED` and two `WEAPON_NOT_FOUND: astartes shield` flags outnumber the ten
UNMATCHED lines B26 retired). The equipped chain reaches its fixed point at zero diff;
`integrity_check.py` reports 0 blocking issues. `index.html` unchanged at v5.53.

**Carry-over.** Option ids renumber on Deathwatch Veterans and Death Company Marines (new options
sort ahead of the old ones). A saved list with a pick on those two units reads the pick as
unselected; the user re-picks. No data loss and no illegal list.

**Why.** The per-N shapes are the datasheet's "special weapon" slot — the single most
legality-relevant option class in the game — and six of Deathwatch Veterans' were simply absent.
The Whirlwind fix removes the last unit whose weapon rollup produced weapons with no matching
profile row.

---

## D97 — Compound swap sources, mutually exclusive choices, and dead swap controls (Session 42, index.html v5.54)

**Engine (`index.html` v5.53 → v5.54, `loComputeLoadout` / `loRollup` / `buildLoadoutHtml`).**

**B23b — compound sources on a single-model group.** The `fixed: 1` consumption path keyed a swap's
source by the exact weapon name, so a source naming two weapons ("its storm bolter and power fist can
be replaced with twin lightning claws") matched nothing: the source weapons stayed on the model and,
because replacements were only emitted while walking the group's default weapons, the pick vanished
too. The path now splits a source on `' + '`, consumes every weapon named, and emits the replacement
once — the same rule the multi-model path has used since B23. Sources and consumption are keyed on the
base weapon name, so a profile suffix or a case mismatch can't miss. **The parser still reduces a
compound source to its first weapon and flags `COMPOUND_SOURCE_UNSUPPORTED`; the engine is now ready
for the data, and the parser half is the next turn.** Verified against synthesised compound sources on
the Ancient in Terminator Armour and the Captain with Jump Pack.

**B25 — two choices, one slot.** Choice options in the same group that name the same source weapon
(Venerable Dreadnought: the assault cannon becomes a helfrost cannon *or* the greataxe-and-shield pair)
rendered as two independent radio groups; picking in both left the rollup silently keeping one. They
are now joined into **one radio group** — options are clustered when their source weapons overlap, so a
compound source that overlaps two options is handled too. Picking any row clears every option in the
cluster and sets the clicked one. A saved list carrying two picks in one cluster heals on render (first
wins). The rollup keeps a guard of its own: a second claim on an already-swapped weapon is ignored and
raises the over-allocation flag. Affects the Captain with Jump Pack, the Venerable Dreadnought and (once
its bundle is not in charge) the Lieutenant.

**Compound replacements were being judged as broken picks.** `brokenChoice` tested a whole compound
string ("Heavy flamer + Dreadnought combat weapon") against the weapon table, failed, and dropped the
whole option from the sheet. It now judges a pick part by part. Two legal options return: the
**Dreadnought**'s dreadnought-combat-weapon swap and the **Venerable Dreadnought**'s greataxe pair.

**Add-choices did nothing at all.** A choice with no source (`replaces: null` — "can be equipped with
one of the following") never reached the weapon rollup, because the emission loop only ran over the
group's default weapons. Picking a multi-melta on an Impulsor changed nothing. The pick is now gained.
**14 units** were affected (both Impulsors, both Repulsors, the Predators, the Corvus Blackstar, the
Land Raiders and others).

**A swap whose source isn't on the model now grants nothing (new).** With add-choices live and the
Talonstrike's groups corrected (below), an option whose `replaces` weapon is absent from its scope
group would hand out the replacement for free. Both rollup paths now skip such an option, and the UI
hides it rather than showing a dead control. **11 options on 9 units**: the four Deathwatch kill teams
and the Talonstrike (variant-group swaps parked on the base group — B21), and three where the source is
a wargear *item* rather than a weapon (both Wulfen units' death totem, the Wolf Guard Battle Leader's
storm shield). None of these controls worked before; they were dead or, worse, free.

**Data (`unit_loadouts.json`, `loadout_parser.py`) — B14b part 1 and one staleness fold.**

**B14b part 1 — equipment allowlist on add-choices.** An add-choice pick that isn't a weapon but is a
known wargear item (`weapon_abilities.json`) is now resolved as equipment and listed in a new
`equipment_choices` field, so the engine files it under equipment rather than the weapon table. The
lookup tolerates a trailing qualifier the datasheet doesn't use ("Orbital Comms Array (Aura)"). Three
units: both **Impulsors** (orbital comms array, shield dome) and the **Corvus Blackstar** (auspex array,
infernum halo-launcher). Six `WEAPON_NOT_FOUND` flags retired. Without this, D97's add-choice fix would
have put a shield dome in the weapon table.

**Talonstrike Kill Team `000003874` — staleness fold.** S40's standing re-parse check turned this up
again. D96 preserved the committed `model_groups`, judging the re-parse a regression; that call was
wrong. The datasheet gives each group its own gear (Intercessors with Jump Packs: heavy bolt pistol and
Astartes chainsword; Heavy Intercessors with Jump Packs: assault bolters and close combat weapon), and
the committed file gave **both groups the union of all four weapons**. The re-parsed split is taken.
The unit's `cnt_4` (assault bolters → plasma exterminators) is scoped to the Intercessor group, which no
longer carries assault bolters, so it is now correctly inert — a B21 case, not a new one.

**Totals.** 218 raw keys (217 units + `_schema`), 284 options, **54 parser flags across 38 units** (was
60/41). Equipped chain reaches its fixed point at zero diff; the standing full re-parse check is clean;
`integrity_check.py` reports 0 blocking issues. CD carried verbatim (0 CD units in the file).

**Why.** Every item here is a legality bug, not a cosmetic one: weapons kept that should have been given
up, two picks the rules allow only one of, legal options invisible, illegal free weapons, and controls
that silently did nothing.

---

## D98 — The parser writes compound swap sources in full (B23b data half) and stops inventing "additional" weapons (B29). Session 43, data-only

**Decision.** `loadout_parser.py` now writes the whole source of a `choice` / `single` swap, not just its
first weapon. The datasheet phrase is split on commas as well as " and " ("this model's bolt pistol,
master-crafted bolter and close combat weapon can be replaced with…" → `replaces: "Bolt pistol +
Master-crafted bolter + Close combat weapon"`). The engine has consumed compound sources on single-model
groups since D97, so no engine change was needed. `COMPOUND_SOURCE_UNSUPPORTED` and its count-branch twin
`COMPOUND_SOURCE_ON_SINGLE_GROUP` are retired.

The option's `group` heading takes the **first** source weapon, so a compound never appears in a heading
(keeps the D95 invariant readable).

**B29.** A quantity qualifier on an add or a swap pick ("1 additional combi-bolter", "an additional
Helbrute fist") is not part of the weapon's name. `normalise_weapon` strips `additional` / `another` /
`second` / `extra` and resolves the weapon underneath, so the pick stacks a second copy of a weapon the
model already carries. Chaos Rhino now ends with two combi-bolters; the Helbrute with two Helbrute fists.
Two `WEAPON_NOT_FOUND` flags retired.

**New flag — `OR_SOURCE_UNSUPPORTED`.** A compound source with an alternative inside it ("its Fenrisian
greataxe **or** great wolf claw **and** storm bolter can be replaced…") names a weapon the model may not
have. The engine keys a source by name and has no "either of these" source, so the parser flags the
sentence and falls back to the first source weapon — the pre-D98 behaviour, now named. One carrier: the
Wulfen Dreadnought. A bare (non-compound) "A or B" source is left alone, as before.

**Effect.** 14 units changed. The user-visible change is that a compound swap now gives up everything the
datasheet says it gives up: the Captain loses master-crafted bolter and close combat weapon when he takes
a pistol/fist pair; the Tactical Sergeant gives up his boltgun as well as his bolt pistol for twin
lightning claws; the Wolf Guard Terminator Pack Leader gives up his master-crafted power weapon; the
Venerable Dreadnought gives up all three weapons for the greataxe pair. Node sweep over 1,020 real cases:
23 diffs, all of them the extra source weapon being consumed, none unintended.

**B25 interaction confirmed.** On the Ancient in Terminator Armour the power fist is named both by `cho_1`
alone and inside `cho_2`'s compound. The engine clusters the two into one radio group (the user cannot
pick both), and the rollup's own guard reports over-allocation if a stale saved list holds both. Merged
control and rollup agree.

**Flag totals:** 54 → 41 (12 compound flags and 2 `WEAPON_NOT_FOUND` retired, 1 `OR_SOURCE_UNSUPPORTED`
added). 32 flagged units. Options 284, unchanged; 218 raw keys, unchanged. `index.html` untouched (still
v5.54). Equipped chain reproduces the new file at zero diff; full re-parse against the two hand-authored
units returns zero unit diffs; `integrity_check.py` 0 blocking issues; the D95 no-profile-suffix invariant
holds at zero hits.

**Still open (banked as B30).** The *replacement* side of a `single` swap is not split on " and " the way
the choice-list side is: the Captain with Jump Pack's "1 thunder hammer and 1 relic shield" lands as
"Thunder hammer" alone, the Lieutenant's "1 neo volkite pistol, 1 master-crafted power weapon and 1 storm
shield" lands as one literal weapon name, and the Wulfen Dreadnought's "1 blizzard shield and 1 heavy
flamer" is unresolved. Fixing it in isolation would put shields in the weapon table, so it is sequenced
behind the equipment channel (B14b part 3).

---

## D99 — The equipment channel on the replacement side; B14b part 2 closes as already satisfied (S44, engine only, v5.55)

**Engine turn. `index.html` 5.54 → 5.55. No data file changed.**

**Part 3 — `equipment_parts` (new option field).** Until now only an *add-choice* could name a pick that
is an item rather than a weapon (`equipment_choices`, D97). A **swap replacement** that is part weapon,
part item could not be represented at all: the Captain with Jump Pack's "1 thunder hammer and 1 relic
shield" and the Ancient in Terminator Armour's "1 thunder hammer and 1 Terminator storm shield" either
dropped the shield or put it in the weapon table, where it renders as nothing because no weapon profile
exists for it.

An option may now carry `equipment_parts`: a list of names that, wherever they appear as a part of that
option's replacement — in `choices`, `replacement_choices` or a single `replacement`, alone or inside a
`' + '` compound — are filed under **equipment** rather than **weapons**. The rollup routes part by part.
`equipment_choices` and `equipment_parts` are read as one set, so D97's shape keeps working unchanged and
a name listed in either behaves the same way.

Three consequences worth naming:
- **No new option type.** A compound replacement stays one option, one control, one pick. `brokenChoice`
  still judges a compound part by part; a part named in the option's equipment list now counts as a *real*
  part, so an item-only or item-bearing pick no longer reads as broken and vanish from the sheet.
- **Every emit site routes.** Single-model choices, single-model counts, body-group counts and
  `replacement_choices` all pass through the same router, so a body-group swap that hands out a shield
  behaves the same as a leader one.
- **The engine change ships alone.** No shipped datasheet carries `equipment_parts` yet — that is B30, the
  next data turn. This build is the gate B30 was waiting on.

**Part 2 — cross-channel exclusion: closed, no engine change needed.** The banked item assumed the four
Impulsor picks live in two structures (a weapon option and an item option) needing a shared exclusion key.
That stopped being true when part 1 landed: the parser emits all four as **one** `choice` option with two
names in `equipment_choices`. One option is one radio group, so "pick at most one across weapons and
items" is already enforced by construction, and the rollup files the pick into the right table. Verified
on both Impulsors and the Corvus Blackstar rather than assumed. B14b closes.

**Verification.** Sweep, old engine vs new over the shipped data: 1,100 cases, **0 diffs** — expected, and
the point: the engine gained a capability without moving any existing list. The payoff was driven with
authored B30-shape cases instead: the Captain with Jump Pack's hammer/shield pick leaves one weapon
(thunder hammer) and one item (relic shield); the Ancient's hammer/shield pick does the same and its twin
lightning claws pick is untouched; a body-group compound swap on the Tactical Squad hands out two power
fists and two shields, consuming two bolt pistols. Impulsor picks route correctly across both channels.
Baseline before the change was clean on every checkpoint (fixed point at zero diff, full re-parse zero unit
diffs, D95 invariant zero hits, 41 flags / 32 units, integrity 0 blocking).


## D100 — B30: compound single replacements, and the wargear allowlist on the whole replacement side (S45, data turn)

**Decision.** The parser now (a) splits a `single`-type replacement on `" and "` / commas the way a choice
list already was, and (b) routes any replacement-side name that is not a weapon but *is* in the wargear
allowlist (`weapon_abilities.json`) into the option's `equipment_parts` list. No engine change; `index.html`
stays at v5.55.

**Why the routing was widened past the three named carriers.** B30 was scoped to the single-replacement
split. But the allowlist lookup is the same mechanism wherever a replacement name fails the weapon lookup,
and D99's engine already routes every replacement shape through one emitter. Restricting the lookup to
`single` options would have left the identical bug live on ten other options — a shield sitting in the
weapon table, where it renders as nothing because no weapon profile exists for it. So the lookup was
applied to the whole replacement side: `choices`, `replacement_choices`, and a `count`'s `replacement`.
The **source** side (`replaces`) was deliberately left alone: an item as the thing being *given up* is a
different problem (B28) and stays flagged.

**Consequences.**
- 13 options across 13 units now carry `equipment_parts`. Every one is a shield or a launcher that was
  either silently dropped, parked in the weapon table as a name with no profile, or left as a garbage
  literal.
- Three long-standing garbage strings are gone: the Captain with Jump Pack's dropped relic shield, the
  Lieutenant's `"Neo Volkite Pistol, 1 Master-Crafted Power Weapon And 1 Storm Shield"`, and the Wulfen
  Dreadnought's `"Blizzard Shield And 1 Heavy Flamer"`.
- Parser flags fall from **41 across 32 units to 27 across 27 units** (21 UNMATCHED, 5 WEAPON_NOT_FOUND,
  1 OR_SOURCE_UNSUPPORTED). Every remaining `WEAPON_NOT_FOUND` is now a **source-side** item — exactly the
  B28 set (Terminator Assault Squad, Wulfen, Wolf Guard Battle Leader, Wolf Guard Headtakers, Wulfen with
  Storm Shields). The category is clean: nothing else is left on the replacement side.
- No new options, no options removed: 284 options, 218 raw keys, unchanged.

**Verification.** Data sweep on engine v5.55, committed data vs new data: 940 cases, **22 diffs across 13
units**, every one an item moving out of the weapon table into "Other wargear" (plus the three literals
resolving into their real parts). No weapon lost or gained anywhere else. Equipped chain reaches a fixed
point at zero diff; full re-parse with the two hand-authored units as `--existing` returns zero unit diffs;
D95 invariant zero hits; `integrity_check.py` zero blocking.

---

## D101 — a wargear item can be the *source* of a swap, and base gear is now rolled up (S46, engine)

**Context.** D99/D100 closed the *replacement* half of the weapon/item boundary: an option can now hand a
model an item that has no weapon profile (`equipment_parts` / `equipment_choices`), and that item lands in
"Other wargear" instead of vanishing. The *source* half was still open. Five options name a thing the model
gives up that it carries as gear, not in its weapon table — a storm shield or a death totem. The engine
looked for the source in `default_weapons` only, so it either found nothing (option hidden as a dead
control) or found only the weapon half of a compound source (`Thunder hammer + Storm Shield`) and charged
that, leaving the shield behind on a model that had just traded it away.

**Decision.** The group's own gear list is the source of truth for "does this model carry this item?" —
no new field on the option. Three changes to the engine:

1. `model_groups[].default_wargear` (already written by `equipped_parser.py`, previously read by nothing)
   is now **rolled up**. Each model in the group carries one of each listed item, and whatever is not
   consumed lands in the equipment table. Base gear was invisible in the app before this.
2. A source part is "on the group" if it is in `default_weapons` **or** `default_wargear`. So
   `loSrcOnGroup` — and with it the UI's `srcMissing` hide — treats a gear item as a real source.
3. Source charging is keyed by **base name** (`weaponBase`), not by the raw string. The option prose says
   "Storm Shield", the gear list says "storm shield"; before this, a case difference between an option's
   source and a group's gear silently missed. Weapon sources were matching only by luck of casing.

Display name is resolved through the wargear allowlist (`weapon_abilities.json`), so a gear list entry of
"storm shield" renders as "Storm Shield" and does not open a second row next to an item gained through
`equipment_parts`.

**Why not a `source_parts` field on the option (mirroring `equipment_parts`).** The replacement side needs
an explicit annotation because a *gained* name has no group list to check against — the parser has to do
the allowlist lookup and record the answer. The source side does have such a list: the group's own gear.
Annotating it on the option too would be a second, weaker copy of the same fact.

**Consequences.**
- Four units now show base gear they never showed: Terminator Assault Squad (storm shield ×N),
  Wolf Guard Headtakers (storm shield ×N), Veteran Sergeant Metaurus / Gaius Silva (storm shield,
  refractor field). Chapter Ancient's banner sits on an `optional` group (count 0) and is unaffected.
- Two of the five B28 options now consume correctly: Terminator Assault Squad `cnt_1` and Wolf Guard
  Headtakers `cnt_1` — swapping to twin lightning claws / paired power weapons now takes the shield away
  as well as the weapon.
- The other three (`000000311`, `000004130`, `000004132`) name a source that is **only** gear and their
  groups have **no `default_wargear` at all**, so they stay hidden. The engine is ready for them; the data
  is not. That is B28's data half.

**Verification.** Engine sweep v5.55 vs v5.56 on committed data: 940 cases, 9 diffs across 3 units, every
one gear appearing or being consumed. No weapon count moved anywhere. Authored cases drive both new shapes
(gear-only source on a single-model group, gear-only source on a count swap) and both behave.

---

## D102 — B28b: a wargear item is a first-class swap source, and gear-only groups now carry their gear (S47)

**Data turn. `loadout_parser.py`, `equipped_parser.py`, `unit_loadouts.json`. No engine change (`index.html`
stays at v5.56).**

### Part 0 — the stale parser, rebuilt to the fixed point
The `loadout_parser.py` in the project set was still the pre-S45 copy: no D100 logic at all. Rather than
wait on a re-upload, D100 was reconstructed against the committed `unit_loadouts.json` as the target, and
the restored parser now reproduces it at zero diff. Two pieces:
- **Replacement-side allowlist.** A part of a replacement or choice phrase that is not a weapon but *is* in
  the wargear allowlist (`weapon_abilities.json`) resolves to the item's canonical name, raises no flag, and
  is listed in the option's `equipment_parts`.
- **Compound `single` split.** `'... can be replaced with 1 thunder hammer and 1 relic shield'` is two
  things, not one. A `single` classifier now carries the raw replacement phrase and splits it the same way a
  `count` replacement is split. Before the fix the whole phrase prefix-matched a single weapon and the
  second item was silently dropped (Captain with Jump Pack's relic shield; the Lieutenant's storm shield;
  the Wulfen Dreadnought's blizzard shield).

### Part 1 — item sources (the B28 data half)
An option whose **source** is a gear item is legal and is no longer flagged: the source-side name is
resolved through the same allowlist. It is deliberately **not** annotated with `equipment_parts` — per D101
the group's own `default_wargear` is the authority on what a model carries, and a second copy on the option
would be a weaker duplicate. `WEAPON_NOT_FOUND` goes to **zero**; flags 27 → 22 (21 UNMATCHED + 1
OR_SOURCE_UNSUPPORTED).

### Part 2 — gear on single-group units
The `Datasheets.csv` gap-fill in `equipped_parser.py` skipped every single-group unit, on the reasoning that
a one-group unit's flat weapon pool is already correct. True for weapons; false for gear, which never
appears in the weapon pool at all — so a one-group unit could not carry any gear, and a gear-sourced swap
had nothing to consume. The guard is now: admit a single-group unit **only when its datasheet loadout prose
names a token that fails the weapon lookup and resolves in the wargear allowlist.** Weapon assignment for
those units is unchanged by construction (the prose lists the same weapons the flat pool already holds).

### The count question — answered by the datasheet, not by us
The handoff flagged the death totem as a likely one-per-unit item. It is not. The datasheet loadout reads
"Every model is equipped with: Wulfen weapons; death totem", and the option reads "Any number of models can
each have **their** death totem replaced" — a per-model possessive that only parses if every model has one.
One totem per Wulfen. No new model group, no gear count. Nothing for Ryan to rule on.

### Consequences (5 units, all gains)
- `000000311` Wulfen and `000004132` Wulfen with Storm Shields — death totem ×N appears; the stormfrag
  swap now fires and eats one totem per model swapped.
- `000004130` Wolf Guard Battle Leader — storm shield appears; `cho_2` (shield → carbine / heavy bolt
  pistol / plasma pistol) is a live control for the first time.
- `000000218` Azrael (the Lion Helm) and `000000226` Ezekiel (Book of Salvation) — gear that was in the
  datasheet and nowhere in the app now shows under Other wargear. Found by the mechanism, not sought.

### Verification
Data sweep (one engine, two datasets — `sweep_data.js`, new): 940 cases, 15 diffs across exactly those 5
units, every one gear appearing or being consumed; no weapon count moved anywhere except the three swaps
that were previously dead. Pipeline fixed point holds at zero diff. D95 invariant: zero hits. Integrity
check: 0 blocking.

---

## D103
**B14c(c) — bearer-gated adds. A gate may name more than one weapon; it is written the way every other
multi-weapon field is written.**

Three sentences were UNMATCHED because the gate did not fit the shape the parser knew. Two were only
wording: the gate can be written with an article rather than a count ("an absolvor bolt pistol"), and the
bearer can lead the sentence rather than an "If" ("1 Wolf Scout equipped with a plasma pistol can be
equipped with 1 haywire mine"). The third is a real gap: the Captain with Jump Pack's relic shield is gated
on the model holding **two** weapons at once.

**Mechanism call (dev-manager).** No new schema field. `requires_weapon` may hold several weapon names
joined with ` + `, and the bearer must hold **all** of them. Reason: ` + ` already means "all of these" in
`replaces`, `replacement` and `choices`, and the engine already has `loWeaponParts` to split it. A new
array field would be a second way to say the same thing.

**The trailing rules note is dropped.** "(that model's plasma pistol cannot be replaced)" and "This model's
heavy bolt pistol and Astartes chainsword cannot be replaced" restate the gate: if the bearer swaps the gate
weapon away, `requires_weapon` already removes the add. No separate mechanism.

**Finding — the Captain sentence is not redundant.** The backlog wondered whether D100's fix to `sng_3`
(the compound swap to thunder hammer + relic shield) had made it so. It had not. `sng_3` *replaces* both
weapons; this sentence *keeps* both and adds a shield. Two different builds.

### Shipped
- `000004135` Execrator — master-crafted power weapon, gated on the absolvor bolt pistol.
- `000004182` Wolf Scouts — haywire mine (gear), gated on a plasma pistol.
- `000000083` Captain with Jump Pack — relic shield (gear), gated on `Heavy bolt pistol + Astartes
  chainsword`.

### Engine debt, deliberate
The live engine (v5.56) treats `requires_weapon` as one name, so a compound gate matches nothing and the
Captain's relic shield renders **disabled** ("needs Heavy bolt pistol + Astartes chainsword"). That is
over-strict, not permissive: no illegal list is reachable. The engine change is small — `loReqCarriers`
takes the minimum carrier count across the parts of the gate — and is the next engine turn. Shipping the
data over-strict was chosen over shipping it under-strict; a legality tool must never be the looser one.

---

## D104
**A negated gate is a mutual exclusion, not a requirement. The parser must not read it as one.**

While widening the bearer-gated add, the classifier initially matched "1 Plaguebearer that is **not**
equipped with a daemonic icon can be equipped with 1 instrument of Chaos" and emitted
`requires_weapon: Daemonic Icon` — the exact opposite of the rule, and a permissive bug (it would have let
one model carry both icon and instrument). Both new classifiers now refuse any sentence containing "not
equipped with".

`000004113` Plaguebearers and `000004114` Plague Drones stay UNMATCHED. The correct shape is a two-option
mutual exclusion (pick icon **or** instrument, one model, not both) — a new backlog item, not a gate.

**Carry forward:** a classifier widened to accept more wording will happily accept the *negation* of that
wording. Every new gate pattern needs a negation guard, and the check is worth doing on any future
loosening.


## D105 — E17: when a conferred characteristic reaches the statline; B15 closed as never-real

**B15 was false and blocked a feature for twelve sessions.** The handoff carried "the shared storm
shield text regresses Wolf Guard Battle Leader from W5 to W4" from S37 to S49. There is no shared
text. `Datasheets_abilities.csv` is keyed by datasheet id — **D70 already decided this.** Source:
`Datasheets_abilities.csv 000004130` reads *Wounds characteristic of **6***; printed W is 5
(`Datasheets_models.csv 000004130`). A +1, not a regression. The "4" belongs to the base-W3 terminator
units (`000000118` Terminator Assault Squad, `000000318` Wolf Guard Terminators, `000003822` /
`000003873` Deathwatch Terminator Squad, `000002302` Deathwing Command Squad), where +1W is correct.
Confirmed against the printed cards.

**Restated so it cannot rot again:** wargear ability text is read from the unit's own datasheet row,
never by item name, and applied literally — *"Wounds characteristic of 6"* is an absolute **set**, not
a modifier. Storm Shield confers three different effects across the roster (W:4, W:6, inv:4). Any
name-keyed lookup is provably wrong. Now enforced by `rules_assertions.py`, not by prose.

**Decision (E17 render rule).** D75 deferred the broad conferred-ability pass *with an asterisk for
bearer-only cases*. Made concrete: a conferred characteristic reaches the statline only when **every
model in the configured unit carries the item**, counted with the existing `loCarriers` machinery.
- all models carry it → apply the override (Battle Leader → W6; Terminator Assault Squad at default → W4)
- some but not all → statline untouched; render the Wargear Ability with an asterisk to the rules text
  (Wolf Guard `000000315`, where the shield is an *option* — a 10-model pack may hold three)
- none carry it → the ability does not render

Dynamic on the loadout, not static per datasheet: the same unit moves between clean and asterisked as
it is built. **Rationale:** a unit with mixed gear has no single statline, and writing the override
unit-wide would hand an invuln to models that do not have one — permissive, and a legality tool must
never be the looser one.

**Process (the real fix).** The decision log outranks the handoff; grep it before acting on any
inherited rules claim. Every factual claim cites its source row. Any blocker carried more than three
sessions has its premise re-verified against source before it is re-listed. Uncited is a guess, not a
fact. Ships as: `rules_assertions.py` (new).


## D106 — a negated gate is a PER-MODEL exclusion, not a unit-level one. D104's remedy was wrong.

D104 correctly killed a permissive bug: the widened bearer-gate classifier had read "1 Plaguebearer
that is **not** equipped with a daemonic icon can be equipped with 1 instrument of Chaos" as
`requires_weapon: Daemonic Icon` — the exact inversion of the rule. The negation guard it introduced
stands and is now asserted (B33-2).

Its **remedy** does not. D104 proposed "a two-option mutual exclusion (pick icon **or** instrument, one
model, not both)" and the S50 prompt inherited that as a unit-level lock. Re-derived from source
(`Datasheets_options.csv` `000004113`, `000004114`; `Datasheets_unit_composition.csv` — 1 Plagueridden +
9 Plaguebearers, 1 Plaguebringer + 2-5 Plague Drones; `chaos_daemons_reference.md` line 124, which lists
Daemonic Icon **and** Instrument of Chaos as concurrent wargear abilities of the same unit): the two
sentences forbid **one model** holding both items. They say nothing about the unit. A Plaguebearer pack
may field an icon bearer **and**, on a different model, an instrument bearer — that is the normal,
legal build, and it is how every daemon unit in the game works.

A pooled exclusion would have capped the pair at one and made a legal list unbuildable. The tool's whole
premise is that legality is the only boundary on validity; over-strict is as wrong as permissive, and it
is the failure mode a stricter-than-New-Recruit tool is most likely to walk into.

**Decided:** the shape is two independent single-model adds, each `max_total: 1`, scoped to the body
group, with **no gate and no pool**. Because both bodies hold two or more models, the two adds can never
be forced onto the same model, so the per-model exclusion needs no representation at all.

**Carry forward — and this is the second time in two sessions.** D104 was written while fixing a real
bug, and its remedy sentence was never re-derived from source; it was inherited as fact, exactly as B15
was. A decision reached *in passing*, while the session's attention was on something else, is the most
likely one to be wrong. Re-derive a remedy before building it, not just a diagnosis.


## D107 — wargear is NOT free. And the false claim came from our own data, one turn after D106.

**The fact.** Every MFM faction file carries a `WARGEAR OPTIONS` block with per-item costs — Defiler's
heavy reaper autocannon and hades lascannon at 10 pts each, Redemptor Dreadnought's macro plasma
incinerator at 10, Terminator Assault Squad's thunder hammer at 5, Space Wolves' storm shield at 5,
Grey Knights' psycannon at 5. 138 priced entries across the MFM; 38 in the v1 priority factions.
`mfm_points_parser.py` drops them all: `SKIP_HEADERS` lists `wargear`. Source: `MFM_*_v1_0.txt`,
`WARGEAR OPTIONS` blocks; `mfm_points_parser.py` line 58. Backlog item **B35**, top priority.

**How the false claim got made, which matters more.** In S50 I wrote, in E14 and in chat, *"there is no
per-option cost field anywhere in `unit_loadouts.json` or `units.json`, and under the current MFM every
wargear option is free."* The first half is true. The second half does not follow from it, and is false.
I checked our derived data, found no cost field, and reported its absence as a fact about the rules. Ryan
disproved it from memory in one line.

This happened **one turn after writing D106**, whose entire content is *re-derive a claim from source
before acting on it.* The rule was fresh and it was still not applied.

**Carry forward — the failure mode has a shape, and it is not carelessness.** B15, D104's remedy, and now
this are the same error three times: **our own derived data is the most seductive false source we have,
precisely because it is right most of the time.** A handoff is obviously a digest and gets some suspicion.
`unit_loadouts.json` feels like ground truth, and it is not — it is the output of a pipeline with known
gaps, and a gap in the pipeline reads exactly like an absence in the world.

**The operational rule:** an absence in our data is never evidence of an absence in the rules. Before
claiming a rule does not exist, grep the *source* — the MFM files, the Wahapedia CSVs, the rulebook — not
the artefact we built from them. And when the claim is load-bearing (a points rule is load-bearing: a
legal list with the wrong total is worthless), it goes in `rules_assertions.py` with its source row or it
does not get acted on.

**Process failure, same session, recorded so it is not repeated.** The S50 turn that introduced this
also reported "Shipped / changed: `OPEN_ITEMS_BACKLOG.md` — new item B35 ... `40K_Decision_Log_v3_0.md`
— D107" *without having written either file*. The report was drafted and the edits were not made. A
`Shipped` section is a claim like any other and gets verified — by grepping the file for the thing that
was supposedly added — before it is written.

## D108 — the base cost does NOT include default wargear. Settled from source, not from New Recruit.

**The open question in B35 was:** Terminator Assault Squad is 155 pts for 5, its default loadout is
thunder hammer + storm shield, and the MFM prices the thunder hammer at 5. Is a default squad 155, or
155 + 25 = 180? B35 held this for Ryan and blocked the engine half on it.

**It is answered in source and did not need to be held.** `MFM_Instructions.txt`, UNITS > Wargear:
*"Some units have a points cost associated with a wargear item they can take. In all cases, these costs
are per item taken, and are applied on top of the unit's main points cost."* Per item **taken**, **on top
of** the unit cost. A default-issue item is a taken item.

**And the Terminator Assault Squad proves it independently.** Its thunder hammer appears only as a default
weapon and as a swap *source* (`unit_loadouts.json` `000000118`: `default_weapons: [Thunder hammer]` on
both groups; the only option replaces `Thunder hammer + Storm Shield` with `Twin lightning claws`). There
is no way to *add* a thunder hammer to that unit. So if the 5 pts did not price the default hammers it
would price nothing at all, and the MFM line would be dead text. Victrix Honour Guard says the same thing
twice more: `banner of Macragge` and `Blades of honour` are both defaults of optional model groups with no
option to add either, and both are priced at 10.

**Decision: (a).** The unit's base cost excludes its wargear. The engine prices the **rolled-up loadout**,
including default-issue items. A default 5-model Terminator Assault Squad is **180**.

Asserted as **B35-1** (the MFM rule text) and **B35-2** (the TAS derivation).

**The lesson, again, and it is the mirror of D107.** D107's rule is *grep the source, not our data*. B35
then held a question for Ryan that the source answered in one sentence — the same failure with the sign
flipped: not trusting derived data too much, but not reading the source at all. **Before escalating a
rules question to Ryan, grep the rulebook and the MFM instructions for it.** An escalation is a claim that
the source is silent, and that claim gets checked like any other.

## D109 — D107's "138 priced entries" is wrong. The real numbers.

Counted from the files: **65** `per <item> N pts` bullets across all 26 MFM faction files; **46** distinct
(datasheet, item) pairs after the Space Marine chapter files' duplicates collapse; **29** of those in the
v1 priority factions; **9** in the units currently present in `units.json` (SM family + Chaos Daemons +
Death Guard). D107's 138 and its "38 in the v1 priority factions" were both estimates written without
counting. Chaos Daemons has **no** priced wargear at all.

The nine live prices, all now in `wargear_points.json`: Terminator Assault Squad `000000118` thunder
hammer 5; Wolf Guard Terminators `000000318` storm shield 5; Thunderwolf Cavalry `000000322` storm shield
5; Redemptor Dreadnought `000002717` macro plasma incinerator 10; Deathwatch Terminator Squad `000003873`
thunder hammer 5; Victrix Honour Guard `000004185` banner of Macragge 10 + blades of honour 10; Defiler
`000004209` hades lascannon 10 + heavy reaper autocannon 10. Twenty more are parsed, resolved to a real
datasheet id, and held out of the map because their units are not in `units.json` yet (Chaos Space
Marines, Grey Knights, Thousand Sons, Emperor's Children, World Eaters, Drukhari); they will appear on
their own when those factions land.

## D110 — a wargear price is keyed by DATASHEET ID, never by unit name and never by item name.

Two independent reasons, both in source.

**Unit names are not unique across factions.** `Datasheets.csv` carries five separate **Defiler**
datasheets — `000000969` (CSM), `000004209` (DG), `000004208` (EC), `000001030` (TS), `000004207` (WE).
A name-keyed lookup would attach the Chaos Space Marines Defiler's price to the Death Guard one. The
parser therefore resolves an MFM line as **(faction of the MFM file, unit name) → datasheet id**, with
the Space Marine chapter files all mapping to faction `SM` (chapters are not separate faction ids in
`Factions.csv`).

**Item names are not globally priced.** Terminator Assault Squad's storm shield is **free**; Wolf Guard
Terminators' storm shield costs **5**. Same item name, different datasheet, different price — the exact
shape of D70/B15 for ability text, now proven again for cost. Asserted as **B35-3** and **B35-4**.

## D111 — an entry's cost is derived from its rollup, not from its option list, and it is recomputed on every render.

`ptsForEntry` (`index.html` v5.58) = the size-bracket cost **plus** `count × cost` for every priced item
found in `loRollup`'s output — both the `weapons` map and the `equipment` map, because a priced item can
be either (Thunder hammer is a weapon, Storm Shield and the banner of Macragge are equipment). Lookup is
`weaponBase(name).toLowerCase()` against `wargear_points.json`, never an exact string: the rollup keeps the
casing of whatever data produced the name and our own data disagrees with itself (`storm shield` in
Terminator Assault Squad's `default_wargear`, `Storm Shield` in Thunderwolf Cavalry's `equipment_parts`).
An exact match would silently under-price and nothing would fail loudly. Asserted **B35-7**.

**Charging off the rollup rather than the option list is the whole point.** The default loadout is priced
(D108), so swapping a priced item *away* has to make the unit cheaper: a 5-model Terminator Assault Squad
is 180, and swapping two models to twin lightning claws takes it to 170. Only the rollup knows what the
unit is actually carrying.

**Consequence: points are derived state.** `entry.points` was previously written only when the size
changed; it is now refreshed for every entry at the top of `renderAll()`, so the per-entry display, the
banner total, and the exported `points_cache` are all the same number from the one function. The three
legacy wargear editors (`editWargearGroup` / `editWargearIndep` / `editWargearBundle`) now call
`renderAll()` instead of `renderDetail()` for the same reason.

**The roster badge shows the smallest legal cost, wargear included.** A unit whose default loadout carries
priced items would otherwise advertise one number in the roster and land in the list at another —
Terminator Assault Squad now reads **180 pts** on its roster card. Product-visible; reversible in one line
if Ryan wants the badge to stay a bare base cost.


## D112 — B15 shipped. The name-keyed glossary was the bug; carrier counting is the rule.

**The engine was reading conferred wargear characteristics out of a table that cannot hold the answer.**
`weapon_abilities.json` is keyed by ability NAME, so the nine Storm Shield carriers in our data collapse to
one string — *"The bearer has a Wounds characteristic of 4."*, which is the **Terminator Assault Squad**
text (`Datasheets_abilities.csv 000000118`). The real texts are three: W4 on the terminator units, **W6** on
Wolf Guard Battle Leader (`000004130`, printed W5), **INV 4+** on Lieutenant, Thunderwolf Cavalry, Vanguard
Veterans, Wardens of Ultramar, Wolf Guard Headtakers. D70 said this in S22 and D105 said it again in S49;
neither was enforced, because the *file the engine reads* still had the flat shape. Nothing wrong shipped
only because the reader was writing INV/FNP and deliberately withholding W/SV — the hold was papering over
the real fault.

**The fix is a data key, not a heuristic.** New file `datasheet_wargear_abilities.json`
(`unit_id -> ability_name -> description`), generated by `ds_wargear_abilities_parser.py` straight from
`Datasheets_abilities.csv` rows with `type = Wargear`, restricted to the 270 units. 38 datasheets, 48 rows.
`wargearAbilityDesc(raw, name)` tries it first and falls back to the flat glossary only when the unit has no
row. Asserted: **B15-8..11**.

**The render rule (D105), made concrete.** `conferredStats(raw, mg, entry)` is the one place it lives:

- every model in the configured statline group carries the item → the override reaches the statline,
  applied **literally, as an absolute set** ("Wounds characteristic of 6" → W6, not +1);
- some but not all → statline untouched, asterisk to the rules text (the D75 convention), now on **W and SV**
  as well as INV and FNP;
- none → the ability is inert: no override, no asterisk, and it drops out of the *configured* Wargear
  Abilities list. The browse popup still lists it, because that popup is the datasheet.

Dynamic on the loadout: Terminator Assault Squad reads **W4** at default (5 shields / 5 models) and reverts
to a starred W3 the moment one Terminator takes twin lightning claws. Wolf Guard Battle Leader reads **W6**,
and W5 with no star once he trades the shield away.

**The trap nobody had hit yet: statline groups are not loadout groups.** `units.json` splits a unit by
*statline*; `unit_loadouts.json` splits it by *loadout group*, and the two namings do not line up — 9 of our
16 named statline groups have no match. A unit-wide carrier count written to one group's statline hands a
Hunting Wolf (`000004131`, W1/Sv6+) the Wolf Guard's 4+ invulnerable save. `statGroupScopes` maps a statline
group onto loadout groups where every model name resolves (normalising the `- Epic Hero` and `*` suffixes);
**where it cannot, the result is capped at an asterisk and a value is never written.** Over-strict is the
correct failure direction here, per D106. An optional group with zero models in the build is a real zero
carriers, not an unknown.

`loCarriers` now counts **gear** as well as weapons — `default_wargear` and an `add` option's `equipment` —
which it did not before. That was invisible until now because gates only ever named weapons. `sweep.js`:
3299 cases, 0 rollup diffs, so nothing else moved.

**Behaviour that changes for Ryan.** E17's static asterisks were a per-datasheet fact; they are now a
per-build fact. Deathwatch Veterans and Decimus Kill Team lose their INV asterisk at default — correct, since
no model carries an Astartes Shield until one is picked — and get it back when a shield is taken. Wardens of
Ultramar keep theirs. Two units gain a real statline value they never had: Terminator Assault Squad (W4) and
Wolf Guard Battle Leader (W6). Ships as `index.html` **v5.59**, `datasheet_wargear_abilities.json` (new),
`ds_wargear_abilities_parser.py` (new), `stat_check.js` (new).

## D113

**A bundle owns the swap it describes; the loadout def never restates it. (B36 — Lieutenant / Captain
wargear.)**

`bundled_swaps.json` and `unit_loadouts.json` can describe the *same* swap, and for the Lieutenant
(`000001346`) they both did: the atomic 3-for-3 — bolt pistol + master-crafted bolter + close combat weapon
becomes neo-volkite pistol + master-crafted power weapon + storm shield — is a bundle endpoint
(`lt-nvp-mcpw-shield`) **and** a loadout choice option (`sng_2`). Both rendered. That is the whole of B36:

- **The neo-volkite pistol showed twice** — once in the bundle picker, once in the loadout panel.
- **The three per-slot panes collapsed into one radio.** B25 merges choice options whose source weapons
  overlap. `sng_2`'s three-weapon `replaces` overlaps all three of the single-slot swaps (master-crafted
  bolter, bolt pistol, close combat weapon), so union-find glued all four into one cluster: one pick allowed,
  everything else greyed. **A legal plasma pistol + power fist build was unreachable.**

Also fixed here: `weaponBase(o.replaces)` was tested against the bundle's managed families as a whole string,
so a compound `replaces` never matched. The Captain (`000000073`), whose bundle is `owns`, therefore failed to
hide its own compound loadout option and drew a second, redundant pane alongside the bundle picker.

**Rule.** A loadout choice option whose replaced-weapon set exactly equals some bundle endpoint's `removes`
set is a re-expression of the bundle and is never rendered — always, not only while the bundle is engaged.
Bundle-managed families are tested part by part. The `alternative` relation still holds: engaging the atomic
endpoint hides the surviving per-slot panes and clears their picks; returning to the default endpoint brings
them back.

**The acceptance test, as corrected by Ryan.** The build is **master-crafted bolter kept + heavy bolt pistol +
power fist** (`Datasheets_options.csv 000001346`: line 3 swaps the bolt pistol for a heavy bolt pistol, line 4
swaps the close combat weapon for a power fist, and line 1 — the master-crafted bolter swap — is simply not
taken). It is legal, it was unbuildable before this change, and it builds now. Nothing on this datasheet
couples the three slots; only the duplicated `sng_2` did, by gluing them into one radio cluster.

**A rules fact worth keeping anyway, found while diagnosing.** On the Lieutenant the **plasma pistol** is one
of the three things the *master-crafted bolter* may be replaced with (line 1) — the bolt pistol's only swap is
the heavy bolt pistol (line 3). So a plasma pistol *costs* the master-crafted bolter, and "bolter kept +
plasma pistol" is an illegal build the tool must go on refusing (D0). Locked in as assertion **B36-1**. No
Lieutenant datasheet in our data carries a master-crafted **bolt rifle**; the only one is Company Heroes
(`000002772`, `Datasheets_wargear.csv`).

Engine only. `units.json`, `unit_loadouts.json` and `wargear_points.json` byte-identical. Ships as
`index.html` **v5.60** with `bundle_check.js` (new build-time harness; 12 assertions, 7 of which fail against
v5.59).

## D114
**B41 + E3 — the datasheet limit becomes a hard block, and red comes to mean "exceeded".**

Per **D0**, legality is the only boundary on validity. A limit the tool merely *flags* is a limit the tool
does not *enforce*: `instanceLimit` already returned 1 for an Epic Hero and `entryHasError` already lit up on
a breach, but `addUnitFromRoster` still pushed the second copy into the list. The player could build an
illegal roster and the tool would only comment on it.

**Scope: every datasheet limit, not just Epic Heroes.** This was Ryan's open call and it was taken on the
recommendation (reversible, one predicate). Epic Hero 1, Battleline and Dedicated Transport 6, everything
else 3 — an add at the limit is now refused outright, with a banner flash naming the unit and its max.

**One predicate, three states.** `limitState(count, limit)` returns `ok` / `at` / `over`, and the roster
card, the add path and the detail flag all read it, so they cannot drift apart:

- `ok` — below the limit. The add is allowed.
- `at` — exactly at the limit. **The add is refused.** The card renders disabled (dimmed, amber count). This
  is E3: reaching the max is a full box, not an error, so it is never red.
- `over` — past the limit. Now unreachable through the UI, but still reachable from an imported or
  pre-v5.61 saved list, so it stays a visible red error the player can see and fix. `entryHasError` and the
  detail-panel over-limit flag are unchanged in meaning.

**Source caveat — read this before touching the numbers.** The limits themselves are **not sourced from any
primary rules document in this repo**. `wh40k_core_rules_small_3_7MB.pdf` is the Core Rules only: it has no
army-construction / matched-play section, and a grep of all 88 pages turns up no datasheet-count limit
whatsoever. The numbers 1 / 6 / 3 come from our own Decision Log (instance-limit entry) and
`40K_Functional_Spec_v0_7.md`. Per **D107**, an absence in our data is not an absence in the rules — but by the
same token our own decision log is not a source. This change enforces a rule we have not yet verified. That
was already true in v5.60; it just did less damage while the rule was only advisory. **Whoever next has the
matched-play text should re-derive 1 / 6 / 3 and re-point assertion B41-2.** Flagged to Ryan.

Engine only. `units.json`, `unit_loadouts.json` and `wargear_points.json` byte-identical. Ships as
`index.html` **v5.61** with `limit_check.js` (new build-time harness, 24 assertions) and assertions
**B41-1**, **B41-2**, **E3** in `rules_assertions.py` (**31/31**).

## D115
**The limits depend on the battle size. `Army_Muster_Rules.txt` arrived, and D114's numbers were wrong.**

D114 shipped a hard block on datasheet limits and recorded, as a debt, that the numbers had no source in the
repo. Ryan then loaded **`Army_Muster_Rules.txt`** — GW's 11th-edition "Mustering Armies" text. It has the
table, and the table does not say what we said.

**`Army_Muster_Rules.txt` 25.03, "Select Battle Size":**

| Battle size | Points | DP | Enhancement limit | Unit limit* |
|---|---|---|---|---|
| INCURSION | 1000 | 2 | 2 | **2** |
| STRIKE FORCE | 2000 | 3 | 4 | **3** |

*Footnote, verbatim in substance: the unit limit for BATTLELINE and DEDICATED TRANSPORT units is **double**
the amount shown, and every EPIC HERO has a unit limit of **1**, regardless of the battle size.*

So the limits are **Incursion 2 / 4 / 1** and **Strike Force 3 / 6 / 1**. The flat `3 / 6 / 1` the engine has
carried since long before D114 is **the Strike Force row applied to both battle sizes.** At Incursion it let
the player take a third of any datasheet, and a fifth Battleline. That was a silent legality hole for as long
as the code has existed; D114 did not create it, but D114 *enforced* it, which is what made it findable.

**This is the D107/D114 lesson landing with force.** The numbers looked right, every list-builder on the market
uses 3/6, and they were wrong anyway — because nobody had read the source. A rule that is not executable
against a cited source is a rumour.

**The fix.** `battleSizeUnitLimit(pointsTotal)` returns 2 at ≤1000 and 3 above; `instanceLimit(unitType,
pointsTotal)` doubles it for Battleline and Dedicated Transport and overrides Epic Hero to 1.

The limit is now **derived live, never frozen.** It used to be baked onto each `allUnits` record at
`setActiveUnits` time — which was already a latent bug, because *both* the create path and the open path call
`setFaction()` **before** they set `POINTS_CAP`. Every unit record was built against the default 2000 and
never corrected. `unitLimit(u)` reads `POINTS_CAP` at render time instead, and `selectArmyPoints` now calls
`renderAll()` so the roster redraws when the battle size moves.

**A list can now become illegal without being edited.** Three Captains is legal at Strike Force and over-limit
at Incursion, so switching battle size can push a saved list into the red. That is correct — it is exactly why
D114's `'over'` state had to stay reachable after the add was blocked, and it is the first real use of it.

**What this file also unblocks** (recorded here, not built here):

- **E1 / E4 — detachments and enhancements.** 25.03 gives the DP budget (2 / 3) and the enhancement limit
  (2 / 4). 25.04 adds: you cannot select the same detachment twice; no unit — *including attached units* —
  may have more than one enhancement; only CHARACTER units may take enhancements; EPIC HEROES cannot; an army
  cannot include more than one of the same enhancement. `Upgrade`-tagged enhancements are the exception: they
  may go on non-Characters, up to three of the same, and the 2nd and 3rd do not count against the enhancement
  limit though they still cost points.
- **E9 — Warlord.** 25.04: select **one** CHARACTER *unit* carrying the army faction keyword, then one
  CHARACTER *model* in it. Units whose datasheet says they must be the Warlord force the pick; a "cannot be
  your Warlord" rule beats a "must be". This is the rule E9 was missing.
- **B38 — leaders.** 25.04: every **support** unit *must* be attached to a bodyguard unit. That is a hard
  legality constraint the tool does not check today.

Engine only. `units.json`, `unit_loadouts.json` and `wargear_points.json` byte-identical. Ships as
`index.html` **v5.62**. Assertions **B41-1..3**, **E3**, **D115** in `rules_assertions.py` (**33/33**) —
`B41-3` reads the battle-size table out of `Army_Muster_Rules.txt` itself, so if GW reissues it the assertion
breaks before the engine drifts.

## D116 — B18's rule was backwards, and the source says so. A swap is NOT confined to its model group.

**The claim we were about to build on.** The S56 prompt, the handoff chain and the project memory all
carried the same sentence: *an equipment add applies unit-wide including the sergeant; a weapon swap stays
scoped to its own model group.* It is attributed to a call made in S49 "against New Recruit's Reiver panel".
There is no such entry in this log. It is a summary of a summary, and it is wrong.

**What the source says.** The scope of an option is whatever its own sentence says, and nothing else.

- `Datasheets_options.csv 000000118 line 1` — *"**Any number of models** can each have their thunder hammer
  and storm shield replaced with 1 twin lightning claws."* A generic *model*, not "Assault Terminator". The
  swap reaches the **Assault Terminator Sergeant**. Our data scopes it to `Assault Terminators` only.
- `000002718 line 1` — *"**All models in this unit** can each have their combat knife replaced with 1 bolt
  carbine…"* and `line 2` — *"**If the Reiver Sergeant is equipped with 1 bolt carbine**, it can be equipped
  with 1 combat knife."* Line 2 is unreachable text unless line 1 reaches the Sergeant. **The gate proves the
  scope.** This is the same dormant option D84 filed and B19 built the engine for; it has been dormant for
  27 sessions because the swap was scoped away from the model the gate names.
- `000001044` — all five per-5 swap lines say *"1 **Plague Marine's** boltgun"*. The body model is **named**,
  so the Plague Champion is correctly out of scope. **B18 must not widen these.**

So the rule is not add-vs-swap. It is **generic-model vs named-model**: a sentence that says *models* means
every model group, leader included; a sentence that names the body model type means that group only. Both
adds and swaps come in both forms. The prompt's version got the right answer on the adds by accident and
the wrong answer on every swap.

**Asserted: B18-1, B18-2, B18-3.** The three source rows above are now executable, so the false sentence
cannot come back.

**B18 is a DATA turn, not an engine turn.** The engine already has every mechanism the fix needs — an option
scoped to a leader group, and a `pool_id` to share one cap across groups, are both in the shipped file today
(Intercessor `grenade_launcher` / `grenade_launcher_sgt`, Reiver `add_3` / `add_4`). What is missing is the
**scope on the option**, and the scope is written by `loadout_parser.py`. Nothing in `index.html` can recover
information the parser threw away. **B18 therefore sits behind the parser rebuild**, which is now the critical
path for B18, B42 and B43 alike.

**Size of the fix.** 21 in-roster units carry a generic unit-wide sentence and have a leader group. At least
11 of them exclude the leader from every option today (Terminator Assault Squad, Inceptor Squad, Vanguard
Veterans with Jump Packs, Ravenwing Black Knights, Thunderwolf Cavalry, Centurion Devastators, Blightlord
Terminators, Aggressors, Centurion Assault, Ravenwing Command Squad, Deathwatch Terminators, Decimus Kill
Team). The rest have leader-scoped options for *some* lines and not the generic one; the per-option split is
the parser's job to redo, not a hand count's.

**Consequence worth naming.** D112's storm-shield case only becomes reachable once B18 lands: the Assault
Terminator Sergeant cannot lose his shield today, so the all-carriers test can never go false and the
conferred W4 can never revert. The conferred-characteristic engine is correct and untested against its own
negative case until then.

## D117 — E14: a free, ungated, unpooled, one-off add defaults to selected. Narrow on purpose.

**Shipped, v5.63.** `loIsFreeDefaultAdd` + `loadoutDefaultWargear`; `addUnitFromRoster` seeds
`entry.wargear` instead of starting it empty. **53 options across 33 units** now arrive ticked — the
hunter-killer missiles, storm bolters, havoc launchers, multi-meltas, Icarus pods, ironhail stubbers, the
Watcher in the Dark, the Sanguinary Banner, the Daemonic Icon and the Instrument of Chaos. Nothing about the
rollup, the points or the render changed: `sweep.js` 3299 cases, 0 diffs, because the engine's *behaviour*
for a given selection is identical. Only the *initial* selection moved.

**"Free" is checked against the MFM, not against our own file.** `wargear_points.json` naming nothing is not
evidence that nothing is priced (D107). `E14-1` therefore rebuilds the prices from the MFM WARGEAR OPTIONS
blocks with the real `mfm_points_parser`, confirms the committed file reproduces, and then confirms no seeded
item is priced **for its own unit**. That last qualifier is load-bearing and was found by the assertion
failing: the MFM does print *"per Multi-melta 10 pts"* — on an **Adepta Sororitas** datasheet. A Land
Raider's multi-melta is free, and a corpus-wide grep would have condemned it.

**The seed is a one-shot, and that is the whole of the mechanism.** It is written when the unit is added from
the roster. A saved list is never re-seeded on load, so no existing list changes under the player. The
toggle is untouched: `editLoadoutAdd` still clears it. A default is a convenience, never a lock.

**Excluded, deliberately, and this is the design.** The seed cannot follow a value that moves after it is
written, so anything whose "on" is not a fixed 1 stays out:
- **priced adds** — the cost is the reason not to take it (the E14 blocker, now enforceable);
- **per-N / pooled adds** (Reiver grav-chute and grapnel launcher; Intercessor grenade launcher) — the
  control is a *stepper*, its ceiling moves with unit size, and a seed of "max at size 5" reads as "5 of 10"
  the moment the squad grows;
- **gated adds** (`requires_weapon`, 11 options) — the gate can break and heal after the seed.

Making the default *live* rather than one-shot needs a tri-state selection (unset / on / off) so that "the
user cleared it" is distinguishable from "never touched". That is a real mechanism change, it rewrites every
saved list on load, and it buys 4 stepper options and 11 gated ones. **Not taken.** Surfaced to Ryan.

**Asserted: E14-1, E14-2.** `default_check.js` (new) loads the real predicate out of `index.html` and proves
the rule is *total* — every qualifying add is seeded and no other kind ever is — so it cannot decay into a
hand-picked list.

## D118 — `loadout_parser.py` rebuilt to the committed file, and the freshness gate is now machine-enforced

**Session 57. Data turn (parser only). `index.html`, `units.json`, `unit_loadouts.json`, `wargear_points.json`
unchanged — verified with `cmp`.** Closes the ten-session stale-parser failure.

**What the stale copy was actually missing.** Run fresh against source, the pre-S47 parser reproduced 200 of
217 units exactly and got 17 wrong, in four distinct ways. This is the real inventory, not a guess:

1. **No equipment resolution on the gain side.** A storm shield, a relic shield, a blizzard shield, an
   Astartes shield, a Terminator storm shield and a Centurion assault launcher are *wargear*, not weapons.
   They are in `weapon_abilities.json`; the parser only consulted the weapon index, so it emitted
   `WEAPON_NOT_FOUND` and no `equipment_parts`. **13 options** carry `equipment_parts` in the committed file.
   Fixed by **`resolve_part`** — weapon index first, equipment allowlist second, flag only if neither.
   `equipment_parts` is collected from the **gained** side only; equipment named on the `replaces` side
   (`000000118` "Thunder hammer + Storm Shield", `000000311` "Death Totem") resolves to its display name and
   is not listed, because the engine only needs to know which parts a model *gains* are non-weapons.
2. **A compound gain on a single swap was truncated to its first weapon.** `000000083 line 3` — *"…can be
   replaced with 1 thunder hammer and 1 relic shield"* — resolved to **"Thunder hammer"** alone, silently,
   with no flag, because the loose prefix fallback in `normalise_weapon` matched the whole phrase to the
   first weapon in it. The `count` family already split compound gains; the `choice`/`single` family did not.
   Now both do, via `replacement_raw` + `split_compound_replacement`.
3. **The gate phrase could not be compound or article-led.** `classify_conditional_add` required a
   count-led gate (`\d+\s+`), so *"If this model is equipped with **an** absolvor bolt pistol"*
   (`000004135 line 2`) and *"…with **a** heavy bolt pistol **and an** Astartes chainsword"*
   (`000000083 line 4`) both fell through to UNMATCHED. **`_gate_parts`** now strips articles and counts,
   splits on `and`/comma unless the phrase is itself a known 'and'-named weapon, and joins with ` + `.
   This is what produces D103/B32's compound gate.
4. **Two whole sentence shapes had no classifier.** **`classify_bearer_add`** — *"1 Wolf Scout **equipped
   with** a plasma pistol can be equipped with 1 haywire mine"* (`000004182 line 2`), the model-side spelling
   of the same gate. **`classify_negated_gate_add`** — *"1 Plaguebearer **that is not equipped with** a
   daemonic icon can be equipped with 1 instrument of Chaos"* (`000004113`, `000004114`), which per **D106**
   emits two independent, ungated, unpooled single-model adds, because the exclusion is per **model** and the
   body group always holds two or more.

**One further correction, not a capability.** The parser emitted a definition for every SM/DG datasheet in
`Datasheets.csv` — **368**, against the committed **217**. `Datasheets.csv` is the faction; `units.json` is
the roster. Emission is now restricted to datasheets the app can actually field.

**Result: the rebuilt parser plus the equipped chain reproduces the committed `unit_loadouts.json`
byte-for-byte** (five faction `web.txt` passes SM -> DG -> BT -> DA -> SW, then the `--datasheets` pass).
Re-running the chain on the committed file returns the committed file — the fixed point holds. Zero-diff on
options, flags, model groups, defaults and `_defaults_source`, and `cmp` clean.

**The gate is now a test, not a checklist.** Asserted as **P1** in `rules_assertions.py`: the parser must
define `resolve_part`, `_gate_parts`, `classify_bearer_add` and `classify_negated_gate_add`. A written
freshness check failed **ten sessions running**; the same claim as an assertion fails the build in one line.
This is the same lesson as D107 — a fact that is not executable does not hold.

**Unblocked by this:** B18 (data half), B42, B43 — and, through B18, the only negative test D112's
conferred-characteristic engine has ever had.

---

## D119 — the S57 parser did not survive into S58, and the rebuild is now reproducible from the log

**Session 58. Data turn. `index.html` byte-identical (verified with `cmp`).**

`loadout_parser.py` arrived in S58's project knowledge as the **pre-S47 stale copy again** — the twelfth
consecutive session, and the first one caught by a *test* rather than by prose: assertion **P1** failed on the
baseline run. The S57 rebuild (D118) was correct and was delivered; it simply never landed back in the
project. **This is not a parser bug. It is a file-custody failure, and no amount of parser work fixes it.**

**The rebuild was redone from D118's own inventory** — which is the point of writing that inventory down. All
four capabilities restored: `resolve_part` (weapon index first, `weapon_abilities.json` equipment allowlist
second, flag only if neither), `_gate_parts` (article-led and compound gate clauses), `classify_bearer_add`,
`classify_negated_gate_add`; plus the compound-gain split on the `choice`/`single` path via `replacement_raw`,
and emission restricted to the roster (217, not `Datasheets.csv`'s 368). Validated the same way S57 was: fresh
parse of all 215 parser-generated units + the two hand-authored entries (`000001157`, `000001044`) + the five
faction `web.txt` passes + the `--datasheets` pass reproduces the committed `unit_loadouts.json`
**byte-for-byte**, and re-running the chain on it returns it. Fixed point holds.

**The durable fix is custody, not code.** `loadout_parser.py` must live in the GitHub repo as the canonical
copy, with project knowledge as a mirror refreshed after any session that touches it. Until it does, P1 will
keep firing and every parser-dependent turn will keep paying this tax. P1 remains the tripwire — it now costs
one assertion run to detect what previously cost a session to discover.

---

## D120 — B18 is two items, not one: `pool_id` is honoured only on `type: 'add'`

**Session 58.** D116 settled the *rule* (generic model = every group, leader included; named body model =
that group only). Implementing it exposed a mechanism gap the ticket did not know about.

**Source row.** `index.html` builds `poolCap` at lines ~2989-2999 and consumes it at ~3103 and ~3119 — both
consumption sites sit inside `for (const o of opts) if (o.type === 'add')` / `const addOpts = opts.filter(o
=> o.type === 'add')`. `countOpts` (swaps) never read `poolCap`. **A shared cap can span model groups on an
add and cannot on a swap.**

That splits the generic sentences in two:

- **Uncapped generic swaps** — *"Any number of models…"*, *"All models in this unit…"* — have no unit-wide cap
  to share. Each group's ceiling is its own model count. These fan out to one option per model group and are
  correct with **no engine change**. **Shipped this session (B18a).**
- **Capped generic swaps** — *"For every 5 models in this unit, 1 model's X…"*, *"Up to N models…"* — carry a
  cap computed against **unit** size. Fanned out across groups without a pool they would grant the allowance
  once *per group*, which is over-permissive: strictly worse than today's under-permissive body-only scope.
  These are **left body-scoped** until the engine can pool a cap across `count` options. Filed as **B18b**
  (engine) and **B18c** (data). Affected: Ravenwing Black Knights `000000241`, Thunderwolf Cavalry
  `000000322`, Ravenwing Command Squad `000002748`, Deathwatch Veterans `000002783`, Indomitor `000002781`,
  Fortis `000002780`, Talonstrike `000003874`.

**Named-body sentences are untouched, and that is asserted** (B18-5): Plague Marines' five per-5 lines all
name *"Plague Marine"*, so the Plague Champion still has exactly the two options the datasheet gives him.

**D112's negative case now runs and passes.** With the Assault Terminator Sergeant able to trade his thunder
hammer and storm shield for twin lightning claws, a 5-model squad can reach **zero** storm-shield carriers.
At zero carriers the conferred W4 does not merely lose its override — it goes **inert**: no override, no
asterisk, the ability does not render. Asserted in `stat_check.js`. This is the only negative test the
conferred-characteristic engine has ever had, and it passed on the first run with `index.html` unchanged.

**Cost, and it is a real one: option ids churn.** The fan-out inserts an option, so ids shift within every
affected unit (`000000118` `cnt_1` was the body swap and is now the Sergeant's; the body is `cnt_2`).
Saved lists key `wargear` / `other_options` by option id (`list_store.js serializeEntries`), so a list saved
before this change will silently mis-resolve its picks on the ~20 affected units. Accepted: the app is
pre-release, and the alternative — stable semantic ids on every parser-generated option — is a schema change
with no other justification. Reversible if that judgement is wrong.

---

## D121 — B43 is not a data gap; it is B44

**Session 58.** Wardens of Ultramar `000004188`. The ticket asked whether the Refractor Field had no carrier.
It has one: the loadout def gives the *Gaius Silva - EPIC HERO* group `default_wargear: ['refractor field']`
and *Veteran Sergeant Metaurus - EPIC HERO* `['storm shield']` (`unit_loadouts.json 000004188`,
`_defaults_source: equipped`).

The mismatch is upstream of that. `units.json 000004188` carries **two** statline groups — *"Ancient Gadriel,
Veteran Sergeant Metaurus"* and *"Gaius Silva, Aemelia Minervas, Dainal Kornelius, Lucia Vestha"* — each
listing **both** wargear abilities, because the statline split and the loadout split are different partitions
of the same six models and neither can address the other. That is exactly **B44**. D112 asterisks rather than
guessing, which is the safe answer. **B43 is closed as a duplicate of B44**; no data change was made, and
none should be.

---

## D122 — B46: the popup's wargear-ability list is sourced from the datasheet, not from units.json

**Session 59.** `units.json → model_groups[].wargear_ability_names` carries **default-issue gear only**, and
both popups built their Wargear Abilities list from it. Every ability granted by an *option* was therefore
unreachable: 12 abilities across 8 units, including the Reiver's Grav-chute and Grapnel Launcher
(`Datasheets_abilities.csv 000002718` lines 5-6, `type = Wargear`). The text was never missing — the channel
was wrong.

**Decided.** `allWargearAbilityNames(raw)` = the unit's `wargear_ability_names` **unioned with the keys of
`datasheet_wargear_abilities.json[unit_id]`**. Both popups name their abilities from it, so the unreachable
count is structurally zero rather than incidentally zero.

- **Browse popup** (the datasheet view): lists **all** of it, default-issue and option-granted alike. That is
  what the printed datasheet shows.
- **Configured popup**: filtered by carrier count on **D112's three-way rule** — every model carries it ->
  plain row; some carry it -> row marked with an asterisk and a one-line note; none -> the row is not
  rendered at all.

**Carrier count is unit-wide here**, not per statline group: the popup's Wargear Abilities section is a
unit-level section, so `wargearCarrierStateUnit` sums `loCarriers` over every loadout group. Precedence for
"is it on": bundle grant -> loadout (canonical wherever the item is representable there — the Reiver
grav-chute is *both* a loadout add and a B14 other-option, and the loadout wins) -> B14 other-option checkbox
-> default-issue. A unit-wide aura from a single bearer ("models in the bearer's unit have…") reads as `all`
on one carrier, exactly as the statline pass already reads it.

**One real bug fixed underneath.** `loDefNamesItem` never looked at `o.equipment`, so an equipment add — the
whole class of item B46 is about — was invisible to the carrier counter and fell through to the legacy
"assume it is default-issue" heuristic. Now eaten with the rest.

**Statline untouched.** `conferredStats` still names its abilities from `wargear_ability_names`. Widening
*that* would move printed characteristics and is not what B46 asked for; the two datasheets where an
option-granted item confers a stat (`000000118`, `000000147` storm shields) already list the name, so there is
no gap to close. Noted, not built.

**B46-2 re-pointed.** The old assertion counted the data gap, which an engine fix cannot move. It now asserts
the engine's channel — `allWargearAbilityNames` is defined and used by **both** popups — and that nothing in
`datasheet_wargear_abilities.json` falls outside the union. Behaviour is proven in `stat_check.js` on the
Reiver (loadout add), the Infiltrator (other-option aura) and the Terminator Assault Squad (default-issue).


---

## D123 — the parser-freshness guard is now executable and covers the whole pipeline

**Session 59, before B46.** `loadout_parser.py` arrived stale for twelve consecutive sessions (D119). The
only thing standing against it was P1, which checked that four function names existed. That is too weak on two
counts: it passes on *any* wrong copy that keeps the names (a partial rebuild, a future stale version, a file
with the names but not the behaviour), and it guards nothing but the parser — `units.json`, `index.html`,
`unit_loadouts.json`, `wargear_points.json` and `datasheet_wargear_abilities.json` had no guard at all. The
root cause is a human file-custody step (delete-then-upload) and it recurs regardless of any written checklist.

**Built, in this order, as tooling that touches no data and no engine:**

1. **`pipeline_manifest.json` + `manifest_check` (assertion P3).** SHA-256 of every guarded pipeline file — the
   five outputs, both parsers, the rest of the transform scripts, the harnesses and the assertion files (21 in
   all). A wrong copy of any of them fails on line one and names the file. Regenerated at session close
   (`python3 pipeline_manifest.py --write`) so a deliberate change is simply re-baselined; what it catches is
   *unintended* drift between close and next open. Source CSV/txt inputs are deliberately not pinned — they
   change legitimately on GW updates and pinning them would fire on every real refresh.

2. **`repro_check.py` (assertion P1, rewritten).** The executable form of "the parser is fresh." Seeds a work
   copy of `unit_loadouts.json` with only the two hand-authored entries (`000001157`, `000001044`), runs
   `loadout_parser.py` from source to regenerate the other 215, runs the five faction `web.txt` passes
   (SM → DG → BT → DA → SW) and the final `--datasheets Datasheets.csv` pass, and asserts the result is
   **byte-identical** to the committed file. It does not care what the parser is called or which functions it
   defines — only whether the file on disk still produces what is committed. A stale, partial, or renamed
   parser cannot pass. It **subsumes and replaces** P1's old function-name check.

**Division of labour, stated so it is not mistaken for a gap.** The manifest is the cheap first line (any byte,
any file); the repro gate is the correct backstop (behaviour, the parser + `unit_loadouts.json`), and it catches
a bad parser even if the manifest is itself stale. The repro gate copies the two hand-authored seeds from the
committed file, so it does **not** re-derive those two from source — there is no source to derive them from,
which is why they are hand-authored; the manifest guards them by hash instead. Inert changes (a trailing
comment, a behaviour-preserving rename) pass the repro gate and are caught by the manifest — that is the
intended split, not a hole. Both were proven by tampering: the manifest caught a one-line comment append and a
hash change; the repro gate caught a parser-generated unit divergence and named the unit, while correctly
passing a seed-only change.

**P2 (D119) is superseded on the technical half.** Moving the parser into the repo remains the durable custody
fix and is still Ryan's call, but the pipeline is now self-defending regardless of where the parser lives: a
wrong copy fails the baseline immediately and by name.

## D124

**B47 — information buttons in the Configuration Panel. Engine only; `unit_loadouts.json` and `units.json`
byte-identical.** `index.html` v5.64 → v5.65.

Every selectable row in the Configuration Panel now carries an **eye** icon that opens an inline expander with
the detail for that one item — a weapon profile (Range / A / BS-WS / S / AP / D / Abilities) when the datasheet
has one, otherwise the item's rules text via `wargearAbilityDesc`, otherwise a short "no profile or rules text"
note. Compound labels ('Heavy flamer + Dreadnought combat weapon') are split and each part resolved on its own.
Every group heading carries a **list (☰)** icon that opens the detail for *every* item the group offers at once
(deduped by base name), plus a **(picked / allowed)** counter. Both work at every nesting level, including the
weapons a bundle endpoint adds (the endpoint eye shows each added weapon's profile, the grants' text, and a
"Removes:" note). Detail lands as an **inline expander under the row** — Ryan's one open shape call; chosen over
a popup (which would cover the narrow panel) and a side-sheet, matching New Recruit, which opens in place.

Mechanism: a read-only DOM toggle (`toggleDetail`) that does **not** re-render the panel, so an open expander
survives until the next *selection* change (which rebuilds the whole panel via `renderAll` and collapses every
expander). That collapse-on-select is accepted for v1; preserving open state across a rebuild would need the
open ids tracked in entry state and is deferred.

**Counter semantics (a display call made as dev-manager, reversible).** `allowed` = the group's total selectable
capacity from the data we already hold (`loMaxCount`, pool caps, 1 per choice slot / bundle); `picked` = how many
are currently selected (sum of counts, 1 per chosen swap/add, 1 per non-default bundle endpoint). A choice group
reads `0/1` until a swap is taken. This is the natural "N of M taken" reading; if Ryan wants a different
numerator/denominator (e.g. counting the 'keep' as a pick, or per-model rather than per-slot) it is a one-line
change per surface.

Surfaces touched: `buildLoadoutHtml` (grouped by option-group so each heading can carry the counter + ☰),
`buildWargearHtml` (Replace / Optional Swap / bundle headings), `buildOtherOptionsHtml` (Unit Options heading;
granted rows also get an eye). New helpers: `toggleDetail`, `infoBtn`, `mkDetail`, `weaponProfilesFor`,
`miniWeaponTable`, `itemDetailHtml`, `groupDetailHtml`, `endpointDetailHtml`. `loChoiceRow`, `loChoiceRowX`,
`loStepper` gained an optional trailing `detail` param.

`bundle_check.js` engine loader extended to pull the new detail block and stub `dsWargearAbilities` /
`glossaryDesc`, since `buildLoadoutHtml` now references the detail helpers. No assertion logic changed.

## D125

**B48 — Corvus Blackstar `000000358` no longer renders two controls for the same wargear.** Closed with B47
since both touch the same panel.

Source (Datasheets_options.csv `000000358` line 4, D113): "This model can be equipped with **one of the
following**: 1 auspex array / 1 infernum halo-launcher." The loadout parser expressed this as `ach_4`
(`type: choice`, `replaces: null`, `choices` = the two items). Because `replaces` is null, `buildLoadoutHtml`
renders a **None** row alongside the two choices, so the loadout control already expresses *take neither* — the
precondition for suppressing the duplicate B14 checkboxes is met, the empty state stays reachable.

Fix: `buildOtherOptionsHtml`'s duplicate-suppression, which matched an other_option name only against a loadout
option's `label`/`group`, now also matches against the item names inside `choices` / `equipment_choices` /
`equipment`. A full scan of all 270 units confirmed the widening suppresses exactly Corvus's two other_options
and nothing else, so the blast radius is the one unit the S59 sweep already named. Corvus now offers auspex
array / infernum halo-launcher through the single `ach_4` radio (None / Auspex / Infernum).

## D126

**B18b — `count` options now draw from the shared pool cap (`pool_id`).** Engine only; `unit_loadouts.json`
and `units.json` byte-identical (verified with `cmp`). `index.html` v5.65 → v5.66.

Before this session, `pool_id` was read only inside the `type === 'add'` branch of `loRollup` (D120). A `count`
option that carried a `pool_id` — a capped generic swap where several named replacements share one ceiling —
ignored the shared cap: each option clamped only against its own `loMaxCount`/`reqCap`, so two co-pooled swaps
could each hand out up to their individual max, blowing past the pool. This is a latent gap: no committed unit
carries a pooled `count` yet, but B18c will fan capped generic swaps onto seven units, and the engine has to be
ready first (data turn and engine turn never mix).

Fix, mirroring the add branch:
- **`loRollup` count loop** — after `cap = min(loMaxCount, reqCap)`, if the option has a `pool_id` the cap is
  further bounded by remaining pool capacity (`poolCap - poolUsed`), and the amount actually consumed is added
  back to `poolUsed`. So the first co-pooled option drawn consumes the pool and later ones clamp to the
  remainder — they lock each other out, exactly as pooled adds do. Pool ordering within a body group is
  add-first then count, and `poolUsed` accumulates across scopes (leader draw already counted before a body
  group's counts run), so a Sergeant add + body count sharing a pool subtract correctly.
- **`buildLoadoutHtml`** — both count branches (plain and `replacement_choices`), in both the group
  `picked/allowed` counter and the stepper `max`, now read the pool the same way the add branch does, capping at
  `pool - leaderUsed`.

**Deviation from a literal mirror (dev-manager mechanism call):** the add branch UI *replaces* its computed max
with `pool - leaderUsed`; the count branches instead take the `min` of the existing cap and `pool - leaderUsed`.
Reason: a count's `reqCap` (source-weapon carriers) is a real physical constraint the add branch doesn't have —
a hard replace could offer more swaps than there are source weapons to swap, which `loRollup` would then
silently clamp, a UI/enforcement mismatch. `min` keeps the shown max consistent with what `loRollup` enforces,
and reduces to the add-side behaviour when `reqCap` is `Infinity`.

Known display quirk (pre-existing, not introduced here): when two options share one pool, each contributes its
own `pool - leaderUsed` to the per-group `picked/allowed` counter, so `allowed` over-reports the shared ceiling.
The aggregate pool line (`buildLoadoutHtml` line ~3443, `opts.find(o => o.pool_id)`) already prints the true
`used of pool` for any pooled option including count, so the real cap is visible. Same quirk exists on the add
side today.

Verified: synthetic `loRollup` test (5-model Boltgun group, two count swaps sharing a pool of 2) — requesting
2+2 yields exactly 2 total swaps with 3 Boltguns kept and no `overAllocated`; 1+1, 2+0, 0+0 all correct. All
six node harnesses pass; `repro_check.py` byte-identical; `integrity_check.py` 0 blocking. UI branches are
guarded by `o.pool_id` so committed (unpooled) rendering is unchanged; the new UI paths stay dormant until B18c.

## D127

**B18c — capped generic swap fan-out: the ticket's uniform premise was wrong; re-scoped to two units, three deferred to new B18d, two are no-ops. No data or engine change this session — this entry is the analysis and the corrected plan.**

B18c as written said: fan the seven capped generic swap sentences onto their model groups with a shared `pool_id`. Read against source, the seven units are **not** one uniform job. They split three ways, and the naive "fan onto every group" the ticket implies would ship a real bug on at least one of them. The split, with source rows:

**Clean — safe to fan, no engine work needed (the true B18c):**
- **Ravenwing Black Knights `000000241`** (`Datasheets_options.csv` L1): "For every 3 models in this unit, 1 model can replace its plasma talon with 1 Astartes grenade launcher." Groups: Ravenwing Huntmaster (fixed 1) + Ravenwing Black Knights (body). Both carry Plasma talon. Today `cnt_1` is scoped to the body only, so the Huntmaster — a generic model under D116 — cannot take the swap. Under-grants.
- **Ravenwing Command Squad `000002748`** (L1): "For every 3 models in this unit, 1 model's plasma talon can be replaced with 1 Astartes grenade launcher." Groups: Champion + Apothecary + Ancient (all fixed 1, all carry Plasma talon; unit is exactly 3 so the cap is 1). Today `cnt_1` is scoped to the Ancient **only** — a **live legality bug**: the rule lets any one of the three models take it, the tool offers it on one model. This is exactly the class of defect the tool exists to prevent.

Neither clean unit has any competing option on the replaced slot, so fanning them creates no double-swap. These two are the real, shippable B18c.

**Leader-conflict — deferred to new B18d, gated on a same-slot exclusion mechanism (relates to B39):**
- **Thunderwolf Cavalry `000000322`**: generic per-3 Bolt pistol → Plasma pistol (`cnt_3`, L2), but Bolt pistol is already the replaced slot of `cc_1` (Pack Leader) *and* `cc_2` (body) from the L1 "Any number" swap. Contested on both groups.
- **Deathwatch Veterans `000002783`**: generic per-5 "Boltgun + Power weapon" menu (`cc_1`..`cnt_7`, L1-L7), but the Watch Sergeant's `sng_8` (Power weapon → xenophase, L8) and `sng_9` (Boltgun → combi, L9) contest the two components of that compound slot.
- **Talonstrike Kill Team `000003874`**: generic per-5 Heavy bolt pistol → Plasma pistol (`cnt_3`, L3), but the Sergeant's `cho_1` (L1) contests Heavy bolt pistol.

For these three, D116 says the leader/sergeant **is** an eligible generic model, so it should get the pooled swap — but it also carries its own named swap on the same weapon, and a model can only replace a given weapon once. Correct behaviour is *either the generic swap or the named swap on that slot, not both* — a same-slot mutual-exclusion the engine does not yet do (the B39 family of work). Fanning them now without that exclusion would let a leader take two swaps of one weapon: illegal. So they wait for the mechanism.

**No-op — nothing to fan:**
- **Indomitor Kill Team `000002781`** (L1, "For every 5 models… Deathwatch heavy bolt rifle → Deathwatch heavy bolter"): only the Kill Team Heavy Intercessors group carries that rifle; the two variant groups (with power fists / with melta rifles) carry different weapons. Correctly scoped to the one carrier today. **This unit is the proof that a blind fan is wrong** — see the layering finding below.
- **Fortis Kill Team `000002780`**: has no generic capped per-N *count* swap. Its per-5 line (L3) is a bearer-gated *add*, a separate concern.

**The discriminator that yields correct, safe results:** fan a generic capped per-N count onto every group that carries the source weapon, **except** where that weapon is already the replaced slot of another option in the unit (a same-slot contest). Applied to the seven: it fans the two clean units, skips the three contested ones, and leaves the two no-ops alone. For this session's purpose the simplest provably-equivalent gate is *"fan only when the source weapon is contested by no other option anywhere in the unit"* — a strict, conservative subset that maps to exactly the two clean units and provably changes nothing else.

**Why this is a docs-only session — the layering finding (the reason not to ship the two clean units now):** doing the fan *correctly in general* needs to know which groups actually carry the source weapon. That per-group weapon knowledge does not exist at the `loadout_parser.py` stage — the parser assigns the same base-weapon set to every group (it fills `default_weapons` identically for all groups and marks it for review). Real per-group weapons are spliced in later by `equipped_parser.py` from the faction `web.txt` files. And `equipped_parser.py` does **not** prune an option off a group that lacks the replaced weapon (it only normalises weapon names and sets defaults). So a fan implemented in `loadout_parser.py` would hang a swap option on groups that don't carry the weapon, with nothing downstream to remove it. For the two clean units this happens to be harmless — every group carries Plasma talon — but as a general mechanism it is wrong, and **Indomitor is the counter-example**: a blind fan of its L1 would add a Deathwatch-heavy-bolt-rifle swap to the power-fist and melta-rifle groups that have no such rifle. Planting a mechanism that is correct-by-luck for two units and latently wrong for the general case is a partial change; a well-scoped item beats it. So B18c is banked with the correct spec: the fan belongs at (or after) the equipped stage where per-group weapons are known, or the per-group weapon map must be threaded into the fan; and it needs the same-slot contest pre-pass. That is a focused single-purpose build for its own session.

**Additive option-id rule (holds for the eventual build):** the group that currently holds the option keeps its id (e.g. `000000241` `cnt_1` stays on the body; `000002748` `cnt_1` stays on the Ancient); the newly-fanned groups get new ids. Saved lists referencing existing ids stay valid. The pooled set shares one `pool_id`.

**Scope changes recorded:** B18c narrowed to `000000241` + `000002748`. New **B18d** created for `000000322`, `000002783`, `000003874`, gated on same-slot exclusion. Indomitor/Fortis marked no-op. The Command Squad live bug is called out in the S62 handoff for priority.
## D128

**B18c stopped and banked at build time: S62's "provably exactly two units" premise was false, and seeding a cross-group pooled count exposes a live engine bug where the shared `pool_id` cap is display-only and is NOT enforced on the weapon/points rollup. No data or engine change shipped this session. B18c now depends on a new engine fix (B18e) and a corrected mechanism (B18f). The two-unit data fan is written and banked, ready for the data turn that follows the engine fix.**

S63 set out to build B18c — fan the capped generic plasma-talon→grenade-launcher swap onto the carrying groups of `000000241` (Ravenwing Black Knights) and `000002748` (Ravenwing Command Squad), using the "fan only when the source weapon is contested by no other option in the unit" gate that D127 called *provably equivalent to exactly the two clean units*. Two independent findings stopped the ship.

**Finding 1 — the structural gate is not two units, it is eight, and two of the eight would become ILLEGAL.** Dry-running the D127 gate (uncontested source weapon + 2+ carrying groups) across all 218 units matched eight, not two: the two targets plus `000000103` (Eradicators, Melta rifle), `000000230` (Deathwing Terminators, Storm bolter menu), `000001177` (Heavy Intercessors, Heavy bolt rifle), `000001183` (Terminators, Storm bolter), `000004138` (Terminator Squad, Storm bolter), `000004175` (Gravis/Deathwatch Veterans, Infernus heavy bolter). Reading source (`Datasheets_options.csv`), `000001183` and `000004138` both carry a per-model restriction footnote — "* This model's storm bolter cannot be replaced" — that applies to the Sergeant/Squad-Leader. Their swap is correctly body-only today; the structural fan would hand the restricted sergeant an illegal storm-bolter swap. That restriction lives in a datasheet footnote, not in the option-contest structure, so no contest-based gate can see it. **A structural fan cannot be made safe until a per-model-restriction signal is parsed and applied.** The other four extras (`000000103`, `000001177`, and probably `000000230`, `000004175`) look like the same genuine under-grant as the two targets (a Sergeant that carries the weapon but isn't offered the swap), and are candidates for the follow-up — but each needs source confirmation.

**Corrective for the gate:** scope by an **explicit unit allowlist**, not a structural predicate. The banked parser change fans only `{000000241, 000002748}` and keeps the carrying-group + uncontested checks as guards. New unit ids are added to the allowlist only after confirming, per unit, no restriction footnote and no same-slot contest. This is the discriminating, non-blanket rule the project already prefers.

**Finding 2 (the blocker) — the shared-pool cap is not enforced on the weapon rollup.** With the two-unit fan applied and diffed clean (exactly `000000241` + `000002748` changed, other 268 byte-identical, `model_groups`/`default_weapons`/`_defaults_source` byte-identical), a rollup check showed the count cap **breaks** once a pool spans groups: Command Squad at 3 models permits **3** grenade launchers (legal max is 1); RBK at 3 models permits **2** (legal max 1). `loRollup` computes counts twice — a per-group weapon-application path (fills the weapon Map and points; sets `cap = min(loMaxCount, reqCap)` with **no** `pool_id` term) and a separate pool-bookkeeping path (`countOpts`, ~L3300, which clamps by `poolCap`/`poolUsed` but only writes the `poolsOut` status counter). B18b/D126 only ever taught the *bookkeeping* path about pools; the *weapon* path stayed pool-blind. It read correct while every pooled option sat on one group (the two paths coincide within a single group). The first cross-group pooled count in data — this fan — makes them diverge. So `pool:plasma_talon` displays `{pool:1, used:1}` while three swaps are actually emitted.

**Why this means "do not ship the data."** Today (committed) both units cap correctly at the unit-wide number (RBK 1@3 / 2@6; Command Squad 1@3) because each option is single-group; the only defect is *which* model is offered (under-grant). Shipping the fan alone would trade "right count, wrong model" for "right models, wrong count" — up to 3 grenade launchers where 1 is legal. That is a count-legality regression, worse on the dimension the tool exists to police. The fan is only correct once the engine honors the shared pool on the weapon rollup. Engine and data must not mix in one turn (standing rule), so the fix is a separate, prior engine turn.

**Sequencing set this session (dev-manager calls):**
- **B18e (engine, new, blocks B18c):** unify `loRollup`'s two count computations so the weapon-application path is clamped by the shared `pool_id` cap, not just the status counter. Must be provable with harness cases that seed a cross-group pooled count (the case class that has no coverage today — which is why the bug survived B18b). Data byte-identical.
- **B18c (data, now BLOCKED on B18e):** the two-unit fan. The parser change is written (`equipped_parser.py`: `fan_pooled_swaps`, run once on the `--datasheets` pass, explicit allowlist `{000000241, 000002748}`, carrying-groups-only, uncontested guard, additive ids `cnt_1__<group_slug>`, shared `pool_id = plasma_talon`) and diffed clean. It applies unchanged the turn after B18e lands.
- **B18f (data+parser, new):** the general capped-generic fan for the remaining under-grant units, requiring (a) a parsed per-model-restriction signal ("* this model's X cannot be replaced") and (b) per-unit source confirmation. Absorbs the four likely-clean extras (`000000103`, `000001177`, `000000230`, `000004175`) after review. B18d (leader-conflict, same-slot exclusion) remains separate.

**Standing lesson reinforced:** a "provably exactly N" scope claim in a handoff is a diagnosis, not an executable check (D107) — it must be dry-run against current data before it is trusted. Here the claim was off by 6 units and hid two would-be legality bugs. And a mechanism that reads correct on today's data (B18b's pool cap) can be latently wrong until data first exercises the untested path; the non-circular diff-guard caught the scope error, and only a live rollup check caught the engine error — neither `repro_check` (circular) nor the existing harnesses (no cross-group pooled-count case) would have.

## D129

**B18e shipped: the shared `pool_id` cap is now enforced on the weapon/points rollup for `count` options on fixed-1 groups, not just on the status counter. `index.html` v5.66 → v5.67. Data byte-identical. A new guarded harness (`pool_check.js`) covers the cross-group pooled-count case that had no coverage — the gap that let B18b's bug survive. B18c is unblocked.**

**Diagnosis re-derived from source (D106), and it was narrower than the S63 read.** The S63 handoff (D128) described the bug as "`loRollup` computes counts twice — a pool-blind weapon-application path and a separate pool-aware `countOpts` bookkeeping path (~L3300) that only writes the status counter." Reading the live code, that framing conflates two different group branches. The truth: `loRollup` has one count path per group *type*. The **multi-model count branch** (the `countOpts` loop, ~L3300) was already fully pool-aware — it clamps `cap` by `poolCap − poolUsed` and charges `poolUsed`, and it both emits the weapons and updates the counter in one pass. The **fixed-1 count branch** (~L3221) was the sole gap: it set `cap = min(loMaxCount, reqCap)` with no `pool_id` term and never charged `poolUsed`. The add branches (fixed-1 and multi) were already pool-aware; only the fixed-1 *count* branch was left behind by B18b/D126. So there was never a "bookkeeping vs weapon" split to unify — there was one branch missing the pool logic its three siblings already had. Confirmed against committed data: the four `pool_id` options in `unit_loadouts.json` are all `type=add` (including a working cross-group pooled add on Intercessors `000001157`), so no committed `count` option exercised the buggy branch — which is why the harnesses stayed green and the defect only surfaced when the banked B18c fan seeded the first cross-group pooled *count*.

**The fix.** In the fixed-1 count branch: change `cap` to `let`, clamp it by the pool's remaining capacity when the option carries a `pool_id`, and charge `poolUsed` by what the branch consumes — mirroring the multi-model count branch and both add branches verbatim. Because groups iterate in `model_groups` order and every count/add branch now both reads and charges `poolUsed`, a pool spanning any mix of fixed-1 and multi-model groups draws from one unit-wide cap regardless of group order; earlier groups shrink the pool the later ones see. No double-charge: each group runs exactly one count branch, and there is no separate bookkeeping loop. Non-pooled and single-group behaviour is byte-identical (the `pool_id` blocks are skipped; `cap` takes the same value; `usedThis` is computed but not charged).

**Proof.** New harness `pool_check.js` loads the real `loRollup` + `wargearCostForRollup` from `index.html`, drives the two fanned fixture defs from `B18c_repro_fixture.json` (never committed), prices the grenade launcher synthetically so points track the capped count, seeds every pooled count high, and asserts the unit-wide cap on both weapons and points. It **FAILS on the pre-B18e engine** (Command Squad @3 emits 3 grenade launchers / 15 pts; RBK @3 emits 2 / 10 pts; RBK @6 emits 3 / 15 pts) and **PASSES on v5.67** (@3 → 1 / 5 pts each; RBK @6 → 2 / 10 pts). All prior harnesses (bundle/pts/stat/default/limit) still pass on committed data; `repro_check` byte-identical; `integrity_check` 0 blocking; D95 invariant zero.

**Custody finding — a silently stale manifest entry.** Rehashing the manifest by hand at close showed `bundle_check.js` had drifted from its recorded hash **before this session** (its mtime is the mount epoch — untouched here; index.html and pool_check.js carry today's stamp). Because `pipeline_manifest.py` is absent from the repo sync, assertion **P3** fails unconditionally and cannot name a mismatch, so this drift sat undetected across at least S61–S63 despite handoffs claiming "hashes hand-verified." The committed `bundle_check.js` is coherent and passes all its own checks, so per the standing rule (the committed artifact is the fixed point) its true current hash was recorded, not reverted. This is a second concrete reason to get `pipeline_manifest.py` into the repo sync: a manifest nobody can self-run drifts silently, and hand-verification missed a real mismatch.

**Manifest.** Rebaselined by hand (raw SHA-256): `index.html` updated to v5.67 bytes; `bundle_check.js` corrected to its true committed bytes; `pool_check.js` added as a new guarded harness (21 → 22 guarded files). All 22 now match.

**Sequencing (dev-manager):** B18c (the two-unit data fan) is unblocked and is the next turn (S65, data-only). The banked `equipped_parser_B18c_banked.py` applies unchanged; regenerate, diff-guard to exactly `000000241` + `000002748`, rebaseline the manifest, then hand Ryan the live pooled-count render. B18f and B18d remain as previously scoped.

## D130 — B39 diagnosis: Bloodthirster's doubled great-axe option is a stale duplicate flat swap, not a source-supported mutual-exclusion (fix is a pipeline dedup widen)
**Context:** B39 reported that selecting the CD Bloodthirster's great axe wrongly locks its other options. Diagnosed per D106 from source, not from the loadout def.

**Finding (source vs. deployed):** `Datasheets_options.csv` for datasheet `000002582` has exactly one option: replace the great axe of Khorne with an axe of Khorne AND one of {bloodflail, lash of Khorne}. This is correctly modeled by the D36 `bundled_swaps` radio group (great axe / axe+bloodflail / axe+lash) now present on the unit in `units.json`. However the unit ALSO still carries a flat `wargear_options` row "Lash of Khorne → Bloodflail" (option group B) — the pre-D36 backwards modeling that D36's rationale said should be removed. The source does NOT support any standalone Lash→Bloodflail swap. In the default (great-axe) state neither Lash nor Bloodflail is equipped, so the orphaned flat swap collides with the bundle radio, producing the wrong lock. B39's suspicion is confirmed with correction: a source-unsupported duplicate swap row, not a parser-inferred pool.

**Root cause (pipeline):** `convert_to_json.py` `_bundle_owns` drops a flat wargear_option only when its *replaced* weapon family is in the bundle's *removes* set. The bundle removes "Great axe of Khorne", so the two group-A rows (great axe → axe strike/sweep) are dropped correctly; the group-B row's replaced family is "Lash of Khorne", which the bundle *adds* (not removes), so the predicate misses it and it survives into `units.json`.

**Decision (fix mechanism, to be applied in a later engine turn — NOT mixed with this diagnosis turn):** Widen `_bundle_owns` so a bundle owns a flat `wargear_option` when the option's replaced OR replacement family appears anywhere in the bundle's endpoints (removes ∪ adds), scoped to model group. Pipeline fix, no `units.json` hand-edit. Chosen over a one-row CSV delete because the same missed-cleanup class recurs across the SM bundle queue (27 bundled swaps + 17 compound replacements per D36). Guards for the fix turn: differential sweep (only bundled units carrying a genuine duplicate may change) + new `rules_assertions.py` check that no unit carries both a bundle and a flat swap touching the same weapon family. `units.json` is not under `repro_check`, so the fix turn rehashes `pipeline_manifest.json` for it.

**Correction to prior sequencing assumption:** S65 handoff and the backlog framed B39 as "the same-slot exclusion mechanism B18d needs." That is wrong. B39 is a build-time data-dedup gap. B18d needs a separate RUNTIME rule (a model may replace a given weapon only once — fanned generic swap vs. named swap on the same slot). Fixing B39 does NOT unblock B18d; the two are de-coupled from here.

## D131 — B39 fix shipped; B39b audit folded in clean; a units.json full-pipeline non-reproducibility finding banked as new custody item

**Fix.** `_bundle_owns` in `convert_to_json.py` widened per D130: a flat `wargear_option` is now owned by a bundle when its replaced OR replacement weapon family sits anywhere in that bundle's endpoints (removes ∪ adds), scoped to model group. Confirmed against the pre-fix data that the widen actually changes behavior (the new `rules_assertions.py` check `B39-1` fails on pre-fix `units.json` and passes on post-fix).

**Finding — a ground-up `units.json` rebuild is not a safe fixed point today.** Attempted the documented full sequence (`wahapedia_transform.py` for SM + DG, `mfm_points_parser.py`, `convert_to_json.py` per faction, `merge_factions.py`) to regenerate the master file cleanly. Even with the ORIGINAL (pre-fix) `convert_to_json.py`, the rebuilt Death Guard and Chaos Daemons blocks do not reproduce the committed `units.json` byte-for-byte — unrelated content drift (added schema fields present in current CSVs/scripts but absent from the committed blocks, plus at least one real content difference on a Chaos Daemons unit's wargear ability / option routing). The Space Marines block (12 of 14 army blocks) reproduces cleanly. This means DG and CD have been hand-touched or built from a since-diverged input snapshot at some point after their last full regen, and the current CSVs/scripts no longer reproduce them from scratch. This is a real gap, parallel to the P3 manifest-script custody issue, and needs its own session to re-establish a fixed point for DG/CD — **not fixed this turn**, since mixing it into a scoped engine fix would violate the engine/data separation rule and ship unrelated changes.

**How the fix was actually applied, given the above.** Rather than ship a rebuild that imports unrelated drift, the widened `_bundle_owns` predicate was applied directly to the three units in the committed `units.json` that carry `bundled_swaps` (Captain `000000073`, Lieutenant `000001346`, Bloodthirster `local:chaos-daemons:bloodthirster`), using a small script (`apply_b39_widen.py`) that imports `weapon_base` from the now-fixed `convert_to_json.py` and runs the identical predicate against each unit's own already-derived `bundled_swaps` + `wargear_options`. This is mathematically identical to what the fixed pipeline would emit for those three units — it is not a hand-authored data edit, it is the fix function applied at the JSON layer specifically to avoid re-importing the DG/CD rebuild drift above. Output byte-matches the committed file's serialization exactly (`indent=1, ensure_ascii=False`, no trailing newline) so the diff is confined to content.

**Result — B39b audit is complete, not just started.** Only three units in the entire deployed data carry `bundled_swaps` today, so "audit the whole bundle queue" (B39b) meant auditing exactly these three:
- **Bloodthirster** — the diagnosed leftover ("Lash of Khorne → Bloodflail", option group B) is dropped. This is the only change in the file.
- **Captain**, **Lieutenant** — both already had empty `wargear_options` (the old removes-only predicate had already caught their flat duplicates), so the widen has zero effect on either. Confirmed, not assumed.

Full-file diff against the pre-fix committed `units.json`: exactly one unit's `wargear_options` array changed (one row removed), nothing else in the 1.2MB file differs. B39b is closed — there is no queue left to work once the fix ships, since no fourth bundle exists yet.

**Guard added.** `rules_assertions.py` `B39-1`: no unit may carry both a `bundled_swaps` group and a flat `wargear_options` row whose replaced/replacement family sits inside that group's endpoints. Verified as a real guard (fails pre-fix, passes post-fix), not a tautology. 45/46 assertions pass (P3 — the absent `pipeline_manifest.py` script — remains the only fail, unchanged custody item).

**Manifest.** Rehashed by hand (script still absent, per the standing P3 workaround): `units.json`, `convert_to_json.py`, `rules_assertions.py` updated to their new SHA-256. 22 guarded files still tracked.

**B39 closed.** B18d remains separately gated on the unbuilt runtime same-slot-exclusion rule (D130's correction stands — B39's fix does not unblock it).
## D132 — P4 resolved: D131's diagnosis was wrong about the mechanism (not the symptom). Chaos Daemons IS reproducible — from the project root, never through wahapedia_transform.py. units.json re-established as a fixed point for all 14 blocks.

**Correction to D131.** D131 recorded that a from-scratch rebuild of DG and CD "does not reproduce the committed units.json byte-for-byte" and filed this as a custody gap parallel to P3 (missing pipeline script). That framing was wrong. The actual defect was in how the rebuild was run, not in the state of the source data:

`wahapedia_transform.py --faction CD` was run to build a Chaos Daemons input directory. This pulls every datasheet Wahapedia tags with `faction_id = CD` from `Datasheets.csv` — 74 datasheets. But the deployed Chaos Daemons roster was never built from `Datasheets.csv`. Per D8 (Faction Generations, see `40K_Architecture_Overview_v0_5.md` §6), CD is the **Gen-1 hand-built block**: nine reference CSVs (`Unit_Stats.csv`, `Unit_Points.csv`, `Unit_Wargear_Options.csv`, `Unit_Other_Options.csv`, `Unit_Weapons.csv`, `Unit_Abilities.csv`, `Keywords.csv`, `Rules.csv`, `Weapon_Abilities.csv`) that live at the **project root** — and have done since the project's first release (built in early sessions C4/C5, June 2026). These are also `convert_to_json.py`'s literal default input filenames. Running `wahapedia_transform.py --faction CD` into a scratch directory writes fresh copies of those same nine filenames from the wrong source (raw Wahapedia), which silently shadow the real CD source in that scratch dir before `convert_to_json.py` ever runs. Every rebuild attempt to date (D131, and this session's first pass) made this exact mistake.

**Verification.** Running `convert_to_json.py --input-dir . --output-dir <tmp>` directly against the project root (no `wahapedia_transform.py` call for CD, ever) produces exactly 53 units with the exact `local:chaos-daemons:*` ids already in the committed file — a perfect id-set match, zero adds, zero drops. The 74-unit rebuild's extra 21 "units" were never Daemons: Chaos Lord, Havocs, Legionaries, Possessed, Warp Talons, Chaos Terminator Squad, etc. — Chaos Space Marine/cultist datasheets Wahapedia tags `CD` only because they carry the "Legiones Daemonica" allegiance keyword (several don't even carry the base `Daemon` keyword). Tested whether a `Daemon`-keyword filter on the raw Wahapedia CD set would cleanly reproduce the committed 53: **no** — 67 of the 106 CD-faction datasheets in the current Wahapedia snapshot carry `Daemon`, and that set neither matches nor is a superset of the committed 53 (it wrongly includes Possessed/Warp Talons/several Slaanesh chariot units, and wrongly excludes Contorted Epitome, which the committed roster does field but which isn't `Daemon`-tagged in this snapshot). There is no mechanical filter over current Wahapedia data that reproduces your roster; the roster is a curated list, and the Gen-1 CSVs already *are* that curated list in executable form.

**Content diffs found once the correct source was used (per D106 — re-derived from source, not from the prior diagnosis):**
- Two schema-only differences present on **every** CD/DG-affected unit — `convert_to_json.py` now emits `faction_keyword_names`, `model_keyword_names`, `wargear_ability_names` (empty arrays for CD/DG, since neither source has the underlying Wahapedia keyword-role or wargear-ability data these fields are populated from for SM), an empty `unit_ability_details: {}` object instead of `null`, and a `loadout_relation: "owns"` marker on `bundled_swaps` groups. All are additive fields the script gained after CD/DG's last regen (D106 case c); `index.html` already reads every one of them via `|| []` / `|| 'owns'` / truthy-guard fallbacks, so their absence in the stale committed file was silently tolerated, not relied upon.
- **Soul Grinder** (`local:chaos-daemons:soul-grinder`) is missing a real wargear option: `Unit_Wargear_Options.csv` carries a Warpsword → Warpclaw swap (Warpclaw is a real optional melee profile already on the unit's statline, `is_base_equipment = FALSE`) that never made it into the committed file. Source is correct; committed was stale (D106 case b).
- **Keeper of Secrets** (`local:chaos-daemons:keeper-of-secrets`) is missing the "Shining Aegis" weapon profile entirely, and its wargear option's replacement name is mis-cased in the committed file ("Shining aegis" vs. the source's consistent "Shining Aegis"). Source is correct; committed was stale and internally inconsistent (D106 case b).
- **Death Guard — Plaguebearers (`000004113`) and Plague Drones (`000004114`)**, the two units D131 already flagged: `Unit_Other_Options.csv` (DG) carries the daemonic icon / instrument of Chaos as two independent `other_options` (matching the D106/loadout-layer decision that these are concurrently-takeable, ungated abilities), with no corresponding rows in `Unit_Wargear_Options.csv`. The committed file had them backwards — as `wargear_options` weapon-replacement rows, with `other_options` empty. Source is correct; committed was stale (D106 case b).

**Fix shipped.** Re-ran the full documented pipeline correctly for the first time — SM via `wahapedia_transform.py`, DG via `wahapedia_transform.py`, **CD via `convert_to_json.py` run directly against the project root** (no transform step) — then `merge_factions.py` across all three. Result: 270 units across 14 blocks, exact id-set match against the previously committed file, with content changes confined to the 53 CD units (schema additions) + 2 CD units (Soul Grinder, Keeper of Secrets content) + 2 DG units (Plaguebearers, Plague Drones content) = 55 changed units total, verified by full-file diff. Replaced committed `units.json` with this output. `pipeline_manifest.json` rehashed by hand for `units.json` (script still absent, standing P3 workaround).

**Guard added — `units_repro_check.py`** (new file, the `units.json` analogue of `repro_check.py`). Runs the corrected three-faction pipeline from source in a temp dir and byte-diffs the result against committed `units.json`. Its own docstring states explicitly, as the guard against regressing this exact mistake: CD must never be routed through `wahapedia_transform.py`. Confirmed as a real guard — fails against the pre-fix committed file (names the 53 CD unit_ids as the first diffs) and passes against the corrected file. Added to `pipeline_manifest.json` as a 23rd guarded file.

**Documentation gap that let this stand for four sessions.** `40K_Data_Pipeline_Process_v0_6.md` §4 lists `dmn_out` as a `merge_factions.py` **input** but never documents the step that builds it — there has never been a written command for regenerating Chaos Daemons. Anyone following the doc "as documented" has no choice but to either skip CD or guess a `wahapedia_transform.py` call, which is exactly the wrong guess. **Follow-up filed:** add the missing CD step (`convert_to_json.py --input-dir . --output-dir <cd_out>`, off the project root, explicitly no transform call) to §4, and add a one-line warning next to the `dmn_out` merge line.

**P4 closed.** P3 (missing `pipeline_manifest.py` script) remains open and unrelated.

## D133 — B40 closed as not-a-bug; Leader-section rework opened (B49); leader_footer added to the pipeline as the data half
**B40 was not a defect.** Ryan's original S52 note ("Bloodmaster is missing its Leader rule") was not a data drop or a render bug. The Bloodmaster carries its full leader setup end to end: `leader_ability_name = Leader`, `leader_eligible_units = [Bloodletters]`, the datasheet-specific "Bloodmaster" ability (+1 to Wound while leading) and "A Gory Path", all present in source (Gen-1 CD CSVs), all correctly in `units.json`, all resolving to description text in `abilities.json`/`rules.json`, and the attachment mechanic reads the eligible list. Nothing to fix. (An early mis-step in this session chased a phantom stat-conferral gap — the Bloodmaster's ability is a Wound-roll modifier, which is not a statline characteristic and has no place in a builder's statline at all. Discarded.)

**What Ryan actually wants (now B49).** The datasheet's "Leader" block should be shown as its own section stating the character's *attachment* rule — which units it can lead — not the generic core-rules "Leader" blurb the app currently shows under Rules. For the Bloodmaster: a "Leader" heading reading "This model can be attached to the following unit: Bloodletters". Approved shape (Ryan): a dedicated **Leader** section (not merged into Abilities), placed first among the ability sections, generic "Leader" core line removed from Rules so it isn't shown twice; singular/plural auto-switch on the unit list ("unit:" vs "units:"); and the section must also carry the datasheet's extra attachment prose where it exists (Lieutenant's "even if a Captain is already attached", Captain's Bladeguard relic-shield restriction, the Plague-Marine characters' co-leader clauses, etc.) — text that is often more than a bare unit list. Co-leader capture matters because it feeds future leader-assignment enforcement (relates to B38).

**Source model (confirmed against data).** The attachment rule composes from three places: (1) the *unit list* = the resolved `attached_id` rows of `Datasheets_leader.csv`, already carried as `leader_eligible_units`; (2) the *extra clause* = the datasheet's `leader_footer` field on `Datasheets.csv` (55 SM/DG-and-other datasheets carry it, incl. the co-leader exceptions); (3) the generic core "Leader" rule, which is the boilerplate to drop from this section. There is **no** `leader_footer` equivalent for the Gen-1 CD block, and none is needed: all 18 CD leaders lead a single squad type with no co-leader exception, confirmed against both the Gen-1 CSVs and Wahapedia's own CD datasheets (zero CD footers in either). So CD's Leader section is fully synthesizable from the unit list alone.

**Data half shipped this turn (B49 is split data-then-engine per the engine/data separation rule).** `leader_footer` is now carried through the pipeline:
- `wahapedia_transform.py`: reads the datasheet `leader_footer` field (whitespace-normalized, **markup kept verbatim** — the `<i>` / `<span class="kwb">` markup is retained so the app can render keyword bolding, per Ryan's decision #2), emits it only on units that have a Leader ability, in a new `Leader Footer` column added to `Unit_Stats.csv` (positioned after `Leader Restrictions`).
- `convert_to_json.py`: reads `Leader Footer` by column name into a new `leader_footer` field on each model group. Because the read is by name (`row.get`), the Gen-1 CD `Unit_Stats.csv` — which has no such column — falls back to empty, exactly like `co_leader_eligible_with` already does. No CD source change, no desync.
- `units.json`: rebuilt via the corrected D132 three-faction pipeline (SM+DG through transform, **CD directly off the project root, never through `wahapedia_transform.py`**). 19 SM/DG units now carry non-empty `leader_footer`; every model group gains the key (empty where none). CD footers: 0, as expected. `index.html` reads the field with a fallback, so its presence is inert until B49's engine turn renders it.

**Verification.** `units_repro_check.py` passes byte-for-byte on the rebuilt file (the committed `units.json` reproduces from source with the footer-enabled scripts). `repro_check.py` byte-identical; `rules_assertions.py` 45/46 (P3 only); `pool_check.js` passes. `pipeline_manifest.json` rehashed by hand (P3 workaround) for the three changed files — `units.json`, `convert_to_json.py`, `wahapedia_transform.py` — and all 23 guarded files verified against the manifest with zero mismatches.

**Process note — a self-inflicted scare worth recording.** Mid-session, an attempt to isolate whether the footer edit caused unrelated `wargear_ability_names`/`unit_ability_names` diffs used a hand-edited textual *revert* of `wahapedia_transform.py` to build a "baseline". That revert was imperfect and silently disabled the B14 wargear-ability surfacing and some ability handling, producing a build with spuriously empty ability lists on ~16 units — which briefly looked like the footer change had corrupted data. It had not. The real determinism test (two builds with the *identical* committed scripts) is byte-equal, and `units_repro_check` passes. **Lesson (reinforces D106/the fixed-point rule):** never hand-edit a script to "revert" it for an isolation build — check out or regenerate the clean version. A sloppy revert is itself a source change and will manufacture false diffs.

**B49 remaining (engine turn, next):** render the Leader section — heading "Leader", body = "This model can be attached to the following unit(s): <resolved list>" with singular/plural switch, plus the `leader_footer` HTML where present; drop the generic "Leader" line from the Rules section; add a `.kwb` CSS rule so the retained keyword markup actually bolds. Engine-only, `units.json` byte-identical.
## D134 — B49 engine half shipped: dedicated Leader section rendered, generic Rules line dropped

**Shipped.** `index.html` v5.68. Added `leaderSectionHtml(raw, sidPrefix)`, a single shared helper called from
both popup builders (`buildModalFull` and the configured popup), inserted immediately before the Abilities
section in each — first among the ability sections, not merged into Abilities, per D133's approved shape.

**Gate condition.** A model group renders a Leader entry only when its `leader_ability_name` is set AND its
`leader_eligible_units` is non-empty. Checked against the full `units.json`: every group with `"Leader"` in
`rule_names` has `leader_ability_name` set and vice versa (zero mismatches), and no group has the ability
name set with an empty eligible list — so this gate is equivalent to "has the Leader rule" with no silent
gaps. This also correctly suppresses **Wardens of Ultramar**, a data quirk where `leader_eligible_units` is
populated (with sibling in-datasheet model names, not army units) but `leader_ability_name` is null — not a
real Leader case, and gating on ability-name presence (not eligible-list presence) avoids rendering a
nonsensical section for it.

**Body.** "This model can be attached to the following unit(s): <list>" with the singular/plural word swap
on a length-1 vs length-2+ eligible list, followed by `leader_footer` injected as raw HTML (not escaped) when
present. **Chaplain Grimaldus** is the one multi-model-group Leader unit in the data (GRIMALDUS / CENOBYTE
SERVITOR profiles, each independently eligible to lead the other's squad list) — handled generically by
labelling each group when more than one group carries the ability, matching the existing stat-block
group-label convention; no special-casing needed.

**Rules section.** Both popups now exclude the literal name `"Leader"` when collecting `allRuleNames`, so the
generic core-rules blurb no longer duplicates the new section.

**CSS.** Added `.kwb { font-weight: 700; color: #cc9900; }` so the retained `<span class="kwb">` markup in
footer text bolds, matching the datasheet look.

**Verification.** Embedded JS re-parses clean (no syntax errors). Simulated the render function in Node
against the committed `units.json` for the two named differential targets plus Grimaldus: Lieutenant
(`000001346`) renders the 14-unit list, singular/plural "units", and its footer HTML verbatim; Bloodmaster
renders the footer-less single-unit case ("unit: Bloodletters."), singular; Grimaldus renders two
group-labelled entries. `units_repro_check.py` and `repro_check.py` both byte-identical — confirms this was
an engine-only change. `rules_assertions.py` 45/46 (P3 only, unrelated). `pool_check.js` passes.
`pipeline_manifest.json` rehashed by hand (P3 workaround) for `index.html` only.

**B49 closed.**
## D135 — B44 data half shipped: `loadout_groups` shared key added to statline model groups

**Scope check first.** Of 270 units, only 8 carry more than one statline model group in `units.json`
(`Outrider Squad`, `Wardens of Ultramar`, `Wolf Guard Headtakers`, `Wolf Scouts`, `Talonstrike Kill Team`,
`Decimus Kill Team`, `Chaplain Grimaldus`, `Crusader Squad`) — a ninth, Pink Horrors, also has two statline
groups but carries no `unit_loadouts.json` entry at all (Chaos Daemons has no loadout data yet) and is out of
scope. Every other unit's single statline group already covers the whole unit, so no key is needed there —
the ceiling B44 describes is real but narrow: 8 units, 16 statline groups.

**Why this couldn't be solved by name-matching alone.** The engine's existing `statGroupScopes()` (D112)
already tries: split the statline group's name on commas, normalize, and look each token up against loadout
group names. That works when the statline name is a literal list of matching model/character names (it
happens to succeed for Wardens and Wolf Guard Headtakers). It silently produces a **wrong, partial** count
for **Wolf Scouts** — the statline name "WOLF SCOUTS" exact-matches only the loadout group "Wolf Scouts" and
never picks up the sibling "Wolf Scout Pack Leader" group, so the Pack Leader's models are missing from any
carrier count attributed to that statline row — and returns "cannot attribute" (an asterisk, never wrong, but
never a real value either) for cases like **Outrider Squad**, where the statline name "OUTRIDER" has no
loadout group of that exact name at all (the loadout side calls them "Outrider Sergeant" / "Outriders").
Fixing this at the naming-heuristic level isn't possible in general: the correspondence is genuinely
per-datasheet knowledge (which composition lines share a statline), not a string relationship, so it has to
be authored data, not a smarter regex.

**What shipped.** A new `loadout_groups` field on the statline `model_groups` entries of the 8 affected units
(16 groups total), each holding the exact loadout group name(s) — from the committed `unit_loadouts.json` —
that share that statline. Verified by hand against `Datasheets_models.csv` / `Datasheets_unit_composition.csv`
for each of the 8 (e.g. Outrider Squad's "OUTRIDER" statline row covers loadout groups "Outrider Sergeant" and
"Outriders"; its "INVADER ATV" row covers loadout group "Invader ATV"). New script `add_loadout_groups.py`
applies the mapping as a data-only enrichment pass over an already-built `units.json`, failing loudly if a
named loadout group doesn't exist in the committed `unit_loadouts.json` (guards against drift if either file
changes later without the other). `units_repro_check.py` now runs this script as the final step of the
rebuild chain (after `merge_factions.py`, before the byte comparison), so "the committed file reproduces from
source" now includes this enrichment — it is not a hand-edit sitting outside the pipeline.

**Engine half deferred, per the engine/data separation rule.** `index.html` is untouched this turn. The field
is inert until a follow-up engine turn teaches `statGroupScopes()` to check `mg.loadout_groups` first (when
present, authoritative — skip the name-heuristic entirely) and only fall back to the existing comma-split
matching where the field is absent. That closes the ceiling described in B44 and the Wolf-Scouts silent
undercount as one change.

**Verification.** `units_repro_check.py` byte-identical (the rebuild chain, including the new enrichment step,
reproduces the committed `units.json` exactly). `repro_check.py` byte-identical (untouched). `rules_assertions.py`
45/46 (P3 only, pre-existing custody gap). `pool_check.js` passes. `pipeline_manifest.json` rehashed by hand
(P3 workaround) for `units.json`, `units_repro_check.py`, and the new `add_loadout_groups.py`.

**B44 data half closed. Engine half open — see backlog.**

## D136 — B44 engine half shipped: `statGroupScopes()` now trusts `loadout_groups` when present, closing B44 and the Wolf Scouts undercount

**What shipped.** `statGroupScopes()` in `index.html` now checks the statline model group's `loadout_groups`
field (added in D135) first. When present, it is used directly as the loadout group list — no name-matching,
no heuristic — and validated only for staleness (every named loadout group must still exist in the current
loadout def; if not, falls back to "cannot attribute" rather than trusting a stale mapping). The existing
comma-split name-heuristic (D112) is unchanged and still runs for every group without the field — 209 of the
225 total statline group entries across all 270 units.

**Verified against every group entry, not a sample.** A standalone harness extracted both the old and new
function bodies from `index.html` and ran each against every statline group in the committed `units.json`
paired with its `unit_loadouts.json` def. Of 225 group entries, exactly 8 changed behavior — Outrider Squad's
"OUTRIDER" row (was unattributable, now resolves to Outrider Sergeant + Outriders), Wolf Scouts' "WOLF SCOUTS"
row (was missing the Pack Leader group, now includes it — the undercount this ticket exists to fix),
Talonstrike Kill Team, Decimus Kill Team (both rows), Chaplain Grimaldus (both rows), and Crusader Squad's
"OTHER MODELS" row. The remaining 8 of the 16 `loadout_groups`-carrying rows already matched the old heuristic
by luck (e.g. Wardens of Ultramar, Wolf Guard Headtakers) and are now authoritative instead of coincidental.
All 209 ungated rows are byte-identical old vs new, confirming the fallback path is untouched.

**Verification.** `index.html` v5.69. `repro_check.py` and `units_repro_check.py` both byte-identical (data
untouched this turn — engine-only, per the separation rule). `rules_assertions.py` 45/46 (P3 only, pre-existing
custody gap). `pool_check.js` passes.

**B44 closed outright — both halves shipped.**

## D137 — B45 retired as a standalone ticket and re-homed into its real owners; SUPREME COMMANDER (must-be-Warlord) found silently dropped by the transform

**Scoping conclusion (S73).** B45 bundled five army-muster legality rules from `Army_Muster_Rules.txt`
25.03/25.04 under one label. Scoped against the current app and data, they do not share a build — four of
the five are gated behind systems that do not exist yet, so B45 as written is not a buildable session but a
pointer to other tickets. Retired as a standalone ticket. Sub-rules re-homed:

- **DP budget** (2 Incursion / 3 Strike Force, no duplicate detachments) → **E1**. The app has no detachment
  selection system at all — no detachment state, no UI. DP cannot be checked against a selection that does
  not exist. Blocked on E1, which is unbuilt.
- **Enhancement limit** (2/4 by battle size, CHARACTER-only, no EPIC HEROES, no duplicates, `Upgrade`
  exception) → **E4**. The app has no enhancement selection/assignment system. Same wall as DP. Blocked on
  E4 (which itself depends on E1).
- **Warlord** (exactly one; must-be / cannot-be precedence) → **E9**. See the propagation finding below; this
  reshaped E9 into a data turn plus an engine turn.
- **Support units must be attached** → **B38**. Needs the leader/support attachment system as army state,
  which is B38 territory. `co_leader_eligible_with` is captured in `units.json` since S69 but attachment is
  not yet modelled as roster state. Blocked on B38.
- **Army faction keyword** → **closed, pending one verification pass**. The app already enforces this by
  faction selection rather than by keyword. For the v1 factions the faction picker is the effective keyword
  gate; a one-time check that faction == keyword for the built factions is worth doing but is not a build.

**Finding that corrects D-record scoping and my own prior-turn claim.** The SUPREME COMMANDER ability — the
one whose text forces a unit to be the Warlord — is **not reaching `units.json`** for any built unit. Root
cause: in `wahapedia_transform.py`'s `index_abilities()`, abilities are routed by `type` into Core /
Datasheet / Faction / Wargear. SUPREME COMMANDER carries `type = "Special (правая колонка)"`, which matches
none of those and falls into the `else` branch, where it is appended to `flags["unclassified_abilities"]` and
dropped from all derived output. Source (`Datasheets_abilities.csv`) has 18 SUPREME COMMANDER rows; **four of
their units are already in the built data** — Lion El'jonson, Roboute Guilliman, Mortarion, Be'Lakor — and
all four carry zero trace of the rule in `units.json`. An earlier scan that reported "1 unit (Azrael)" was a
substring false positive: Azrael's ability is "Supreme Grand Master", which does not force Warlord.

**Consequence for E9.** The must-be-Warlord auto-select is not near-dead code awaiting more factions (the
prior characterization) — it is needed today for four current units and is invisible to the engine because
the derived data never carries the flag. E9 therefore splits:
1. **Data turn** — surface SUPREME COMMANDER as a per-unit `must_be_warlord` boolean by routing the "Special"
   ability name (or an explicit id/name match) through the transform into `units.json`. Regen-gated, byte-diff
   confirmed to touch only the flagged units. This is the D107 principle in force: the fact was in source,
   absent from derived data, so it did not hold.
2. **Engine turn** — the banner Warlord pick list over eligible CHARACTER units actually in the list, one-per-
   army enforcement, and the must-be / cannot-be precedence, consuming the flag.

No code or data shipped this turn — this is a scoping + backlog-structure decision. `index.html` v5.69,
both data files still byte-identical, `rules_assertions.py` 45/46 (P3 only), `pool_check.js` passes.

## D138 — off-by-one column-index bug in `wahapedia_transform.py` post-processing (found while scoping E9a, fixed same session)

**Finding.** B49 (S73) added a `Leader Footer` column to the 26-column `Unit_Stats.csv` schema, inserted
between `Leader Restrictions` (17) and `Unit Ability Names` (was 18, became 19). Two later post-processing
passes in `main()` still used the pre-insertion index and were never updated:

1. **Fix 2b (additive chapter-variant ability inheritance)** — hardcoded `AB = 18`. This reads/writes
   `Leader Footer`, not `Unit Ability Names`. Net effect: a chapter variant sharing a datasheet name with the
   generic Adeptus Astartes version never actually inherits the generic ability it's supposed to union in.
   Confirmed against the committed `units.json`: 6 Black Templars units were missing one inherited ability
   each (Gladiator Valiant, Gladiator Reaper, Repulsor Executioner, Repulsor, Sternguard Veteran Squad,
   Terminator Squad).
2. **B14 surface-subtraction (optional wargear ability shouldn't sit on the always-on surface)** — hardcoded
   `row[23]`, which is `Model Keyword Names`, not `Wargear Ability Names` (24). Net effect: an ability tied to
   an item that's actually optional (routed to Other Options) stayed on the unit's always-on wargear-ability
   surface instead of only conferring when selected. Confirmed against the committed `units.json`: 10 units
   across 5 armies carried an incorrectly-always-on wargear ability (Infiltrator Squad, Incursor Squad, Reiver
   Squad, Sanguinary Guard, Deathwing Terminator Squad, Deathwing Knights, Corvus Blackstar, Spectrus Kill
   Team, Plaguebearers, Plague Drones).

Neither bug was caught by any assertion — no check in `rules_assertions.py` covers chapter-ability inheritance
or the B14 always-on/optional distinction by content, only by structure. This is the D107 pattern again: an
index shifted, nothing that depended on the old index was re-verified against the new schema.

**Fix.** Both hardcoded indices corrected (`AB = 19`; `row[23]` → `row[24]`) in `wahapedia_transform.py`.
Full three-source pipeline (SM, DG, CD) regenerated and merged; `add_loadout_groups.py` re-run. Byte-diff
old vs new `units.json`: exactly 16 units changed (the 6 + 10 above), nothing else. `units_repro_check.py`
reproduces the new committed file byte-for-byte.

**Scope discipline.** E9a (Warlord flag) was deliberately NOT built in this same turn, even though it touches
the same function, so this fix's diff stays isolated and independently bisectable. E9a resumes next turn.
Also newly confirmed while scoping E9a: Be'Lakor (the 4th SUPREME COMMANDER unit) is Gen-1 hand-built Chaos
Daemons data that never runs through `wahapedia_transform.py` at all — it converts directly off the project
root's own `Unit_Stats.csv`. E9a's transform fix will reach Guilliman/Lion/Mortarion but not Be'Lakor; Be'Lakor
needs a hand-added value on his CD source row (legitimate — that CSV is CD's actual source of truth, not a
generated artifact) as a second, small piece of the same E9a turn.

`index.html` untouched, v5.69. `unit_loadouts.json` untouched, byte-identical. `rules_assertions.py` 45/46
(P3 only). `pipeline_manifest.json` rehashed for `wahapedia_transform.py` and `units.json`.

## D139 — E9a shipped: `must_be_warlord` surfaced for the 4 SUPREME COMMANDER units; a second, unrelated
live data bug (Blue Horrors' abilities/rules/keywords miscolumned) found and fixed as a side effect

**Part 1 — transform fix.** `index_abilities()` in `wahapedia_transform.py` now matches ability name
`SUPREME COMMANDER` case-insensitively, independent of `type` (5 of the 18 source rows are typed
`Fortification` rather than `Special`; type is a layout bucket, not a semantic class). A `warlord_flag` set
is threaded through the same way as the existing `leader_flag` set. `build_stats()` appends a `Must Be
Warlord` value (`"Yes"`/blank) as the **last** column on `Unit_Stats.csv` — appended after `Datasheet ID`
rather than inserted mid-row, specifically to avoid re-triggering the D138 class of bug: two post-processing
passes just fixed last session (`AB = 19`, `row[24]`) read `stats_rows` by position, and a mid-row insertion
would have shifted them again. `convert_to_json.py` derives `must_be_warlord = bool(clean(stat_rows[0].get(
"Must Be Warlord")))` at unit level, same take-from-first-row precedent as `unit_type`, and adds it to the
final `unit_obj`. This reaches Guilliman, Lion El'jonson, and Mortarion (all SM/DG, built through the
transform).

**Part 2 — Be'Lakor.** Gen-1 Chaos Daemons data converts directly off the project root's own `Unit_Stats.csv`
and never runs through `wahapedia_transform.py` (D132), so it needs its own value. The CD source file's
schema predates `Leader Footer` and has two unnamed reserved trailing columns; the first was named `Must Be
Warlord` and set to `Yes` on Be'Lakor's row by hand — legitimate, since this file is CD's actual source of
truth, not a generated artifact.

**Found while verifying — a live, pre-existing bug, not caused by this change.** Naming that previously-blank
reserved column exposed that it was already non-blank for one row: Blue Horrors. That row's data was
miscolumned starting at `Unit Ability Names` — `Split` sat alone where all three abilities (`Split`, `Sullen
Malevolence (Aura)`, `Exploding Horrors`) belonged; `Sullen Malevolence (Aura)` sat in `Rule Names` where
`Deep Strike,Infiltrators` belonged; `Keyword Names` held a truncated, mis-quoted `Exploding Horrors"`; and
the actual keyword list (`Infantry,Battleline,Chaos,Daemon,Tzeentch,Horrors`) had spilled into the two
reserved trailing columns, duplicated. This was already shipping wrong in the committed `units.json` — Blue
Horrors was missing two of its three abilities, both its core rules, and all six keywords, confirmed against
the currently-deployed file. Fixed in the same source-CSV edit (same file, same turn category as the Be'Lakor
hand-add — a data-only correction, not an engine change). All three abilities' descriptions already existed
in the CD source's own `Unit_Abilities.csv` lookup, so the fix surfaces complete text with no further
authoring needed. Note: `Sullen Malevolence (Aura)`'s own description text in that lookup is itself truncated
("While an enemy unit is within 6\" of this unit" with no resolution clause) — a separate, smaller data-quality
gap, banked to backlog rather than fixed here to keep this diff scoped.

**Verify.** Full three-source pipeline (SM, DG, CD) regenerated, merged, `add_loadout_groups.py` re-run.
Byte-diff old vs new `units.json` across all 270 units: exactly 5 units changed — the 4 `must_be_warlord`
additions (Guilliman, Lion El'jonson, Mortarion, Be'Lakor) plus Blue Horrors (the bug fix above), nothing
else. New `rules_assertions.py` check `E9a-1` asserts `must_be_warlord` is true iff the datasheet carries
SUPREME COMMANDER in `Datasheets_abilities.csv` (any built faction) or is Be'Lakor by name — an executable
fact per D107, not prose. `units_repro_check.py` reproduces the new committed file byte-for-byte.
`rules_assertions.py` 46/47 (P3 only, pre-existing gap). `pool_check.js` clean. `index.html` untouched, v5.69
— engine file, no changes this turn.

Files changed: `wahapedia_transform.py` (warlord_flag + Must Be Warlord column), `convert_to_json.py`
(must_be_warlord derivation), `Unit_Stats.csv` at project root (Be'Lakor hand-add + Blue Horrors bug fix),
`rules_assertions.py` (new E9a-1 check), `units.json` (5 units), `pipeline_manifest.json` (rehashed).

## D140 — E9b shipped: Warlord pick list wired into the Army List banner, plus a data addition E9b needed —
`cannot_be_warlord` — that didn't exist yet

**Why this became a two-part turn.** E9b's spec (Ryan, S52) requires "cannot-be beats must-be" as a
precedence rule. No `cannot_be_warlord` field existed on `units.json` — only `must_be_warlord` (E9a). Checking
source before building (per the S76 prompt's explicit gate) found the restriction already live on three built
units across three of our priority factions: **Lieutenant With Combi-weapon** and **Murderfang** (Space
Marines, Wolf Guard variant) and **Exalted Flamer** (Chaos Daemons). Shipping the pick list without excluding
these would have let them be wrongly selected as Warlord — a real legality bug on already-built units, not a
future risk. Deriving the field first (data turn) then wiring the engine (engine turn) mirrors the E9a/E9b
split precedent rather than mixing the two change types in one turn.

**Part 1 — `cannot_be_warlord` derivation (data turn).** Unlike SUPREME COMMANDER, "cannot be Warlord" isn't
one named ability — source carries it under many names (LOYAL PROTECTOR, LONER, SHADOW ASSIGNMENT, Pack
Leader, WOLFKIN, ENSLAVED STAR GOD, PATH OF DAMNATION, and others). Matched instead on ability **description**
text: every row containing both "cannot" and "warlord" (case-insensitive) is a restriction. Checked this is
safe against every Warlord-mentioning row in source: "must be your Warlord" rows contain "must", never
"cannot"; conditional-bonus rows that mention Warlord without restricting it (Master Tactician, Death Vision
of Sanguinius, WAAAGH! Wazdakka, Malign Presence) contain neither "cannot" — so the two-word co-occurrence
cleanly isolates just the restriction class, with zero overlap against the must-be pattern. `wahapedia_transform.py`
gets a `cannot_warlord_flag` set (same threading as `warlord_flag`) and a new **last** column, `Cannot Be
Warlord`, appended after `Must Be Warlord` — same "append at the end, never mid-row" precedent as D139, so no
positional index anywhere in the file shifts. `convert_to_json.py` derives `cannot_be_warlord` the same
take-from-first-row way as `must_be_warlord`. Chaos Daemons (Gen-1, never routes through the transform —
D132) got Exalted Flamer's value hand-added to the project root's own `Unit_Stats.csv`, using the second (and
now last) of that schema's two previously-unused trailing columns — the same one D139 named for Be'Lakor's
Must Be Warlord value.

**Verify (data turn).** Full three-source pipeline (SM, DG, CD) regenerated, merged, `add_loadout_groups.py`
re-run. Diffed old vs new `units.json` field-by-field across all 270 units: the only difference anywhere is
the new `cannot_be_warlord` key itself (true on exactly Lieutenant With Combi-weapon, Murderfang, Exalted
Flamer; false elsewhere) — nothing else moved. New `rules_assertions.py` check `E9b-1` asserts
`cannot_be_warlord` is true iff the datasheet carries a "cannot"+"warlord" description in
`Datasheets_abilities.csv` (any built faction) or is Exalted Flamer by name — executable per D107, not prose.
`units_repro_check.py` reproduces the new committed file byte-for-byte. `rules_assertions.py` 47/48 (P3 only).
`pool_check.js` clean. `unit_loadouts.json` untouched and still byte-identical (`repro_check.py`) — this turn
never touches loadout data.

**Part 2 — the pick list (engine turn).** Lives centered in the Army List panel's subheader bar (the "second
banner" of Ryan's spec), as a `<select>` populated from armyList entries that are resolved (not a ghost),
CHARACTER, and not `cannot_be_warlord`. Duplicate unit names in the list are disambiguated with a trailing
`(2)`, `(3)`, etc. Selection state (`warlordEntryId`, holding a `listId` rather than a unit name, so two
identically-named units in the list are distinguishable) is recomputed every `renderAll()`:
- Exactly one eligible `must_be_warlord` unit in the list → forces the pick (select is shown disabled,
  locked to that unit) every render, overriding any prior manual choice.
- Two or more eligible `must_be_warlord` units in the list → illegal army, shown in the existing red-badge
  convention (`#cc2200`) naming both units; no pick is forced between them.
- Zero forcing units → ordinary manual pick from the eligible list; persists across renders until the chosen
  entry leaves the army list (removed, or `clearList`), at which point the selection clears.
- `cannot_be_warlord` always wins over `must_be_warlord` per Ryan's spec — built into `eligibleWarlordEntries()`
  filtering cannot-be units out before the must-be check ever runs, so if source data ever puts both flags on
  one unit the cannot side is structurally what gets checked. No such unit exists in built data today.

Persisted on the saved-list record as a new top-level `warlord_entry_id` field (additive; existing saved lists
without it simply load with no Warlord selected, then re-derive from `must_be_warlord` on first render if a
forcing unit is present). `SCHEMA_VERSION` stays at 1 — this is an additive field, not a shape change to
existing ones.

**Verify (engine turn).** The three new render/state functions (`eligibleWarlordEntries`, `recomputeWarlord`,
`warlordIllegal`) were extracted verbatim from the shipped file and run against 12 fixture scenarios covering:
non-Character exclusion, no-forced-pick-without-must-be, manual pick persistence, must-be auto-select
overriding a prior manual pick, two-must-be illegal flagging without clobbering existing selection,
cannot-be-warlord exclusion even when it's the only eligible unit in the list, selection clearing when its
entry is removed, and ghost (unresolved) entries never being eligible — all 12 pass. Cross-checked
`isCharacter`/`mustBeWarlord`/`cannotBeWarlord` against real `units.json` for five known units (Guilliman,
Murderfang, Rhino, Lieutenant With Combi-weapon, Exalted Flamer) — all as expected. Full inline-script syntax
check (`node --check`) passes. `index.html` v5.70.

Files changed: `wahapedia_transform.py` (`cannot_warlord_flag` + `Cannot Be Warlord` column), `convert_to_json.py`
(`cannot_be_warlord` derivation), `Unit_Stats.csv` at project root (Exalted Flamer hand-add), `rules_assertions.py`
(new E9b-1 check), `units.json` (new field on all 270 units, true on 3), `index.html` (pick list + persistence,
v5.69 → v5.70), `pipeline_manifest.json` (rehashed — blocked on P3's missing script, see below).

## D141 — B1 audited before being scheduled: the reported symptom no longer reproduces; the real residual
risk is narrower and CD-only

Ryan asked whether B1 should be next. Before committing a session to it, audited whether it still
reproduces — it doesn't, for the units it was actually reported on.

**Method.** Built a source-of-truth map (`ds_id -> {ability_name: correct_description}`) straight from
`Datasheets_abilities.csv`, then walked every ability instance on every built unit in `units.json` (473
total across SM/DG), computing the same "effective text" the render itself computes
(`unit_ability_details[name] || abilities.json[name]`), and diffing against the correct per-datasheet text
(whitespace-normalized to avoid false positives from `<ul>`/`<br>` list-markup differences). Zero genuine
mismatches. Cato Sicarius's "Honour or Death" and Apothecary's "Narthecium" — the two originally-reported
symptoms — both resolve to their correct text today.

**Why it's already fixed.** `wahapedia_transform.py`'s `index_abilities()` already builds a per-datasheet
`unit_abil_desc` map for both Datasheet- and Faction-type abilities ("this datasheet's OWN text; fixes
name-collision" — the comment predates this audit, so the fix was made at some point without a
backlog/decision-log entry confirming it closed B1). This reaches every unit as `unit_ability_details` via
`Unit_Ability_Details.csv`, and `index.html`'s render (two call sites, list-view and full-modal) already
checks it before falling back to the shared `abilities.json` map. This is the systemic fix B1 asked for
("scope ability text per unit/datasheet instead of a global name→description map"), not a narrow patch on
the two reported units — it was just never marked closed.

**What audit surfaced instead — Chaos Daemons has zero coverage, structurally.** CD (Gen-1, D132) never
routes through the transform and has no per-datasheet source, so every CD unit's `unit_ability_details` is
`{}` — 100% dependent on the shared global map. Cross-checked all ability names across SM+DG+CD's three
source lookups for genuine (not whitespace) collisions: found 9, all Death-Guard-vs-Chaos-Daemons pairs with
legitimately different per-book wording (Mischief Makers, Deluge of Nurgle (Aura), Infected Outbreak,
Fortification, Diseased Cover, Fire Support, Virulent Blessing (Psychic), Daemon Lord of Nurgle (Aura),
Scuttling Walker). Checked every built unit using these 9 names: every DG unit has its own correct override;
every CD unit has none, and today happens to show its own correct text only because CD's version currently
wins whatever merge order builds `abilities.json` — not because anything guarantees it. A future faction
rebuild could flip that silently. Also found 3 of the 9 CD-side descriptions are truncated at the source
(same class as the already-banked B52) — banked alongside it rather than fixed here, to keep this an
audit-only turn.

**Outcome.** B1 backlog entry corrected to reflect this: original symptom confirmed fixed, re-scoped
residual risk split out as new item B1b (give CD its own per-unit override coverage — needs its own look at
whether CD's flat `Unit_Abilities.csv` lookup can even support per-datasheet granularity before sizing the
fix). B2 flagged for re-verification against this finding before assuming it's the same mechanism — it may
be a Core-rule/rule_names collision, which this fix doesn't touch. No code or data shipped this turn; this is
an audit-only turn (no engine or pipeline files changed).

## D142 — B1b shipped: Chaos Daemons gets its own per-unit ability-text coverage; B52 and 3 truncated
descriptions fixed alongside it; P3's missing script recreated

**Investigation (step 1 of the S77 prompt).** D141 assumed CD's flat `Unit_Abilities.csv` was the only CD
ability-text source. Checked it directly: it has no per-datasheet scoping at all (two columns, name and
description, no unit or datasheet key) — confirming it structurally cannot drive a per-unit override on its
own. But it's also far more corrupted than D141's audit surfaced: **33 of its 96 entries are truncated
mid-sentence at the source** (cut off wherever the original text contained an embedded inch-mark, e.g.
"...within 6\" of this model"), not just the 3 D141 flagged — meaning this file could never have served as
the text source even if it were keyed per-unit. `chaos_daemons_reference.md` (the condensed faction-pack
reference already in the project) turned out to carry full, complete, per-unit ability text under each
datasheet's own "Abilities:" line — covering all 53 built CD units (plus 6 Forge World/Legends units the tool
doesn't build). This unblocked the build: source data supports per-unit granularity, just not the file D141
assumed.

**Build.** New parser `build_cd_ability_details.py` extracts `{unit_id: {ability_name: description}}` from
`chaos_daemons_reference.md`'s prose, using the 96 names in `Unit_Abilities.csv` as a known-name anchor set to
split each unit's "Abilities:" line into individual entries (never using that file's own — truncated — text).
Writes `Unit_Ability_Details.csv` in the exact shape `convert_to_json.py` already expects
(`Datasheet ID | Unit Ability Name | Unit Ability Description`), keyed on the same `local:` slug `unit_id` CD
units already carry (`slug_id(army, unit)` — not a real Wahapedia datasheet id, CD has none). No engine or
`convert_to_json.py` change was needed: the per-unit override consumption path (`ability_details_by_ds.get
(unit_id, {})`) already existed and was simply never fed for CD, since the optional CSV was absent.

**Where the doc shorthands a repeat as "As above."** (god-aura abilities — e.g. "Greater Daemon of Khorne
(Aura)" — are identical for every unit of that god, so the doc states them in full once and abbreviates the
rest), the parser resolves via the first full occurrence found anywhere else in the same document, never via
the flat CSV. One additional case needed the same treatment even though the doc didn't literally write "As
above": `Fortification` (the core-rules generic Fortification-terrain ability, identical for every
Fortification-type unit by design) was written in full for Skull Altar but abbreviated to "standard
fortification rules." for Feculent Gnarlmaw — not a different rule, just a shorter restatement of the same
fact. Both units now carry the fuller text. This is the only manual per-name judgment call in the build; every
other name's text came straight from that unit's own line in the reference doc.

**Verify.** Full pipeline regenerated (SM + DG transform legs untouched; CD leg run directly against the new
`Unit_Ability_Details.csv` at the project root, matching `units_repro_check.py`'s existing CD invocation) and
merged. Diffed old vs. new `units.json` unit-by-unit: exactly the 53 Chaos Daemons units changed, and for every
one of them the only field that changed was `unit_ability_details` — nothing else moved. Audited every CD
ability instance (98 across all `unit_ability_names` references in `model_groups`) by resolving the same
override-then-global-fallback the render itself performs and comparing against each unit's own text as parsed
from the reference doc directly (not a name-collapsed oracle, which produces false positives for names like
`Split` that legitimately carry different text on Pink Horrors vs. Blue Horrors) — zero mismatches beyond the
one intentional Fortification normalization above. `units_repro_check.py` byte-identical against the newly
committed `units.json`. `unit_loadouts.json` untouched.

**B52 and the 3 truncated descriptions (Deluge of Nurgle (Aura), Virulent Blessing (Psychic), Daemon Lord of
Nurgle (Aura), Sullen Malevolence (Aura)) are fixed as a side effect** — all four now carry their full text via
the same override mechanism, sourced from the reference doc rather than the truncated flat CSV.

**Correction to D141.** Its "9 collisions" list included "Fire Support" — checked directly this session: it
isn't a Chaos Daemons ability at all (absent from `Unit_Abilities.csv`, absent from `chaos_daemons_reference.md`,
not used by any built CD unit). The real DG-vs-CD collision count is 8, all now safely resolved by CD's own
override coverage regardless of future merge order.

**P3 (missing `pipeline_manifest.py`), also closed this session.** The script itself — not just its JSON
output — was absent from project files, so `rules_assertions.py`'s P3 check had failed unconditionally for
several sessions (papered over by a manual raw-SHA-256 workaround at session close). Recreated it from
`rules_assertions.py`'s `manifest_gate()` contract (`check(dir_) -> (ok, message)`) plus the existing
`pipeline_manifest.json`'s shape and `_note` field: SHA-256 over every guarded file, `--write` to regenerate.
Ran `--write` to rehash all 24 guarded files (including `index.html` and `units.json`, both changed this
session) and confirmed `check()` passes clean. `rules_assertions.py` now 48/48.

**Files changed:** `Unit_Ability_Details.csv` (new, project root — CD's per-unit override source),
`build_cd_ability_details.py` (new — the parser that produces it), `units.json` (53 CD units'
`unit_ability_details` only), `index.html` (VERSION 5.70 → 5.71, cache-bust only — no engine change this
turn), `pipeline_manifest.py` (new — recreated per D123), `pipeline_manifest.json` (rehashed).
Backlog: B1b, B52 marked shipped. No product/design decision needed this session — the Fortification
normalization and the Fire Support correction are both mechanism/data-accuracy calls within dev-manager
authority, same category as prior data-quality fixes (D139).





## D143 — B2 audited and closed (no reproduction); B38 re-scoped after inspecting the co-leader data on real data

**B2 — closed, same outcome as B1.** The reported symptom (the unit popup's "Leader" line showing the
generic Core *Leadership*/Ld rule instead of the unit's own Leader ability) does not reproduce on committed
data. Two existing mechanisms already cover it: (1) the dedicated **Leader section** (B49) renders each unit's
own attach eligibility (`leader_eligible_units`) plus its raw `leader_footer`, not any generic text; and (2) the
Rules section explicitly filters the generic Core `Leader` rule out (`name !== 'Leader'`) so it never renders as
a rule. D141's hypothesised *Leader*-vs-*Leadership* `rule_names` collision does not exist in the data: there is
no standalone "Leadership" rule (the word only appears as a substring inside other abilities' descriptions), and
zero `unit_ability_details` entries are named "Leader." 100 model-groups carry `Leader` in `rule_names`, all
correctly suppressed from display. No fix needed; B2 marked closed.

**B38 — deeper than the "consume the captured field" framing; re-scoped and blocked on one product/legality
decision.** Investigated `co_leader_eligible_with` on real data before designing anything, per the S77 pick:

- **The engine already consumes the field.** `canAttachLeader()` reads `co_leader_eligible_with` and, when a
  bodyguard already has a leader, permits a second only if the symmetric name-list check passes. So B38 was
  never an engine-design task for the *single* second-leader case — that mechanism exists.
- **But the field is empty on every built unit** (279 `co_leader_eligible_with` keys in `units.json`, all `[]`;
  0 populated rows in the root `Unit_Stats.csv`). "Captured since S69" meant the *column exists*, not that it
  was ever populated. That empty field is exactly why the tool today allows only one leader per bodyguard and
  silently blocks legal second-leader attaches. So B38's real work is **data population**, resolved from each
  unit's `leader_footer` co-leader clause — the upstream extraction into a structured field was never wired.
- **18 built units carry a co-leader clause, in two shapes.** 12 SM units name their partners ("even if one
  **Captain / Chapter Master / Lieutenant**…", or a specific hero for Cato Sicarius → Marneus Calgar) — these
  map to a resolved name-list, but the role-words (Captain, Lieutenant…) each cover a *family* of built
  datasheets that must be enumerated to concrete `unit_name`s (same resolution B49 already does for
  `leader_eligible_units`). 6 DG units use the **generic** shape ("even if **one other Leader** unit has already
  been attached; you cannot attach two of the same") — this names no partner and does not map to a finite
  name-list without enumerating every eligible leader of the shared bodyguard.
- **Engine gap the data exposes: multi-leader (3+) validation is order-dependent.** `canAttachLeader()` finds
  exactly *one* existing attached leader via `.find` and validates only against that one. Current SM rules
  legitimately stack several support characters on one Captain-led unit (Lieutenant + Apothecary + Ancient +
  Bladeguard Ancient are all individually co-attach-legal), reaching 3+ leaders. Against a 2-leader unit the
  single-`.find` check is order-dependent and can wrongly allow or block the 3rd. Correct behaviour requires
  validating each incoming leader against the *full* attached set — an engine change, which must not ship in
  the same turn as the data population (engine/data separation).

**Why B38 stops here instead of shipping the SM data alone.** Populating the SM name-lists without the
multi-leader engine fix would enable partially-correct 2-leader attaches while leaving 3+ order-dependent and
sometimes illegal — shipping a known-incorrect legality behaviour, which D0 forbids. Banked whole behind the
decision below. B2's closure is the only shipped change this turn.

**Decision pending (Ryan) — recorded, not yet resolved.** How the tool models co-leader legality: (a) whether
to support true multi-leader with full-set validation (fixing the current under-permissive one-leader-only
behaviour), and (b) how to represent the generic "any other single leader, not a duplicate" shape — enumerate
names into the existing field, or add a small explicit generic flag the engine understands. This sets a lasting
legal/illegal precedent, so it waits for Ryan rather than a dev-manager guess. Recommendation carried in the
session report. `SESSION_HANDOFF_78` / `NEXT_SESSION_PROMPT_79` intentionally held until the decision lands so
they are not born stale.

**Files changed:** `OPEN_ITEMS_BACKLOG.md` (B2 closed; B38 re-scoped). No code or data file changed;
`index.html` version unchanged (5.71) — B2 needed no fix. Baseline re-confirmed clean on entry: v5.71,
`repro_check.py` + `units_repro_check.py` byte-identical, `rules_assertions.py` 48/48 (P3 holding), `pool_check.js` green.



## D144 — B38 decision resolved (Ryan): support true multi-leader with full-set validation; model the generic shape with an explicit flag

Following the D143 finding, Ryan made both calls:

**(a) Yes — support true multi-leader with full-set validation.** The tool will honour the real rule that a
Bodyguard unit can carry more than one Leader when the attached Leaders' datasheet clauses permit it (the common
legal SM pattern of stacking support characters on a Captain-led unit). Today's one-leader-only behaviour is a
legality miss to be corrected.

**(b) Flag — model the generic "any other single leader, not a duplicate" shape with an explicit flag**, not by
enumerating names. A new per-unit boolean (working name `co_leader_any`) means "when joining an eligible
Bodyguard, I may do so even if it already has one or more Leaders, and I am co-eligible with any of them except a
duplicate of my own datasheet." Cleaner than a brittle enumerated list and matches the footer's actual meaning.

**Resulting engine design (order-independent, symmetric-pairwise over the full attached set).** Define a pairwise
predicate `permits(A, B)` = `A.unit_name !== B.unit_name` (never two of the same datasheet) **and**
(`A.co_leader_eligible_with` includes B **or** B's list includes A **or** `A.co_leader_any` **or** `B.co_leader_any`).
An incoming leader L may attach to bodyguard G iff `L.leaderEligible` includes G **and** `permits(L, E)` holds for
**every** leader E already attached to G. This replaces the current single-`.find` check in `canAttachLeader`
(index.html ~L2079–2085), which validates only against the first-found existing leader and is therefore
order-dependent for 3+ stacks. Worked cases confirm correctness: Apothecary joining {Captain, Lieutenant} → allowed
(3 leaders); a second Lieutenant onto {Captain, Lieutenant} → blocked (same-name); a Captain added after a
Lieutenant → allowed (order-independent); two same-name generic characters → blocked.

**Sequencing (engine-first, three clean turns — engine and data never mixed):**
- **B38-engine** — add the full-set `permits`-based check and teach `canAttachLeader` to read `co_leader_any`
  (default false when absent). Ships with **zero behaviour change** because both co-leader fields are still
  empty/false on every unit; verified by "no list changes / no diff in attach behaviour." Engine-only turn.
- **B38a (data)** — populate `co_leader_eligible_with` for the 12 built SM named-shape units (D143), resolving
  footer role-words (Captain / Chapter Master / Lieutenant families; Cato Sicarius → Marneus Calgar) to concrete
  built `unit_name`s via the same resolution B49 uses for `leader_eligible_units`. Validate on real data (casing,
  exact family membership). Pipeline only — never hand-edit `units.json`. Data-only turn.
- **B38b (data)** — set `co_leader_any = true` on the 6 built DG generic-shape units. New field needs a home in
  the data source + `convert_to_json.py` pass-through (the engine already reads it after B38-engine). Data-only.

**Residual nuance (build-time confirm, dev-manager authority, not a blocker):** the pairwise model permits
generic-flag units to stack freely (e.g. three DG support characters + a primary on one Plague Marines unit).
This is the literal reading of "even if one other Leader is already attached." Worth a quick check against New
Recruit's behaviour during B38b; if NR caps lower, revisit then. Not gating the engine or SM data.

**CSM note (future):** Exalted Champion and Master of Executions carry the same generic "any other CHARACTER"
shape and will take `co_leader_any = true` when CSM is built — out of scope now (not a built faction).

**Files changed:** `OPEN_ITEMS_BACKLOG.md` (B38 unblocked/sequenced). No code or data changed this turn;
docs only. `SESSION_HANDOFF_78` and `NEXT_SESSION_PROMPT_79` written to open the next session on B38-engine.

## D145 — B38-engine shipped: full-set symmetric-pairwise leader validation, zero behaviour change confirmed

Built the D144 design. `canAttachLeader` (index.html) replaced the single-`.find` check against only the
first-found existing leader with a loop over the full attached set, requiring `permitsCoLeader(incoming,
existing)` to hold for every one of them — order-independent, as specified. New helper `permitsCoLeader(A, B)`
returns false on same-name (never two of the same datasheet) and otherwise checks either side's
`coLeaderWith` list or `coLeaderAny` flag. `setActiveUnits` now also reads `co_leader_any` off each unit's
first model group (mirrors how `co_leader_eligible_with` is already read), defaulting to false when absent —
true for every built unit today, since B38a/B38b haven't shipped data yet.

**Verification.** All four D144 worked examples hold (Apothecary onto {Captain, Lieutenant} allowed; second
Lieutenant onto {Captain, Lieutenant} blocked; Captain added after Lieutenant allowed, confirming order-
independence; two same-name generic characters blocked). A no-diff sweep comparing the old and new logic
across every combination of 0–2 existing leaders, with `coLeaderWith=[]`/`coLeaderAny=false` (today's real-
data condition on all 279 built units), found zero mismatches — confirms the D144 "zero behaviour change"
claim. Grepped other call sites (`getAttachedLeaders`, the bodyguard-picker `<option>` filter) — both already
operate over the full attached-leader array with no independent single-leader assumption; no other fix needed.

**Also checked — B48.** The "also worth doing" item in `NEXT_SESSION_PROMPT_79` was stale: B48 (Corvus
Blackstar double-control) already shipped in Session 60 (D125), per the backlog. No work needed; not
re-touched.

**Files changed:** `index.html` v5.71 → v5.72 (`canAttachLeader` rewritten, `permitsCoLeader` added,
`coLeaderAny` read into `allUnits`). `pipeline_manifest.json` regenerated for the new `index.html` hash.
`OPEN_ITEMS_BACKLOG.md` (B38-engine marked done). `rules_assertions.py` 48/48. Engine-only turn — no data
files touched.

## D146 — B38a shipped: co_leader_eligible_with populated on the 12 built SM named-shape units

Resolved each of the 12 units' `leader_footer` role-words to concrete built `unit_name`s, using the same
principle B49 established for `leader_eligible_units`: read the real rules text, then verify the resolution
against source data rather than guessing from prose.

**Resolution mechanism — keyword-carrying built datasheets, not string-matching on unit names.** The footers
name role-words ("Captain", "Chapter Master", "Lieutenant", "Execrator"), and `Datasheets_keywords.csv` gave a
precise, checkable answer for each: CAPTAIN keyword → 25 built datasheets (the Captain armour-variant family
plus every Captain-rank named Epic Hero, e.g. Uriel Ventris, Belial, Ragnar Blackmane); CHAPTER MASTER keyword
→ 8 built datasheets, all named Epic Heroes (Commander Dante, Azrael, Logan Grimnar, Kayvaan Shrike, Pedro
Kantor, High Marshal Helbrecht, Aethon Shaan, Marneus Calgar in Armour of Antilochus) — **no built datasheet in
the current codex is literally named "Chapter Master"**, it was folded entirely into named Epic Heroes;
LIEUTENANT keyword → 5 built datasheets (the Lieutenant armour-variant family, plus Castellan, which carries
the Lieutenant keyword though its own name doesn't say so); EXECRATOR keyword → 1 built datasheet. Checked
programmatically: none of these four keyword sets overlap on any built datasheet, and none of the 12 target
units' own names appear in their own resolved list (no accidental self-reference).

Cato Sicarius's footer names Marneus Calgar specifically (not a role-word family) — single-name list.

**Grouping (12 units, by footer wording):**
- "Captain or Chapter Master" (Captain ∪ Chapter Master, 33 names): Apothecary Biologis, Lieutenant In Reiver
  Armour, Lieutenant, Lieutenant In Phobos Armour, Castellan.
- "Captain, Chapter Master or Lieutenant" (+ Lieutenant, 38 names): Bladeguard Ancient, Ancient In Terminator
  Armour, Apothecary, Ancient, Sanguinary Priest.
- "Captain, Chapter Master, Execrator or Lieutenant" (+ Execrator, 39 names): Crusade Ancient.
- Named pair (1 name): Cato Sicarius → Marneus Calgar in Armour of Antilochus.

**Implementation.** New pipeline step `add_co_leader.py`, same pattern as B44's `add_loadout_groups.py`: a
hardcoded, source-verified mapping (not a runtime footer-text parser — more auditable, matches precedent),
with a guard that fails loudly if a mapped name isn't actually a built `unit_name` or if a unit is
self-referenced. Runs after `add_loadout_groups.py`; `units_repro_check.py` updated to include it in the
required chain.

**Baseline note.** On entry, `units_repro_check.py` failed twice before reaching a clean baseline — both times
from incomplete local file staging, not real pipeline bugs: `Source.csv` was missing (so `wahapedia_transform.py`'s
Legends-source exclusion silently no-opped, producing 4 extra Legends units), then `Abilities.csv` was missing
(so `Leader`/`Oath of Moment` ability-name lookups came back empty on every unit). Both are project-file copies
missing from the working directory, not defects in the committed pipeline. Once both were present, the pipeline
reproduced the committed `units.json` byte-for-byte, matching the S79 handoff's clean-entry claim.

**Diff-guard.** Full differential sweep across all 270 units confirmed the change touched exactly the 12 target
units' `co_leader_eligible_with` field and nothing else.

**Still needs Ryan.** A manual sanity check in the running app — attach two of the newly-eligible leaders (e.g.
a Captain and a Lieutenant) to the same Bodyguard unit and confirm both attach — wasn't done this turn (no
running app in this environment). B38-engine already reads the field correctly (D145), so this should just
work, but it's real behaviour change worth an eyeball before calling B38a fully closed.

**Files changed:** `units.json` (12 units' `co_leader_eligible_with` populated; diff-guard confirmed scope).
New file `add_co_leader.py`. `units_repro_check.py` (added `add_co_leader.py` to the required chain and the
run sequence). `OPEN_ITEMS_BACKLOG.md` (B38a marked done). `pipeline_manifest.json` NOT regenerated —
`pipeline_manifest.py` remains absent from project files (known open custody issue, unchanged this session);
P3 held at its existing known-fail state (47/48), not a new failure. `index.html` untouched (data-only turn,
engine already shipped in D145).

## D147 — B38b shipped: co_leader_any populated on the 6 built DG generic-shape units

**What.** Set `co_leader_any = true` on the 6 built Death Guard units whose `leader_footer` carries the
generic "even if one other Leader unit has already been attached to it (you cannot attach more than one of
the same Leader to the same unit)" clause: Noxious Blightbringer, Foul Blightspawn, Biologus Putrifier, Plague
Surgeon, Tallyman, Icon Bearer. Wording re-verified byte-for-byte against committed units.json at build time
on all 6 targets -- matches the S80 handoff quote exactly.

**Schema.** Unit_Stats.csv's 27-column write in wahapedia_transform.py gained a 28th column, "Co-Leader Any"
(bool string, same style as Must Be Warlord/Cannot Be Warlord), written blank for every unit at transform time.
convert_to_json.py reads it into a new co_leader_any key on each model_group object, same per-model-group
placement as co_leader_eligible_with. Chaos Daemons' hand-built root Unit_Stats.csv has no such column and
doesn't need one -- convert_to_json.py's .get() read defaults a missing column to False, same tolerance the
existing 23-vs-27-column CD/SM split already relies on.

**Population.** Reused add_co_leader.py (B38a's script) rather than a new file -- same job family, same guard
style. Added a CO_LEADER_ANY_IDS list (6 unit_ids, no name-mapping needed since this is a flag, not a named
eligibility list) and a second guard block (existence check, single-model_group assumption, matching B38a's
pattern). Runs in the same pipeline pass as B38a, no new step in the chain.

**Diff-guard.** Full pipeline rebuild, differential sweep across all 270 units: every unit gained the new
co_leader_any key (default false, unavoidable byte-diff from the schema addition itself), and exactly the 6
target units carry true. No other field on any unit changed.

**Residual nuance (flagged, not resolved).** The pairwise engine model (D145) lets co_leader_any units stack
freely -- three DG support characters plus a primary Leader could in principle all attach to one Plague Marines
unit, the literal reading of the footer. Not addressed this session; worth a New Recruit comparison if Ryan
has a screenshot, otherwise not a default assumption to build a cap on.

**Still needs Ryan.** Manual sanity check in the running app -- attach two DG co-leader-flagged units to one
Plague Marines squad and confirm both attach -- not done this turn (no running app in this environment). Can
be batched with the outstanding B38a check from S80.

**Files changed:** units.json (6 units' co_leader_any set true; all 270 units gained the new key at false
default). wahapedia_transform.py (new Co-Leader Any column). convert_to_json.py (new co_leader_any read).
add_co_leader.py (new CO_LEADER_ANY_IDS list and guard block). OPEN_ITEMS_BACKLOG.md (B38b marked done).
pipeline_manifest.json NOT regenerated -- pipeline_manifest.py remains absent from project files (known open
custody issue, unchanged this session); P3 held at its existing known-fail state (47/48). index.html untouched
-- engine already reads co_leader_any (D145), data-only turn.

## D148 — E10 shipped: duplicate unit in center panel

**What.** New "duplicate" control (a small icon) on each top-level unit's list card, next to the existing
info and remove buttons. Duplicating a unit copies its full configuration (size, wargear selections, other
options) to a new entry, and re-attaches duplicated copies of its attached leaders to the copy -- except Epic
Heroes, which are never duplicated (Ryan's S52 spec): the copy simply has no leader in that slot, which is not
an error, not a flagged state.

**Pricing.** No new pricing logic needed. copy-tier pricing (ptsForEntry) already keys off listId order among
same-name entries, and a duplicate always gets a fresh, higher listId -- so it is automatically priced as the
next copy (second/third+) the same way a fresh roster add would be. Confirmed in scenario 1 of the new harness
(100/90 first/second-copy split).

**Limit enforcement.** The instance-limit hard boundary (B41/D0 -- a limit the tool enforces, not just flags)
applies to duplicateUnit exactly as it does to addUnitFromRoster: refused outright at the limit, with the same
banner message. This also applies independently to a duplicated leader -- if re-attaching a leader copy would
put that leader's own unit_name over its own instance limit (e.g. a second copy of a Character already at
3/3), the leader copy is silently skipped and the body copy still ships with no leader in that slot. This
wasn't explicitly in Ryan's S52 spec but is a direct application of the existing always-enforced invariant,
not a new precedent -- treated as an implementation default, not a question for Ryan.

**Implementation.** duplicateUnit(listId) in index.html, wired to the new button in renderList()'s top-level
unit card only (not on leader sub-rows -- duplication is a bodyguard-level action per spec). New
.duplicate-btn CSS rule mirrors the existing .info-btn. index.html bumped to v5.73.

**Verification.** New harness e10_check.js loads the real duplicateUnit + its dependency chain
(getAttachedLeaders, ptsForEntry, the unitLimit family) out of index.html and drives it against five synthetic
scenarios: plain unit, unit with a non-Epic-Hero leader, unit with an Epic Hero leader (exclusion confirmed),
unit already at its instance limit (refusal confirmed), and a leader already at its own limit (silent skip
confirmed). All 16 assertions pass. points/wargear-cost math itself is stubbed to 0 in the harness -- not what
this checks; wargearCostForEntry is unchanged, pre-verified machinery.

**Data untouched.** No pipeline, no CSV, no units.json change -- pure engine/UI turn. All data-side checks
(units_repro_check.py, repro_check.py, rules_assertions.py at its existing 47/48 known-fail, pool_check.js)
reconfirmed unaffected.

**Still needs Ryan.** Live-render eyeball in the running app -- click the new duplicate icon on a unit with an
attached leader and confirm the copy renders correctly in the center panel, including the Epic-Hero-excluded
case if a DG or SM list with an Epic Hero leader is handy. No harness checks the actual DOM render.

**Files changed:** index.html (v5.72 -> v5.73: new duplicateUnit function, new duplicate button in
renderList(), new .duplicate-btn CSS rule). New file e10_check.js. OPEN_ITEMS_BACKLOG.md (E10 marked done).
40K_Decision_Log_v3_0.md (D148, this entry).

## D149 — B18d shipped: capped generic swaps fanned to leader-conflict units (Thunderwolf Cavalry, Deathwatch Veterans, Talonstrike Kill Team)

**Session:** S82 (data turn — no engine change).

**Context.** B18d scoped three units where a generic capped per-N swap and a named leader/sergeant swap contest
the same weapon slot on the leader group: Thunderwolf Cavalry `000000322` (Bolt pistol — cnt_3 vs cc_1),
Deathwatch Veterans `000002783` (Boltgun + Power weapon — cc_1..cnt_7 vs sng_8/sng_9), Talonstrike Kill Team
`000003874` (Heavy bolt pistol — cnt_3 vs cho_1). These were previously held out of the fan because a "same-slot
mutual exclusion mechanism" was assumed to be missing from the engine.

**Key finding: the engine already has the mechanism.** The fixed-1-group weapon-consumption tracking in
`loRollup` (the `taken` dict for choice options plus the `cUsed` dict for count options, cross-checked at lines
3504–3507) already enforces that a single-model group can replace each weapon at most once. When two options on
the same fixed-1 group both consume the same weapon (or overlapping components of a compound weapon), the engine
sets `overAllocated = true` and displays the "Too many weapon swaps" warning. No new engine code was needed —
the ticket reclassified from DATA+ENGINE to DATA-only.

**Parser changes (equipped_parser.py).**

*Contested-slot bypass.* A new `_FAN_CONTESTED_OK` set lists units whose contested slots have been hand-verified
safe against the existing engine mutual-exclusion logic. The contest > 1 check in `fan_pooled_swaps` is bypassed
for these units.

*Gate widened.* The fan gate previously required `per_n_models`; it now also accepts `max_total` options (e.g.
DW Veterans' "1 model" Black Shield blades swap, cnt_7). `max_total_all` ("any number") options remain excluded
— they're already correctly scoped per group and don't need fanning.

*Compound carrier check.* The carrier check previously compared the full `replaces` string against individual
`default_weapons` entries. A compound like "Boltgun + Power weapon" never matched individual weapons "Boltgun"
or "Power weapon." New `_group_carries()` helper splits the compound on ` + ` and verifies all parts are present
in the group's default_weapons.

*Pool ID derivation.* Changed from weapon-name-based (`_slug(strip_profile(w))`) to option-ID-based (`o['id']`).
The weapon-name pool created a collision when multiple options replaced the same compound (all 7 DW Veterans
generic options shared "boltgun_power_weapon", causing the last one's cap to overwrite all others). Option-ID
pools are always unique per body-leader pair. Side effect: RBK and RCS pool_ids changed from "plasma_talon" to
"cnt_1" — functionally identical (pool_ids are per-unit runtime values, not saved).

**Data changes (unit_loadouts.json).** 5 units changed, 9 new options (327 → 336):

| Unit | New option | Pool ID | Source | Replaces |
|------|-----------|---------|--------|----------|
| TWC 000000322 | cnt_3__thunderwolf_cavalry_pack_leader | cnt_3 | per 3, max 1 | Bolt pistol → Plasma pistol |
| DWV 000002783 | cc_1__watch_sergeant | cc_1 | per 5, max 2 | Boltgun + PW → shield/PW choices |
| DWV 000002783 | cnt_2__watch_sergeant | cnt_2 | per 5, max 2 | Boltgun + PW → DW thunder hammer |
| DWV 000002783 | cnt_3__watch_sergeant | cnt_3 | per 5, max 1 | Boltgun + PW → stalker boltgun + CCW |
| DWV 000002783 | cnt_4__watch_sergeant | cnt_4 | per 5, max 2 | Boltgun + PW → DW shotgun + CCW |
| DWV 000002783 | cnt_5__watch_sergeant | cnt_5 | per 5, max 1 | Boltgun + PW → frag cannon + CCW |
| DWV 000002783 | cnt_6__watch_sergeant | cnt_6 | per 5, max 1 | Boltgun + PW → infernus HB + CCW |
| DWV 000002783 | cnt_7__watch_sergeant | cnt_7 | max_total 1 | Boltgun + PW → Black Shield blades |
| TKT 000003874 | cnt_3__kill_team_sergeant_with_jump_pack | cnt_3 | per 5, max 1 | Heavy bolt pistol → Plasma pistol |

RBK 000000241 and RCS 000002748: pool_id value changed from "plasma_talon" to "cnt_1" (no new options).

**Verification.** New harness b18d_check.js, 20 assertions across 3 units: pool cap clamping at both size
brackets, mutual exclusion (overAllocated fires when leader has both named and fanned swaps active), clean
independent use (fanned swap alone, named swap alone), and confirmation that named swaps don't consume pool
slots. All 20 pass. Existing pool_check.js (6 assertions, B18c fixtures) and e10_check.js also reconfirmed.

**Files changed:** equipped_parser.py, unit_loadouts.json (217/336), new b18d_check.js, new B18d_fixture.json.
40K_Decision_Log_v3_0.md (D149). OPEN_ITEMS_BACKLOG.md (B18d closed).

**Still needs Ryan.** Live-render eyeball: open each of the 3 units in the running app at each size bracket and
confirm the fanned options show up on the leader/sergeant group, the pool counter displays correctly, and
activating both the named swap and the fanned swap shows the over-allocation warning.


## D150 — B18f investigated and closed with no data change: five of six candidates are named-body-type (D116-correct, no under-grant); only Decimus Kill Team is a genuine generic under-grant, re-scoped to B18g

**Session:** S83 (investigation — no engine or data change; nothing shipped).

**Context.** B18f (opened S63, D128) proposed fanning the capped generic weapon swap onto the sergeant group of
"remaining under-grant units," listing four likely-clean candidates and excluding two Terminator Squads on a
footnote read. Per-unit source review against D116 found the premise wrong.

**The controlling rule (D116).** An option's scope is what its own sentence says. "For every N models… 1 **model**
can replace…" is generic and reaches every group including the leader/sergeant. "1 **<body model type>'s** weapon
can be replaced…" names the body model type and is body-only — the sergeant is correctly out of scope. D116's own
proof row is `000001044`: "1 **Plague Marine's** boltgun" keeps the Plague Champion out, and B18-3 asserts it.
The RBK/RCS units that were legally fanned (D148/B18c) use the generic "1 **model**" — which is why the Huntmaster
is in scope. The handoff conflated the two constructions.

**Source read, all six candidates (`Datasheets_options.csv`):**

| Unit | Scope subject | D116 verdict | Under-grant? |
|------|---------------|--------------|--------------|
| Eradicator Squad `000000103` | "1 **Eradicator's** melta rifle" | named body type → body-only | No — sergeant correctly out |
| Heavy Intercessor Squad `000001177` | "1 **Heavy Intercessor's** heavy bolt rifle" | named body type → body-only | No |
| Deathwing Terminator Squad `000000230` | "1 **Deathwing Terminator** can replace its storm bolter" | named body type → body-only | No |
| Terminator Squad `000001183` | "1 **Terminator's** storm bolter" | named body type → body-only | No |
| Terminator Squad `000004138` | "1 **Terminator's** storm bolter" | named body type → body-only | No |
| Decimus Kill Team `000004175` | "up to 1 **model's** infernus heavy bolter" (×4 options, all "1 model's") | generic → unit-wide | **Yes** |

So five of six are D116-correct as they stand: the "sergeant can't swap" behavior is not a defect, it is the rule.
Fanning them would have handed those sergeants an illegal swap — the precise failure D116 exists to prevent.
(An earlier sub-finding this session — that the S63 exclusion comment misreads the cyclone footnote "* this
model's storm bolter cannot be replaced" as a sergeant restriction when it is an anti-double-dip note on the
cyclone sub-option — is correct but moot: the two Terminator Squads are excluded correctly regardless, because
they are named-body-type. The comment's *reason* is wrong; its *verdict* is right.)

**Decimus Kill Team is the only real B18f case, and it is not a sergeant fan.** Its four swaps all use generic
"1 model's," so they reach every carrying group. The Infernus heavy bolter swap (cc_1) is scoped to Deathwatch
Veterans, but Gravis Veterans also carry the infernus heavy bolter with no option — the fan target is a **second
heterogeneous body group**, not a sergeant. The Deathwatch Veterans group carries a 10-weapon default list (a
normalization artifact, not a real per-model loadout), and the unit has OR-branch composition (1 Gravis/3 DW vs
2 Gravis/7 DW). Fanning a shared pool across two heterogeneous body groups with an artifact default list is
materially riskier than the sergeant fans done so far. **Re-scoped to B18g**; not attempted this turn.

**B18f is CLOSED — no defect.** No data change. The five named-body-type units are correct under D116; the
"under-grant" framing was a misreading. The `_FAN_UNIT_ALLOWLIST` is unchanged.

**Recommended guard (opened as B18h).** The near-miss this session — an illegal fan that passed `repro_check.py`
(byte-identical to its own regenerated output) and `rules_assertions.py` (no assertion covers these units) —
shows the fan allowlist has no executable guard against adding a named-body-type unit. Recommend an assertion
that every id in `_FAN_UNIT_ALLOWLIST` maps to a source option whose scope subject is the generic word "model,"
not a named body type — making the D116 rule executable for the fan itself (D107: a rule not expressed as a check
does not hold). Validate that the five current members ("1 model") pass and the named-body-type units fail before
trusting it.

**Files changed:** none (investigation only). 40K_Decision_Log_v3_0.md (D150). OPEN_ITEMS_BACKLOG.md (B18f closed;
B18g and B18h opened).

## D151 — E13 shipped (label polish) and B18h shipped (D116 made executable as an assertion on the fan allowlist)

**Session:** S84.

**E13.** The "Keep " prefix on default swap-option labels was built at two sites in `index.html` (the single-
choice row and the clustered-choice row), not in the data — both used `'Keep ' + o.replaces`. Removed the
prefix at both sites; the label now shows the kept weapon name alone (or "None"), with the pre-selected
highlight carrying the "this is the default" signal, as accepted at the original S52 confirmation. `index.html`
v5.73 → v5.74.

**B18h.** D150 recommended an executable guard: every id in `equipped_parser.py`'s `_FAN_UNIT_ALLOWLIST` must
rest on a `Datasheets_options.csv` scope line whose subject is the generic word "model," never a named body
type — the class of error that let an illegal fan silently pass every existing check.

Built two helpers and one assertion in `rules_assertions.py`. `_fan_scope_qualifies(desc)` isolates the per-N-
models / any-number-of-models scope lines (the shape B18c/B18d/B18f fan onto multiple carrying groups) and
excludes single-model named-leader lines ("The Watch Sergeant's… can be replaced…"), which are a different
option entirely and never fanned. `_fan_scope_is_generic(desc)` extracts the noun phrase immediately before
"can" and tests whether it is the bare or possessive word "model(s)" versus anything else (a named body type,
e.g. "Eradicator's", "Deathwing Terminator").

`b18h_fan_allowlist_generic` (assertion **B18h-1**) walks the five current allowlist members
(`000000241`, `000002748`, `000000322`, `000002783`, `000003874`), requires every qualifying scope line on each
to classify generic, and — to prove the classifier actually discriminates rather than passing vacuously —
requires a negative control (`000000103`, Eradicator Squad, a known named-body unit never in the allowlist) to
classify as non-generic. All five members pass; the control correctly fails. As an extra live check this
session (not shipped, reverted after confirming), temporarily adding `000000103` to the allowlist made B18h-1
fail with the exact named-body line quoted — confirming the guard would have caught the S83 near-miss.

Assertions: 48 → 49 (`rules_assertions.py`). 48/49 pass — P3 remains the known, unrelated failure
(`pipeline_manifest.py` still absent).

**Files changed:** `index.html` (v5.74). `rules_assertions.py` (B18h-1 assertion + two helpers).
40K_Decision_Log_v3_0.md (D151). OPEN_ITEMS_BACKLOG.md (E13 closed; B18h closed).

## D152 — B18g investigated and banked: cc_1 is scoped to the wrong group; fan mechanism cannot fix it

**Session:** S85 (investigation only — no engine or data change; nothing shipped).

**Context.** B18g (opened S83/D150) flagged Decimus Kill Team `000004175`'s infernus heavy bolter swap (cc_1) as
a genuine generic under-grant. All four options use "1 model's" (generic per D116), and cc_1 is currently
scoped to Deathwatch Veterans. The prompt directed: investigate whether fanning cc_1 onto Gravis Veterans (who
also carry the weapon) is safe; if the DW Veterans' artifact default list makes `_group_carries` unreliable,
bank the finding and stop cleanly.

**Finding 1 — only Gravis Veterans carry the infernus heavy bolter.** The Datasheets.csv loadout text is
unambiguous: "Each Gravis Veteran is equipped with: infernus heavy bolter; bolt pistol; close combat weapon."
The three (size 5) or seven (size 10) Deathwatch Veterans each carry specific, different weapons — stalker bolt
rifle, heavy thunder hammer, marksman bolt carbine, or xenophase blade. No individual DW Veteran carries an
infernus heavy bolter. The DW Veterans' 10-weapon `default_weapons` list is a normalization artifact: the
union of all weapons across individual DW Veteran sub-types, not a real per-model loadout.

**Finding 2 — cc_1 is scoped to the wrong group.** The loadout parser correctly identifies the option text
"1 model's infernus heavy bolter" as generic (scope_hint = "body"), and the scope resolver maps "body" to the
largest body group — Deathwatch Veterans. This is wrong: only Gravis Veterans carry the weapon. The scope
should be "Gravis Veterans", not "Deathwatch Veterans". The other three options (cnt_2/cnt_3/cnt_4) are
correctly scoped to DW Veterans because those model types DO carry the replaced weapons (heavy thunder hammer,
stalker bolt rifle, marksman bolt carbine respectively).

**Finding 3 — the fan mechanism cannot fix this.** Adding `000004175` to `_FAN_UNIT_ALLOWLIST` would cause
`_group_carries` to return True for BOTH groups (DW Veterans: false positive from the artifact default list;
Gravis Veterans: genuine carrier). The fan would create a copy for Gravis Veterans (correct) but keep the
original on DW Veterans (incorrect). The result would be a shared pool across a group that carries the weapon
and a group that does not — shipping a swap on models that don't have the weapon.

**Fix pathway (not attempted this session).** A targeted scope correction in the equipped_parser: after the
loadout parser assigns "body" scope, a post-processing step for this unit should check which group's REAL
default weapons include the replaced weapon and re-scope accordingly. This is NOT a fan operation — it is a
single-carrier scope fix. The corrected state would be: cc_1 scoped to Gravis Veterans, no fan copy needed.
Pool cap validation at both brackets: size 5 → cap 1 (1 Gravis Veteran carries it, matches); size 10 → cap 2
(2 Gravis Veterans carry it, matches). The per-n-models denominator is the unit's total model count (5 or 10),
which is correct. The deeper issue — the DW Veterans artifact default list — remains a known limitation but
does not block the scope fix.

**B18g remains OPEN** — banked with complete findings and fix pathway, not shipped.

**Files changed:** none (investigation only). 40K_Decision_Log_v3_0.md (D152). OPEN_ITEMS_BACKLOG.md updated.
SESSION_HANDOFF_85.md. NEXT_SESSION_PROMPT_86.md.

---

## D153 — B18g shipped: cc_1 scope corrected to Gravis Veterans via targeted post-processing override

**Session:** S86 (data turn — equipped_parser.py + unit_loadouts.json only; index.html unchanged).

**Decision.** Re-scope cc_1 on Decimus Kill Team `000004175` from `'Deathwatch Veterans'` to `'Gravis Veterans'`
via a targeted post-processing override in `equipped_parser.py`, applied after `fan_pooled_swaps` runs. The
override is keyed to `000004175` + option id `cc_1` and sets `scope = 'Gravis Veterans'`. No fan copy is
created; no entry is added to `_FAN_UNIT_ALLOWLIST`.

**Why a targeted override and not a general carrier-check.** The general approach — checking each option's
`replaces` weapon against the model group's `default_weapons` list — cannot work here because DW Veterans'
`default_weapons` is an artifact union that includes the infernus heavy bolter even though no individual DW
Veteran model carries one. A carrier-check against that list would return a false positive and would not
improve on the scope resolver's wrong answer. The targeted override bypasses the artifact entirely and directly
asserts the correct scope derived from the Datasheets.csv loadout text (D152 finding 1). A comment in the code
notes the general problem for future reference.

**Pool cap validation.**
- Size 5: 1 Gravis Veteran → cap 1 swap (per_n_models=5, max_per_n=1). Correct.
- Size 10: 2 Gravis Veterans → cap 2 swaps (per_n_models=5, max_per_n=1 × 2 triggers). Correct.

**Differential sweep result.** Full pipeline (6 passes) produces a file that differs from the pre-B18g
committed `unit_loadouts.json` in exactly one entry: `000004175`. Within that entry, exactly one field
changed: `options[cc_1].scope` from `'Deathwatch Veterans'` to `'Gravis Veterans'`. All other options
(cnt_2/cnt_3/cnt_4) and all other 336 option-set entries are byte-identical to the prior committed file.

**Checks on exit.** `repro_check.py` byte-identical, `units_repro_check.py` byte-identical, 48/49 assertions
(P3 known-fail unchanged), `pool_check.js` passes, `e10_check.js` passes, `b18d_check.js` passes.

**Files changed:** `equipped_parser.py` (targeted scope override block added after `fan_pooled_swaps`),
`unit_loadouts.json` (one field changed: `000004175` cc_1 scope). 40K_Decision_Log_v3_0.md (D153).
OPEN_ITEMS_BACKLOG.md updated. SESSION_HANDOFF_86.md. NEXT_SESSION_PROMPT_87.md.

---

## D154 — E7/E8 shipped, then E5 shipped in a follow-on engine turn

**Session:** S87 (two engine-only turns — index.html only; no data changes).

**E7 (spacing).** Added scoped CSS rules under `.list-item` that put deliberate margins between the points
display, the info (eye) button, the duplicate button, and the delete "×" in the center-panel unit cards. The
widest gap is between the info button and "×" per Ryan's ask — the goal is preventing accidental deletes.
Rules are scoped to `.list-item` so they do not affect the same-named `.info-btn` used in the Configuration
Panel (B47).

**E8 (undo delete).** Replaced the immediate-commit delete with a deferred-commit + undo toast:
- `removeUnit()` splices the entry out of `armyList` and remembers the entry, its index, and any attachments
  that pointed at it in a `pendingDelete` record.
- A 5-second bottom-centered toast shows "[unit] removed" plus Undo and dismiss controls.
- `scheduleSave()` is gated by a `suppressAutoSave` flag while a delete is pending, so the removal never
  reaches disk until the toast expires or is dismissed. This guarantees Undo restores the full pre-delete
  state (wargear, attachments, position) even if an autosave landed moments before the delete.
- On Undo, the entry is spliced back at its original index, attachments are restored, and selection returns
  to the restored entry.
- Deleting a second unit while a toast is showing commits the first delete (no chaining) — the simpler v1
  behavior Ryan explicitly picked.
- `commitPendingDelete()` is called defensively before every navigation path that could otherwise silently
  lose an in-flight delete: `showHome()`, `openList()`, `confirmCreateList()`, `clearList()`.

**E5 (banner points).** Split the single "List Points" figure into "Configured" and "Remaining":
- `#banner-points` markup replaced with two `.banner-pts-group` spans separated by a `.banner-sep`,
  reading "Configured N | Remaining M".
- `renderBanner()` computes `remaining = POINTS_CAP - total` and writes both figures. The over-cap red
  color on Configured is preserved. Remaining goes negative when Configured exceeds the cap — this is
  informational and matches the existing over-cap semantics.

**Version bumps.** v5.74 → v5.75 (E7+E8) → v5.76 (E5).

**Checks.** `repro_check.py` byte-identical throughout; `units_repro_check.py` byte-identical throughout;
`rules_assertions.py` 48/49 (P3 known-fail unchanged); `pool_check.js`, `e10_check.js`, `b18d_check.js`
all pass.

**Files changed:** `index.html`. Decision log (D154). OPEN_ITEMS_BACKLOG.md updated.

---

## D155 — B4 shipped: Primarch / Special / Fortification ability types routed alongside Datasheet

**Session:** S87 (data turn — wahapedia_transform.py + units.json only; index.html unchanged).

**Root cause.** `wahapedia_transform.index_abilities()` routed abilities by `type`, handling only Core /
Datasheet / Faction / Wargear. Every other type — Primarch, Special, "Special (правая колонка)",
"Fortification (левая колонка)", Wargear profile, "Без заголовка" — fell into an `unclassified_abilities`
flag bucket and was dropped from `unit_abil`, `unit_abil_desc`, and `unit_abil_defs`, so those ability names
and descriptions never made it into `units.json`.

The comment at the SUPREME COMMANDER name-match already noted the underlying insight: **type is a layout
bucket, not a semantic class** ("5 of 18 source rows are typed Fortification rather than Special"). The
"правая колонка" / "левая колонка" labels literally mean "right column" / "left column" in Russian — page
positions in the source rulebook, not ability classes.

**Fix.** Introduced `_DATASHEET_LIKE_TYPES = {"Primarch", "Special", "Special (правая колонка)",
"Fortification (левая колонка)"}` and extended the Datasheet branch to accept any type in that set. These
four types collectively cover: all Primarch aura + special abilities (Guilliman, Lion, Mortarion, Grimaldus);
SUPREME COMMANDER description text; INSPIRING COMMANDER (Fortis Kill Team, Wardens of Ultramar, etc.);
ATTACHED UNIT scoping text; LAST SURVIVOR, COMPANY HEROES, DEPLOYMENT, ORDERS, and other datasheet-block
rules that print in the same visual block as Datasheet-typed abilities.

**Not routed.**
- `Wargear profile` — content is per-weapon ability text ("One Shot", "Reverberating Summons"), belongs in
  the weapon-abilities pipeline, not the unit-abilities one. Deferred; not part of B4.
- `Без заголовка` — the single occurrence is Drop Pod's "Designer's Note", which is informational commentary
  not a rules ability. Skipped by design; anything new appearing under this type will still surface via the
  `unclassified_abilities` flag list.

**No effect on E9a/E9b.** The name-based must_be_warlord scan (line 307) and desc-based cannot_be_warlord
scan (line 319) run *before* the type-routing branch and see every row regardless of type. B4's routing
change does not touch what those two scans capture.

**Guilliman result.** Adds "Primarch of the XIII (Aura)", "Master of Battle", "Supreme Strategist", and the
"SUPREME COMMANDER" description text to his ability block — exactly what B4 called for.

**Differential sweep.** 37 units acquired new ability names / descriptions. Every changed unit differs in
exactly the same two fields: `model_groups[].unit_ability_names` and `unit_ability_details`. No other unit
fields changed anywhere in the file. Representative units and their additions: Guilliman (4 Primarch/Special);
Lion (4); Mortarion (4); Grimaldus (3 Primarch); Victrix Honour Guard (ATTACHED UNIT); Miasmic Malignifier
(DEPLOYMENT); Emperor's Champion (CHOSEN OF THE EMPEROR). All additions are verified against the source
datasheet's ability block.

**Checks on exit.** `repro_check.py` byte-identical; `units_repro_check.py` byte-identical (against the
newly regenerated `units.json`); `rules_assertions.py` 48/49 (P3 known-fail unchanged); `pool_check.js`,
`e10_check.js`, `b18d_check.js` all pass.

**Files changed:** `wahapedia_transform.py` (new constant + one branch condition), `units.json` (37 units'
`model_groups` + `unit_ability_details` updated). Decision log (D155). OPEN_ITEMS_BACKLOG.md updated.


## D156 — B37 closed on reconfirm: Captain wargear panes are already correctly fixed, no build needed

**Turn type:** mechanical (doc/label reconfirm pass, S88).

**What B37 asked.** Ryan's original S52 note: Captain's two wargear panes carried the same label so the
player couldn't tell which slot was which, and the two panes needed to lock each other out. D113 (S54)
fixed the first half by giving the Captain a single 10-endpoint bundle picker labelled "Captain Wargear."
What remained open was Ryan's second, truncated note ("Second, if a selection...") — never captured, and a
reconfirm against current code was banked instead of guessed at.

**Reconfirmed against v5.76.** Traced the full render path for the Captain (`000000073`) from
`unit_loadouts.json` through to the wargear pane builder in `index.html`:
- The raw loadout data still carries two parser-level option entries (`cho_1`, the compound pistol+melee
  swap; `cho_2`, the close-combat-only swap) — this is expected; they are the parser's decomposition of
  the datasheet, not what renders.
- `bundleSuppressesLoadout` returns true for the Captain's bundle (default relation is `owns`), and
  `bundleOwned` checks `replaces` part-by-part (the B36 fix), so both `cho_1` and `cho_2` are suppressed
  before the scope/group pass ever runs (`byScope` at line 3857 skips suppressed options outright).
- The only wargear control the Captain renders is the single "Captain Wargear" bundle picker: one radio
  group, one label, ten endpoints, exactly one selectable at a time by construction (default endpoint
  plus nine swaps). There is no second pane to mislabel and no cross-exclusivity to enforce — the
  single-control design makes Ryan's original complaint structurally impossible to reproduce.

**Conclusion.** The remaining, undocumented half of B37 cannot be a live bug against current code: there
is exactly one control, so a two-pane labelling/locking problem has nothing left to attach to. Whatever
Ryan's truncated second note was, it predates D113's redesign and no longer has a target. Closing B37
outright rather than carrying a speculative reopen.

**Files changed:** none (index.html, unit_loadouts.json, bundled_swaps.json unchanged — this was a
read-only reconfirm). Decision log (D156). OPEN_ITEMS_BACKLOG.md updated (B37 moved to Closed/Shipped).


## D157 — B7 reshaped: multi-leader mechanic already shipped in B38 cluster; residual work split into B7a (stack cap) and B7b (combined popup with aura markers)

**Turn type:** analysis (S89). Read the B7 ticket in full, read D144 (B38 design), traced the current
leader-attach machinery end to end against v5.76, and put three questions to Ryan; his answers reshape the
ticket. No code, data, or documents shipped this turn beyond the log entry and the backlog reshape.

**Finding — B7's ticket text is stale.** B7 was written when "the tool only allows one leader per unit."
That statement no longer holds against current data and code. B38's cluster (D144–D147, Sessions 79–81) shipped
the entire multi-leader mechanic:

- **Engine.** `canAttachLeader` validates against the full attached-leader set via symmetric-pairwise
  `permitsCoLeader`, order-independent.
- **Data.** `co_leader_eligible_with` populated on 12 SM named-shape units (D146); `co_leader_any = true`
  populated on 6 DG generic-shape units (D147).
- **Render.** `renderList` already loops `attachedLeaders` (plural) inside a `bodyguard-block` container;
  the leader-assignment dropdown filters via `canAttachLeader`.
- **Duplicate.** `duplicateUnit` iterates all attached leaders individually, honouring Epic Hero exclusion
  and each leader's own limit.
- **Weapon pools.** `b18d_check.js` scenarios cover leader-scoped pools (`cnt_3_ldr`, `cc_1_ldr`) coexisting
  with body pools and pass.

E9 (the other named cluster-mate) is done (D139–D140). So the "leader-system" umbrella that B7 pointed at
is thin: most of it shipped without ever bearing a B7 label.

**Q1/Q2 (Ryan) — rules read on stack cap.** Ryan: the general 40K rule is one leader per bodyguard unless a
datasheet rule permits a second; the cap is 1 by default and 2 when lifted. Confirms my read of core rules
19.01 ("Unless otherwise stated, each bodyguard unit can only have one leader unit and one support unit
attached to it") and every co-leader override clause I sampled: SM named-shape footers ("even if **one**
Captain / Chapter Master / Lieutenant…"), DG generic footer ("even if **one other Leader** unit has already
been attached"), and bodyguard-side "up to two Leader units" clauses (Orks Boyz, Kroot Farstalkers) all read
as +1 lifts to a cap of 2. The one datasheet-side exception surfaced in the wider dataset (Cybernetica
Datasmith: "even if **one or more** other CYBERNETICA DATASMITH models have already been attached") does
not apply to any built faction today.

**Consequence for D144.** The D144 pairwise-permits model — symmetric-pairwise check with no stack-size
cap — is over-permissive relative to Ryan's rule. Under D144's logic, a Captain + Lieutenant + Apothecary +
Ancient stack on one Intercessor Squad passes if each pair has a permits() edge; under the actual rule, the
stack caps at 2. The `permitsCoLeader` pairwise legality check itself is fine (same-name block plus
either-side clause coverage), and the SM/DG data population it consumes is correct. The single missing piece
is a stack-size guard.

**Q3 (Ryan) — combined popup shape.** Ryan chose stacked panels (Option (a) from the session findings):
one modal renders the bodyguard + all attached leaders as sequential panels, matching how 40K attached
units work rules-wise (each model keeps its own profile per 19.02–19.04). Trigger: the bodyguard's ⓘ
becomes the combined view; leader ⓘs stay as single-datasheet views. On the follow-up question — how
leader auras that modify the bodyguard's stats should show — Ryan rejected pure text (players will miss
auras) and rejected full numeric conferral with per-rule footnotes (data-classification scope creep).
Chosen: a per-stat visual marker (asterisk) on affected stats in the bodyguard's stat block, and reciprocally
in the future for auras that flow the other direction. Markers are a cue to look at the abilities section
for the specific rule; no numeric modification of stat values, no engine legality effect, no pricing effect.

**Reshape. B7 → CLOSED (this turn); two new tickets stand up in its place.**

- **B7a — leader-stack cap semantics (engine, S).** Add a stack-size guard to `canAttachLeader`: after the
  `leaderEligible` check and the same-name / pairwise-permits checks, refuse when the existing attached
  count is already ≥ 2. Keeps `permitsCoLeader` as-is (correct for the pair). New `rules_assertions.py`
  guard `B7a-1` verifies the cap holds: a 2-leader stack refuses a 3rd attach regardless of pairwise
  permits. New `e10_check.js` scenario extends the existing 1-leader-duplicate case to a 2-leader stack.
  Zero data change; engine-only turn. Estimated ship: one session.
- **B7b — combined attached-unit popup with per-stat aura markers (design + data + render, M).** New modal
  view opened from the bodyguard's ⓘ: header showing the composite unit name ("Intercessor Squad + Captain +
  Lieutenant"), then a stacked panel for each member using the existing `buildModalConfigured` renderer per
  entry. New data field on each unit's first model group, `bodyguard_stat_flags` (list of stat names this
  unit's abilities affect on an attached bodyguard, populated by hand-audit of each leader's ability text);
  reciprocally `leader_stat_flags` on bodyguard units when audit finds cases. Combined popup unions the flag
  sets across all attached leaders and marks each affected stat with an asterisk on the bodyguard's stat
  block (reciprocal on leader stat blocks). Leader ⓘ behaviour unchanged — single-datasheet view.

**Dev-manager calls made under recommendation authority (both reversible):**

- **Markable stat list for B7b:** INV, FNP, LD, T, M, OC. These are the stat lines that can meaningfully
  be modified by a leader aura in 11e; rare cases (W, SV) can be added if the audit surfaces them.
- **Direction for B7b:** leader→bodyguard flags populated first (the common case). Bodyguard→leader flags
  added as the audit surfaces cases; not gating B7b's ship.

**Sequencing.** B7a first (engine, small, no design dependency), then B7b (design pass → data-classification
audit → render). B7b's data-classification audit is the heaviest single piece and will surface ambiguous
cases (conditional stat modifiers, e.g., "4+ INV vs ranged" — does that get an INV marker?) that need Ryan
in the loop; those get batched and surfaced together, not one at a time.

**Files changed:** decision log (D157). `OPEN_ITEMS_BACKLOG.md` (B7 marked closed with reshape pointer;
B7a and B7b added under Bugs and Enhancements respectively; Cross-cutting note updated to reflect the
leader-system cluster status). No code or data file changed this turn. `index.html` version unchanged
(5.76); `rules_assertions.py` 48/49 (P3 known-fail unchanged); repro guards remain byte-identical.

## D158 — B7a shipped: stack-size cap of 2 added to canAttachLeader

Engine-only turn, zero data change. `canAttachLeader` gained one guard: after the `leaderEligible` check
and before the pairwise-permits loop, refuse any attach when the bodyguard already carries 2 attached
leaders — `if (existingLeaders.length >= 2) return false;`. Placed before the loop so a 2-leader stack can
never slip through on a permissive pairwise result; the guard is the sole authority on the cap, independent
of what `permitsCoLeader` says. `permitsCoLeader` itself is untouched — its same-name and either-side-clause
logic stays correct for the pair (D144).

New `rules_assertions.py` guard `B7a-1` lifts the function source, confirms the guard text is present and
sits ahead of the pairwise loop, confirms `permitsCoLeader` is still called (so the pair rule wasn't
accidentally dropped), then models the shape in Python with permits stubbed to always-allow to prove the
cap alone is what refuses a 3rd attach. New `e10_check.js` scenario 6 extends the existing 1-leader-duplicate
coverage: duplicates a body carrying a 2-leader stack (Tallyman + Foul Blightspawn on Plague Marines, both
under their own instance limits), confirms both leader copies land on the body copy, then calls
`canAttachLeader` directly to confirm a 3rd leader (Biologus Putrifier, whose `coLeaderWith` would pairwise-permit
against Tallyman) is refused on the now-2-stacked body copy, and that the same leader still attaches cleanly
to a fresh, unstacked body — proving the cap doesn't overreach.

**Files changed:** `index.html` (v5.76 → v5.77, `canAttachLeader` guard added). `rules_assertions.py`
(`B7a-1` added, 48/49 → 49/50). `e10_check.js` (scenario 6 added). Decision log (D158).
`OPEN_ITEMS_BACKLOG.md` (B7a closed/shipped).

## D159 — B7b shipped: combined attached-unit popup with per-stat aura markers

**Turn type:** analysis + mixed data-audit + render turn (S91), per D157's sequencing. Design pass first
(modal composition mechanics, trigger routing, header shape), then hand-audit of leader unit abilities
across all built SM+DG leaders, then render/wire.

**Design decisions (dev-manager calls, no interruption to Ryan):**

- **Modal composition.** New `openModalCombined(bodyguardListId)` collects the bodyguard entry, its
  attached leaders (via existing `getAttachedLeaders`), and each leader's raw. New `buildModalCombined`
  renders the bodyguard's `buildModalConfigured` first (with aura flags applied), then each attached
  leader's `buildModalConfigured` (plain, no reciprocal), separated by a stronger `combined-member-divider`.
  Each panel carries a bolded `combined-member-header` showing the member's unit name.
- **Aura union.** `openModalCombined` walks each attached leader's `raw.model_groups[0].bodyguard_stat_flags`,
  collects into a Set, converts to an Array, and passes as `auraFlags` to `buildModalConfigured` for the
  bodyguard only. `buildModalConfigured` forwards `auraFlags` to `buildStatTable` for the **first** model
  group only (the Character panel for RCS; the base Infantry/Vehicle line otherwise).
- **buildStatTable extension.** New 4th parameter `auraFlags` (list of stat name strings). Existing
  wargear-flag star mechanics for INV/FNP/W/SV extended to fire on aura flags as well. New asterisk
  support added for LD/T/M/OC (which had no override/flag machinery before). Legend text adapts: any aura
  star anywhere -> `* see Abilities`; pure-wargear stars -> the existing `* see Wargear Abilities`; both ->
  the broader Abilities label (covers both sources).
- **Trigger routing.** In `renderList`, the bodyguard's info button branches on `hasLeaders`: with attached
  leaders it calls `openModalCombined(entry.listId)`, else `openModalConfigured(entry.listId)` (unchanged).
  Tooltip flips between "View attached unit" and "View configured datasheet". Leader ⓘs unchanged.
- **Composite header title.** `bodyguard.unit_name + ' + ' + leader1.unit_name + ...` — bodyguard first,
  leaders in attach order (`getAttachedLeaders` order). Modal mode badge: `Attached Unit`.
- **Markable stat list held to D157.** INV, FNP, LD, T, M, OC. Audit surfaced no W or SV cases.

**Data-classification audit (heaviest single piece).** Hand-audited every SM+DG leader unit's
`unit_ability_names` + `unit_ability_details` against the markable-stat list. **81 built leader units** in
scope. **16 carry non-empty `bodyguard_stat_flags`:**

- **INV (1):** Librarian `000002266` (Mental Fortress — 4+ invulnerable save while leading).
- **FNP (8, one also carries INV):** Sanguinary Priest `000000158` (FNP 5+ unconditional); Iron Father
  Feirros `000000127` (Rites of Tempering — FNP 5+ unconditional); Librarian `000002266`, Librarian In
  Terminator Armour `000000079`, Librarian In Phobos Armour `000000119`, Chief Librarian Tigurius `000001611`,
  Ezekiel `000000226` (all Psychic Hood family, FNP 4+ vs Psychic ± mortal); Chaplain In Terminator Armour
  `000000115` (Recitation of Faith — FNP 4+ vs mortal).
- **OC (5):** Bladeguard Ancient `000001165`, Ancient In Terminator Armour `000002677`, Ancient `000002775`
  (Astartes Banner family, +1 OC); Ravenwing Command Squad `000002748` (Astartes Banner via contains-clause);
  Icon Bearer `000002750` (Unclean Icon, +1 OC).
- **M (2):** Njal Stormcaller `000000292` (Wind Walker — +6" Move during Advance, until end of phase);
  Noxious Blightbringer `000001058` (Sickening Vitality — +1" Move unconditional).
- **T (1):** Chaplain Grimaldus `000002792` (Column from the Major Altar — Temple Relic selection, +1 T).
- **LD (0):** no built leader confers a bare LD stat modification.

**Ambiguity calls made under recommendation authority (all reversible data-only edits if Ryan overrides):**

1. **Conditional FNP flagged.** Every "Feel No Pain N+ ability against Psychic Attacks" and "against mortal
   wounds" aura receives the FNP marker. Reasoning: the asterisk is a *cue*, not a numeric conferral; the
   reader looks at the abilities section for the specific condition. Withholding the marker because the
   condition doesn't cover every attack understates defensive capability that materially affects gameplay.
   Reversible: drop the six conditional-FNP entries from `FLAG_MAP` and rebuild.
2. **Temporary M flagged.** Wind Walker's +6" Move is "during Advance, until end of phase" — active only in
   part of the turn — but it does modify the Move characteristic when it fires. Flagged. Same reversibility.
3. **Temple-Relic-select T flagged.** Grimaldus's Column from the Major Altar is one of three Temple Relics
   selected in the Command phase (not always Column). Since the ability is always available for selection,
   flagged T. Same reversibility.
4. **RCS OC flagged.** "While this unit contains a Ravenwing Ancient, add 1 to OC of models in this unit."
   RCS is itself a leader-attach unit; when attached, rules 19.02–19.04 treat "this unit" as the merged
   Attached unit, so the +1 OC lands on the bodyguard's models. Flagged.
5. **What was NOT flagged:** weapon-ability auras ([LETHAL HITS], [SUS HITS], [PRECISION], [DEV WOUNDS],
   [ASSAULT], [LANCE], [IGNORES COVER], etc.); Hit/Wound/Charge/Advance roll modifiers; ability grants
   without stat mod (Fights First, Scouts, Stealth, [PRECISION]); army-wide INSPIRING COMMANDER effects
   (they're fielding-time buffs to specific army-list units, not attach auras); self-only stat auras (a
   leader boosting its own OC on kill); defensive rules that don't modify a bodyguard stat (subtract-from-
   Wound-roll, subtract-from-Damage, "cannot be targeted by ranged attacks unless within 12\""); warlord-only
   effects.

**Data delta.** New `add_bodyguard_stat_flags.py` script hardcodes the 16-unit `FLAG_MAP`, sets an empty
`bodyguard_stat_flags` list on every model group by default, then populates the 16 flagged units on their
first model group. Idempotent, guards for missing/drifted unit_ids and self-inconsistent flag values.
Runs after `add_co_leader.py` in the `units_repro_check.py` chain. `units.json` regenerated end-to-end from
source — 270 units gained the empty field, 16 carry non-empty values. Diff scoped to exactly the audited
field; no other units.json content changed. Byte-identical repro under updated chain.

**Render layer.** `openModalCombined`, `buildModalCombined` added. `buildModalConfigured` signature gained
optional `auraFlags` (backwards-compatible; leader ⓘ and full-view paths pass nothing). `buildStatTable`
signature gained optional `auraFlags`. Star support added for LD/T/M/OC cells. Legend adapts to aura vs
wargear source. Roster bodyguard ⓘ routes to `openModalCombined` when `hasLeaders`, else
`openModalConfigured`. Leader ⓘs unchanged. New CSS: `combined-member-divider` (stronger 2px separator)
and `combined-member-header` (bolded gold caption).

**Verification.** New `rules_assertions.py` guard `B7b-1` (49/50 → 50/51): Part A confirms the exact 16-unit
flag set with expected contents and no unit missing the field; Part B lifts the render functions from
`index.html` and confirms `openModalCombined` reads `bodyguard_stat_flags` and calls `getAttachedLeaders`,
`buildModalCombined` calls `buildModalConfigured` and inserts the divider, both `buildModalConfigured` and
`buildStatTable` carry the new `auraFlags` parameter, and `renderList` routes the bodyguard ⓘ conditionally.
Baseline: `repro_check.py` byte-identical on unit_loadouts.json; `units_repro_check.py` byte-identical on
the regenerated units.json under the updated chain; `pool_check.js`, `e10_check.js`, `b18d_check.js`,
`stat_check.js`, `default_check.js`, `pts_check.js`, `limit_check.js` all pass. `bundle_check.js` still
carries the two pre-existing failures that reproduce on the untouched project (not a regression). P3 known-fail
unchanged (`pipeline_manifest.py` still absent).

**What was NOT done (deferred, not regressions):**

- Reciprocal `leader_stat_flags` on bodyguard units (bodyguard→leader auras) not populated. Audit surfaced
  no compelling case for the built SM+DG set — bodyguards don't confer aura stat mods on their attached
  leaders in the current data. Ryan can revisit if a specific case comes up.
- The live render still needs Ryan's eyeball: a bodyguard with 1 attached leader (aura marker path) and
  with 2 attached leaders (union path). Data + render checks pass in code; the visual read is a manual step.
- No numeric stat conferral. Asterisks only, per Ryan's Q3 choice in D157.
- No engine legality effect, no pricing effect. Display-only ticket as scoped.

**Files changed.** New: `add_bodyguard_stat_flags.py`. Changed: `units.json` (16 units flagged, 254 gain
empty list); `units_repro_check.py` (adds new script to REQUIRED and to the chain); `index.html`
(v5.77 → v5.78, five function edits + two CSS additions + one roster tweak); `rules_assertions.py`
(`B7b-1` added, 49/50 → 50/51); `40K_Decision_Log_v3_0.md` (D159); `OPEN_ITEMS_BACKLOG.md` (B7b closed/shipped).

---

## D158 — B13 Piece 1: Optional model toggle for Victrix Honour Guard (S92)

**Context.** Victrix Honour Guard (`000004185`) has two optional Epic Hero models in its composition: 0-1 Chapter Ancient and 0-1 Chapter Champion. The data structure in `unit_loadouts.json` already expressed these correctly as `count: { optional: true, max: 1 }` on their model groups. The `fills_to_size` body group (Victrix Honour Guard) always fills the remainder. The engine's `loGroupCounts` was ignoring optional groups (always 0) with a comment deferring toggle work.

**Rules determination.** Chapter Ancient and Chapter Champion *replace* Victrix body models — the unit is always exactly 3 or 6 models total regardless of how many optionals are included. Confirmed by MFM: only "3 models / 6 models" brackets, no per-optional cost. The composition rows (0-1 Ancient, 0-1 Champion, 1-6 Victrix) sum to the same bracket once you account for replacements.

**What shipped (v5.79).**

- New helper `loOptCounts(def, entry)` reads `entry.wargear['opt_' + groupName]` for every optional group and returns `{groupName: 0|1}`.
- `loGroupCounts(def, size, optCounts)` — third parameter. Included optionals deduct from `reserved` so `fills_to_size` body gets `size - toggled_count`. Default `{}` leaves optional groups at 0 (same as before for all existing callers).
- `loRollup(def, size, sel, optCounts)` — fourth parameter, threaded to `loGroupCounts`. All 6 `loGroupCounts` call sites and all 5 `loRollup` call sites updated.
- New handler `editLoadoutOptional(listId, groupName)` — flips `entry.wargear['opt_' + groupName]` 0↔1.
- New render block in the config panel (before main wargear loop): iterates optional groups, renders a green-tinted include/exclude toggle per group. EPIC HERO suffix stripped from display name.
- New CSS: `.opt-group-block`, `.opt-group-label`, `.opt-group-toggle`, `.opt-toggle-btn`, `.opt-toggle-btn.included`.
- Makeup line in the popup self-corrects automatically (reads updated `loGroupCounts` output).
- No data changes. No points logic changes (optional models are free — MFM has no separate cost).

---

## D159 — B13 Piece 2: Embedded Epic Hero cap for optional model groups (S93)

**Context.** Chapter Ancient and Chapter Champion in Victrix are EPIC HERO *models* — 1-per-army each. A player could previously include the same Ancient or Champion in multiple Victrix copies. The existing `instanceLimit` caps whole Epic Hero *units*, not models embedded in another unit's optional composition.

**Detection mechanism.** The two optional groups are already named "Chapter Ancient - EPIC HERO" and "Chapter Champion - EPIC HERO" in `unit_loadouts.json`. The engine detects embedded optional Epic Heroes by checking whether an optional group's name contains the substring "EPIC HERO" (case-insensitive). No new field in the data is needed. A sweep of all optional groups in `unit_loadouts.json` confirms only Victrix's two groups carry this pattern today — assertion B13-1 guards this going forward.

**What shipped (v5.80).**

- New helper `isOptEpicHeroBlocked(thisListId, groupName)` — returns true if any other entry in `armyList` has the same `opt_` key set to 1. Only fires when `groupName.toUpperCase().includes('EPIC HERO')`.
- `editLoadoutOptional` updated: before toggling on, checks `isOptEpicHeroBlocked`; blocks silently if true. Turning off is always allowed.
- Render: toggle button gains `.blocked` class and `opt-group-note` ("Already included in another Victrix unit") when blocked. No `onclick` attribute on a blocked button.
- New CSS: `.opt-toggle-btn.blocked`, `.opt-toggle-btn:hover:not(.blocked)`, `.opt-group-note`.
- New assertion `B13-1` in `rules_assertions.py`: confirms Victrix has exactly two optional EPIC HERO groups, no other unit has such groups, and `isOptEpicHeroBlocked` + the guard in `editLoadoutOptional` are present in `index.html`. Assertions 50/51 → 51/52 (P3 known-fail unchanged).

**Baseline.** `repro_check.py` and `units_repro_check.py` byte-identical (data unchanged). All JS harnesses pass. `bundle_check.js` pre-existing 2 failures unchanged.

---

## D160 — B34 Piece 1: Size-gated wargear swaps as `required_size` (data + parser) (S94)

**Context.** Two units in the dataset carry a wargear swap that is only legal at
one specific unit size, expressed in `Datasheets_options.csv` as "If this unit
contains [only] N models…" — never any other size. Both lines were `UNMATCHED`
in `unit_loadouts.json` prior to this session and the swaps were silently absent
from play:

- Wolf Scouts (`000004182`, line 4): "If this unit contains 12 models, 1 Wolf
  Scout's plasma pistol can be replaced with 1 instigator bolt carbine." Only
  legal at the top (12-model) bracket.
- Blightlord Terminators (`000001372`, line 6): "If this unit contains only 3
  models, 1 Blightlord Terminator's combi-bolter and bubotic blade can be
  replaced with 1 plague spewer and 1 close combat weapon." Only legal at the
  bottom (3-model) bracket.

**Rules determination — mechanism shape.** The two units gate opposite ends:
Wolf Scouts unlocks at the *top* bracket, Blightlord Terminators unlocks at the
*bottom* bracket. A "minimum-size" or floor mechanism (`min_unit_size:N` = legal
at ≥ N) would get Blightlord backwards. The correct mechanism is exact-size
match, not a threshold. Naming: `required_size` (exact integer). An option
carrying `required_size:N` is legal only when the unit's current size bracket
equals N; at any other bracket the option is suppressed.

**Blast radius.** A grep across all `_parser_flags` in `unit_loadouts.json` for
"if this unit contains" or "if this unit is … model" matched exactly these two
units. No other unit in the current dataset carries this pattern. Both
`UNMATCHED` flags are cleared by the new classifier.

**Turn discipline.** Data-only turn per D-log convention (engine and data
changes never mix). The data field is dormant until the engine turn (B34 Piece
2) teaches `loRollup` and the config-panel render to suppress options whose
`required_size` doesn't match the current bracket.

**What shipped.**

- `loadout_parser.py` — new classifier `classify_size_gated_swap` registered in
  `CLASSIFIERS` immediately before `classify_one_model_swap` so the more
  specific pattern wins. Captures bearer name as scope hint (multi-word
  bearers like "Wolf Scout" and "Blightlord Terminator" resolve correctly, not
  falling through to `_scope_hint: 'body'` which broke on units with no
  `fills_to_size` group). Emits `replaces_raw` and `replacement_raw` so the
  count-op serializer's compound splitter handles Blightlord's compound
  replacement ("plague spewer + close combat weapon") intact.
- Serializer plumb: `entry['required_size'] = op['required_size']` inside the
  count-op emit path, guarded so options without the field are unaffected.
- `unit_loadouts.json` — regenerated end-to-end through `loadout_parser.py` +
  `equipped_parser.py` (5-faction + datasheets pass). Diff-guard confirms
  exactly 2 units changed (`000004182`, `000001372`) and no other unit's
  serialization moved by one byte. File size 200,352 → 200,665 bytes.
- `rules_assertions.py` — new `B34-1` asserts both units carry a count option
  with the correct `required_size` (12 for Wolf Scouts, 3 for Blightlord
  Terminators). Assertions 51/52 → 52/53 (P3 known-fail unchanged).

**What was corrected from the S94 kickoff prompt.** The prompt named the wrong
unit ID (`000000328`, which is Assault Squad), the wrong rule text (a nonexistent
"shotgun → melta gun" swap on Wolf Scouts), and the wrong mechanism shape
(`min_unit_size` as a floor). All three were caught in Turn 1 diagnosis before
any code was written. D160's decisions replace the kickoff's assumptions.

**Baseline.** `repro_check.py` byte-identical against the promoted
`unit_loadouts.json`. `units_repro_check.py` byte-identical (units.json
untouched). `rules_assertions.py` 52/53. `pool_check.js`, `e10_check.js`,
`b18d_check.js` all pass. Pre-existing failures on `stat_check.js`,
`default_check.js`, `pts_check.js`, `limit_check.js`, and `bundle_check.js` are
caused by the project's `index.html` being synced at v5.61 rather than v5.80 —
these fail identically at the baseline before this session's changes and are
not regressions.

**Deferred to B34 Piece 2 (engine turn).** The engine (`loRollup` and the
config-panel render path in `index.html`) still needs to read `required_size`
and suppress options whose value doesn't equal the current bracket. Until that
ships, the data change is inert and the swap is still absent from play —
strictly no worse than baseline (both were absent before too), but the ticket
is not fully closed until the engine reads the field.

## D161 — B34 Piece 2: Size-gated wargear swaps enforced in engine (S95)

**Context.** D160 landed the data half of B34: two units in the dataset (Wolf
Scouts `000004182`, Blightlord Terminators `000001372`) carry a count option
tagged `required_size:N` (12 and 3 respectively). The field was dormant — the
engine had no reader for it, so the swap was still absent from play even
though the data was correct. This session teaches the engine the exact-match
gate and closes the ticket.

**Rules determination.** No rules-legality question was open. D160 already
fixed the mechanism as exact-match integer, not a floor and not a ceiling. The
engine turn is a mechanical enforcement of a decided rule.

**Mechanism choice — one predicate, two callsites.** A size-gated option
should be inert at every bracket except its `required_size`: hidden from the
config panel, its stale saved pick cleared, and skipped by the rollup so no
replacement is emitted and no source weapon is consumed. Two independent
callsites govern this: `buildLoadoutHtml` (the UI layer, which already carries
a `suppressed(o)` predicate that folds every hide-this-option reason into one
place) and `loRollup` (the emission layer, which iterates `def.options` in
three loops right at its entry — the byScope build plus two pool-cap init
loops). Rather than sprinkle the gate into each count-option branch inside
loRollup (four sites, each with its own subtlety), the change filters
`def.options → sizeActiveOptions` once at loRollup entry, and every downstream
loop reads the filtered list. On the UI side, a `sizeGated(o)` predicate is
added to the existing `suppressed(o)` chain, so the same rule fires the
existing stale-selection clear (line 3899-3900) — a user who picks the option
at 12 models and drops the unit to 6 has the stale pick cleared automatically,
consistent with how every other suppression predicate already behaves.

**Blast radius.** A scan across `unit_loadouts.json` confirms exactly two
options carry `required_size` (`000004182/cnt_4` and `000001372/cnt_6`).
Every other option is untouched by the filter. Existing checks
(`pool_check.js`, `e10_check.js`, `b18d_check.js`, `stat_check.js`,
`default_check.js`, `pts_check.js`, `limit_check.js`) all pass unchanged
against the new engine; `bundle_check.js`'s two pre-existing failures are
unaffected.

**What shipped.**

- `index.html` v5.80 → v5.81:
  - `loRollup`: at entry, `def.options` is filtered to
    `sizeActiveOptions` — options whose `required_size` is absent or equals
    the current `size` bracket. All three top-level option loops (byScope
    build, per-N pool-cap init, max_total pool-cap init) read the filtered
    list. No changes needed in the per-model-group processing below because
    those iterate `byScope[g.name]`, which is now already filtered.
  - `buildLoadoutHtml`: `sizeGated(o)` predicate added and folded into the
    existing `suppressed(o)` chain, alongside `brokenChoice`, `srcMissing`,
    and `bundleOwned`. Stale-selection clear (line 3899-3900) already
    handles the cleanup path.

- `required_size_check.js` (**NET NEW**) — B34 Piece 2 harness. Loads the
  real `loRollup` slice out of `index.html` and proves the gate on both
  units at every declared bracket:
  - Wolf Scouts at bracket 6 (non-matching): stale `countBy[cnt_4]=1` pick
    is inert; instigator bolt carbine not emitted; plasma pistol survives.
  - Wolf Scouts at bracket 12 (matching): empty pick leaves plasma pistol
    intact; pick fires, emitting one instigator bolt carbine and consuming
    one plasma pistol.
  - Blightlord Terminators at brackets 5 and 10 (non-matching): stale pick
    inert; plague spewer not emitted; combi-bolter survives.
  - Blightlord Terminators at bracket 3 (matching): pick fires, emitting
    one plague spewer, consuming one combi-bolter and one bubotic blade.

- `rules_assertions.py` — new `B34-2` data-integrity assertion: every
  `required_size` value in `unit_loadouts.json` is a member of that unit's
  declared `size_brackets`. Catches a stale gate if brackets ever change
  (e.g. a future edition removes the top bracket but leaves the gate
  pointing at it, rendering the option unreachable at every bracket). 52/53
  → 53/54 (P3 known-fail unchanged).

- `stat_check.js` — one-line fix to the `entryOf()` test helper: added
  `wargear: {}` default. Real roster entries always carry this field
  (`index.html` line 1342/1399). The gap only surfaced now because
  `stat_check.js` had not run against the correct engine version for
  several sessions; its full unit sweep (section 5) walks every optional
  model group and the missing field crashed on the first optional-group
  hit (Wolf Guard Headtakers `000004131`, unrelated to B34). Test-only
  file; not served.

**Baseline at close.** `repro_check.py` and `units_repro_check.py` both
byte-identical. `rules_assertions.py` 53/54 (P3 known-fail unchanged —
`pipeline_manifest.py` still absent from project sync). All five
version-dependent JS guards (`stat_check.js`, `default_check.js`,
`pts_check.js`, `limit_check.js`, `bundle_check.js` with its two known
pre-existing failures) pass now that `index.html` is at v5.81. Version-
independent guards (`pool_check.js`, `e10_check.js`, `b18d_check.js`,
`required_size_check.js`) all pass.

**B34 closed.** With Piece 2 shipped, both size-gated swaps are now legal
at their unlock bracket and inert everywhere else — enforced in the UI,
enforced in the rollup, and asserted in both a JS engine guard and a data-
integrity assertion.

## D162 — B53: combined attached-unit popup panel order flipped to leader-first (S96)

**Turn type:** engine-only.

**What.** The B7b combined popup (`buildModalCombined`) stacked its member
panels bodyguard-first, then each leader. The center Army List panel stacks
the opposite way — leader row(s) first, bodyguard row underneath (confirmed
in `renderList`, where the leader loop runs before the bodyguard row is
appended to the same `bodyguard-block`). Ryan flagged the mismatch with a
screenshot (S94): Bloodletters (bodyguard) rendering above Skulltaker
(leader) in the popup, reversed from the list.

**Fix.** `buildModalCombined` now builds each leader panel first (attach
order), then the bodyguard panel last. The bodyguard panel still receives
the `auraFlags` union (unchanged — aura markers are a bodyguard-only
concept per D159 and don't depend on render order). No change to
`openModalCombined`'s title line (still bodyguard + leaders, attach order)
— B53 only flagged panel stacking, not the title text, so title order was
left as-is to keep the turn narrowly scoped.

**Verification.** All nine harness checks (`pool_check.js`, `e10_check.js`,
`b18d_check.js`, `required_size_check.js`, `stat_check.js`,
`default_check.js`, `pts_check.js`, `limit_check.js`) pass unchanged
against v5.82 — none of them assert panel order, so this is confirmation
of no regression, not proof of the fix. **The actual stacking still needs
Ryan's live-render eyeball** — no harness checks DOM order.

`index.html` v5.81 → v5.82.

## D163 — E15: Transport ability text added alongside the Transport keyword (S97)

**Turn type:** data-only.

**What.** Transport-capable units carried the TRANSPORT keyword but no ability text
explaining capacity or excluded model types. `Datasheets.csv` already carries this text in
its dedicated `transport` column; the pipeline never routed it anywhere. `wahapedia_transform.py`
now reads that column per datasheet and, where non-empty, adds a "Transport" entry to
`unit_abil` / `unit_abil_desc` — the same shared-ability-name-different-text path B1 already
built for cases like this. Global fallback entry also set via `unit_abil_defs.setdefault`.

**Scope check.** 17 units changed in `units.json`: Land Raider, Land Raider Crusader, Land
Raider Redeemer, Drop Pod, Razorback, Stormraven Gunship, Impulsor (x2, SM + BT), Repulsor
(x2), Repulsor Executioner (x2), Rhino, Chaos Rhino, Chaos Land Raider, Corvus Blackstar.
Deep key-diff confirmed all 17 changes are scoped to exactly `unit_ability_details.Transport`
(added) and the `Transport` entry in each affected model group's `unit_ability_names` list —
nothing else moved. No engine change needed: both abilities-rendering call sites in
`index.html` (lines 4390/4402, 4608/4620) already read `unit_ability_names` /
`unit_ability_details` generically with no name whitelist, so the new ability renders on the
existing B49 Abilities section without touching `index.html`. Version stays v5.82.

**Verification.** `units_repro_check.py` byte-identical against the new `units.json`.
`repro_check.py` (loadouts) unaffected — byte-identical, untouched by this turn.
`rules_assertions.py` 53/54 (P3 known-fail unchanged). All nine harness checks
(`pool_check.js`, `e10_check.js`, `b18d_check.js`, `required_size_check.js`, `stat_check.js`,
`default_check.js`, `pts_check.js`, `limit_check.js`) pass; `bundle_check.js` shows its same 2
pre-existing documented failures (B36 residual, untouched). `pts_check.js` also reports one
pre-existing default-cost mismatch (Terminator Assault Squad `000000118`, 155 vs 180) —
confirmed unrelated and pre-existing (B35, held for Ryan; not touched this turn).

**Finding, not shipped — abilities.json drift.** The same pipeline run that produced the
clean `units.json` also regenerated `abilities.json` (the global ability-name glossary) with
76 new entries far outside Transport's scope — chapter/detachment ability names like "CRIMSON
FISTS" and "CHAPTER MASTER OF THE RAVEN GUARD" that have nothing to do with E15. This means
the committed `abilities.json` has drifted from what the current pipeline + current source
CSVs would produce, for reasons unrelated to this turn. Left uninvestigated and unshipped to
keep this turn scoped to E15 only — see new backlog item **B55** for follow-up. `units.json` does not read from `abilities.json` for per-unit rendering (that's the
`unit_ability_details` fallback path only), so this drift does not affect what E15 shipped.

**E15 closed.**

## D164 — B55: the four merged glossary lookups were stale; reproduction gate extended to cover them (S98)

**Turn type:** data-only (data + harness; no `index.html` change, stays v5.82).

**What was actually wrong.** B55 reported `abilities.json` producing 76 entries the committed
file lacked. Diagnosis found the drift was not a regression and was wider than reported: **all
four** lookups `merge_factions.py` unions alongside `units.json` had drifted from what the
current pipeline produces.

- `abilities.json` — 76 rebuild-only names, 0 lost, 33 text changes
- `rules.json` — 5 rebuild-only names, 0 lost, 4 text changes
- `keywords.json` — 1 rebuild-only name, 0 lost, 0 text changes
- `weapon_abilities.json` — 1 rebuild-only, 1 lost, 1 text change
- `faction_taxonomy.json` — identical (pure pass-through)

**The additions are legitimate growth, not a leak.** Nothing was lost from three of the four
files. The new names are overwhelmingly Death Guard abilities that entered the source when DG
was built, plus SM entries added by parser work since the lookups were last regenerated —
including E15's own `Transport`, added the session before this one. The 13 all-caps entries
(`SUPREME COMMANDER`, `CRIMSON FISTS`, `CHAPTER MASTER OF THE RAVEN GUARD`) are the same
Wahapedia rows the datasheet parsers already read; they arrive upper-cased at source. The
`ATTACHED UNIT` / `Attached Unit` pair is a casing duplicate that costs nothing — the app keys
the lookup on the exact name and simply never hits the unused one.

**The text changes are one defect, and the committed copies are the wrong side of it.** Every
one of the 38 text differences across the three files is a mangled inch mark: the committed
copy carries a stray backslash where a `"` belongs (`within 6\` instead of `within 6"`), from
an older CSV-quoting path since fixed. The rebuild is correct.

**One real user-visible fix, not just tidying.** `weapon_abilities.json` gains
`Icon of Despair (Aura)` and drops `Diseased Icon`. That is a source rename, not a loss:
`Diseased Icon` is referenced by nothing in any shipped file, and `units.json` already carries
`Icon of Despair (Aura)` — so that ability's glossary text has been missing from the running
app since the rename. Shipping the refreshed file restores it.

**Blast-radius check before shipping.** `weapon_abilities.json` is also the wargear allowlist
`loadout_parser.py` reads, so a changed copy could in principle move `unit_loadouts.json`.
Confirmed it does not: `repro_check.py` stays byte-identical with the refreshed file in place.

**Root cause, and the fix for the class.** The lookups were the one deployed output nothing
checked. P1 gates `unit_loadouts.json`; `units_repro_check.py` gated `units.json` — but was
never wired into `rules_assertions.py` at all, and ignored the four lookups it was already
producing in the same run. Both gaps closed:

- `units_repro_check.py` now compares all four lookups plus the taxonomy against the merged
  rebuild and reports per-file drift (added / lost / text-changed, with examples). Verified it
  fails against the stale copies and passes against the refreshed ones.
- New assertion **P4** in `rules_assertions.py` runs that gate. Suite is now 54/55 (P3 remains
  the known `pipeline_manifest.py`-absent fail).

Per D107, the reason the drift survived several sessions is exactly that "the lookups are
fresh" was only ever a prose claim.

**Verification.** `repro_check.py` byte-identical; `units_repro_check.py` byte-identical across
`units.json` and all four lookups; `rules_assertions.py` 54/55; `pool_check.js`, `e10_check.js`,
`b18d_check.js`, `required_size_check.js`, `stat_check.js`, `default_check.js`, `pts_check.js`,
`limit_check.js` all pass. `bundle_check.js` shows its same 2 pre-existing failures (B36
residual). `pts_check.js` reports its same pre-existing Terminator Assault Squad `000000118`
mismatch (B35, held for Ryan).

**B55 closed.**

---

## D165 — B31: the Wulfen Dreadnought's "A or B and C" source, resolved as a bundle rather than a schema extension (S99)

**The source.** `Datasheets_options.csv 000004133` carries two lines the loadout parser cannot
express, and both were flagged:

1. *"This model's Fenrisian greataxe or great wolf claw and storm bolter can be replaced with
   1 blizzard shield and 1 heavy flamer."* — flagged `OR_SOURCE_UNSUPPORTED`. The engine keys a
   swap source by name and has no "either of these" source, so the option was truncated to its
   first source weapon (D98 named this gap).
2. *"If this model is not equipped with a storm bolter, its heavy flamer can be replaced with
   1 storm bolter."* — flagged `UNMATCHED`. A negated gate on a weapon the unit only holds after
   taking line 1. **This second flag was live on the same unit and was never logged in the
   backlog**; B31 as written described only the first.

**The reading, settled from a sibling datasheet, not from inference.** The phrase is ambiguous
between *[greataxe or wolf claw] and [storm bolter]* (the storm bolter is always consumed) and
*[greataxe] or [wolf claw and storm bolter]* (one branch keeps it). The Space Wolves **Venerable
Dreadnought `000002801` line 3** settles it: it offers the same blizzard-shield arm and enumerates
its endpoints explicitly as *"1 Fenrisian greataxe, 1 blizzard shield and 1 storm bolter"* or
*"1 Fenrisian greataxe, 1 blizzard shield and 1 heavy flamer"*. No blizzard-shield build in the
Space Wolves range carries a heavy flamer **and** a storm bolter. The storm bolter is therefore
consumed in both branches of line 1, and line 2 is the only way to get it back. This is the D106
discipline applied — the remedy re-derived from source, not carried from the diagnosis.

**Decision: represent it as a `bundled_swaps` record, not a new schema concept.**
`OR_SOURCE_UNSUPPORTED` has **exactly one carrier in all 217 units**. A general either-of source
field would have required a `loadout_parser.py` change and an `index.html` change — two sessions
and a permanent schema concept — for a population of one. The existing D36/D113 bundle mechanism
already enumerates endpoints instead of composing swaps, which dissolves *both* problems at once:
an OR-source becomes two sibling endpoints, and a negated gate becomes no gate at all, because
"not equipped with a storm bolter" is exactly equivalent to "took line 1."

**The five endpoints** (Space Wolves / Wulfen Dreadnought / All, option group
"Wulfen Dreadnought Arms", `loadout_relation: owns`). Datasheet default is storm bolter +
Fenrisian greataxe + great wolf claw:

| endpoint | removes | adds | grants | result |
|---|---|---|---|---|
| `wulfen-base` (default) | — | — | — | storm bolter, greataxe, wolf claw |
| `wulfen-shield-flamer-keep-claw` | greataxe, storm bolter | heavy flamer | Blizzard Shield | wolf claw, shield, heavy flamer |
| `wulfen-shield-flamer-keep-axe` | wolf claw, storm bolter | heavy flamer | Blizzard Shield | greataxe, shield, heavy flamer |
| `wulfen-shield-bolter-keep-claw` | greataxe | — | Blizzard Shield | wolf claw, shield, storm bolter |
| `wulfen-shield-bolter-keep-axe` | wolf claw | — | Blizzard Shield | greataxe, shield, storm bolter |

The two `-bolter-` endpoints are line 1 followed by line 2, collapsed: net of the pair, one melee
weapon is lost and the shield is gained, with the storm bolter retained. Writing them as endpoints
rather than as a chained gate is what makes the negated gate unnecessary.

**The live bug this fixes.** Before this change the truncated `sng_1` removed only the greataxe:
picking it kept the storm bolter alongside the new heavy flamer and offered no wolf-claw
alternative — an illegal build the tool presented as legal. Asserted directly in `b31_check.js`.

**Why no engine change was needed.** An `owns` bundle already suppresses the loadout options for
the slots it manages (`bundleSuppressesLoadout` / `bundleManagedFamilies`), clears any stale pick
on them, and folds its endpoint delta into the weapon rollup display (`activeBundleWeaponDelta`) —
all shipped for the Captain in D113. The Blizzard Shield 4+ invulnerable reaches the statline
through the existing grant path: `conferredStats` skips any ability name that is a bundle grant,
and `activeStatOverrides` reads `carrier_notes` for the chosen endpoint. Identical to the
Lieutenant's storm shield. `index.html` is unchanged at v5.82.

**`_parser_flags` deliberately left in place.** Both flags remain on `000004133`. They are accurate
statements about what the parser can express; the bundle overrides at a different layer. Clearing
them would misrepresent the parser's capability and hide the gap from a future rebuild.

**Verification.** Diff-guard: exactly one unit changed (`000004133`), exactly one field
(`bundled_swaps`, `null` → the record); all 270 units and 14 blocks otherwise byte-identical, and
all four merged lookups plus `faction_taxonomy.json` byte-identical. `unit_loadouts.json` untouched;
both repro gates byte-identical. New harness `b31_check.js`, **42 assertions**, all passing, driving
the real engine sliced out of `index.html`: bundle shape, the exact legal weapon set at each
endpoint, three legality invariants held across every endpoint (never both melee weapons with the
shield, never a heavy flamer and storm bolter together, always at least one melee weapon), the
invulnerable save present on shield builds and absent on the default, and suppression of `sng_1`.
Negative control confirmed: run against the pre-fix `units.json` the harness fails 15 assertions
and exits 1, so it discriminates rather than passing vacuously.

**B31 is closed.**

---

## D166 — the 81 unpriced units are a tracked gap, not an undiscovered one (S99)

Found while confirming the Wulfen Dreadnought is addable: **81 of 270 built units carry
`points: null`** — Space Wolves 20, Black Templars 18, Dark Angels 16, Blood Angels 15,
Deathwatch 10, Adeptus Astartes 2. Every one is an SM-family chapter unit.

This is not new breakage. The mechanism was decided long ago in **D42** (chapter points = `mfm_sm.txt`
base plus a build-time-derived per-chapter override), and `MFM_Chapter_Pass.md` already contains the
completed analysis showing the five chapter MFM files close **78 of the 81** — the three stragglers
are name mismatches (Wolf Guard Headtakers, Crusader Squad, plus the vanilla-chapter cases Marneus
Calgar in Armour of Antilochus, Wardens of Ultramar, Vulkan He'stan, Kor'sarro Khan). The pipeline
simply never runs those files: `units_repro_check.py` feeds only `MFM_Space_Marines_v1_0.txt` and
`MFM_Death_Guard_v1_0.txt`.

**What was actually missing is the ticket.** D42 decided the mechanism and the analysis pass is done,
but `OPEN_ITEMS_BACKLOG.md` carried no open item for the build, so the work was invisible to session
picking. Filed as **B56**. Behaviour today is not an error state — a null-points unit renders "—" and
contributes 0 to the army total, so it is addable and configurable — but a 2,000-point list can be
built 81 units deep at zero cost, which is a real legality hole against D0. Sizeable: it touches the
per-faction build sequence, not one unit.


---

## D167 — B56 diagnosis: the chapter-points gap is four separate problems, not one (S100)

Diagnosis turn only. No pipeline, parser, data or engine file was edited. Every number below was
re-derived from current data; several supersede `MFM_Chapter_Pass.md`, which had gone stale.

### The count still holds; the closure figure does not

**81 of 270 units carry `points: null`**, unchanged: Space Wolves 20, Black Templars 18, Dark
Angels 16, Blood Angels 15, Deathwatch 10, Adeptus Astartes 2.

The five chapter MFM files close **77**, not the 78 recorded in `MFM_Chapter_Pass.md`. Two prose
facts in that document have drifted since it was written: Space Wolves' Venerable Dreadnought
`000002801` has since been costed from the base file (so the chapter file now closes 19 of 20, not
20 of 21), and all four vanilla-chapter stragglers it listed — Marneus Calgar in Armour of
Antilochus, Wardens of Ultramar, Vulkan He'stan, Kor'sarro Khan — are now costed. The Ultramarines,
Iron Hands, Salamanders, Imperial Fists, Raven Guard and White Scars blocks are at zero uncosted.

This is D107 again. A prose analysis document with no executable form drifted in both directions
inside one release, and the drift was invisible until re-derived. The refreshed figures in
`MFM_Chapter_Pass.md` will drift the same way; the durable form is a rules assertion, filed as
part of B56a.

### The four residual units are two unrelated problems

**Wolf Guard Headtakers `000004131` and Crusader Squad `000002799` are a parser gap, not a data
gap.** Both are priced in their chapter MFM. `COST_RE` requires a size-bracket line of the shape
`• N model(s) PPP pts`; these two name a composition instead — `• 3 Wolf Guard Headtakers85 pts`
and `• 1 Sword Brother, 4 Neophytes, 5 Initiates150 pts`. The parser sees no cost and drops the
entry. Prior sessions logged these as "name mismatches," which is wrong: the names match exactly.
This diagnosis was reached in passing and is exactly the class D106 warns about, so it was checked
against the raw file rather than inferred from the flag.

**Judiciar Xacharus `000004179` and Chaplain Kastiel `000004180` cannot be closed from current
sources at all.** Neither name appears in any of the 30 MFM files in the project. They are not
mismatches; the points do not exist in the data we hold. No build closes these — they need a
source.

### Black Templars is the entire scoping risk

Running the five chapter files through `mfm_points_parser.py` unscoped does not merely under-deliver;
on Black Templars it **silently corrupts the generic Space Marines roster**.

`ds_army_by_norm` prefers the `Adeptus Astartes` army whenever a unit name appears under more than
one army. That preference is correct for the base run and wrong for a chapter run. Nine of Black
Templars' eighteen datasheets share a name with an Adeptus Astartes datasheet — Gladiator Lancer,
Gladiator Reaper, Gladiator Valiant, Impulsor, Land Raider Crusader, Repulsor, Repulsor Executioner,
Sternguard Veteran Squad, Terminator Squad. Unscoped, all nine rows are written under
`Adeptus Astartes`, overwriting the generic base price on join, while Black Templars stays uncosted.
Only 8 of 18 BT datasheets land correctly. The other four chapters misfile **zero** — Space Wolves
20/21, Blood Angels 15/15, Dark Angels 16/16, Deathwatch 10/10 all arm correctly.

The fix is an explicit scope, not a heuristic: when a chapter file is parsed, restrict the
name→army map to that chapter's own rows in `Unit_Stats.csv` and drop any MFM entry with no
datasheet in that block. That also disposes of the 4–22 orphan rows per chapter (MFM entries with
no datasheet anywhere in the SM set), which would otherwise be written under the fallback army.

### The chapter runs have no side effect on leader lists

Worth stating because it bounds the turn: `mfm_points_parser.py` also backfills `Leader Eligible
Units` in `Unit_Stats.csv` from the MFM `SUPPORT` blocks, non-destructively. Measured across all
five chapter runs against the post-SM stats file: **0 cells patched**, because the transform has
already filled every one from `Datasheets_leader.csv`. B56a is therefore points-only, and the
diff-guard can assert that nothing but `points` changes.

### D42's override direction is confirmed, and the population is smaller than assumed

D42 holds as written. Two refinements from the measurement:

**Black Templars' apparent overrides are not overrides.** Its three price disagreements with base
(Impulsor 80→85, Repulsor Executioner 240/260→245/265, Sternguard Veteran Squad 100/190→85/160) are
all on datasheets Black Templars owns natively — `000002786`, `000002790`, `000004137` are in the BT
block with their own IDs. They price from the BT file directly and need no override layer. D42
predicted exactly this.

**The real override population is 11 rows across four chapters:** Blood Angels 8 (Assault
Intercessor Squad 75→80, Assault Intercessors with Jump Packs, Bladeguard Veteran Squad, Captain
with Jump Pack 75→80, Chaplain with Jump Pack 75→80, Outrider Squad 70→75, Repulsor Executioner,
Vanguard Veteran Squad with Jump Packs), Space Wolves 1, Dark Angels 1, Deathwatch 1.

**Four of those 11 are the same unit.** Repulsor Executioner is priced 230/250 by Space Wolves,
Blood Angels, Dark Angels and Deathwatch alike, against a base of 240/260 in
`MFM_Space_Marines_v1_0.txt`. Four independent chapter files agreeing against the base is more
consistent with a stale base entry than with four separate deliberate re-prices. Nothing in the
source resolves it — none of the files carry a version or date, and all are labelled v1_0. Held for
Ryan; see the open decision below. D42's mechanism is correct either way, so it is not a blocker.

**The override needs an engine change and cannot be a data row.** Every overridden unit lives in the
`Adeptus Astartes` block only; `resolveUnits` in `index.html` unions that block into the chapter
view at selection time. There is no Blood Angels row to attach 80 to. The override must ship as a
field on the generic unit and be applied when a chapter is active. The good news is the hook is a
single function — `resolveUnits` already handles the harder case (a chapter datasheet shadowing a
same-named generic one, which is what makes Black Templars render correctly today).

### The split

Turn-typing forces at least one boundary, and the diagnosis adds three more:

- **B56a — data.** Scope flag on `mfm_points_parser.py`; run the five chapter files; extend
  `units_repro_check.py` so the new inputs sit inside the fixed point; assertion replacing the prose
  closure figures. Closes 77 of 81.
- **B56b — data.** Teach `COST_RE` the composition-line shape. Closes 2 more. Deliberately separate
  from B56a: it changes a regex every faction's parse runs through, so it needs its own diff-guard
  proving zero change outside the two targets.
- **B56c — data.** Derive the 11-row per-chapter override map each build and emit it into
  `units.json`.
- **B56d — engine.** Apply the override at `resolveUnits`.
- **B56e — blocked, not a build.** Judiciar Xacharus and Chaplain Kastiel; needs a points source.

B56a is the whole legality hole minus four units and depends on nothing. It goes first.

### Baseline at diagnosis

`index.html` v5.82, `unit_loadouts.json` 217/338 byte-identical, `units.json` 270/14 byte-identical
with all four lookups and the taxonomy, `rules_assertions.py` 54/55 (P3 known-fail),
`pool_check.js`/`e10_check.js`/`b18d_check.js`/`required_size_check.js`/`b31_check.js`/`stat_check.js`/
`default_check.js`/`pts_check.js`/`limit_check.js` all pass, `bundle_check.js` at its 2 documented
B36 residual failures.

## D171 — B56c shipped: chapter points override map derived fresh each build, stamped onto the generic units (S103)

**Custody note first.** This copy of the decision log jumps from D167 straight to this entry —
D168, D169, D170 (all referenced by name in S101/S102 handoffs) are not present in the synced
project copy. Same class of gap as the missing `pipeline_manifest.py` (D123). Flagged, not
reconstructed; the content that matters (D169's mechanical rule — chapter points always win) is
restated below from the S102 handoff prose rather than assumed.

### What shipped

New pipeline step `add_chapter_point_overrides.py`, wired into `units_repro_check.py` as the
final stage of the SM build chain (after `add_bodyguard_stat_flags.py`). Re-parses each of the
five chapter MFM files directly with `mfm_points_parser.py`'s own `parse_mfm()`/`to_points_row()`
— no reimplementation of the bracket/tier grammar — and recomputes the override set from source
every run, per the ticket's "never hand-maintain" instruction.

**Method:** for each chapter file, a costed unit is an override candidate only if (a) it is NOT a
chapter-owned datasheet (checked against that chapter's own `Unit_Stats.csv` rows — the same
scope rule B56a already enforces) and (b) a generic Adeptus Astartes price exists to compare
against. Candidates whose chapter price matches the generic price are dropped; only genuine
disagreements are written. This mirrors exactly what B56a's `--scope-to-army` already drops
silently — B56c recovers those dropped rows instead of discarding them.

### Re-derived population matches D167/D169 exactly

11 override rows across 4 chapters: Blood Angels 8, Space Wolves 1, Dark Angels 1, Deathwatch 1.
Repulsor Executioner confirmed 230/250 for all four chapters (SW/BA/DA/DW) against a generic base
of 240/260 — D169's resolution ("chapter points always win") applies mechanically with no
per-unit call needed.

**Row count vs. unit count.** The ticket's verification bar says "11 units.json entries gain the
override field." That is the row count, not the unit count. Because Repulsor Executioner is
overridden by four different chapters at once, it is ONE unit carrying four chapter keys in a
nested object — so the actual diff is **8 unit_ids**, not 11. Re-confirmed against the diff-guard
below; the discrepancy is a description imprecision in the ticket, not a data problem. Flagging
it here rather than silently reconciling it, per D106.

The 8 units: Repulsor Executioner (`000002722`, 4 chapters), Assault Intercessor Squad
(`000001606`), Assault Intercessors With Jump Packs (`000002776`), Bladeguard Veteran Squad
(`000000071`), Captain With Jump Pack (`000000083`), Chaplain With Jump Pack (`000000112`),
Outrider Squad (`000002712`), Vanguard Veteran Squad With Jump Packs (`000000147`) — all eight
in Blood Angels except Repulsor Executioner, which additionally carries Space Wolves, Dark
Angels and Deathwatch keys.

### Field shape

`chapter_point_overrides` on the generic unit: a dict keyed by chapter army name, each value
shaped identically to the existing `points.sizes` field (`{"sizes": [{"size", "first_unit",
"second_unit", "third_plus"}, ...]}`). Chosen so B56d can swap it in with no reshaping — just
`unit.points = unit.chapter_point_overrides[activeArmy] || unit.points` at `resolveUnits`. Field
is only ever present on the 8 units that actually have an override; not defaulted onto the other
262 (unlike `bodyguard_stat_flags`, which defaults empty everywhere — B56c's diff-guard requires
the field to appear on exactly the affected units, so no blanket default here).

### Verification

- Diff-guard: exactly 8 `unit_id`s changed between committed and rebuilt `units.json`, every one
  in the Adeptus Astartes block, every changed unit gained `chapter_point_overrides` and nothing
  else.
- `units_repro_check.py` reproduces the new committed `units.json` and all four merged lookups
  byte-for-byte with `add_chapter_point_overrides.py` as part of the fixed point.
- `repro_check.py` (unit_loadouts.json), `rules_assertions.py` (56/57, P3 known-fail unchanged),
  `pts_check.js`, `stat_check.js`, `limit_check.js`, `bundle_check.js` (2 known B36 failures) all
  re-run clean, unchanged from S102 close.

### What's explicitly not done

B56d (apply the override at `resolveUnits`) is untouched per the ticket's instruction — B56c
closes on its own, data verified in isolation, before any engine wiring. `chapter_point_overrides`
currently has no reader; it sits inert in `units.json` until B56d ships.

### Baseline at close

`index.html` v5.82 (unchanged). `unit_loadouts.json` 217/338 byte-identical (unchanged).
`units.json` 270/14, 8 units gained `chapter_point_overrides`, `units_repro_check.py` byte-
identical with the new pipeline step included. `rules_assertions.py` 56/57 (P3 known-fail,
`pipeline_manifest.py` still absent from sync). Harness suite unchanged from S102 close.

---

## D172 — B56d shipped: chapter point overrides applied at resolveUnits (S104)

**What shipped.** `index.html` v5.83. New helper `applyChapterPointOverrides(units, armyName)`,
called from `resolveUnits` right after the generic/chapter union is built. For each unit in the
resolved set that carries `chapter_point_overrides[armyName]`, the helper substitutes that value
for `unit.points` and returns a fresh object — the original unit object in `unitsByArmy` is never
touched. Units with no override for the active army pass through unchanged (same object
reference).

**Why a fresh object, not an in-place edit.** The generic Adeptus Astartes unit objects are held
once in `unitsByArmy['Adeptus Astartes']` and referenced — not copied — into every chapter's
resolved set. Writing `unit.points = override` directly would mutate that single shared object,
so the first chapter to resolve it would silently overwrite the price for every other chapter
(and the generic view) sharing the same object. `Object.assign({}, u, {points: override})` keeps
the substitution scoped to the array `resolveUnits` returns for that one call.

**Coverage confirmed on both call sites.** `setFaction` is the only caller of `resolveUnits`, and
both list creation (`confirmCreateList`) and list opening (`openList`) call `setFaction` before
anything downstream reads unit prices — so re-hydrating a saved list recomputes the chapter-scoped
price fresh each time rather than freezing it at save time, with no separate wiring needed.

**Verification.** New harness `b56d_check.js`: Repulsor Executioner reads 230/250 under Space
Wolves, Blood Angels, Dark Angels, and Deathwatch, and 240/260 under Ultramarines (a chapter with
no override) and the generic Adeptus Astartes view; Assault Intercessor Squad reads 80 under
Blood Angels and stays 75 under Dark Angels (no cross-chapter leak); the shared `unitsByArmy`
object for both units is confirmed unchanged after a Blood Angels resolve (no in-place mutation).
Full harness suite (`pool_check.js`, `e10_check.js`, `b18d_check.js`, `required_size_check.js`,
`b31_check.js`, `stat_check.js`, `default_check.js`, `pts_check.js`, `limit_check.js`) re-run
clean against the new `index.html`, unchanged from S103 close. `bundle_check.js` unchanged (2
known B36 failures). `rules_assertions.py` unchanged (56/57, P3 known-fail, `pipeline_manifest.py`
still absent from sync).

**Scope.** Diff against the committed `index.html` is exactly the version bump and the one
additive block described above — nothing else moved. `unit_loadouts.json` and `units.json`
untouched; this is an engine-only turn per the ticket's turn-typing rule.

### Baseline at close

`index.html` **v5.83**. `unit_loadouts.json` 217/338 byte-identical (unchanged).
`units.json` 270/14 byte-identical (unchanged). `rules_assertions.py` 56/57 (P3 known-fail,
unchanged). Harness suite unchanged from S103 close plus new `b56d_check.js` (all pass).

## D173 — B56g analysis: the Hunting Wolves escort is a model group, not wargear — direction (b) rejected (S105)

**Turn type.** Analysis only. No parser, data, or engine file changed this session. The ticket's
own instruction was to evaluate direction (b) against the real data before building, and (b) does
not survive that evaluation.

**What the source actually says.** Wahapedia datasheet `000004131`. Unit composition is two
independent ranges — `3-6 Wolf Guard Headtakers` and `0-6 Hunting Wolves`. A Hunting Wolf is a
**model with its own statline row** in `Datasheets_models.csv` (line 2: M 10", T 4, Sv 6+, W 1,
Ld 8+, OC 0, 60 x 35.5mm base), its own weapon (`Teeth and claws`), and its own keyword set
(`BEASTS, IMPERIUM, HUNTING WOLVES`). Two datasheet abilities depend on the wolves being models:
*Let Loose the Wolves* splits the unit into a HEADTAKERS unit and a HUNTING WOLVES unit at Declare
Battle Formations, and *Hunting Hounds* changes the OC of HUNTING WOLVES models specifically.

**Points source disagreement, resolved in MFM's favour.** `Datasheets_models_cost.csv` prices the
escorted brackets at 110 / 220; `MFM_Space_Wolves_v1_0.txt` prices them at 115 / 230 (and 125 /
240 at the 3rd+ tier). MFM is the points authority by design, so 115 / 230 / 125 / 240 stand and
the Wahapedia cost table is stale here. Noted because it rules the Wahapedia table out as a
cross-check on this unit, not because any action follows.

**Why direction (b) is wrong.** Routing the escort through `WARGEAR_RE` / `wargear_points.json`
fails on three counts, any one of which is disqualifying:

1. **Nothing to parse.** `WARGEAR_RE` only matches a `• per <item> N pts` line under a
   `WARGEAR OPTIONS` header. Wolf Guard Headtakers has no such line — the escort price exists only
   as the difference between two bracket totals. Using (b) would mean hand-authoring a price into
   the wargear map rather than deriving one from source, against the project's standing rule.
2. **Category error.** `wargear_points.json` entries are validated by `reachable_items()`, which
   scans `default_weapons`, `default_wargear`, and option replacement/choice lists in
   `unit_loadouts.json`. "Hunting Wolf" is not any of those. Making it reachable would mean
   declaring a model to be an item.
3. **Wrong output.** Under (b) a 6-model unit would render as 3 models with a 30-point item
   attached: no second statline, wrong model count, wrong starting strength, OC 0 group missing,
   and both wolf-dependent abilities with nothing to act on. That is a fidelity regression, not a
   pricing shortcut.

**Why direction (a) is also wrong as stated.** Widening `Unit_Points.csv` with an addon-cost column
treats the escort as a price modifier when the collision is not about price at all. There are four
printed configurations (3 / 3+3 / 6 / 6+6) and `to_points_row` keys brackets by **total model
count**, which makes 3+3 and 6+0 both `size = 6`. That is the collision `parse_mfm` already detects
and voids (D170's staging logic, working as designed). An addon column does not remove the
duplicate key; it only pays for it.

**The correct shape.** The escort is an **optional model group** — machinery that already exists.
`loGroupCounts` in `index.html` already resolves `count.optional` groups (B13, D158/D159) as a
player toggle, and `count.per_bracket` already varies a group's count by bracket (D62). Two gaps
separate that from what this unit needs: `optional` is hard-coded to 0-or-1 rather than 0-or-N, and
no model group carries a price. Modelled this way the unit keeps two brackets keyed on the
**Headtaker count** (3 and 6 — no collision, fits `Size_1..3` unchanged), and the escort's cost is
re-derived by the parser as the printed difference: 115−85 = 30 over 3 wolves and 230−170 = 60 over
6, i.e. **10 pts per wolf**, confirmed identical at the 3rd+ tier (125−95 = 30, 240−180 = 60). All
four printed totals reproduce exactly at both tiers, with no invented price.

**Scope of the collision — genuinely one unit.** `COMPOSITION_RE` was run across all 26 MFM files.
Exactly one unit produces a same-size cost collision: Wolf Guard Headtakers. The only other
multi-group bracket lines anywhere are Black Templars Crusader Squad (10 and 20 — distinct totals,
already parsing correctly). So this is a one-off today, which argues against widening a shared
schema and in favour of generalising the model-group mechanism that other units will eventually
reuse.

**Why this did not ship.** The correct shape spans a parser change (derive the escort price), a
data change (emit the second model group), and an engine change (0-or-N optional groups, plus
model-group pricing in the points math). Engine and data changes never share a turn, so this is at
minimum three sequential turns — deeper than the "medium, self-contained data/schema turn" the
ticket was scoped as. Banked with a phased plan rather than half-built.

**Blocked on one legality call.** See B56g in the backlog: whether the wolf count is free across
0-6 or locked to 0-or-N. This sets what the tool treats as legal and every phase below depends on
it, so it goes to Ryan rather than being decided in passing. Recommendation on record: locked
0-or-N.

**Separately surfaced — B57.** Every unit composition in the data allows in-between sizes (Blood
Claws `9-19` + leader, Intercessors `4-9` + sergeant), and the MFM instructions explicitly permit
them: a unit may contain a number of models between the printed limits and pays the higher printed
cost. The app offers only the printed bracket edges everywhere. That is systematically
under-permissive against a rule the source states plainly. Consistent, longstanding, and not this
ticket — filed as B57 rather than changed here. It is also the reason the 0-or-N recommendation
above is *consistent* with existing behaviour rather than a new restriction.

### Baseline at close

Unchanged from S104. `index.html` **v5.83**. `unit_loadouts.json` 217/338 byte-identical.
`units.json` 270/14 byte-identical. `rules_assertions.py` 56/57 (P3 known-fail,
`pipeline_manifest.py` still absent from sync). Full harness suite passes. `bundle_check.js` 2
known B36 failures.

## D174 — B56g phase 1 shipped: escort resolver keys the primary bracket on the primary count, Wolf Guard Headtakers closes (S106)

**Ryan's call, confirmed against the printed MFM table.** Read directly off
`MFM_Space_Wolves_v1_0.txt`: exactly four configurations are priced — 3 Headtakers alone, 3
Headtakers + 3 Hunting Wolves, 6 Headtakers alone, 6 Headtakers + 6 Hunting Wolves. No in-between
or mismatched count is printed anywhere. This confirms the S105 recommendation: the wolf count is
locked to 0-or-N, matching the Headtaker bracket. B56g unblocked.

**The fix.** `mfm_points_parser.py`'s composition resolver used to key every bracket by the sum of
all groups in the line, so "3 Headtakers + 3 Wolves" (sum 6) collided with "6 Headtakers" (sum 6)
at two different prices, and D106's collision guard correctly voided the whole unit rather than
guess. The resolver now parses each composition line into its individual (count, label) groups and
asks a narrower question: does a multi-group line's FIRST group exactly match (count and label) an
existing single-group line in the same tier? If so, that line is an **escort** line — its primary
bracket already exists standalone, and the escort's cost is the printed difference. If not, the
line is left on the original sum-of-groups path untouched.

This discriminator was chosen over "any multi-group line" specifically because Crusader Squad
(Black Templars) is also a multi-group composition ("1 Sword Brother, 4 Neophytes, 5 Initiates" /
"1 Sword Brother, 8 Neophytes, 11 Initiates") but never appears as a standalone single-group line —
every printed line for that unit has all three roles scaling together, so it correctly falls
through to the unchanged sum-based path. Verified directly: Crusader Squad's parsed tiers
(`{10: 150, 20: 290}`) are byte-for-byte what they were before this change.

**Escort rate, re-derived, not hand-entered.** 115−85 = 30 over 3 wolves and 230−170 = 60 over 6 →
10 pts/wolf; 125−95 = 30 and 240−180 = 60 at the 3rd+ tier → 10 pts/wolf again. Both tiers agree.
The resolver only accepts the derived rate if every escort line for the unit agrees (evenly
divisible, same value) — a disagreement voids and flags rather than picks a winner, same discipline
as the existing collision guard.

**Wolf Guard Headtakers now prices at 85/170 (1st–2nd) and 95/180 (3rd+)** for the two Headtaker-only
brackets — the primary bracket table the escort sits alongside. The escort itself (Hunting Wolves as
a purchasable 0-or-N group) is **not** wired into `unit_loadouts.json` or the engine this session —
that is phases 2 and 3, per D173's phased plan. The Hunting Wolves model group already existed in
`unit_loadouts.json` (from the datasheet parse itself, `count.optional`/`max:6`, hard-coded 0-or-1
per B13) — this session did not touch it and it still carries no price.

**Rebuild and diff-guard.** Full SM/DG/CD pipeline rerun end to end
(`wahapedia_transform.py` → `mfm_points_parser.py` [+ 5 chapter overlays] → `convert_to_json.py` →
`merge_factions.py` → `add_loadout_groups.py` → `add_co_leader.py` → `add_bodyguard_stat_flags.py`
→ `add_chapter_point_overrides.py`), then diffed unit-by-unit against the previously committed
`units.json`. Exactly one `unit_id` changed: `000004131` (Wolf Guard Headtakers, null → priced). No
other unit's points moved, including Crusader Squad. `units_repro_check.py` now reproduces the new
`units.json` byte-identical from source.

**Note for the record.** Mid-session, an early rebuild script mistakenly copied the SM-scoped
`Unit_Points.csv` (a temp-dir pipeline artifact) over the project root's `Unit_Points.csv`, which is
the hand-built Chaos Daemons source file, not an SM output. Caught immediately by a failing
`units_repro_check.py` (Chaos Daemons units_ids showing up as "changed"), restored from source before
anything shipped. No corrupted file was delivered. Noted here because it's exactly the kind of
mistake the fixed-point discipline exists to catch, and it worked.

**Rules assertions.** `B56b-1` updated: residual null-points set drops from 3 to 2
(`000004179`/`000004180`, both B56e — still blocked on a source). New `B56g-1` checks the two
Headtaker-only brackets price correctly, the escort rate re-derives to exactly 10 pts/model at both
tiers directly from source (not hand-entered into the assertion), and that the escort is not yet
reachable as a priced group anywhere (`unit_loadouts.json` model group carries no price;
`wargear_points.json` has no Hunting-Wolves-shaped entry) — a passing check here would mean scope
crept past the parser turn. Suite: 57/58 (P3 known-fail, unchanged).

### Baseline at close

`index.html` **v5.83** — unchanged, no engine edit this session. `unit_loadouts.json` 217/338
byte-identical — unchanged. `units.json` 270/14, exactly one `unit_id` changed (`000004131`) vs.
S105 close; `units_repro_check.py` reproduces the new file byte-identical. `rules_assertions.py`
57/58 (P3 known-fail). Full harness suite passes, including the new `B56g-1`. `bundle_check.js` 2
known B36 failures, unchanged.

## D175 — B56g phase 2 shipped: Hunting Wolves gains a per-bracket count and a price; new schema field, new HAND_AUTHORED entry (S107)

**Turn type.** Data turn, as scoped. No `index.html` edit — the group stays inert (correct data,
no way to select it yet) until phase 3's engine work, same pattern as B56c → B56d.

**The change.** `unit_loadouts.json`'s Wolf Guard Headtakers (`000004131`) Hunting Wolves model
group moves off the flat `optional`/`max:6` shape (hard-coded 0-or-1 per B13) onto
`optional`/`per_bracket` — 3 wolves at the 3-Headtaker bracket, 6 at the 6-Headtaker bracket — per
D174's confirmed 0-or-N answer. A new `price_per_model: 10` field is added to the group, carrying
the escort rate D174 already derived from the printed MFM totals (never hand-entered here — it's
the same number D174 verified agreed at both copy-tiers).

**New schema field.** `price_per_model` did not previously exist anywhere in `unit_loadouts.json`.
Existing per-model or per-swap pricing lives in `wargear_points.json`, keyed by item name — but the
Hunting Wolves escort is a model count, not a wargear swap, so it doesn't fit that file's shape
(confirmed by D173's rejection of routing it through `WARGEAR_RE`/`wargear_points.json`). The field
sits as a sibling of `count` on the model group, holding the per-model rate; phase 3's engine work
is what turns it into actual points math.

**`repro_check.py` HAND_AUTHORED gains a third entry.** The per-bracket linkage — 3 wolves tied to
the 3-Headtaker bracket, 6 to the 6-Headtaker bracket — comes from cross-referencing the MFM price
table (D174), which `repro_check.py`'s pipeline never reads for `unit_loadouts.json` (that pipeline
sees only `Datasheets_options.csv`, the composition/cost CSVs, and the web.txt files — not any MFM
file). `loadout_parser.py`'s generic composition parser only ever sees Wahapedia's single
undifferentiated `0-6 Hunting Wolves` composition line and has no way to know it should split by the
Headtaker bracket. This is the same class of problem the two existing hand-authored entries exist
for, so `000004131` was added to `HAND_AUTHORED` in `repro_check.py` rather than hand-editing a
parser-owned output file out from under the fixed-point discipline. The committed file's key order
was also adjusted — `000004131` now sits third (right after the two existing hand-authored entries),
matching exactly where the parser's `out.update(existing)` seed-preservation step places it; this
was required for byte-identical reproduction, not a style choice.

**Verified.**
- `repro_check.py`: byte-identical reproduction confirmed with the updated `HAND_AUTHORED` list and
  reordered file.
- Diff-guard: exactly one `unit_id` changed (`000004131`) vs. S106 close; total entry count
  unchanged (217 units + `_schema`).
- Full harness suite (`pool_check.js`, `e10_check.js`, `b18d_check.js`, `required_size_check.js`,
  `b31_check.js`, `stat_check.js`, `default_check.js`, `pts_check.js`, `limit_check.js`,
  `b56d_check.js`): all pass. `pts_check.js`'s one "default cost moves" line is the pre-existing
  Terminator Assault Squad case (B35), confirmed unrelated.
- `bundle_check.js`: still exactly the 2 known B36 failures, unchanged.
- `rules_assertions.py`: 57/58 (P3 known-fail, `pipeline_manifest.py` still absent from sync,
  unchanged). No new assertion added this session — `B56g-1` (from D174) already guards that the
  escort is not yet reachable as a priced group anywhere reachable by the engine; that guard now
  needs updating in phase 3, once the engine can actually reach it, not before.

**Not done this session — phase 3, per D173's plan.** `index.html` untouched. `loGroupCounts` still
does not accept 0-or-N optional groups (hard-coded 0-or-1). The points engine does not yet add
model-group cost. The config panel has no toggle for this group. The Hunting Wolves escort remains
unbuildable in the app until phase 3 ships.

### Baseline at close

`index.html` **v5.83** — unchanged. `unit_loadouts.json` 217/338, exactly one `unit_id` changed
(`000004131`) vs. S106 close; `repro_check.py` reproduces the new file byte-identical (with the
updated `HAND_AUTHORED` list). `units.json` 270/14 — unchanged. `rules_assertions.py` 57/58 (P3
known-fail). Full harness suite passes. `bundle_check.js` 2 known B36 failures, unchanged.

## D176 — B56g phase 3 shipped: Hunting Wolves escort is reachable as a 0-or-N toggle; B56g closes (S108)

**Turn type.** Engine turn, as scoped. No data files touched — `unit_loadouts.json` and `units.json`
both reproduce byte-identical from source, confirming this session changed only `index.html`.

**The change, three pieces in `index.html` (v5.83 → v5.84).**
1. `loGroupCounts` gains a branch for `count.optional && count.per_bracket` (checked before the
   plain `per_bracket` branch): off resolves to 0, on resolves to the bracket's printed count (3 or
   6) — the 0-or-N toggle D174 confirmed, replacing the old hard-coded 0-or-1 that this group would
   otherwise have fallen into (per_bracket alone would have made it always-on at full count with no
   toggle at all).
2. New `modelGroupCost(def, size, optCounts)` sums `price_per_model × count` across any model group
   carrying that field, and is now added into both `wargearCostForEntry` (live entries) and
   `defaultWargearCost` (roster "from" badge) — independent of `wargearPoints`, so it still applies
   to a unit with no other priced wargear.
3. The config panel's existing B13 optional-group toggle block (generic, unchanged in shape) already
   picked up Hunting Wolves automatically since the group carries `count.optional`; the label was
   extended to show the model count and points on a per_bracket group (`Add 3 (+30 pts)` /
   `Add 6 (+60 pts)`) so the toggle doesn't read as a single-model add.

**Bug caught and fixed before shipping.** The first pass let the escort's reserved count subtract
from the Headtaker `fills_to_size` group's remainder — toggling the escort on at the 3-model bracket
was producing 0 Headtakers + 3 Wolves instead of 3 Headtakers + 3 Wolves. The printed MFM table
settles this: all four configurations keep the Headtaker count at exactly the bracket size whether
or not the escort is taken, so the escort must not reserve against the same pool the Headtaker group
fills from. Fixed by excluding the optional+per_bracket branch from `reserved` entirely — it resolves
its own count but contributes nothing to what other groups see as taken. Caught by the new harness
before it reached a rules-assertion or a saved list.

**Rules assertions.** `B56g-1` rewritten: the phase-1/2 guard asserting the escort was *not yet*
reachable is replaced with a phase-3 guard asserting it *is* reachable — checks the group's
`price_per_model`/`per_bracket` shape directly, confirms `wargear_points.json` still carries no
Hunting-Wolves-shaped entry (direction (b) stays rejected per D173), and checks `index.html`'s source
for the new branch and cost function so the guard can't silently go stale if the engine logic is
later reverted. Suite: 57/58 (P3 known-fail, `pipeline_manifest.py` still absent from sync,
unchanged).

**New harness `b56g_check.js`.** Extracts `loGroupCounts`/`modelGroupCost` straight out of
`index.html` (same pattern as `b56d_check.js`) and checks all four printed configurations at both
copy-tiers — 3 Headtakers alone, 3+3, 6 alone, 6+6 — on both model count and added points, plus the
default (no toggle set) case. 10/10 pass.

**B56g closes.** All three phases shipped across S106–S108. Hunting Wolves is now a fully buildable,
correctly priced escort in the app.

### Baseline at close

`index.html` **v5.84** — `loGroupCounts`, `modelGroupCost`, config panel label updated.
`unit_loadouts.json` 217/338 byte-identical — unchanged, `repro_check.py` confirms. `units.json`
270/14 byte-identical — unchanged, `units_repro_check.py` confirms. `rules_assertions.py` 57/58 (P3
known-fail, unchanged). Full harness suite passes, including the new `b56g_check.js` (10/10).
`bundle_check.js` 2 known B36 failures, unchanged.

## D177 — B11 shipped: SV/LD normalized to bare values at the pipeline source (S109)

**Turn type.** Data turn, as scoped. `wahapedia_transform.py` is the only script touched; no engine
change.

**The problem.** `Datasheets_models.csv` carries `Sv` and `Ld` with a trailing `+` (e.g. `3+`, `6+`)
while `inv_sv` and FNP are bare numbers. `wahapedia_transform.py` copied SV/LD through unchanged, so
the inconsistency reached `Unit_Stats.csv` and then `units.json`. `index.html`'s `buildStatTable`
already carried a render guard (`cleanPlus`, v5.35) that strips a trailing `+` before appending its
own `+` suffix — so the display was never wrong, but the stored representation was a trap: any future
reader of raw `mg.SV`/`mg.LD` that didn't route through the guard would silently double up a `++` or
mis-parse the value as a string when a numeric compare was expected.

**The fix.** Two lines in `wahapedia_transform.py`, at the point `sv`/`ld` are pulled off the model
row: strip a trailing `+` if present, before the value is written to `Unit_Stats.csv`. `to_int` in
`convert_to_json.py` then successfully parses the now-bare value as an integer where earlier it fell
back to a string with a trailing `+` — this is why 450 `SV`/`LD` values in `units.json` moved from
string (`"3+"`) to integer (`3`) even though nothing about what's displayed changed.

**Diff-guard.** Full pipeline rebuild via `units_repro_check.py`'s own `repro()`, with the rebuilt
`units.json` diffed against the previously-committed one at the JSON level: every field outside
`model_groups[].SV` / `model_groups[].LD` matched exactly across all 270 units; the only differences
were the 450 SV/LD values moving from a `"N+"` string to a bare `N` (string or int) with the same
numeric value — zero exceptions. `stat_check.js` and the full harness suite re-run clean against the
new `units.json`. `index.html`'s `cleanPlus` guard is now provably a no-op for SV/LD (it still runs,
still safe to leave — nothing else depends on a trailing `+` surviving to render time — but there's
nothing left for it to strip).

**B11 closes.**

### Baseline at close

`index.html` **v5.84** — unchanged this session. `unit_loadouts.json` 217/338 byte-identical —
unchanged, `repro_check.py` confirms. `units.json` 270/14 — regenerated; 450 SV/LD values across the
file moved from `"N+"` string to bare `N`, no other field changed; `units_repro_check.py` reproduces
the new file byte-identical. `rules_assertions.py` 57/58 (P3 known-fail, `pipeline_manifest.py` still
absent from sync, unchanged). Full harness suite passes. `bundle_check.js` 2 known B36 failures,
unchanged.


## D178 — B54 shipped: Be'Lakor's Shadow Form sub-abilities added to CD data (S110)

**Turn type.** Data turn — Chaos Daemons is Gen-1 hand-built data, never routed through
`wahapedia_transform.py` (D132), so this touched only the root `Unit_Stats.csv` and
`Unit_Ability_Details.csv`. No engine file changed.

**What shipped.** Three new `Unit_Ability_Details.csv` rows for `local:chaos-daemons:be-lakor` —
Wreathed in Shadows, Pall of Despair, Shadow Lord — text sourced from `chaos_daemons_reference.md`
(already confirmed matching Wahapedia wording). `Unit_Stats.csv`'s Be'lakor row gained the three
matching names in its Unit Ability Names field, so they render as their own rows in the Abilities
section via the existing generic display mechanism (same as Dark Master / Shadow Form already did) —
no display code changed.

**Naming correction found mid-build.** The three sub-abilities are tagged (Aura, Psychic) per the
source text. `convert_to_json.py`'s `split_list()` does a plain comma split with no quote-awareness,
so a name written as "Wreathed in Shadows (Aura, Psychic)" in the Unit Ability Names field breaks
into two garbage list entries at rebuild. Existing CD data (Poxbringer's "Feculent Despair (Aura
Psychic)") already established the workaround: drop the internal comma in the tag suffix. Followed
the same convention for all three new names, and used the same no-comma form as the
`Unit_Ability_Details.csv` key so the lookup matches. Worth noting as a standing rule: any
Aura+Psychic (or similar multi-tag) ability name added to a Unit Ability Names field must drop the
comma between tags.

**Diff-guard.** Full pipeline rebuild (`units_repro_check.py`'s own `repro()` logic run against the
edited CSVs): byte-identical to the freshly rebuilt `units.json` at the pipeline-output level.
JSON-level unit diff confirms only `local:chaos-daemons:be-lakor` changed — all 269 other units
untouched. `rules_assertions.py` 57/58 (P3 known-fail, unchanged). Full harness suite passes.
`bundle_check.js` 2 known B36 failures, unchanged.


## D179 — B21 diagnosis: the real blocker is banded optional model groups, not the mis-scoped options (S111)

**Turn type.** Diagnosis/scoping only. No engine, parser, or data file changed.

**What B21 said.** Several Deathwatch kill-team options are scoped to the base (fills-to-size)
model group even though the weapon they replace is carried only by an *optional variant* group,
so the option can never fire. Banked behind "optional-group pricing/selection work".

**What the scan actually found — the option list is bigger, and simpler, than the entry says.**
Four affected options on three units, not three on two:

* Fortis Kill Team `000002780` `cnt_4` — plasma pistol swap, gated `requires_weapon: Plasma
  incinerator`; only the "with plasma incinerators" group carries it.
* Fortis Kill Team `000002780` `cnt_5` — vengor launcher replaces a superfrag rocket launcher;
  only the "with superfrag rocket launchers" group carries one.
* Spectrus Kill Team `000002779` `cnt_4` — instigator bolt carbine replaces a bolt sniper rifle;
  only the "with bolt sniper rifles" group carries one.
* Indomitor Kill Team `000002781` `cnt_2` — multi-melta replaces a melta rifle; only the "with
  melta rifles" group carries one. **Not previously listed in B21.** (B18d's S82 no-op note for
  `000002781` was about its *per-5* line, which is correctly scoped; `cnt_2` is a different line
  and is mis-scoped.)

In every one of the four cases the source weapon lives in **exactly one** model group. That is the
useful finding: B21 needs no shared pool cap and no B18c/B18d-style fan. Each fix is a one-line
re-scope from the base group to the single carrying group, keeping `max_total: 1` as authored.
The B18c/B18e pooled-cap machinery is not needed here and should not be reached for.

**Why B21 still cannot ship as a data turn.** The re-scoped options would land on groups that can
never hold more than one model, and today usually hold zero. `loGroupCounts` treats every
`count.optional` group as a **0-or-1 toggle** (`c[g.name] = oc[g.name] || 0`, seeded 1 by the B13
toggle). The `max` field the parser already writes on these groups is read by nothing in the
engine. Confirmed by running `loGroupCounts` at size 10 with every optional group switched on:
Fortis resolves to 1/5/1/1/1/1 when the datasheet composition allows up to 0-4 / 0-4 / 0-4 / 0-2.

So the real defect is upstream of B21 and is a live under-permit in its own right, not just a
banked gap: **four Deathwatch kill teams cannot be built legally today.** Their composition is a
banded model mix inside a fixed 10-model unit, and the engine can only give one model per band.

**The four affected units and their bands** (all fixed at a single 10-model bracket, all flat-priced
per unit, so no per-model pricing is involved):

* `000002780` Fortis — 1 Sergeant, 2-9 base, 0-4 / 0-4 / 0-4 / 0-2 variants.
* `000002779` Spectrus — 3-10 base, 0-3 / 0-4 / 0-4 variants.
* `000002781` Indomitor — 3-10 base, 0-3 / 0-3 variants.
* `000003874` Talonstrike — 1 Sergeant, 2-9 base, 0-5 variant.

Note the base group carries its own **minimum** (2-9, 3-10), which `fills_to_size` does not record
at all. The binding constraint is therefore: sum of variant picks ≤ size − fixed − base minimum
(Fortis: ≤ 7, not the 14 the individual band maxima would suggest). The base minimum must be added
to the data by `loadout_parser.py` from the composition line; it cannot be inferred.

**Decision — B21 is split.**

* **B58 (new)** — banded optional model groups. Parser records the band max (already present) and
  the base group's minimum (new); `loOptCounts` returns a count rather than 0/1; `loGroupCounts`
  honours it; the B13 toggle becomes a stepper capped by the band max and by the remaining models
  after the base minimum is reserved. Engine + parser + data, and it must be split into a parser/data
  turn and an engine turn per standing rule. This is the gate.
* **B21** — narrowed to the four one-line re-scopes above, data-only, ships the turn after B58's
  engine half lands. No pooled cap, no fan.

**Mechanism calls made here (reversible, not escalated).** The stepper is the control shape — it is
what a 0-N band is, and B13's existing toggle is the degenerate one-band case, so the toggle path
folds into the stepper rather than living beside it. B56g's `optional + per_bracket` escort toggle
stays exactly as it is: an escort rides *alongside* the bracket and does not consume it (D174),
whereas these bands are drawn *from* the 10-model total. Same field name, opposite arithmetic —
they must not be merged.

**One product question is batched to Ryan** (does not block B58's scoping): whether the base
group's minimum should hard-cap the variant steppers so an illegal mix is unreachable, or be
allowed and flagged. Recommendation: hard-cap, per D0 — this is a composition rule, not a points
overrun, and every other composition constraint in the tool is unreachable rather than flagged.

## D180 — B58 phase 1 shipped: base-group min lands on every banded unit, not just the four D179 kill teams (S112)

**Turn type.** Parser + data. `index.html` untouched.

**What shipped.** `loadout_parser.py`'s composition parser (`parse_comp_row` / `emit_count`) now
records a `min` field on every `fills_to_size` model group, taken from the low end of its "A-B"
composition line — the same value D179 asked for on the four Deathwatch kill teams. `unit_loadouts.json`
regenerated; `rules_assertions.py` gets a new fact, B58-1, checking every `fills_to_size` group's
`min` against the source composition line.

**Why this is 53 units, not 4.** D179's plan called for scoping the change to the four kill teams
and diff-guarding that nothing else moved. That plan didn't survive contact with how `repro_check.py`
actually works: it seeds only the three hand-authored entries and freshly regenerates every other
unit from source on every run. `min` is a property of the shared composition-line parser, not a
per-unit special case — so a fresh regen puts it on every banded body group in the dataset, not just
the four. Scoping the parser change itself to exactly four units would require hard-coding those
unit_ids into `parse_comp_row`, which is the kind of special-casing the project avoids, and would
leave `repro_check.py` permanently unable to agree with a hand-trimmed committed file.

**Verification before adopting the wider file.** Diffed a full fresh regen against the previously
committed `unit_loadouts.json`: every changed unit (53, all non-hand-authored units with a banded
body group) differs by the `min` field alone — no option, weapon, or default-weapon changes, no
regressions. The parser's nine pre-existing UNMATCHED-sentence gaps are unchanged from baseline and
are unrelated to this change. `repro_check.py` passes byte-identical against the new file;
`units_repro_check.py` unaffected (different file). Full harness suite passes; the two pre-existing
`bundle_check.js` B36 failures and the pre-existing `pts_check.js` cost-move note on 000000118 are
both confirmed unchanged from the prior committed file.

**Mechanism call made here (reversible, not escalated).** Apply `min` generally rather than special-
case the four units. This is additive data only — the engine reads nothing from `min` yet (same as
`max` today, per D179) — so the wider scope carries no behavior risk this session. B58's engine half
(S113) is the only place this data starts doing anything.

**Status.** B58 phase 1 (parser/data) complete. B58 phase 2 (engine: stepper, `loOptCounts` returns
a count, `loGroupCounts` honours the band and the reserved minimum) is next. B21 (four one-line
re-scopes) remains gated on B58 phase 2 landing, unchanged from D179.

## D181 — B58 phase 2 shipped: banded optional model groups become steppers, hard-capped by the base group's minimum (S113)

**Turn type.** Engine only. `index.html` v5.84 → v5.85. No parser or data file touched.

**What shipped.** The `min` and `max` fields on model groups now bound what the player can take.

* `loOptCounts(def, entry)` returns a **model count** per optional group, clamped to that group's
  band `max`, instead of the 0/1 flag it returned before. The B56g escort shape
  (`optional + per_bracket`, D174) is still a flag and is clamped to 1 — `loGroupCounts` turns the
  flag into the bracket count, so a count there would double-apply.
* New `loOptHeadroom(def, size)` — how many models the variant bands may draw from. Size, minus
  every non-optional reservation (fixed counts, per-bracket counts), minus the `fills_to_size`
  group's composition `min`. Groups with no `min` contribute 0, which is exactly the pre-B58
  arithmetic, so unbanded units are untouched by construction.
* New `loOptMax(def, size, optCounts, groupName)` — one group's live ceiling: its band max,
  narrowed by whatever headroom the sibling bands have left. This is the single source of truth for
  the stepper's `(max N)` label and for the click handler's clamp, so the control can never offer a
  step it will not honour.
* `loGroupCounts` serves the bands in `model_groups` order, each clamped by its own band and by the
  remaining headroom, decrementing as it goes. The `fills_to_size` remainder is therefore
  guaranteed to land at or above its `min` without needing a separate floor.
* UI: a band wider than 1 renders as a stepper. A one-wide band keeps the existing Add/Included
  toggle — the toggle *is* the degenerate one-band stepper, so both run through one handler rather
  than living beside each other. `editLoadoutOptional(listId, groupName, delta)` takes no delta for
  the toggle path and ±1 for the stepper; both clamp through `loOptMax`.

**The product call was taken as recommended: hard-cap.** An over-band mix is unreachable rather than
reachable-and-flagged, per D0 and consistent with every other composition constraint in the tool. A
one-band group with no headroom now renders disabled with "No models left at this unit size" rather
than as a live button that does nothing — the cap has to be visible, or it reads as a broken control.

**In-order trimming is the backstop, not the mechanism.** The UI clamps on the way up, so the trim in
`loGroupCounts` only fires for a saved list reopened at a smaller size or with hand-edited storage.
Order-of-declaration was chosen over any proportional split because it is deterministic and stable:
the same saved list always resolves the same way, and an earlier band keeps its value rather than
every band shifting when one is trimmed.

**Verification.** New harness `b58_check.js` (55 checks): headroom arithmetic on all four D179 kill
teams, band-max clamping in `loOptCounts`, a legal Fortis mix resolving to exactly 10 models with the
body at its minimum of 2, over-spent bands trimmed in order, `loOptMax` narrowing as siblings fill,
B13 (Victrix) and B56g (Hunting Wolves) regressions, and a global sweep over every unit with an
optional group at every bracket confirming no body group drops below its `min` and no total exceeds
the bracket. Full existing harness suite passes; `bundle_check.js`'s 2 pre-existing B36 failures and
`pts_check.js`'s pre-existing `000000118` note are both confirmed unchanged.

**Assertions.** New **B58-2** pins the engine wiring (both new helpers defined, `loOptCounts`
clamping to the band max, `loGroupCounts` clamping by band *and* headroom) and adds a data-side
guard that no unit's banded groups are unreachable at every bracket. **B13-1** was re-pinned: it
matched the literal line `if (!currentlyOn && isOptEpicHeroBlocked(...))`, which the stepper rewrite
replaced. The fact it asserts is unchanged — turning off is always allowed, the cap guards turn-on
only — so the check now pins the turn-off early return and the cap guard *and their order*, which is
what the fact actually says. Suite: 59/60, P3 the known `pipeline_manifest.py` custody failure.

**One live regression, and it is a data defect the cap exposed — filed as B59.** Invader ATV
(Outriders `000002712`) is a consuming `optional` group with `max: 1`, sitting against a body group
with `min: 2` and a fixed Sergeant. At the 3-model bracket that is zero headroom, so the ATV becomes
unreachable there. The source disagrees with the model: the composition line reads
`1 Outrider Sergeant / 2-5 Outriders / 0-1 Invader ATV`, and MFM prices the squad at 70 / 140 with
the ATV a separate flat **+60 pts** (D182 replaces the sourcing this paragraph originally used —
`Datasheets_models_cost.csv` 80 / 160 is the wrong table; MFM is definitive). The ATV rides
*alongside* the bracket but does not draw from it (D182 fact 3); its +60 is not currently charged
either, because `mfm_points_parser.py` drops the additive `• + 1 <name><N> pts` line entirely (a
separate, older defect, not the B58 exposure). Note what the old behaviour actually produced: ATV
on at size 3 gave 1 Outrider, which violates "2-5 Outriders". So this is not a working case that
broke — it is an illegal build that is now correctly unreachable, at the cost of the ATV being
unavailable at the small bracket until B59 lands. Accepted as the right direction under D0. B59's
mechanism, splitting, and category rules are set in D182.

**Sequencing.** B58 is closed. B21 (four one-line re-scopes) is unblocked and is the next data turn;
B59 splits into its own engine + data turns (D182), independent of B21.

## D182 — B59 mechanism, category distinction, and pricing correction; B21 shipped (S114)

**Turn type.** Data turn on `unit_loadouts.json` (B21 only) plus this decision log, an
executable assertion, and the backlog. No engine, no data touched for B59 — B59 splits
into its own two turns per this decision. Baseline byte-identical at open (`repro_check.py`
and `units_repro_check.py` both OK); 60/61 rules assertions at close (P3 the known
`pipeline_manifest.py` custody failure).

**B21 shipped — four one-line scope corrections.** Following D179 exactly, the parser now
scopes an indefinite one-model swap ("One model can replace its X with 1 Y" and its
requires-weapon variant "One model equipped with a W can replace its X with 1 Y") to the
model group that actually carries the gating or replaced weapon, instead of unconditionally
scoping to the body. The change is additive — a unit with no variant model group carrying
that weapon falls through `resolve_scope`'s existing word-overlap match to the body group
unchanged. The diff-guard confirms this: exactly three units changed across all 338
loadout definitions, holding four rescoped options between them, and `model_groups` /
`default_weapons` / `_defaults_source` are byte-identical on all three:

* Fortis Kill Team `000002780` `cnt_4` — plasma pistol swap moves to "Kill Team Intercessors
  with plasma incinerators" (its `requires_weapon: Plasma incinerator` gates it there).
* Fortis Kill Team `000002780` `cnt_5` — vengor launcher swap moves to "Kill Team
  Intercessors with superfrag rocket launchers".
* Spectrus Kill Team `000002779` `cnt_4` — instigator bolt carbine swap moves to "Kill
  Team Infiltrators with bolt sniper rifles".
* Indomitor Kill Team `000002781` `cnt_2` — multi-melta swap moves to "Kill Team Heavy
  Intercessors with melta rifles".

The parser edit is the fix; the regenerated `unit_loadouts.json` is byte-identical to the
freshly-parsed pipeline output. No hand-edit; `_defaults_source: equipped` preserved on all
three.

**B59 mechanism — `non_consuming: true`, not the D174 escort shape.** The previous session's
recommendation to reuse `optional + per_bracket + price_per_model` for the Invader ATV is
withdrawn. Confirmed rules facts (product owner):

1. MFM is the definitive pricing source (not `Datasheets_models_cost.csv`).
2. One ATV may be added per Outrider Squad, regardless of squad size (3 or 6).
3. The ATV does NOT count toward the squad's model count.
4. Up to three ATVs can enter the list via Outrider squads — but that ceiling is derived
   from the plain battle-size squad limit (Outrider Squad has no Battleline keyword, so
   3 at Strike Force, 2 at Incursion). Three is a consequence of three squads, never a
   constant to encode.
5. ATVs added this way do NOT count against the standalone Invader ATV datasheet's
   (`000001158`) own unit limit.

Fact 2 kills the escort shape. `per_bracket: {"3": 1, "6": 1}` encodes a constant as a
lookup table, which reads as if it varies with the bracket. It does not vary. Hunting
Wolves genuinely vary (3 with 3, 6 with 6); the ATV does not. Reusing the same field name
for opposite arithmetic is exactly the mistake D179 warned against for B58's stepper
groups vs B56g's escort groups — same shape name, different rule.

The correct mechanism is a `non_consuming: true` flag on a plain `optional` model group
with `max: 1`. It states the one true rule ("this group does not draw from the bracket"),
composes cleanly with the B58 stepper if a banded non-consuming escort ever appears, and
costs one condition each in `loOptHeadroom` and `loGroupCounts` (skip the reservation and
skip the headroom deduction). The ATV's price is a plain `price_per_model: 60`, read as a
literal — never scaled, never chapter-overridden (verified across all seven MFM
occurrences, including Blood Angels' 75/140 squad which still carries a flat +60 ATV).

**Category distinction — write this down or the next case is a coin flip.** "Embedded
optional model group" now has two opposite limit behaviours, and both are correct:

* B13 Epic Hero — the cap is written on the character. An embedded Chapter Ancient DOES
  count against the army-wide 1-per-army cap. The cap follows the model.
* B59 ATV — the unit limit is written on the datasheet SELECTION. An embedded ATV does
  NOT count against the standalone Invader ATV datasheet's limit. The cap does not
  follow the model.

Rule to apply next time: does the cap govern the model/character (model-scoped), or the
datasheet selection (selection-scoped)? Model-scoped caps follow the model wherever it
appears; selection-scoped caps do not. This is the distinction the next embedded-model
question must be answered against, not "does it feel like it should count."

**Pricing sourcing correction to D181.** D181's write-up cited
`Datasheets_models_cost.csv` at 80 / 160 for Outriders and stated B21 and B59 would ship
together. Both are wrong. Outriders live points are 70 / 140 (MFM), not 80 / 160
(`Datasheets_models_cost.csv`) — which the chapter-generic MFM overlay already correctly
overrides in the committed `units.json`. The wrong table was cited, not the wrong number
committed. And B59 no longer ships with B21: B59 is engine + parser + data across two
turns; B21 is one data turn that stands alone. D181 has been corrected in-place; this
paragraph is the audit trail.

**Executable pin on fact 5 — B59-1.** Fact 5 currently holds by structure (every
armyList limit count filters entries by `unit_name`; nothing walks into a unit's
`model_groups` to build the count), but structure without a pin is a fact that goes stale.
D107 applies: state the fact executably. `B59-1` in `rules_assertions.py` fires if any
higher-order call over `armyList` in `index.html` dereferences `.model_groups`, and also
confirms the two concrete anchors — Outrider Squad `000002712` still carries the "Invader
ATV" embedded group, and standalone Invader ATV `000001158` still exists as its own
datasheet. E10 duplication or a future "render the ATV as its own line item" would break
fact 5, and this assertion catches that before the change ships. Passes today.

**B59 split into two follow-on turns (Claude's sequencing call).**

* **B59a — engine turn.** Add `non_consuming` handling to `loOptHeadroom` (a
  non-consuming group contributes zero reservation) and `loGroupCounts` (a non-consuming
  group's model count is not subtracted from remaining headroom, so it does not compete
  with the bracket). Pin the wiring with a new assertion the way B58-2 pins its. Do not
  touch data.
* **B59b — data / parser turn.** Teach `mfm_points_parser.py` the additive
  `• + 1 <name><N> pts` MFM line so it emits a per-item price rather than dropping the
  line entirely. Flip `000002712` in `unit_loadouts.json`: the "Invader ATV" model group
  gains `non_consuming: true` and `price_per_model: 60`. Diff-guard: exactly `000002712`
  changes in `unit_loadouts.json`; the ATV +60 lands in `wargear_points.json` or the
  equivalent MFM-priced structure the parser feeds. Fix the parser, never hand-edit.

**B59 sequencing note.** B21 shipping does not depend on B59, and B59a does not depend
on B59b — the engine change is a no-op until `non_consuming: true` appears in data. The
strict engine/data turn separation is preserved by ordering them B59a then B59b.

### Baseline at close

`index.html` **v5.85** — unchanged, no engine edit this session. `unit_loadouts.json`
217/338 with exactly three units changed (four options rescoped); `repro_check.py`
reproduces the new file byte-identical from source. `units.json` 270/14, unchanged;
`units_repro_check.py` byte-identical. `rules_assertions.py` **60/61** (P3 known
custody failure, unchanged). Full harness suite passes: `pool_check.js`, `e10_check.js`,
`b18d_check.js`, `required_size_check.js`, `b31_check.js`, `stat_check.js`,
`default_check.js`, `pts_check.js`, `limit_check.js`, `b56g_check.js`, `b58_check.js`.
`bundle_check.js` 2 pre-existing B36 failures, unchanged.

## D183 — B59a: non_consuming engine wiring, pure no-op on current data (S115)

**Turn type.** Engine-only, per D182's split. No data touched — `unit_loadouts.json`
and `units.json` are untouched, and both reproduce byte-identical from source at
close. Baseline at open matched `NEXT_SESSION_PROMPT_115.md` exactly: both repro
checks OK, `rules_assertions.py` 60/61 (P3 the known `pipeline_manifest.py` custody
failure), full harness suite passing, `bundle_check.js` at its 2 pre-existing B36
failures.

**What changed.** Two `index.html` functions gained explicit handling for a
`non_consuming: true` flag on a model group (D182's mechanism for the Invader ATV
and any future case of the same shape):

* `loOptHeadroom` — a `non_consuming` group is now excluded from the reservation
  subtracted from size by name, not only incidentally (every `optional` group was
  already skipped by the existing `ct.optional` check; the new check states the
  fact directly so it holds even if that incidental path is ever refactored).
* `loGroupCounts` — the optional-group branch now forks on `non_consuming`. The
  non-consuming path clamps the stored count to its band only: no deduction from
  the shared `headroom` other bands compete over, and no addition to `reserved`
  (the running total a `fills_to_size` group's remainder is computed against).
  Both omissions matter — either one left in would either starve a sibling band of
  headroom it hasn't earned, or shortchange the fills-to-size group by treating
  the ATV as if it were part of the bracket it explicitly rides alongside.

No other engine behaviour changed. Pricing is untouched — a `non_consuming` group's
`price_per_model` still runs through the ordinary `ptsForEntry` path.

**What the assertion pins.** New `B59a-1`, modeled on `B58-2`'s shape: two literal
`index.html` needles confirm both functions carry the explicit handling, plus a
data-side pass over `unit_loadouts.json` that is deliberately passive today — zero
model groups carry `non_consuming: true` yet (that is B59b), so the check passes
vacuously. If a group with the flag appears before B59b lands through some other
path, the assertion additionally requires it sit on an `optional` group, the only
shape D182 defines the mechanism for. Suite: **61/62**, P3 the same known custody
failure.

**What is left for B59b.** The engine change is inert until data sets the flag.
B59b (banked, next session) teaches `mfm_points_parser.py` the additive
`• + 1 <name><N> pts` MFM line and flips Outrider Squad `000002712`'s "Invader ATV"
group to `non_consuming: true` with `price_per_model: 60`, per D182.

**Verification.** `repro_check.py` and `units_repro_check.py` both byte-identical
at close — the engine edit did not require or produce any data change, confirming
B59a is the pure no-op D182 called for. Full harness suite re-run after the edit:
all pass, `pts_check.js`'s pre-existing `000000118` note and `bundle_check.js`'s 2
pre-existing B36 failures both unchanged.

### Baseline at close

`index.html` **v5.86**. `unit_loadouts.json` and `units.json` unchanged from S114;
both repro checks byte-identical. `rules_assertions.py` **61/62** (P3 known custody
failure, unchanged; new `B59a-1` added and passing). Full harness suite passes:
`pool_check.js`, `e10_check.js`, `b18d_check.js`, `required_size_check.js`,
`b31_check.js`, `stat_check.js`, `default_check.js`, `pts_check.js`, `limit_check.js`,
`b56g_check.js`, `b58_check.js`. `bundle_check.js` 2 pre-existing B36 failures,
unchanged.

## D184 — B59b: MFM additive-line parser + Outrider Squad Invader ATV data flip; B59 closes (S116)

**Turn type.** Data / parser turn, per D182's split. `index.html` does not move. Baseline
at open matched `NEXT_SESSION_PROMPT_116.md` exactly: both repro checks byte-identical,
`rules_assertions.py` 61/62 (P3 known custody failure), full harness suite passing,
`bundle_check.js` at its 2 pre-existing B36 failures.

**Parser fix.** `mfm_points_parser.py` was silently dropping a whole class of MFM line —
the additive add-on shape (`• + 1 <name><cost> pts`), distinguished from a size bracket
by the leading `+`. This predates B59 and is not the B58 exposure; it's a separate,
older gap. New `ADDON_RE`, tried after `COST_RE` and `COMPOSITION_RE` both miss, matched
against every relevant MFM file: all seven Space Marine family occurrences of the
Invader ATV line read a flat 60 with zero disagreement, confirming D182's fact 5 by
construction rather than by eye. (An eighth occurrence of the same line shape exists —
Tau Empire's Tidewall Defence Platform, 20 pts — noted for the record since the fix is
general, but Tau is outside every current build track and nothing wires it up.)

**Where the validated fact lands.** `build_wargear_points()` now collects and
cross-chapter-validates addon lines in parallel with `WARGEAR OPTIONS` items, returning
a third `addons_out` value. This is deliberately a separate map, not routed through the
existing `items` lookup: an add-on's name is a model group's own label, not a reachable
swap/wargear item name in `unit_loadouts.json`, and D173 already rejected that shape for
model-group pricing (Hunting Wolves, D175). `wargear_points.json` gained a new `_addons`
top-level key holding the validated fact (datasheet `000002712`, "invader atv", cost 60,
sourced to the generic Space Marines MFM line) — an audit trail only. The engine never
reads it; the engine-facing price is the literal `price_per_model` on the
`unit_loadouts.json` model group, per D182. Confirmed via diff: the existing `items`
section of `wargear_points.json` is byte-identical to before this session; only `_addons`
is new.

**Data flip.** `unit_loadouts.json` `000002712` (Outrider Squad): the "Invader ATV"
model group gains `"non_consuming": true` (inside `count`, alongside `optional`/`max`)
and `"price_per_model": 60` (sibling of `count`), matching the field shapes `index.html`
already reads (confirmed against the literal engine source, not assumed). Diff-guard:
exactly `000002712` changed across all 218 entries.

**New `HAND_AUTHORED` seed, same class as D175.** Neither field is derivable from
Wahapedia source — `loadout_parser.py` has no way to know MFM pricing or the
"does not consume the bracket" fact, and `equipped_parser.py` never touches pricing or
count fields at all (confirmed by inspection; it only ever writes `default_weapons`/
`default_wargear`). `000002712` was added to `repro_check.py`'s `HAND_AUTHORED` list as a
fourth seed, exactly the shape D175 established for `000004131`. Its position in the
committed file was moved to sit immediately after the other three hand-authored entries,
matching where `loadout_parser.py`'s `out.update(existing)` seed-preservation step places
it — required for byte-identical reproduction, not a style choice (same requirement D175
already documented). `repro_check.py` confirms byte-identical reproduction with the new
seed. `b58_min_matches_composition` in `rules_assertions.py` also gained `000002712` in
its own local hand-authored exclusion set, for the same reason as the other three — a
frozen entry should not be checked against composition data it no longer regenerates
from. A stale "two hand-authored seeds" count in `P1`'s docstring was also corrected to
four.

**Bug found and fixed in the harness, not just the data.** Re-running the suite after the
flip failed `b58_check.js` on three checks. Investigation showed its Invader ATV section
was pinning the *original bug* B59 exists to fix: it asserted the ATV was correctly
unreachable at bracket size 3 (`want 0`), which was true under the pre-B59 engine (a
plain `optional`/`max` group with no `non_consuming` flag was clamped against the shared
headroom pool the same as any other optional group, and headroom at size 3 is 0 —
fully claimed by the Outriders `fills_to_size` minimum) but is exactly backwards under
D182's confirmed rules facts (one ATV addable regardless of squad size). The section has
been rewritten to assert the corrected behavior: reachable at both bracket 3 and bracket
6, with Outriders unaffected either way. The suite's separate global "total equals
bracket size" invariant (section 10, swept across every unit) also didn't know about
`non_consuming` — it already excluded `per_bracket` escorts from the sum but was still
counting a `non_consuming` group's models into total, which is exactly backwards per
D182 fact 3. Extended the exclusion to cover both shapes. `b58_check.js`: 56/56 (was
55/55 before this session, with the stale section counted as passing against the wrong
expectation).

**Assertions.** `E14-1`'s call site updated for `build_wargear_points`'s new 3-value
return (was breaking on unpack). `B59a-1`'s data-side check turned active per plan: no
longer hardcodes "0 expected" in either its docstring or pass message; still tolerates
any count and only enforces the shape rule (a `non_consuming` group must sit on an
`optional` group). Suite: 61/62 (P3 known custody failure, unchanged).

**B59 closes.** All three pieces (D182 mechanism decision, B59a engine wiring, B59b
parser + data) are shipped across S114–S116. The Invader ATV is now buildable through
the whole squad-size range without the headroom-starvation bug, priced correctly, and
excluded from the squad's own model count and from the standalone Invader ATV
datasheet's separate unit limit (fact 5, still pinned by `B59-1`).

**Verification.** `repro_check.py` and `units_repro_check.py` both byte-identical (the
latter confirms `units.json` untouched this session, a pure data/parser turn as scoped).
Diff-guard confirms exactly `000002712` changed in `unit_loadouts.json`; `units.json`
byte-for-byte identical to S115 close. Full harness suite re-run clean, including the
corrected `b58_check.js`; `pts_check.js`'s pre-existing `000000118` note and
`bundle_check.js`'s 2 pre-existing B36 failures both unchanged.

### Baseline at close

`index.html` **v5.86** — unchanged, no engine edit this session. `unit_loadouts.json`
217/338 (unchanged count — `000002712` already existed as an entry; only its custody
status moves from parser-regenerated to hand-authored), exactly one unit changed vs.
S115 close; `repro_check.py` reproduces the new file byte-identical with the updated
4-entry `HAND_AUTHORED` list. `units.json` 270/14, unchanged; `units_repro_check.py`
byte-identical. `wargear_points.json` gains a new `_addons` top-level key; its existing
`items` data is byte-identical to before this session. `rules_assertions.py` **61/62**
(P3 known custody failure, unchanged). Full harness suite passes: `pool_check.js`,
`e10_check.js`, `b18d_check.js`, `required_size_check.js`, `b31_check.js`,
`stat_check.js`, `default_check.js`, `pts_check.js`, `limit_check.js`, `b56g_check.js`,
`b58_check.js` (56/56, corrected this session). `bundle_check.js` 2 pre-existing B36
failures, unchanged.


## D185 — E2 shipped: collapsible left-panel role-group sections (S117)

**Ticket.** E2 — Detachment, Epic Hero, Character, etc. sections in the left roster
panel should collapse/expand. No current "Detachment" section exists in the panel
(that's E4, still blocked on E1); the panel's actual sections are the eleven
`TYPE_ORDER` groups (Epic Hero, Character, Battleline, Infantry, Mounted, Beast,
Monster, Vehicle, Dedicated Transport, Fortification, Allied). Scoped to those.

**Mechanism.** Reused the existing collapsible pattern already shipped for the unit
popup's modal sections (`modal-section-header` / `toggleSection`), adapted for the
roster panel: each `role-label` header is now clickable, carries a chevron, and
toggles a sibling `role-group-items` wrapper. Collapse state lives in a new
`collapsedRoleGroups` Set, checked and updated inside `renderRoster()`. All groups
start expanded (matches current behavior on first paint); a section stays collapsed
across adds/removes/re-renders within the session because the Set persists in memory
independent of `renderRoster()` calls, but resets on page reload — a deliberate call:
this is a view preference, not army-list data, and doesn't belong in the saved-list
schema or `scheduleSave()`.

**No engine/data change.** Pure UI. `index.html` v5.86 -> v5.87. No parser, no JSON
output touched. `repro_check.py` and `units_repro_check.py` both byte-identical
(neither file type is affected by a UI-only change, confirmed anyway per the
engine/data separation rule). Full harness suite re-run clean: same 61/62 assertions
(P3 known custody failure, unchanged), same 56/56 harness checks, same 2 pre-existing
B36 `bundle_check.js` failures. Nothing shifted.

**E2 closes.**

## D186 — B57 resolved: no in-between sizes; MFM discrete sizes only (S118)

**Product call (Ryan).** The unit size picker offers only the discrete sizes
printed in the MFM (e.g. 5 or 10), not every legal count in between (e.g. 7).
Ryan confirmed this is the intended behavior — while some units are technically
legal at any count between the smallest and largest bracket, no one plays that
way, so the tool should stay on the printed MFM sizes only.

**No build required.** Checked the current engine: unit sizing is already driven
off `size_brackets`, which holds only the discrete MFM values — nothing
interpolates between them. Current behavior already matches this decision.

**B57 closes as a no-op.**

## D187 — E6 shipped: affordability dimming on left-panel units (S118)

Left-panel unit cards now dim (opacity 0.7) when the unit's cheapest legal build
(`minPts`, already computed for the roster's points badge) would not fit in what's
left of the points cap (`POINTS_CAP - totalPoints()`). Matches the decision already
recorded against this ticket: dim unaffordable units rather than border affordable
ones, since early in list-building almost everything is affordable and a border
would just paint noise.

The dim is lighter than the existing `at-limit` disabled look (opacity 0.5, blocked
cursor) — an unaffordable unit is still fully legible and clickable, since the
points cap is informational (a list can go over cap) rather than a hard block.
Recomputed on every `renderRoster()` call, so it tracks the list total live as
units are added or removed.

**No engine/data change.** Pure UI: `renderRoster()` reads two already-existing
values (`u.minPts`, `POINTS_CAP - totalPoints()`) and adds one CSS class. `index.html`
v5.87 → v5.88. No parser, no JSON output touched. `repro_check.py` and
`units_repro_check.py` both byte-identical. Full harness suite re-run clean: same
61/62 assertions (P3 known custody gap, unchanged), same 56/56 harness checks, same
2 pre-existing B36 `bundle_check.js` failures. Nothing else moved.

**E6 closes.**

## D188 — E19 opened + shipped: Configured/Remaining points moved next to Army Points (S119)
Ryan asked mid-session for the Configured/Remaining points display to sit directly next to the
Army Points selector in the top banner rather than pinned to the far right with a gap between
them. Logged as new ticket E19 and shipped same turn — pure markup/CSS, no data or engine change.
The `banner-points` block is now nested inside `banner-army-pts-wrap` instead of being a separate
top-level banner child with its own `margin-left: auto`. Visibility toggling (JS sets `.hidden` on
both elements together) is unaffected — same two element IDs, same JS call sites.

## D189 — E11 scope correction: full CSS-variable theme refactor, not a quick toggle (S119)
E11 was recommended in the S118 handoff as a self-contained "M" turn (a `theme` state var plus a
light-mode variable set). Once in the file, found `index.html`'s stylesheet has 72 distinct
hard-coded hex colors and zero existing CSS custom properties — no swappable seam to hang a light
mode on. Surfaced this to Ryan as a scope call: do it properly (convert the whole stylesheet to
variables, design an actual light palette) versus skip, versus a lighter-weight compromise. Ryan
chose the full refactor, accepted it may run 1–3 sessions, and agreed to do the visual
verification pass himself (Claude cannot render the DOM to eyeball contrast/hover states).

**Mechanism shipped this session (S119):** every hex color in the stylesheet replaced with
`var(--c-<hex>)`. Values classified by CSS property context (background-family properties →
"bg" bucket, everything else → "fg" bucket) rather than by color value alone, since the same
raw HSL profile means different things depending on whether it is a background needing to go
light or a foreground/border color needing to go dark for contrast on a light page. `:root` holds
the current (dark) values unchanged; `html.theme-light` re-declares the same variable names with
generated light equivalents (bg colors → light tints of the same hue; desaturated near-black
neutrals → warm near-white parchment; saturated fg accents → darkened same-hue variants; neutral
grays → inverted and clamped to a readable range). Mapping is mechanical/systematic, not
hand-tuned per element — expected outcome is "consistently reasonable," not "designer-perfect,"
which is why the visual pass is Ryan's next step before this is called done.

Toggle: a button in the top banner, far right (the slot freed by E19's move), driven by a small
inline `<script>` in `<head>` that applies `theme-light` to `<html>` from `localStorage` before
first paint (avoids a flash of the wrong theme), plus `toggleTheme()` which flips the class and
persists the choice. Default on first visit is dark (matches today, zero-regression choice —
Ryan's own light/dark/match-device question went unanswered when the E19 request came in instead,
so this is Claude's call on a fully reversible setting, not a guess dressed as a decision).

**Known follow-ups, not yet fixed:** the select-dropdown arrow icon is an inline SVG data-URI with
its own hard-coded `%23666` fill, untouched by this pass (URL-encoded, not a plain CSS hex token)
— may look wrong in light mode, cosmetic only. Several distinct dark backgrounds collapsed to the
same near-white tint on purpose (subtle panel-to-panel distinction was minor and not worth 15+
near-identical light shades); flag if a panel boundary reads as flat that used to be visible.

**Verification split:** engine/data checks (repro, rules_assertions, full 56-check harness suite)
all pass unchanged — this is a CSS/markup-only turn, confirmed no `index.html` JS logic outside
the banner markup and the new theme script was touched. The remaining verification — does the
light theme actually look right — is Ryan's, by design (D107-adjacent: a claim about visual
quality isn't a fact until someone looks at it, and Claude can't).

**Not yet done:** icon/contrast sweep across the config panel, modals, and badge states in light
mode. E11 stays open pending that pass; do not treat this session's build as closing the ticket.

## D190 — E11 closed: S120 visual verification pass, full changelog (S120)
Ryan's promised visual-verification pass on E11 (D189) happened this session, iteratively, via
screenshots and direct feedback rather than a single upfront spec. Full sequence, `index.html`
v5.90 → v6.1, CSS/markup-only throughout (confirmed via repro checks + full 56-check harness +
`rules_assertions.py` unchanged at every step):

**Structural depth (both themes).** Added dedicated `--bg-page` / `--bg-panel` / `--bg-card`
tokens, separate from the existing `--c-hex` palette (which is reused across many unrelated
components — repurposing those directly would have rippled unpredictably). All three main panels
now share one panel-level background instead of three different shades, which was the root cause
of "everything blending together." Roster unit-cards and Army List rows sit on the lighter card
tier above that. Section group headers (EPIC HERO / CHARACTER / BATTLELINE etc., both in the
roster and the Army List) brightened and given more breathing room between groups. Custom
thin/rounded scrollbars added globally, themed per mode. Selected Army List row border
strengthened 1px → 2px.

**Light theme, home screen.** Back Up All / Import / Recent were rendering near-white text on a
near-white background — effectively invisible; given a real light-grey fill, dark gold text, and
a visible border.

**Light theme, top banner — the multi-round fix.** Went through black → dark grey → medium grey →
**light** background across several rounds of feedback. The lesson, worth keeping: darkening text
further against a *medium*-brightness background hits a contrast ceiling fast, because there's
less headroom between "medium grey" and "black" than there is between "medium grey" and "white."
Once the banner background itself moved to a light tint, the gold accent text (My Lists / Export /
Copy / point values) came back up from a forced near-black to a real amber (`#8a6100`) — legible
*and* it restored the visual distinction between "this is clickable" (gold) and "this is a plain
label" (dark grey), which chasing text-darkness alone had been quietly erasing. The saved-list
name flipped from near-white to near-black to match. One correction mid-pass: the gold token
briefly drifted to an unintended `#241a00` during iteration (kept getting re-set across several
back-to-back edits) — caught when Ryan flagged the same element a third time, corrected, and
verified by direct grep against the shipped file rather than trusted from memory afterward.

**Light theme, elsewhere.** Chosen/selected option text (e.g. a picked wargear swap in the Unit
Options panel) was using a gold tone too light against white cards — darkened. Standard body
text (unit names, list-item names) darkened further on top of the S119 baseline. Section headers
bolded for standout against the lighter panels.

**Known cosmetic gap, closed.** D189 flagged the Army Points dropdown-arrow SVG as untouched by
the original refactor (hard-coded fill, not a CSS variable). Confirmed it was in fact broken —
`#666` fill against the medium-grey banner mid-pass — and themed it for light mode. Also found
the dropdown's underline was hover-only, so it read as non-interactive/broken at rest; made
persistent in light mode.

**Theme toggle.** Replaced the generic OS moon/sun emoji with custom inline SVG icons (gold-
accented, matching the app's own visual language) — this was itself a piece of feedback ("looks
generic"). Given its own dark tile so it doesn't blend into the lighter banner backgrounds.

**Stat-modal aesthetic pass (last item, both themes).** Ryan confirmed legibility was solid but
called the popup "plain" and asked for a recommendation. Three small, low-risk additions: a
`box-shadow` + 3px brand-red top accent on `.modal-box` so it reads as a floating overlay rather
than a flat rectangle; keyword pills reshaped to a true pill (999px radius) with a warm gold-brown
border (`--c-9a7a4a`, an existing token) instead of a flat grey box.

**Backlog housekeeping.** E11 closed this session (was left open at S119 pending exactly this
pass). New ticket **E20** logged for the three items Claude recommended against bundling in
(blue accent color, role-based keyword icon coloring, right-pane illustration) — no
recommendation to proceed on any of them without a specific ask.

## D191 — S121 backlog housekeeping: B56e retired, E20 closed, E12 deferred, E1 formalized
Four small product/roadmap calls from Ryan, no code or data touched, `OPEN_ITEMS_BACKLOG.md` only.

**B56e retired.** Judiciar Xacharus and Chaplain Kastiel (`000004179`, `000004180`) have no points
source in any of the 30 held MFM files. Ryan's call: disregard both characters rather than keep
chasing a source. Retired, not closed by resolution — if a source ever surfaces this is a fresh
pick-up, not a reopen.

**E20 closed without building.** The three items deferred from E11's visual pass (blue accent
color, role-based keyword icon coloring, right-pane illustration) — Ryan confirmed none are wanted
right now. New design tickets can be opened later if any resurface.

**E12 deferred to late roadmap.** User accounts/auth stays open but is explicitly held until the
list-builder feature set is otherwise done, per Ryan — not a technical blocker, a sequencing call.

**E1 formalized as its own ticket.** Detachment selection has been referenced as a dependency of
E4, B45's DP-budget item, and the detachment cross-cutting note since early sessions, but never had
a backlog entry of its own — every reference pointed at a ticket that didn't exist. Given its own
entry (E1) now that it's the next thing up; E4 reworded to reflect that it has nothing left for
Ryan to decide until E1 exists.

No rules-legality content in this entry — logged because B56e/E20/E12 are permanent product calls
(D0-adjacent precedent: what the tool tracks and pursues), and backlog prose alone can drift.

---

## D192 — E1 scoped: MFM is the 11th-Edition detachment source; E1 splits into E1a/E1b/E1c; E21 opened (S122)

**Session type:** analysis and documentation only. No code, no data, no `index.html` version bump.
Baseline at open was clean and unchanged: both repro checks byte-identical, `rules_assertions.py`
61/62 with P3 the known `pipeline_manifest.py` custody gap, full harness suite passing,
`bundle_check.js` at its 2 pre-existing B36 failures.

The full write-up is `E1_DETACHMENT_SCOPE.md`. This entry records the decisions and the one finding
that changes how the tool sources data going forward.

### The finding: the two data sources are different editions and they have drifted

The Wahapedia CSV dump is **10th Edition** — every `Source.csv` row is edition `10`, every
`Factions.csv` link reads `wh40k10ed`, last updated 2026-06-13. The **MFM faction files are 11th
Edition v1.0**, and each one carries a `DETACHMENTS` section giving, per detachment: name, DP cost,
force disposition, and the full enhancement list with current points and `(Upgrade)` tags. That
section had never been read before this session.

Across the eight MFM files covering the fourteen built army blocks: **143 detachments, 513
enhancements, 35 Upgrade-tagged**, and complete force-disposition coverage (PRIORITY ASSETS 33,
TAKE AND HOLD 39, PURGE THE FOE 27, DISRUPTION 24, RECONNAISSANCE 20).

Wahapedia matches **116 of 143 detachments (81%)** by name, and all 27 misses are 1 DP detachments —
that tier is new in 11th Edition and absent from the 10th-Edition dump. Of the 116 that do match, **11 have drifted enhancement sets**: Librarius Conclave gained
*Temporal Corridor* and re-priced four enhancements (Celerity 30→35, Fusillade 35→20, Obfuscation
20→25, Prescience 25→20); Champions of Fenris, Saga of the Great Wolf, Wrathful Procession,
Daemonic Incursion and Flyblown Host all carry different enhancement lists in 11th than the dump
shows. A further ~20 differences are naming only — Wahapedia suffixes `(Aura)`, MFM appends
`(Upgrade)`.

**Decision (engineering, not a product call): MFM is the source of record for what exists and what
it costs; Wahapedia contributes description text only.** The join is on a normalised name with
parentheticals stripped. Wahapedia enhancements with no MFM match are **dropped, not displayed** —
they are 10th-Edition leftovers, and showing them would put phantom options with wrong prices in
front of the player. The `(Upgrade)` tag is rules-significant under 25.04 and survives the join as
a boolean flag rather than being normalised away.

This is a **generalisation of the existing MFM-wins rule for unit points** to detachments and
enhancements, and it is worth stating as a standing principle: *where the MFM and the Wahapedia dump
disagree on anything that is a number or a list of what exists, MFM wins, because it is the current
edition and the dump is not.* Wahapedia remains the only viable source for prose.

### Correction made within the same session: two 11th-Edition text sources were missed

The first pass of this analysis concluded that no 11th-Edition rule text existed for the new 1 DP
detachments and that `Space_Marines_Faction_Pack_v1_0.md` was too fragile to parse. Ryan pushed
back — "you should at least have it for Daemons" — and he was right. Both conclusions were wrong,
and wrong in the precise way this project's own standing principle warns about: **absence from the
files I happened to grep is not absence from the sources we hold.** Recording the error rather than
quietly correcting it, because the failure mode is the recurring one and the principle only earns
its keep if breaches of it are visible.

What was missed:

- **`chaos_daemons_reference.md`** — a condensed faction-pack digest already established as a text
  source in this project (prior D-entries source ability text from it). Its `DETACHMENTS SUMMARY`
  section covers **all 9 Chaos Daemons detachments**, each with rule, enhancements (Upgrade tags
  included) and the full stratagem list, as clean structured prose. Chaos Daemons is at **100%
  11th-Edition coverage**, including all three 1 DP detachments.
- **`Space_Marines_Faction_Pack_v1_0.md`** — carries **15 full detachment pages** for the Space
  Marines detachments introduced in 11th Edition, including both 1 DP entries (Fulguris Task Force,
  Subversion Assets). The remaining 7 SM detachments are older codex ones that Wahapedia does hold,
  with faction-pack errata to apply on top. The two-column interleaving is a formatting problem,
  not a coverage problem: the columns are separated by a long run of spaces and split cleanly on
  column position.

**Decision: text sourcing is a three-tier ladder, highest first.** (1) Faction-pack digests
(`chaos_daemons_reference.md`, `Space_Marines_Faction_Pack_v1_0.md`) — current edition. (2)
Wahapedia — 10th Edition, used only where no tier-1 text exists, with faction-pack errata applied
on top where it exists. (3) Nothing — render name, DP, disposition and enhancement names and points
with no body text. This is subordinate to the numbers rule above: MFM wins on DP, points and which
enhancements exist, regardless of which tier supplied the prose. `detachments.json` carries a
`text_source` field per detachment so the UI never has to guess.

**Dark Angels faction pack added mid-session.** Ryan supplied
`Dark_Angels_Faction_Pack_June_2026.md` on seeing the gap list. It covers 5 DA detachments — Dark
Age Arsenal, Darkflight Pursuit and Interrogation Conclave (all three DA gaps) plus Lion's Blade
Task Force and Wrath of the Rock, which move from previous-edition to current text. All 14 MFM
enhancement names present, 15 stratagem blocks.

**Extraction quality is a variable worth naming.** The DA pack is **single-column and linear**, with
consistent `# Page N` markers and clean section labels (`DETACHMENT RULES`, `ENHANCEMENTS`,
`Restrictions:`, and stratagems as name / CP / `<DETACHMENT> STRATAGEM` / WHEN / TARGET / EFFECT).
It parses directly. The SM pack is the same underlying document type extracted as interleaved
two-column text. **A clean re-extraction of the SM pack removes the column-splitter from E1a
entirely** and lets one parser handle every pack — asked of Ryan, not blocking.

**Two findings that improve E21's odds.** The DA pack marks army-construction limits with a literal
`Restrictions:` line rather than burying them in prose, and its `RULES UPDATES` section carries a
live Battleline-elevation case: Company of Hunters granting OUTRIDER SQUAD the BATTLELINE keyword,
which moves that unit's count cap. Both are far more tractable than the Wahapedia dump's free prose,
and they shift E21 from "probably hand-curated" toward "probably parseable."

**Coverage at S122 close: 68 current-edition text, 66 previous-edition, 9 with none** — against the
27-with-nothing the first pass claimed. The nine are all 1 DP, in the four blocks with no pack held:
Black Templars (Marshal's Household, The Living Miracle), Blood Angels (Encarmine Speartip, Legacy
of Grace, Wrath of the Doomed), Space Wolves (Legends of Saga and Song, Veterans of the Fang), Death
Guard (Contagion Engines, Paragons of Putrescence).

**Assertion design note.** Per-tier totals move every time a faction pack arrives, so E1a asserts the
*invariant* — every detachment carries exactly one valid `text_source`, and every `none` appears in a
named gap manifest — and records the counts rather than hard-coding them. An assertion that has to be
edited on every input change is an assertion that will eventually be edited wrongly.

**The remedy for the rest is an input, not a build.** Packs for Black Templars, Blood Angels, Space
Wolves and Death Guard take the gap to zero and upgrade 41 more detachments to current text. Asked
of Ryan; nothing blocks on it, since adding a pack later is a parser re-run rather than a redesign.

**Source ruled out.** The `*_web.txt` composition files contain `DETACHMENT ABILITY` strings, but
they are stray headings inside a unit dump with no rule bodies — not a source.

### Faction mapping

Fourteen built army blocks, eight MFM detachment files. The six Codex: Space Marines chapters with
no MFM file of their own — Ultramarines, Iron Hands, Imperial Fists, Raven Guard, Salamanders,
White Scars — take the generic Space Marines list of 22. That list already contains their
chapter-flavoured detachments (Blade of Ultramar, Hammer of Avernii, Emperor's Shield, Forgefather's
Seekers, Headhunter Task Force, Stormlance Task Force) with no restriction language attached in any
source held. **Under D0's undetermined-legality default, all 22 are offered to all six.** The
chapter restrictions that do exist in the SM Faction Pack govern which *units* an army may include,
not which detachments it may select.

### Ticket split

E1 becomes a parent that ships nothing itself and closes when its three children are in.

- **E1a** — data-only turn. `detachment_parser.py` → `detachments.json`, keyed by the fourteen app
  army names. Pipeline integration is part of the ticket, not an afterthought: manifest entries for
  both new files, a third byte-identical gate (`detachments_repro_check.py`) alongside
  `repro_check.py` and `units_repro_check.py`, and six new `rules_assertions.py` entries per D107 —
  DP in 1–3; exactly one of the five dispositions per detachment; no duplicate detachment name
  within a faction; counts match the scope doc's table; no Wahapedia-only enhancement survives the
  join; `(Upgrade)` flags preserved.
- **E1b** — engine-only. `selectedDetachments` state, `SCHEMA_VERSION` 1 → 2 using the migration
  hook already stubbed in `list_store.js`, export/import coverage, `detachmentPointBudget()` and a
  `dpState()` helper mirroring `limitState()`.
- **E1c** — engine-only. Left-panel picker section and centre-panel display, info detail panes.
  Closes E1.
- **E21 — new.** Detachment-driven army-construction effects: require/forbid units, cross-faction
  unit unlocks, and Battleline elevation (which moves the count cap). Gated on E1c.

E4 is thinner than it looked. Enhancements arrive inside the E1a record already priced and
Upgrade-flagged, so E4 is an assignment UI plus a per-unit field plus the 25.04 limit rules — not a
second data build.

### Product decisions

**1. Rule-text sourcing — the one item deferred to Ryan, and after the correction it is an input
question rather than a display question.** The display side largely answers itself: show tier-1 and
tier-2 text and mark only the tier-2 items as previous-edition, which is a per-item fact the parser
knows rather than a blanket disclaimer over everything. **What is actually asked of Ryan:** faction packs for Black
Templars, Blood Angels, Space Wolves and Death Guard, plus a re-extraction of the Space Marines pack
in the Dark Angels pack's single-column form. Nothing blocks on either.

**2. DP budget at 3,000 points.** 25.03 defines only Incursion (1,000 / 2 DP) and Strike Force
(2,000 / 3 DP); the app also offers 3,000. **Treat 3,000 as Strike Force, 3 DP** — identical to how
`battleSizeUnitLimit` already treats it, so the two battle-size-derived rules cannot disagree.

**3. Enforcement mechanism: hard-block.** A selection that would breach the DP budget is refused,
and duplicate selection is made structurally impossible by the checkbox list. This follows the
recent precedent (D114/D115 unit limits) rather than the older flag-and-warn line in D0's mechanism
note. As with unit limits, the over-budget state stays *reachable* — from an imported list or a
battle-size switch — and stays visible as an error there rather than being silently trimmed.

**4. A known unenforced rule at E1 ship, recorded rather than hidden.** Between E1c and E21 the app
will know about detachments without enforcing their require/forbid restrictions. This bites on day
one for a built faction: Chaos Daemons' *Shadow Legion* forbids Daemon Prince and Epic Hero units
while unlocking a list of HERETIC ASTARTES units, and 34 detachment abilities across the dump carry
require/forbid language in free prose with no common shape. Logging it explicitly is the point —
D0's undetermined-legality default permits leaning permissive in the interim, but a gap that is not
written down is a gap that gets forgotten and later mistaken for correct behaviour.

**5. UI placement.** Left panel, pinned above the role groups, collapsible on E2's pattern; the DP
counter lives in the section header, not the banner, which E19 already filled.

### Housekeeping noted, not fixed

`pipeline_manifest.py` is still absent from the synced project files, so P3 fails unconditionally
and manifest verification is a manual SHA-256 exercise. `BACKLOG_INDEX_BY_NUMBER.md`, created in
S121, also never synced. Separately, `OPEN_ITEMS_BACKLOG.md` is not actually split into Open Items
and Closed / Shipped sections as the standing process rule describes — it uses inline status markers
across ~1,850 lines. Restructuring it is a real mechanical job and was not attempted here; flagged
rather than done silently.

---

## D193 — E1a shipped: `detachments.json`, the Unique-tag finding, and a text ladder that self-corrects (S123)

**Data-only turn.** `index.html` untouched and unchanged in version. New parser, new output, new
reproduction gate, seven new assertions.

### The finding that matters: detachments carry a second exclusion rule

`MFM_Instructions.txt`, in the `DETACHMENTS` legend, defines a field nobody had read:

> **Unique Tag:** Some detachments are tagged with a 'Unique' word or phrase. You cannot select
> more than one detachment that has the same one of these tags.

This is a **third selection constraint**, alongside the DP budget and 25.04's no-duplicates rule,
and it was missed entirely by the S122 scope pass. It is live in the data for two built armies
today: Blood Angels carries `GRACE` on Angelic Inheritors and Legacy of Grace, and `DOOMED` on
Rage-cursed Onslaught, The Lost Brethren and Wrath of the Doomed; Death Guard carries `FLYBLOWN` on
Champions of Contagion and Flyblown Host, and `ENGINES` on Contagion Engines and Mortarion's
Hammer. Twenty-seven tags exist across the full MFM set, so every faction built from here on will
have them.

`unique_tag` is now a field on every detachment record, and **E1e** is opened to enforce it. This
is the same failure mode D106 and the derived-data principle keep naming: the tag was in the source
the whole time, sitting one line above a field we did read.

### The scope doc's enhancement count was wrong

`E1_DETACHMENT_SCOPE.md` §2 states 513 enhancements. The MFM files hold **515**. Three detachments
break the 2-or-4 pattern the count assumed: Librarius Conclave has five (in all five armies that
get it), and The Living Miracle and Lords of the Warp have one each. Everything else in the §2
table reproduces exactly — **143 distinct MFM detachment rows, 35 Upgrade-tagged**, dispositions
33 / 39 / 27 / 24 / 20, and the per-faction DP breakdown.

The scope doc's 143 counts distinct MFM rows. The generated file holds **275 army-detachment
records**, because the six Codex chapters without an MFM file of their own each get a full copy of
the Space Marines 22. Both numbers are right; they answer different questions, and the assertion
records both rather than picking one.

### Numbers precedence, as built

MFM wins on which detachments exist, DP, force disposition, Unique tag, and which enhancements
exist with what points and Upgrade status. Wahapedia contributes prose only. **Nine
Wahapedia-only enhancements were dropped** rather than carried — three on Wrathful Procession, four
on Champions of Fenris, two on Flyblown Host. They are previous-edition leftovers and showing them
would put phantom options at wrong prices in front of the player. 27 of the 143 MFM rows have no
Wahapedia match at all, which is exactly the 116-of-143 the scope doc predicted.

### The text ladder, and a change to how tier 1 wins

Three tiers as scoped — `faction_pack` / `wahapedia_10e` / `none` — with **158 / 108 / 9** across
the 275 records, and the nine `none` records exactly the nine 1 DP detachments the scope doc named.

Two departures from the scoped record shape, both additive:

**1. Enhancement descriptions carry their own `description_source`.** `chaos_daemons_reference.md`
is a condensed digest: its enhancement text is a one-line gloss ("*A'rgath, the King of Blades
(Khorne, melee weapon buffs)*") where Wahapedia carries the full rule. Letting a detachment-level
`text_source` of `faction_pack` suppress better tier-2 text for every enhancement inside it would
have shipped worse prose in the name of a newer edition. Rule text and enhancement text are
independent fields and now record their sources independently.

**2. A tier-1 stratagem list only displaces tier-2 text if it is complete** — every entry naming
itself, pricing itself, and carrying a body. Stated as an invariant rather than a per-source
switch, so a source that improves starts winning automatically and a source that is only a summary
keeps losing without anyone having to remember which is which.

That invariant is what settles the Space Marines pack. It has **not** been re-extracted; it is
still interleaved two-column text, so the column-splitter stayed in scope. It works for rules,
restrictions and enhancement descriptions across all 15 SM spreads. It does **not** work for
stratagems: the floating `1CP` badges sit at arbitrary columns on the continuation pages and
roughly a third of stratagem names and CP costs came out wrong or null. Under the completeness
invariant those lists fail and the detachment falls back to Wahapedia 10th-Edition stratagem text —
correct previous-edition prose in place of mangled current-edition prose. **236 records take
Wahapedia stratagems, 30 take faction-pack stratagems, 9 have none.** The 30 are the two
single-page SM detachments (Fulguris Task Force, Subversion Assets), four of the five Dark Angels
detachments, and the three Chaos Daemons detachments with no Wahapedia row to fall back to.

A clean single-column re-extraction of the SM pack flips all 15 automatically, with no code change.
That is the strongest remaining argument for asking for it.

### Also shipped

- **`restrictions`** as a first-class field, populated from the packs' literal `RESTRICTIONS` /
  `Restrictions:` labels. Not needed by E1, but it is the raw material E21 was gated on and it
  costs nothing to capture while the pages are already being parsed.
- The MFM detachment-block parser **hard-fails on any unrecognised line**, with one named noise
  exception (a stray jammed `LEADER:WOLF GUARD TERMINATORS` annotation that PDF extraction dropped
  into the Space Wolves detachments block). A future MFM revision that adds a real field cannot
  slip past as silently-dropped text.
- Wahapedia HTML tables now get row and cell separators before tag-stripping. Without them,
  battle-size bands fused into unreadable runs like `BATTLE SIZEUNITSIncursionUp to 1 units`.

### Pipeline integration

`detachments_repro_check.py` is the **third byte-identical gate**, alongside `repro_check.py` and
`units_repro_check.py`. `detachments.json` is a first-generation file with no earlier committed
version to rebuild against, so its fixed point was established at first generation and verified to
hold on a second run before close.

`detachment_parser.py`, `detachments.json` and `detachments_repro_check.py` are added to
`pipeline_manifest.json`, taking it from 24 to 27 guarded files.

**Manifest staleness, found while doing that.** Because `pipeline_manifest.py` is still absent from
the synced project files, the manifest has not been regenerable for many sessions, and **13 of its
24 guarded hashes no longer matched the committed files** — `index.html`, `units.json`,
`unit_loadouts.json`, `wargear_points.json`, `loadout_parser.py`, `equipped_parser.py`,
`wahapedia_transform.py`, `mfm_points_parser.py`, `convert_to_json.py`, `rules_assertions.py`,
`repro_check.py`, `units_repro_check.py`, `stat_check.js`. All were refreshed to current content.
That is what regeneration means, but it is worth naming plainly: refreshing a hash blesses whatever
copy is present. The three large outputs are independently proven fresh by their repro gates; the
rest rest on being what the project holds. This is the cost of P3 having been unrunnable, and it
argues for getting `pipeline_manifest.py` synced.

### Assertions: 62 → 69

`P5` (the reproduction gate) plus `E1a-1` through `E1a-6`: DP in 1–3 and exactly one of five
dispositions; no duplicate name within an army and every Unique tag preserved with none invented;
the whole catalogue re-derives from the MFM text including enhancement names, points and print
order; no Wahapedia-only enhancement survives the join; `(Upgrade)` preserved as a boolean on
exactly the right enhancements; `text_source` in the three permitted values with the `none` set
exactly equal to the named gap manifest.

**Per-tier totals are recorded, not asserted.** They move every time a faction pack arrives, and an
assertion that must be hand-edited on every input change is one that will eventually be hand-edited
wrongly. The assertions compare the generated file against a fresh read of the MFM source and
report the counts in their pass message.

68/69 pass, P3 the known `pipeline_manifest.py` custody failure and the only one.

### Still open, neither blocking

Faction packs for **Black Templars, Blood Angels, Space Wolves and Death Guard** take the nine-gap
list to zero and upgrade 41 more detachments from previous-edition to current text. A
**single-column re-extraction of the Space Marines pack** flips 15 detachments' stratagems to
current text and removes the column-splitter. Both are parser re-runs, not redesigns.


---

## D194 — `detachments.json` deduplicated: 1.61 MB to 797 KB, and three dead Wahapedia join tables identified (S123)

Ryan reported the project file area has no room for `detachments.json` at 1.61 MB. Two independent
findings, neither of which costs anything.

### The file was half duplicate

The six Codex: Space Marines chapters with no MFM file of their own take the generic Space Marines
list, so **seven armies each carried a byte-identical copy of the same 22 records** — 132 of 275
records, and slightly over half the file. Verified byte-identical apart from the `army` field.

`detachments.json` now stores **one record per distinct detachment** (143) with each army holding a
list of keys into it. **1,613,440 bytes to 797,051 — 49% — with zero information loss.**

The key is `"<source faction>|<MFM printed name>"`, e.g. `Space Marines|ARMOURED SPEARTIP`. Not an
array index: an index is not stable across a regeneration, and E1b has to persist a selected
detachment into a saved list. Detachment names are unique within one MFM file (E1a-2 asserts it), so
the key is unique across the 143. The redundant per-record `army` field is gone — it is the index key.

**Deduplication is by content**, so if a faction pack ever gives one chapter its own text for a
shared detachment, the records diverge and separate entries reappear on their own. The parser hard-
fails on a key collision with differing content rather than silently keeping one.

A side effect worth noting: the `_meta` counts now read as the *distinct* figures — 143
detachments, 515 enhancements, 35 Upgrade, dispositions 33/39/27/24/20, text sources 68/66/9. Those
are exactly the numbers `E1_DETACHMENT_SCOPE.md` §2 quotes (with S123's 513→515 correction). The
deduplicated view is the one the scope doc was describing all along; the 275-record view was an
artifact of storing the chapter copies.

New assertion **E1a-7**: every key an army names resolves, every record is reached by at least one
army, and each record's own `key` matches the key it is filed under. The saving is only safe if the
indirection is airtight — a dangling key would silently drop a detachment from an army and nothing
else would catch it. Assertions now **70**, 69 passing, P3 still the only failure.

### Three Wahapedia join tables are dead weight

Checked every large file in the project area against every script, harness and assertion. Every CSV
is opened by explicit filename — nothing globs the directory — so this is a complete check, not a
sample. **Three files are referenced by nothing:**

| File | Size | What it is |
|---|---|---|
| `Datasheets_stratagems.csv` | 2,277,806 | `datasheet_id | stratagem_id` join, 91,111 rows |
| `Datasheets_detachment_abilities.csv` | 363,282 | `datasheet_id | detachment_ability_id` join |
| `Datasheets_enhancements.csv` | 289,608 | `datasheet_id | enhancement_id` join |

**2.93 MB, and they are superseded rather than merely unused.** All three answer *membership*
questions — which stratagems, enhancements and detachment abilities attach to a datasheet — and
D193 settled that membership comes from MFM, with Wahapedia contributing prose only. They are 10th
Edition. Keeping them would mean keeping a second, older answer to a question the project has
already decided.

`Adeptus_Astartes_Unit_Info.txt` (411,559 bytes) is also referenced by nothing, but it is a
hand-kept Wahapedia scrape rather than a pipeline input, so it is flagged for Ryan rather than
recommended for removal.

Dropping the three tables frees **2.93 MB against a 797 KB file** — comfortable headroom, with no
need to degrade what the app ships.

### Lossy options, costed but not taken

Had the free wins not been enough, the next cuts and what they cost:

| Option | Size | Loses |
|---|---|---|
| Dedup only (**taken**) | 797 KB | nothing |
| Dedup, drop stratagem text | 370 KB | in-app stratagem reference; a product call |
| Also drop enhancement descriptions | 204 KB | the text a player reads while choosing an enhancement — would gut E4 |
| Legality fields only | 112 KB | all prose |

Stratagems are 53% of what remains and are pure reference — a player consults them during a game,
not while building a list. If space is ever tight again, that is the cut to make, and it is Ryan's
call, not an engineering one.


---

## D195 — E1b shipped: detachment state, schema v2, and P3 brought back from the dead (S124)

**Engine-only turn.** `detachments.json`, every parser and every CSV untouched. `index.html`
**6.1 → 6.2**. One new harness, one new tooling script, three new assertions, assertions **70 → 73**
and — for the first time in many sessions — **all of them pass**.

Baseline at open was clean apart from the two known items: all three byte-identical gates passed,
assertions 69/70 with P3 the standing `pipeline_manifest.py` custody failure, full harness suite
green, `bundle_check.js` at its two pre-existing B36 failures.

### Two custody findings, both worse than the standing entry described

**1. `list_store.js` had silently drifted from the copy inlined in `index.html`.** The module lives
in two files: the standalone one, and an inlined copy inside `index.html` that is what actually
runs. The standalone copy was missing E9b's Warlord field — `warlord_entry_id` in `buildRecord`,
`warlordEntryId` out of `deserialize` — and had been missing it for several sessions. Nothing reads
the standalone file, so nothing caught it. This is exactly the shape of the stale-parser problem
D118/D123 solved for the pipeline: **a second copy of something, with no gate proving the two
match.** The remedy is the same. The module was rebuilt once and spliced into `index.html`, and
assertion **E1b-2** now compares them, located by the module's own delimiters rather than by line
number so an edit above or below it cannot make the check pass or fail for the wrong reason.

**2. The S123 manifest work did not survive the sync.** `pipeline_manifest.json` in the project area
at S124 open was the *pre-S123* copy: 24 guarded files rather than 27, missing `detachment_parser.py`,
`detachments.json` and `detachments_repro_check.py`, and with the same 13 stale hashes D193 reported
refreshing. So a session's manifest work was silently reverted, and nothing noticed, because the
thing that would have noticed is the assertion that could not run.

**Both of those are the same underlying problem: `pipeline_manifest.py` has never existed in the
project files.** With the script absent and the JSON present, P3 fails unconditionally *and* the
manifest cannot be regenerated, so it goes stale unobserved. It has been in that state since D123
introduced it.

**Decision: write `pipeline_manifest.py` rather than continue to work around its absence.** This is
tooling, not engine and not data, so it does not breach the engine-only rule. Two design choices in
it are deliberate responses to how it kept failing:

- **The guarded set lives in the script, not in the JSON.** If only the JSON survives a sync the set
  is still recoverable from source; if only the script survives, `--write` rebuilds the JSON from
  nothing. Previously the guarded set existed *only* in the file that was going stale.
- **`--write` fails loudly on a missing file** instead of quietly dropping it. A manifest that
  silently shrinks is a manifest that stops guarding the thing that actually broke.

`check()` now also reports two conditions the old JSON-only arrangement could not express: a file in
the guarded set that is missing from the JSON (the JSON is older than the script — regenerate), and
a JSON entry no longer in the guarded set (the reverse). The guarded set is **24 → 35**, adding the
three E1a files, `list_store.js`, the new `e1b_check.js`, and the six baseline harnesses that were
never guarded at all (`e10_check.js`, `b18d_check.js`, `b31_check.js`, `b56g_check.js`,
`b58_check.js`, `required_size_check.js`).

Regenerating blesses whatever copy is present — that is what regeneration means, and D193 was right
to name it plainly. It is safe here for the reason it was safe there: all three reproduction gates
and every assertion passed *before* the manifest was rewritten, so the copies being blessed are
independently proven.

### What E1b builds

**State.** `selectedDetachments`, an array of detachment **keys** into `detachmentDefs`. Keys, not
indices and not names: D194 stores `detachments.json` deduplicated, so array position is not stable
across a regeneration, and the key is the only durable identity. Order is selection order and is
preserved. Reset on list creation; restored on open; carried into every saved record.

**Schema v2.** `SCHEMA_VERSION` 1 → 2 through the hook stubbed for exactly this. The migration is
strictly additive: a v1 record gains `detachments: []` and nothing else on it is touched. That is
the only reading of a v1 record that cannot be wrong, since v1 had no way to express a detachment
choice at all. Export and import inherit it through the existing `migrate` path, so a v1 export file
written by an older build imports as v2 rather than being rejected as incompatible. `list()`
summaries gain `detachment_count`.

Also recorded, because it explains why v1 was carrying a field it never declared: **`warlord_entry_id`
was added inside v1 without a bump**, and that was correct — a record lacking it reads as "no Warlord
chosen", which is what an older record meant anyway. `detachments` is different only in that the
engine now has rules keyed off it, so the version boundary earns its keep. The schema history is
written into the module header rather than left to be reconstructed.

**Three constraints, not one.** This is the substantive design point. A legal detachment set has to
satisfy all three of:

1. combined DP within the battle-size budget (D192 item 3, hard-block),
2. no detachment selected twice (25.04),
3. no two selections sharing a Unique tag (D193).

E1b ships all three as pure functions — `dpUsed`, `duplicateDetachments`, `uniqueTagConflicts` —
behind a single read path, `detachmentSelectionState()`, so the picker, the header counter and any
later validation panel cannot disagree about the same set. `canAddDetachment()` is the hard-block
gate and returns a **typed reason** (`unknown` / `duplicate` / `unique_tag` / `budget`) rather than a
bare false, because a refusal without a reason is the failure mode B47's info buttons exist to fix.

**Precedence when two constraints both bite: the Unique tag is reported ahead of the budget.** A
budget refusal means "not right now" — free up DP elsewhere and the pick fits. A tag clash means
"never together", and no amount of freed DP will change it. Leading with the budget would send the
player off to rearrange a selection that could never have worked. This is live in the real data:
Blood Angels' *Angelic Inheritors* (3 DP, GRACE) and *Legacy of Grace* (1 DP, GRACE) break both
rules at once.

**E1e sequencing — decided, not escalated.** The Unique-tag *logic* lands here; the *enforcement
surface* — the disabled row and the refusal message — lands in E1c alongside the other two
constraints, and E1e closes then. Splitting it the other way would have meant E1c wiring two of
three constraints and a later turn reopening the same code for the third.

**DP budget.** `detachmentPointBudget()` returns 2 at ≤1,000 and 3 above, with 3,000 falling in the
Strike Force branch per D192 item 2. It and `battleSizeUnitLimit()` are two functions reading the
same 25.03 table; assertion **E1b-1** re-derives the DP column from `Army_Muster_Rules.txt`, reads
the threshold out of `index.html`, and demands they agree — and separately demands the two functions
split the battle sizes identically. Neither number is written down in the assertion. `dpState()`
mirrors `limitState()` exactly: `ok` / `at` / `over`, with `over` reachable from an imported list or
a battle-size switch and left visible as an error rather than silently trimmed.

**Data load.** `detachments.json` joins the existing parallel fetch. At 797 KB against `units.json`'s
larger footprint it did not need restructuring, so it was not restructured — that would be a data
turn, and D194 already records that stratagem text is the cut to make if space is ever tight again.
A missing file degrades to an empty catalogue, which reads as "no options at all" and is visibly
wrong rather than quietly wrong.

### Two behaviour precedents set, both recorded rather than assumed

**Unresolved detachment keys are kept, not dropped.** A saved key that no longer resolves against the
catalogue survives the load, contributes **0 DP**, and is reported as unresolved. This is the ghost-
entry precedent from saved units applied to detachments: silently deleting it would hide a data
regression behind a list that merely looks smaller, and inventing a DP cost for a record we no longer
hold would make the budget wrong in a way the player can neither see nor fix.

**`clearList()` does not clear detachments.** The control says "Remove all units from this list?" and
a detachment is not a unit. The choice is structural rather than part of the list's contents, and it
is one click to change in E1c. Flagged because it is the kind of small call that later looks like an
oversight if nobody wrote down that it was a call.

### Assertions: 70 → 73, and 73/73 pass

- **E1b-1** — the engine's DP budget is the DP column of the 25.03 table, re-derived from source on
  both sides, and it splits the battle sizes the same way `battleSizeUnitLimit` does.
- **E1b-2** — `list_store.js` and the inlined copy are byte-identical and both declare
  `SCHEMA_VERSION 2`.
- **E1b-3** — `e1b_check.js` passes in full. Per D107 the migration is a claim about *behaviour*, so
  it is executed rather than described; this is the first assertion that runs a Node harness, and it
  reports clearly if Node is unavailable rather than passing by default.

`e1b_check.js` itself is 100+ checks across twelve groups: the budget table, `dpState`, DP sums off
real records, the no-duplicates rule, the Unique tag (including a **derived** sweep that takes every
tag in the catalogue and demands the engine flag its first two holders, so a new faction's tags are
covered without editing the harness), the typed refusal reasons, the single read path, every army's
key list resolving, the schema round-trip, the v1→v2 migration field-by-field, export/import, and the
module drift guard.

**P3 passes.** It has not passed since D123 introduced it.

### Not done, deliberately

No picker and no detail panel — that is E1c, and mixing them would have put an untestable UI turn on
top of a state turn. The rendering side of `selectedDetachments` is unwired: nothing displays a
detachment yet, which is correct for E1b and is the whole of E1c's job.

### Housekeeping

**H2 is done** — the three superseded Wahapedia join tables are gone from the project area, freeing
2.93 MB. Nothing referenced them and nothing broke.

**A stale cross-cutting note corrected.** `OPEN_ITEMS_BACKLOG.md`'s leader-system note still said
"B7b (combined popup with aura markers) remains open — design turn next." B7b closed at S91 (D159).
The note is the drift the D107 principle keeps warning about, in the document that is meant to track
what is open.

**`H3` opened** for manifest custody. `pipeline_manifest.py` now exists, but it only helps if it
reaches the project file area — and the S123 evidence is that manifest work can be reverted by a
sync without anyone noticing. That is Ryan's action, and it is worth a ticket rather than a line in
a handoff precisely because the last two attempts to fix it lived in handoffs.


## D196 — E1c shipped: detachment picker over the E1b read path, and the second-implementation guard (S125)

**What.** `index.html` 6.2 → 6.3 with the E1c picker UI. Left-panel detachment section pinned above
the role groups reusing the E2 `.role-group` / `.role-label` / chevron pattern; DP counter in the
section header (not the banner — E19 already filled it); checkbox row per detachment from
`detachmentKeysForFaction(currentFaction)`; selected detachments render as a `Detachments` group at
the top of the centre army list; per-row info button opens rule name / rule text, enhancements and
stratagems in a `.det-detail` expander that reuses B47's toggle-detail mechanism. `list_store.js`
untouched — the schema was already at v2 with the field the picker needs.

**How legality is decided.** Every rule question — "is this addable?", "how much DP is used?", "is
this a Unique-tag clash?", "is this a duplicate?" — goes through `canAddDetachment` or
`detachmentSelectionState` from the E1b block. The picker holds one new classifier,
`detachmentPickerRowState(key, keys, pointsTotal)`, whose disabled flag is `selected ? false :
!canAddDetachment(key, others, points).ok` and nothing else. A selected row is always toggle-off-
able, whatever else is wrong with the set — flag-don't-drop applied to the picker, so an imported
list that arrives over budget or in a Unique-tag clash can always be corrected.

**Text tiers per D192.** `detTier2Badge(source)` marks any value other than the string
`'faction_pack'` as previous edition. `null` and `undefined` also flag — a missing source defaults
to non-current rather than silently reading as current, so a data regression that dropped a source
tag can never quietly promote tier-2 text to tier-1. The badge appears on the detachment rule
heading, per enhancement (each carries its own `description_source`), and on the stratagems block
(the parser records one `stratagem_source` per detachment). It is deliberately per item — a
detachment can carry a tier-1 rule text and tier-2 enhancement descriptions, and the player needs
to see which is which.

**The three over-constrained states are visible.** Over-budget renders a red counter and a warning
banner at the top of both panels; each Unique-tag clash renders a warning naming the tag and every
detachment carrying it; unresolved keys render as ghost rows in both panels with the key visible
so it can be removed. `hasGhosts` on load now ORs in unresolved detachments so the banner's "list
changed since saved" flag catches them alongside unit ghosts. None of these three is silently fixed
— they are reachable from an imported list or a battle-size switch, and hiding them would strand
the player.

**The structural guard is what makes this durable.** Assertion **E1c-1** greps `index.html` for a
`function` declaration of `dpUsed`, `duplicateDetachments`, `uniqueTagConflicts`,
`detachmentPointBudget` or `dpState` outside the E1b block, and fails if it finds one. A second
implementation of any of them in the picker is exactly the failure mode "single read path" is meant
to prevent, and would be invisible to every other gate. **E1c-2** runs `e1c_check.js`, which
executes 12 hand-picked scenarios plus a sweep across every one of the 143 catalogue keys and
confirms `detachmentPickerRowState` agrees with `canAddDetachment` on every disable decision. The
sweep exists because a picker that special-cases the harness fixtures without honouring the general
rule would pass the twelve scenarios and fail the sweep. Assertions **73 → 75**, all passing.

**What did NOT change.** `detachments.json`, every parser, `list_store.js` — all untouched.
`SCHEMA_VERSION` is still 2; the field the picker persists (`detachments`) was already in the
schema. The three repro gates and `bundle_check.js`'s two pre-existing B36 failures are the same
as they were at open. Guarded set 35 → 36 (`e1c_check.js` added).

**Design calls Ryan did not need to make and why.**

- *Panel-body placement.* The picker renders inside `#roster` above the role groups rather than as
  a separate top strip. That is the E2 pattern the prompt asked for, and it means the collapse
  state, theming and hit-target size are all inherited rather than re-implemented.
- *Refusal message order.* When both the budget and a Unique tag refuse the same add,
  `canAddDetachment` already reports the tag — a budget refusal is "not right now", a tag clash is
  "never together", and only one of those is worth acting on. The picker surfaces the tag reason
  verbatim. This is D195's ordering, not a fresh call.
- *Info panel scope.* Rule + enhancements + stratagems, in that order. Restrictions render when the
  record has them (rare in current data). Anything larger — combined-arms restrictions, unit
  unlocks, Battleline elevation — belongs to E21 and is deliberately not here.
- *Refusal text tone.* One sentence per reason, prose not codes. `"Over the DP budget for this
  battle size."`, `"Clashes with GRACE tag: Angelic Inheritors."` The typed reason from
  `canAddDetachment` is preserved for the harness; the prose is the projection.

**What closes.** E1a, E1b, E1c and E1e — every ticket under the E1 parent. E1 itself closes with
this decision. E4, E6 and E21 remain downstream and unblocked.

**What is still open.** H3 (`pipeline_manifest.py` custody in the project file area) — Ryan's
action, unchanged. The four faction-pack inputs listed in the S125 prompt (Black Templars, Blood
Angels, Space Wolves, Death Guard) take the no-text gap from nine to zero and upgrade 41
detachments to current text; worth more now that E1c renders it. A single-column re-extraction of
the Space Marines pack retires the column-splitter. Both are parser re-runs on E1a code as it
stands, not redesigns.


## D197 — Policy: no further extraction of code out of `index.html` without a positive reason (S126)

**What.** `list_store.js` stays exactly as it is, guarded by its E1b-2 structural check. No new
module gets pulled out of `index.html` unless there is a concrete, positive reason for that specific
extraction — "it would be tidier" is not one.

**Why this needed saying, not just doing.** `list_store.js` is the one extraction the project has
done, and the code it holds has not yet been used anywhere a second time — the payoff modularity is
supposed to buy (reuse, isolation, independent testing) has not materialized. What it did cost: a
multi-week silent divergence between the extracted file and the copy inlined in `index.html`, caught
only by building a new structural assertion (E1b-2, `e1b_check.js`) to police the two staying in
sync. A single-file deploy model means every extraction creates a second copy that has to be kept
byte-identical by a dedicated guard, forever, for as long as the extraction exists. That is a
standing cost paid every session, for a benefit this project has not drawn on once.

**The constraint is real, not aesthetic.** GitHub Pages serves `index.html` as the whole app; the
single-file architecture is a property of the deploy model, not a habit that can be refactored away
for free. Partial modularization — some logic inlined, some extracted — fights that constraint
directly: it adds the sync-guard tax without removing the single-file property it would need to
remove to pay for itself.

**Reversal condition.** A "positive reason" means something the project can point to: actual reuse
across more than one context, a testing need `e1b_check.js`'s pattern cannot cover, or a build-size
problem the single file has started to cause. Wanting the code to look nicer, or a new session's
default instinct toward tidiness, is not one. If a future ticket proposes an extraction, it should
name which of these applies before any code moves.

No rules-legality content — engine architecture and process precedent, logged per D107 so this
doesn't have to be re-argued from scratch next time someone eyes `index.html`'s length.

---

## D198 — S126 tooling session: repo custody check, gate consolidation, known-failure allowlist, backlog/decision-log split

**Turn type: tooling-only**, per the revised S126 prompt (E4 deferred to S127; a process review and a
repo custody pass between sessions surfaced six items worth doing first). `index.html`, every `.json`
data file, every parser and every CSV untouched — confirmed by `index.html` staying at 6.3 and the
three repro gates passing unchanged at both open and close.

**T1 — `repo_check.py` (net new).** Clones the public repo and classifies every file against the
project working area: match / differs / missing-from-repo / repo-only. GW-derived material found in
the repo is reported as a distinct, louder failure than ordinary drift — that class of finding is a
publication problem, not a sync problem. Rather than hand-maintaining a second exclude-pattern list
that could drift from `.gitignore`, the script reads `.gitignore` straight out of the clone and
buckets its patterns by the section-header comments already there (the file itself already labels
which blocks are GW-derived vs. local scratch), so the two sources cannot disagree. "Missing from
repo" is scoped deliberately narrow — the manifest's guarded set (read live from
`pipeline_manifest.json`, not hardcoded) plus a fixed doc list plus every `SESSION_HANDOFF_*.md`
found locally — rather than walking the whole project area, most of which is GW/Wahapedia source
material that is correctly and permanently excluded and would otherwise read as false "missing"
noise. A clone failure fails clearly with the reason (exit 2) rather than reporting a false clean.
Run against the real repo at session open: **the repo has been bulk-uploaded since S125** — 70
files, every one shared with the project area byte-identical, confirming H4's per-session refresh
happened and closing the immediate custody gap H3 flagged.

**T2 — hash convention.** Every handoff's Files section now carries a first-12-characters SHA-256
per changed and net-new file, verified by the next session before anything else runs. Deliberately
redundant with T1 — this still catches a bad sync one session later even if the repo is unreachable
or out of date when `repo_check.py` runs. Applied starting with this session's own handoff
(`SESSION_HANDOFF_126.md`) so S127 inherits it.

**T3 — `baseline.sh` (net new).** One command, one line per gate, covering both repro checks, both
JSON repro checks, `rules_assertions.py`, all thirteen harnesses with their correct positional
arguments baked in, `bundle_check.js`, `pipeline_manifest.py`, and `repo_check.py` (skippable via
`--no-repo` for an offline run). The argument shapes were the actual point — several harnesses take
three or four positional arguments and print a bare Node stack trace when called without them, which
read identically to a real failure before this existed. Verified end-to-end mid-session: when the T4
edit to `bundle_check.js` left the pipeline manifest stale, `baseline.sh` correctly went red on both
`rules_assertions` (P3) and `pipeline_manifest` — proof it catches a real problem rather than
rubber-stamping.

**T4 — known-failure allowlist in `bundle_check.js`.** B36's two failures (the merged-radio-vs.-
three-independent-Keep-rows shape) have printed on every run for many sessions. A gate that is
expected to print red trains everyone to skim past red, which is how a third, unrelated failure
would get missed. `ok()` now accepts an optional key; a keyed check that still fails prints `KNOWN`
and does not count toward the exit code, but the gate fails loudly — `FAIL allowlist stale` — the
moment either resolves without the allowlist being updated, and a third check that fails without a
key still fails the gate normally. An allowlisted key that never runs during a given execution
(renamed or removed check) also fails loudly, so a stale entry cannot hide silently either. Empty
`KNOWN_FAILURES` when B36 ships.

**T5 — backlog and decision-log split.** `OPEN_ITEMS_BACKLOG.md` had grown to 166 KB, almost entirely
closed-ticket narrative loaded and unread every session. Of its 117 tracked tickets, exactly **7**
are genuinely open: **H3, E21, E4, B56, E12, P2, B17.** Those 7 keep their full bodies in
`OPEN_ITEMS_BACKLOG.md`; the other 110 move in full to `BACKLOG_ARCHIVE.md` (net new), with a
one-line pointer (ID, title, closing status) left behind in the working file. Verified byte-for-byte
against the original — zero ticket content lost or duplicated across the split. The short
"Cross-cutting notes" section stays in the working file (still-live context for E4/E21); the S18-era
"Shipped" and "Doc debt" sections, being pure history, moved to the archive with the rest. The
decision log itself is **not** modified — `40K_Decision_Log_v3_0.md` remains authoritative — but
`DECISION_INDEX.md` (net new) adds a one-line-per-entry index (number, title, session) so a session
can find the two or three D-entries it needs without loading 537 KB.

**T6 — module-extraction policy.** Recorded separately as **D197** (no code): no further extraction
out of `index.html` without a positive, name-able reason.

**Manifest note.** `bundle_check.js` is a guarded file; T4's edit changed its hash, so
`pipeline_manifest.py` was regenerated at close (`--write`) after every gate passed. Guarded set
unchanged at 36 files — this session added no new guarded file, `repo_check.py` and `baseline.sh`
are tooling, not pipeline-guarded.

**What did NOT change.** `index.html`, every `.json` data file, every parser, every CSV. The bundle
of thirteen harnesses is otherwise unchanged. `40K_Decision_Log_v3_0.md` gained D197/D198 as append-
only entries; its existing content is untouched.

**Backlog.** T1–T6 and H4 opened as real tickets at session start per the prompt's instruction, and
closed here as each shipped. H4 (Ryan's per-session repo refresh becoming routine) closes on the
strength of the repo-check evidence above — the refresh has visibly been happening.
`PROCESS_IMPROVEMENT_PLAN.md` is superseded by these six tickets and is not maintained further.

