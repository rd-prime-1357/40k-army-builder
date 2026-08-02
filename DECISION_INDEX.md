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
