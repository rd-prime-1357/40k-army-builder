# Drukhari — Build Scope

Scoping-only pass (S222). No committed file changed. All numbers below come from command output
against this session's own baseline open (34 gates, sources loaded via `--fetch --data-turn`,
122/122 assertions, all three repro checks byte-identical, `repo_check` clean). Dry-run transforms
and parser runs were written only to throwaway temp dirs; nothing under `units.json`,
`unit_loadouts.json`, `detachments.json`, or any parser was edited.

Drukhari's roster is clean and small (23 current-edition units) and every points/threshold shape
it uses is already handled by the existing parsers, proven by direct dry-run execution, not read
of the code. The real finding this session is not in the roster — it's a cross-faction allied-unit
mechanic (Harlequins/Anhrathe) that has no precedent in any built faction and surfaces a genuine
transform bug along the way. See §2 and §6.

---

## 1. Roster size: 23 units, matches exactly, 7 Legends exclusions confirmed both ways

`Datasheets.csv` holds 23 rows for `faction_id == DRU` and `source_id == 000000031` (the current
10th-edition Drukhari Faction Pack); `MFM_Drukhari_v1.1.txt` lists exactly 23 units under its main
`UNITS` header. Checked both directions by name — every MFM unit has a datasheet, every datasheet
has an MFM entry.

7 more `DRU`/`source_id == 000000384` ("Drukhari (Warhammer Legends)") rows exist — Beastmaster,
Court of the Archon, Grotesques, Raven Strike Fighter, Reaper, Tantalus, Urien Rakarth — and these
match, name for name, the 7 units under the MFM file's own `LEGENDS` header. Correctly excluded by
`wahapedia_transform.py`'s existing Legends/Forge-World filter (`source_is_excluded`, keyed on
edition ≠ "10" or "legend"/"forge world" in the source name).

Zero `SUPPORT` units — Drukhari has no Support-slot/co-leader shape at all, simpler than every
Space-Marine-descended faction built so far. 6 `LEADER` units in the 23 (Archon, Drazhar,
Haemonculus, Lady Malys, Lelith Hesperax, Succubus); a 7th LEADER (Urien Rakarth) is Legends-only
and out of the base build.

## 2. A real transform bug, found by running the pipeline, not by reading it — DO NOT run
`--faction DRU` unfixed

`wahapedia_transform.py --faction DRU` (dry run, scratch dir) selects **37 datasheets, not 23**.
The extra 14 are Harlequins and Aeldari Corsair units (Death Jester, Shadowseer, Solitaire, Troupe
Master, Starweaver, Skyweavers, Troupe, Voidweaver, Corsair Voidreavers, Corsair Voidscarred,
Corsair Skyreavers, Kharseth, Prince Yriel, Starfangs) — Wahapedia tags them `faction_id == DRU`
(a legacy holdover) but their real `source_id` is `000000186`, the **Aeldari** Faction Pack
(current-edition, 10th, not Legends). The existing filter only excludes non-current/Legends
sources; it has no faction-of-origin check, so it waves these 14 through. This is the first faction
where that gap actually fires — no prior built faction shares a Wahapedia faction_id tag with units
sourced from a different current-edition faction pack.

Independent confirmation, not just filter-reading: a dry `mfm_points_parser.py` run against
`MFM_Drukhari_v1.1.txt` reports these same 14 datasheets under "Datasheets with NO MFM points" —
they don't appear anywhere in the Drukhari MFM file (checked directly: zero Harlequin/Corsair names
in its `UNITS`, `DETACHMENTS`, or `LEGENDS` blocks), because they're priced from `Codex: Aeldari`,
not this file.

**This is not noise to filter and forget — it's real game content.** See §6. The units build must
not run `wahapedia_transform.py --faction DRU` until this is resolved; doing so today would ship a
37-unit roster with 14 mis-costed, mis-sourced entries. Fixing the filter (exclude `source_id`
`000000186` specifically, or add a "target faction's own source only" check generally) is a small,
contained tooling fix — recommend doing it as its own XS tooling turn immediately before the
Drukhari units data turn, not folded into it.

## 3. Leader/attachment mapping — one target correctly drops, nothing to fix

