# Decision Index

One line per entry in `40K_Decision_Log.md` (number, title) — net new at **S126 (T5)**,
so a session can find the two or three entries it needs without loading a 537 KB file. The
decision log itself is authoritative and is not modified by this index; if the two ever
disagree, the decision log wins.

Two numbers (D158, D159) legitimately appear twice in the source log itself — both
occurrences are listed below in document order, exactly as the source has them. A handful of
entries (D93, D103, D104, D113–D115, D124–D129) carry no title on the heading line itself in the source; their one-liner below is pulled from the entry's opening sentence instead.

- **D0** — Foundational Rule: Legality Is the Only Boundary
- **D1** — Tool Purpose
- **D2** — Game Format
- **D3** — Points Limit
- **D4** — Technology Stack
- **D5** — Data Maintenance Approach
- **D6** — JSON File Structure
- **D7** — Excel as Data Maintenance Tool
- **D8** — Weapon Options Enforced
- **D9** — Release Philosophy
- **D10** — Browser Caching
- **D15** — Abilities Embedded Per Unit
- **D22** — INV and FNP Storage
- **D23** — Two-Level Parameterized Ability Naming
- **D25** — Daemonic Allegiance Units: Single Datasheets, God Selection at List-Build Time
- **D26** — units.json Nested Structure
- **D27** — Unit Size: Ordered Slots with Trailing Blanks
- **D28** — Points Pricing: Fully-Populated 3×3 Lookup Matrix
- **D29** — Army-Level Unit Instance Limit: Derived from Type with Override
- **D31** — Immediate-Add Interaction Model
- **D32** — No Hard Enforcement of Instance Limits
- **D33** — Leader Display in Army List
- **D34** — Error Flag System
- **D35** — Banner Layout and Color System
- **D36** — Bundled / Compound Weapon Swaps
- **D37** — Stable Unit Reference: Wahapedia datasheet_id carried through pipeline
- **D38** — List Management: Storage Mechanism
- **D39** — Saved-List Data Model: Reference, Versioned, Flag-Don't-Drop
- **D40** — List Construction Model: Model 2 (faction-on-list, autosave, home page)
- **D41** — MFM Update Strategy: Full Re-Pull of Changed Armies, No Patcher
- **D42** — SM-Family Chapter Points Sourcing: Base + Build-Time-Derived Override
- **D43** — Cross-Faction / Allied Points Sourcing (Pattern Catalog)
- **D44** — Structured Loadout Definition Schema (unit_loadouts.json)
- **D45** — Weapon Count Rollup: Exact, Not Heuristic
- **D46** — Add vs. Swap Distinction (Critical for Correct Counts)
- **D47** — Parser + Override Layer Pattern for Loadouts
- **D48** — army-name Flag Required for Non-SM Factions
- **D49** — Equipped-With Composition Parser (New Source + Parser Layer)
- **D50** — default_wargear Schema Field
- **D51** — default_weapon_counts Schema Field
- **D52** — Curated-Roster Scoping + Orphan Pruning
- **D53** — Legends: Keep in Source, Defer Processing
- **D54** — Wargear-Option Controls: Two-Control Model
- **D55** — Leader/Champion Block Visually Separated (Configure Pane)
- **D56** — Two Option Surfaces: Unconfigured Popup vs Configure Pane
- **D57** — Heterogeneous Named-Model Units Require Composition Prose
- **D58** — "Every Other Model" Resolves to the Complement of Named Groups
- **D59** — Tolerant Group-Name Matching (Footnotes, Irregular Plurals, "model" Suffix)
- **D60** — Victrix Honour Guard Count Model + Army-Wide Character Cap
- **D61** — Un-onboarded Units: Points-Driven "Unverified" Badge, Not Hide (resolves old Item 8)
- **D62** — "OR" Alternative-Profile Units → Size Brackets + Per-Bracket Counts
- **D63** — Compound "A and B" Replacement Choices Are One Pick (D0 held)
- **D64** — Coupled-Control Hard Interlock (Local Exception to D0 Flag-and-Warn)
- **D65** — Leader Inclusion in a Per-N Carrier Pool Follows the Datasheet Wording
- **D66** — Any-number-family parser: named-model scope + compound weapons
- **D67** — Any-number swap caps + per-source-weapon pool
- **D68** — Any-number swaps get their own heading; live-test gaps banked
- **D69** — Points join normalized; units.json reproduction chain established
- **D70** — Per-model keyword split, wargear abilities, per-datasheet ability text
- **D71** — Unit classification from shared + namesake keywords; Leader/Character promotion (B8)
- **D72** — Heterogeneous fixed-group split (B9)
- **D73** — Bundle / loadout integration and the compound-swap control model (B5, B6)
- **D74** — Stat-line INV/FNP overrides; configured popup made selection-aware
- **D75** — Captain relic-shield W correction; general characteristic-from-text reader; Shining Aegis de-hardcoded (B12 remainder)
- **D76** — B14: optional per-model wargear items routed to Other Options
- **D77** — B14 render wiring corrected; other-option / loadout de-dup; weapon-count root cause found
- **D78** — B16 shipped: per-model-group default weapons (weapon-count fix)
- **D79** — B17 (part 1): loadout option-parser gaps closed for the Deathwatch/Deathwing partials
- **D80** — B17 (part 2): the banked single-model / conditional-swap shapes
- **D81** — B17 (engine turn): count `requires_weapon` gate + `max_total` pool cap; Spectrus helix/comms
- **D82** — JSON export / import wired into the UI (data-loss recovery)
- **D83** — B17 (true-1b): variant sub-group default weapons (Deathwatch Kill Teams)
- **D84** — Reiver Squad parser gap: conditional add + unit-wide per-model item adds (S29)
- **D85** — Sanguinary Guard banner: one-model item add (S30)
- **D86** — "Back up all lists" multi-list export (S31)
- **D87** — E16: sort control on "My Army Lists" home page
- **D88** — B15 (safe subset): broad conferred always-on wargear characteristics → statline
- **D89** — E17: asterisk on statline cells with a per-model (bearer-only) INV/FNP
- **D90** — B14b/B14c investigation: rescope, and the `requires_weapon` gate is dormant (S35)
- **D91** — B19: the `requires_weapon` gate becomes a carrier count (S36, v5.52)
- **D92** — B14c(b): the three bearer-gated adds go live (S37, data-only)
- **D93** — B20 — engine half: single-model groups now honour `count` options, and every per-N cap is bounded by its own model group (v5.53,…
- **D94** — "N model's X can be replaced with…" is N models in the unit, not N per 5 models (parser + data)
- **D95** — Weapon names in `unit_loadouts.json` are family names, and a swap source can be compound (parser + data)
- **D96** — Session 41: the per-N passive-possessive shape (B26), the Whirlwind bleed (B27), and a 23-unit staleness fold
- **D97** — Compound swap sources, mutually exclusive choices, and dead swap controls (Session 42, index.html v5.54)
- **D98** — The parser writes compound swap sources in full (B23b data half) and stops inventing "additional" weapons (B29). Session 43, data-only
- **D99** — The equipment channel on the replacement side; B14b part 2 closes as already satisfied (S44, engine only, v5.55)
- **D100** — B30: compound single replacements, and the wargear allowlist on the whole replacement side (S45, data turn)
- **D101** — a wargear item can be the *source* of a swap, and base gear is now rolled up (S46, engine)
- **D102** — B28b: a wargear item is a first-class swap source, and gear-only groups now carry their gear (S47)
- **D103** — B14c(c) — bearer-gated adds. A gate may name more than one weapon; it is written the way every other multi-weapon field is written
- **D104** — A negated gate is a mutual exclusion, not a requirement. The parser must not read it as one
- **D105** — E17: when a conferred characteristic reaches the statline; B15 closed as never-real
- **D106** — a negated gate is a PER-MODEL exclusion, not a unit-level one. D104's remedy was wrong.
- **D107** — wargear is NOT free. And the false claim came from our own data, one turn after D106.
- **D108** — the base cost does NOT include default wargear. Settled from source, not from New Recruit.
- **D109** — D107's "138 priced entries" is wrong. The real numbers.
- **D110** — a wargear price is keyed by DATASHEET ID, never by unit name and never by item name.
- **D111** — an entry's cost is derived from its rollup, not from its option list, and it is recomputed on every render.
- **D112** — B15 shipped. The name-keyed glossary was the bug; carrier counting is the rule.
- **D113** — A bundle owns the swap it describes; the loadout def never restates it. (B36 — Lieutenant / Captain wargear.)
- **D114** — B41 + E3 — the datasheet limit becomes a hard block, and red comes to mean "exceeded"
- **D115** — The limits depend on the battle size. `Army_Muster_Rules.txt` arrived, and D114's numbers were wrong
- **D116** — B18's rule was backwards, and the source says so. A swap is NOT confined to its model group.
- **D117** — E14: a free, ungated, unpooled, one-off add defaults to selected. Narrow on purpose.
- **D118** — `loadout_parser.py` rebuilt to the committed file, and the freshness gate is now machine-enforced
- **D119** — the S57 parser did not survive into S58, and the rebuild is now reproducible from the log
- **D120** — B18 is two items, not one: `pool_id` is honoured only on `type: 'add'`
- **D121** — B43 is not a data gap; it is B44
- **D122** — B46: the popup's wargear-ability list is sourced from the datasheet, not from units.json
- **D123** — the parser-freshness guard is now executable and covers the whole pipeline
- **D124** — B47 — information buttons in the Configuration Panel. Engine only; `unit_loadouts.json` and `units.json` byte-identical
- **D125** — B48 — Corvus Blackstar `000000358` no longer renders two controls for the same wargear
- **D126** — B18b — `count` options now draw from the shared pool cap (`pool_id`)
- **D127** — B18c — capped generic swap fan-out: the ticket's uniform premise was wrong; re-scoped to two units, three deferred to new B18d, two are…
- **D128** — B18c stopped and banked at build time: S62's "provably exactly two units" premise was false, and seeding a cross-group pooled count exposes…
- **D129** — B18e shipped: the shared `pool_id` cap is now enforced on the weapon/points rollup for `count` options on fixed-1 groups, not just on the…
- **D130** — B39 diagnosis: Bloodthirster's doubled great-axe option is a stale duplicate flat swap, not a source-supported mutual-exclusion (fix is a pipeline dedup widen)
- **D131** — B39 fix shipped; B39b audit folded in clean; a units.json full-pipeline non-reproducibility finding banked as new custody item
- **D132** — P4 resolved: D131's diagnosis was wrong about the mechanism (not the symptom). Chaos Daemons IS reproducible — from the project root, never through wahapedia_transform.py. units.json re-established as a fixed point for all 14 blocks.
- **D133** — B40 closed as not-a-bug; Leader-section rework opened (B49); leader_footer added to the pipeline as the data half
- **D134** — B49 engine half shipped: dedicated Leader section rendered, generic Rules line dropped
- **D135** — B44 data half shipped: `loadout_groups` shared key added to statline model groups
- **D136** — B44 engine half shipped: `statGroupScopes()` now trusts `loadout_groups` when present, closing B44 and the Wolf Scouts undercount
- **D137** — B45 retired as a standalone ticket and re-homed into its real owners; SUPREME COMMANDER (must-be-Warlord) found silently dropped by the transform
- **D138** — off-by-one column-index bug in `wahapedia_transform.py` post-processing (found while scoping E9a, fixed same session)
- **D139** — E9a shipped: `must_be_warlord` surfaced for the 4 SUPREME COMMANDER units; a second, unrelated
- **D140** — E9b shipped: Warlord pick list wired into the Army List banner, plus a data addition E9b needed —
- **D141** — B1 audited before being scheduled: the reported symptom no longer reproduces; the real residual
- **D142** — B1b shipped: Chaos Daemons gets its own per-unit ability-text coverage; B52 and 3 truncated
- **D143** — B2 audited and closed (no reproduction); B38 re-scoped after inspecting the co-leader data on real data
- **D144** — B38 decision resolved (Ryan): support true multi-leader with full-set validation; model the generic shape with an explicit flag
- **D145** — B38-engine shipped: full-set symmetric-pairwise leader validation, zero behaviour change confirmed
- **D146** — B38a shipped: co_leader_eligible_with populated on the 12 built SM named-shape units
- **D147** — B38b shipped: co_leader_any populated on the 6 built DG generic-shape units
- **D148** — E10 shipped: duplicate unit in center panel
- **D149** — B18d shipped: capped generic swaps fanned to leader-conflict units (Thunderwolf Cavalry, Deathwatch Veterans, Talonstrike Kill Team)
- **D150** — B18f investigated and closed with no data change: five of six candidates are named-body-type (D116-correct, no under-grant); only Decimus Kill Team is a genuine generic under-grant, re-scoped to B18g
- **D151** — E13 shipped (label polish) and B18h shipped (D116 made executable as an assertion on the fan allowlist)
- **D152** — B18g investigated and banked: cc_1 is scoped to the wrong group; fan mechanism cannot fix it
- **D153** — B18g shipped: cc_1 scope corrected to Gravis Veterans via targeted post-processing override
- **D154** — E7/E8 shipped, then E5 shipped in a follow-on engine turn
- **D155** — B4 shipped: Primarch / Special / Fortification ability types routed alongside Datasheet
- **D156** — B37 closed on reconfirm: Captain wargear panes are already correctly fixed, no build needed
- **D157** — B7 reshaped: multi-leader mechanic already shipped in B38 cluster; residual work split into B7a (stack cap) and B7b (combined popup with aura markers)
- **D158** — B7a shipped: stack-size cap of 2 added to canAttachLeader
- **D159** — B7b shipped: combined attached-unit popup with per-stat aura markers
- **D158** — B13 Piece 1: Optional model toggle for Victrix Honour Guard (S92)
- **D159** — B13 Piece 2: Embedded Epic Hero cap for optional model groups (S93)
- **D160** — B34 Piece 1: Size-gated wargear swaps as `required_size` (data + parser) (S94)
- **D161** — B34 Piece 2: Size-gated wargear swaps enforced in engine (S95)
- **D162** — B53: combined attached-unit popup panel order flipped to leader-first (S96)
- **D163** — E15: Transport ability text added alongside the Transport keyword (S97)
- **D164** — B55: the four merged glossary lookups were stale; reproduction gate extended to cover them (S98)
- **D165** — B31: the Wulfen Dreadnought's "A or B and C" source, resolved as a bundle rather than a schema extension (S99)
- **D166** — the 81 unpriced units are a tracked gap, not an undiscovered one (S99)
- **D167** — B56 diagnosis: the chapter-points gap is four separate problems, not one (S100)
- **D171** — B56c shipped: chapter points override map derived fresh each build, stamped onto the generic units (S103)
- **D172** — B56d shipped: chapter point overrides applied at resolveUnits (S104)
- **D173** — B56g analysis: the Hunting Wolves escort is a model group, not wargear — direction (b) rejected (S105)
- **D174** — B56g phase 1 shipped: escort resolver keys the primary bracket on the primary count, Wolf Guard Headtakers closes (S106)
- **D175** — B56g phase 2 shipped: Hunting Wolves gains a per-bracket count and a price; new schema field, new HAND_AUTHORED entry (S107)
- **D176** — B56g phase 3 shipped: Hunting Wolves escort is reachable as a 0-or-N toggle; B56g closes (S108)
- **D177** — B11 shipped: SV/LD normalized to bare values at the pipeline source (S109)
- **D178** — B54 shipped: Be'Lakor's Shadow Form sub-abilities added to CD data (S110)
- **D179** — B21 diagnosis: the real blocker is banded optional model groups, not the mis-scoped options (S111)
- **D180** — B58 phase 1 shipped: base-group min lands on every banded unit, not just the four D179 kill teams (S112)
- **D181** — B58 phase 2 shipped: banded optional model groups become steppers, hard-capped by the base group's minimum (S113)
- **D182** — B59 mechanism, category distinction, and pricing correction; B21 shipped (S114)
- **D183** — B59a: non_consuming engine wiring, pure no-op on current data (S115)
- **D184** — B59b: MFM additive-line parser + Outrider Squad Invader ATV data flip; B59 closes (S116)
- **D185** — E2 shipped: collapsible left-panel role-group sections (S117)
- **D186** — B57 resolved: no in-between sizes; MFM discrete sizes only (S118)
- **D187** — E6 shipped: affordability dimming on left-panel units (S118)
- **D188** — E19 opened + shipped: Configured/Remaining points moved next to Army Points (S119)
- **D189** — E11 scope correction: full CSS-variable theme refactor, not a quick toggle (S119)
- **D190** — E11 closed: S120 visual verification pass, full changelog (S120)
- **D191** — S121 backlog housekeeping: B56e retired, E20 closed, E12 deferred, E1 formalized
- **D192** — E1 scoped: MFM is the 11th-Edition detachment source; E1 splits into E1a/E1b/E1c; E21 opened (S122)
- **D193** — E1a shipped: `detachments.json`, the Unique-tag finding, and a text ladder that self-corrects (S123)
- **D194** — `detachments.json` deduplicated: 1.61 MB to 797 KB, and three dead Wahapedia join tables identified (S123)
- **D195** — E1b shipped: detachment state, schema v2, and P3 brought back from the dead (S124)
- **D196** — E1c shipped: detachment picker over the E1b read path, and the second-implementation guard (S125)
- **D197** — Policy: no further extraction of code out of `index.html` without a positive reason (S126)
- **D198** — S126 tooling session: repo custody check, gate consolidation, known-failure allowlist, backlog/decision-log split
- **D199** — E4 scoped: enhancement assignment design, the name-collision finding, and eligibility by unit_type (S127)
- **D200** — E4b built: enhancement engine, schema v3, and a correction to D199's eligibility claim (S128)
- **D201** — E4c built: enhancement picker UI, roster chip; E4 fully shipped (S129)
- **D202** — B56 closed: verified against `units.json` directly, header had been stale (S129)
- **D203** — E21 scoped: construction effects are a data table, not a parser; E21 splits a/b/c/d and E22 opens (S130)
- **D204** — Ryan's rulings on D203's three calls; the Plague Legions leak (a live D0 violation); E21/E22 resequenced (S130)
- **D205** — Chaos Daemons source CSVs lost and rebuilt from shipped output; repo was never a backup for them (S131)
- **D206** — Soul Grinder god weapons never gated: `Allegiance_Condition` dead between CSV and converter; Ryan's one-weapon ruling (S131)
- **D207** — B63 shipped: Soul Grinder's god weapon gated at the converter, `units.json` re-banked, four assertions filed (S132)
- **D208** — B61 shipped: Plague Legions tagged at the parser via a known-label lookup, six-unit census pinned, four assertions filed (S133)
- **D209** — E21a shipped: `detachment_effects.json` authored + six assertions; E23 opened (Headhunter Task Force Tank Ace keyword grant) (S134)
- **D210** — The `/mnt/project` mount deduplicates by filename and is not evidence about presence, absence or duplication (S134)
- **D211** — Project-area capacity: the metric is tokens; S134's three options all wrong; built factions pin their sources permanently; P4 opened and the source census made executable (S134/S135)
- **D212** — E21b shipped: `effectiveUnitType()` across three call sites, chapter exclusivity made executable, two harness slices repaired (S135)
- **D213** — P4 step 1 measured: capacity responds to volume (94% → 92% on 174 KB), but JSON whitespace is not yet priced; a second cheap measurement inserted before minification (S135)
- **D214** — E21c/E22b shipped: forbid (Shadow Legion add + detachment-select refusal), allied unlock with battle-size points sub-cap and offer filter closing the live D0 leak, and the detachment-scoped Warlord ban (Tallyband Summoners); E22 closed; new harness `e21c_check.js`; one E21d residual recorded (stranded allied units after deselect) (S136)
- **D215** — E21d shipped: polished refusal prose, the picker's forbid gate made visible before the click (E1c-2 extended), the Battleline indicator; E21 closes. Three UI tickets from a screenshot review batched in: B64 (detachment detail moves to the shared modal), B65 (DP-budget refusal is no longer red — E3/D114's convention applied), B66 (config-panel eye icon → info icon, one shared renderer). Piece 3 (stranded-allied) deliberately not built — awaiting Ryan's confirmation (S137)
- **D216** — B62 shipped: `is_base_equipment` boolean fix (a real latent bug, not inert as D205 assumed) on Keeper of Secrets and Soul Grinder; `units.json` re-banked and verified to change only those two records; new `B62-1` presence-and-parse gate over the nine Gen-1 Chaos Daemons root CSVs (S138)
- **D217** — `BACKLOG_ARCHIVE.md` confirmed intentionally repo-only (not project-area resident); fetch-from-GitHub maintenance pattern established; pointer header in `OPEN_ITEMS_BACKLOG.md` now states this so a future session doesn't misread the mount (S138)
- **D218** — E21d piece 3 shipped, closing E21: a unit stranded by a later change — its unlocking detachment deselected/switched away, its allied group over the sub-cap after a battle-size drop, or a forbidden unit seated by import — reads as a visible roster error (`entryAlliedError`, wired into `entryHasError`), never silently trimmed or blocked. Ryan's ruling: a quick detachment switch-and-back must leave the list intact; same treatment generalises to enhancement over-states. New assertion E21d-1; `e21c_check.js` Section 8 drives all three branches on real data. `index.html` 6.8 → 6.9 (S139)
- **D219** — P4 step 2 shipped: `equipped_parser.py`'s terminal writer switched to compact separators; `unit_loadouts.json` regenerated 201,999 → 124,652 bytes (77,347 removed, matching D213's estimate); fixed point re-banked, manifest reissued. Percentage read and the step-3 decision rule wait on Ryan re-uploading to the project area (S140)
- **D220** — P4 step 3 cancelled: 77 KB of whitespace removal did not move the displayed percentage (92% before and after), so per D213's pre-set rule whitespace is near-free to the tokeniser. `wh40k_core_rules.md` (139 KB, GW text, unreferenced by any script) removed from the project area as the next lever — verified safe by static scan and park-and-rerun (23/23), delivered to Ryan for local backup, pending his deletion and a fresh percentage read (S141)
- **D221** — B60 closed: `detachment_parser.py` now routes every detachment's chapter-exclusivity restriction to `restrictions`, consistently. Two root causes fixed — the Wahapedia tier folded the restriction into `rule_text` in two shapes (separate "Restrictions" ability row + embedded `hi_custom` RESTRICTIONS section), and the DA pack bled stratagem clauses into two records' restrictions where page-collated CP tokens defeated stratagem recognition. `restrictions` now populated for all 25 chapter-exclusive detachments, zero left in `rule_text`, no stratagem/CP debris; 16 records changed, restrictions/rule_text only. Consistency not yet pinned as an assertion (data-only turn) — filed as B60a. Data-only; `detachments.json` re-banked, manifest reissued (S142)
- **D222** — B60a shipped: two new assertions pin D221's chapter-exclusivity shape as an executable fact (25 in `restrictions`, 0 in `rule_text`, no stratagem/CP debris); 104/104 assertions pass. Tooling-only (S143)
- **D223** — Repo custody audit: `repo_check.py` pulled from the reachable repo and run for real. CRITICAL — `Unit_Weapons.csv` and `wh40k_core_rules.md` found committed to the public repo (single-commit history, today's bulk upload); flagged to Ryan as B67, amend-and-force-push recommended. Also corrects D221/S142's claim that `detachments.json` is "not repo-eligible" — contradicted by `pipeline_manifest.json`'s guarded set, `repo_check.py`'s own `.gitignore`-driven detection, the file's actual byte-matching presence in the repo, and the live site's hard dependency on it; `detachments.json` stays repo-eligible (S143)
- **D224** — `Space_Marines_web.txt`'s stratagem-section removal (11,364 → 7,906 lines, Ryan's edit) verified safe against source and mechanically (`repro_check.py` byte-identical, 104/104 assertions, 23/23 gates) — stratagems were never read by any parser, confirming Ryan's belief. `Chaos_Space_Marines_web.txt` supplied (8,337 lines, 58 UNIT COMPOSITION anchors, structurally consistent) — CSM's build blocker cleared, ready for its own scoped data-build turn (S144)
- **D225** — Baseline reconciliation: B67's "single commit" premise corrected (249 commits, not one; both GW-derived files removed from HEAD, confirmed via the API; full history purge remains optional, filed as B67b). Dark Angels replacement and new Space Wolves file verified against the real pipeline — every difference traced to a known cause, including one genuine pre-existing Dark Angels bug (Ravenwing Dark Talon's missing second Hurricane bolter) confirmed against source and now fixed. `Space_Marines_web.txt`'s further edit re-verified clean. `unit_loadouts.json` regenerated and re-banked — 23/23 gates, 104/104 assertions (S145)
- **D226** — Process rule: before starting a Black Templars/Death Guard/Space Marines `_web.txt` regeneration turn, Claude pauses, asks Ryan to load that faction's new file, and waits — doesn't assume it's ready (S145)
- **D227** — Chaos Space Marines build scoped: 58 units, 17 detachments, four cross-sourced cult-troop prices (S146)
- **D228** — Prose-less current-edition detachments: build them selectable, prose-incomplete — recommendation, awaiting Ryan (S146)
- **D229** — CSM turn A shipped: 54 self-priced units built (four cult-troop units deliberately withheld), `units_repro_check.py` updated, `datasheet_wargear_abilities.json` scope gap closed, E4B_KEYWORD_GAPS extended for three Character-typed units, manifest reissued (S147)
- **D230** — B68 opened: `loadout_parser.py`/`equipped_parser.py` resolve by unit name not army+unit_id; Death Guard/CSM's seven shared generic Chaos vehicle names bleed across factions; deferred to a dedicated parser turn, `unit_loadouts.json` and `repro_check.py` left untouched (S147)

