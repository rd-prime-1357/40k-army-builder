# E1 — Detachment Selection System: Scope

**Session 122. Analysis only — no code or data shipped this session.**
**S123 corrections applied in place, marked inline. E1a is built; D193 is authoritative where the two differ.**
Supersedes the one-paragraph E1 sketch in `OPEN_ITEMS_BACKLOG.md`. Decisions recorded as **D192**.

---

## 1. What the rules require

`Army_Muster_Rules.txt` 25.03 / 25.04:

- Battle size sets a Detachment Point budget: **Incursion (1,000 pts) = 2 DP; Strike Force (2,000 pts) = 3 DP.**
- You may select any combination of detachments whose combined DP does not exceed the budget.
- You may **not** select the same detachment twice.
- You may only select detachments available to your army faction.
- Each detachment grants a force disposition, a detachment rule, enhancements, and stratagems.
- Some detachment rules **require or forbid** specific units or other detachments; the army must obey them.
- Enhancements come only from selected detachments (that is E4, and it sits directly on this).

There is no 3,000-point row in the rules table.

---

## 2. Where the data actually is — the central finding

**The Wahapedia CSV dump is 10th Edition** (`Factions.csv` links read `wh40k10ed`; every `Source.csv` row is
edition `10`; `Last_update.csv` = 2026-06-13). **The MFM faction files are 11th Edition v1.0.** They disagree,
and the disagreement is not cosmetic.

Each `MFM_<Faction>_v1_0.txt` carries a `DETACHMENTS` section giving, per detachment: **name, DP cost, force
disposition, and the full enhancement list with current points and `(Upgrade)` tags.**

*(S123: and a fourth field this pass missed — a `UNIQUE:` tag. `MFM_Instructions.txt` defines it:
no two selected detachments may share a Unique tag. A third selection constraint, live in Blood
Angels and Death Guard data today. Shipped as `unique_tag` in E1a; enforcement is E1e.)* That is the authoritative
11th-Edition source and it is already in the project.

Across the eight MFM files covering the fourteen built army blocks: **143 detachments, ~~513~~ 515 enhancements,
35 of them `(Upgrade)`-tagged.** *(S123: the enhancement figure was wrong. Librarius Conclave has
five, not four, in all five armies that get it; The Living Miracle and Lords of the Warp have one
each. 143, 35 and the disposition split all reproduced exactly.)* Force dispositions are complete — every detachment has exactly one of
PRIORITY ASSETS (33), TAKE AND HOLD (39), PURGE THE FOE (27), DISRUPTION (24), RECONNAISSANCE (20).

DP costs per faction:

| Army block | Detachments | 1 DP | 2 DP | 3 DP |
|---|---|---|---|---|
| Space Marines (and the six codex chapters) | 22 | 3 | 14 | 5 |
| Black Templars | 19 | 5 | 10 | 4 |
| Blood Angels | 23 | 6 | 11 | 6 |
| Dark Angels | 23 | 6 | 12 | 5 |
| Deathwatch | 16 | 3 | 9 | 4 |
| Space Wolves | 22 | 6 | 12 | 4 |
| Chaos Daemons | 9 | 3 | 5 | 1 |
| Death Guard | 9 | 3 | 5 | 1 |

### Rule text: a three-tier source ladder

**Corrected within Session 122.** An earlier pass in this session concluded that no 11th-Edition
rule text existed for the new 1 DP detachments. That was wrong, and wrong in exactly the way this
project's own standing principle warns about — absence from the files I happened to grep is not
absence from the sources we hold. Two held sources carry current 11th-Edition detachment content
and were missed:

- **`chaos_daemons_reference.md`** — a condensed faction-pack digest already established as a text
  source in this project (D-entries have sourced ability text from it before). Its `DETACHMENTS
  SUMMARY` section covers **all 9 Chaos Daemons detachments**, each with detachment rule,
  enhancements (Upgrade tags included) and the full stratagem list. Clean structured prose, no
  parsing problem. Chaos Daemons is at **100% 11th-Edition coverage**, including all three 1 DP
  detachments.
- **`Space_Marines_Faction_Pack_v1_0.md`** — carries **15 full detachment pages** (rule,
  enhancements, stratagems) for the Space Marines detachments introduced in 11th Edition, including
  both 1 DP entries, Fulguris Task Force and Subversion Assets. Its two-column PDF-to-text
  interleaving is a formatting problem, not a coverage problem, but see the note on extraction
  quality below.