|Leader|Attaches to|
|---|---|
|Archon|Court of the Archon (Legends — see below), Hand of the Archon, Incubi, Kabalite Warriors|
|Drazhar|Incubi|
|Haemonculus|Wracks|
|Lady Malys|Hand of the Archon, Incubi, Kabalite Warriors|
|Lelith Hesperax|Wyches|
|Succubus|Wyches|
|*(Legends)* Urien Rakarth|Wracks|

Archon's attach list names Court of the Archon, which is Legends-only and absent from the
23-unit build. Confirmed this is already a solved case, not a gap: a dry `mfm_points_parser.py`
run reports it under "MFM attach-list entries with NO matching datasheet (dropped)" — an existing
guard (B73/D260) already strips attach-list entries with no matching datasheet rather than shipping
a dangling reference. Archon will build with a 3-target list (Hand of the Archon, Incubi, Kabalite
Warriors); Court of the Archon drops silently and correctly, as designed. No new engine work.

"Attach eligibility overridden from MFM (B73): 6 (6 Leader, 0 Support)" in the same dry run — one
override per Leader unit, expected, not an anomaly.

## 4. Points/threshold shapes — all precedented, proven by direct parse, not assumed

Comparing `MFM_Drukhari_v1_0.txt` and `MFM_Drukhari_v1.1.txt` directly, exactly 3 units changed:

- **Raider**: flat 85 pts (v1_0) → tiered in v1.1, `1ST TO 3RD` 75 pts (▼-10) / `4TH+` 85 pts
  (unmarked, same as old flat price) — a **new threshold added**, in the `1st-to-3rd/4th+` shape
  (not the more common `1st-to-2nd/3rd+` shape used elsewhere in this same file for Hellions,
  Incubi, Mandrakes, Reavers, Scourges, Talos).
- **Ravager**: tiered in v1_0 (`1ST TO 2ND` 100 / `3RD+` 110) → flat 110 pts (▲+10) in v1.1,
  explicitly tagged `UPDATED` / `REQUISITION THRESHOLDS REMOVED` — a **threshold removed**. Also
  gains a `WARGEAR OPTIONS` line (per Dark lance, 5 pts) not present in v1_0.
- **Venom**: flat 70 pts (v1_0) → tiered in v1.1, `1ST TO 3RD` 65 pts (▼-5) / `4TH+` 75 pts — same
  **new-threshold** shape as Raider.

The `1st-to-3rd/4th+` shape is not new to the project — it's the exact shape B87 added an `esc4`
reader for (Rubric Marines, fixed as a shipped-bug correction). Rather than trust that read, I ran
`mfm_points_parser.py --mfm MFM_Drukhari_v1.1.txt` directly: Raider parsed as 75/75/75 then 85 pts
at copy 4; Venom as 65/65/65 then 75 pts at copy 4; Ravager as a flat 110 across all three
copy-tiers. All three correct, no parser change needed.

