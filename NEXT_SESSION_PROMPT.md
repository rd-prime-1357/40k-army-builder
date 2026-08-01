# Next-session prompt — Session 183

**Assigned: E23 build turn — `HEADHUNTER TASK FORCE` Tank Ace Character-keyword grant.**
The mechanism and all source facts are settled (D272 scoping, D273 data confirmation). This session
writes the effect row, the pick state, and the engine wiring. Turn type is **data + engine** (a
`detachment_effects.json` row plus `index.html`/`list_store.js` changes) — decide at open whether to
split it, but per turn-typing do not also touch parsers or unrelated data in the same session.

## Open at session start

Read `SESSION_HANDOFF_182.md` first, then `40K_Decision_Log.md` **D273** (the confirmed source facts,
army by army) and **D272** (the mechanism decision and engine touch points). Do not trust any
session/version/decision number from memory — re-derive from source. `index.html` is at **v6.14**.

Run the full baseline: `./baseline.sh --fetch --data-turn`. The row you add references unit keywords
and `unit_type`, so tier-B (the three repro rebuilds + `rules_assertions.py`) must run against loaded
GW sources — it must not silently start tier-A-only. Expect 29/29 green at open.

## What D273 confirmed (do not re-derive the facts, build against them)

- The grant is **one Space Marines detachment shared by six armies**, `rule_text` byte-identical in all
  six `detachments.json` records (`cadd53c18131`). Keys: `<Army>|HEADHUNTER TASK FORCE` for Space
  Marines, Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves.
- **Tank Ace = Adeptus Astartes Vehicle, excluding Fortifications, Drop Pods, Walkers, and units that
  can Fly.** A keyword/type exclusion predicate — `Fly`/`Walker`/`Drop Pod` live in model-group
  `keyword_names`, `Fortification` is a `unit_type`.
- **Cap: up to three** picks, per list.
- **Per-army eligible ground truth** (for the assertion): Space Marines 16, Black Templars 16, **Blood
  Angels 17** (adds Baal Predator), Dark Angels 16, Deathwatch 16, Space Wolves 16. The 16 generic
  eligibles and the 12 generic carve-outs are enumerated in D273. No eligible unit is already
  `Character`/`Epic Hero`.

## The build

Per D272's decided mechanism (hybrid, reversible):

1. **`detachment_effects.json` — a new fifth effect kind** (four today: `battleline`, `forbid`,
   `unlock`, `warlord`; the schema `_meta.effect_kinds` block must be extended). Carries the
   detachment-scoped static facts: the eligibility predicate (base = Vehicle **keyword**; exclude
   keywords `Fly`/`Walker`/`Drop Pod` and `unit_type` `Fortification`) and the count cap `3`. Filed
   against all six `<Army>|HEADHUNTER TASK FORCE` keys. Follow D273 note (a): base on the Vehicle
   keyword, **not** `unit_type: Vehicle`, so the Fortification exclusion catches Hammerfall Bunker
   (Vehicle keyword, Fortification type) — its only Adeptus Astartes case. Do **not** enumerate unit
   names in the row (D273 note b): it's a predicate, evaluated per list entry on that entry's keywords.

2. **`list_store.js` — purely-additive pick state.** An array of picked `listId`s, length-capped by the
   detachment's grant, added the same way `warlord_entry_id` (v1) and `force_disposition` (v3) were —
   absence reads as "none elevated," so **no `SCHEMA_VERSION` bump** (stays 3). Continuous silent
   revalidation on every recompute, the `recomputeWarlord()` shape: drop any picked `listId` that stops
   being eligible (leaves the list, detachment deselected, cap exceeded). No confirmation dialog, no
   Muster gate (the app models no Muster phase).

3. **Engine wiring (`index.html`), three touch points from D272:**
   - `eligibleWarlordEntries()` — OR the new per-entry pick array alongside the existing
     `x.unit.isCharacter` test.
   - `canAssignEnhancement`/`enhancementTypeEligible`'s three call sites (~3194, ~3375, ~3689) — use an
     effective per-entry type (`'Character'` when the entry's `listId` is a live pick, else the raw
     `unit_type`), mirroring `effectiveUnitType()`'s overlay shape but at per-entry granularity. Do not
     mutate the raw record.
   - UI: the detachment needs a way to pick up to three eligible entries (identical editability to
     Warlord/Enhancement selection). Product-facing surface — if the picker's placement or wording is
     genuinely ambiguous, batch it for Ryan; otherwise proceed on the closest existing pattern.

## Assertions to add (facts as executable checks)

- Per-army resolved eligible pool matches D273 ground truth: **Blood Angels 17, the other five 16**,
  with the exact excluded army-vehicles (DA's four flyers, SW's four Walker Dreadnoughts, DW's Corvus
  Blackstar, BA's Death Company Dreadnought, Drop Pod, the 5 generic Walkers, the 6 generic flyers).
- The predicate excludes Hammerfall Bunker via the Fortification clause (the keyword-base check).
- **No non-Adeptus-Astartes vehicle can enter these six pools** (D273 note c) — the faction qualifier
  is satisfied by pool construction today, not a keyword test; police it so a future allied vehicle
  can't silently become Tank Ace-eligible.
- Cap = 3 on every one of the six effect rows; schema integrity for the new kind (fifth kind present in
  `_meta.effect_kinds`, all six keys resolve against `detachments.json`).
- `list_store.js` round-trips a pick array and an absent field reads as empty without a version bump.

## After this

- **B69** (select-N ability pools) — data + engine arc, M-sized.
- **B70** (Wardens of Ultramar join mechanic) — decided S175 (D266); needs its own scoping turn first.
- **B75/B85** — blocked on real PDF access from Ryan.
- **Emperor's Children** — next unstarted faction in the priority order; needs an
  `EMPERORS_CHILDREN_BUILD_SCOPE.md` scoping pass before a build, on the CSM/TS model.

## Close protocol

Produce the four documents: `SESSION_HANDOFF_183.md`, overwrite `NEXT_SESSION_PROMPT.md`, append the
decision log + `DECISION_INDEX.md`, update `OPEN_ITEMS_BACKLOG.md` (E23 moves to Closed / Shipped when
the build ships). Bump `index.html`'s `VERSION` and state the new number. Every changed and net-new
file carries a SHA-256 (first 12) in the handoff Files section. Append `SESSION_HANDOFF_183.md` to
`GUARDED` in `pipeline_manifest.py` this same session, then `python3 pipeline_manifest.py --write` then
`--freshness-check` at the very end, after all text is finalized. Repo is public and flat — no
GW-derived material committed; state the exclusions when listing files for the repo.
