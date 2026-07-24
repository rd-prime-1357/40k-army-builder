# Backlog Archive

Closed/shipped tickets moved here in full at **S126 (T5)** from `OPEN_ITEMS_BACKLOG.md`, which
had grown to 166 KB of mostly-closed narrative loaded every session. The standing rule is
unchanged: closed items keep their complete history (audit findings, decision references, what
shipped when) — the history just lives here now. `OPEN_ITEMS_BACKLOG.md` keeps a one-line
pointer to each entry below, in the same order.

### B1 — Ability-description collision (SYSTEMIC) — **AUDITED S76 (D141), residual risk (B1b) SHIPPED S77.**
Symptoms Ryan flagged: Cato Sicarius's "Honour or Death" shows the wrong text;
Apothecary's "Narthecium" contains "Ravenwing". Root cause as originally diagnosed: the
ability-description lookup (`abilities.json`, built name→description) keeps ONE
description per ability *name*. When several units share a name but carry
different (chapter-specific) text, the first-indexed version wins and every unit
with that name inherits it.

**S76 finding: this mechanism was already fixed before this bug was ever reported, just not confirmed
closed.** `wahapedia_transform.py` already carries a per-datasheet `unit_abil_desc` map (threaded into
`Unit_Ability_Details.csv` → `unit_ability_details` on each unit), and `index.html`'s render already prefers
it over the global map (`raw.unit_ability_details[name] || abilitiesLookup[name]`). Audited all 473
ability instances across every built SM/DG unit against the correct per-datasheet source text in
`Datasheets_abilities.csv` — **zero mismatches**. Cato Sicarius's "Honour or Death" and Apothecary's
"Narthecium" both resolve correctly in current data. This mechanism covers both Datasheet- and Faction-type
abilities, so it isn't a narrow patch — it's the systemic fix B1 asked for, already shipped for every
faction that routes through the transform.

**What's actually still open — Chaos Daemons (Gen-1) has zero override coverage.** CD never routes through
`wahapedia_transform.py` (D132) and has no equivalent per-datasheet source, so every CD unit's
`unit_ability_details` is an empty `{}` — every CD ability falls back to the shared global map. Found 9
ability names that genuinely collide between Death Guard and Chaos Daemons with different (legitimately
different per-book) text: Mischief Makers, Deluge of Nurgle (Aura), Infected Outbreak, Fortification,
Diseased Cover, Fire Support, Virulent Blessing (Psychic), Daemon Lord of Nurgle (Aura), Scuttling Walker.
Checked which built units actually use these — every DG unit has its own override and is correct; every CD
unit using one of these 9 names has NO override and today happens to show its own (CD-correct) text only
because CD's version currently wins the merge into `abilities.json` — an accident of build/merge order, not a
structural guarantee. A future faction rebuild could silently flip the winner and CD units would start
showing DG's wrong text with nothing to catch it.