- **D231** — P4 scoped as a target architecture: area = per-session working set, public repo fetched as one tarball, new private repo `rd-prime-1357/data-sources` for the 71 GW source files fetched with a read-only token stored in-area and hard-guarded out of the public repo; gates tiered A/B; migration M0–M3 sequenced (M0 next). Ryan's custody calls settled — accept-risk for pre-release (revisit at public launch), private repo over zip, token in area (S148)
- **D232** — M0 built and proven: `pipeline_manifest.py` extended 41→101 (full public-repo coverage, self-guard fixed); `baseline.sh` gained `--fetch`/`--data-turn` (tarball fetch-verify-overlay, token/zip source fetch, loud refusal with neither); `rules_assertions.py` gained `--tier a`, auto-classified from reachable code (names + GW filename constants) rather than hand-tagged, catching two real gaps (three source-opening assertions missed by a first pass; a legitimate new census reference) via sources-absent simulation; `repo_check.py` gained the `SOURCE_REPO_TOKEN.txt` custody guard; `source_manifest.json` created and confirmed against Ryan's real file-list screenshots at 70 entries (an initial screenshot pass misread three files as absent; re-checked and corrected same-day). Exit test proven correct by simulation; literal live-green `--fetch` blocked until tonight's push, a structural one-session gap not a bug (S149)
- **D233** — `--fetch` confirmed live-green against the real public repo: the live `pipeline_manifest.py` carries the 101-file guarded set, and a fresh tarball fetch-verify against it fails only one file, `40K_Data_Pipeline_Process_v0_6.md` — hash-confirmed as the exact pre-existing area-ahead-of-repo drift D232 already named, not a new regression. M1 (Ryan, no session) is now unblocked. Also found and reconciled: `NEXT_SESSION_PROMPT.md` had gone stale (still S149's opening prompt, never overwritten at close) — rewritten for S151. Tooling-only, verification only (S150)
- **D234** — M1 confirmed already run (27 repo-resident guarded files absent from the area, matching the S151 prompt's own anticipation). Found and fixed a real M0 design gap: the fetch-open's verify step checked the *entire* fetched tree unconditionally, so any single mismatched file — including ordinary area-ahead-of-repo drift on a file that wasn't part of the overlay — blocked recovering every evicted file, contradicting the "area copy wins" authority rule. `pipeline_manifest.py` gained `check_overlay()`/`--overlay-check`, scoping verification to only the guarded files absent locally; `baseline.sh` wired to it. Closed a manifest gap along the way — `SESSION_HANDOFF_149.md`/`.150.md` were never appended to `GUARDED` (S149 missed its own append step); added, plus `.151.md`. Manifest regenerated, 104 guarded files. Full baseline clean except the carried-forward B68 failure and three known push-pending files. Tooling-only (S151)
- **D235** — B68 closed: the seven-unit repro divergence (carried since S147) fixed in `equipped_parser.py` alone. Flat `name2id` (name → unit_id, last-write-wins) misrouted Death Guard's seven shared generic Chaos vehicle equipped lines to their CSM twins once both factions co-existed in `units.json`. New `scoped_name2id()` infers the owning faction from the composition filename and prefers the in-scope block candidate for colliding names; single-candidate/unscoped passes unchanged. No caller edit — pure engine turn. Repro byte-identical, no data regenerated; durable for the future CSM web pass. `loadout_parser.py` untouched (unit_id-keyed; its `ds_by_name` is dead) (S152)
- **D236** — CSM turn B shipped: loadout defaults built (CSM added to `repro_check.py`'s `FACTIONS`/`WEB_PASSES`; `unit_loadouts.json` regenerated, +54 CSM entries, 0 changed/removed). Surfaced and closed a second gap: `wargear_points.json` had silently never picked up CSM's MFM wargear (gated on a loadout entry existing, which CSM lacked until now) — regenerated with the canonical generic-before-chapter MFM file order, +2 entries (`000000967`, `000000969`), 0 changed. `rules_assertions.py`'s E14-2 hardcoded count updated 53/33 → 64/44 (CSM's 11 own free-seeded adds, spot-checked). `detachment_parser.py`/`detachments_repro_check.py` deliberately left untouched — no same-session regeneration to verify them against; deferred to CSM turn C. 23/23 gates green. Data-only (S153)
- **D237** — CSM turn C shipped, closing the CSM detachment build: `detachment_parser.py` gained CSM's three config lines (`ARMY_TO_MFM`, `MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`), `detachments_repro_check.py` gained the CSM MFM file in its required-inputs list. `detachments.json` regenerated: +17 CSM detachments (160 total, 14→15 armies), 0 existing records changed, 0 removed — diff-traced key-by-key against the committed file, confirmed CSM-only. The two MFM-only detachments (Devotees of Destruction, Murdertalon Raiders) came through with no rule prose as scoped (D192/§3); the other 15 sourced from Wahapedia tier-2 prose, no faction pack existing for CSM. `detachments_repro_check.py` reproduces byte-for-byte. Surfaced two real gaps for the tooling turn: (1) E4b-3's same-army enhancement-collision census moved 29→30 (6 distinct names, was 5) — CSM's own enhancements introduced one new same-army collision, the literal needs updating, not the rule; (2) E21a-5's coverage check now fails — CSM's Chaos Cult detachment grants TRAITOR GUARDSMEN SQUAD units the BATTLELINE keyword, a real construction effect with no row yet in `detachment_effects.json` — filed as new ticket B74. Also found: `40K_Decision_Log_v3_0.md` is absent from the mounted project area and `D231_entry.md`–`D234_entry.md` are still present there, the reverse of what S153 closed with — read as mount staleness (the area mount is a point-in-time snapshot per standing constraint, not evidence of the repo's real state) rather than a real regression, but flagged for Ryan to confirm with a fresh upload if the log is genuinely missing. This entry banked as standalone `D237_entry.md` (the same fallback pattern S153 retired, revived because the log wasn't reachable this session) pending confirmation. Data-only throughout — no engine logic change beyond the config lines; `index.html` untouched, matching CSM_BUILD_SCOPE.md §6's expectation (S154)
- **D238** — CSM tooling turn shipped, per `CSM_BUILD_SCOPE.md` §8 step 4: three new assertions (`CSM-1` roster count 54/58, recorded honestly rather than rounded up; `CSM-2` detachment count 17; `CSM-3` the two MFM-only detachments' `text_source: none` pinned as documented shape, not a gap). `E4b-3`'s pinned collision census re-derived fresh from `detachments.json` rather than assumed from D237's handoff prose — confirmed 30 pairs / 6 names / 1 differing-price, the sixth colliding name is CSM-internal (Warp-Fuelled Thrusters), the differing-price collision is unrelated to CSM (Dark Angels/Deathwing Assault, unchanged). Literal and docstring updated in both the assertion statement and the function body. `pipeline_manifest.py --write` reissued (105 guarded files). Full `baseline.sh --no-repo` pass: 22/23 gates green, the sole failure is `rules_assertions.py`'s `E21a-5` (B74 — Chaos Cult's BATTLELINE grant has no `detachment_effects.json` row), correctly failing by design and explicitly out of scope this session per the S155 prompt. B74 remains open, filed for its own small data turn next. `40K_Decision_Log_v3_0.md` is still absent from the mounted project area this session (third session running); this entry banked standalone again pending Ryan's confirmation of the log file's real status. Tooling-only: no engine logic changed, `index.html` untouched, no data file regenerated (S155)
- **D239** — B74 shipped: `detachment_effects.json` gained a `battleline`-kind row for `Chaos Space Marines|CHAOS CULT` elevating Traitor Guardsmen Squad, matching the five existing rows' shape; `e21b_check.js`'s pinned full-table count updated 4→5 alongside it. Closes the CSM tooling arc (`CSM_BUILD_SCOPE.md` §8) in full. Baseline reconciliation before B74: confirmed via a live clone of the public repo that the decision log and all guarded files are intact there — the mount's absences are pruning under 96% area capacity, not repo drift, closing the three-session D237/D238 flag without asking Ryan. Also found and fixed a real bug: `pipeline_manifest.json`'s stored hashes for `DECISION_INDEX.md` and `OPEN_ITEMS_BACKLOG.md` were stale versus both files' actual (repo-matching) content — S155's manifest write ran before those two files reached their final edited state and was never repeated; undetected since because no session had the full guarded-file set to check against. Reissued clean, no content lost. D237 and D238 folded into the main log from their standalone files (D231–D234 were already folded at S153 but their standalone files were never deleted, which is why they kept resurfacing); all six now-redundant `D2NN_entry.md` files deleted. 23/23 gates, 107/107 assertions, data-only, `index.html` untouched (S156)
- **D240** — CSM cult-troop cross-file points shipped, closing the roster gap 58/58: the four
  units unpriced in CSM's own MFM (Khorne Berzerkers, Plague Marines, Rubric Marines, Noise
  Marines) each priced via `mfm_points_parser.py --scope-to-army --append` against their own
  god-legion's MFM (World Eaters, Death Guard, Thousand Sons, Emperor's Children). New
  `_scope_stats_csv()` isolates each call to a single-row stats input, since the full 58-row CSM
  block would let several already-priced generic Chaos vehicles (Chaos Rhino, Helbrute, Defiler,
  etc. — separately priced in the same legion MFMs) resolve in scope and get silently overridden.
  Verified empirically: each of the four calls added exactly one row. Checked source directly:
  none of the four units carry separately-priced wargear anywhere, so `wargear_points.json` needed
  no new entries. `units.json` +4 (328 total, 0 changed/removed elsewhere), `unit_loadouts.json` +4
  (additive, re-derived from source). `CSM-1` updated to a clean 58/58 pass; `E14-2`'s literal
  64/44 → 65/45 (Khorne Berzerkers' Icon of Khorne, the only qualifying free add among the four).
  Manifest reissued twice, 108 guarded files. 20/20 gates, 70/70 assertions, data-only, `index.html`
  untouched. Closes `CSM_BUILD_SCOPE.md` §4 — CSM's build is complete except for M2 (S157)
- **D241** — Thousand Sons build scoped (S158, tooling/scoping-only): `THOUSAND_SONS_BUILD_SCOPE.md`
  written. 34 current-edition units (60 raw, 26 Legends-FW), no new selection mechanism needed, 9
  current detachments via the same D192 MFM-authoritative pattern as CSM. Reciprocal cross-file
  points gap checked and comes back clean — TS is fully self-sourced, 34/34. One real blocking gap:
  no `Thousand_Sons_web.txt` exists for loadout defaults, needs Ryan to source it. Also fixed a real
  B15-9 drift at baseline open: S157 added 4 units to `units.json` without regenerating
  `datasheet_wargear_abilities.json`; reran the parser, +3 entries, additive only (S158)
- **D242** — M2 dress rehearsal shipped: Ryan's private sources repo and read-only token verified
  live against the GitHub API — full fetch, unpack, and byte-compare of all 70 files against
  `source_manifest.json` passed clean (0 missing, 0 mismatches). Found and fixed a real bug:
  `baseline.sh`'s private-source fetch URL was hardcoded to a nonexistent repo name
  (`rd-prime-1357/data-sources` instead of the actual `rd-prime-1357/rd-prime-1357-data-sources`) —
  would have silently broken every future data-turn fetch. `SOURCE_REPO_TOKEN.txt` written and handed
  to Ryan to upload. Deletion from the area deliberately not done this session — that's Ryan's
  screenshot-verified step, per the standing M2 procedure (S158)
- **D243** — Project-area GW-source reconciliation closed; S158's repo batch was simply unpushed (S159)
- **D244** — `faction_pack_transform.py` (NET NEW): GW faction pack PDF → markdown, with a known limitation on portrait Rules Updates pages (S159)
- **D245** — Thousand Sons turn A deferred; correcting a wrong reading of `allied_group` (S159)
- **D246** — Rolling documents drop version numbers from their filenames (S159)
- **D247** — Duplicate ticket ID: open B61 renumbered to B80 (S159)
- **D248** — Thousand Sons has nine detachments, not seven; D245 regressed a count D241 already had right (S160)
- **D249** — Manifest custody gap from S158/S159 reconciled at S160 open (S160)
- **D250** — Thousand Sons turn A shipped: 34 units banked, closing E24 and B78; B61's four census assertions generalised to cover Death Guard and Thousand Sons (S161)
- **D251** — Force Disposition selection designed and filed as E25 (data already retained 169/169; engine-only work); S161 handoff manifest-ordering drift reconciled (S162)
- **D252** — Thousand Sons turn B shipped: loadout defaults banked (34 new entries, additive-only); TS Defiler wargear gap fixed (same class as D236's CSM finding); E14-2's stale count corrected 65/45 -> 75/54 (S163)
- **D253** — Thousand Sons tooling turn shipped: TS-3 roster census (34 units) added to `rules_assertions.py`, mirroring CSM-1; closes the Thousand Sons build (S164)
- **D254** — E25 shipped: Force Disposition selection — derivation, auto-select, invalidation, persistence, and the Army List output line; `e25_check.js` added (S165)
- **D255** — B71 shipped: config-panel expanders now survive a re-render — `mkDetail` keyed by stable id instead of a render-order counter, `openDetailIds` persists open state; `b71_check.js` added (S166)
- **D256** — Session-open reconciliation: manifest hashes for the decision log and prior session's
  handoff were stale versus their (repo-matching) real content — same defect class as D239, third
  occurrence; filed B81 (S167)
- **D257** — B81 shipped: `pipeline_manifest.py --freshness-check`, a close-time gate that re-hashes
  the decision log and latest handoff against the manifest, run last after `--write` (S168)
- **D258** — B72 and B80 shipped (engine-only): B72 — `loOptMax` now exempts `non_consuming` optional
  groups from the headroom clamp, so the Outrider Squad's Invader ATV is offered at every legal size,
  not only 6; B80 — combined-popup section IDs scoped per member via a new `idScope`, so the bodyguard's
  chevron no longer toggles the leader's section; `b72_check.js` added; `index.html` v6.12 (S169)
- **D259** — B69 corrected (Ryan: remove the "(see left)" cue and nest granted abilities under their
  selector, not rewrite to "(see below)") and generalized: same select-N-from-pool shape on six units
  across four factions; the selector→pool link is absent from our data, so it's a data turn (parser
  re-capture, asserted) + an engine turn, re-sized S→M; no hardcode shipped, B69 re-scoped not built (S169)
- **D260** — B70/B73 audit complete: root cause is `mfm_points_parser.py`'s LEADER/SUPPORT-blind backfill;
  B70 not-a-bug (Wardens has no Leader ability in any source), B73 confirmed systemic across 13 characters;
  source-of-truth decision needed from Ryan; no code/data shipped (S170)
- **D261** — B77 audited and closed as already-resolved: the six Scintillating Legions carriers already
  carry the faction keyword in `units.json` and it already renders in the UI; ticket's S159 diagnosis was
  stale, not something this session fixed; closed on standing authority, no code/data shipped (S171)
- **D262** — Faction pack converter sized against all 11 packs (635 pages): B75 is 64 flagged pages,
  ~10x its estimate, and its claim that only Rules Updates pages fail is false (detachment pages fail
  too); filed B84 (note names wrong page type), B85 (faction-keyword detector reports ~1 false
  positive per datasheet, drowning the real notes), B86 (image-only page needs OCR); converter's
  install message fixed for Windows; recorded that this conversation opened against a 12-session-stale
  project area (S172)
- **D263** — B84 shipped (converter's KNOWN LIMITATION note no longer names a page type it doesn't
  own); B75/B85 found blocked on real PDF access rather than judgment — no PDFs reachable from this
  environment, a synthetic test of B85's reported bleed pattern didn't reproduce it, so a diagnostic
  was added instead of a guessed fix; manifest gap from S172 (never reissued, guarded set missing
  `SESSION_HANDOFF_172.md`) reconciled at open (S173)
- **D264** — Manifest hash for `SESSION_HANDOFF_172.md` didn't match the actual repo file (verified
  two ways); only entry affected across all 128 guarded files; manifest regenerated against a
  verified repo clone, corrected copy delivered for Ryan to push (S174)
- **D265** — B76 shipped: five versioned docs renamed to drop frozen version suffixes, content
  unchanged; live scripts and live cross-references updated, historical text left untouched (S174)
- **D266** — B70: Ryan approved building the join/Starting-Strength mechanic (new scope, sizing TBD).
  B73: Ryan chose MFM as authoritative wherever both exist; re-deriving from source found D260's
  LEADER/SUPPORT mechanism description didn't match the actual code — the parser has no `LEADER`
  handling at all today, only `SUPPORT`, so the real fix needs a new collection path before any
  override logic, not a one-line change; also surfaces that Wardens' `SUPPORT` list is currently
  mislabeled as leader data, which the B73 fix and B70's build both touch (S175)

- **D267** (S176, data-only) — B73 shipped. MFM made source of truth for attach eligibility. Two
  corrections against source before building: Support is the same attach mechanic as Leader (core
  rules 19.01/24.22/24.34), not B70's join mechanic; and the engine gates attachment on the eligible
  list alone (index.html 4676), never the ability name — so both lists stay in one field, distinction
  recorded in `leader_ability_name`, reversing the S175 "separate field" plan (confirmed with Ryan).
  `mfm_points_parser.py` rewritten (LEADER + SUPPORT captured one line each, MFM replaces stale
  Wahapedia, unresolved entries dropped, D260 over-read fixed); `units.json` regenerated, diff clean
  (43 units, only leader_eligible_units/leader_ability_name/leader_footer). Ancient/Apothecary/
  Lieutenant → Support; Epic Heroes narrowed to MFM lists; Wardens carved out (MFM 6 vs datasheet 3
  — Heroes of Ultramar, B70). Assertion B73 added (111 total). Stipulations → E26 (stacking
  enforcement + exceptions) and E27 (popup/output wording). Open 12 → 13.

- **D268** — E26 re-scoped from source (S177, analysis-only). CSM "data gap" investigated to source and
  found not to exist: the live engine's `permitsCoLeader` (index.html 4271) returns false for a bare
  Support against every Leader — that is the real defect, and it is engine, not data. MoE type is
  governed by D192+D267 (MFM wins → Support), not a new call; its footer was correctly cleared by B73;
  the only two CSM co-attach footers are MoE and the unbuilt Exalted Champion, so no CSM data change
  exists and the deferred D144 CSM `co_leader_any` population resolves as unnecessary. Three of my own
  proposals corrected against source (discard name lists; add MotM to Huron; set `co_leader_any` on
  MoE — all wrong). E26 re-scoped **engine-only, no data dependency**: Support pairs with any Leader;
  keep DG second-Leader path; read a Leader's `leader_eligible_units` naming a character as a permit
  (Huron→MotM, sole cross-reference in 16 factions); same-type cap blocks two Supports. Open 13 → 13.
- **D269** — E26 shipped (S178, engine-only). `permitsCoLeader` rewritten with four D268 requirements:
  bare CHARACTER Support pairs with any Leader (R1); DG `co_leader_any` second-Leader path kept (R2);
  Leader cross-reference for non-CHARACTER Support — Huron→MotM only (R3); same-type cap (R4).
  `leaderAbilityName` added to allUnits view. Assertion E26 added (10 cases + symmetry, 9 shape
  fragments). `index.html` v6.12 → v6.13. Open 13 → 12.
- **D270** — E27 shipped (S179, UI-only). `renderDetail` attach-panel heading/hint and
  `leaderSectionHtml`'s modal heading now read `leaderAbilityName`/`leader_ability_name` instead of a
  hardcoded "Leader" string. List-panel row and JSON export checked and found to need no change (no
  role word present at either). Rules-section dedup filter left keyed on the literal string 'Leader'
  by design — datasheet ability box is always literally "Leader" (129/131 model groups); the
  Leader/Support split comes from the MFM's own block headers, a different document. Assertion E27
  added (structural shape only). `index.html` v6.13 → v6.14. Open 12 → 11.
- **D271** — GUARDED-list close-out fix; not a ticket (S180, tooling-only). `pipeline_manifest.py`'s
  `GUARDED` list had fallen 3 handoffs behind (`177`-`179` never appended, silently unguarded).
  Re-added the three; also added `unguarded_handoffs()`, folded into `check()` and `check_overlay()`
  (checked against the full fetched repo tree, not local dir — local housekeeping deletes old
  handoffs, so only the repo copy reliably still has them) so a forgotten append now fails the very
  next baseline instead of going silent for sessions. Verified against the real fetched repo that this
  would have caught S177-179 immediately. Rejected switching `GUARDED` to `latest_handoff()`-style
  auto-discovery — it can find files but never notice one missing, trading away real detection.
  Backfilled `BACKLOG_ARCHIVE.md` full entries for B73 (S176) and E26 (S178), previously missing.
  Open count unchanged at 11 (no ticket).
- **D272** — E23 scoped from source (S181, analysis-only). Corrected the S181 prompt's "sixth effect
  kind" claim — the schema has four kinds in use today (`battleline`, `forbid`, `unlock`, `warlord`);
  Headhunter Task Force's grant would be the fifth, not sixth. Key finding: E9's `isCharacter` is
  computed once per unique unit name (shared across every copy), and E4 reads the raw `unit_type`
  field directly at six construction sites, never through `effectiveUnitType()`; Tank Ace's up-to-three
  player-picked-instance grant fits neither shape, so this needs new per-entry logic in both, not a
  pure data change. No overlap risk found — no Vehicle-type unit in the generic Adeptus Astartes block
  is already `unit_type: Character`. **Mechanism decided:** a new declarative effect kind for the
  detachment-scoped facts (eligible set, count cap), plus a purely-additive `list_store.js` array field
  for the player's picks (no version bump, same pattern as `warlord_entry_id`/`force_disposition`).
  **Revalidation decided:** continuous silent drop, identical to `recomputeWarlord()`; no Muster phase
  exists in the app to gate against. Both sub-questions the S181 prompt flagged as possibly
  Ryan-facing resolved by existing precedent, not escalated. Still blocked on a data turn (not run this
  session) to confirm exact wording/cap across all six armies. No ticket shipped; E23 re-scoped in
  place. Open count unchanged at 11.
- **D273** — E23 data-turn: `HEADHUNTER TASK FORCE` source facts confirmed across all six armies (S182,
  data-only — no engine, no data-file, no `index.html` change; baseline 29/29 with GW sources loaded).
  **All four facts confirmed; D209/D272's "most Vehicles" corrected to a precise predicate.** (1) Grant
  wording identical across all six because it is one Space Marines detachment — verbatim only in the SM
  Faction Pack and Wahapedia `Detachment_abilities.csv` (`faction_id=SM`), byte-identical `rule_text`
  in all six `detachments.json` records. (2) Tank Ace = Adeptus Astartes Vehicle *excluding
  Fortifications, Drop Pods, Walkers and units that can Fly* — a keyword/type predicate computable from
  built `keyword_names`+`unit_type`, not a name list. (3) "Up to three" cap identical in all six. (4)
  Keys `<Army>|HEADHUNTER TASK FORCE`, `dp:2`, PRIORITY ASSETS, all six. **Per-army eligible pool
  resolved from source: SM 16, BT 16, Blood Angels 17 (adds Baal Predator), DA 16, DW 16, SW 16 — Blood
  Angels is the only one that is not 16.** Generic AA block: 28 Vehicle-type → 16 eligible, 12 carved
  out (5 Walkers, 6 Fly, Drop Pod). No eligible unit is already Character/Epic Hero in any pool.
  **Build-turn notes:** base the test on the Vehicle *keyword* (so the Fortification clause catches
  Hammerfall Bunker, its only Adeptus Astartes case); encode the carve-out as a per-entry exclusion
  predicate, not a per-detachment name list; add an assertion that no non-Adeptus-Astartes vehicle can
  enter these pools (the faction qualifier is satisfied by pool construction today, not a keyword
  check). E23's data dependency cleared; backlog text updated. Open count unchanged at 11.
- **D274** — MFM v1.1 intake (S183, doc-only; `index.html` stays v6.14; baseline 29/29). 15 v1.1
  captures banked in the private repo (all built armies + Emperor's Children + four extra); SM repo
  copy text-identical to the reviewed sample; chapters confirmed inside the SM page. **Current parser
  cannot read the v1.1 layout** — 0 costs, 25 unit names missed on SM v1.1 vs 179/179 on v1_0.
  Intake policy set: GW version number in filenames (underscore; rename of the dot-named uploads is a
  Ryan action), keep every version, capture only bumped built factions + next build, per-faction MFM
  version recorded in `source_manifest.json`, one parser with per-file format sniff, refresh arc
  ahead of E23 (D273 pool counts re-verified post-adoption). Tickets opened: B87 (parser tooling),
  B88 (reconciliation), B89 (adoption). Open count 11 → 14.
- **D275** — MFM filename convention: dot separator, spaces allowed (S183, Ryan call). Filenames
  use dots for the GW version (`v1.1`) and natural spacing (`Chaos Daemons`), matching Ryan's local
  naming. Parser and manifest accept as-uploaded — no rename step. Old v1_0 files keep their
  underscore names. Open count unchanged at 14.
- **D276** — SM-family chapter rosters are two tiers, not one union (S184, Ryan-flagged, refines
  D42). Six vanilla chapters (no dedicated MFM) correctly union generic + chapter entries. Five
  dedicated-MFM chapters (Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves) are
  complete self-contained rosters and must never union with generic — confirmed against
  `MFM_Black_Templars_v1.1.txt` (76 units, no union). Current `resolveUnits()` unions unconditionally,
  leaking 90 illegal units into Black Templars alone (all Librarians, 11 other-chapter characters) —
  a live D0 violation across all five. B90 opened: engine `roster_mode` flag, five-chapter rebuild
  from own MFM files, new exclusivity assertion. Open count 14 → 15.
- **D277** — B90 turn 1 shipped: `resolveUnits()` two-tier mechanism + `roster_mode` taxonomy flag
  (S185, engine turn). All eleven SM-family chapters flagged `'union'` this turn; the five Tier-2
  chapters flip to `'complete'` in the B90 data turn, not now — because their `units.json` blocks are
  source-verified **deltas** (BT 18, BA 15, DA 16, DW 10, SW 21), not baked unions, so flagging them
  `'complete'` now would strip the generic units they legitimately field. Live behavior unchanged
  (still union-leaked, unregressed) until the data turn. Mechanism proven via `b90_check.js` fixture;
  presence pinned by `rules_assertions.py` B90-1. Also flagged two decision-log integrity gaps (guard
  points at stale `40K_Decision_Log.md`; live `_v3_0` unguarded and diverged) → opened B91. Corrects
  the S185 prompt's data-shape assumption; build-sequencing refinement of D276, no legality change.
  Open count 15 → 16.
- **D278** — S186 open reconciliation: `faction_taxonomy.json` re-serialised to canonical
  no-trailing-newline form, restoring `units_repro_check` to green (S186, data turn). S185's
  engine-turn hand-edit left a stray trailing newline; that turn ran tier-A-only and skipped
  the repro gates, so it shipped uncaught until this data turn loaded sources. Content
  unchanged (5643→5642 bytes). Lesson: merge-passthrough JSON must go through the serialiser,
  never hand-saved. No ticket (opened+closed same turn). Open count unchanged at 16.
- **D279** — B90 turn 2 deferred: the Tier-2 complete-roster rebuild is a pipeline build
  (no existing path emits a full per-chapter roster; today they are deltas + runtime union),
  and its target is blocked on two source questions (S186, data turn). Source confirms D276's
  legality model (BT lists 0 Librarians; chapter rosters genuinely differ), but (a) the
  pipeline pins **v1_0** MFMs while unadopted **v1.1** files carry corrected points — the tool
  ships stale points; adopting v1.1 is a faction-wide refresh → opened **B92**; and (b) direct
  source count is **BT=90**, not the **76** D276/the prompt state — the acceptance figure is
  contradicted by source and must be corrected before any assertion pins it. Both decisions are
  points-legality precedent → Ryan. Reconciliation (D278) banked; B90 stays open. Open count
  16 → 17 (B92 added).
- **D280** — E23 data turn: `detachment_effects.json` gains a fifth kind (`tank_ace`) and six
  rows for the HEADHUNTER TASK FORCE Tank Ace grant (S187, data-only). D273's facts re-derived
  from source, not trusted; caught and fixed a real bug first (the generic key's `army` field
  was set to the unresolvable label `Space Marines` instead of its true seven owning armies —
  `Adeptus Astartes` + six vanilla chapters — via a new `_owning_armies()` helper). Two new
  assertions (`E23-1` coverage, `E23-2` pool counts), `E21a-3`/`E21a-4` extended for the new
  kind. `rules_assertions.py` 114/114 → 116/116. All rows `enforced: false` — E23's engine turn
  (list_store.js pick state, index.html eligibility hooks) not attempted, ticket stays open.
  `index.html` unchanged (v6.15). Open count unchanged at 17.
- **D281** — Two tickets opened from Ryan-reported gaps (S188, doc-only): **E28** — move selected
  Detachments/Force Disposition from the always-on centre-list widget to a right-panel
  click-to-configure view, matching the unit mechanic (recommended with one adjustment: Force
  Disposition attaches to the Detachments group, not each row, since it's one value for the whole
  selection). **B93** — `enhancementTypeEligible()` checks Character-vs-not only, never the
  Enhancement's own qualification text; Upgrades get zero type check today (live gap), regular
  Enhancements over-admit past their named keyword/unit. Sampling found the qualification clause
  isn't reliably the description's first sentence as reported, and two records (Thousand Sons'
  Stave Abominus, Chaos Daemons' Leaping Shadows) have no usable qualification text yet — a source
  pass across all 607 records is needed before either is built. Open count 17 → 19.
- **D282** — B91 resolved: `40K_Decision_Log.md` and the stray `40K_Decision_Log_v3_0.md` merged
  into one canonical file (byte-diffed first — D264–D275 only in the guarded copy, D276–D281 only
  in the versioned copy, D276 relocated from its out-of-order position beside D42 to its correct
  place after D275; every D-number 0–281 confirmed present exactly once). The four other
  version-suffixed doc pairs from D265's incomplete rename (`40K_Architecture_Overview_v0_5.md`,
  `40K_Data_Dictionary_v2_0.md`, `40K_Data_Pipeline_Process_v0_6.md`,
  `40K_Functional_Spec_v0_7.md`) confirmed byte-identical to their renamed counterparts and safe to
  delete outright. B90's roster mechanism confirmed against `MFM_Black_Templars_v1.1.txt` directly
  (no Librarian entry at all — not an unoverridden generic unit), matching B90 turn 2's existing
  native-rebuild plan. B92 closed as a duplicate of D274's already-decided MFM-edition policy;
  B87→B88→B89 is the real execution path, now confirmed unblocked. Open count 19 → 17
  (B91, B92 closed).
- **D283** — B87 shipped: `mfm_points_parser.py` reads the MFM v1.1 layout via a per-file sniff +
  normalization pass (all 15 v1.1 files cost fully, v1_0 output unchanged except two corrected units).
  A shipped Rubric Marines overcharge (CSM + TS, 110/200 → correct 100/190 for the 1st-to-3rd copies)
  found and fixed in-flight; the `1st-to-3rd/4th+` tier shape now has a reader, the 4th+ tier captured
  for B94. B90's Legends/Forge-World roster question answered (yes — a chapter's own MFM prices them
  legal). v1.1 detachment parsing rescoped to B88. Net-new `b87_check.js`. B87 closed, B94 opened,
  open count unchanged at 17.
- **D284** — B88 shipped: `detachment_parser.py` reads the MFM v1.1 DETACHMENTS layout via the same
  sniff + normalization pattern B87 used for the points file (all 15 v1.1 files parse cleanly, 0
  before; v1_0 output byte-identical on all 10 live-army files). Two quirks handled beyond B87's
  precedent: a bare trailing marker on a DP line with no delta (Thousand Sons' Hexwarp Thrallband,
  2DP→3DP) and a third editorial note string (`UNIQUE TAG REMOVED`, World Eaters). Net-new
  `b88_check.js`. `mfm_reconcile.py` generalized from the old one-off SM pass into a per-faction delta
  tool across the 10 built-army MFM file pairs — points, roster, wargear, attach lists/Leader-Support
  flips, and detachment deltas, each classified adopt-mechanically vs investigate-first. A
  misclassification (force disposition/unique tag counted as adopt-mechanically) caught and fixed
  before shipping. Final: 189 adopt / 71 investigate; report banked as `MFM_v1_1_Reconciliation.md`,
  B89's work order. B95 opened: `faction_taxonomy.json` `built` flag disagrees with `units.json` for
  CSM and Thousand Sons. Open count unchanged at 17 (B88 closed, B95 opened).
- **D285** — B95 shipped: `faction_taxonomy.json`'s `built` flag was stale for CSM/Thousand Sons
  (both fully built — CSM 58/58 units + 17 detachments, TS 34/34 units + 9 detachments, all assertions
  passing), but the real gap was bigger — neither had a `data_army` key, which `resolveUnits`/
  `resolveDetachments` need or they silently serve the wrong pool/an empty detachment list. Both
  `built: true` and `data_army` added together; new assertion B95-1 pins the contract for future
  faction flips (117 assertions, was 116). B94 answered by Ryan (add the real 4th copy-tier),
  queued as S193's engine turn. Open count 17 → 16 (B95 closed).
- **D286** — B94 engine turn shipped: the real 4th copy-tier landed. MFM `1ST TO 3RD` / `4TH +`
  breaks a unit's copy price at the 4th copy (34 units); the 3-tier schema couldn't hold it, so their
  4th+ copy silently priced at `third_plus`. Added an optional `fourth_plus` tier and routed all three
  points sites (`ptsForEntry`, `addUnitFromRoster`, size-selector) through one shared `copyTierPts`
  helper (≥4th copy → `fourth_plus`, fallback `third_plus`). Byte-identical on current data (no row
  carries `fourth_plus` yet); nothing re-prices until the data turn. Python mirror `copy_tier_pts` +
  assertion `B94-1` pin the ladder single-source and the JS↔Python agreement (118 assertions, was
  117). `index.html` v6.15 → v6.16. Parser check found `to_points_row` never emits the 4th tier into
  the row, so B94's next step is a tooling turn to carry it through, then the data turn (folds into
  B89), then a data-side assertion. Baseline defect found: `b87`/`b88` crash without `--data-turn` —
  ticketed **B96**. Open count 16 → 17 (B96 opened; B94 stays open).
- **D287** — B94 pipeline-emit shipped: `mfm_points_parser.py` now writes the captured esc4 4th+ tier
  into three new `Points_b-4` CSV columns (unconditional, blank on non-esc4 units); `convert_to_json.py`
  carries it into `points.sizes[*].fourth_plus`, gated behind an opt-in `--emit-fourth-plus` flag
  (default off) so every existing call site — including `units_repro_check.py`'s real-source run —
  stays byte-identical to committed `units.json`. First unconditional design broke `units_repro_check`
  (Rubric Marines diverged from committed data because real sources now carry the 4th tier); the opt-in
  gate resolved it. Verified via isolated synthetic CSV, real-source parser output, and a full-CLI
  Thousand Sons build diffed flag-off vs flag-on (only Rubric Marines + Chaos Rhino change, correctly).
  `b87_check.js` extended with a 4th fact pinning the row-level carry-through. **B96 folded in and
  closed**: `b87`/`b88` moved into `baseline.sh`'s sources-loaded conditional, `SKIP` cleanly now
  instead of crashing. Session also reconciled a stale manifest (Ryan's out-of-band B97/B98/B99 backlog
  edit between S193 and S194) before starting. Open count 20 → 19 (B96 closed).
- **D288** (S195): B94 data turn shipped — first migration of B89's MFM v1.1 adoption arc. Thousand
  Sons regenerated from `MFM_Thousand_Sons_v1.1.txt` with `--emit-fourth-plus`. Real per-faction
  pipeline run (transform → points → convert → merge → post-processors), diffed against committed
  `units.json`: exactly 12 units differ, all confined to `points` — 11 real re-prices matching
  `MFM_v1_1_Reconciliation.md`'s adopt-mechanically list exactly, plus Rubric Marines gaining
  `fourth_plus`. All other 15 armies byte-identical. A first-pass false structural diff (missing
  `bodyguard_stat_flags` key) traced to omitting the merge-time post-processors, not a real
  regression. `rules_assertions.py` carries no TS points-value pins, needed no reconciliation.
  `source_manifest.json` needed no change (both source files already correctly hashed).
  `units_repro_check.py` updated to build TS from v1.1 going forward; `_v1_0.txt` stays required
  for CSM's cross-legion cult-troop pricing. 4 TS investigate-first items (Defiler wargear,
  detachment force-disposition) left untouched, already tracked, out of scope for units.json.
