# Open Items Backlog

Originally logged Session 18; reorganised **S126 (T5)** — closed/shipped ticket bodies moved in
full to `BACKLOG_ARCHIVE.md`. Each keeps a one-line pointer here (ID, title, closing session,
decision reference). The Open Items section below is the only section awaiting work; if it is
not here, it isn't open. **7 open** as of S130 close: B61 (live D0 violation, next), P2, E21 (scoped a/b/c/d), E22 (partly unblocked), B60, E12, B17.

## Open Items


### P2 — `loadout_parser.py` custody — **NEW S58; PROCESS; softened by D123 (S59)**
The durable fix — commit the parser to the GitHub repo as canonical, mirror to project knowledge — is still
Ryan's call. But the pipeline is now self-defending regardless of where the parser lives: a stale or wrong copy
fails P1 (reproduction) and P3 (manifest) on the baseline run and by name, so a bad copy can no longer cost a
whole session's work silently. See **D119, D123**.


### E21 — Detachment-driven army-construction effects — **SCOPED S130 (D203); AMENDED by D204; splits E21a/b/c/d**

Detachment rules that require or forbid units, or elevate units to Battleline (which moves the count
cap — Functional Spec §5). Opened S122 (D192), gated on E1c, scoped S130.

**The S122 framing was wrong and is retracted.** The ticket read "34 detachment abilities across the
full dump carry require/forbid language, in free prose with no common shape." Re-derived from source
in S130: the dump-wide figure is ~41 real muster-time effects (57 raw matches, less in-battle false
positives), the dump is the wrong denominator anyway, the shapes reduce to four recurring kinds, and
against our **143 built detachment records** the untouched work is **six detachments, not
thirty-four** — two of which are blocked and moved to E22. Full derivation in **D203**.