**B1b — give Chaos Daemons its own per-unit ability-text coverage — SHIPPED S77 (see decision log D142).**
`Unit_Abilities.csv` (CD's flat global lookup) has no per-datasheet scoping and turned out to be far more
corrupted than D141's audit found — 33 of its 96 entries are truncated at the source, not just the 3 flagged,
so it could never have served as the text source. `chaos_daemons_reference.md` (the condensed faction-pack
reference) does carry full per-unit ability text under each datasheet's own "Abilities:" line, covering all 53
built CD units; a new parser (`build_cd_ability_details.py`) extracts it into the same `Unit_Ability_Details.csv`
shape the SM/DG mechanism already consumes, keyed on the same `local:` slug `unit_id` CD units already use —
no engine change needed, `convert_to_json.py`'s existing optional-CSV hook picked it up as-is. Also corrected:
D141's "9 collisions" list included "Fire Support", which isn't actually a Chaos Daemons ability at all (not in
`Unit_Abilities.csv`, not used by any built CD unit) — the real count is 8.

**B52 and the 3 truncated CD descriptions also fixed by this same build** (see below).


### B2 — "Leader" rule shows the game Leadership rule, not the unit's Leader ability — **CLOSED (audited S78, D143)**
~~In the unit popup Rules section, "Leader" resolves to a generic leadership/Ld
description rather than the unit's own Leader ability.~~ Not reproducible on committed data.
Two existing mechanisms already cover it: the dedicated **Leader section** (B49) renders each
unit's own `leader_eligible_units` + raw `leader_footer` (not generic text), and the Rules
section explicitly filters the Core `Leader` rule out (`name !== 'Leader'`) so it never renders
as a rule. D141's hypothesised *Leader*-vs-*Leadership* `rule_names` collision does not exist:
there is no standalone "Leadership" rule (substring only, inside other abilities), and zero
`unit_ability_details` entries named "Leader." Same outcome as B1 — closed by existing mechanism,
no fix needed.


### B3 — Wrong faction assignment: Chaplain Kastiel & Judiciar Xacharus — **CLOSED (already resolved)**
~~Both listed under Ultramarines in error.~~ Not reproducible in committed data.
Both carry faction keywords Adeptus Astartes + **Blood Ravens**; Blood Ravens is not
a KNOWN_CHAPTER / built subfaction, so `build_army_names` correctly drops them to the
generic **Adeptus Astartes** block and raises an `unknown_chapter_kw` flag. Ultramarines
block audited — all 8 units correctly Ultramarines-keyworded; neither is misfiled there.
The old mis-assignment was fixed by the current resolution logic in an earlier session.
(Name corrected: the unit is "Judiciar **Xacharus**", not "Xacharius".)


### B4 — Roboute Guilliman missing abilities — **SHIPPED S87 (D155)**
Root cause was ability-type routing in `wahapedia_transform.py`: only Core / Datasheet / Faction / Wargear
types were surfaced, and Primarch / Special / "Special (правая колонка)" / "Fortification (левая колонка)"
were silently dropped. Extended the Datasheet branch to accept those four types (they're layout buckets, not
semantic classes — the same insight the SUPREME COMMANDER name-match comment already noted). Guilliman gains
Primarch of the XIII (Aura), Master of Battle, Supreme Strategist, and SUPREME COMMANDER text. 37 units total
gained ability text, all verified against source. `Wargear profile` (One Shot etc.) stays unrouted — belongs
in the weapon-abilities pipeline; deferred. `Без заголовка` stays unrouted — Drop Pod's Designer's Note is
not an ability.

*Original entry:*
Needs "Author of the Codex Astartes" abilities listed, and the "Supreme Commander"
ability added. Investigate whether these are dropped by ability-type routing
(e.g., Primarch/Special types not surfaced) or a data gap.
- Size: S–M.


### B5 — SM Lieutenant weapon swap wrong (all-three-at-once) — **SHIPPED (v5.41)**
The atomic 3-for-3 (bolt pistol + master-crafted bolter + close combat weapon →
neo-volkite pistol + master-crafted power weapon + storm shield) is now authored as
an `alternative` bundle. Picking it hides and clears the three per-slot swaps (and
vice versa via mode-aware suppression); it grants a storm shield (INV → 4+). The
mangled single-weapon version (`sng_2`) is dropped as a broken compound. See D73/D74.


### B6 — Captain weapon swap wrong (one-of-the-following) — **SHIPPED (v5.41)**
Root cause was the render dispatch: loadout-defined units showed *either* their
loadout options *or* their bundle, never both, so the Captain's correct ten-endpoint
bundle was never drawn and only the parser's broken duplicate options showed. Fixed
by integrating the two systems (bundle add/remove folds into the loadout weapon
rollup; the bundle picker + grants render alongside; the loadout options the bundle
owns are suppressed). The Captain is now driven by its `owns`-mode bundle; the relic
shield fires (Wounds → 7), which also closed the B12 relic-shield case. See D73.
Original rule (one of): heavy bolt pistol / neo-volkite / plasma pistol × power fist /
master-crafted power weapon, plus heavy bolt pistol + master-crafted power weapon +
relic shield.


### B7 — Multi-leader attachment not supported — **CLOSED S89 (D157) — mechanic already shipped in B38 cluster; residuals reshaped into B7a and B7b**
Rules allow more than one leader on a unit (e.g., Captain + Lieutenant on the same
bodyguard unit). The tool only allows one leader per unit.
- Size: M. Connects to E9 (Warlord) and the attached-unit combined popup already
  banked. Best designed together as a leader-system pass.

**S89 finding (D157):** the ticket text is stale. B38's cluster (D144–D147, S79–S81) shipped the
multi-leader mechanic end to end — engine (`canAttachLeader` full-set validation), data (`co_leader_eligible_with`
on 12 SM named-shape units, `co_leader_any` on 6 DG generic-shape units), render (`renderList` loops all
attached leaders), duplicate (`duplicateUnit` iterates all attached leaders), weapon pools (`b18d_check.js`
green with leader-scoped pools). E9 is done (D139/D140). Ryan confirmed the rules cap is 2 (1 by default,
+1 when a datasheet lift clause applies), matching every source clause sampled. Reshape:
- **B7a (engine)** — add the stack-size cap-of-2 guard to `canAttachLeader` (D144's pairwise model is
  over-permissive without it). **CLOSED S90 (D158).** See B7a below.
- **B7b (design + data + render)** — the banked combined attached-unit popup, with per-stat asterisk
  markers for leader-conferred stat auras (Ryan's Q3 choice). See B7b below.


### B7a — leader-stack cap semantics (engine) — **CLOSED S90 (D158)**
D144's `canAttachLeader` ran pairwise-permits with no stack-size cap. Under Ryan's rule (cap of 1 by
default, +1 to 2 when a lift clause applies), a Captain + Lieutenant + Apothecary + Ancient stack could pass
pairwise but violate the cap. **Shipped:** a stack-size guard added to `canAttachLeader` — after the
`leaderEligible` check and before the pairwise-permits loop, refuse when the existing attached count is
already ≥ 2. `permitsCoLeader` unchanged (correct for the pair, D144). New `rules_assertions.py` guard
`B7a-1` (48/49 → 49/50). New `e10_check.js` scenario 6 (2-leader stack duplicate + cap refusal on the
duplicated body). Zero data change; `index.html` v5.76 → v5.77. Future note: an "unbounded exception" data
field (e.g., `leader_stack_cap_override`) will be needed when factions with special stacking clauses are
built (Cybernetica Datasmith / Kastelan Robots for AdMech; Boyz "up to 2 including a Warboss" for Orks); not
in scope for SM/DG.


### B7b — combined attached-unit popup with per-stat aura markers — **CLOSED S91 (D159); cluster: leader system**
Today `openModalConfigured` is per-entry — click a leader's ⓘ, see just that leader; click the bodyguard's
ⓘ, see just the bodyguard. There is no view of the fielded attached unit as a whole. Design (D157):
- **Shape.** Stacked panels in one modal. Header shows the composite unit name (e.g., "Intercessor Squad +
  Captain + Lieutenant"). Each attached member (bodyguard + N leaders) renders as its own panel using the
  existing `buildModalConfigured` renderer, separated by dividers. Matches how attached units work rules-wise
  (per 19.02–19.04, models keep their own profiles; nothing merges).
- **Trigger.** The bodyguard's ⓘ opens the combined view. Leader ⓘs stay as single-datasheet views.
- **Aura markers.** New data field on each unit's first model group, `bodyguard_stat_flags` — a list of
  stat names that this leader's unit abilities modify on the bodyguard. In the combined popup, the union
  of all attached leaders' flags is applied to the bodyguard's stat block as an asterisk on each flagged
  stat, cueing the reader to look at the abilities section for the specific rule. No numeric stat
  modification, no engine legality effect, no pricing effect. Reciprocal `leader_stat_flags` on bodyguard
  units for auras that flow the other direction (added when audit surfaces cases).
- **Markable stat list** (dev-manager call, revisable): INV, FNP, LD, T, M, OC. Rare stats (W, SV) added if
  audit surfaces them.
- **Data-classification pass.** Hand-audit of leader unit abilities across all built SM + DG units. Judgment
  calls on ambiguous cases (conditional modifiers like "4+ INV vs ranged attacks" — does the INV stat get a
  marker, or is that too conditional?) will be batched and surfaced together, not one at a time.
- **Order of build**: after B7a. Design turn first (small — modal composition + trigger routing), then
  data-audit turn, then render+wire turn. Data audit is the heaviest single piece.

**S91 shipped:** Audit walked all 81 SM+DG leader units against the markable-stat list. **16 leaders** carry
non-empty flags: 1 INV (Librarian, Mental Fortress 4+ invuln), 7 FNP (Sanguinary Priest + Iron Father Feirros
unconditional; Librarian, Librarian In Terminator Armour, Librarian In Phobos Armour, Chief Librarian
Tigurius, Chaplain In Terminator Armour, Ezekiel conditional-Psychic/mortal), 5 OC (Bladeguard Ancient,
Ancient In Terminator Armour, Ancient, Ravenwing Command Squad, Icon Bearer), 2 M (Njal Stormcaller +6"
during Advance, Noxious Blightbringer +1" unconditional), 1 T (Chaplain Grimaldus, Column from the Major
Altar Temple Relic). Zero LD. Ambiguity calls batched into D159 (all reversible): conditional FNP flagged;
temporary M flagged; Temple-Relic-select T flagged; RCS OC flagged under merged-unit rule (19.02–19.04).
Everything not flagged: weapon-ability auras ([LETHAL HITS] etc.), roll modifiers (Hit/Wound/Charge/Advance),
ability grants (Fights First, Scouts, Stealth), army-wide fielding effects (INSPIRING COMMANDER), self-only
auras, defensive rules that don't modify a stat (subtract-from-Damage, subtract-from-Wound). **New
`add_bodyguard_stat_flags.py` script** in the units.json rebuild chain, following the `add_co_leader.py`
precedent — hardcoded flag map keyed by unit_id, hand-verified, idempotent, guards for missing/drifted ids.
Every model group gets `bodyguard_stat_flags` (empty list default) so consumers read it unconditionally.
**Render layer**: new `openModalCombined` + `buildModalCombined` functions; `buildModalConfigured` takes an
optional `auraFlags` parameter that only applies to the first model group; `buildStatTable` gains the
`auraFlags` parameter and grows asterisk support for LD, T, M, OC (INV/FNP/W/SV already had it via B15/D112).
Legend text adapts: `* see Abilities` when aura stars fire, `* see Wargear Abilities` otherwise. Bodyguard
info button routes conditionally — `openModalCombined` when attached leaders exist, `openModalConfigured`
otherwise. Leader ⓘs unchanged (single-datasheet view). New `rules_assertions.py` guard `B7b-1` (49/50 → 50/51):
verifies the exact 16-leader flag set matches the audit, no unit is missing the field, and all render
functions exist with the expected signatures + wiring. `index.html` v5.77 → v5.78. `units.json` changed
(byte-identical repro via updated chain). Reciprocal `leader_stat_flags` not populated this pass — no audit
case surfaced (Ryan can revisit if desired).

---


### B8 — Unit classification mis-buckets multi-model units — **CLOSED (D71, v5.36→v5.37) — backlog entry was stale, corrected S92**
Left-panel section comes from `unit_type`, which reads the FULL keyword set
including model-specific keywords. Symptoms: Victrix Honour Guard → Epic Hero
(the EPIC HERO on Chapter Ancient/Champion leaks up) and Ravenwing Command Squad →
Mounted (its Character is model-specific on the Ravenwing Champion, so it doesn't
promote the unit).

**Shipped.** `wahapedia_transform.py`'s `unit_type` already classifies from the union of
all-models keywords and the namesake model's keywords (D71) — this entry was left open in
error after D71 shipped. Confirmed against the current committed `units.json`: Victrix
Honour Guard → Infantry, Ravenwing Command Squad → Character. No new work needed; S92
kickoff's B8 pick is void — see S92 handoff for the replacement pick.


### B9 — Company Heroes weapon counts (heterogeneous fixed group) — **SHIPPED**
Company Heroes showed master-crafted bolt rifle / heavy bolter ×2 (should be ×1).
Root cause: the two Company Veterans carry *different* weapons ("One Company Veteran
… heavy bolter" / "One … bolt rifle"), but the parser collapsed them into one
2-model group with the weapons unioned, and the rollup multiplied each by the group
size. Fix (`equipped_parser`): when a fixed-N group receives exactly N singular
("One <model>…") equip lines and has no scoped options, split it into N one-model
sub-groups named by their distinguishing weapon. Only Company Heroes matches this
shape across SM+DG. Strict diff: 1 of 217 loadout entries changed.
Ships as `equipped_parser.py`, regenerated `unit_loadouts.json`, `index.html` v5.38.
The Victrix half of the original B9 moved out to B13 — it's not the same bug.


### B13 — Victrix embedded Epic Heroes: optional-model toggle + 1-per-army cap — **CLOSED (D158 Piece 1 v5.79 S92; D159 Piece 2 v5.80 S93)**

**Rules:** Ancient and Champion replace Victrix body models — unit is always 3 or 6 total. No separate points cost (MFM prices only "3 models / 6 models" brackets).

**Piece 1 (D158, v5.79, S92):** `loOptCounts` helper; `loGroupCounts` and `loRollup` accept opt-state; `editLoadoutOptional` handler; green-tinted toggle render block in config panel; EPIC HERO suffix stripped from display name; makeup line self-corrects. All 6 `loGroupCounts` and 5 `loRollup` call sites threaded through.

**Piece 2 (D159, v5.80, S93):** `isOptEpicHeroBlocked` detects embedded Epic Hero groups by "EPIC HERO" substring in optional group name (no new data field needed). `editLoadoutOptional` guards toggle-on; render shows `.blocked` button + note when cap consumed by another entry. Assertion B13-1 added (51/52).


### B10 — DW Decimus Kill Team: no config options / not attachable — **CLOSED (stale; corrected S92)**
Both symptoms were already resolved before S92. Decimus (`000004175`) is fully present in `unit_loadouts.json`
with 4 count-swap options (cc_1, cnt_2, cnt_3, cnt_4). It appears in `units.json` under the Deathwatch army
block (`unit_type: Battleline`). 28 leaders list `Decimus Kill Team` in their `leader_eligible_units` (the
transform already expands the "attached to Intercessor Squad" indirection from Wahapedia's `Datasheets_leader.csv`).
The engine's `canAttachLeader` check reads those lists correctly. Deathwatch is `built: true` in
`faction_taxonomy.json`. No work needed; entry was left open in error.


### B11 — SV/LD data carries a trailing "+" while INV/FNP are bare — **CLOSED S109 (D177)**
Fixed at the source: `wahapedia_transform.py` now strips a trailing "+" off SV/LD when
read from `Datasheets_models.csv`, before it reaches `Unit_Stats.csv`. `units.json`
regenerated — 450 SV/LD values moved from `"N+"` string to bare `N`, no other field
changed (full JSON diff-guard against the pipeline rebuild). The v5.35 render guard
(`cleanPlus`) is now a provable no-op for SV/LD; left in place as harmless.


### B12 — Wargear stat effects not applied to the statline — **CLOSED (v5.39–v5.42)**
Done: stat-override machinery reaches units via the bundle picker on loadout-defined
units and applies to INV/FNP as well as SV/W (D73/D74). The "b" remainder shipped in
v5.42 (D75): a general reader parses a wargear/ability's text (`N+ invulnerable save`,
`Wounds characteristic of N`, `Save characteristic of N+`, `Feel No Pain N+`) into a
stat override, wired to active bundle-grant `carrier_notes` (authored override wins)
and active weapon/wargear abilities. Shining Aegis is de-hardcoded. Also fixed a bug:
the foot Captain relic shield is W 6, not the W 7 shipped last session (that value
belongs to Wolf Lord on Thunderwolf / Captain on Bike). The always-on payoff (Helix
Gauntlet FNP) remains gated on B14. See **B15** for the broad surface.


### B15 — Conferred always-on wargear characteristics not on the statline (broad pass) — **CLOSED S53 (D112, v5.59)**
Shipped. The real fault was the *file*: `weapon_abilities.json` is name-keyed and flattens Storm Shield to one
text. New `datasheet_wargear_abilities.json` restores the datasheet key; `conferredStats()` applies the D105
three-way carrier-count rule (all → override, some → asterisk on W/SV/INV/FNP, none → inert) against the
*configured* loadout, scoped to the statline group where that group can be mapped to loadout groups and capped
at an asterisk where it cannot. Asserted B15-8..11.

_Original text below, retained for the record:_
The claimed W5 -> W4 regression on Wolf Guard Battle Leader does not exist: `Datasheets_abilities.csv 000004130` reads *Wounds characteristic of 6* against a printed W5. Ability text is per-datasheet (D70) and always was. No Ryan call needed. Build with E17 under the D105 carrier-count rule. Facts locked in `rules_assertions.py`.

_Original text below, retained for the record:_
**Shipped (D88):** broad reader wired to `wargear_ability_names` in both statline views, with the
conditional/summon sentence guard, grant-gated skip, and single/uniform-vs-multi-model-bearer
classification. Writes **INV and FNP only** — 5 groups now carry a correct broad INV (both
Impulsors INV5, both SW Dreadnoughts INV4, Azrael INV4 no-op). **HELD — needs Ryan:** the W/SV
(characteristic-*override*) writes. The shared glossary text hardcodes a per-datasheet number
("Storm Shield → Wounds characteristic of 4") that regresses on other carriers (Wolf Guard Battle
Leader W5→W4). Affected always-on W carriers: Captain w/ Jump Pack, Chaplain in Term Armour, Ancient
in Term Armour (Relic/Terminator Storm Shield → W6, all *increases*, likely correct) and Wolf Guard
Battle Leader (Storm Shield → W4, a *decrease*, wrong). Ryan's call: per-carrier verify or data-fix
the W/SV entries before they can be applied. **Multi-model bearer groups with a DEFAULT per-model
invuln** (Wardens, Deathwatch Vets, Decimus Kill Team) are now handled by **E17 asterisk (DONE, D89)**
— no whole-group value written. Units whose invuln is an OPTIONAL storm-shield swap (Terminator
Assault Squad, Wolf Guard Terminators/Headtakers, Thunderwolf Cavalry, Deathwatch Terminator Squad)
are NOT in E17's default-gear scope — banked as a separate option-swap-invuln pass.

Original scope note:
The v5.42 reader is wired only to bundle grants and active weapon/wargear abilities.
The larger surface — ~a dozen SM/DG units whose `wargear_ability_names` confer an
always-on invuln/wounds (Refractor Field INV5, Shield Dome INV5, Astartes/Blizzard
Shield INV4, Storm Shield, the Lion Helm unit-wide INV4, …) — still shows base stats
in the table while the Wargear Abilities section says otherwise. Apply the reader to
that surface: **uniform** effects (single-model Characters, groups where every model
carries the gear, "models in the unit have…") → real value in the cell; **per-model
"the bearer has…" on a multi-model group** (Wardens, Deathwatch Vets — only one model
gets it) → **E17 asterisk**, not a whole-group value; genuinely different model-groups
already render as separate statlines. **Hard requirement, discovered in v5.42:** the
reader matches its phrases even inside a conditional clause — the Lion Helm and Watcher
in the Dark both contain a once-per-battle summoned "Feel No Pain 4+" — so this pass
MUST add a conditional/bearer guard (reject matches under "once per battle", "in
addition", "against …", summon clauses) before writing any of these to the statline.


### B14 — Optional per-model wargear matcher ("1 X can be equipped with…") — **DONE (SM), D76**
Item adds now route to Other Options with an include/exclude toggle; item-only "one of
the following" lists emit as mutually-exclusive groups; the item's ability is removed
from the always-on surface and confers only when checked. Helix Gauntlet drives FNP 6+
through the reader (payoff live). Shipped SM only this pass (8 units). DG (Deathshroud
icon of despair) picks up the fix on the next DG regen; CD icons stay as-is (Gen-1,
not regenerated).


### B14b — Mixed weapon+item exclusive group (Impulsor group C) — **CLOSED (D99, S44)**
When a "one of the following" group mixes weapon systems and wargear items (Impulsor:
Ironhail skytalon array / bellicatus missile array / orbital comms array / shield
dome), the four are one pick-one set but split across Wargear Options (weapons) and
Other Options (items) with no shared exclusion key. **S35 finding — worse than "just
needs an exclusion key":** on both Impulsors (`000002568`, `000002786`) two of the four
options — *orbital comms array* and *shield dome* — don't reach the loadout at all; they
carry `WEAPON_NOT_FOUND` parser flags because they're equipment *items*, not weapons, and
fail the weapon-index lookup. So B14b is two parts, not one:
  1. **Parse the missing items** — route the two equipment items through the equipment
     allowlist (as `weapon_abilities.json`-style entries) so they land as options, the
     way SG1 did for the Sanguinary banner. Parser/data.
  2. **Cross-channel mutual-exclusion** — emit a shared group id spanning the four and
     have the app honour "pick at most one" across the weapon + item structures. Parser
     emits the key; **engine** enforces it. Engine change → separate turn from part 1.
Not a clean small win. Sequence part 1 (parser) first, then part 2 (engine) after.

**Closed S44 (D99).** Part 1 (D97) already dissolved part 2: the parser emits all four picks as **one**
`choice` option with the two items listed in `equipment_choices`, so one radio group spans weapons and
items and "pick at most one" holds by construction — no shared exclusion key needed. Verified on both
Impulsors and the Corvus Blackstar. **Part 3** (added S43 — the equipment channel on the *replacement*
side of a swap) shipped in the same turn as the new `equipment_parts` field; see D99. B14b is done.


### B18a — option scope: generic "models" means EVERY model group (uncapped shapes) — **CLOSED S58 (D120)**
The uncapped generic sentences — "Any number of models…", "All models in this unit…" — now fan out to one
option per model group, leader included. 22 sentences on 20 units; option count 291 -> 324. `index.html`
unchanged. Asserted **B18-4** (Assault Terminator Sergeant is in scope) and **B18-5** (the Plague Champion is
still correctly out of scope). D112's negative case runs and passes: at zero storm-shield carriers the
conferred W4 goes inert. **Option ids churned within the 20 affected units — saved lists will mis-resolve
their wargear picks on those units (accepted; see D120).**


### B18b — pooled cap on `count` options — **CLOSED S61 (D126); index.html v5.66**
Shipped. `loRollup`'s count loop and both `buildLoadoutHtml` count branches (counter + stepper max) now read
`pool_id` the way the add branch does, so co-pooled generic swaps lock each other out against one shared cap.
Engine only — data byte-identical; UI paths dormant until B18c seeds pooled counts. Original spec below.

_`pool_id` was read only inside `type === 'add'` branches of `index.html`. A capped generic swap ("For every 5
models in this unit, 1 model's X…") therefore could not share one unit-wide cap across model groups; fanning it
out would grant the allowance once per group. Fix taught `countOpts` to draw from `poolCap` the way `addOpts`
do. Source and reasoning: **D120**._


### B18c — fan the capped generic swaps (two clean units) — **CLOSED S65; DATA; `unit_loadouts.json` 217 units / 327 options**
Shipped. Ravenwing Black Knights `000000241` (Huntmaster was missing the swap, under-granting) and Ravenwing
Command Squad `000002748` (**live bug fixed** — swap was offered only on the Ancient; now correctly reaches any
of the 3 models) both gained fanned options via `fan_pooled_swaps` (promoted from the banked file into
`equipped_parser.py` proper — explicit allowlist `{000000241, 000002748}`; carrying-groups-only; uncontested
guard; additive ids `cnt_1__<group_slug>`; shared `pool_id`). Diff-guard confirmed **exactly these two units**
changed (other 268 byte-identical; `model_groups`/`default_weapons`/`_defaults_source` byte-identical within the
two). Differential sweep (4,229 scenarios, new-def option set) confirms zero rollup change outside the two units.
Committed-data cap confirmed directly: Command Squad @3 → 1 grenade launcher; RBK @3 → 1; RBK @6 → 2 — matches
legal count, not the pre-B18e over-grant. `repro_check.py` reproduces the new committed file byte-for-byte.
`pipeline_manifest.json` rebaselined by hand for `unit_loadouts.json` and `equipped_parser.py` (manifest script
still absent from repo sync — see carried custody item). **Remaining gate: Ryan's live-render eyeball** (add both
units, drive the grenade-launcher steppers past the cap, confirm the shared pool locks at 1 @3 in the UI) — no
harness checks the render itself.

**Why it did not ship (D128):** seeding this cross-group pooled count exposes a live engine bug — the shared
`pool_id` cap is enforced only on the status counter, not on the weapon/points rollup. With the fan applied, the
count cap breaks: Command Squad permits **3** grenade launchers @3 models (legal 1); RBK permits **2** @3 (legal 1).
Shipping the data alone would trade today's "right count, wrong model" for "right models, wrong count" — a count
regression. **B18c ships the turn after B18e lands, parser change unchanged.**

**Superseded plan note:** D127's "fan only when the source weapon is contested by no other option" gate was found
in S63 to match **eight** units, not two, and two of those (`000001183`, `000004138`) would gain an *illegal* swap
(sergeant storm bolter is restricted by a datasheet footnote). The structural gate is abandoned; scope is an
explicit allowlist. The remaining under-grant units move to **B18f**.


### B18d — capped generic swaps on leader-conflict units — **CLOSED S82 (D149); equipped_parser.py + unit_loadouts.json 217/336**
_S82 analysis found the engine already had the mutual-exclusion mechanism via weapon-consumption tracking in
the fixed-1-group path (taken + cUsed cross-check). No engine change was needed — ticket reclassified from
DATA+ENGINE to DATA-only. Parser extended: contested-slot bypass for hand-verified units, max_total gate,
compound carrier check, option-ID pool derivation. 9 new leader-copy options across 3 units: TWC (1), DWV (7),
TKT (1). 20 assertions in b18d_check.js all passing. See D149 for full details._

_No-op (recorded, closed for B18c/d): Indomitor Kill Team `000002781` — the per-5 swap's source weapon is carried
by only one group, correctly scoped today. Fortis Kill Team `000002780` — no generic capped per-N count swap (its
per-5 line is a bearer-gated add)._


### B18e — engine: enforce shared `pool_id` cap on the weapon rollup — **CLOSED S64 (D129); index.html v5.67**
The bug was narrower than the S63 read: `loRollup` has one count branch per group *type*, and only the **fixed-1
count branch** was pool-blind — it set `cap = min(loMaxCount, reqCap)` with no `pool_id` term and never charged
`poolUsed`. The multi-model count branch and both add branches were already pool-aware. Fix: teach the fixed-1
count branch to clamp `cap` by `poolCap − poolUsed` and charge `poolUsed`, mirroring its three siblings — so a pool
spanning any mix of fixed-1 and multi-model groups draws from one unit-wide cap on the emitted weapons and points,
not just the status counter. Non-pooled / single-group behaviour byte-identical; data byte-identical. New guarded
harness **`pool_check.js`** drives the two fixture defs and asserts the cross-group cap on weapons AND points; it
fails on the old engine (CS @3 → 3 GL; RBK @3 → 2; RBK @6 → 3) and passes on v5.67 (1 / 1 / 2). B18c unblocked.


### B18f — general capped-generic fan for remaining under-grant units — **CLOSED S83 (D150) — no defect; candidate list rested on a D116 misreading**
Opened S63 (D128) on the belief that the RBK/RCS under-grant B18c fixed also existed on other units, with four
"likely-clean" candidates to fan onto the sergeant. **S83 per-unit source review against D116 found the premise
wrong.** D116's rule keys on the option's scope subject: generic "1 **model**" reaches every group (leader
included); a **named body model type** ("1 Plague Marine's boltgun") is body-only and correctly excludes the
sergeant (B18-3 asserts this; "B18 must not widen these"). The RBK/RCS units that were legally fanned use
"1 model." Five of the six B18f candidates do **not**: Eradicator Squad `000000103` ("1 **Eradicator's**"),
Heavy Intercessor Squad `000001177` ("1 **Heavy Intercessor's**"), Deathwing Terminator Squad `000000230`
("1 **Deathwing Terminator**"), and both Terminator Squads `000001183`/`000004138` ("1 **Terminator's**") are all
named-body-type → body-only. Their sergeants are correctly out of scope; there is no under-grant and nothing to
fix. Fanning them would have handed those sergeants an illegal swap. (The S63 comment excluding the two Terminator
Squads on the cyclone footnote "* this model's storm bolter cannot be replaced" is a misread — that note is an
anti-double-dip on the cyclone sub-option, not a sergeant restriction — but its verdict is right for the other
reason.) The one genuine generic under-grant, Decimus Kill Team `000004175` ("1 **model's**"), is a second-body-
group case, split to **B18g**. Guard against this class of error split to **B18h**. `_FAN_UNIT_ALLOWLIST`
unchanged; no data shipped.


### B18g — Decimus Kill Team infernus heavy bolter: generic swap under-granted to a second body group — **CLOSED S86 (D153)**
Decimus Kill Team `000004175` is the only genuine B18f survivor. Its four swaps all use generic "1 model's," so
they reach every carrying group (D116). The infernus heavy bolter swap (`cc_1`) was scoped to **Deathwatch
Veterans**, but only **Gravis Veterans** carry the infernus heavy bolter.

**S85 findings (D152).** The fan mechanism cannot fix this. Only Gravis Veterans carry the infernus heavy bolter
(confirmed from Datasheets.csv loadout text — no individual DW Veteran carries it). The DW Veterans' 10-weapon
`default_weapons` list is a normalization artifact (union of all weapons across individual DW Veteran
sub-types), causing `_group_carries` to return a false positive. Fanning would keep the wrong copy (DW Veterans)
and add the right one (Gravis Veterans) — a shared pool across a carrier and a non-carrier.

**S86 fix (D153).** Targeted post-processing override in `equipped_parser.py` (after `fan_pooled_swaps`),
keyed to `000004175` + `cc_1`, sets `scope = 'Gravis Veterans'`. Not a fan — single-carrier scope fix. Pool
cap validates at both brackets: size 5 → cap 1 (1 Gravis carrier), size 10 → cap 2 (2 Gravis carriers).
Differential sweep: exactly one unit changed (`000004175`), exactly one field changed (`cc_1.scope`). All
checks pass on exit.


### B18h — executable D116 guard on the fan allowlist — **CLOSED S84 (D151)**
Added assertion `B18h-1` in `rules_assertions.py`, backed by `_fan_scope_qualifies` / `_fan_scope_is_generic`.
Checks every id in `_FAN_UNIT_ALLOWLIST` against its `Datasheets_options.csv` scope line and requires the
subject to be the generic word "model" (bare or possessive), never a named body type. A negative control
(Eradicator Squad `000000103`) proves the classifier discriminates rather than passing vacuously; a live test
(add `000000103` to the allowlist, confirm the assertion fails, revert) confirmed the guard would have caught
the S83 near-miss. Assertions 48 → 49; 48/49 pass (P3 unrelated known-fail).


### B18 (original) — **CLOSED S99 — every sub-item shipped; header was stale**
_S99 housekeeping: B18 carried forward on the open list purely as a header. Every sub-item is closed —
B18a (S58/D120), B18b (S61/D126), B18c (S65), B18d (S82/D149), B18e (S64/D129), B18f (S83/D150),
B18g (S86/D153), B18h (S84/D151). Nothing is outstanding under this label. Do not re-open B18 as a
build target; the individual sub-entries below hold the record._

**Originally: SUPERSEDED by B18a / B18b / B18c (D120)**
**The rule, from source, not from a summary.** The scope of an option is whatever its own sentence says.
A sentence that says a generic *model* — "All models in this unit", "Any number of models", "For every 5
models in this unit, 1 model…" — covers **every model group, leader included**. A sentence that **names the
body model type** — "1 Plague Marine's boltgun", "1 Scout's boltgun", "1 Terminator's storm bolter" — covers
that group only. This cuts across add-vs-swap: both come in both forms. The long-carried claim that *adds go
unit-wide and swaps stay in their group* is **false** and is retired by **D116**.

**Proof rows (asserted B18-1..3):** `Datasheets_options.csv 000000118 line 1` ("Any number of models" →
reaches the Assault Terminator Sergeant); `000002718 lines 1-2` (line 2 gates on the *Reiver Sergeant* holding
a bolt carbine, and line 1's "All models" swap is the only source of one — the gate proves the scope);
`000001044` (all five per-5 lines name "Plague Marine", so the Plague Champion is correctly excluded).

**Why it is not an engine turn.** The engine already has every mechanism required: an option scoped to a
leader group, and a `pool_id` sharing one cap across groups, both ship today (Intercessor
`grenade_launcher`/`grenade_launcher_sgt`; Reiver `add_3`/`add_4`). What is missing is the **scope written on
the option**, and `loadout_parser.py` writes it. `index.html` cannot recover what the parser discarded.
**B18 sat behind the parser rebuild. That rebuild landed in S57 (D118), so B18 is now the next turn.**

**Size.** 21 in-roster units carry a generic sentence and have a leader group; at least 11 exclude the leader
from every option today — Terminator Assault Squad `000000118`, Inceptor Squad `000000125`, Vanguard Veterans
w/ Jump Packs `000000147`, Ravenwing Black Knights `000000241`, Thunderwolf Cavalry `000000322`, Centurion
Devastators `000001193`, Blightlord Terminators `000001372`, Aggressors `000002099`, Centurion Assault
`000002703`, Ravenwing Command Squad `000002748`, Deathwatch Terminators `000003873`, Decimus Kill Team
`000004175`. The remainder have leader-scoped options for some lines but not the generic one; the per-option
split is the parser's to redo.

**Dependency worth naming.** D112's conferred-characteristic engine cannot reach its own negative case until
B18 lands: the Assault Terminator Sergeant cannot lose his storm shield, so the squad never reaches zero
carriers and the W4 override never reverts.


### SG1 — Sanguinary Guard banner (one-model item add) — **DONE (D85, S30)**
`000000165`: "One model can be equipped with 1 Sanguinary banner." now classifies via the new
`classify_one_model_add` (body-scoped, `max_total` 1, equipment). 3/6 size selector from
`size_brackets [3,6]`. Same run added **Diseased Icon** to the `weapon_abilities.json` equipment
allowlist so the classifier's other real instance — Death Guard Possessed `000001045`
("1 model can be equipped with 1 diseased icon") — resolves as equipment; Possessed is
out-of-roster (pruned), so no shipped data changed. Classifier is UNMATCHED-only → zero
regression.


### B14c — Bearer-qualified adds ("1 model equipped with a <weapon> can…") — **CLOSED S99 — all three parts shipped; header was stale**
_S99 housekeeping: like B18, B14c stayed on the open list as a header after all of its parts landed —
(a) resolved by B19 (S36/D91), (b) shipped as B14c(b) (S37/D92), (c) shipped S48/D103. Nothing outstanding.
Original rescope text retained below for the record._

**Originally: rescoped S35; NOT a minor parser item**
An add gated on the bearer still carrying a named weapon. **S35 investigation found the
"minor parser item" framing was wrong** — the pieces split three ways, and the pure-data
ones are inert today:

**(a) Gates that already exist but are DORMANT.** The `requires_weapon` mechanism only
fires when a **same-scope `choice`-type** option replaces the required weapon
(`reqOk`/`reqOkUI` in `index.html` inspect `type === 'choice'` only). But every in-roster
unit that carries one of these gates loses the weapon through **`count`-type** swaps, not
choices — so the gate never disqualifies anything. This is already true of the gates
shipped in D81/S28: **Spectrus** (`000002779`, marksman carbine removed by `cnt_4/5/6`)
and **Fortis** (`000002780`, bolt rifle) both have live `requires_weapon` values that
have no runtime effect. (D81/S28 noted "harmless today"; the reason is this choice-only
check.) → The real fix is engine, tracked as **B19** below. Until B19, adding more
`requires_weapon` values is writing dormant data.

**(b) Stale / un-gated data that B19 would activate.**
  - `000002285` **Death Company Marines w/ Bolt Rifles** — parser-generated; the current
    `classify_per_n` already emits `requires_weapon: 'bolt rifle'` on the grenade-launcher
    add, but the committed entry predates it (stale). Strip-from-existing → re-parse →
    splice (preserve `model_groups`/`default_weapons`) when B19 makes it matter.
  - `000001157` **Intercessor Squad** — **hand-authored** entry (semantic option ids, no
    `_parser_flags`); its main grenade-launcher add is un-gated. Hand-edit the authored
    entry to add the gate (parser won't touch preserved entries).
  - `000001044` **Plague Marines** — **hand-authored**; icon-of-despair add un-gated on
    "boltgun". Here the boltgun *is* swappable (blight launcher / spewer / bubotic / heavy,
    all `count`-type), so this one is a genuine legality case once B19 lands. Hand-edit the
    authored entry to add `requires_weapon: 'Boltgun'`.

**(c) Bearer-gated adds that don't parse at all (`UNMATCHED`) — **DONE (Session 48, D103)**.**
All three now parse. `000004135` Execrator (master-crafted power weapon, gated on the
absolvor bolt pistol), `000004182` Wolf Scouts (haywire mine, gated on a plasma pistol),
`000000083` Captain w/ Jump Pack (relic shield, gated on `Heavy bolt pistol + Astartes
chainsword` — the two-weapon combo). A gate may now name several weapons joined with ` + `;
the bearer must hold all of them. **The Captain's option is over-strict until B32 lands** —
see below.


### B14c(b) — bearer-gated adds, data half — **DONE (Session 37, D92)**
Death Company Marines `000002285` (re-parsed/spliced; `add_3` gated on Bolt rifle, `adds_weapon`
corrected to the base name), Intercessor `000001157` (body add gated on Bolt rifle; inert but
correct), Plague Marines `000001044` (icon of despair gated on Boltgun — the one live
tightening). Data-only; equipped chain fixed point holds at zero diff.


### B19 — `requires_weapon` gate: carrier counting (engine) — **DONE (Session 36, D91, v5.52)**
Replaced the choice-only `reqOk`/`reqOkUI` test with a real carrier count per scope group:
models holding the required weapon as default gear, minus models that swapped it away
(choice **or** count swaps), plus models that gained it from a swap or an add. Base-name
matching (so "Plasma incinerator" matches its `– standard`/`– supercharge` profiles) and
compound "A + B" replacements are split and counted. Gated options are now also **capped**
by the carrier count, not just switched off, and gated adds on non-leader groups are gated
at all for the first time (the rollup never called `reqOk` on them). Differential sweep of
54,800 random selections across all 217 units: exactly 2 units change (both gated), 0
ungated units affected.


### B20 — `count` swaps scoped to a single-model group are silently ignored (engine + data) — **CLOSED (D93 engine S38, D94 parser+data S39; stale entry corrected S92)**
Engine half (D93, v5.53): the rollup's `fixed: 1` branch now processes `count` options as well as
`choice` and `add`. Helbrute `cc_2` remained inert at that point because it still used `per_n_models: 5`
(floor(1/5)=0). Ravenwing Ancient `cnt_1` started working immediately. Data half (D94, S39):
`classify_n_model_swap` now emits `max_total: N` instead of `per_n_models: 5 / max_per_n: 1`, fixing
Helbrute (`cnt_2`, `cc_3` now both carry `max_total: 1`). Both units confirmed in committed data.


### B21 — Options mis-scoped to the base group when the required weapon lives in a variant group — **CLOSED S114 (D182)**
Four options, three units, one-line parser fix in `loadout_parser.py`'s indefinite-one-model
matcher (`classify_one_model_swap`). The scope hint on this branch used to be a hard-coded
`'body'`, so every "One model can replace its X with 1 Y" fell to the base group even when
the source or replaced weapon only lived in a variant group. It now derives the scope hint
from the swap's own gating weapon (`requires_weapon`, when named) or else the weapon being
replaced, and `resolve_scope` picks the model group whose name matches on word overlap. A
unit with no such variant group keeps the pre-existing behaviour — the base group wins the
overlap by default. Additive, verified in a full-pipeline diff-guard: exactly three units
changed across all 338 loadout definitions, holding four rescoped options between them, and
`model_groups` / `default_weapons` / `_defaults_source` are byte-identical on all three:

* Fortis `000002780` `cnt_4` — plasma pistol, gated on Plasma incinerator → "Kill Team
  Intercessors with plasma incinerators".
* Fortis `000002780` `cnt_5` — vengor launcher replaces superfrag rocket launcher → "Kill
  Team Intercessors with superfrag rocket launchers".
* Spectrus `000002779` `cnt_4` — instigator bolt carbine replaces bolt sniper rifle → "Kill
  Team Infiltrators with bolt sniper rifles".
* Indomitor `000002781` `cnt_2` — multi-melta replaces melta rifle → "Kill Team Heavy
  Intercessors with melta rifles".

Fix is in the parser, not the output; the committed `unit_loadouts.json` is byte-identical
to a fresh pipeline run. B59 no longer ships with B21 (see D182); it splits into its own
engine + data turns.


### B58 — banded optional model groups (0-N) are treated as 0-or-1 toggles — **CLOSED S113 (phase 1 D180 / phase 2 D181)**
`loGroupCounts` resolves every `count.optional` group to 0 or 1 (`c[g.name] = oc[g.name] || 0`),
and the `max` the parser already writes on those groups is read by nothing. Four Deathwatch kill
teams have a banded model mix inside a fixed 10-model unit and therefore **cannot be built legally
today** — only one model per band is reachable:

* `000002780` Fortis — 1 Sergeant, 2-9 base, 0-4 / 0-4 / 0-4 / 0-2 variants.
* `000002779` Spectrus — 3-10 base, 0-3 / 0-4 / 0-4 variants.
* `000002781` Indomitor — 3-10 base, 0-3 / 0-3 variants.
* `000003874` Talonstrike — 1 Sergeant, 2-9 base, 0-5 variant.

All four are single-bracket (10) and flat-priced per unit, so no per-model pricing is involved.

**Phase 1 (parser/data) — SHIPPED S112, D180.** `loadout_parser.py` now records the base group's
`min` (from the composition line's low bound) on every `fills_to_size` group, not only the four
above — the field is a property of the shared composition parser, and `repro_check.py`'s full-regen
model means it could not be scoped to four units without hard-coding unit_ids into the parser. 53
units gained the field; verified additive-only (diffed against the prior committed file — no option,
weapon, or default-weapon changes anywhere). New assertion **B58-1** checks every `fills_to_size`
group's `min` against its source composition line. `min` is not yet read by the engine (same as
`max` today) — no behavior change this session.

**Phase 2 (engine) — SHIPPED S113, D181, v5.85.** `loOptCounts` returns a model count clamped to the
band `max`; new `loOptHeadroom` computes the models available to the bands (size minus fixed and
per-bracket reservations minus the `fills_to_size` group's `min`); new `loOptMax` gives one group's
live ceiling once its siblings have drawn. `loGroupCounts` serves bands in declaration order, each
clamped by band and remaining headroom, so the body group can never fall below its minimum. UI: a
band wider than 1 is a stepper, a one-wide band keeps the Add/Included toggle as the degenerate
one-band case, and both run through one `editLoadoutOptional(listId, groupName, delta)` handler.
B56g's escort toggle was kept separate throughout, as required.

**Product call taken as recommended: hard-cap.** An over-band mix is unreachable, not flagged (D0). A
one-band group with no headroom renders disabled with a reason rather than as a dead button.

**Verified** by new harness `b58_check.js` (55 checks, including a global sweep over every unit with
an optional group at every bracket) and new assertion **B58-2**. All four kill teams now build legal
10-model mixes. One data defect surfaced in the process — see **B59**.



### B59 — Invader ATV should ride alongside the Outrider Squad and its +60 is uncharged — **CLOSED S116 (D182/D183/D184); SHIPPED ACROSS B59a + B59b**
Surfaced by B58 phase 2's headroom cap. Outriders `000002712` models the Invader ATV as a
**consuming** `optional` group (`max: 1`) sitting against a body group with `min: 2` plus a fixed
Sergeant. At the 3-model bracket that leaves zero headroom, so the ATV is unreachable there.
Confirmed rules facts (product owner, D182): one ATV per squad regardless of size (3 or 6); ATV
does not count toward the squad's model count; up to three ATVs total is a *consequence* of the
plain battle-size squad limit, not a constant; MFM is the pricing source (Outriders 70/140, ATV
a flat +60 across all seven MFM occurrences); embedded ATVs do NOT count against the standalone
Invader ATV datasheet `000001158`'s unit limit (D107-pinned as **B59-1**).

**Mechanism: `non_consuming: true` flag, not the D174 escort shape.** Fact 2 (constant count
regardless of bracket) rules out `per_bracket: {"3": 1, "6": 1}` — that encodes a constant as a
lookup table and would silently return 0 for a future third bracket. Hunting Wolves genuinely
vary with the bracket; the ATV does not. A `non_consuming: true` flag on a plain `optional`
group with `max: 1` states the one true rule, composes with B58's stepper if a banded
non-consuming escort ever appears, and costs one condition in each of `loOptHeadroom` and
`loGroupCounts`.

**Category distinction (D182), for the next embedded-model question.** Cap on the model →
follows the model (B13 Epic Hero: embedded Chapter Ancient DOES count against the army-wide
1-per-army). Cap on the datasheet selection → does not follow the model (B59 ATV: embedded
ATV does NOT count against standalone 000001158's limit). "Model-scoped" vs "selection-scoped."


### B59a — Engine: `non_consuming` handling in `loOptHeadroom` / `loGroupCounts` — **CLOSED S115 (D183); ENGINE-ONLY; M**
A group flagged `non_consuming: true` contributes zero reservation in `loOptHeadroom` (does
not eat body-group room) and its model count is not subtracted from remaining headroom in
`loGroupCounts` (does not compete with the bracket). Pin the wiring the way `B58-2` pins its
own. No data change in the same turn (turn-typing rule); the engine change is a no-op until
B59b flips a group.

**Shipped.** `index.html` v5.86: `loOptHeadroom` skips a `non_consuming` group's reservation
by name; `loGroupCounts`'s optional branch forks on the flag, clamping to band only with no
headroom deduction and no addition to `reserved`. New assertion `B59a-1` (61/62 suite, P3 the
known custody gap) pins both functions and passively checks `unit_loadouts.json` (0 flagged
groups today, as expected — B59b sets the first one). `repro_check.py` and
`units_repro_check.py` both byte-identical at close — confirmed no-op on current data. Full
harness suite re-run clean; `pts_check.js`'s pre-existing `000000118` note and
`bundle_check.js`'s 2 pre-existing B36 failures both unchanged.


### B59b — Data / parser: MFM additive-line parser + Outriders group flip — **CLOSED S116 (D184); DATA-ONLY; M**
Two parts of the same data turn:
1. `mfm_points_parser.py` learns the additive `• + 1 <name><N> pts` MFM line and emits a
   per-item price rather than dropping it entirely. The dropped `+ 1 Invader ATV 60 pts` line
   is a separate, older defect independent of B58 — the +60 has never been charged.
2. `unit_loadouts.json` `000002712`: the "Invader ATV" model group gains `non_consuming: true`
   and `price_per_model: 60`. Diff-guard: exactly `000002712` changes; the ATV +60 lands in
   `wargear_points.json` (or the MFM-priced structure the parser feeds).

Never encode "3" as a constant for the ATV ceiling — it falls out of the plain squad limit
(3 at Strike Force, 2 at Incursion; Outriders has no Battleline keyword).

**Shipped.** `mfm_points_parser.py` gained `ADDON_RE`, matched against every relevant MFM
file: all seven Space Marine family Invader ATV occurrences read a flat 60, zero
disagreement. The validated fact lands in a new `_addons` key in `wargear_points.json`
(audit trail only — kept out of the existing `items` lookup on purpose, since D173 already
rejected that shape for model-group pricing). `unit_loadouts.json` `000002712`'s Invader
ATV group gained `non_consuming: true` and `price_per_model: 60`; since neither field is
derivable from Wahapedia source, `000002712` became a fourth `HAND_AUTHORED` seed in
`repro_check.py`, the same class D175 established for the Hunting Wolves escort. Diff-guard
confirmed exactly `000002712` changed; `repro_check.py` and `units_repro_check.py` both
byte-identical. A stale `b58_check.js` section was found pinning the ORIGINAL bug (ATV
wrongly unreachable at bracket 3) as expected behavior — rewritten to assert the corrected
D182 behavior instead; the suite's global "total = size" invariant also gained a
`non_consuming` exclusion alongside its existing `per_bracket` one. `b58_check.js`: 56/56.
`rules_assertions.py`: 61/62 (P3 known custody gap, unchanged); `B59a-1`'s data-side check
now active (1 flagged group, no longer "0 expected"). Full harness suite re-run clean;
`pts_check.js`'s pre-existing `000000118` note and `bundle_check.js`'s 2 pre-existing B36
failures both unchanged. **B59 fully closes.**


### B32 — engine: `requires_weapon` with more than one weapon — **CLOSED S49 (v5.57)**
`loReqCarriers` now splits the gate with `loWeaponParts` and returns the **minimum** carrier
count across the parts, so the bearer must hold every named weapon. A single-name gate splits
to one part and is unchanged by construction. The disabled row reads the gate as prose
("needs Heavy bolt pistol and Astartes chainsword") via a new `loReqLabel`. Verified with
`sweep.js` (one dataset, two engines): 3,290 cases, 1 diff, `000000083` only — the relic
shield appears when the Captain still holds both weapons and stays suppressed the moment
either is swapped away.


### B33 — negated gates — **CLOSED S50 (data)**
Shipped as two independent single-model adds, **not** as a pooled mutual exclusion.
D104's diagnosis was right (the classifier must refuse a negated gate) but its proposed
remedy was wrong: the exclusion in "1 Plaguebearer that is not equipped with a daemonic
icon can be equipped with 1 instrument of Chaos" is **per model**, not per unit. One model
takes the icon, a different model takes the instrument, and both are legal in the same unit.
A pooled exclusion would have made a legal list unbuildable. Corrected in **D106**;
`000004113` / `000004114` now each carry an ungated, unpooled icon add and instrument add,
both capped at 1. No engine change was needed. Asserted as B33-1/2/3 in `rules_assertions.py`.


### B35 — paid wargear options — **CLOSED (data half S51, engine half S52)**
**Wargear is not free.** See **D107** (the fact), **D108** (the pricing rule), **D109** (the real counts),
**D110** (the price is keyed by datasheet id), **D111** (how the engine charges it).

**Data half — S51.** `mfm_points_parser.py --wargear` produces `wargear_points.json`:
`datasheet_id -> items -> lowercased item name -> {cost, display, source}`. Nine priced items on seven
units; twenty more resolve to real datasheet ids and are held out until their factions land. Asserted
**B35-1..5**.

**Engine half — S52.** `index.html` v5.58 loads `wargear_points.json`; `ptsForEntry` adds a
rollup-driven sum (`count × cost` over both the `weapons` and `equipment` maps of `loRollup`, matched
through `weaponBase().toLowerCase()`); entry points are now derived on every render rather than only on
size change, so a wargear click moves the total. The roster "from" badge carries the default loadout's
priced wargear too (Terminator Assault Squad advertises 180, not 155). Asserted **B35-6..8**;
`pts_check.js` is the regression harness. `sweep.js`: 3299 cases, zero rollup diffs.

**Left for later, deliberately:** the price is charged per item carried, which is what the MFM says. If a
unit is ever found where an item is priced but only some copies of it should be charged, that is a new
decision, not a bug in this shape.


### B34 — Size-gated wargear swaps (`required_size`) — **CLOSED S95 (D160 + D161)**

**Piece 2 (engine) — shipped S95 / D161.** `index.html` v5.80 → v5.81.
`loRollup` filters `def.options → sizeActiveOptions` at entry so options whose
`required_size` doesn't equal the current bracket contribute nothing to the
byScope split or the pool-cap init loops. `buildLoadoutHtml` gains a
`sizeGated(o)` predicate folded into the existing `suppressed(o)` chain, so
size-gated options are hidden from the config panel at non-matching brackets
and the stale-selection clear (line 3899-3900) drops any pick a user made
before dropping the unit's model count. New JS guard `required_size_check.js`
(NET NEW) proves the gate at every declared bracket on both units:
suppression at non-matching brackets (Wolf Scouts @6, Blightlord @5 and @10)
and correct firing at the matching bracket (Wolf Scouts @12, Blightlord @3),
with source consumption on the compound Blightlord swap verified across both
weapons. New data-integrity assertion **B34-2** in `rules_assertions.py`
confirms every `required_size` value is a member of that unit's declared
`size_brackets` (catches a stale gate if brackets ever change). Assertions
52/53 → 53/54 (P3 known-fail unchanged).

**Piece 1 (data + parser) — shipped S94 / D160.** Two units carry a swap that
is only legal at one specific unit size: Wolf Scouts `000004182` (unlocks at 12
models: plasma pistol → instigator bolt carbine) and Blightlord Terminators
`000001372` (unlocks at *only* 3 models: combi-bolter + bubotic blade → plague
spewer + close combat weapon). Both were `UNMATCHED` in `unit_loadouts.json`
and the swaps were silently absent. Blast-radius grep confirmed no other unit
carries this pattern. New classifier `classify_size_gated_swap` in
`loadout_parser.py` emits count ops with `required_size:N` (exact-match integer,
not a floor — Blightlord unlocks at the bottom bracket, so `min_unit_size`
would get it backwards). `rules_assertions.py` gained **B34-1**. Diff-guard
confirmed exactly those two units changed; no collateral.


### B42 — Vanguard Veterans' storm shield is missing from the loadout def — **CLOSED S58**
Root cause: GW drops its own "with" on `Datasheets_options.csv 000000147 line 1` ("...bolt pistol replaced
one of the following"), so `classify_any_number` never matched and the whole line was UNMATCHED. The parser
now tolerates the missing "with". The storm shield resolves through the equipment allowlist and lands as
`equipment_parts` on both the Sergeant and the body option. Asserted **B42-1**.

#### original note
`000000147` carries `wargear_ability_names: ['Storm Shield']` (INV 4+ per `Datasheets_abilities.csv
000000147`) but the item appears nowhere in its `unit_loadouts.json` def — not as default gear, not as a
swap. The player cannot take it. The engine falls back to the legacy heuristic and asterisks the INV cell,
which is the safe answer but not the right one. Loadout data turn (needs the parser rebuilt first).


### B43 — Wardens of Ultramar: Refractor Field has no carrier — **CLOSED S58 as a duplicate of B44 (D121)**
The carrier exists (`unit_loadouts.json 000004188`, Gaius Silva group, `default_wargear: ['refractor field']`).
The fault is that `units.json` splits `000004188` into two statline groups and `unit_loadouts.json` into six
loadout groups, and neither partition can address the other — which is B44 exactly. No data change made.

#### original note
`000004188` group 1 lists `Refractor Field` as a wargear ability but no model in the def holds the item, so
under D112 it now renders inert. Either the item is missing from the def (like B42) or the ability is
attached to the wrong statline group. Check against `Datasheets_wargear.csv 000004188` before deciding.


### B44 — statline groups and loadout groups have no shared key — **CLOSED S72 (D135 data half, D136 engine half)**
`units.json` splits a unit by statline; `unit_loadouts.json` splits it by loadout group, and the two namings
don't line up for 8 units (Outrider Squad, Wardens of Ultramar, Wolf Guard Headtakers, Wolf Scouts,
Talonstrike Kill Team, Decimus Kill Team, Chaplain Grimaldus, Crusader Squad) — a 9th, Pink Horrors, has no
loadout data at all and is out of scope. D112's name-matching heuristic silently undercounts on Wolf Scouts
(misses the Pack Leader) and can't attribute Outrider Squad at all (asterisk fallback).
**Shipped (data half, S71/D135):** a hand-verified `loadout_groups: []` key added to each of the 16 affected
statline groups, naming the loadout group(s) it corresponds to. New `add_loadout_groups.py`, run as the final
step of the `units.json` rebuild chain in `units_repro_check.py`.
**Shipped (engine half, S72/D136):** `index.html`'s `statGroupScopes()` now checks `mg.loadout_groups` first
(authoritative, skip the name-heuristic) and falls back to the existing comma-split matching only where the
field is absent. Verified against all 225 statline group entries in the committed data: exactly the 8 expected
groups changed behavior (Outrider Squad now attributable, Wolf Scouts undercount fixed, plus 6 more), 209
ungated entries byte-identical old vs new. `index.html` v5.69.


### B36 — Lieutenant wargear options are wrong — **CLOSED S54 (D113), `index.html` v5.60**
One cause behind all three symptoms: the Lieutenant's atomic 3-for-3 swap is written both as a
`bundled_swaps` endpoint and as a `unit_loadouts.json` choice option (`sng_2`), and both rendered. The
duplicate showed the neo-volkite twice, and its three-weapon `replaces` transitively merged the three
single-slot swaps into one B25 radio cluster. A loadout option that restates a bundle endpoint's `removes`
set is now never rendered, and bundle-managed families are tested part by part (which also removes the
Captain's redundant second pane). Acceptance test (as corrected by Ryan mid-session): **master-crafted bolter kept + heavy
bolt pistol + power fist** — legal, unbuildable in v5.59, builds in v5.60. Separately confirmed and asserted:
on the Lieutenant a plasma pistol replaces the *master-crafted bolter*, so "bolter kept + plasma pistol" is an
illegal build and stays refused. Proven by `bundle_check.js`.


### P3 — file-integrity manifest + reproduction gate — **DONE (Session 59, D123)**
Two machine-enforced guards, built as tooling ahead of B46 (no data, no engine). `pipeline_manifest.json`
holds the SHA-256 of 21 guarded files (five outputs, both parsers, the transform scripts, the harnesses, the
assertion files); assertion **P3** verifies them at baseline and names any wrong copy. `repro_check.py` runs
the full pipeline from source (loadout_parser + two hand-authored seeds → five web.txt passes → datasheets
pass) and asserts byte-identical reproduction of the committed `unit_loadouts.json`; **P1 is rewritten to be
this gate**, retiring its old function-name check. Regenerate the manifest at session close
(`python3 pipeline_manifest.py --write`). Proven by tampering: manifest caught a comment append; repro caught a
parser-generated unit divergence and named it. Assertions now **45/45**.


### B37 — Captain wargear panes are mislabelled — **CLOSED S88 (D156), no build needed**
Both option panes carry the same label, so the player cannot tell which slot is which. Per Ryan: the first
pane keeps or swaps the **entire wargear set**, the second swaps only the **close combat weapon**, and the
two are **mutually exclusive** — a swap in one must lock the other. Same cluster as B36. **S54: the known
half fixed by D113** — the Captain's bundle is `owns`, and its compound loadout option was leaking through
a whole-string `weaponBase` test and drawing a second pane; the fix made it a single 10-endpoint bundle
picker. **S88 reconfirm (D156):** traced the full render path against v5.76 — both parser-level options
(`cho_1`, `cho_2`) are suppressed before any pane is built, so the Captain renders exactly one control,
one label, mutually exclusive by construction. Ryan's truncated second note ("Second, if a selection...")
predates the D113 redesign and has no target left to attach to — a two-pane labelling/locking problem is
structurally impossible against the current single-control design. Closed with no code change.


### B38 — a second leader on one unit (co-leader) — **CLOSED S81 — B38-engine SHIPPED S79 (D145); B38a SHIPPED S80 (D146); B38b SHIPPED S81 (D147)**
Investigated `co_leader_eligible_with` on real data before designing anything (S77 pick), findings in D143.
**Ryan's decision (D144): (a) yes** — support true multi-leader with full-set validation, fixing today's
under-permissive one-leader-only behaviour. **(b) flag** — model the generic "any other single leader, not a
duplicate" shape (DG's clause) with a new explicit boolean, not by enumerating names.

**Design (D144).** Symmetric-pairwise check over the *full* attached set, order-independent — replaces the
current single-`.find` check in `canAttachLeader` that only validates against the first-found existing leader
(a real bug: SM legitimately stacks 3+ support characters on a Captain-led unit, and the single-check is
order-dependent for the 3rd+). New per-unit field `co_leader_any` (default false): "I may join a Bodyguard that
already has Leaders, co-eligible with any of them except a duplicate of my own datasheet."

**Sequencing — engine first, three clean turns, never mixed:**
1. **B38-engine — DONE (S79, D145).** `canAttachLeader` now validates the full attached set via
   `permitsCoLeader`, order-independent; `allUnits` also carries `coLeaderAny`. Confirmed zero behaviour
   change on real data (no-diff sweep) and all four D144 worked examples hold.
2. **B38a (data) — DONE (S80, D146).** `co_leader_eligible_with` populated on the 12 built SM named-shape
   units. Role-words resolved to keyword-carrying built datasheets (Captain: 25, Chapter Master: 8 — all
   named Epic Heroes, no built datasheet is literally named "Chapter Master", Lieutenant: 5, Execrator: 1),
   verified no overlap between the four keyword sets. Cato Sicarius → single-name list (Marneus Calgar in
   Armour of Antilochus). New pipeline step `add_co_leader.py`, run after `add_loadout_groups.py`. Diff-guard
   confirmed only the 12 target units changed. **Next up: B38b.**
3. **B38b (data) — DONE (S81, D147).** `co_leader_any` populated on the 6 built DG generic-shape units
   (Noxious Blightbringer, Foul Blightspawn, Biologus Putrifier, Plague Surgeon, Tallyman, Icon Bearer);
   footer wording re-verified byte-for-byte against committed data. New `Co-Leader Any` column added to
   `Unit_Stats.csv`'s write in `wahapedia_transform.py`, wired through `convert_to_json.py`. Same
   `add_co_leader.py` script reused (new `CO_LEADER_ANY_IDS` list + guard block). Diff-guard confirmed only
   the 6 target units carry `true`; every unit gained the new key at its `false` default (unavoidable
   schema-addition byte-diff).

**Residual nuance (flagged S81, not a blocker):** the pairwise model lets generic-flag units stack freely
(e.g. three DG support characters + a primary on one Plague Marines unit) — the literal reading of the
footer. Worth a quick New Recruit check if Ryan has a screenshot; revisit only if NR caps lower.

*(Superseded note: the D70-style "unit text wins over generic" precedence Ryan originally set here is already
handled — B2/D143 confirms the Leader display shows unit-specific text, not the generic Core rule.)*


### B39 — Bloodthirster options lock each other out wrongly — **CLOSED S67 (D131)**
Root cause (D130): the Bloodthirster carried BOTH the correct D36 `bundled_swaps` radio group AND a stale
flat `wargear_options` row "Lash of Khorne → Bloodflail" that the source does not support. `convert_to_json.py`
`_bundle_owns` only dropped flat swaps whose *replaced* family was in the bundle's *removes* set; the leftover
row's replaced family (Lash) was only *added* by the bundle, so it survived. **Fixed S67:** `_bundle_owns`
widened to own a flat option when its replaced OR replacement family is anywhere in the bundle's endpoints
(removes ∪ adds), scoped to model group. Applied to `units.json`; the leftover row is gone; nothing else in
the file changed. New guard `rules_assertions.py` `B39-1` verified real (fails pre-fix, passes post-fix).
**De-coupled from B18d** — B39 was a build-time data-dedup gap, NOT the runtime same-slot exclusion B18d needs.
B18d shipped S82 (D149) without any engine change — the existing weapon-consumption tracking already handled it.


### B39b — Audit the whole bundle queue for the same leftover-flat-swap class — **CLOSED S67 (D131)**
Audited all three units that carry `bundled_swaps` in the currently deployed `units.json` (Captain, Lieutenant,
Bloodthirster — that is the entire existing queue; the "27 bundled swaps + 17 compound replacements" figure
referenced in earlier handoffs is unbuilt future scope, not present in shipped data yet). Only Bloodthirster
had a leftover flat swap; Captain and Lieutenant already had empty `wargear_options` under the old predicate.
Full-file diff confirms exactly one unit changed. Closed — there is nothing further to audit until a new
bundle is built.


### P4 — RESOLVED S68 (D132). units.json rebuild fixed point re-established for all 14 blocks.
D131's diagnosis was wrong about mechanism: the rebuild had routed Chaos Daemons through
`wahapedia_transform.py --faction CD`, which pulls the raw Wahapedia CD-faction dump (74 datasheets,
including ~21 CSM/cultist units wrongly tagged CD via the Legiones Daemonica keyword) and silently
overwrites the real Gen-1 hand-built CD source — nine CSVs (`Unit_Stats.csv`, `Unit_Points.csv`, etc.)
that live at the project root and are `convert_to_json.py`'s literal default input filenames. Running
`convert_to_json.py` directly against the project root (no transform step) for CD reproduces the exact
53-unit roster. Real content found and fixed: Soul Grinder's Warpsword→Warpclaw option and Keeper of
Secrets' "Shining Aegis" profile were both missing from the stale committed file (source was already
correct); Plaguebearers/Plague Drones' icon routing (flagged in D131) was also source-corrected, committed
stale. `units.json` replaced; new `units_repro_check.py` added as a standing guard (analogue of
`repro_check.py`), its docstring stating explicitly that CD must never be routed through
`wahapedia_transform.py`. See D132 for full detail.


### B40 — Bloodmaster is missing its Leader rule — **CLOSED S69 (D133), not a bug**
Not a data drop or a render bug. The Bloodmaster carries its full leader setup end to end — `leader_ability_name`,
`leader_eligible_units = [Bloodletters]`, the datasheet-specific "Bloodmaster" (+1 Wound while leading) and
"A Gory Path" abilities, all in source (Gen-1 CD), all in `units.json`, all resolving to description text, and the
attachment mechanic reads the eligible list. What Ryan was actually pointing at — the Leader section should show the
character's *attachment* rule (which units it can lead) instead of the generic core "Leader" blurb — is real product
work, now tracked as **B49**. See D133.


### B41 — Epic Heroes: adding past the limit should be blocked, not flagged — **CLOSED S55 (D114 + D115)**
Shipped in `index.html` v5.62 as a hard block on **every** datasheet limit, not just Epic Heroes.
`limitState()` is the single predicate; `addUnitFromRoster` refuses an add at the limit and flashes the banner.
D114's source caveat was cleared the same session: `Army_Muster_Rules.txt` 25.03 arrived and showed the limits
**depend on battle size** — Incursion 2 / 4 / 1, Strike Force 3 / 6 / 1. The old flat 3 / 6 / 1 was the Strike
Force row applied to both, which permitted an illegal Incursion list. Fixed in D115.

*Original entry:*
`instanceLimit` already returns 1 for Epic Heroes and `entryHasError` already flags a breach, but
`addUnitFromRoster` still lets the player add a second copy and then shows it as an error. Ryan wants the
add **refused** for Epic Heroes. Open question (see "Decisions needed", S52): whether every datasheet limit
(3 per datasheet, 6 for Battleline / Dedicated Transport) should also be a hard block, since D0 says the
app enforces legality rather than reporting it. Recommendation: hard-block all of them.


### B45 — army-level legality rules — **CLOSED S100 — header retired S73 (D137), fully re-homed; kept surfacing as a candidate pick**
Was a single label over five army-muster rules from `Army_Muster_Rules.txt` 25.03/25.04. Scoped in S73:
four of the five are gated behind systems that do not exist yet, so B45 is not a session — it is a pointer.
Retired; each sub-rule now lives in its real owner. Do not re-open B45 as a build target.

1. **Detachment Points** (2 Incursion / 3 Strike Force, no duplicate detachments; detachment rules may
   require/forbid units) → **E1**. SCOPED S122 (D192) — see E1/E1a/E1b/E1c; the require/forbid half
   split out to **E21**.
2. **Enhancement limit** (2/4 by battle size, CHARACTER-only, no EPIC HEROES, no duplicates; `Upgrade`
   exception — non-Characters allowed, up to 3 of the same, 2nd/3rd cost points but don't count) → **E4**.
   E4 unblocks when E1c lands; S122 confirmed the seam is clean — enhancements arrive priced and
   Upgrade-flagged inside the E1a record, so E4 is a UI + limits ticket, not a data build.
3. **Warlord** (exactly one CHARACTER unit with the army faction keyword; one CHARACTER model within it;
   "must be Warlord" datasheets force the pick; "cannot be Warlord" beats "must be") → **E9**. See E9 below —
   this reshaped E9 into a data turn + an engine turn after the SUPREME COMMANDER propagation gap was found.
4. **Support units must be attached** (every support unit attached to a bodyguard) → **B38**. Blocked:
   attachment is not yet modelled as army state (`co_leader_eligible_with` captured since S69, but not consumed).
5. **Army faction keyword** → **CLOSED, pending one verification pass**. The app enforces this by faction
   selection rather than by keyword; for the v1 factions the picker is the effective keyword gate. A one-time
   check that faction == keyword for the built factions is worth doing but is not a build.


### E14 — Free, unconditional adds default to selected — **CLOSED S56 (D117, v5.63)**
`loIsFreeDefaultAdd` + `loadoutDefaultWargear`; `addUnitFromRoster` seeds `entry.wargear`. **53 options
across 33 units** default ticked (hunter-killer missiles, storm bolters, havoc launchers, Icarus pods,
ironhail stubbers, Watcher in the Dark, Sanguinary Banner, Daemonic Icon, Instrument of Chaos). The toggle
still clears them — a default is a convenience, never a lock. Saved lists are not re-seeded on load, so no
existing list moves under the player. "Free" is checked by rebuilding the MFM prices with the real parser and
confirming no seeded item is priced **for its own unit** — the corpus-wide grep is wrong, because the MFM does
price a multi-melta, on a *Sororitas* datasheet. Harness: `default_check.js` (new). Asserted E14-1, E14-2.

**Left out, and open (see Decisions with Ryan):** priced adds (by rule), **per-N / pooled stepper adds** (4
options: Reiver grav-chute and grapnel launcher; plus the pooled Intercessor grenade launcher), and **gated
adds** (`requires_weapon`, 11 options). The seed is a one-shot written at add time and cannot follow a value
that moves afterwards — a stepper's ceiling moves with unit size, and a gate can break and heal. A *live*
default needs a tri-state selection (unset / on / off) so a deliberate clear survives; that rewrites saved
lists on load and was not taken.


### B46 — wargear abilities granted by an OPTION never reach the popup — **DONE (Session 59, D122; index.html v5.64)**
Shipped. `allWargearAbilityNames(raw)` unions `units.json → wargear_ability_names` with the keys of
`datasheet_wargear_abilities.json[unit_id]`, and both popups name their abilities from it. Browse popup shows
all of it; configured popup filters by unit-wide carrier count on D112's three-way rule (all -> plain, some ->
asterisked row plus a one-line note, none -> not rendered). `loDefNamesItem` now eats `o.equipment`, without
which no equipment add could be counted at all. Asserted: `rules_assertions.py` B46-2 (channel + zero
unreachable), `stat_check.js` section 6 (Reiver 000002718, Infiltrator 000000128, Terminator Assault Squad
000000118). `unit_loadouts.json` and `units.json` byte-identical.

_Original text below:_

**Symptom (Ryan, S56).**
A Reiver Squad's popup lists no Grapnel Launcher and no Reiver Grav-chute, under
Abilities, Rules or anywhere else — so there is no way to find out what taking one does.

**Root cause, found.** Both popups build their **Wargear Abilities** list from
`units.json → model_groups[].wargear_ability_names`, and that field is populated from **default-issue gear
only**. The Reiver groups have `wargear_ability_names: []`. The ability text is not missing from the data —
it is in `Datasheets_abilities.csv 000002718` lines **5** (Grapnel Launcher) and **6** (Reiver Grav-chute),
both `type = Wargear`, and it is already in `datasheet_wargear_abilities.json` (D112's file, built straight
from those rows). The text is orphaned: the **control** lives in the loadout options, the **text** lives in
`other_options[].carrier_notes`, and the popup's list reads **neither**.

`conferredStats` cannot be the fix. It walks `wargear_ability_names`, it **skips** any ability named by an
`other_option` or a bundle grant (`gated`), and it drops any ability that does not parse to a stat override
(`if (!keys.length) continue`). Deep Strike and "ignore vertical distance" are not stat overrides, so they
are invisible to it by design.

**The fix.** Source the Wargear Abilities *list* from `datasheet_wargear_abilities.json` (the datasheet's own
`type = Wargear` rows — complete), unioned with `wargear_ability_names`. Then:
- **browse popup** — list all of them. That popup *is* the datasheet.
- **configured popup** — list the ones this build actually carries, via the existing `wargearCarrierState` /
  `loCarriers` machinery, summed across model groups. Zero carriers → out (the D112 rule, extended from
  characteristics to plain ability text).

**The 8 affected units** (`datasheet_wargear_abilities.json` has a row `units.json` does not list):
Infiltrator Squad `000000128` (Helix Gauntlet, Infiltrator Comms Array), Sanguinary Guard `000000165`
(Sanguinary Banner), Deathwing Terminator Squad `000000230` and Deathwing Knights `000000231` (Watcher in
the Dark), Corvus Blackstar `000000358` (Auspex Array, Infernum Halo-launcher), Incursor Squad `000001159`
(Haywire Mine), Reiver Squad `000002718` (Grapnel Launcher, Reiver Grav-chute), Spectrus Kill Team
`000002779` (Helix Gauntlet, Infiltrator Comms Array — partial; some are listed).

**Sharper after E14.** Six of these eight are now seeded ON by default (D117), so the player is *given* gear
whose rules text the app will not show them.


### B47 — information buttons on every configurable item and every option group (Configuration Panel) — **DONE (Session 60, D124). v5.64 → v5.65**
Shipped. Eye per selectable row (weapon profile / wargear rules text / short note for a bare item), list (☰)
per group heading opening every item at once, (picked/allowed) counter per heading, all at every nesting level
including the weapons a bundle endpoint adds. Detail lands as an **inline expander under the row** (Ryan's shape
call, recommended and taken). Read-only DOM toggle that does not re-render — an open expander collapses only on
the next selection change (accepted for v1). Counter semantics chosen as dev-manager (allowed = capacity from
`loMaxCount`/pool/1-per-slot; picked = current selections); a different reading is one line per surface. See
D124 for the full note and the helper list.

Original spec kept below for reference:
**Two controls, not one.** New Recruit's Lieutenant panel shows the reference behaviour:

- **Eye icon — per item.** Every selectable row carries one: every weapon choice ("Power fist", "Heavy Bolt
  Pistol", "Plasma pistol"), every wargear item, and the *bundle endpoint label itself* ("Pistol,
  Master-crafted Bolter & Melee Weapon"). It opens the detail for that one thing — the weapon profile for a
  weapon, the ability text for a piece of wargear.
- **List icon (☰) — per group heading.** It sits on the heading beside the counter: `Wargear (1/1) ☰`,
  `Melee Weapon (1/1) ☰`, `Pistol (1/1) ☰`, `Replace Bolter (1/1) ☰`. It opens the detail for **every item in
  that group at once**, so the alternatives can be compared without opening and closing four popups.

**Both icons appear at every level of nesting**, including inside an expanded bundle endpoint. NR also puts a
**(picked / allowed)** counter on every group heading — we have the same information (`loMaxCount`, the pool
lines) but do not show it as a counter. Worth taking in the same turn; it is the same heading row.

**Where the content comes from.** Weapon profiles: `raw.weapons` (already rendered in the popup). Wargear
ability text: `datasheet_wargear_abilities.json` — **which is exactly what B46 is about**. Do B46 first or
half of B47's items will open an empty box.

**Open, small:** whether the detail lands as a popup, an inline expander under the row, or a side sheet.
*Recommendation: inline expander under the row.* The panel is already the narrowest column and a popup over it
hides the very list you are choosing from; NR's own icons open in place.


### B48 — Corvus Blackstar renders two controls for the same wargear — **DONE (Session 60, D125). Rode with B47**
Shipped. Precondition confirmed against source (Datasheets_options.csv `000000358` line 4 — "one of the
following", optional): `ach_4` has `replaces: null`, so `buildLoadoutHtml` renders a **None** row and the empty
state stays reachable. Fix: `buildOtherOptionsHtml` suppression now also matches a loadout option's
`choices`/`equipment_choices`/`equipment`, not just `label`/`group`. Full-270 scan: suppresses exactly Corvus's
two options and nothing else. Corvus now offers None / Auspex Array / Infernum Halo-launcher through the single
`ach_4` radio.

Original spec kept below for reference:
Found while sourcing B46. `000000358` is the only unit where an item is double-sourced *and* the existing
suppression misses it. `buildOtherOptionsHtml` suppresses a B14 other-option when its name matches a loadout
option's `label`/`group` — but the Corvus's Auspex Array and Infernum Halo-launcher sit inside a **choice**
(`unit_loadouts.json 000000358 ach_4`, `group: "Wargear"`, `choices: [Auspex Array, Infernum Halo-launcher]`),
so the names live in `choices`, not in the group label. Both the loadout radio and the two other-option
checkboxes render, and the two channels confer independently. Sweep of all 270 units: **Corvus only.**
The suppression should also match a loadout option's `choices` / `equipment_choices` / `equipment` — but check
first that the loadout choice can express *neither item taken*, or suppressing the checkboxes would make the
"take nothing" state unreachable. Not a B46 regression; it predates it.


### B49 — Leader section: show the character's attachment rule, not the generic core "Leader" blurb — **CLOSED S70 (D134)**
The datasheet's "Leader" block now appears as its own section stating which units the character can lead (plus any
extra attachment clause), instead of the generic core-rules "Leader" text.

**Shipped.** `index.html` v5.68. Dedicated **Leader** section, NOT merged into Abilities, placed first among the ability
sections in both popups; body = "This model can be attached to the following unit(s): <resolved `leader_eligible_units`>"
with singular/plural auto-switch, plus `leader_footer` HTML injected verbatim where present; generic "Leader" line
dropped from Rules so it isn't shown twice; `.kwb` CSS rule added so retained keyword markup bolds. Gate is
`leader_ability_name` set + eligible list non-empty — correctly renders the multi-group case (Chaplain Grimaldus, one
label per profile) and correctly suppresses the one data quirk with a populated eligible list but no real Leader ability
(Wardens of Ultramar). `units.json` byte-identical (engine-only). Feeds future leader-assignment enforcement (relates
to B38).


### E15 — "Transport" as an ability, not just a keyword — **CLOSED S97 (D163)**
Transports carried the Transport keyword but not the Transport ability text (capacity,
excluded model types). `wahapedia_transform.py` now reads the `transport` column already
present in `Datasheets.csv` and adds a "Transport" entry to `unit_abil` / `unit_abil_desc`
per datasheet, the same shared-name-different-text path B1 established. 17 units gained the
ability (all Transport-keyword-bearing units that had a transport capacity row: Land Raider
variants, Drop Pod, Razorback, Stormraven Gunship, Impulsor, Repulsor variants, Rhino
variants, Corvus Blackstar). Pure data turn — `units.json` only, no engine change, since
abilities already render generically off `unit_ability_names` / `unit_ability_details`
(confirmed at `index.html` lines 4390/4402, 4608/4620). `index.html` stays v5.82.


### E16 — Sort control on "My Army Lists" page — **DONE (Session 32, D87)**
Sort pick-list added to the home actions bar (`index.html` v5.48 -> v5.49): three options —
Recent (modified desc, default), Name A–Z (case-insensitive), Faction (by primary_faction, name
tiebreak). Shown only when >=1 saved list exists (same toggle as "Back up all"). Pure UI over the
existing `store.list()` rows; sort is non-mutating and re-renders in place.


### E17 — Asterisk on statline stats that have a non-representable rule benefit — **DONE (D89, v5.51); SUPERSEDED S53 (D112)**
The asterisk is no longer a static per-datasheet fact. It now falls out of the D105 carrier count on the
*configured* build, covers W and SV as well as INV/FNP, and is never written where a unit-wide count cannot be
attributed to a statline group. Deathwatch Veterans and Decimus Kill Team therefore lose their default-state
asterisk (nobody carries an Astartes Shield until one is picked) and regain it when a shield is taken.

_Original text below:_
Shipped for the default-gear per-model INV/FNP case. `bearerOnlyStatFlags(raw, mg)` flags a
multi-model group whose default `wargear_ability_names` carries an unconditional "the bearer has…"
INV/FNP; `buildStatTable` appends a "*" to that cell and a right-aligned "* see Wargear Abilities"
legend. Guards mirror B15 (grant-gated skipped, single-model excluded, uniform excluded, conditional
auras never flagged; suppressed if the cell already shows a real override). Net: 5 groups / 3 units,
all INV — Wardens of Ultramar (both groups), Deathwatch Veterans, Decimus Kill Team (both groups).

**Not covered (banked as B15-swap / future):** units whose invuln comes from an OPTIONAL storm-shield
swap (Terminator Assault Squad, Wolf Guard Terminators/Headtakers, Thunderwolf Cavalry, Deathwatch
Terminator Squad) — that's the active-loadout option surface, not a default ability, and marking it
is a separate pass. Scoped out of E17 on purpose.

Ryan prefers make-up listed above the statline. Deferred because the make-up line
is produced inside the loadout weapon renderer (which also computes the fragile
weapon counts); reordering cleanly means splitting that function. Cosmetic, do
carefully.

List all detachment options with their detachment-points cost and a radio/checkbox
(match app style). User may pick any combination totaling ≤ 3 detachment points.
Selected detachments appear in the army-list section. Info button (left + center)
opens detachment details: rules, available enhancements, stratagems — each shown
like Rules (names visible, drop-down arrow reveals the detail).
- Foundational: unblocks E4 (enhancements) and feeds the points model. Needs a
  data source for detachments/enhancements/stratagems (Detachments.csv,
  Detachment_abilities.csv, Enhancements.csv, Stratagems.csv are in the raw set —
  need a pipeline path to surface them, which doesn't exist yet).
- Decision: confirm the ≤3 detachment-point rule scope and how selected
  detachments interact with legality (D0).


### E2 — Collapsible/expandable left-panel sections — **SHIPPED S117 (D185)**
Each of the eleven roster-panel role groups (Epic Hero, Character, Battleline, etc.) now has a
clickable header with a chevron that collapses/expands its unit list. Reuses the modal's existing
collapsible-section pattern. Collapse state is session-only (a view preference, not saved-list
data) and starts fully expanded on load. No "Detachment" section exists yet in the panel — that's
still E4, blocked on E1.


### E3 — Left-panel unit counts: red only when EXCEEDED, not when max is met — **CLOSED S55 (D114)**
Shipped in v5.61. `limitState()` returns `at` when the max is reached (card dims, count goes amber, add
refused) and `over` only past it (red). Over-limit is now only reachable from an imported or pre-v5.61 list.

*Original entry:*
Small render rule change. Reaching the max is not an error — only going past it is. Today `renderRoster`
reddens the badge at `count >= u.limit`; it should be `count > u.limit`. Pairs with **B41** (Epic Heroes:
refuse the add rather than flag it).


### E1 — Detachment selection system — **CLOSED S125 (D196); parent over E1a/E1b/E1c/E1e; all four shipped**
The app has no detachment selection at all today — no picker, no stored choice, no data path.
Scoped in full in S122; the authoritative write-up is `E1_DETACHMENT_SCOPE.md`, which this entry
summarises rather than repeats. E1 itself ships nothing — it closes when E1a, E1b and E1c are all
in. E4 and E6's points math sit on top of it; E21 (new) sits on top of E1c.

**S125 closure.** E1a (data), E1b (engine + persistence) and E1c (picker UI + info detail) are all
shipped and their behaviour gates green. E4, E6 and E21 are unblocked; they were logged as
downstream and remain so.

**The central S122 finding.** The Wahapedia dump is **10th Edition** (every `Source.csv` row is
edition 10; `Factions.csv` links read `wh40k10ed`). The **MFM faction files are 11th Edition v1.0**
and each carries a `DETACHMENTS` section giving name, DP cost, force disposition, and the full
enhancement list with current points and `(Upgrade)` tags. MFM is therefore the source of record
for *what exists and what it costs*; Wahapedia contributes description text only. **S123 addition:
MFM also carries a `UNIQUE:` tag on some detachments — a second exclusion rule the S122 pass missed
entirely; see E1e.** Across the eight
MFM files covering the fourteen built army blocks: **143 detachments, 515 enhancements, 35
Upgrade-tagged** (S123 correction — the scope doc said 513; three detachments break the 2-or-4
pattern the count assumed), five force dispositions (PRIORITY ASSETS 33 / TAKE AND HOLD 39 / PURGE THE FOE 27
/ DISRUPTION 24 / RECONNAISSANCE 20) with complete coverage.

**Text sourcing is a three-tier ladder** (corrected within S122 after Ryan pushed back on a wrong
first-pass finding). Tier 1, current edition: `chaos_daemons_reference.md` (all 9 CD detachments),
`Space_Marines_Faction_Pack_v1_0.md` (15 SM detachment pages, both 1 DP entries included), and
`Dark_Angels_Faction_Pack_June_2026.md` (5 DA detachments, added by Ryan during S122 — closes all
three DA gaps and upgrades two more). Tier 2: Wahapedia 10th-Ed text, only where no tier-1 text
exists, with faction-pack errata applied on top. Tier 3: no text — name, DP, disposition and
enhancement names and points only. `detachments.json` carries a `text_source` field per detachment.
**Coverage: 68 current / 66 previous-edition / 9 none** — against 27-with-nothing in the first pass.
The nine remaining gaps are all 1 DP, in the four blocks with no pack held: BT (Marshal's Household,
The Living Miracle), BA (Encarmine Speartip, Legacy of Grace, Wrath of the Doomed), SW (Legends of
Saga and Song, Veterans of the Fang), DG (Contagion Engines, Paragons of Putrescence). **Remedy is
an input, not a build** — packs for those four take the gap to zero and upgrade 41 more detachments
to current text. Asked of Ryan; nothing blocks on it.

**Extraction quality is a live variable.** The DA pack is single-column and linear and parses
directly; the SM pack is the same document type extracted as interleaved two-column text. A clean
re-extraction of the SM pack removes the column-splitter from E1a entirely. Also relevant to **E21**:
the DA pack labels army-construction limits with a literal `Restrictions:` line, and its `RULES
UPDATES` section carries a live Battleline-elevation case (Company of Hunters granting Outrider
Squad the BATTLELINE keyword, which moves that unit's count cap).

**Wahapedia drift, where it is still the source.** 116 of 143 match by name. Of those, 11 have
drifted enhancement sets: Librarius Conclave gained *Temporal Corridor* and re-priced four
enhancements (Celerity 30→35, Fusillade 35→20, Obfuscation 20→25, Prescience 25→20); Champions of
Fenris, Saga of the Great Wolf, Wrathful Procession, Daemonic Incursion and Flyblown Host all
differ. Enhancements present in a text source but absent from MFM are **dropped, not displayed**.
~20 further differences are pure naming — Wahapedia suffixes `(Aura)`, MFM appends `(Upgrade)`.
The `(Upgrade)` tag is rules-significant (25.04) and survives the join as a flag.

**Source ruled out.** `*_web.txt` — its `DETACHMENT ABILITY` strings are stray headings in a unit
dump with no rule bodies.

**Faction mapping.** Fourteen built army blocks, eight MFM detachment files. The six Codex: Space
Marines chapters with no MFM file of their own (Ultramarines, Iron Hands, Imperial Fists, Raven
Guard, Salamanders, White Scars) take the generic SM list of 22, which already contains their
chapter-flavoured detachments with no restriction language in any source held. Under D0's
undetermined-legality default all 22 are offered to all six. The SM Faction Pack's chapter
restrictions govern which *units* an army may include, not which detachments.


### E1a — Detachment data turn: parser + `detachments.json` — **CLOSED S123 (D193/D194); DATA-ONLY; `detachments.json` 14 armies / 143 distinct records / 275 army slots / 515 enhancements / 797 KB**
Shipped `detachment_parser.py` -> `detachments.json`. Stored **deduplicated** (D194): one record per
distinct detachment, each of the fourteen app armies holding a list of keys into it, key being
`"<source faction>|<MFM printed name>"`. Per record: key, name, name_raw, dp, force_disposition,
**unique_tag**, source_faction, text_source,
text_source_detail, rule_name, rule_text, **restrictions**, enhancements (name, name_raw, points,
is_upgrade, description, **description_source**), stratagems, stratagem_source. MFM parsed for
structure and numbers; text joined per the three-tier ladder.

**Counts as built.** **143 distinct detachment records** filling **275 army slots** (the six Codex
chapters index the same SM 22 the generic list does) and carrying **515 enhancements**, 35
Upgrade-flagged — exactly the scope doc's §2 figures once its 513 is corrected to 515. `text_source`: 158 faction_pack / 108 wahapedia_10e / 9 none, the nine being
exactly the 1 DP gaps the scope doc named. **The scope doc's 513-enhancement figure was wrong — the
MFM files hold 515** distinct enhancement lines (Librarius Conclave has five, not four; The Living
Miracle and Lords of the Warp have one each). Everything else in the §2 table reproduced exactly.
Nine Wahapedia-only enhancements were dropped as previous-edition leftovers.

**Two additive departures from the scoped record shape**, both in D193: enhancements carry their
own `description_source`, because the Chaos Daemons digest's one-line glosses should not suppress
Wahapedia's full text; and a tier-1 stratagem list only displaces tier-2 text if **every** entry
names itself, prices itself and carries a body. The second is stated as an invariant, not a
per-source switch, so an improved source starts winning with no code change.

**The SM pack was not re-extracted**, so the column-splitter stayed in scope. It works for rules,
restrictions and enhancement text across all 15 SM spreads; it does not work for stratagems, whose
floating CP badges sit at arbitrary columns, so those detachments fall back to Wahapedia stratagem
text under the completeness invariant. A single-column re-extraction flips all 15 automatically.

Pipeline integration shipped with it: `detachments_repro_check.py` is the third byte-identical gate;
`pipeline_manifest.json` went 24 -> 27 guarded files; `rules_assertions.py` went 62 -> **70** (`P5`,
`E1a-1`..`E1a-7`), 69/70 passing with P3 the only failure.

**Size (D194).** First cut was 1.61 MB and did not fit the project file area. Seven armies were each
carrying a byte-identical copy of the Space Marines 22 — 132 of 275 records, over half the file.
Deduplication took it to **797 KB with zero information loss**; `E1a-7` asserts the key indirection
is airtight. Separately, three Wahapedia join tables (`Datasheets_stratagems.csv`,
`Datasheets_detachment_abilities.csv`, `Datasheets_enhancements.csv`, 2.93 MB together) are
referenced by nothing and answer membership questions D193 gave to MFM — **recommended for removal
from the project file area**, which frees nearly 4x what the new file needs.


### E1b — Detachment state + persistence — **CLOSED S124 (D195); ENGINE-ONLY; `index.html` 6.1 → 6.2**
`selectedDetachments` in app state. `SCHEMA_VERSION` 1 → 2 with a migration reading a v1 record as
an empty detachment set — the migration hook in `list_store.js` is already stubbed for exactly this
(`if (v < 2) { ... }`). Export/import carry the field. `detachmentPointBudget(POINTS_CAP)` returns 2
at ≤1,000 and 3 above. A `dpState()` helper mirroring `limitState()` returning ok / at / over.

**Shipped S124.** `selectedDetachments` holds detachment **keys** (D194 dedup means array position is
not stable across a regeneration, so the key is the only durable identity); reset on create, restored
on open, carried into every saved record. Schema v2 with a strictly additive v1 → v2 migration —
a v1 record gains `detachments: []` and nothing else is touched. Export/import inherit it through the
existing `migrate` path, so a v1 export file imports rather than being rejected. `list()` summaries
gain `detachment_count`.

Scope grew by one thing beyond the ticket, deliberately: **all three selection constraints** ship as
pure helpers, not just the DP budget — `dpUsed`, `duplicateDetachments` (25.04) and
`uniqueTagConflicts` (D193/E1e) — behind a single read path, `detachmentSelectionState()`, so the
picker, the header counter and any later validation panel cannot disagree. `canAddDetachment()` is
the hard-block gate and returns a typed reason (`unknown` / `duplicate` / `unique_tag` / `budget`)
rather than a bare false. **The Unique tag is reported ahead of the budget when both bite**: a budget
refusal is "not right now", a tag clash is "never together", and only one of those is worth acting on.

Two behaviour precedents recorded in D195: an unresolved detachment key is **kept**, costs 0 DP and is
flagged (ghost-entry precedent), and `clearList()` does **not** clear detachments (the control says
units, and a detachment is not a unit).

Two custody findings came out of the baseline, both in D195: `list_store.js` had silently drifted from
the copy inlined in `index.html` (missing E9b's warlord field, unnoticed for several sessions, because
nothing compared them — now assertion E1b-2), and the S123 manifest regeneration had been reverted by
a sync. See H3.

New: `e1b_check.js` (100+ checks, twelve groups, including a derived Unique-tag sweep that needs no
editing when a new faction's tags arrive). Assertions **70 → 73** — E1b-1 (DP budget re-derived from
`Army_Muster_Rules.txt` on both sides, and pinned to `battleSizeUnitLimit`), E1b-2 (the two module
copies are byte-identical), E1b-3 (the harness gate; per D107 the migration is a behaviour claim, so
it is executed). **73/73 pass** — the first fully green assertion run since D123 introduced P3.


### E1c — Detachment picker + detail UI — **CLOSED S125 (D196); ENGINE-ONLY; `index.html` 6.2 → 6.3**
Left-panel detachment section pinned above the role groups, collapsible on E2's existing pattern,
with a `DP 2 / 3` counter in its header. Each detachment is a checkbox row showing name, DP and
disposition; a row whose DP would breach the budget renders disabled, matching how the roster
disables a unit at its limit. Selected detachments render in the centre army list. An info control
on each opens rule text, enhancements and stratagems as collapsible detail, reusing the Rules-style
drop-down and B47's info-button pattern. Closes E1 when it lands.

**S125 shipped.** UI over the E1b engine state. Section renders at the top of `#roster` reusing
`.role-group`/`.role-label`/chevron so the collapse behaviour matches E2. DP counter in the section
header (not the banner — E19 already filled it); red only when `dpState() === 'over'`, gold at
budget, muted below. Checkbox rows call `toggleDetachment()`, which routes every add through
`canAddDetachment()`; disabled rows spell out the typed reason (over budget, `unique_tag` naming
the tag and the clashing detachment by name, unknown / duplicate). Info button opens a per-row
detail panel with rule name / rule text, enhancements (name + points + description), stratagems
(name + CP + type + description); `text_source` / `description_source` / `stratagem_source` drive a
`prev. ed.` badge per item (D192), not a blanket disclaimer. Selected detachments render as a
`Detachments` group at the top of the centre army list with DP badges, force disposition and remove
buttons. Over-budget banner and each Unique-tag clash render in both panels. Unresolved keys render
as ghost rows on the flag-don't-drop precedent — a saved list opened after a data change surfaces
the key so it can be removed, rather than disappearing. `hasGhosts` on load ORs in unresolved
detachments so the banner's "list changed since saved" flag catches them. New `e1c_check.js` (12
scenarios + a sweep across all 143 catalogue keys); assertions **E1c-1** (five legality helpers
defined once, inside the E1b block, called nowhere else) and **E1c-2** (harness gate) added.
Assertions 73 → 75, all passing. Guarded set 35 → 36.


### H2 — Retire three superseded Wahapedia join tables from the project file area — **CLOSED S124 (D195); housekeeping**
`Datasheets_stratagems.csv` (2,277,806 bytes), `Datasheets_detachment_abilities.csv` (363,282) and
`Datasheets_enhancements.csv` (289,608) are referenced by no script, harness or assertion. Every CSV
in the pipeline is opened by explicit filename — nothing globs the directory — so that is a complete
check rather than a sample. All three are `datasheet_id | x_id` membership joins from the 10th
Edition dump, and D193 settled that membership comes from MFM with Wahapedia contributing prose only,
so they are superseded rather than merely unused. Removing them frees **2.93 MB**. Ryan's action —
they live in the project file area.

`Adeptus_Astartes_Unit_Info.txt` (411,559 bytes) is also unreferenced but is a hand-kept Wahapedia
scrape rather than a pipeline input; flagged for Ryan's judgement rather than recommended.

**Done S124.** All three files are gone from the project area at S124 open, freeing 2.93 MB. Nothing
referenced them and nothing broke. `Adeptus_Astartes_Unit_Info.txt` remains and is still unreferenced —
left alone, as flagged.


### E1e — Enforce detachment Unique-tag exclusivity — **CLOSED S125 (D196); engine + UI**
`MFM_Instructions.txt`'s `DETACHMENTS` legend defines a field the S122 scope pass missed entirely:
*"Some detachments are tagged with a 'Unique' word or phrase. You cannot select more than one
detachment that has the same one of these tags."* This is a **third selection constraint** alongside
the DP budget and 25.04's no-duplicates rule, and it is live in built data today — Blood Angels
carries `GRACE` on two detachments and `DOOMED` on three; Death Guard carries `FLYBLOWN` on two and
`ENGINES` on two. Twenty-seven tags exist across the full MFM set, so every faction built from here
on will have them.

E1a already ships `unique_tag` on every record and asserts it survives the parse unchanged
(`E1a-2`). What is missing is enforcement: selecting a tagged detachment must disable every other
detachment sharing that tag, on the same hard-block mechanism D192 item 3 chose for the DP budget,
with the over-constrained state staying reachable and visible for an imported list. Cheap next to
E21 — the tag is a plain string equality test, not a prose-parsing problem.

**S124 sequencing call (D195).** The logic shipped inside E1b: `uniqueTagConflicts()` names every
offending tag and both sides of each clash, and `canAddDetachment()` refuses with reason
`unique_tag`, ahead of the budget refusal when both apply. What remains is the **enforcement
surface** — the disabled row and the message — which rides with E1c alongside the other two
constraints. Splitting it the other way would have meant E1c wiring two of three constraints and a
later turn reopening the same code for the third. E1e closes when E1c lands.

**S125 closure (D196).** The picker's disabled state, refusal text and warning banners now surface
`unique_tag` refusals identically to budget refusals: the row disables, the refusal text names the
tag *and* the clashing detachment by name, and any pre-existing clash (from an import or a battle-
size switch) is called out in a warning row at the top of both the picker and the centre panel. The
worst-case case — over budget AND clashing AND with a ghost — is covered by the E1c-2 harness. Rides
in with E1c per the S124 sequencing call.


### E5 — Rename banner "List Points" → "LIST POINTS" with two figures — **SHIPPED S87 (D154)**
Banner now shows "Configured N | Remaining M" with `remaining = POINTS_CAP - total`. Over-cap red carries on
the Configured figure; Remaining goes negative when over cap (informational). No data change.

*Original entry:*
Show "Configured" and "Remaining" (or similar). "Remaining" requires the army
points ceiling to be known (list size, e.g. 2000) — confirm where that's set.


### E6 — Affordability cue on left-panel units — **SHIPPED S118 (D187)**
Left-panel unit cards dim (opacity 0.7, lighter than the `at-limit` disabled look)
when the unit's cheapest legal build won't fit in what's left of the points cap.
Still fully legible and clickable — matches the decision below. No engine/data
change; pure UI reading two already-existing values.

*Original entry:*
**DECIDED: subtly dim the unaffordable units** (keep fully legible + selectable),
not a border on affordable ones. Reason: early in list-building almost everything
is affordable, so bordering "fits" units would paint most of the panel and read as
noise; dimming grows more useful as the list fills. Depends on E5's "Remaining".


### E7 — More spacing between points / info / x in the center panel — **SHIPPED S87 (D154)**
Scoped CSS rules under `.list-item` put deliberate margins between points, info, duplicate, and the delete
"×", with the widest gap right before "×". Rules are scoped so they do not affect the same-named `.info-btn`
in the Configuration Panel (B47).

*Original entry:*
Especially between info and "x" to reduce accidental deletes. Plenty of room.
Confirmed: keep this spacing even though E8 adds undo — both, not either/or.


### E8 — Delete safety — **SHIPPED S87 (D154)**
Delete no longer commits immediately. A 5-second bottom-center toast shows "[unit] removed" + Undo + dismiss.
The entry is held in memory (with attachments and index) and auto-save is suppressed until the toast expires
or is dismissed. On Undo the entry is spliced back at its original index with attachments restored. A second
delete during a pending toast commits the first (no undo chaining — the simpler v1 path). Navigation
(home, open list, new list, clear all) commits any pending delete first so nothing is silently lost.

*Original entry:*
Skip a per-delete confirmation dialog; add an **undo** toast after delete instead.
A modal on every delete is friction in a tool where users churn units constantly;
E7 (spacing) removes most misclicks, and undo is the low-friction safety net that
actually prevents data loss. (Optional future gate: a confirm only on units that
have been configured — non-default wargear/points invested — not fresh defaults.)


### E9 — Warlord selection — **DONE (Sessions 75–76, D139, D140)**
Today the Warlord is not presented anywhere. Ryan's design:
- **Where.** Either an option in the configure panel on each qualifying unit (Epic Hero, Character), or —
  his preference to weigh — a **pick list in the second banner**, the one carrying "Army List", centred.
  Recommendation: the banner pick list, because "exactly one per army" is an army-level fact and a
  per-unit checkbox makes the user hunt for the one that is ticked.
- **Contents.** Only units actually in the army list and eligible to be Warlord.
- **Auto-select.** A unit whose datasheet says it must be the Warlord is selected automatically.
- **Error.** Two units in the list that each *must* be the Warlord is an illegal army — show it in red.
**Source is settled (was the open decision on this item):** `Datasheets_abilities.csv` carries a
**SUPREME COMMANDER** ability whose text is "If this model is in your army, it must be your Warlord."
(18 rows in source; e.g. `000000138`; Ghazghkull `000000008` words it as "its ... model must be your
Warlord"). Eligibility itself is the CHARACTER keyword per the core rules — assert both before building.

**Reshaped S73 (D137): E9 is now two turns, because the must-be-Warlord flag does not reach the derived data.**
The SUPREME COMMANDER rows carry `type = "Special (правая колонка)"`, which `wahapedia_transform.py`'s
`index_abilities()` does not route — it falls into the `else` branch and lands in
`flags["unclassified_abilities"]`, dropped from all output. So none of the four already-built must-be-Warlord
units — **Lion El'jonson, Roboute Guilliman, Mortarion, Be'Lakor** — carry the rule in `units.json`. This is
needed **now**, not after more factions ship (an earlier "1 unit, Azrael" scan was a false positive: Azrael's
ability is "Supreme Grand Master", which does not force Warlord). Build order:
- **E9a — SHIPPED S75 (D139).** `must_be_warlord` now live on `units.json` for exactly 4 units: Guilliman,
  Lion El'jonson, Mortarion (transform name-match, independent of `type`), and Be'Lakor (hand-added on the CD
  source row, per D132). New `rules_assertions.py` check `E9a-1` holds this as an executable fact. A live,
  unrelated data bug (Blue Horrors' abilities/rules/keywords miscolumned in the CD source, shipping wrong
  since before this session) was found and fixed as a side effect — see D139.
- **E9b — SHIPPED S76 (D140).** Turned out to need a data addition first: `cannot_be_warlord` didn't exist on
  `units.json`, and checking source before building found 3 already-built units carrying the restriction
  (Lieutenant With Combi-weapon, Murderfang, Exalted Flamer) — shipping the pick list without it would have
  let them be wrongly Warlord-eligible. Derived via description text-match ("cannot"+"warlord"), same
  take-from-first-row/append-only-column precedent as E9a; new `rules_assertions.py` check `E9b-1`. The pick
  list itself lives centered in the Army List panel-subheader: a `<select>` over CHARACTER, non-ghost,
  non-cannot-be-warlord entries in the list, disambiguated by `(2)`/`(3)` suffix on duplicate names. A single
  must-be unit forces and locks the pick every render; two forces an illegal-army red flag instead of guessing
  between them; cannot-be-warlord always wins over must-be structurally (filtered out before the must-be check
  runs). Selection persists on the saved-list record as an additive `warlord_entry_id` field (`SCHEMA_VERSION`
  unchanged). `index.html` v5.69 → v5.70.
Data pool as built: 270 units, 121 CHARACTER, 58 Epic Heroes, 4 must-be-Warlord, 3 cannot-be-Warlord units
live today.


### B50 — off-by-one column index in `wahapedia_transform.py` post-processing — **DONE (Session 74, D138)**
Shipped. `Leader Footer`'s insertion (B49) shifted every later `Unit_Stats.csv` column right by one; two
hardcoded post-processing indices weren't updated. Fix 2b (chapter-variant ability inheritance) was reading
`Leader Footer` instead of `Unit Ability Names` (`AB = 18` → `19`) — 6 Black Templars units were missing an
inherited generic ability. B14 surface-subtraction was reading `Model Keyword Names` instead of `Wargear
Ability Names` (`row[23]` → `row[24]`) — 10 units across 5 armies carried an incorrectly-always-on optional
wargear ability. Full three-source pipeline regenerated; byte-diff confirms exactly these 16 units changed,
nothing else. See D138 for the full unit list and root cause.


### B51 — Blue Horrors' abilities/rules/keywords were miscolumned in the CD source — **DONE (Session 75, D139)**
Found while verifying E9a: the CD source `Unit_Stats.csv` row for Blue Horrors was already writing into the
(previously blank) trailing columns E9a repurposed — the row's data was shifted, not the new column. Missing
two of three abilities (`Sullen Malevolence (Aura)`, `Exploding Horrors`), both core rules (`Deep Strike`,
`Infiltrators`), and all six keywords in the live, currently-deployed `units.json`. Fixed by hand-correcting
the source row (same file, same turn as the Be'Lakor E9a edit). See D139.


### B52 — `Sullen Malevolence (Aura)`'s ability description is truncated in the CD source — **SHIPPED S77**
`Unit_Abilities.csv` (project root, CD's own lookup) had the text cut off mid-sentence: "While an enemy unit
is within 6\" of this unit" with no resolution clause. Fixed alongside B1b — the full text ("...worsen LD of
models in that enemy unit by 1.") now reaches every unit that uses this ability via the new
`unit_ability_details` override, sourced from `chaos_daemons_reference.md` rather than the (still-truncated)
flat CSV. See D142.


### B53 — Combined attached-unit popup renders bodyguard on top, leader on bottom — should be leader first — **CLOSED S96 (D162); `index.html` v5.81 → v5.82**
Shipped. `buildModalCombined` now builds each leader panel first (attach order), bodyguard panel last —
matches the center Army List panel's stacking. Aura-flag union still applied to the bodyguard panel only
(unchanged). Engine-only, no data change. All eight version-dependent/independent harness checks pass
unchanged (none assert panel order, so this confirms no regression, not the fix itself). **Still needs
Ryan's live-render eyeball** — no harness checks DOM order. See D162.

Original spec kept below for reference:
Follow-up to B7b (S91, D159). The combined popup for an attached unit stacks the panels in the wrong order
relative to the rest of the app: the bodyguard renders on top and the leader below, but the center Army List
panel presents the leader first, then the bodyguard. Screenshot from Ryan (S94) shows Bloodletters (bodyguard)
above Skulltaker (leader) in the popup. The order should match the center panel: leader first, bodyguard
underneath. Small engine ticket in `buildModalCombined` / the panel-render loop; no data change, no legality
effect. Pairs cleanly with any other B7b follow-ups.


### B56a — chapter Unit_Points rows (scoped) — **SHIPPED S101 (D168)**
Added `--scope-to-army` (restrict the name→army map to the given army's own `Unit_Stats.csv`
rows; drop MFM entries with no datasheet in that block, never fall back) and `--append`
(extend an already-written `Unit_Points.csv` with no header/BOM) to `mfm_points_parser.py`.
Ran the five chapter files scoped and appended into the SM sequence, ahead of
`convert_to_json.py`. All five now sit inside `units_repro_check.py`'s fixed point.

Closed **77 of 81**. Black Templars — the negative control — arms 17/18 with zero misfiles;
the Impulsor pair (Adeptus Astartes 80 / Black Templars 85) stays distinct, proving no
overwrite. Two rules assertions (B56a-1, B56a-2) replace the prose closure figures.

Found in the process, not predicted by D167: **Space Wolves' Venerable Dreadnought is priced
in two MFM files with different numbers** (165 generic vs. 125/135 chapter). It was already
armed pre-S101, so it's not one of the 81 and isn't a B56c override case either (it has no
Adeptus Astartes counterpart to override). `--append` now detects any such collision and
keeps the existing value rather than silently applying the chapter one. Filed as B56f.


### B56b — parser: composition-shaped size-bracket lines — **SHIPPED S102 (D170) — Crusader Squad only**
`COST_RE` required `• N model(s) PPP pts`. Added `COMPOSITION_RE`: one or more comma-separated
`<count> <label>` groups summing to the bracket size, cost jammed onto the end exactly as the
bare-count shape. Crusader Squad (`000002799`) closed cleanly — two composition lines, no
ambiguity, sums to 10/20 models, priced 150/290.

**Wolf Guard Headtakers did NOT close** — it looked like the same shape but isn't. Its bracket
lines carry an optional Hunting Wolves escort (0–6, already a separate optional model group in
`unit_loadouts.json`), and two different compositions total the same 6-model bracket at two
different prices (170 vs 115). Summing total models as the bracket key — the original plan —
collides. The parser now stages composition matches and resolves them per unit/per-tier after the
full block is read: any same-tier size collision voids that unit's *entire* composition table
rather than guessing a winner or shipping a partial bracket row. Wolf Guard Headtakers stays
`points: null`, tracked separately as **B56g** below (schema/mechanism decision, not a regex fix).

Rules assertion **B56a-1 renamed to B56b-1**, residual-null set shrunk from 4 to 3. B56a-2 (BT
negative control) updated: Black Templars closes 18/18, not 17/18.

Verification: composition regex checked against every non-`COST_RE` bullet line across all five
chapter files plus the base SM file by hand — zero false positives. Base SM run byte-identical
old-vs-new parser. Five-chapter overlay diff: exactly Crusader Squad added. `units.json` rebuild:
exactly one `unit_id` changed, all four merged lookups byte-identical.


### B56g — Wolf Guard Headtakers: Hunting Wolves escort is an optional priced model group — **CLOSED S108 (D174, D175, D176)**
Split off B56b when the composition-bracket parse revealed Wolf Guard Headtakers isn't a simple
composition unit. **S105 analysis (D173) rejected both original directions. S106 confirmed the
blocking question against the printed MFM table (locked 0-or-N — exactly four configurations are
priced, nothing in between) and shipped phase 1.**

**What the unit is.** Composition is two independent ranges — `3-6 Wolf Guard Headtakers` and
`0-6 Hunting Wolves`. A Hunting Wolf is a model with its own statline row in
`Datasheets_models.csv` (M 10", T 4, Sv 6+, W 1, Ld 8+, OC 0), its own weapon (`Teeth and claws`),
its own keywords (`BEASTS, IMPERIUM, HUNTING WOLVES`), and two datasheet abilities that only work
if it is a model — *Let Loose the Wolves* splits the unit in two by keyword, *Hunting Hounds*
raises the OC of HUNTING WOLVES models specifically.

**Phase 1 (S106, D174) — parser turn, shipped.** `mfm_points_parser.py`'s composition resolver now
parses each bracket line into (count, label) groups and keys the primary bracket on the Headtaker
group alone rather than the sum of all groups — the collision (3+3 and 6+0 both summing to 6) never
occurs, because the escort line is recognised and pulled out before the sum-based path runs. Wolf
Guard Headtakers now prices at 85/170 (1st-2nd) and 95/180 (3rd+), the two Headtaker-only brackets.
The escort rate is re-derived from the printed difference, never hand-entered: 115−85 = 30 over 3,
230−170 = 60 over 6 → 10 pts/wolf, confirmed identical at the 3rd+ tier. Crusader Squad (the only
other multi-group bracket unit, Black Templars) is untouched — verified byte-identical parse output
— because its printed lines never include a standalone single-group line to match against.
Diff-guard: full pipeline rebuild, exactly one `unit_id` changed (`000004131`). New rules assertion
`B56g-1`.

**Points authority note.** `Datasheets_models_cost.csv` says 110 / 220 for the escorted brackets;
the MFM says 115 / 230. MFM wins by design — the Wahapedia cost table is stale for this unit and
is not a valid cross-check here.

**Phase 2 (S107, D175) — data turn, shipped.** The Hunting Wolves model group's count moved off the
flat `optional`/`max:6` shape onto `optional`/`per_bracket` (3 wolves at the 3-Headtaker bracket, 6
at the 6-Headtaker bracket), and a new `price_per_model: 10` field was added — a new schema field,
since no existing field in `unit_loadouts.json` carries a per-model price (that lives in
`wargear_points.json` for wargear swaps, which this isn't). `repro_check.py`'s `HAND_AUTHORED` list
gained a third entry (`000004131`) — the bracket linkage comes from the MFM price table, which the
composition-CSV-driven parser never sees, so it's a genuine hand-authored exception, same class as
the two existing ones. Diff-guard: exactly one `unit_id` changed. Full detail in D175.

**Phase 3 (S108, D176) — engine turn, shipped. B56g closes.** `loGroupCounts` now accepts the
optional+per_bracket shape as a 0-or-N toggle; a new `modelGroupCost` adds the group's cost
(`price_per_model × count`) into points math; the existing B13 config-panel toggle block picked up
the group automatically and now shows the model count and points. A bug in the first pass — the
escort's count wrongly shrinking the Headtaker `fills_to_size` group — was caught by the new harness
(`b56g_check.js`) and fixed before shipping; the printed table confirms the escort rides alongside
the bracket, not inside it. `B56g-1` rewritten from a not-yet-reachable guard to a now-reachable
guard. Hunting Wolves is now a fully buildable, correctly priced escort in the app.


### B57 — in-between unit sizes are not offered anywhere — **CLOSED S118 (D186); no build needed**
Every unit composition in the data expresses a **range** (Blood Claws `1 Pack Leader` + `9-19 Blood
Claws`; Intercessor Squad `1 Sergeant` + `4-9 Intercessors`; Thunderwolf Cavalry `1 Pack Leader` +
`2-5`), and `MFM_Instructions.txt` states the rule plainly: a unit *can* contain a number of models
between the printed limits, and pays the maximum printed cost when it holds more than the minimum.
The app offers only the printed bracket edges — 10 or 20, 5 or 10, 3 or 6 — with nothing in
between, because `points.sizes` is the sole source of the size selector.

This is systematically **under-permissive**: a legal 7-model Intercessor Squad cannot be built.
Under-permission is the safer failure (a visible gap the player complains about, versus silently
shipping an illegal or mispriced list), and the behaviour is longstanding and consistent, so this
is filed as a finding rather than a defect to fix on sight.

**Needs a product call before any build.** Should the size selector offer every legal count in the
range (pricing per the MFM round-up rule), or stay on printed brackets only? Offering the full
range touches the selector UI, the points math, `required_size` matching (D160/D161 — an exact
integer match against the bracket, which would need re-reading against a free count),
`per_bracket` group counts (D62), and every saved list's `sizeIdx`. Large. No recommendation yet —
it depends on whether players build off-bracket units in practice, which is a New Recruit
comparison worth making first.

Surfaced during B56g analysis (D173) because the 0-or-N recommendation there is consistent with
current behaviour precisely *because* of this gap.

**Resolved S118 (D186).** Ryan's call: stay on the discrete sizes printed in the MFM only — no
in-between counts, even where technically legal, since no one plays that way in practice. Current
behavior (size selector driven off `size_brackets`) already matches this. No build needed. B57
closes as a no-op.


### B56c — derive the per-chapter points override map — **SHIPPED S103 (D171)**
New pipeline step `add_chapter_point_overrides.py`, re-derives the override set from the five
chapter MFM files fresh every build (never hand-maintained) and stamps it onto the matching
generic Adeptus Astartes units as `chapter_point_overrides`. Wired into `units_repro_check.py`
as the final SM build step.

Re-derived population matches D169 exactly: 11 override rows across 4 chapters (Blood Angels 8,
Space Wolves 1, Dark Angels 1, Deathwatch 1), collapsing to **8 unique units** — Repulsor
Executioner is overridden by all four chapters at once (230/250 vs. generic 240/260) and carries
all four as one nested object rather than four separate unit entries. Diff-guard: exactly 8
`unit_id`s changed, all in the Adeptus Astartes block, no other field moved. `units_repro_check.py`
reproduces byte-identical with the new step included.

Field is inert until B56d reads it — no engine change shipped this session, per the ticket's
explicit instruction to close B56c in isolation first. See D171.


### B56d — engine: apply the chapter override at selection — **SHIPPED S104 (D172)**
`resolveUnits` in `index.html` (v5.83) now calls a new helper, `applyChapterPointOverrides`, right
after the generic/chapter union is built. A unit carrying `chapter_point_overrides[armyName]` for
the active army gets a fresh copy with `points` substituted — the shared generic unit object is
never mutated in place, so the override can't leak into a different chapter's view. Both list
creation and list opening call `resolveUnits` before anything reads prices, so saved-list
re-hydration recomputes the chapter-scoped price fresh rather than freezing it at save time.

New harness `b56d_check.js` (14/14 pass): Repulsor Executioner 230/250 under Space Wolves, Blood
Angels, Dark Angels, Deathwatch; 240/260 under Ultramarines and the generic view; Assault
Intercessor Squad 80 under Blood Angels, stays 75 under Dark Angels; source objects confirmed
unmutated after resolve. Full harness suite re-run clean, no regressions. See D172.


### B56e — Judiciar Xacharus & Chaplain Kastiel have no points source — **RETIRED S121 (Ryan: disregard these characters)**
`000004179` and `000004180` appear in none of the 30 MFM files held in the project. Ryan directed
these two characters be disregarded — no source will be sought, no build will follow. Retired, not
closed by resolution.


### B56f — Venerable Dreadnought priced twice, generic and chapter disagree — **CLOSED S101 (D169)**
Ryan resolved (D169): faction points always override generic — confirms D42 as written. The
Space Wolves chapter price 125/135 wins over the generic 165. `mfm_points_parser.py --append`
now strips the base row and writes the chapter row on collision, logging each override.
Applied this session; `units.json` shows SW Venerable Dreadnought at 125/135.

Same decision resolves the S100-open Repulsor Executioner question: SW/BA/DA/DW 230/250
wins over generic 240/260 when B56c ships.


### B54 — Be'Lakor's Shadow Form ability shows the rule name but not the pickable abilities — **CLOSED S110 (D178)**
Be'Lakor's Shadow Form ability gives him a choice among several sub-abilities each turn (per the datasheet).
The popup previously showed the ability name and its top-level rule text but did not surface the specific
abilities that could be chosen. Player had no way to see what the options were without leaving the app.

**S109 diagnosis:** the sub-ability text was already known (in `chaos_daemons_reference.md`) but not yet in
the CD data files. Chaos Daemons is Gen-1 hand-built data in Wahapedia-shaped CSVs at the project root and is
**never** routed through `wahapedia_transform.py` (D132), so `convert_to_json.py` reads the root CSVs
directly for this faction — the root `Unit_Ability_Details.csv` had only two rows for
`local:chaos-daemons:be-lakor` (The Dark Master, Shadow Form); the three sub-abilities were missing entirely.

**S110 build.** Added three rows to `Unit_Ability_Details.csv` (Wreathed in Shadows, Pall of Despair, Shadow
Lord — text from `chaos_daemons_reference.md`, matching Wahapedia wording) and extended Be'lakor's Unit
Ability Names list in `Unit_Stats.csv` so all three render in the Abilities section via the existing generic
display mechanism — no engine/display code changed.

**Naming-convention finding, now a standing rule.** `convert_to_json.py`'s `split_list()` does a plain comma
split with no quote-awareness. Writing a multi-tag ability name with an internal comma — e.g. "Wreathed in
Shadows (Aura, Psychic)" — breaks it into two garbage list entries at rebuild. Existing CD data (Poxbringer's
"Feculent Despair (Aura Psychic)") had already worked around this by dropping the internal comma; followed
the same convention here, and used the same no-comma form as the `Unit_Ability_Details.csv` key so the
lookup matches. **Any future Aura+Psychic (or other multi-tag) ability name added to a Unit Ability Names
field must drop the comma between tags, or the pipeline silently corrupts the list.**

Diff-guard: full pipeline rebuild, byte-identical except `local:chaos-daemons:be-lakor` (JSON-level diff
confirmed zero other units moved). Full detail in D178.


### B55 — `abilities.json` has drifted from what the pipeline currently produces — **CLOSED S98 (D164)**
**Diagnosed and closed.** Not a pipeline regression — the committed lookups were simply stale, and
the drift was wider than B55 originally described: **all four** merged glossary lookups had drifted,
not just `abilities.json`. `rules.json` (+5 names, 4 text), `keywords.json` (+1), and
`weapon_abilities.json` (+1 / −1 / 1 text) were stale too. The rebuild lost nothing from
`abilities.json`, `rules.json` or `keywords.json` — pure additions, mostly Death Guard ability text
plus SM entries added by parser work since the last regeneration (including E15's own `Transport`).
The 33 "text changes" in `abilities.json` (and the 4 in `rules.json`, 1 in `weapon_abilities.json`)
were all one defect: a mangled inch mark, a stray backslash where a `"` belongs, from an older
CSV-quoting path. The rebuild is correct; the committed copies carried the corruption.
One real fix, not just tidying: `weapon_abilities.json` gained `Icon of Despair (Aura)` and dropped
the orphaned `Diseased Icon` — `units.json` already referenced the new name, so that ability's
glossary text was missing in the shipped app until now. All four refreshed lookups shipped.
Root cause of the drift is now closed as a class: the lookups were the one deployed output nothing
checked. `units_repro_check.py` now compares them alongside `units.json`, and that gate is wired
into `rules_assertions.py` as **P4** (it had never been wired in at all).

<details><summary>Original S97 report</summary>
Found while shipping E15 (D163): running the full pipeline produces an `abilities.json` (the
global ability-name glossary) with 76 entries not in the committed file — names unrelated to
Transport, e.g. "CRIMSON FISTS", "CHAPTER MASTER OF THE RAVEN GUARD". Committed `abilities.json`
was not rebuilt from current source CSVs for some prior span of sessions. Not shipped this
session to keep E15 scoped. `units.json` per-unit rendering does not depend on
`abilities.json` (confirmed — it's a fallback glossary only), so this is not user-visible yet,
but the drift should be diagnosed and closed before it masks a real gap. Diagnosis turn first:
confirm what the 76 entries are (legitimate CSV growth vs a pipeline regression) and whether
any other consumer reads `abilities.json` directly.
</details>


### E10 — Duplicate unit in center panel — **DONE (S81, D148)**
Right-side icon duplicate control shipped in the center panel's unit card. Ryan's rules (all confirmed in
the shipped build):
- Duplicating a unit that has **attached leaders duplicates the leaders too**, and re-attaches them to the
  copy.
- **An Epic Hero is never duplicated** — if an attached leader is an Epic Hero, everything else is copied
  and the Epic Hero is simply left off the copy (it is not an error; the copy just has no leader in that
  slot).
- The copy inherits the original's size and full wargear configuration.
- Copy-tier pricing (first/second/third+) applies to the copy automatically — no new pricing logic needed,
  since `ptsForEntry` already reads copy order off `listId`, and a duplicate always gets a fresh, higher one.

Implementation default (not in Ryan's original spec, applied as a direct read of the existing hard-limit
invariant rather than a new precedent): if re-attaching a duplicated leader would put that leader's own
unit_name over its own instance limit, the leader copy is silently skipped and the body copy still ships
with no leader in that slot — same treatment the tool already gives every other limit boundary.

New harness `e10_check.js`, 16 assertions across 5 scenarios (plain unit, non-Epic-Hero leader, Epic Hero
leader, unit at its own limit, leader at its own limit), all passing. `index.html` v5.72 → v5.73.
**Still needs Ryan's live-render eyeball** — no harness checks the actual DOM render.


### E11 — Light/dark background toggle — **SHIPPED S120 (D190); closed**
Original estimate assumed a quick CSS variable set. Found `index.html` had zero existing CSS
variables and 72 hard-coded hex colors — no seam to hang a toggle on. Ryan chose the full,
properly-designed refactor over a quick compromise. **Shipped S119:** every hex color converted
to a `var(--c-hex)` reference; `:root` holds current dark values; `html.theme-light` holds a
systematically generated light palette (bg-context colors → light tints, fg-context accents →
darkened same-hue variants, neutral grays → inverted). Toggle button lives in the top banner, far
right; theme choice persists via `localStorage` (`40kab_theme`), applied pre-paint to avoid a
flash; default is dark.

**S120 — Ryan's visual verification pass, iterative, v5.90 → v6.1:** three-level depth system
(page/panel/card backgrounds, both themes) so the three main panels stop merging into one flat
field; roster and Army List rows now sit on a visible card surface; section group headers
(EPIC HERO/CHARACTER/BATTLELINE etc.) brightened and given breathing room; custom thin/rounded
scrollbars, themed per mode; selected Army List row border strengthened to 2px. Light theme
specifically: Back Up All / Import / Recent controls were rendering invisible (near-white on
near-white) — given a real light-grey fill and dark text; chosen/selected option text (e.g. a
picked wargear swap) darkened for legibility; standard body text darkened further; section
headers bolded. Top banner went through several rounds before landing: black → dark grey →
medium grey → **light** background, because dark text has a hard contrast ceiling against a
mid-brightness backdrop — moving the banner to a light background (not just darkening the text
further) is what actually fixed it, and let the gold accent text return to a real amber
(`#8a6100`) instead of being forced near-black to survive against medium grey. Theme toggle icon
replaced (generic OS moon/sun emoji → custom SVG, gold-accented) and given its own dark tile so it
doesn't blend into the lighter banner. Closed the backlog's own known cosmetic gap: the Army
Points dropdown arrow SVG had a hard-coded fill untouched by the original refactor — themed for
light mode; the dropdown's underline was also hover-only, so it read as broken at rest — now
persistent in light mode. Stat-modal aesthetic pass: shadow + brand-red top accent so it reads as
a floating overlay instead of a flat rectangle; keyword pills reshaped to true pill (999px
radius) with a warm gold-brown border instead of flat grey. One correction mid-session: a gold
value drifted to an unintended near-black during the iteration and was caught and fixed.
Base type scale nudged up ~6% (root font-size 16→17px) — since the app is almost entirely
rem-sized, this lifts text and spacing together.

All engine/data checks (repro, rules_assertions, full 56-check harness, bundle) unchanged
throughout — every S120 change was CSS-only, confirmed no JS logic touched. See D189 (S119
mechanism) and D190 (S120 verification-pass changelog) for full detail.


### E20 — Visual polish, phase 2 (deferred items from E11's pass) — **CLOSED S121 (Ryan: not pursuing)**
Three items came up during E11's light-mode pass — blue accent color, role-based keyword icon
coloring, right-pane illustration/watermark. Ryan closed without building any of them; new design
tickets can be opened later if he wants one.


### E19 — Move Configured/Remaining points next to Army Points in the banner — **SHIPPED S119 (D188)**
Ryan asked for the two points displays to sit directly beside the Army Points selector instead of
pinned to the banner's far right with a gap. Pure markup/CSS: `banner-points` nested inside
`banner-army-pts-wrap`; same two element IDs, same JS visibility toggling. Freed up the banner's
far-right slot, which E11's theme toggle now occupies.


### E13 — Drop "Keep" prefix from default swap-option labels — **CLOSED S84 (D151)**
Default/base rows in Wargear Options rendered as "Keep <weapon>" at two sites in `index.html`
(`'Keep ' + o.replaces`, single-choice and clustered-choice rows). Both now show just the weapon
name; the pre-selected highlight carries the default signal, per the S52 trade-off. `index.html`
v5.73 → v5.74. App-side only, no data/parser/regen.


### E18 — JSON export / import (list portability + data-loss recovery) — **DONE (Session 27, D82).**
Saved lists lived only in `localStorage`; a cache-clear wiped them (Ryan hit this). The
storage module already had `exportRecords`/`importRecords` + the `migrate` hook; this turn
wired them to the UI (`index.html` v5.46 → v5.47, app-only, no data/engine change). File shape
is the module envelope (`format: "40kab-lists"`, `schema_version`, `lists: []`) plus an
`app_version` stamp. Export = download `.json` (file-first, survives cache-clearing) + clipboard
copy, from the builder chrome or a per-row button on home. Import = file picker + paste box;
each record gets a fresh id so it can never overwrite a surviving list; newer-schema records are
surfaced and refused, not silently dropped; unknown `unit_id`s ride the existing ghost-row path
on open. v1 is one-list-per-action; the envelope already supports many, so a "back up all lists"
export is a format-free fast-follow.

**Back-up-all fast-follow — DONE (Session 31, D86).** Added the home-page "Back up all" button (`index.html` v5.47 -> v5.48): packs every saved list into one `40k-army-lists-backup-YYYY-MM-DD.json` via the existing envelope; shown only when >=1 list exists; skips/counts newer-schema records at fetch. Import side unchanged (already round-trips a multi-list envelope).

---


### B16 — Per-model-group default weapons (weapon-count fix) — **DONE (Session 23, D78).** Fixed in equipped_parser.py via a Datasheets.csv loadout-column gap-filler; 19 units repartitioned, 0 regressions.
Root cause of the configured-popup weapon miscounts (e.g. Deathwing Knights
showing 10 melee weapons on 5 models). `loadout_parser.py` assigns the full
base-weapon set to *every* model group (`g['default_weapons'] = base_ws` ~line
785; documented shortcut ~line 521). Fix: read the datasheet `loadout` prose in
Datasheets.csv ("The Knight Master is equipped with: X. Every Deathwing Knight is
equipped with: Y.") and partition base weapons to the correct model group by
matching the model-name clauses to the parser's model groups. This also removes
the false-positive noise (Sergeant pistol+primary, vehicle multi-guns, weapon
profile-variants) because the prose is authoritative per group. Requires a
loadout regen scoped to all supported factions (DK is Dark Angels, not SM/DG) and
validation across all multi-group units. Fix parser, not output.


### B22 — "1 model's X can be replaced" is parsed as a per-5-models allowance (parser + data) — **CLOSED (D94, S39)**
`classify_*` for the sentence shape "1 model's <weapon> can be replaced with …" hardcodes
`per_n_models: 5, max_per_n: 1`. The sentence means **exactly one model in the unit**, so at
size 10 the app currently offers two of a single-model upgrade — an illegal list the tool
should be refusing. Should emit `max_total: 1` (or a `choice` where the scope group is a
single model). **7 units, all parser-generated:** `000000070` Tactical Squad, `000001046`
Helbrute, `000001997`, `000002285` Death Company Marines, `000002737`, `000002783`,
`000004182` Wolf Scouts. Overlaps **B20** (Helbrute is a fixed-1 group) — the parser halves of
B20 and B22 are the same classifier; do them in one pass, engine half of B20 first.


### B23 — compound "A and B can be replaced with C" — **`count` family CLOSED (D95, S40)**
`classify_per_n` and `classify_n_model_swap` now emit the compound source (`"Bolt rifle + Close
combat weapon"` on `replaces`), which the engine's multi-model path already splits and charges per
weapon. The replacement side is compound- and comma-list-aware too. Live in: Death Company Marines
with Bolt Rifles, DCM with Jump Packs, Blightlord Terminators, Sword Brethren, Wolf Guard
Terminators, Deathwatch Veterans, Wolf Scouts. The remainder is **B23b** below.


### B23b — compound source on a `choice` option (engine + parser) — **CLOSED (engine D97/v5.54 S42; parser D98 S43)**
The engine keys a choice's replaced weapon by exact name (`replaced[o.replaces]` in the `fixed: 1`
branch, and `cUsed[src]` in the same branch), so a compound `'A + B'` source there would consume
nothing. The parser therefore still emits only the **first** weapon for these lines and flags them
`COMPOUND_SOURCE_UNSUPPORTED` / `COMPOUND_SOURCE_ON_SINGLE_GROUP`. Effect today: the character keeps
a weapon it should have given up (e.g. the Tactical Sergeant swaps bolt pistol **and** boltgun for
twin lightning claws but keeps the boltgun). ~13 units: `000000070` (`sng_3`), `000000073`,
`000000083`, `000000117`, `000000136`, `000000166`, `000000318` (`cho_3`), `000001172` (UNMATCHED),
`000001346`, `000002202` (UNMATCHED), `000002677`, `000002775`, `000002801`, `000004133`.
Fix: teach the two single-model consumption paths in `index.html` to split `' + '` on the source
(the multi-model path already does), then drop the parser guard and re-splice. Engine turn — pairs
naturally with **B25**, which touches the same branch.


### B26 — per-N "up to N models can each have their X replaced with Y" — **CLOSED (D96, S41)**
`classify_per_n` now handles the passive-possessive form, reads the per-bracket cap from the sentence
("up to 3 models" → `max_per_n: 3`) instead of hardcoding 1, tolerates "can **each** be replaced", and
normalises the Death Company datasheet's "replaced with equipped with" typo. All 58 "For every N
models…" lines in the SM/DG set now classify; zero UNMATCHED per-N lines remain. Options gained by
Deathwatch Veterans `000002783` (+6), Blightlord Terminators `000001372`, Sword Brethren `000002798`,
Crusader Squad `000002799`, Death Company Marines `000001997`. No engine change was needed — the
multi-model path already splits a compound `' + '` source for `count` and for `count` +
`replacement_choices`.
**Carry-over:** option ids renumber on `000002783` and `000001997`; a saved pick on those two reads as
unselected and the user re-picks.


### B20 — CLOSED (engine half D93/v5.53; parser half D94/S39)
The rollup's `fixed: 1` branch now handles `count` options, and `loMaxCount` bounds any
`per_n_models` cap by the option's scope group. Live fixes: Reiver Sergeant/body grav-chute and
grapnel caps (`000002718`), Ravenwing Ancient grenade-launcher swap (`000002748`).
**Parser half closed in D94** — `classify_n_model_swap` now emits `max_total: N`. Helbrute's fist swaps are live (`cnt_2`, `cc_3`).


### B24 — profile-pinned `replaces` / `replacement` — **CLOSED (D95, S40)**
Weapon names in `unit_loadouts.json` are now family (base) names everywhere — options *and*
`default_weapons` / `default_weapon_counts`. `loadout_parser.py` emits them; `normalise_profiles` in
`equipped_parser.py` folds the whole file on every run so the invariant can't drift. This also fixed
a bigger bug found while scoping it: **45 of 217 units were dropping every multi-profile weapon from
the unit weapon table and the weapon-abilities roll-up**, because the rollup keyed the weapon by its
profile name and the table looked it up by base name.
**Carry-over:** a saved list that stored a `count`-choice pick as a profiled name ("Plasma gun –
standard") no longer matches the option's `replacement_choices` and reads as unselected. The user
re-picks; no data loss, no illegal list.


### B27 — Whirlwind's `default_weapons` contain weapons the unit does not have — **CLOSED (D96, S41)**
Confirmed as an `equipped_parser.segment` bleed. Composition anchors were attributed to the nearest
preceding **roster** title, so an off-roster datasheet (Astraeus, Thunderhawk — Legends entries sitting
right after the Whirlwind in `Space_Marines_web.txt`) had no title of its own and its equipped line was
credited to the Whirlwind. `find_titles` now recognises every datasheet block and returns `None` for an
off-roster one; anchors owned by `None` are dropped. A rewritten group also has its `default_wargear`
and `default_weapon_counts` cleared first, so bleed can't survive a re-run. One unit changed.


### B25 — two `choice` options in one single-model group replace the same weapon (engine/UI) — **CLOSED (D97, v5.54, S42)**
Three units: `000000083` Captain with Jump Pack (`cho_1` + `sng_3`, both replace Heavy bolt pistol),
`000001346` Lieutenant (`sng_2` + `sng_3`, both replace Bolt pistol), `000002801` Venerable
Dreadnought (`cho_1` + `cho_3`, both replace Assault cannon). They render as separate radio groups,
so the user can pick both; the rollup keeps whichever option is written last and silently drops the
other. The list looks legal and quietly isn't the list the user built. The fix is mutual exclusion —
options sharing a scope + `replaces` should be one control, or should lock each other out — not a
rollup patch. Note `000001346 sng_2` also carries a garbage parse as its only choice
("Neo Volkite Pistol, 1 Master-Crafted Power Weapon And 1 Storm Shield"), which wants fixing anyway.


### B23b (parser half) — stop reducing a compound source — **CLOSED (D98, S43)**
`loadout_parser.py` writes the full `' + '` source on `choice` / `single` options, splitting the
datasheet phrase on commas as well as " and ". `COMPOUND_SOURCE_UNSUPPORTED` and
`COMPOUND_SOURCE_ON_SINGLE_GROUP` retired (12 flags). 14 units changed; node sweep over 1,020 cases
produced 23 diffs, all the intended extra source weapon being consumed. The option `group` heading now
takes the first source weapon so a compound never reaches a heading. New flag `OR_SOURCE_UNSUPPORTED`
covers the one shape that stays truncated (Wulfen Dreadnought — see B31).


### B30 — the replacement side of a `single` swap isn't split on " and " — **CLOSED S45 (D100)**
Shipped as a data turn. The `single`-replacement side is now split on `" and "` / commas like the choice
list, and every replacement-side name that is a wargear item rather than a weapon is routed through the
allowlist into `equipment_parts`. Widened past the three named carriers to the whole replacement side
(`choices`, `replacement_choices`, `count.replacement`) — the same bug was live on ten more options.
13 options now carry `equipment_parts`. Flags 41 → 27. The **source** side is untouched: see B28.


### B31 — an "A or B and C" source — **CLOSED S99 (D165); DATA; `bundled_swaps.json` + `units.json`**
Shipped as a 5-endpoint `owns` bundle on Space Wolves / Wulfen Dreadnought `000004133`, not as a schema
extension. **Two flags closed, not one** — S99 found a second live flag on the same unit that this entry
never mentioned: line 2's `UNMATCHED` negated gate ("if this model is not equipped with a storm bolter, its
heavy flamer can be replaced with 1 storm bolter"). Enumerating endpoints dissolves both at once, because
"not equipped with a storm bolter" is exactly equivalent to "took line 1."

**The reading was settled from a sibling datasheet, not inferred.** Venerable Dreadnought `000002801`
line 3 offers the same blizzard-shield arm and enumerates its endpoints explicitly — no blizzard-shield
build in the Space Wolves range carries a heavy flamer *and* a storm bolter. So the storm bolter is
consumed in **both** branches of line 1.

**Why a bundle and not a general mechanism:** `OR_SOURCE_UNSUPPORTED` has exactly one carrier in all 217
units. A general either-of source field meant a parser change plus an engine change — two sessions and a
permanent schema concept — for a population of one. `_parser_flags` on the unit are deliberately left in
place: they accurately describe what the parser can express; the bundle overrides at a different layer.

**Live bug fixed:** the truncated `sng_1` removed only the greataxe, so picking it kept the storm bolter
beside the new heavy flamer and offered no wolf-claw alternative — an illegal build presented as legal.
No engine change (v5.82 unchanged); the `owns`-bundle suppression, weapon delta and grant paths all shipped
for the Captain in D113. New harness `b31_check.js`, 42 assertions passing, negative control confirmed
(15 failures against pre-fix data). Diff-guard: exactly one unit, exactly one field.

*Original entry:*
`000004133` Wulfen Dreadnought: "this model's Fenrisian greataxe **or** great wolf claw **and** storm
bolter can be replaced with…". The model carries one of the two; the engine keys a source by name and has
no "either of these" source. Flagged `OR_SOURCE_UNSUPPORTED` and truncated to the first source weapon,
which is what it did before D98 — this is a named gap, not a regression. Fix wants either a source that
can name alternatives, or per-carrier authoring once the Wulfen Dreadnought's two variants are separate
model groups.


### B28 — a swap whose source is a wargear *item*, not a weapon — **CLOSED (D101 engine S46, D102 data S47; header corrected S92)**
Three options name a source the model carries as gear rather than in its weapon table, so they can
never consume it: both Wulfen units' `cnt_1` (death totem → stormfrag auto-launcher) and the Wolf
Guard Battle Leader's `cho_2` (storm shield → bolt carbine / heavy bolt pistol / plasma pistol).
Each carries a `WEAPON_NOT_FOUND` flag. Since D97 the engine skips them and the UI hides them (they
were dead controls or, on the Wulfen, a free weapon). To restore them the source has to be
representable — either the item joins the group's gear list, or a swap gains an `item_source` field.
Pairs with the equipment channel (D99), which solved the *replacement* half of the weapon/item boundary.
B28 is the remaining *source* half: an item the model carries as gear cannot be consumed by a swap.
**Carrier list corrected S45.** After D100 cleared the replacement side, the source-side flags are the
*only* `WEAPON_NOT_FOUND` left, and there are **five**, not three: Terminator Assault Squad `000000118`
(storm shield), Wulfen `000000311` (death totem), Wolf Guard Battle Leader `000004130` (storm shield),
Wolf Guard Headtakers `000004131` (storm shield), Wulfen with Storm Shields `000004132` (death totem).
The category is now clean — B28 is exactly the set of remaining `WEAPON_NOT_FOUND` flags.

**Engine half CLOSED (D101, S46).** The engine now rolls up `default_wargear`, accepts a gear item as a
swap source, and keys source charging by base name. Terminator Assault Squad `000000118` and Wolf Guard
Headtakers `000004131` are fixed outright (their compound source now consumes the shield too).

**Data half CLOSED (D102, S47).** `equipped_parser.py`'s `Datasheets.csv` gap-fill now admits a single-group
unit when its loadout prose names a wargear-allowlist token that fails the weapon lookup, so the item lands
in `default_wargear`; `loadout_parser.py` resolves a source-side item through the allowlist instead of
flagging it. `WEAPON_NOT_FOUND` is now **zero** (flags 27 → 22: 21 UNMATCHED + 1 OR_SOURCE_UNSUPPORTED).
Five units gained gear — the three targets plus Azrael (the Lion Helm) and Ezekiel (Book of Salvation),
which the same mechanism caught. The death-totem count question resolved on the datasheet: "Every model is
equipped with: ... death totem", one per model, no product call needed. **B28 is closed.**


### B29 — "Additional Combi-Bolter" isn't normalised to a weapon — **CLOSED (D98, S43)**
`000001047` `ach_1` offers "Additional Combi-Bolter" or "Combi-weapon"; the first fails the weapon
lookup and now lands in the weapon table under that literal name. The datasheet means a second
combi-bolter. **Fixed:** `normalise_weapon` strips a quantity qualifier ("additional" / "another" /
"second" / "extra") and resolves the weapon underneath, so the pick stacks a second copy. Chaos Rhino now
ends with two combi-bolters; the Helbrute's "additional Helbrute fist" swap (`000001046` `cho_1`) was the
same bug and is fixed with it. Two `WEAPON_NOT_FOUND` flags retired.


### P1 — `loadout_parser.py` stale-copy failure — **CLOSED S57 (D118)**
Ten consecutive sessions ran with a pre-S47 parser that silently dropped `equipment_parts`, compound gates,
bearer-gated adds and negated-gate adds, and emitted 368 definitions where the roster holds 217. Rebuilt to
reproduce the committed `unit_loadouts.json` byte-for-byte, fixed point through the equipped chain confirmed.
The written freshness checklist is retired and replaced by assertion **P1** in `rules_assertions.py`, which
fails the build if any of the four capability functions is absent.


### H3 — `pipeline_manifest.py` custody: get the script into the project file area — **CLOSED S126 (D198)**
`pipeline_manifest.py` has never existed in the synced project files, while `pipeline_manifest.json`
always has. That combination is the worst of both: assertion **P3** fails unconditionally *and* the
manifest cannot be regenerated, so it drifts unobserved. It had been in that state since D123
introduced it.

Two pieces of evidence for how costly that is. D193 found **13 of 24 guarded hashes stale** when it
finally checked by hand. Then S124 opened with the **pre-S123 manifest back in place** — 24 files
rather than 27, the same 13 stale hashes — so a whole session's manifest work had been reverted by a
sync and nothing noticed, because the thing that would have noticed is the assertion that could not run.

**S124 writes the script.** The guarded set now lives *in the script* rather than only in the JSON, so
it survives either file being lost; `--write` fails loudly on a missing file instead of quietly
shrinking the guarded set; and `check()` reports a JSON that is older than the script, which the old
arrangement could not express. Guarded set **24 → 35**. P3 passes.

**Closed S126.** T1's `repo_check.py`, run against the real repo at session open, found the repo
holding 70 files with every one shared with the project area byte-identical — `pipeline_manifest.py`
included. The script has reached the project file area and stayed there. See D198.

### H4 — Ryan's per-session repo refresh becoming routine — **CLOSED S126 (D198)**
Opened per the revised S126 prompt to track whether the bulk repo upload and the habit of refreshing
it each session actually take hold, rather than living only as a hope in a handoff. Closed on direct
evidence: `repo_check.py` found the repo at 70 files with 67 shared with the project area all byte-
identical at session open — the refresh has visibly been happening. Revisit only if a future
session's `repo_check.py` run finds drift.

### T1 — `repo_check.py` (net new) — **CLOSED S126 (D198)**
Clones the public repo and classifies every file it holds as match / differs / missing-from-repo /
repo-only against the project working area. GW-derived material found in the repo is a distinct,
louder failure than ordinary drift. Reads its exclude patterns straight out of the clone's own
`.gitignore`, bucketed by that file's own section-header comments, rather than hand-maintaining a
second pattern list that could drift from it. "Missing from repo" is scoped to the manifest's live
guarded set plus a fixed doc list plus every locally-present `SESSION_HANDOFF_*.md`, not to the whole
project area (most of which is GW/Wahapedia source material that is correctly and permanently
excluded). A clone failure reports clearly (exit 2) rather than a false clean. See D198.

### T2 — SHA-256 hash convention in handoffs — **CLOSED S126 (D198)**
Every handoff's Files section now carries a first-12-characters SHA-256 per changed and net-new
file, verified by the next session before anything else runs. Deliberately redundant with T1 — still
catches a bad sync one session later even if the repo is unreachable when `repo_check.py` runs.
Applied starting with `SESSION_HANDOFF_126.md`. See D198.

### T3 — `baseline.sh` (net new) — **CLOSED S126 (D198)**
One command, one line per gate: both repro checks, the detachments repro check, `rules_assertions.py`,
all thirteen harnesses with their correct positional arguments encoded, `bundle_check.js`,
`pipeline_manifest.py`, and `repo_check.py` (skippable via `--no-repo`). Encodes the argument shapes
that previously had to be re-derived per session from each harness's `Usage:` line. Verified
end-to-end mid-session: correctly went red on `rules_assertions` and `pipeline_manifest` when T4's
edit to `bundle_check.js` left the manifest briefly stale. See D198.

### T4 — known-failure allowlist in `bundle_check.js` — **CLOSED S126 (D198)**
`ok()` now accepts an optional key; a keyed check that still fails prints `KNOWN` and does not count
toward the exit code, but fails loudly (`FAIL allowlist stale`) the moment it resolves without the
allowlist being updated, or if an allowlisted key never runs at all in a given execution. The two
existing B36 failures (merged-radio-vs.-three-independent-Keep-rows) are keyed as `b36-keep-count`
and `b36-keep-offered`; empty `KNOWN_FAILURES` when B36 ships. See D198.

### T5 — backlog and decision-log split — **CLOSED S126 (D198)**
`OPEN_ITEMS_BACKLOG.md` had grown to 166 KB, almost entirely closed-ticket narrative. Of 117 tracked
tickets, 7 are genuinely open (H3, E21, E4, B56, E12, P2, B17 — H3 has since also closed, see above).
Those keep full bodies in the working file; the other 110 moved in full to `BACKLOG_ARCHIVE.md` (this
file, net new), with a one-line pointer left behind. Verified byte-for-byte against the original —
zero content lost or duplicated. `DECISION_INDEX.md` (net new) adds a one-line-per-entry index over
`40K_Decision_Log_v3_0.md`, which is itself unmodified and remains authoritative. See D198.

### T6 — module-extraction policy — **CLOSED S126 (D197)**
No further extraction of code out of `index.html` without a positive, name-able reason. `list_store.js`
stays as the one existing extraction, unused a second time anywhere and costing a standing sync-guard
tax (`e1b_check.js`) for a payoff the project has not drawn on. Recorded as policy, no code touched.
See D197.


- v5.33: removed the "(fixed)" size label.
- v5.34: systemic per-model keyword / faction-keyword / wargear-ability pass;
  points join-normalization; units.json reproduction chain established.
- v5.35: configured popup now renders faction line, model-specific keyword lines,
  and Wargear Abilities (was only in the available-unit popup); `buildStatTable`
  strips the doubled "+" on SV/LD.


## Doc debt still open (this session's close-out)
- D69 — points join-normalization + units.json reproduction chain established.
- D70 — systemic per-model keyword / faction-keyword / wargear-ability pass (v5.34).
- Data Dictionary — add `faction_keyword_names`, `model_keyword_names`,
  `wargear_ability_names` to the model-group schema.

### E4 — Detachment enhancement assignment — **CLOSED S129; SCOPED S127 (D199), E4b SHIPPED S128 (D200), E4c SHIPPED S129 (D201)**
Design is D199, as corrected by D200. The planned E4a data turn was cancelled — the 515 enhancement
records verified clean in S127. Eligibility keys off `unit_type`. Two data facts shaped the design:
29 same-army cross-detachment name collisions make the duplicate rule name-keyed army-wide, and
Deathwing Assault at 30/15 pts in two Dark Angels detachments means a stored assignment must carry
its detachment key, not just the name. Four batched calls for Ryan ride in D199 (duplicate identity,
Epic-Hero-ban-on-Upgrades, free-text restrictions displayed-not-enforced, inline config-panel picker
UI) — still formally unreviewed by Ryan at close; calls 1, 2 and 4 are load-bearing in shipped code.

**E4b — engine + persistence — SHIPPED S128 (D200).** Per-entry `enhancement: {name,
detachment_key}`; `list_store.js` schema v2→v3 with `normaliseEnhancement()` at the boundary;
`canAssignEnhancement` as the single read path over the five 25.04 rules (hard block, D114/D115
line); the Upgrade carve-out (three copies, all priced, only the first counted); the one-per-unit
rule enforced over the *attached* unit; attach-action gate as the second enforcement point; points
folded into `ptsForEntry`; flag-don't-drop on stale imports. Two calls beyond D199: a duplicated
unit does not inherit its enhancement, and ghost entries' enhancements do not count. Five
assertions added (E4b-1..5) plus `e4b_check.js`; E1b-2 repinned to schema 3. D200 corrects D199's
eligibility claim — the keyword derivation only agrees once written as CHARACTER *and not* EPIC HERO.

**E4c — assignment UI — SHIPPED S129 (D201).** Inline single-select row in the unit's config panel,
filtered to rows `enhancementTypeEligible` for the unit — plus two calls beyond D199: whatever an
entry currently holds stays in its row list even if stale, so it is always clearable; and each row
carries the same expandable rules-text detail every other pick in this panel has, with the
previous-edition tier badge, since the panel's own convention and the prior handoff's standing note
both anticipated it. Roster-level "Enhancements n/limit" chip off `enhancementArmyState`, with
warning lines (never trimmed) for the states only an import or a battle-size/detachment change can
reach — `over`, `notOffered`, `wrongType`, `sharedUnits`. `e4c_check.js` net new, 75 checks. No new
legality — every verdict is `enhancementRowState` / `canAssignEnhancement` / `enhancementArmyState`'s
answer, rendered.

### B56 — 81 built units carry no points — **CLOSED S129 (D202); NEW S99 (D166); DIAGNOSED S100 (D167); B56a SHIPPED S101 (D168), B56b SHIPPED S102 (D170), B56c SHIPPED S103 (D171), B56d SHIPPED S104 (D172), B56g CLOSED S108 (D174/175/176), B56e RETIRED S121**
Note: B56c/B56d do not themselves close any of the 81 null-points units — B56c/B56d is a separate
override mechanism for units that already carry a generic price. See B56c and B56d entries.
**81 of 270 units had `points: null`** at diagnosis — Space Wolves 20, Black Templars 18, Dark Angels
16, Blood Angels 15, Deathwatch 10, Adeptus Astartes 2. All SM-family chapter units.

**Why it mattered:** a null-points unit renders "—" and contributes 0 to the army total, so it is
addable and configurable. A 2,000-point list could be built 81 units deep at zero cost — a real
legality hole against D0. Not an error state, just silently free.

**Diagnosed S100 (D167).** Not one ticket. Split into B56a–B56g. Corrections to the S99 framing, all
re-derived from current data:
- The five chapter files closed 77, not 78 at the time. `MFM_Chapter_Pass.md` had drifted in both
  directions — SW's Venerable Dreadnought was since costed from base, and all four vanilla-chapter
  stragglers it listed closed.
- Wolf Guard Headtakers and Crusader Squad were a parser gap, not a name mismatch — both names
  matched exactly; their MFM size-bracket lines named a composition rather than "N models", which
  `COST_RE` could not read. Closed via B56b (Crusader Squad) and B56g (Wolf Guard Headtakers).
- Judiciar Xacharus and Chaplain Kastiel appear in no MFM file in the project — unsourceable.
  **Retired S121 (B56e): Ryan's call to disregard these two characters.**
- Black Templars was the scoping risk flagged at diagnosis time: 9 of its 18 datasheets share a name
  with an Adeptus Astartes datasheet, and an unscoped chapter run would write those rows under
  `Adeptus Astartes`, overwriting generic base prices while leaving BT uncosted.
- D42 held. The real override population was 11 rows across 4 chapters, not the larger set implied
  by raw diffs — BT's three apparent overrides were its own natively-priced datasheets.

**Closed S129 (D202).** Verified directly against `units.json` rather than trusted from the header's
own stale count: 270 total units, exactly 2 carry `points: null` — Judiciar Xacharus and Chaplain
Kastiel, both retired. The header had never been updated after the last chapter fixes landed, so it
had been sitting open for several sessions past its actual completion.

### B63 — Soul Grinder ships all four god weapons at once — **NEW S131 (D206); LIVE D0 VIOLATION; SHIPPED S132 (D207)**

`index.html` filters god-conditional weapons at lines 6580 and 6604 on `w.allegiance_condition`.
`convert_to_json.py` never reads the `Allegiance_Condition` column, so the field never reaches
`units.json` and the app's filter is dead code reading a field that is not there. Soul Grinder
therefore shipped with torrent of burning blood, warp gaze, phlegm bombardment **and** scream of
despair all flagged as base equipment simultaneously. Pick Khorne, receive all four.

Predates the S131 recovery — the committed `units.json` pulled from the repo already lacked the data.
The rebuild exposed it, it did not cause it.

**Ryan's ruling (D206):** exactly one god weapon is added, set by the allegiance chosen at
list-building. The four become allegiance-tagged conditionals rather than base equipment. Base
equipment is Harvester cannon, Iron claw and Warpsword; Warpclaw stays the existing swap against
Warpsword; one god weapon is added on top, replacing nothing.

**Shipped S132 (D207).** `Allegiance_Condition` restored as `Unit_Weapons.csv`'s sixteenth column,
matching `wahapedia_transform.py`'s existing header order. Populated on the four Soul Grinder rows per
the D206 mapping; `Is Base Equipment` cleared on the same four (now `No`, was `Yes`). Threaded through
`convert_to_json.py` into the weapon objects as `allegiance_condition` — present as `null` on every
weapon that doesn't carry one, non-null only on Soul Grinder's four. The full pipeline was re-run
exactly as `units_repro_check.py` runs it and its output copied over the committed `units.json` and
the four merged lookups; diffing old against new confirmed the only substantive change in the entire
catalogue is Soul Grinder's eight weapon rows. `units_repro_check.py` reports byte-identical
reproduction again — the fixed point is re-banked, not hand-patched.

Four assertions filed: **B63-1** (exactly four allegiance-tagged weapons, one per god), **B63-2**
(none of the four is base equipment; Harvester cannon, Iron claw and Warpsword all are), **B63-3** (no
unit anywhere else in the catalogue carries the field), **B63-4** (every value is one of the four god
name strings `index.html`'s `GODS` array uses). Assertions 84/84 at close.

**Converter-only turn, no engine work** — the app-side filter already existed and was simply reading a
field that never arrived. `index.html` untouched at 6.5. **Not yet verified on the rendered app** —
Ryan needs to confirm each god selection yields exactly one god weapon.