- **D289** (S196): B94 data turn shipped — second migration of B89's MFM v1.1 adoption arc. Death
  Guard regenerated from `MFM_Death_Guard_v1.1.txt` with `--emit-fourth-plus`. Real per-faction
  pipeline run (transform → points → convert → merge → post-processors), diffed against committed
  `units.json`: exactly 5 units differ, all confined to `points` — matching
  `MFM_v1_1_Reconciliation.md`'s adopt-mechanically list exactly (Plague Marines, Deathshroud
  Terminators, Mortarion, Defiler re-priced; Chaos Rhino gains `fourth_plus`, B94's second faction).
  All other 15 armies byte-identical. Found the reconciliation report's Death Guard wargear note
  wrong — Defiler's Heavy reaper autocannon/Hades lascannon are repriced, not removed; flagged for
  whoever next touches `wargear_points.json`. `rules_assertions.py` carries no Death Guard points-value
  pins, needed no reconciliation. `source_manifest.json` needed no change (both source files already
  correctly hashed). `units_repro_check.py` updated to build Death Guard from v1.1 going forward;
  `_v1_0.txt` stays required for CSM's cross-legion cult-troop pricing. Death Guard's 2
  investigate-first items (Defiler wargear repricing, CONTAGION ENGINES detachment) left untouched,
  tracked, out of scope for units.json.

