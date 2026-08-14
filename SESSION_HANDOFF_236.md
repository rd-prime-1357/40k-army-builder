# SESSION HANDOFF 236

**Turn type:** engine-only. See D330. No data file changed; all three repro checks are
byte-for-byte unchanged. `baseline.sh` and `pipeline_manifest.py` were touched only to register
the new harness, which is the standing convention for a new gate, not a tooling change.

## What happened

1. **Open.** Read `NEXT_SESSION_PROMPT.md`, `SESSION_HANDOFF_235.md` and `B99_SCOPE.md`. All five
   S235 file hashes verified against the handoff table and matched. `40K_Decision_Log.md` was
   again absent from the project-area mount (fourth session running) and was recovered by the
   fetch overlay. Full baseline `--fetch --data-turn`: **34/34 gates pass**, both repro checks
   byte-for-byte, `rules_assertions.py --tier all` 125/125, `repo_check` green — Ryan's S235 push
   landed and nothing had drifted.

2. **The census was re-derived from source, and S235's is wrong in one place.** Set A is
   **57 records / 32 names** — D329's figure exactly. Set A2 is **23 records / 13 names**, not
   17 / 12, and the union is **78 / 43**, not 72. The entire difference is *Eye of the Primarch*
   (6 records): it targets "…equipped by the bearer **and** Battleline models in the bearer's
   unit", which is word-for-word the shape of *Blades of Valour*, and D329 put one in Set A and
   the other in Set D only. Including one and excluding the other is arbitrary; both are in.
   D329's §4 flags *Blades of Valour* as a straddle and does not notice its twin.

3. **Set A's boundary re-checked rather than assumed.** *Possessed Blade* reads as unconditional
   under D329's clause rule only because the split on `;` orphans "add 1 to the Attacks
   characteristic of that weapon" from the "At the start of the battle, select one melee weapon"
   that governs it. One player-chosen weapon, not knowable at list-building time — correctly out,
   which is why Set A's 32 names came out right despite the splitter's false positive.

4. **Trap 3's stated test is wrong and is not what shipped.** D329 §4 names ten
   "Character/Epic Hero units … loadout-defined with more than one model group". Epic Heroes can
   never bear an enhancement (`enhancementTypeEligible`), so three of the ten are not at risk at
   all; the real multi-statline-group Character population is six records across three units
   (*Dark Apostle*, *Dark Commune*, *Traitor Enforcer*, each duplicated in CSM and Chaos Daemons).
   More seriously, the statline-group test **misses the one unit that most needs the rule**:
   *Ravenwing Command Squad* has ONE statline group — `isSingleModelGroup` returns true — but
   three loadout groups and three models, only one of which is the CHARACTER, and nothing in the
   data says which. Building to §4 literally would have written a modified profile onto all three.
   The shipped test is on **loadout groups and live model counts**.

5. **Built.** A curated `ENHANCEMENT_WEAPON_EFFECTS` table (78 rows, B113's key and shape), a
   delta applier with the AP sign inversion isolated in one function and string composition for
   variable `A`/`D`, a bearer-attribution rule on the existing D105/D112 three-way pattern reusing
   `statGroupScopes` / `loCarriers` / `loGroupCounts`, and both render sites. The two weapon tables
   now call one shared cell builder (`b99Cells`) and compute nothing of their own, so they cannot
   drift — the divergence failure mode this project has already paid for once is closed by
   construction rather than policed.

6. **Display shipped on D329 §6's recommendations** — Ryan had not answered, all four are
   reversible, and none blocked. Modified value written in gold in the cell; no asterisk on a
   written value; asterisk *instead of* a value wherever the row spans models the bearer is not;
   legend line beneath the table naming the enhancement; conditional clauses unmarked; Set A2
   grants ride the same table into the Abilities column. This is the D89/D112 statline idiom
   unchanged, and no new CSS was needed.

7. **Three engine reading calls, made and noted rather than referred.** An assignment whose record
   no longer resolves modifies nothing (matching `enhancementPoints`). A `not_offered` assignment
   still modifies, because it still costs points — profile and points stay consistent. `'None'` is
   a real stored value and is never modified.

8. **New finding, opened as B122.** Chaos Daemons' 29 enhancement records carry shorthand
   summaries instead of rule text — *Neverblade* as "(Tzeentch Monster, +2S, +1A, +1AP on melee
   weapons, +1 Hit roll)", *A'rgath* as "(Khorne, melee weapon buffs)", several as empty strings.
   At least three are real Set A records that cannot be curated from source. That is why D329
   recorded Chaos Daemons as the one army with no record in either set: the army has them, our
   data does not carry the text. Nothing was curated from the summaries.