**25 of the 143 are already enforced structurally.** Chapter exclusivity ("your army may include this
Chapter and no other") cannot be violated: `resolveUnits()` composes a chapter army as the generic
Adeptus Astartes block plus that chapter's own units, so no foreign-chapter unit is ever in the pool.
D0 satisfied by construction. E21 adds an assertion to police it, not a feature.

**Mechanism: a hand-authored `detachment_effects.json`, not a text parser.** Three findings kill the
parser approach — `rule_text` spans three fidelity tiers of which one is a paraphrase that
*disagrees on rule content* (Shadow Legion's Be'Lakor requirement exists in the faction-pack text and
nowhere in Wahapedia); nine built detachments carry no rule text at all, so a parser silently emits
nothing and reports success; and the unit names in the prose do not match `units.json` ("Daemon
Prince" vs. **Daemon Prince of Chaos**, "Be'lakor" vs. **Be'Lakor**), so a name-matcher would forbid
nothing while appearing to work. Hand-authored input + referential-integrity assertions fails loudly
on a typo; a parser fails silently. See D203 for why this does not breach *fix parsers, never
hand-edit outputs* — that rule protects generated outputs, and this is an input.

**Amended by D204 (Ryan's rulings):**
- **Effect kinds are `battleline` | `forbid` | `unlock` | `warlord`.** `require` is dropped — no built
  detachment needs it. Be'Lakor is **not** required by Shadow Legion; he is optional, and *if included
  must be the Warlord*. The faction-pack paraphrase had compressed a conditional Warlord constraint
  into an unconditional inclusion requirement, inverting the rule's logical shape — which strengthens
  D203's case for authoring from the rules rather than from `rule_text`.
- **Elevated units render under the Battleline group**, not in their own group with a badge. D203's
  scanning argument lost to comprehension of a legality-relevant fact, and New Recruit does it this
  way. Cost checked: `unit_type` is read at two grouping sites and one limit site; all three take a
  single `effectiveUnitType(unit, selectedDetachments)` helper, live against the current selection.

**The split:**
- **E21a — data-only.** `detachment_effects.json` + referential-integrity and unenforced-inventory assertions.
- **E21b — engine-only.** `effectiveUnitType()` feeding `instanceLimit()` **and** both grouping sites, plus the chapter-exclusivity structural assertion.
- **E21c — engine-only.** Forbid + conditional Warlord — Shadow Legion add-path refusal and army state, in E4b's mould. Runs with E22b (same turn, same table).
- **E21d — UI-only.** Refusal prose, roster warnings, Battleline indicator. E21 closes here; it does not wait on E22.

**The six live cases:** Battleline elevation in Blood Angels|THE LOST BRETHREN (Death Company
Marines ×2), Dark Angels|COMPANY OF HUNTERS (Outrider Squad), Death Guard|SHAMBLEROT VECTORIUM
(Poxwalkers); require/forbid in Chaos Daemons|SHADOW LEGION; and two unlock cases moved to E22.


### E22 — Detachment ally unlocks, points sub-caps and Warlord bans — **NEW S130 (D203); PARTLY UNBLOCKED by D204**

Some detachments unlock units from another faction, capped by a points sub-budget keyed to battle
size, with a rider that no unlocked model may be the Warlord. Two cases touch built armies:
Death Guard|TALLYBAND SUMMONERS (Plague Legions) and Chaos Daemons|SHADOW LEGION (HERETIC ASTARTES).

**D203 said nothing in the app could name an allied unit set. That was wrong.** Per Ryan's ruling and
verified in D204, the MFM faction files define each group as a named section carrying that group's
units and their in-context points: **PLAGUE LEGIONS** (Death Guard, line 140), **SCINTILLATING
LEGIONS** (Thousand Sons), **BLOOD LEGIONS** (World Eaters), **LEGIONS OF EXCESS** (Emperor's
Children), **HARLEQUINS** and **YNNARI** (Aeldari). Every god-legion case in the priority factions,
found the same way.

**Death Guard half is fully buildable** once B61 lands the marking. **Shadow Legion stays blocked** —
`MFM_Chaos_Daemons_v1_0.txt` has no HERETIC ASTARTES section; that unlock is an explicit ~15-name list
in the detachment's own text and every name is a Chaos Space Marines datasheet, so it waits on CSM
(already next in the faction priority order). Its record ships in `detachment_effects.json` with
`enforced: false`.

- **E22a** — folded into **B61** (the marking is the same parser change).
- **E22b — engine-only.** Gate allied units on the unlocking detachment; enforce the battle-size
  points sub-cap as a second budget; enforce the Warlord ban. Runs with E21c.


### B63 — Soul Grinder ships all four god weapons at once — **NEW S131 (D206); LIVE D0 VIOLATION; S**

`index.html` filters god-conditional weapons at lines 6580 and 6604 on `w.allegiance_condition`.
`convert_to_json.py` never reads the `Allegiance_Condition` column, so the field never reaches
`units.json` and the app's filter is dead code reading a field that is not there. Soul Grinder
therefore ships with torrent of burning blood, warp gaze, phlegm bombardment **and** scream of despair
all flagged as base equipment simultaneously. Pick Khorne, receive all four.

Predates the S131 recovery — the committed `units.json` pulled from the repo already lacked the data.
The rebuild exposed it, it did not cause it.

**Ryan's ruling (D206):** exactly one god weapon is added, set by the allegiance chosen at
list-building. The four become allegiance-tagged conditionals rather than base equipment. Base
equipment is Harvester cannon, Iron claw and Warpsword; Warpclaw stays the existing swap against
Warpsword; one god weapon is **added** on top, replacing nothing.

**Fix (converter turn):** restore `Allegiance_Condition` to `Unit_Weapons.csv` with the four values
from `chaos_daemons_reference.md`, clear `is_base_equipment` on those four rows, thread the column
through `convert_to_json.py` into the weapons objects, regenerate, re-bank the fixed point, and add an
assertion pinning exactly one god weapon per allegiance. No engine work — the app side already exists.

**Sequenced ahead of B61.** Both are D0 violations on built factions; this one hands out weapons the
unit cannot legally have, and needs no engine turn.


### B62 — `FALSE` string literal in Is Base Equipment, and no presence gate on the CD CSVs — **NEW S131 (D205); S**

Keeper of Secrets' Shining Aegis and Soul Grinder's Warpclaw carry the literal string `FALSE` in the
Is Base Equipment column instead of `Yes`/`No`. The converter does not recognise it and passes it
through, so `units.json` ships the string `"FALSE"` where every other weapon carries a boolean.
Harmless today, latent trap tomorrow — and it was the last six bytes standing between fail and pass
during the S131 rebuild.

Second half of the ticket: the nine Chaos Daemons CSVs have no presence-and-parse assertion. When
three went missing this session the symptom was a confusing repro byte mismatch rather than a clear
"missing pipeline input". Add the assertion to `rules_assertions.py` so a missing or malformed one
fails loudly at session open.


### B61 — Plague Legions units are offered to every Death Guard army, ungated — **NEW S130 (D204); LIVE D0 VIOLATION; S–M**

All six Plague Legions units — Beasts of Nurgle, Great Unclean One, Nurglings, Plaguebearers, Plague
Drones, Rotigus — are already in the Death Guard army in `units.json` and offered with **no gate at
all**. A Death Guard player can field Great Unclean One and Rotigus under any detachment or none, with
no points sub-cap and with Rotigus eligible as Warlord: three live illegalities on a built faction.
Not an unshipped gap — a reachable illegal state, which under D0 outranks everything else open.

**Cause:** Wahapedia carries these six datasheets twice, under faction `CD` and again under `DG` (the
DG copies exist because the detachment makes them includable). `mfm_points_parser.py` reads a unit
header as an ALLCAPS line followed by a tier header; `PLAGUE LEGIONS` is followed by a unit name, so it
is correctly not read as a unit — but is not read as anything else either, and the six units below it
flow into the Death Guard block indistinguishable from Plague Marines.

**Fix (parser turn):** recognise the allied-group section header, tag the units below it with an
`allied_group` field, regenerate `units.json`, re-bank the `units_repro_check.py` fixed point, add
assertions pinning the allied set per army. E22b then consumes the field.

**Checked and clean, so nobody re-opens these:** `LEGENDS` sections are handled (explicit skip map in
the parser; no Legends unit is in any pool), and the Space Marines chapter sub-sections split
correctly via the Wahapedia datasheet blocks (Darnath Lysander is in Imperial Fists, not in the
generic pool). An early crude scan this session suggested five Space Wolves Legends leaks — a false
positive from misreading leader-attachment lists as datasheet names.


### B60 — `detachment_parser.py`: `restrictions` is populated inconsistently — **NEW S130 (D203); S**

Of the 25 built detachments carrying chapter-exclusivity text, **11 hold it in the `restrictions`
field and 14 hold the identical sentence inside `rule_text` — zero overlap.** The split tracks the
text-source tier, not the content, so `restrictions` currently presents itself as a structured field
while being unreliable as one. Only 12 of 143 records have it populated at all.

Does not block E21 — `detachment_effects.json` reads neither field — but anything downstream that
trusts `restrictions` will be reading a field that is right less than half the time. Parser fix and
a `detachments_repro_check.py` regeneration; no engine or UI impact.


### E12 — User accounts (login/passwords) — **OPEN; DEFERRED S121 (Ryan: hold until near the end); L; architectural**
Biggest lift by far — moves the app from static GitHub Pages + local storage to
something with a backend/auth. Flag: this reshapes hosting and data storage and
should be scoped on its own, well apart from the list-builder work. Ryan has
deferred this to late in the roadmap, after the list-builder feature set is otherwise done.


### B17 — Loadout completeness gaps — **PARTS 1–2 + ENGINE TURN DONE (Sessions 24–26, D79/D80/D81); remainder S–M.**
Part 1 (option-parser gaps) shipped: `loadout_parser.py` now handles per-N clauses with
"in the unit" / "up to N" / active voice, active-voice definite (sergeant) swaps,
active-voice "any number / all" swaps, and by-name equipment adds (Watcher in the Dark).
Five units fully or partly cleared — Talonstrike (3→0 flags), Decimus (4→0), Deathwing
Terminator Squad (2→0, incl. the storm-bolter swap group + Watcher), Fortis (5→3),
Spectrus (4→2). Data-only, `index.html` still v5.45.

**Part 2 (Session 25, D80) — DONE (four of five flags):** indefinite single-model swap
(`count` + `max_total:1`) and conditional per-model scope (`requires_weapon`) now parse.
Cleared: Fortis vengor, Fortis plasma-pistol (dormant gate), Fortis grenade-launcher per-5
(live gate), Spectrus instigator. Fortis 3→0, Spectrus 2→1. Data-only, `index.html` still v5.45.

**Engine turn (Session 26, D81) — DONE.** `index.html` **5.45 → 5.46**. Count path now honours
`requires_weapon` (rollup skip + clear-on-lose + disabled "needs `<weapon>`" render) — the
Fortis plasma-pistol gate is live (harmless today; nothing removes the incinerator). Shared-pool
cap now also seeds from `max_total` members (bounded by the largest member; `per_n_models` keeps
precedence). New `classify_conditional_add_choice` handles "One model equipped with a `<weapon>`
can be equipped with one of the following: …" → capped adds sharing a per-sentence `pool_id`.
Spectrus helix/comms modelled as two `max_total:1` equipment adds, shared pool (cap 1),
`requires_weapon` marksman bolt carbine → exclusive one-model choice. **Spectrus 1→0 flags.**
Splice was one unit, `options`/`_parser_flags` only; `model_groups` byte-identical; fixed point
holds; CD verbatim. Render states unverified in-DOM.

**Variant sub-group DEFAULT weapons (true 1b) — DONE (Session 28, D83).** Root cause was a
`match_group` gap, not merged-list synthesis: the per-variant "…with `<weapon>` is equipped
with: …" lines already exist in prose but failed to bind because the singularizer only
normalized the trailing word (the plural sat mid-phrase). Added a per-word-singularized
unique-equality fallback to `match_group`; re-derived the three affected units (Spectrus,
Fortis, Heavy-Intercessor team `000002781`), correcting ten variant groups' `default_weapons`
to their authoritative loadouts. Only those units changed; base groups/options/flags/counts
byte-identical; fixed point re-established; CD verbatim. Data-only, `index.html` v5.47.

**Still open in B17 (banked with reason):**
- **Reiver Squad** — **DONE (D84, S29).** Two new classifiers (`classify_conditional_add`,
  `classify_all_models_add`): Sergeant conditional combat-knife add gated on bolt carbine
  (reuses `requires_weapon`); grav-chute + grapnel as independent per-model equipment adds
  fanned across both model groups. Only `000002718` changed; fixed point re-established; CD
  verbatim; v5.47.
- **Sanguinary Guard** — "One model can be equipped with 1 Sanguinary banner" (max-1 add)
  + confirm the 3/6 size selector surfaces from `size_brackets [3,6]`. **S–M.**
Fix parsers, not output; the five-unit change reached the preserved file via strip-from-
existing → re-parse → splice options/flags, keeping B16 `default_weapons` byte-identical.


## Closed / Shipped — pointers

Full history for every one of these lives in `BACKLOG_ARCHIVE.md`, in the same order.

- **H3** — `pipeline_manifest.py` custody — CLOSED S126 (D198); `repo_check.py` confirms the script is present and byte-identical in the public repo
- **H4** — Ryan's per-session repo refresh becoming routine — CLOSED S126 (D198); repo_check.py found the bulk upload had happened and 67/67 shared files matched
- **T1** — `repo_check.py` (net new) — CLOSED S126 (D198)
- **T2** — SHA-256 hash convention in handoffs — CLOSED S126 (D198)
- **T3** — `baseline.sh` (net new) — CLOSED S126 (D198)
- **T4** — known-failure allowlist in `bundle_check.js` — CLOSED S126 (D198)
- **T5** — backlog/decision-log split (`BACKLOG_ARCHIVE.md`, `DECISION_INDEX.md`, both net new) — CLOSED S126 (D198)
- **T6** — module-extraction policy — CLOSED S126 (D197)

- **B1** — Ability-description collision (SYSTEMIC) — AUDITED S76 (D141), residual risk (B1b) SHIPPED S77.
- **B2** — "Leader" rule shows the game Leadership rule, not the unit's Leader ability — CLOSED (audited S78, D143)
- **B3** — Wrong faction assignment: Chaplain Kastiel & Judiciar Xacharus — CLOSED (already resolved)
- **B4** — Roboute Guilliman missing abilities — SHIPPED S87 (D155)
- **B5** — SM Lieutenant weapon swap wrong (all-three-at-once) — SHIPPED (v5.41)
- **B6** — Captain weapon swap wrong (one-of-the-following) — SHIPPED (v5.41)
- **B7** — Multi-leader attachment not supported — CLOSED S89 (D157) — mechanic already shipped in B38 cluster; residuals reshaped into B7a and B7b
- **B7a** — leader-stack cap semantics (engine) — CLOSED S90 (D158)
- **B7b** — combined attached-unit popup with per-stat aura markers — CLOSED S91 (D159); cluster: leader system
- **B8** — Unit classification mis-buckets multi-model units — CLOSED (D71, v5.36→v5.37) — backlog entry was stale, corrected S92
- **B9** — Company Heroes weapon counts (heterogeneous fixed group) — SHIPPED
- **B13** — Victrix embedded Epic Heroes: optional-model toggle + 1-per-army cap — CLOSED (D158 Piece 1 v5.79 S92; D159 Piece 2 v5.80 S93)
- **B10** — DW Decimus Kill Team: no config options / not attachable — CLOSED (stale; corrected S92)
- **B11** — SV/LD data carries a trailing "+" while INV/FNP are bare — CLOSED S109 (D177)
- **B12** — Wargear stat effects not applied to the statline — CLOSED (v5.39–v5.42)
- **B15** — Conferred always-on wargear characteristics not on the statline (broad pass) — CLOSED S53 (D112, v5.59)
- **B14** — Optional per-model wargear matcher ("1 X can be equipped with…") — DONE (SM), D76
- **B14b** — Mixed weapon+item exclusive group (Impulsor group C) — CLOSED (D99, S44)
- **B18a** — option scope: generic "models" means EVERY model group (uncapped shapes) — CLOSED S58 (D120)
- **B18b** — pooled cap on `count` options — CLOSED S61 (D126); index.html v5.66
- **B18c** — fan the capped generic swaps (two clean units) — CLOSED S65; DATA; `unit_loadouts.json` 217 units / 327 options
- **B18d** — capped generic swaps on leader-conflict units — CLOSED S82 (D149); equipped_parser.py + unit_loadouts.json 217/336
- **B18e** — engine: enforce shared `pool_id` cap on the weapon rollup — CLOSED S64 (D129); index.html v5.67
- **B18f** — general capped-generic fan for remaining under-grant units — CLOSED S83 (D150) — no defect; candidate list rested on a D116 misreading
- **B18g** — Decimus Kill Team infernus heavy bolter: generic swap under-granted to a second body group — CLOSED S86 (D153)
- **B18h** — executable D116 guard on the fan allowlist — CLOSED S84 (D151)
- **None** — ### B18 (original) — CLOSED S99 — every sub-item shipped; header was stale
- **SG1** — Sanguinary Guard banner (one-model item add) — DONE (D85, S30)
- **B14c** — Bearer-qualified adds ("1 model equipped with a <weapon> can…") — CLOSED S99 — all three parts shipped; header was stale
- **B14c(b)** — bearer-gated adds, data half — DONE (Session 37, D92)
- **B19** — `requires_weapon` gate: carrier counting (engine) — DONE (Session 36, D91, v5.52)
- **B20** — `count` swaps scoped to a single-model group are silently ignored (engine + data) — CLOSED (D93 engine S38, D94 parser+data S39; stale entry corrected S92)
- **B21** — Options mis-scoped to the base group when the required weapon lives in a variant group — CLOSED S114 (D182)
- **B58** — banded optional model groups (0-N) are treated as 0-or-1 toggles — CLOSED S113 (phase 1 D180 / phase 2 D181)
- **B59** — Invader ATV should ride alongside the Outrider Squad and its +60 is uncharged — CLOSED S116 (D182/D183/D184); SHIPPED ACROSS B59a + B59b
- **B59a** — Engine: `non_consuming` handling in `loOptHeadroom` / `loGroupCounts` — CLOSED S115 (D183); ENGINE-ONLY; M
- **B59b** — Data / parser: MFM additive-line parser + Outriders group flip — CLOSED S116 (D184); DATA-ONLY; M
- **B32** — engine: `requires_weapon` with more than one weapon — CLOSED S49 (v5.57)
- **B33** — negated gates — CLOSED S50 (data)
- **B35** — paid wargear options — CLOSED (data half S51, engine half S52)
- **B34** — Size-gated wargear swaps (`required_size`) — CLOSED S95 (D160 + D161)
- **B42** — Vanguard Veterans' storm shield is missing from the loadout def — CLOSED S58
- **B43** — Wardens of Ultramar: Refractor Field has no carrier — CLOSED S58 as a duplicate of B44 (D121)
- **B44** — statline groups and loadout groups have no shared key — CLOSED S72 (D135 data half, D136 engine half)
- **B36** — Lieutenant wargear options are wrong — CLOSED S54 (D113), `index.html` v5.60
- **P3** — file-integrity manifest + reproduction gate — DONE (Session 59, D123)
- **B37** — Captain wargear panes are mislabelled — CLOSED S88 (D156), no build needed
- **B38** — a second leader on one unit (co-leader) — CLOSED S81 — B38-engine SHIPPED S79 (D145); B38a SHIPPED S80 (D146); B38b SHIPPED S81 (D147)
- **B39** — Bloodthirster options lock each other out wrongly — CLOSED S67 (D131)
- **B39b** — Audit the whole bundle queue for the same leftover-flat-swap class — CLOSED S67 (D131)
- **P4** — RESOLVED S68 (D132). units.json rebuild fixed point re-established for all 14 blocks.
- **B40** — Bloodmaster is missing its Leader rule — CLOSED S69 (D133), not a bug
- **B41** — Epic Heroes: adding past the limit should be blocked, not flagged — CLOSED S55 (D114 + D115)
- **B45** — army-level legality rules — CLOSED S100 — header retired S73 (D137), fully re-homed; kept surfacing as a candidate pick
- **E14** — Free, unconditional adds default to selected — CLOSED S56 (D117, v5.63)
- **B46** — wargear abilities granted by an OPTION never reach the popup — DONE (Session 59, D122; index.html v5.64)
- **B47** — information buttons on every configurable item and every option group (Configuration Panel) — DONE (Session 60, D124). v5.64 → v5.65
- **B48** — Corvus Blackstar renders two controls for the same wargear — DONE (Session 60, D125). Rode with B47
- **B49** — Leader section: show the character's attachment rule, not the generic core "Leader" blurb — CLOSED S70 (D134)
- **E15** — "Transport" as an ability, not just a keyword — CLOSED S97 (D163)
- **E16** — Sort control on "My Army Lists" page — DONE (Session 32, D87)
- **E17** — Asterisk on statline stats that have a non-representable rule benefit — DONE (D89, v5.51); SUPERSEDED S53 (D112)
- **E2** — Collapsible/expandable left-panel sections — SHIPPED S117 (D185)
- **E3** — Left-panel unit counts: red only when EXCEEDED, not when max is met — CLOSED S55 (D114)
- **E1** — Detachment selection system — CLOSED S125 (D196); parent over E1a/E1b/E1c/E1e; all four shipped
- **E1a** — Detachment data turn: parser + `detachments.json` — CLOSED S123 (D193/D194); DATA-ONLY; `detachments.json` 14 armies / 143 distinct records / 275 army slots / 515 enhancements / 797 KB
- **E1b** — Detachment state + persistence — CLOSED S124 (D195); ENGINE-ONLY; `index.html` 6.1 → 6.2
- **E1c** — Detachment picker + detail UI — CLOSED S125 (D196); ENGINE-ONLY; `index.html` 6.2 → 6.3
- **H2** — Retire three superseded Wahapedia join tables from the project file area — CLOSED S124 (D195); housekeeping
- **E1e** — Enforce detachment Unique-tag exclusivity — CLOSED S125 (D196); engine + UI
- **E5** — Rename banner "List Points" → "LIST POINTS" with two figures — SHIPPED S87 (D154)
- **E6** — Affordability cue on left-panel units — SHIPPED S118 (D187)
- **E7** — More spacing between points / info / x in the center panel — SHIPPED S87 (D154)
- **E8** — Delete safety — SHIPPED S87 (D154)
- **E9** — Warlord selection — DONE (Sessions 75–76, D139, D140)
- **E4** — Detachment enhancement assignment — CLOSED S129 (D199 scope, D200 engine, D201 UI); full body in `BACKLOG_ARCHIVE.md`
- **B50** — off-by-one column index in `wahapedia_transform.py` post-processing — DONE (Session 74, D138)
- **B51** — Blue Horrors' abilities/rules/keywords were miscolumned in the CD source — DONE (Session 75, D139)
- **B52** — `Sullen Malevolence (Aura)`'s ability description is truncated in the CD source — SHIPPED S77
- **B53** — Combined attached-unit popup renders bodyguard on top, leader on bottom — should be leader first — **CLOSED S96 (D162); `index.html` v5.81 → v5.82
- **B56a** — chapter Unit_Points rows (scoped) — SHIPPED S101 (D168)
- **B56b** — parser: composition-shaped size-bracket lines — SHIPPED S102 (D170) — Crusader Squad only
- **B56g** — Wolf Guard Headtakers: Hunting Wolves escort is an optional priced model group — CLOSED S108 (D174, D175, D176)
- **B56** — 81 built units carry no points (cluster header) — CLOSED S129 (D202); verified against `units.json` directly — 270 units total, exactly 2 null-points (Judiciar Xacharus, Chaplain Kastiel, both retired by Ryan's S121 call, B56e) — header was stale, all sub-items had already shipped; full body in `BACKLOG_ARCHIVE.md`
- **B57** — in-between unit sizes are not offered anywhere — CLOSED S118 (D186); no build needed
- **B56c** — derive the per-chapter points override map — SHIPPED S103 (D171)
- **B56d** — engine: apply the chapter override at selection — SHIPPED S104 (D172)
- **B56e** — Judiciar Xacharus & Chaplain Kastiel have no points source — RETIRED S121 (Ryan: disregard these characters)
- **B56f** — Venerable Dreadnought priced twice, generic and chapter disagree — CLOSED S101 (D169)
- **B54** — Be'Lakor's Shadow Form ability shows the rule name but not the pickable abilities — CLOSED S110 (D178)
- **B55** — `abilities.json` has drifted from what the pipeline currently produces — CLOSED S98 (D164)
- **E10** — Duplicate unit in center panel — DONE (S81, D148)
- **E11** — Light/dark background toggle — SHIPPED S120 (D190); closed
- **E20** — Visual polish, phase 2 (deferred items from E11's pass) — CLOSED S121 (Ryan: not pursuing)
- **E19** — Move Configured/Remaining points next to Army Points in the banner — SHIPPED S119 (D188)
- **E13** — Drop "Keep" prefix from default swap-option labels — CLOSED S84 (D151)
- **E18** — JSON export / import (list portability + data-loss recovery) — DONE (Session 27, D82).
- **B16** — Per-model-group default weapons (weapon-count fix) — DONE (Session 23, D78).** Fixed in equipped_parser.py via a Datasheets.csv loadout-column gap-filler; 19 units repartitioned, 0 regressions.
- **B22** — "1 model's X can be replaced" is parsed as a per-5-models allowance (parser + data) — CLOSED (D94, S39)
- **B23** — compound "A and B can be replaced with C" — `count` family CLOSED (D95, S40)
- **B23b** — compound source on a `choice` option (engine + parser) — CLOSED (engine D97/v5.54 S42; parser D98 S43)
- **B26** — per-N "up to N models can each have their X replaced with Y" — CLOSED (D96, S41)
- **B20** — CLOSED (engine half D93/v5.53; parser half D94/S39)
- **B24** — profile-pinned `replaces` / `replacement` — CLOSED (D95, S40)
- **B27** — Whirlwind's `default_weapons` contain weapons the unit does not have — CLOSED (D96, S41)
- **B25** — two `choice` options in one single-model group replace the same weapon (engine/UI) — CLOSED (D97, v5.54, S42)
- **None** — ### B23b (parser half) — stop reducing a compound source — **CLOSED (D98, S43)
- **B30** — the replacement side of a `single` swap isn't split on " and " — CLOSED S45 (D100)
- **B31** — an "A or B and C" source — CLOSED S99 (D165); DATA; `bundled_swaps.json` + `units.json`
- **B28** — a swap whose source is a wargear *item*, not a weapon — CLOSED (D101 engine S46, D102 data S47; header corrected S92)
- **B29** — "Additional Combi-Bolter" isn't normalised to a weapon — CLOSED (D98, S43)
- **P1** — `loadout_parser.py` stale-copy failure — CLOSED S57 (D118)

## Cross-cutting notes

- **Combinatorial-swap cluster** (B5, B6, plus the banked Devastator Sergeant
  "pick two"): all need one shared design decision on the control model —
  mutually-exclusive option *sections* where picking one atomic multi-weapon swap
  locks the others. Design this once, apply to all three.
- **Leader-system cluster** (originally B7 multi-leader, E9 Warlord, plus the banked attached-unit
  combined popup): substantially shipped. B38 cluster (D144–D147) shipped the multi-leader mechanic;
  E9 shipped (D139/D140); B7 closed S89 (D157) with residuals reshaped into B7a and B7b. B7a (stack
  cap engine refinement) shipped S90 (D158). B7b (combined popup with aura markers) closed S91 (D159).
  The cluster is fully shipped. *(This note said B7b was still open until S124; it had been closed for
  thirty-odd sessions — the exact drift D107 warns about, in the document meant to track what is open.)*
- **Detachment cluster** (E1a→E1b→E1c, then E4 and E21; E5's "Remaining" total feeds off the same
  points math): scoped S122 (D192), authoritative write-up in `E1_DETACHMENT_SCOPE.md`. Build order
  is fixed and not open for re-litigation — E1a is a data-only turn, E1b and E1c are engine-only
  turns, and they cannot be merged without breaking the never-mix rule. The new pipeline path is
  MFM-first (11th Ed, authoritative on DP and points) with the 10th-Ed Wahapedia dump joined in for
  description text only. E21 (require/forbid, unit unlocks, Battleline elevation) is deliberately
  downstream of E1c, not part of it.
- **Sequencing intuition** (for discussion, not committed): B1 first (credibility —
  wrong rule text is worse than a missing feature), then the quick UI wins
  (E3, E7, E2, E5), then the detachment foundation (E1→E4→E6), with the
  combinatorial-swap and leader-system clusters slotted per your priority.