A `--wargear` harvest pass against the same file correctly found all 4 wargear-cost items in the
file (Ravager's Dark lance +5; Scourges with Heavy Weapons' Haywire blaster +5 and Dark lance +5;
Talos's Twin haywire blaster +5) — ordinary "per weapon" wargear pricing, already generically
handled.

No Requisition Threshold or wargear point-scaling shape in this file is new. The prompt's caution
against assuming Drukhari mirrors any prior faction was right to give — Raider and Venom's tier
boundary is genuinely different from the rest of the file's own units — but the shape itself is
already-built engine capability, confirmed by running it, not inferred.

## 5. Detachments — 9, DP 1–3, three shared Unique tags (precedented), 30 enhancements, 3
force-disposition changes

Both `MFM_Drukhari_v1_0.txt` and `MFM_Drukhari_v1.1.txt` list the same 9 detachments, same names,
same DP costs:

|Detachment|DP|Force Disposition (v1.1)|Unique tag|Enhancements|
|---|---|---|---|---|
|Covenite Coterie|2|Take and Hold *(changed from Purge the Foe — `UPDATED`)*|COVENS|4|
|Exhibition of Slaughter|1|Reconnaissance *(changed from Disruption — `UPDATED`)*|WYCH CULT|2|
|Kabalite Agonysts|1|Disruption *(changed from Purge the Foe — `UPDATED`)*|KABAL|2|
|Kabalite Cartel|2|Disruption|KABAL|4|
|Realspace Raiders|2|Priority Assets|—|4|
|Reaper's Wager|3|Purge the Foe|—|4|
|Skysplinter Assault|2|Reconnaissance|—|4|
|Spectacle of Spite|2|Purge the Foe|WYCH CULT|4|
|Tools of Torment|1|Take and Hold|COVENS|2|

DP range 1–3. Enhancement total: 30. Three detachments changed Force Disposition between v1_0 and
v1.1 (each explicitly tagged `UPDATED` / `FORCE DISPOSITION(S) CHANGED` in the source, not inferred
from a diff); DP costs and enhancement point values otherwise unchanged version to version.

**Three Unique tags are each shared by two detachments** (COVENS: Covenite Coterie + Tools of
Torment; WYCH CULT: Exhibition of Slaughter + Spectacle of Spite; KABAL: Kabalite Agonysts +
Kabalite Cartel) — meaning within each pair, only one of the two can be taken in the same army.
Checked directly against `detachments.json`: this exact shared-tag-across-multiple-detachments
pattern already exists and is already enforced for Blood Angels (GRACE, DOOMED), Death Guard
(FLYBLOWN, ENGINES), Chaos Space Marines (NIGHTMARE), and Thousand Sons (MUTANT) —
`rules_assertions.py`'s `e1a_no_duplicate_names_and_unique_tags` and the live
`uniqueTagConflicts` engine state already handle it faction-agnostically. **Not a new mechanism.**

**Enhancement name collisions across detachments, same faction**: "Towering Arrogance" appears in
both Kabalite Agonysts (15 pts) and Kabalite Cartel (20 pts); "Periapt of Torments" appears in both
Exhibition of Slaughter (20 pts) and Spectacle of Spite (25 pts). Enhancements key off
detachment+name, not name alone, so this is a non-issue mechanically — flagged only so it isn't
mistaken for a data error when the detachments build runs.

One enhancement — Tools of Torment's "Elixir of the Corpse Courts (Upgrade)" — carries the
`(Upgrade)` suffix. Also not new: `detachment_parser.py` already strips and flags this suffix
(`is_upgrade` field), with 47 such enhancements already shipped across built factions.

**Three of the 9 detachments have no Wahapedia rule text at all**: Exhibition of Slaughter,
Kabalite Agonysts, and Tools of Torment appear nowhere in `Detachment_abilities.csv` or
`Detachments.csv` — no fluff, no rule name, no ability text, for either version. No GW Faction Pack
text source exists for Drukhari in the project area either (only Dark Angels and Space Marines
faction-pack `.md` files are present). These three will ship with `text_source: "none"`, matching
the 25 already-precedented instances of this gap across built factions (see `detachments.json`
meta). Not a blocker, just a known-shape gap.

`B113` (LEADER: enhancement-eligibility lines silently dropped) gains **zero new instances** —
confirmed by direct text search of the Drukhari `DETACHMENTS` block, same as Grey Knights and
Chaos Daemons before it.

## 6. Cross-faction allied-unit inclusion — a genuinely new mechanic, needs a product decision

This is the substantive finding this session, and it's why the 14 "extra" datasheets in §2 exist.

Drukhari carries an army-wide rule, **"Corsairs and Travelling Players"** (`Abilities.csv`,
DRU-scoped, not tied to any detachment): if your Army Faction is Drukhari, you can include
Harlequins and Anhrathe (Corsair) units up to a combined points cap that scales with battle size
(250 / 500 / 750 pts for Incursion / Strike Force / Onslaught). Units included this way cannot be
Warlord and cannot take Enhancements.

Separately, the **Reaper's Wager** detachment's own ability, "Callous Competition," grants a
**larger, detachment-specific version of the same allowance**: full Harlequins inclusion (not
Anhrathe) at double the base caps (500 / 1000 / 1500 pts), with a Warlord restriction but no stated
Enhancement restriction, and an explicit note that selecting this detachment means you **cannot**
use the base Corsairs and Travelling Players rule — the two are mutually exclusive per detachment
choice, not additive.

The 14 datasheets flagged as a "bug" in §2 are exactly the Harlequins and Anhrathe/Corsair units
these two rules make legal to include. This isn't noise — it's the real mechanic. But building it
properly means pricing these 14 units from `Codex: Aeldari`'s own points (a different MFM file,
`MFM_Aeldari_v1_0.txt`, present in the project area but never scoped or built), tracking a
points-cap-by-battle-size that varies by which rule/detachment is active, and enforcing the mutual
exclusion and Warlord/Enhancement restrictions. Aeldari is not in the faction priority order at
all, and has no roster, detachments, or loadouts built.

