# Next-session prompt — Session 136

Session 135 shipped **E21b** (**D212**): `effectiveUnitType()` is live in `index.html` at **6.6**,
feeding `unitLimit()`, `groupByType` and the roster's `typeGroups` build; chapter exclusivity is
policed by **E21b-1**, read from `Datasheets_keywords.csv` rather than from block membership.
Assertions **97/97**, baseline **22/22**. Read `SESSION_HANDOFF_135.md` **including its addendum**, then **D212** and **D213**, then **D204**
(rulings 1 and 3, which govern this session's work) and **D208** (B61's `allied_group` tag).

## Turn type

**Engine-only.** `index.html` only, plus harnesses and assertions. No parser, no converter, no data
file, no JSON regeneration. `detachment_effects.json` is a hand-authored **input** — never edit it to
make the engine pass.

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline) — **22 gates now**, including `e21b_check`. Verify the
S135 hashes in `SESSION_HANDOFF_135.md`'s Files section before trusting the sync.
`detachment_effects.json` is unchanged from S134 and its hash is still `e38c38dcef31`.

## The task: E21c with E22b — the remaining three effect kinds

Both read the same table and both land on the add path, which is why D204 put them in one session.
`forbid`, `unlock` and `warlord` are all still unread by the engine; E21b touched only `battleline`.

**1. `forbid` — Chaos Daemons | SHADOW LEGION.** The army cannot include any Daemon Prince, Daemon
Prince with Wings or Epic Hero, excluding Be'Lakor. The table expresses this as
`unit_types: ["Epic Hero"]` with `except_units: ["Be'Lakor"]` plus the two Daemon Princes named
explicitly — they are `unit_type: Character`, not Epic Hero, so a type rule alone misses them (D209).
D0 applies: the add is **refused**, not flagged. Refusal must also cover a unit already in the list
when the detachment is later selected — that is a reachable state and it needs a defined answer.

**2. `unlock` + points sub-cap — Death Guard | TALLYBAND SUMMONERS.** This closes the **live D0
violation** D204 found: the six Plague Legions units are currently in the Death Guard pool with no
gate at all. Without this detachment selected they must not be offered. With it, they are offered
bounded by the points cap keyed by battle size (500 / 1000 / 1500 against 1000 / 2000 / 3000). B61
already tagged the six with `allied_group`; consume that tag, do not re-derive the list.

**3. `warlord`** — `cannot_be` for the Plague Legions group under Tallyband Summoners. Be'Lakor needs
no row: his unit-level `must_be_warlord` is unconditional and strictly stronger (E21a-6 pins this).

Add `e21c_check.js` covering all three kinds, in the mould of `e21b_check.js` — including the
already-in-list case for `forbid` and the sub-cap arithmetic at both battle sizes. Register it in
`baseline.sh` and in the manifest's guarded set (40 → 41).

**Expect the same slice breakage E21b hit.** Any harness that slices the add path out of `index.html`
will need the new block pulled in alongside it. Repair the slice; do not loosen the check.

## Ground rules

* Engine-only. `index.html`, harnesses, assertions. No data file touched.
* Do not rename anything — project name still unsettled.
* Refusals need a reason string. E4b's `canAssignEnhancement` refusal-reason shape is the precedent
  and `enhancementRefusalText` is the model; prose polish is E21d's, but a mute refusal is a bug.

## After E21c/E22b

* **S137 — UI-only.** E21d: refusal prose, roster warnings, Battleline indicator. E21 closes there.
* **E23** — scoping turn, unsequenced. Headhunter Task Force's Tank Ace → Character grant. A fifth
  effect kind (muster-time keyword grant, count-limited, player-chosen recipients), so it is player
  state rather than a static table row, and it lands on E4's enhancement eligibility and E9's Warlord
  eligibility. Over-restriction, not a D0 violation.
* **B62** — the `FALSE` string-literal quirk and the missing presence-and-parse assertion over the
  nine CD CSVs. Open and untouched since D205.
* **S138 — data-only.** P4 step 2. Decision rule fixed in advance in D213: ~0.6 points means step 3
  minifies `units.json` and `detachments.json`; no movement means step 3 is cancelled.

## Standing inputs

* **P4 step 1 is DONE (D213).** `BACKLOG_ARCHIVE.md` removed after park-and-rerun verification;
  **94% → 92%** on 174 KB, so the capacity metric responds to volume at roughly 123 KB of prose per
  displayed point. **Do not extrapolate that to the 797 KB of JSON whitespace** — prose and long runs
  of identical spaces do not tokenise alike. **P4 step 2** (minify `unit_loadouts.json` alone, 77 KB,
  then read the percentage) is a **data turn** and is sequenced after this session, not into it.
* **A local backup folder** for the GW-derived files — the nine Chaos Daemons CSVs, the Wahapedia
  export, the MFM `.txt` files, the faction web and pack files. The repo cannot hold them; S131 lost
  three and rebuilt them only because `units.json` happened to carry enough. `wh40k_core_rules.md`
  (139 KB) is opened by nothing and is the obvious first tenant.
* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard**.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* **D199's four batched calls remain unreviewed — since S127, now nine sessions.**

## Effort

**Analysis — use a strong model at high effort.** This session decides what the tool refuses. Three
effect kinds land on the add path, one of them closing a live D0 violation, and a wrong call ships a
tool that either permits an illegal list or refuses a legal one. Do not run it mechanically.

## Backlog

**9 open:** B62, P2, P4, E21 (E21a/E21b shipped; c/d remain), E22 (E22a done, E22b remains), E23,
B60, E12, B17.