- **D290** — B89 third migration shipped: Chaos Daemons regenerated to MFM v1.1 by direct hand-edit of
  the Gen-1 root `Unit_Points.csv` (S197). Mechanism decision: CD's root CSVs are hand-authored source,
  never regenerated by any parser, so a direct hand-edit of the 6 changed values is correct and
  precedented — not the prohibited "hand-edit output" pattern. A `mfm_points_parser.py`-against-CD path
  exists in principle (`FACTION_BY_MFM` already maps CD's files) but is unvalidated, new tooling work,
  deferred as a future Gen-2 question, not attempted. 6 units changed (Beasts of Nurgle, Bloodcrushers,
  Fluxmaster, Kairos Fateweaver, Lord of Change, Shalaxi Helbane), all confined to `points`, diff-guarded
  against all 15 other armies and all four merged lookups. Found the reconciliation report wrong twice:
  3 enhancement re-prices misattributed to SCINTILLATING LEGION instead of SHADOW LEGION (detachments.json
  scope, flagged not fixed); a PLAGUE LEGION "FORCE DISPOSITION(S) CHANGED" banner is a text-extraction
  artifact, verified unchanged (`TAKE AND HOLD` in both versions). `source_manifest.json` hash updated for
  `Unit_Points.csv` — Ryan action required to push the matching edit to the private
  `rd-prime-1357-data-sources` repo, since Claude's token there is read-only.

- **D291** — B89 fourth migration shipped: the six-file Space Marines group (base + Black Templars,
  Blood Angels, Dark Angels, Deathwatch, Space Wolves) moved to MFM v1.1 as one atomic turn (S198).
  Chaining question resolved: `add_chapter_point_overrides.py` compares each chapter's shared-unit
  prices against the *current* generic base price on every build, so a version-mismatched base/chapter
  pairing corrupts every affected chapter's overrides — the group cannot split faction-by-faction like
  CD/DG/TS did. No new tooling needed: `mfm_points_parser.py`'s v1.1 filenames were already mapped
  (B87/D275), the P4 source census regex doesn't see dot-versioned filenames; only edit was
  synchronizing the hardcoded v1_0 filenames to v1.1 in `units_repro_check.py` and
  `add_chapter_point_overrides.py`. Also found and stopgap-fixed a genuine source-text defect: a missing
  comma in `MFM_Space_Marines_v1.1.txt`'s Marneus Calgar LEADER line glued two real unit names into one
  unresolvable token, silently dropping both from his legal attach list. Fixed via a narrow, filename-
  and-substring-scoped `_KNOWN_SOURCE_FIXES` patch in `mfm_points_parser.py` that fails loudly if the
  source changes underneath it — not a general glue-heuristic. Scanned all six SM-family files'
  validation reports for the same defect pattern; confirmed isolated to this one instance. 47 units
  changed (14 Adeptus Astartes, 8 Ultramarines, 9 Dark Angels, 7 Space Wolves, 1 White Scars, 8 Black
  Templars): `points` on all 47, `chapter_point_overrides` on 2, `model_groups` on 1 (Uriel Ventris's
  legitimate new Victrix Honour Guard attach eligibility). Diff-guarded against all ten other armies and
  all four merged lookups. One pinned `rules_assertions.py` value reconciled (`b56a_bt_negative_control`:
  Impulsor AA/BT distinctness check, 80/85 -> 70/75). `detachments.json` scope (new VENGEFUL HOSTS
  detachment, enhancement re-prices) untouched, tracked separately per the CD/DG/TS convention. Ryan
  action: push the missing-comma fix to the private repo's `MFM_Space_Marines_v1.1.txt`, then remove the
  stopgap dict entry from `mfm_points_parser.py`.

- **D292** — B89 blocked on all fronts this session (S199). Verified via a direct fetch from the private
  repo (not the local copy) that the Calgar comma fix has not landed; stopgap unchanged. Corrected the
  standing framing that Grey Knights is a B89 migration candidate: `units.json` has zero GK units at any
  version, so there is nothing to migrate — GK needs a net-new faction build (its own scoping pass, in
  the mould of `CSM_BUILD_SCOPE.md`/`THOUSAND_SONS_BUILD_SCOPE.md`), which is out of B89's definition
  and out of this session's data-only typing. Re-checked and confirmed Chaos Space Marines still blocked
  on World Eaters/Emperor's Children (neither built). No data, parser, or engine files changed —
  verification-only turn.

- **D293** — Standing rule set (S200): **always build from the newest MFM available**, units and
  detachments alike, for new builds as well as migrations. Never previously written down; the
  per-faction migrations had each deferred the detachments side, which for a brand-new faction would
  have meant authoring known-stale values on first build. Grey Knights becomes the first army with
  v1.1 detachments while the other sixteen stay v1_0. Also: Grey Knights scoped as a net-new build
  (`GREY_KNIGHTS_BUILD_SCOPE.md`, net-new). 25 current-edition datasheets (not the raw 31); the six
  exclusions verified against the MFM's own `LEGENDS` header, so Draigo's absence is correct, not a
  bug; the Thunderhawk is unbuildable (Wahapedia Forge World source is edition `0`) rather than
  excluded. B94's open Grey Knights copy-tier concern retires — the `1ST TO 3RD`/`4TH +` shape is
  gone in v1.1 (`REQUISITION THRESHOLDS REMOVED`). Points coverage complete, self-contained, no
  chapter chain. Only four units need loadout authoring. Nine detachments; v1_0 vs v1.1 differ only
  in three force dispositions. Two defects found, neither Grey Knights' fault: **B101** — no-duplicate
  wargear selection is unenforced, a live D0 gap reachable in three shipped CSM units; **B102** —
  `detachment_parser.py --report` crashes on any gap (`g["army"]` vs `source_faction`), latent because
  no gate passes `--report`.
- **D294** — B101 engine half shipped (S201), engine-only, `index.html` v6.16 → **v6.17**. New
  optional boolean `distinct` on `count` options carrying `replacement_choices`, expressing "you
  cannot select the same option more than once". Enforced at **three** places by design, since
  whichever is omitted becomes the hole: the selection path (`editLoadoutChoiceCount` gains a sixth
  `perMax` argument), the renderer (the `+` disables rather than being offered-and-rejected), and the
  rollup (`loDistinctPicks`, in **both** `loRollup` branches — fixed-1 group and body group — so a
  list saved before the flag cannot roll up illegal weapons or their points). Derived ceiling: a
  distinct option can never take more picks than it lists choices (`loChoiceGroupCap`). Over-selection
  truncates in `replacement_choices` order, deterministically. Non-distinct paths left byte-for-byte
  unchanged on purpose — the body branch's loose total handling would change shipped lists' points if
  touched, so it is **B103**, not a side effect. **The data half is still open:** no shipped option
  carries the flag, so the three CSM units are as wrong for a player at v6.17 as at v6.16; the parser
  must emit it (tooling) and the data be regenerated (data) — **B101-data**. Found while looking:
  selecting the marker string does not just look wrong, it adds a weapon named after the rules
  sentence to the unit (points unaffected). S200's table corrected — Legionaries `cc_5` is
  `per_n_models: 5 / max_per_n: 1`, not uncapped. Net-new `b101_check.js`, synthetic fixtures by
  design, each enforcement point mutation-tested.
- **D295** — B101-data turn 1 shipped (S202), tooling-only. `_choices_from_list` in
  `loadout_parser.py` now recognises the no-duplicate marker at the START of a captured list
  (GW inserts it between "one of the following" and the list; the old trailing-only parenthetical
  strip missed it) and returns `(choices, distinct)`. All ten call sites updated — six carry
  `distinct: true` onto `count_choice`/`any_count_choice`/`count` options; four single-pick types
  discard it. A second fix was needed in `build_loadout`, which rebuilds the `entry` dict from `op`
  and wasn't copying `distinct` through. Checked, not assumed: Raptors' and Legionaries' additional
  `UNMATCHED` flags are separate, unrelated parser gaps (a distinct-model-count sentence shape and a
  spelled-out "One" that doesn't match `\d+`), not the same defect — left untouched. Proven in a temp
  dir (no `unit_loadouts.json` regeneration this session): key-level diff against committed shows
  exactly the three target units changed, nothing else. B102 rode along (tooling, unrelated):
  `detachment_parser.py --report`'s `KeyError: 'army'` fixed to read `source_faction`; proven against
  real sources, all 11 known gaps render, `detachments.json` output unaffected.
- **D296** — B101-data turn 2 shipped (S203), data-only. `unit_loadouts.json` regenerated via the real
  pipeline in a scratch dir, diff-guarded at key level: exactly the three predicted units changed
  (`000000958`, `000002570`, `000002590`), nothing else across 305 parsed units. Added `rules_assertions.py`
  **B101-DATA**: scans `Datasheets_options.csv` for the no-duplicate marker across ALL rows (not pinning
  the three IDs), checks every currently-built, successfully-classified hit carries `distinct: true`.
  Scoping check found one more marked datasheet in-scope (Nemesis Claw `000003876`, CSM) but its row is
  `UNMATCHED` — marker text never reaches output, excluded correctly. Negative-controlled against the
  pre-regen file fetched from the repo: fails and names the three units; passes against the regenerated
  file. 119 assertions, all pass. Baseline-open housekeeping: `SESSION_HANDOFF_202.md` had been left off
  `pipeline_manifest.py`'s `GUARDED` list at S202 close (the S180 failure mode) — appended. `repro_check.py`
  was genuinely absent from the project file area — recovered from the repo clone, hash verified against
  the manifest. B101-data closed outright, both turns shipped.
- **D297** — B100 units half shipped (S204), data-only. `units.json` regenerated with Grey Knights (25
  units), diff-guarded at key level: exactly 25 added, nothing else moved. Four merged lookups came
  along in the same fixed point; `datasheet_wargear_abilities.json` regenerated separately (+2).
  Demonstrated (not assumed) Grey Knights needs no dedicated `_web.txt` file — its six multi-group
  units gap-fill completely from the final `--datasheets` pass alone. Loadouts half NOT shipped:
  attempting it surfaced **B104**, a real pre-existing bug in `equipped_parser.py`'s `scoped_name2id`
  ambiguous-candidate fallback that silently corrupts 8 unrelated already-shipped generic-vehicle
  units (Land Raider and variants, Rhino, Razorback, Stormhawk/Stormtalon/Stormraven) whenever a
  same-named-vehicle faction is appended after them in `units.json`. Reverted the `FACTIONS` addition
  to `repro_check.py`; `unit_loadouts.json` untouched, byte-identical to S203. Also opened **B105**
  (a passive single-model swap sentence shape no classifier matches) and **B106** (B101's `distinct`
  support doesn't cover a fixed-1-group pure-addition "up to N distinct" shape) — both found authoring
  Grey Knights' four flagged units, both left as residual `UNMATCHED` flags per the Raptors/Legionaries
  precedent once the loadouts turn actually runs. Baseline-open housekeeping: `40K_Decision_Log.md`'s
  own D296 entry had gone missing (index and backlog referenced it correctly, but the full prose entry
  was never written despite S203's handoff claiming it was) — reconstructed from the handoff, manifest
  regenerated.
- **D298** — B104 fixed (S205), tooling-only. `equipped_parser.py`'s `scoped_name2id` rewritten with
  scope-alias + parent-army fallback from `faction_taxonomy.json`, plus propagation of composition data
  to all same-named candidates. Fixes the insertion-order-dependent `cands[-1]` fallback that silently
  corrupted 8 vehicles when Grey Knights was appended to `units.json`. Also corrects a pre-existing gap
  where 7 Adeptus Astartes generic vehicles (Land Raider Crusader, 3 Gladiators, Impulsor, Repulsor,
  Repulsor Executioner) never received `equipped` composition data because the SM web pass's scope
  (`Space Marines`) didn't match the block name (`Adeptus Astartes`). Synthetic B104 assertion added to
  `rules_assertions.py`. `unit_loadouts.json` regenerated (without GK in FACTIONS) to capture the 7 AA
  improvements; repro_check byte-identical.
- **D299** — Manifest gap resolved (S206). `SESSION_HANDOFF_203.md` confirmed genuinely
  unrecoverable (re-verified via fresh clone; git history holds no trace) — removed from
  `pipeline_manifest.py`'s `GUARDED` list rather than left permanently red; its substance already
  lives in D296. A second, related gap found: `Thousand_Sons_web.txt` was never added to the private
  source repo's census, only ever living in the project mount — pulled a working copy to unblock this
  session, but the private-repo token is read-only, so pushing it and regenerating
  `source_manifest.json` is a Ryan action. P4 source census re-run per its own instruction, catching up
  on S205's B104 change (5 filenames added to `P4_REFERENCED_SOURCES`, no functional change).
- **D300** — Grey Knights loadouts half shipped (S206). B105 (new classifier for the passive
  single-model swap sentence) and B107 (new — a quote-normalisation mismatch between
  `weapon_abilities.json`'s raw punctuation and `loadout_parser.py`'s cleaned option text, found while
  verifying B105's target units; the backlog's claim that this path needed no code change was checked
  against source and found wrong). `GK` added to `repro_check.py`'s `FACTIONS`; `unit_loadouts.json`
  regenerated (25 GK units added, 0 changed elsewhere; repro_check byte-identical).
  `wargear_points.json` regenerated using the canonical `FACTION_BY_MFM` file order (4 GK units added,
  0 changed elsewhere; a naive alphabetical order was tried first and discarded — it silently shifted
  provenance on 2 unrelated entries, the same trap D236 documented for CSM). `E14-2`'s pinned census
  updated 75/54 → 90/61, verified by faction breakdown. B100 substantially closed; B106 (Dreadknights'
  distinct-addition engine gap) remains open, untouched, correctly the only residual flag left on Grey
  Knights.
- **D301** — B106 shipped (S207), engine-only. `loRollup`'s fixed-1 branch now accepts a distinct-
  addition count option: a `count` with `distinct: true`, `replacement_choices: [...]`, `max_total: N`
  and **no** `replaces` — a pure addition ("this model can be equipped with up to N of the following,
  but cannot take duplicates"). Chosen after tracing both existing paths against source: the fixed-1
  branch was the actual gap (a two-line guard, plus a one-line skip inside `chargeF`); the body-group
  branch already accepted the shape via `loSrcOnGroup` returning true for empty `replaces` (verified,
  not assumed); the `add`+`pool_id` path can't express the rule because its cap is `max` of member
  caps, not a sum; a new top-level type would multiply surface area across the renderer, cost
  calculator, selection path and every check harness. Net-new `b106_check.js` (32 assertions covering
  helpers, both rollup branches, selection path, and the plain-replacement regression), gated in
  `baseline.sh` and `pipeline_manifest.py`. `index.html` v6.17 → v6.18. Grey Knights fully unblocked
  for data-turn authoring (parser change + Dreadknight regeneration next session). Baseline reconciled
  at open surfaced a critical, unrelated finding: `Thousand_Sons_web.txt` is committed to the public
  repo — verbatim GW composition material, standing-constraint violation — and the S206 Ryan action
  to push it to the private repo is still not done. Cannot fix from this session (public-repo push
  scope + read-only private token); opened as **B108**.
- **D302** — B106-DATA shipped (S208), data+parser turn. New classifier `classify_this_model_add_count_choice`
  matches "This model can be equipped with up to N of the following, but cannot take duplicates" (N
  spelled as a word, confirmed across a full corpus scan — never a digit), emitting the exact shape
  B106's engine fix (D301) was built to accept: `type: 'count'`, `distinct: true`, `replacement_choices`
  populated, `max_total` set, no `replaces`. Both Grey Knights Dreadknights authored — the only two
  currently-built matches, confirmed by running the classifier against the full options corpus (four
  more raw-text matches found, all Tau, different sentence shape, not currently built, correctly left
  alone). `unit_loadouts.json` regenerated via the seven-pass chain seeded with only the four
  `HAND_AUTHORED` entries (2 units changed, 0 elsewhere; `repro_check` byte-identical).
  `wargear_points.json` regenerated via the canonical `FACTION_BY_MFM` file order (2 units added, 0
  elsewhere; v1_0/v1.1 prices confirmed identical before trusting the v1_0 provenance). New structural
  assertion `B106-DATA`, re-derived from source per the `B101-DATA` pattern rather than pinned to the
  two unit IDs. **B100 (Grey Knights) CLOSED — faction fully complete, 25/25 units, zero residual
  `_parser_flags`.** Faction-priority census corrected by reading `units.json` directly: all twelve
  Adeptus Astartes entries are already built (Grey Knights was the last, not mid-list, consistent with
  D293's "sixteen pre-existing armies" framing at S200) — **Emperor's Children is the correct next
  faction**, not "the next Adeptus Astartes faction" as S206/S207's prompts carried forward. Needs its
  own scoping pass first; no scope doc exists yet. B108 (Ryan action) remains open — public-repo
  removal side still outstanding, private-repo push side now confirmed done. Also logged: **B109** —
  "My Army Lists" page, "Target ####" → "#### Points" label change (Ryan-reported, UI copy only).
- **D303** — Emperor's Children scoped (S209), scoping-only. No committed file changed.
  `EMPEROR'S_CHILDREN_BUILD_SCOPE.md` written (net-new). 23 datasheets, zero LEGENDS exclusions,
  zero engine gaps found — the first faction where scoping surfaces no engine ticket. Full dry-run
  pipeline clean (23/23 priced, 0 collisions). Loadout parser flagged exactly 2 units (Tormentors,
  Infractors — same free equip-only "icon of excess" item, already-solved shape). Confirmed no
  version-mismatch risk in CSM's already-shipped cross-reference to `MFM_Emperors_Children_v1_0.txt`
  for its own Noise Marines cult-troop unit (a different datasheet ID from EC's own Noise Marines;
  both MFM versions price it identically). Confirmed EC needs no chapter-override or co-leader
  registration. Detachments: 10, no unique tags, 4 force-disposition changes v1_0→v1.1, one genuine
  Defiler wargear price increase (10→15 pts ×2 options) — build from v1.1 per D293. Unrelated finding
  logged as **B110**: `faction_taxonomy.json` still shows Grey Knights `built: false`, stale since
  B100 closed at S208. Located but did not touch B109's render site in `index.html`
  (`renderMyLists`) — an engine edit would mix with this scoping turn.
- **D304** — Emperor's Children units shipped (S210), data-only. `EC` registered in
  `units_repro_check.py` (mirrors GK/TS) and `merge_factions.py`. Real pipeline run end to
  end: 23 EC units added, 0 changed/removed elsewhere; `units_repro_check.py` byte-identical.
  Confirmed by direct demonstration that S209's scope doc overestimated manual-authoring
  need: of the "6 manual" wargear groups and 5 "ambiguous" weapon matches flagged at scoping,
  the real `loadout_parser.py` run resolved every one cleanly via existing cross-faction
  precedent (bare weapon names, `classify_n_model_swap`'s compound-swap handling, EC's own
  Defiler matching its already-shipped CSM/DG/TS/WE siblings exactly) — no `bundled_swaps.json`
  entry needed. Only Tormentors and Infractors needed genuine hand-authoring: both carry "1
  `<UnitName>` can be equipped with 1 icon of excess," a shape none of the 19 `CLASSIFIERS`
  match (the literal word "model" is hard-coded); checked the actual source text before
  copying the Icon of Despair precedent and found EC's text carries no gating clause, so the
  two new entries use the plain add/equipment/max_total:1 shape only. Added to
  `repro_check.py`'s `HAND_AUTHORED`; `EC` added to `FACTIONS`; no `WEB_PASSES` entry needed,
  confirmed the same way GK didn't need one. `unit_loadouts.json` regenerated via the real
  chain: 23 EC entries added (21 auto + 2 hand-authored), 0 changed/removed elsewhere,
  byte-identical repro. New structural assertion `EC-DATA` (122 total), scoped to Emperor's
  Children specifically since the same sentence shape already exists unfixed on other
  factions' datasheets as pre-existing backlog debt, not something this session touches.
  `datasheet_wargear_abilities.json` regenerated (+5 EC entries, a real gap, not previously
  flagged). `B61-2`/`B61-3` extended for EC's Legions of Excess carriers (5 units, confirmed
  distinct `local:chaos-daemons:*` ids on the Chaos Daemons side, same shape as DG/TS).
  `E14-2`'s count updated 90/61 → 98/67, verified by faction breakdown before updating the
  literal. **Found and opened B111**: every v1.1 MFM file dropped the leading bullet
  character from `WARGEAR OPTIONS` lines that v1_0 files have; `mfm_points_parser.py`'s
  `WARGEAR_RE` regex requires it, so the `--wargear` pass has been silently blind to v1.1
  pricing for every faction since the v1.1 migration — confirmed universal (GK/DG/TS/CSM v1.1
  files all affected), not EC-specific, and harmless everywhere else only because those
  factions' v1_0/v1.1 wargear prices happen to match. `wargear_points.json` shipped EC's
  Defiler at v1_0's 10 pts (matching its already-shipped siblings), not v1.1's correct 15 pts
  — diff-guarded, 1 unit added, 0 changed/removed elsewhere. Not fixed this session (engine
  change; would mix with a data-only turn). **B110 corrected, not executed**: checked
  `detachments.json` directly and found Grey Knights has zero detachment entries — flipping
  `built: true` per the original B110 wording would expose a faction with no detachment
  picker (`index.html` uses `built` to gate faction selectability). Flagged for Ryan rather
  than executed; Grey Knights' taxonomy flag stays `false` until its detachments ship.
  Detachments and `faction_taxonomy.json` deliberately untouched this session — Emperor's
  Children's own detachments are next.
- **D305** — Emperor's Children detachments shipped (S211), data-only. `EC` registered in
  `detachment_parser.py`'s three maps, pointed at v1.1 per D293 (not the flawed TS/CSM/DG
  v1_0 precedent — see finding below). 10 detachments, DP 1-3, zero unique tags, all four
  scoped force-disposition changes landed correctly. Diff-guarded against committed
  `detachments.json`: exactly EC's block added, 0 changed/removed elsewhere, byte-identical
  repro. Carnival of Excess carries a Legions of Excess allied-group unlock (500/1000/1500
  pts cap by battle size) plus a "cannot be Warlord" restriction, same shape as Thousand
  Sons' Changehost of Deceit; scanned all 10 EC detachments directly, only this one
  qualifies. One new `detachment_effects.json` entry authored
  (`Emperor's Children|CARNIVAL OF EXCESS`), appended at file end preserving insertion
  order, diff-guarded clean. `faction_taxonomy.json`: EC's `built` flag flipped to `true`,
  `data_army: "Emperor's Children"` added — units and detachments both complete now.
  **Finding, not fixed this session**: `ARMY_TO_MFM` sources Chaos Space Marines, Death
  Guard, and Thousand Sons' detachments from v1_0 MFM files, not v1.1, despite those
  factions' units already being on v1.1. Direct parse-and-diff confirms real, already-shipped
  bugs: Thousand Sons' Hexwarp Thrallband is priced 2 DP (should be 3 DP); six force-
  disposition mismatches across the three factions (2 TS, 2 CSM, 1 DG, plus a third TS one);
  Chaos Space Marines' Soulforged Warpack enhancement Tempting Addendum priced 25 pts
  (should be 40 pts). Not new — `MFM_v1_1_Reconciliation.md` (B89's own work order) already
  flagged these as "investigate-first" at the time of the original migration; B89 has stayed
  open since, and its detachment-side work for these three factions was never finished.
  Recommending it as the next data turn under B89, not opened as a new ticket.

- **D306** — CSM/Death Guard/Thousand Sons detachments re-pointed to v1.1 (S212), data-only. Fixes
  the D305 finding: `ARMY_TO_MFM` re-pointed at each faction's v1.1 MFM file, mirroring Emperor's
  Children. 7 detachment records changed (0 added/removed, 179 total unchanged), matching D305's
  predicted list exactly — Hexwarp Thrallband 2 DP to 3 DP, six force-disposition corrections,
  Soulforged Warpack's Tempting Addendum 25 to 40 pts. One extra harmless diff: a v1.1 hyphenation
  fix in Contagion Engines' enhancement name. `detachment_effects.json` and `rules_assertions.py`
  both checked directly and confirmed unaffected. B89 stays open — the same v1_0 sourcing gap still
  applies to the six-file Space Marines group, not yet confirmed/quantified by direct diff.

- **D307** — Space Marines-family group (base Adeptus Astartes, Black Templars, Blood Angels, Dark
  Angels, Deathwatch, Space Wolves) detachments re-pointed to v1.1 (S213), data-only. Direct
  parse-and-diff run first, not assumed from D291's prose. 6 detachments added (a new "Vengeful
  Hosts" per source file, matching the pre-existing no-text-source pattern), 50 changed — 37
  force-disposition corrections (each verified against the MFM's own "UPDATED" marker) and 13
  enhancement price changes across five enhancement names. `detachment_effects.json` and
  `rules_assertions.py` both checked directly against the full changed/added set — zero overlap,
  no update needed. `faction_taxonomy.json` confirmed unchanged. This closes B89's
  detachments-side gap for the entire Adeptus Astartes group — only Chaos Daemons remains blocked
  on GW not having published a v1.1 detachment file.
- **D308** — B109 "My Army Lists" label fix (S214), engine-only. `index.html`'s `renderMyLists()`
  `tgt` line changed from `'target ' + r.points_target` to `r.points_target + ' Points'`. Version
  bumped 6.18 → 6.19. Only file touched. B109 closed.
- **D309** — B111 tooling fix (S215), tooling-only. `mfm_points_parser.py`'s `WARGEAR_RE` leading
  bullet made optional so bullet-less v1.1 `WARGEAR OPTIONS` lines parse (v1_0 output byte-identical;
  all twelve built v1.1 files now read wargear, previously zero). Finding: B111 is not splittable as
  the S215 prompt assumed — assertion E14-1 rebuilds `wargear_points.json` from the parser every
  baseline, so fixing the parser makes it red until the data is regenerated. Shipped the tooling half
  and closed with E14-1 as a documented known-red; B111 data turn made mandatory-next. Confirmed live
  price changes for the data turn: four Defilers (CSM/TS/DG/EC) 10→15 pts, plus SM Banner of Macragge
  10→15 pts (new casualty).
- **D310** — B111 data turn (S216), data-only. `wargear_points.json` regenerated from v1.1 MFM
  sources. 9 price changes as forecast in D309 (four Defiler factions' Heavy reaper autocannon and
  Hades lascannon 10→15 pts; SM Banner of Macragge 10→15 pts). Plus 3 genuinely new v1.1-only
  wargear items surfaced and verified (Black Templars Repulsor Executioner heavy laser destroyer,
  Thousand Sons Forgefiend ectoplasma cannon, Centurion Devastator Squad twin lascannon) — none
  double-counted against base unit points. Zero removed. E14-1 now green; repro/b87/b88 all
  byte-identical. B111 fully closed.
- **D311** — World Eaters scoped (S217), scoping-only. No committed file changed.
  `WORLD_EATERS_BUILD_SCOPE.md` written (net-new). 30 datasheets, 28 Legends exclusions confirmed
  both directions, zero engine gaps. "Blood Legions" allied-Daemon block confirmed already-wired
  (B61 pattern, DG's Nurgle-Daemon units are the shipped precedent). Leader mapping (5 blocks)
  cross-checked against `Datasheets_leader.csv` independently — exact match. Build from v1.1: two
  force-disposition changes, two `UNIQUE TAG REMOVED` events (zero unique tags remain), one
  enhancement re-price. Full pipeline dry run clean (0 collisions, 5 leader overrides, 3 wargear
  items already priced from sibling factions). `loadout_parser.py` flagged 2 of 30: Jakhals (a
  genuinely new two-option composition shape, confirmed unique by direct grep) and Helbrute
  (already-solved shape, three sibling factions ship the identical sentence). **B113 opened**: a
  `LEADER:` enhancement-eligibility restriction is discarded as parser noise, pre-existing on CSM
  (×2)/TS(×1)/EC(×1), not a World Eaters blocker. **B112 unblocked**: a v1.1 Chaos Daemons MFM
  file now exists in the private repo (absent at S214), ready for its own data turn.

- **D312** — World Eaters units shipped (S218), data-only. `units.json` built from
  `MFM_World_Eaters_v1.1.txt`, diff-guarded: 30 added, 0 changed/removed. `units_repro_check.py`
  gained the WE block (mirroring GK/EC); `MFM_Emperors_Children_v1.1.txt` also added to `REQUIRED`
  (a pre-existing gap, not new behavior). Jakhals (`000002628`) hand-authored into
  `unit_loadouts.json` — a genuinely new two-bracket `or:` composition shape, default weapons read
  directly off the datasheet's own loadout prose (Dishonoured carry no sidearm). Helbrute needed no
  hand authoring — resolved automatically with the same already-accepted `UNMATCHED` flag shipped
  on three sibling factions' Helbrutes. Full loadout regen diff-guarded: 30 added, 0 changed/removed.
  A mid-session false alarm (three unrelated units appearing to change) was traced to a mistake in
  a diagnostic seed file, not a real engine issue — confirmed by rebuild with the correct seed.
  Companion updates, all verified before changing: `ALLIED_CARRIER_GROUPS` (B61) gained World
  Eaters' five Blood Legions carriers; `wargear_points.json` regenerated (+2 units, Forgefiend/
  Defiler, matching the scope doc's forecast); E14-2 literal 98/67 → 108/75 (WE +10/+8, every other
  army's count reverified unchanged); `datasheet_wargear_abilities.json` regenerated (+5 WE
  datasheets). Full baseline green except the expected pre-`--write` state. `detachments.json`
  deliberately untouched — World Eaters' own detachments are next.

- **D313** — World Eaters detachments shipped (S219), data-only. `WE` registered in
  `detachment_parser.py`'s three maps, built from `MFM_World_Eaters_v1.1.txt`. `detachments.json`
  diff-guarded: 8 added, 0 changed/removed — the forecast Brazen Engines/Butchers of Khorne
  disposition changes, zero remaining `UNIQUE:` tags, and Archslaughterer's 40→30 pt re-price all
  confirmed direct from source. Checking `detachment_effects.json` directly (not assumed clean)
  found **two** construction-effect gaps, not the one the scope doc anticipated: Khorne Daemonkin
  (Blood Legions allied-unlock + no-Warlord, the expected pattern) and Cult of Blood (Jakhals/
  Goremongers BATTLELINE grant, an unflagged pattern caught by `rules_assertions.py`'s
  `e21a_coverage` assertion on baseline re-run). Both rows authored mirroring existing sibling-
  faction precedent, diff-guarded 0 changed/removed elsewhere. `e21b_check.js`'s battleline-sweep
  literal updated 7 → 9 units, confirmed by the harness's own live sweep. `faction_taxonomy.json`:
  World Eaters `built` flipped to `true`, `data_army` added — World Eaters is now fully built and
  selectable. B113 gains 2 more instances (not opened new). B112 remains open, not picked up.

- **D314** — Grey Knights detachments shipped (S220), data-only. `GK` registered in
  `detachment_parser.py`'s three maps, built from `MFM_Grey_Knights_v1.1.txt`. `detachments.json`
  diff-guarded: 9 added, 0 changed/removed — zero `UNIQUE:` tags, and the three forecast
  force-disposition changes all confirmed direct from source. **Correction to the scope doc: 30
  enhancements, not the scoped 28** (Upgrade count of 4 was right), caught by re-deriving rather
  than trusting prior-session prose. `detachment_effects.json` checked directly: no row needed,
  confirmed both by manual scan and by `rules_assertions.py`'s `e21a_coverage` passing clean.
  `faction_taxonomy.json`: Grey Knights `built` flipped to `true`, `data_army` added — **closes
  B110**. Grey Knights is now fully built and selectable. **All twelve Adeptus Astartes armies are
  now complete.** Also reconciled at open: `OUTPUT_FORMAT_SPEC_for_project_instructions.md` had
  drifted from the manifest (project-area copy ahead of the unpushed repo); re-pinned to the area's
  copy, left `repo_check.py` correctly red as a Ryan push action.

- **D315** — Chaos Daemons LORDS OF THE WARP disposition shipped (S221), data-only. Verified from
  source, not the forecast: v1.1 confirms Purge the Foe → Take and Hold, its own banner present.
  `detachment_parser.py` re-pointed (not re-registered) at `MFM_Chaos Daemons_v1.1.txt`.
  `detachments.json` diff-guarded: only the disposition change and 3 Scintillating Legion re-prices
  (10→15, 25→20, 20→25) anywhere in the file, all matching the source's own price markers. **Closes
  B112.** `detachment_effects.json` checked directly: existing Shadow Legion HERETIC ASTARTES unlock
  row found stale — its `enforced: false` reason names Chaos Space Marines as not-built, which has
  been false since S212 — **opens B114** rather than fixed in this data-only turn. B113 gains 0 new
  instances. `faction_taxonomy.json` already correct, no edit needed.
- **D316** — Drukhari scoped (S222), scoping-only. Roster 23 units (7 Legends exclusions, both
  confirmed), zero Support units, all points/threshold shapes precedented and proven by direct
  parse. Detachments: 9, DP 1–3, 30 enhancements; three shared-Unique-tag pairs (COVENS, WYCH CULT,
  KABAL), confirmed already-precedented against `detachments.json` (Blood Angels, Death Guard, CSM,
  Thousand Sons). B113 gains 0 new instances. **Two real findings**: (1) `wahapedia_transform.py
  --faction DRU` wrongly pulls in 14 Harlequin/Aeldari-Corsair datasheets (legacy `faction_id`
  mistag; real source is the Aeldari Faction Pack) — a real transform bug, must be fixed before the
  units data turn; (2) those 14 units are not noise — Drukhari's "Corsairs and Travelling Players"
  army rule and the Reaper's Wager detachment legally permit including them at a battle-size-scaled
  points cap sourced from a different, unbuilt faction's MFM — no built faction has this shape.
  Recommended deferring the allied-inclusion mechanic to a follow-on ticket and shipping Drukhari's
  own 23-unit/9-detachment build first; flagged for Ryan's call (sets precedent). `DRUKHARI_BUILD_
  SCOPE.md` produced; no units/detachments build started.
- **D317** — B115 fixed (S223), tooling-only. Open-time finding: `pipeline_manifest.py` failed on
  two files whose local/repo content (verified identical to each other) didn't match the hashes
  banked at S222 close — reconciled via `--write` against the verified-correct state, root cause
  unconfirmed, no further action needed. B115: tested the "preferred" generalized fix (exclude any
  source belonging to a different real faction) against every faction_id first — it would have
  broken the already-shipped Chaos Space Marines roster (its 4 cult-troop units are legitimately
  CSM-tagged but sourced from their own Legion's Faction Pack, per D240/S157). Shipped the targeted
  fix instead: a `FOREIGN_SOURCE_OWNER` map (Aeldari's `source_id` → `AE`) threaded through
  `source_is_excluded`. Verified by exact datasheet-id-set comparison: only DRU changes (37→23),
  every other faction byte-identical. Downstream re-verified: 0 "no MFM points" datasheets (was
  14), same 7 Legends exclusions, same 1 attach-list drop — exact match to S222, now proven by
  rerun. Full baseline clean, zero regression. No units/detachments build started (tooling-only).
- **D318** — Drukhari units built (S224), data-only. 23/23 datasheets match scope exactly, all 6
  Leader attach lists correct, Raider/Venom/Ravager v1.1 tier shapes confirmed. Rebuild diffed
  against a clean repo fetch: units.json +23 units/0 changed, abilities.json +59,
  weapon_abilities.json +8, datasheet_wargear_abilities.json +6 — all purely additive, zero
  removals. wargear_points.json correctly unchanged (gated on unfinished loadout groups).
  Detachment-map registration (prompt's own step 3) deferred to the detachments build turn —
  registering early breaks detachments_repro_check since Drukhari's detachments.json doesn't exist
  yet; reverted after testing. Full baseline clean, zero regression.
- **D319** — Drukhari loadouts built (S225), tooling-only. Re-derived the flagged-unit set from
  the real pipeline rather than trusting §7's carried-forward numbers: actual gap was 4 units
  needing authoring (Wracks, Talos, Cronos, Ravager), not 9 — 4 of §7's named units resolve
  automatically, 4 more flagged units need no unit_loadouts.json entry at all (other_options
  handles them natively, same precedent as Incursor Squad's Haywire Mine). Diff-guarded: +23
  units, 0 removed, 0 existing changed. wargear_points.json rebuilt, exactly the 4 forecasted
  Drukhari items populate. E14 literal updated 108/75 → 109/76, verified by full per-army
  breakdown. Full baseline clean, zero regression.
- **D320** — Drukhari detachments built (S226), data-only. 9 detachments, DP 1–3, 30 enhancements,
  three shared Unique tags; Drukhari's units, loadouts, and detachments now all shipped, B116 the
  only item left open.
- **D321** — B113 build stopped at open and re-scoped (S227), scoping. `LEADER:` line is an
  attach-enabler, not an assignment restriction; real bearer census is 8, not 6. Decision put to
  Ryan; see `B113_LEADER_RESTRICTION_SCOPE.md`.
- **D322** — B113 built and closed (S228), engine turn. Ryan chose option (A): bearer restriction
  enforced, `LEADER:` attach-enablement left unenforced. `index.html` v6.20, two new pinned
  assertions (E4b-6, E4b-7), full baseline clean.
- **D323** — B114 scoped (S229), scoping-only. Shadow Legion's stored unlock target had no
  consuming engine code; real unlockable set is 21 source-derived units. Recommended reusing the
  `allied_group` mechanism. `B114_SHADOW_LEGION_SCOPE.md` written.
- **D324** — B114 build attempt stopped (S230), scoping. Correct build is a pipeline run against 21
  new datasheet IDs, not a two-file data edit — S229's plan undercounted the work. Stopped cleanly.
- **D325** — B114 built and closed (S231), pipeline/data. CD-faction datasheet rows are Wahapedia
  mistag duplicates, not book-variant reprints. 21 units appended into Gen-1 Chaos Daemons root
  CSVs; `detachment_effects.json` retargeted onto `allied_group`, `enforced: true`.
- **D326** — Session-open reconciliation (S232), tooling. Fixed `classify_tier`'s reachability gap;
  restored a doc-integrity gap (D324/D325 full entries had landed only in this index, not the log).
  Real finding logged as **B117** (6 GW-derived CSVs on the public repo), Ryan action.
- **D327** — GK §6/§7 confirmed already shipped (stale prompt recommendation); private
  data-sources repo found to have never received B114's 21-unit append; reconstructed and
  verified byte-identical, but could not push — token read-only in practice. Opened as **B118**
  (S233), Ryan action.
- **D328** — B98 closed (S234), data-only. Daemon Prince of Tzeentch "heliforged"/"Hellforged"
  source typo fixed via a scoped `SOURCE_TYPO_CORRECTIONS` lookup in `equipped_parser.py`; full
  regen chain diff-guarded to exactly the two targeted records. Session-open reconciliation found
  **B108, B117, and B118 all already resolved** by Ryan pushing both repos ahead of this session —
  verified directly and closed all three. Full baseline 33/33.
- **D329** — B99 scoped (S235), scoping-only. No engine path exists between an assigned
  enhancement and any weapon characteristic; censused 57 unconditional bearer-weapon numeric
  records + 17 ability-grant records (72 union) across 13 armies, banked Sets C/D as B119/B120,
  corrected B99's "D0-adjacent" framing to display-fidelity, chose the B113 curated-table +
  census-assertion mechanism. `B99_SCOPE.md` written. Six scope docs found unguarded → **B121**.
- **D330** — B99 engine turn shipped (S236), engine-only. `index.html` v6.21: curated
  `ENHANCEMENT_WEAPON_EFFECTS` table on the B113 key, delta applier (AP sign inverted, variable
  A/D composed as strings), bearer-attribution rule on the D105/D112 three-way pattern, both
  weapon tables fed from one shared cell builder, new `b99_check.js`. Re-derived census corrects
  D329: Set A2 is 23/13 not 17/12 (*Eye of the Primarch* straddles like *Blades of Valour*), so
  the union is **78 records / 43 names**, not 72. D329's trap-3 test was on statline groups and
  missed *Ravenwing Command Squad*; shipped test is on loadout groups and live model counts.
  Chaos Daemons enhancement text is shorthand, not rule text → **B122**.
- **D331** — B99 tooling turn shipped (S237), tooling-only. New `rules_assertions.py` assertion
  `B99-CENSUS`: re-derives the Set A/A2 candidate population from `detachments.json` descriptions
  independently of the curated table and fails on any unhandled record (source → table direction).
  Matches D330 exactly (57/32, 23/13, 78/43), found and fixed two real regex bugs along the way
  (bare "bearer" over/under-matching, `+` missing from the bracket-ability pattern), and reports
  Chaos Daemons' 29 shorthand records (B122) as skipped rather than silent non-matches.
  `B99_SCOPE.md` §1/§7 corrected to 57/23/78/43, closing out the stale 72 figure. **B121** folded
  in: six scope docs added to GUARDED, all verified against a fresh repo clone first — one
  (`EMPEROR'S_CHILDREN_BUILD_SCOPE.md`) has a literal apostrophe in its real filename that the
  project-area mount silently strips to an underscore; the sanitised name would have gone in
  GUARDED wrong and turned the gate permanently red.
- **D332** — B119 engine turn shipped (S238), engine-only. `index.html` v6.22: curated
  `ENHANCEMENT_BEARER_STATS` (10 records / 6 names / 8 armies, re-derived from source at build
  time and matching D329 exactly), a delta applier, a per-statline-group bearer-mode resolver, and
  T/OC override support in `buildStatTable`. New harness `b119_check.js`. Four things settled
  against the data rather than the ticket: the delta lands on a SET value not the printed one;
  T/W/OC compute rather than compose (integers everywhere, re-checked each run); a retinue
  statline group gets nothing rather than an asterisk, while *Ravenwing Command Squad* gets the
  asterisk and never a value; Save/Leadership/Movement deliberately unimplemented with a gate
  rather than a guessed sign. Legend wording factored into one shared `enhModLegend`. Two
  populations D329 never censused, both banked: **B123** (25 records that SET a bearer statline
  value or grant Feel No Pain — held back on a display-precedence decision, not on mechanism) and
  **B124** (*Master Artisan*'s unit-wide Toughness half, in neither B119 nor B120). All six names
  also carry an unenforced "X model only" bearer restriction → corroborates **B93**, raising its
  priority. B119's tooling half (a `B99-CENSUS`-shaped assertion) remains open.