- **`Dark_Angels_Faction_Pack_June_2026.md`** — added by Ryan during S122. Covers **5 Dark Angels
  detachments**: Dark Age Arsenal, Darkflight Pursuit and Interrogation Conclave (all three of Dark
  Angels' no-text gaps) plus Lion's Blade Task Force and Wrath of the Rock, which move from
  previous-edition text to current. All 14 MFM enhancement names are present, along with 15
  stratagem blocks.

**Extraction quality matters more than expected.** The Dark Angels pack is **single-column and
linear** — no interleaving, consistent `# Page N` markers, and section labels (`DETACHMENT RULES`,
`ENHANCEMENTS`, `Restrictions:`, and stratagems as name / CP / `<DETACHMENT> STRATAGEM` / WHEN /
TARGET / EFFECT) that parse directly. The Space Marines pack is the same underlying document type
extracted badly. **If the SM pack is re-extracted the way the DA pack was, the column-splitter comes
out of E1a entirely** and one parser handles every faction pack. Worth asking for before building.

**A bonus for E21.** The DA pack marks army-construction restrictions with a literal `Restrictions:`
label (3 instances) rather than burying them in prose, and its `RULES UPDATES` section contains a
live Battleline-elevation case — Company of Hunters changing Outrider Squad to gain the BATTLELINE
keyword, which moves that unit's count cap. Both are far more tractable than the free prose in the
Wahapedia dump, and they raise the odds that E21 is parseable rather than hand-curated.

**Source precedence for rule and enhancement text, highest first:**

1. `chaos_daemons_reference.md` / `Space_Marines_Faction_Pack_v1_0.md` — current edition.
2. Wahapedia `Detachment_abilities.csv` / `Enhancements.csv` / `Stratagems.csv` — 10th Edition,
   used only where no tier-1 text exists. Where the faction pack carries errata for a
   Wahapedia-sourced detachment, the errata is applied on top.
3. Nothing — render name, DP, disposition and enhancement names and points, with no body text.

This is separate from and subordinate to the numbers rule: **MFM always wins on DP, points, and
which enhancements exist**, regardless of which tier supplied the prose.

### Corrected coverage

| Army block | Current text | Previous-edition | No text |
|---|---|---|---|
| Space Marines | 15 | 7 | 0 |
| Black Templars | 7 | 10 | 2 |
| Blood Angels | 8 | 12 | 3 |
| Dark Angels | 13 | 10 | 0 |
| Deathwatch | 8 | 8 | 0 |
| Space Wolves | 8 | 12 | 2 |
| Chaos Daemons | 9 | 0 | 0 |
| Death Guard | 0 | 7 | 2 |
| **Total** | **68** | **66** | **9** |

Wahapedia still matches 116 of 143 by name, but it is now the *fallback* rather than the primary,
and the no-text gap is **9 detachments**, down from the 27 the first pass claimed and from 12 before
the Dark Angels pack arrived. All nine are 1 DP and sit in the four army blocks with no digest held:
Black Templars (Marshal's Household, The Living Miracle), Blood Angels (Encarmine Speartip, Legacy
of Grace, Wrath of the Doomed), Space Wolves (Legends of Saga and Song, Veterans of the Fang), Death
Guard (Contagion Engines, Paragons of Putrescence).

**The remedy is an input, not a build.** the Dark Angels pack shows the shape that works.
Equivalent packs for **Black Templars, Blood Angels, Space Wolves and Death Guard** would take the
gap to zero and would also upgrade a further 41 detachments from previous-edition text to current.
That is a question for Ryan, not something to engineer around.

### Enhancement text and drift

Where Wahapedia does supply enhancement descriptions, the sets have still drifted in 11 of the 116
matched detachments: Librarius Conclave gained *Temporal Corridor* and re-priced four enhancements
(Celerity 30→35, Fusillade 35→20, Obfuscation 20→25, Prescience 25→20); Champions of Fenris, Saga of
the Great Wolf, Wrathful Procession, Daemonic Incursion and Flyblown Host all differ. Roughly 20
further differences are naming only — Wahapedia suffixes `(Aura)`, MFM appends `(Upgrade)`.

**Engineering rule (not a Ryan call):** MFM is the source of record for which detachments and
enhancements exist, their DP, their points and their Upgrade status. Text sources contribute
descriptions only, joined on a normalised name with parentheticals stripped. Enhancements present
in a text source but absent from MFM are **dropped, not displayed** — they are stale leftovers, and
showing them would put phantom options at wrong prices in front of the player. The `(Upgrade)` tag
is rules-significant under 25.04 and survives the join as a boolean flag.

### Source ruled out

`*_web.txt` — its `DETACHMENT ABILITY` strings are stray headings inside a unit dump, with no rule
bodies. Not a source.

---

## 3. Faction mapping

Fourteen built army blocks, eight MFM detachment files. The six Codex: Space Marines chapters without their
own MFM file — **Ultramarines, Iron Hands, Imperial Fists, Raven Guard, Salamanders, White Scars** — take the
generic Space Marines list of 22. That list already contains their chapter-flavoured detachments (Blade of
Ultramar, Hammer of Avernii, Emperor's Shield, Forgefather's Seekers, Headhunter Task Force, Stormlance Task
Force) with no restriction language attached in any source we hold. Under D0's undetermined-legality default,
all 22 are offered to all six. The chapter restrictions that do exist in the SM Faction Pack are about which
*units* an army may include, not which detachments.

---

## 4. Ticket split

E1 becomes a parent with three build children plus one new downstream ticket.

### E1a — data turn (build first)

New `detachment_parser.py` producing new `detachments.json`, keyed by the fourteen app army names.
Per detachment: name, DP, force disposition, source faction, `text_source` (`faction_pack` /
`wahapedia_10e` / `none`), enhancement list (name, points, is_upgrade, description-or-null), rule
text-or-null, stratagem list-or-empty. MFM parsed for structure and points; text joined per the
three-tier ladder in §2. The Dark Angels pack parses directly. The Space Marines pack needs a
column-splitter unless it is re-extracted first — that is the only non-trivial parsing in the
ticket, and it disappears if a clean re-extraction arrives.

Pipeline integration is part of this ticket, not an afterthought: add `detachment_parser.py` and
`detachments.json` to `pipeline_manifest.json`, and add a `detachments_repro_check.py` byte-identical gate
alongside the two existing ones. New assertions in `rules_assertions.py` (D107 — a prose claim is not a fact):
every DP in 1–3; every detachment carries exactly one of the five dispositions; no duplicate detachment name
within a faction; total counts match the table in §2; no Wahapedia-only enhancement survives the join;
`(Upgrade)` tags are preserved as flags; and `text_source` is one of the three permitted values with
the per-tier counts are recorded in the generated file and reproduce on re-run. Do **not** hard-code
the per-tier totals in the assertion — they move every time a faction pack arrives, and an assertion
that has to be edited on every input change is an assertion that will be edited wrongly. Assert the
invariant (every detachment carries exactly one valid `text_source`, and every `none` is listed in a
named gap manifest), not the arithmetic.

**Data-only turn.** No engine changes.

### E1b — engine turn: state and persistence

`selectedDetachments` in app state. `SCHEMA_VERSION` 1 → 2 with a migration that reads a v1 record as an empty
detachment set (the migration hook at `list_store.js` is already stubbed for exactly this). Export/import
carry the field. `detachmentPointBudget(POINTS_CAP)` returns 2 at ≤1,000 and 3 above. A `dpState()` helper
mirroring `limitState()` returning ok / at / over.

### E1c — engine turn: UI

Left-panel detachment section, pinned above the role groups, collapsible on E2's existing pattern, with a
`DP 2 / 3` counter in its header. Each detachment is a checkbox row showing name, DP and disposition; a row
whose DP would breach the budget is disabled, matching how the roster disables a unit at its limit. Selected
detachments render in the centre army list. An info control on each opens rule text, enhancements and
stratagems as collapsible detail, reusing the Rules-style drop-down and B47's info-button pattern.

### E21 — NEW: detachment-driven army-construction effects

Detachment rules that require or forbid units, unlock units from other factions, or elevate units to
Battleline (which moves the count cap). These are real and they bite on day one for a built faction: Chaos
Daemons' *Shadow Legion* forbids Daemon Prince and Epic Hero units while unlocking a list of Heretic Astartes
units. 34 detachment abilities across the full dump carry require/forbid language, in free prose with no
common shape. Gated on E1c. Explicitly **not** in E1.

### E4 — unblocked once E1c lands

The seam is already clean: enhancements arrive inside the detachment record with points and Upgrade flag, so
E4 is an assignment UI plus a per-unit enhancement field and the 25.04 limit rules — not a second data build.

---

## 5. Decisions

**Recorded as D192. Items 2–5 are proceeding on the recommendation; item 1 is Ryan's.**

**1. Rule-text sourcing — one question for Ryan, and it is now about inputs rather than display.**
With the three-tier ladder in §2, 63 detachments have current 11th-Edition text, 68 fall back to
10th-Edition Wahapedia text, and 9 have none. The display question largely answers itself: show
tier-1 and tier-2 text, and mark only the tier-2 items as sourced from the previous edition, since
that marking is now a per-item fact the parser knows rather than a blanket disclaimer over
everything. E1a emits a `text_source` field per detachment so the UI can do this without guessing.

**The real question: faction packs for Black Templars, Blood Angels, Space Wolves and Death Guard,
plus a re-extraction of the Space Marines pack in the Dark Angels pack's single-column form.** The
first takes the no-text gap to zero and upgrades 41 more detachments to current text; the second
removes the column-splitter from E1a entirely. Nothing blocks on either — E1a ships with whatever
sources are present, and adding a pack later is a parser re-run, not a redesign.

**2. DP at 3,000 points.** The rules define no 3,000-point battle size. Treat 3,000 as Strike Force, 3 DP —
identical to how `battleSizeUnitLimit` already treats it.

**3. Enforcement mechanism.** Hard-block a selection that would exceed the DP budget, and make duplicate
selection structurally impossible via the checkbox list. Mirrors the most recent precedent (D114/D115 unit
limits), not the older flag-and-warn line. An over-budget state stays reachable from an imported or
battle-size-switched list and stays visible as an error there.

**4. Known unenforced rule at E1 ship.** Between E1c and E21 the app will know about detachments without
enforcing their require/forbid restrictions. Recorded openly rather than left as a silent gap; consistent
with D0's undetermined-legality default of leaning permissive.

**5. UI placement.** Left panel, pinned above the role groups; DP counter in the section header rather than
the banner, which E19 already filled.
