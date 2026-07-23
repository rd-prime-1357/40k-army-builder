# Session 128 handoff — engine-only: E4b shipped (D200), D199's eligibility claim corrected

**Turn type: engine-only.** `index.html` 6.3 → **6.4**, `list_store.js` schema 2 → **3**. No `.json`
data file, no parser, no CSV touched. Authoritative write-up is **D200** in
`40K_Decision_Log_v3_0.md`.

**Baseline: opened 19/19, closed 20/20.** Assertions **75 → 80**. All four S127 hashes verified at
open; the project-area sync gap S127 reported is closed — `repro_check.py`, `pipeline_manifest.py`
and a current `pipeline_manifest.json` were all present, so no detour was needed.

---

## The finding that mattered

**D199's eligibility claim is wrong as written, and had to be corrected before E4b-2 could exist.**
D199 says a full scan found no unit whose CHARACTER keyword qualifies it while `unit_type`
disqualifies it. Fifty-three Epic Heroes do exactly that — in the rules an Epic Hero *is* a
Character, and 25.04 bans them by a separate bullet. The claim holds only once the keyword
derivation is written as **has CHARACTER and NOT EPIC HERO**; with that carve-out the two
derivations agree exactly, bar the two exceptions D199 already names, both in the safe direction.

No behaviour D199 specified changes. What changes is the assertion. Written to D199's prose, E4b-2
would have failed on first run against fifty-three units, and the obvious repair under time
pressure — dropping the EPIC HERO half — yields a gate that passes while asserting the opposite of
the rule. Full detail in D200.

**Other re-derivations, all confirmed:** 29 collision pairs (5 distinct names across 7 chapter
armies — the pair count and the name count are very different numbers), Deathwing Assault 30/15 as
the sole differing-price case and *not* an Upgrade, 35 upgrade records over 20 names with
`is_upgrade` consistent for every name, 70 Character / 58 Epic Hero. The 25.03 **Enhancement Limit
column is 2/4**, not the 2/3 DP column beside it.

---

## Shipped

Per-entry `enhancement: {name, detachment_key}`. Schema v3 with `normaliseEnhancement()` at the
persistence boundary; v2 records migrate by gaining `enhancement: null` and nothing else.
`canAssignEnhancement` as the single read path over the five 25.04 rules, hard block on the
D114/D115 line, reasons ordered permanent-before-temporary as `canAddDetachment` does.
`enhancementRowState` classifies a picker row over it and re-derives nothing. Two enforcement
points: the assignment action refuses as a no-op, and `editLeaderTarget` consults
`enhancementAttachBlock` so two carriers cannot be attached into one unit — 25.04's per-unit bullet
reads "including attached units", so the scope is the whole cluster. Points fold into
`ptsForEntry`. Upgrade carve-out: three copies, all priced, only the first counted.

**Two calls beyond D199, both recorded in D200:** a duplicated unit (and a duplicated leader) does
not inherit its enhancement — inheriting would create a duplicate at the instant of the copy, which
is what B41/D0 refuse rather than flag; and a ghost entry's enhancement does not count, following
`totalPoints()`.

**Assertions:** E4b-1 (limit from the Enhancement column, with an explicit trap for it having been
taken from the DP column), E4b-2 (derivations agree, with a two-entry allowlist that fails if a gap
closes and goes stale), E4b-3 (census pinned three ways — 29 pairs / 5 names / 1 priced
differently), E4b-4 (sixteen functions defined once inside the block, *and both enforcement points
wired* — a declared-but-uncalled gate is worse than none), E4b-5 (`e4b_check.js`, 60 checks).
E1b-2 repinned to schema 3. `e1b_check.js` now reads the version from the module rather than
pinning a literal, so later field additions do not require touching nine assertions.

`e10_check.js` gained scenario 7 and now loads the real E4b block rather than stubbing it, so the
duplicate carve-out is executed against real code.

---

## Still open for Ryan

**D199's four batched calls remain unreviewed, and E4b is built on all four:** name-keyed
duplicates, Epic-Hero-ban-on-Upgrades, free-text restrictions displayed-not-enforced, and the
inline config-panel picker. The first two are now load-bearing in shipped engine code and in
assertions; overruling either is a rework of `canAssignEnhancement` plus E4b-2/E4b-3, not a
one-line change. The fourth (UI shape) is still free — E4c has not started.

---

## Files

**Changed (SHA-256, first 12):**
- `index.html` — v6.4, E4b block + wiring — `e1f1923a5ba8`
- `list_store.js` — schema v3 — `2bc2c445e205`
- `e1b_check.js` — reads the module version; v2→v3 step asserted — `7dc666f9bbec`
- `e10_check.js` — scenario 7; loads the real E4b block — `5a7917a86975`
- `rules_assertions.py` — E4b-1..5 added, E1b-2 repinned — `e70d8488a0e6`
- `pipeline_manifest.py` — `e4b_check.js` guarded — `225e47ac61d4`
- `pipeline_manifest.json` — regenerated, 37 files — `be0d5838b04a`
- `baseline.sh` — `e4b_check` gate added — `97b6c69b9f8d`
- `40K_Decision_Log_v3_0.md` — appended D200 — `ac636085758a`
- `DECISION_INDEX.md` — `1fc7cfd9aa89`
- `OPEN_ITEMS_BACKLOG.md` — `0ff8e37a0ae7`

**Net new:**
- `e4b_check.js` — the E4b behaviour harness — `7ca74addb5a0`

Verify at S129 open per T2.

**Unchanged:** every `.json` data file, every parser, every CSV, all other harnesses.

**Repo custody:** every file above is project-generated and carries no GW text — all are
repo-eligible. `repo_check.py` was not in the project area this session and could not be run;
S129 should run it at open. Excluded from any repo push as always: the Wahapedia CSV export, the
MFM `.txt` files, the faction web/pack files, `Army_Muster_Rules.txt` and `wh40k_core_rules.md`.

---

## Backlog

| | |
|---|---|
| **Beginning** | 7 — P2, E21, E4b, E4c, E12, B56, B17 |
| **Resolved** | 1 — E4b |
| **Added** | 0 |
| **Ending** | 6 — P2, E21, E4c, E12, B56, B17 |