9. **`b99_check.js` written and registered** in `baseline.sh` and the GUARDED list. 48 checks
   across the AP sign, variable-value composition, every selector, grant de-duplication, the
   value/asterisk/nothing rendering, the curated table against the source records it came from,
   the bearer-attribution rule against the shipped data (including *Ravenwing Command Squad* and
   *Dark Apostle* by name, and the group-0 assumption across every multi-group Character), the two
   surfaces agreeing cell-for-cell, and the browse view staying untouched.

10. **Close.** `SESSION_HANDOFF_236.md` registered in GUARDED **before** `--write`. Baseline
    re-run, `--write`, then `--freshness-check` as the last command.

## Shipped / changed

- `index.html`: **v6.20 → v6.21**. Two new blocks — `B99 BEGIN … B99 END` (the curated table, the
  selector, the appliers, the shared cell builder and the legend) and `B99 MODE BEGIN … B99 MODE
  END` (bearer attribution and the rollup context). `loWeaponTable`, `loadoutWeaponHtml` and
  `buildWeaponTable` rewritten to route their value cells through the shared builder. Diff is
  16 lines removed, all accounted for: the version constant, the two `loWeaponTable` call sites,
  and the two table bodies.
- `baseline.sh`: `b99_check` gate added after `b106_check`.
- `pipeline_manifest.py`: `b99_check.js` and `SESSION_HANDOFF_236.md` appended to GUARDED (before
  `--write`). `pipeline_manifest.json`: regenerated by `--write` at close.
- `40K_Decision_Log.md`: D330 appended. `DECISION_INDEX.md`: D330 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: B99's entry updated with the corrected census and the shipped engine
  half, and left open for its tooling half; B122 opened; header count 22 → 23.

### Net New Files

`b99_check.js` — a new harness; the project has never held a gate covering enhancement-conferred
weapon modifications, and it replaces nothing. `SESSION_HANDOFF_236.md` is a rolling document,
not net new.

## Ryan action required

- **Push** this session's changed files to the public repo. `repo_check` is red at close for the
  seven files listed below, as expected for unpushed work — not a regression.
- **The render needs your eyeball.** I cannot see the DOM. Worth checking one bearer of each shape:
  a plain single-model Character (gold modified numbers plus a "Modified by …" legend), *Dark
  Apostle* with *Cursed Fang* (Accursed crozius modified, Close combat weapon untouched), and
  *Ravenwing Command Squad* with any Set A enhancement (asterisks, no values, "bearer only" legend).

## Decisions waiting on Ryan

- **B99 display, four decisions** — shipped on the recommendations, all still reversible. New
  Recruit screenshots would settle the idiom if you want it matched.
- **B116** — unchanged. Drukhari's Harlequins/Anhrathe cross-book allied-inclusion mechanic
  (`DRUKHARI_BUILD_SCOPE.md` §6). Blocks nothing shipped.
- **Next faction** — unchanged; the documented priority order is fully built and none is queued.
  Recommendation stands: clear the engine backlog first.

## Files (SHA-256, first 12)

Verify these at S237 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | `e7323a6d2e3e` | v6.21 — the B99 engine build |
| `b99_check.js` | `9155bf36d7a8` | net new — the B99 gate |
| `baseline.sh` | `f8dae08da4e3` | `b99_check` gate registered |
| `pipeline_manifest.py` | `fd1038602890` | two files appended to GUARDED |
| `40K_Decision_Log.md` | `a640bd75bbf9` | D330 appended |
| `DECISION_INDEX.md` | `51ba36b2fe61` | D330 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `659c69fcbd85` | B99 updated, B122 opened, 22 → 23 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `SESSION_HANDOFF_236.md` | (this file) | not self-referential; checked by `--freshness-check` |

## Backlog

22 open at S235 close; **23 open at S236 close** (B122 opened; nothing closed — B99's engine half
shipped but its tooling half is still owed, so it stays open).

Beginning: B116, B99, B119, B120, B121, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75,
P2, P4, E23, B67b, E12, B17 (22).
Resolved: none (0).
Added: B122 (1).
Ending: B116, B99, B119, B120, B121, B122, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70,
B75, P2, P4, E23, B67b, E12, B17 (23).