This is the same *family* of pattern as the existing Chaos Daemons → Shadow Legion (unlocks CSM
units) and the Legions of Excess / Scintillating Legions / Plague Legions pattern on Emperor's
Children / Thousand Sons / Death Guard — but those all price the allied units **inline in the
host faction's own MFM file**, with no points cap and no battle-size scaling. Drukhari's version
sources from a *different, unbuilt* faction's MFM, with a cap that varies by battle size and by
which detachment/rule is active. No built faction has this shape yet.

**Recommendation** (mine to make on the tooling/sequencing side, but the underlying "does the tool
support cross-book allied inclusion, and if so when" question sets real precedent, so it's flagged
below for your call): ship Drukhari's own 23-unit / 9-detachment build first, without the
Harlequins/Anhrathe allowance. This under-represents legal army options (a player can't yet build
the small Harlequins/Corsair contingent Drukhari armies are entitled to) but does not let anyone
build an illegal one — D0 is about unreachable illegal states, not about completeness of legal
ones, so this is a safe thing to defer. Open a follow-on ticket for the allied-inclusion mechanic
itself, to be picked up if/when Aeldari is prioritized.

## 7. Loadouts — bounded manual-authoring load, isolated from the transform bug

The dry-run transform's "not auto-parsed" flags include both true-Drukhari and contaminating
Harlequin/Corsair entries (§2); separated out, the true Drukhari-only manual-authoring load across
the 23-unit roster is:

- **13 wargear-option groups** across 9 units needing manual construction: Wracks (2 groups), Hand
  of the Archon (2 groups), Hellions (2 groups), Talos (2 groups), Razorwing Jetfighter, Voidraven
  Bomber, Scourges with Heavy Weapons, Ravager, Scourges with Shardcarbines (1 group each).
- **8 compound replacements** ("X and Y" swaps), all within the same 9 units above.
- **1 bundled two-weapon swap** (Wyches).
- **4 ambiguous weapon-name matches** needing a manual pick: Incubi (demiklaives, single vs. dual
  blade), Wracks ×2 (tools vs. twin tools), Voidraven Bomber (missile variant).
- **1 equip/add item with no weapon profile**: Voidraven Bomber's Voidraven missiles (wargear item,
  not a weapon profile).
- **1 multi-model-line unit needing a split review**: Incubi (2 model lines).

This is on the same order as Grey Knights (4 flagged units) and smaller factions before it — bounded,
ordinary loadout-authoring work for the tooling turn, not an engine gap.

## 8. Suggested sequencing

1. **XS tooling turn**: fix `wahapedia_transform.py`'s faction-selection filter so `--faction DRU`
   excludes `source_id 000000186` (or generalize to "a source belonging to a different faction's
   current-edition pack"), and re-verify the dry run drops to exactly 23. Small, contained, blocks
   everything else in this list.
2. **Data turn**: run the (now-fixed) transform, `mfm_points_parser.py`, and register Drukhari in
   `detachment_parser.py`'s three maps; build `units.json` for the 23-unit roster.
3. **Tooling turn**: author the 13 flagged wargear-option groups per §7.
4. **Data turn**: build `detachments.json` for the 9 detachments per §5.
5. **Separate, later ticket**: the Harlequins/Anhrathe allied-inclusion mechanic (§6), gated on
   Ryan's call on whether/when to build it, and on Aeldari's own scoping if so.

## Decisions needed

1. **§6 — Harlequins/Anhrathe allied-unit inclusion.** Recommend deferring past the initial
   Drukhari build (ship without it, open a follow-on ticket) rather than blocking Drukhari on
   Aeldari being scoped and built first. This sets precedent for how the tool handles cross-book
   allied inclusion generally, so flagging rather than deciding unilaterally. No urgency — nothing
   currently blocks on this, and it doesn't risk an illegal-state gap either way.
