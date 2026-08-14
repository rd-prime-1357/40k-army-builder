# SESSION HANDOFF 238

**Turn type:** engine-only. `index.html` v6.21 → v6.22, plus one net-new harness and its two
registrations (`baseline.sh`, `pipeline_manifest.py`). **No data file changed** — every JSON
output is byte-identical to S237.

## What happened

1. **Open.** Read `NEXT_SESSION_PROMPT.md` and `SESSION_HANDOFF_237.md`. All ten S237 file
   hashes verified against the handoff table and matched, against a freshly fetched repo.
   Baseline `--fetch`: **29/29 gates pass, 5 tier-B skipped** (GW sources not loaded, correct for
   an engine turn). `repo_check` **green** — S237's push had landed, so the "repo is red" note
   carried in `NEXT_SESSION_PROMPT.md` was already stale. `40K_Decision_Log.md` again absent from
   the project-area mount (sixth session running) and again recovered from the repo, already
   carrying D331.

2. **B119's census re-derived from source rather than trusted.** D329's Set C figures were
   re-run against `detachments.json` using B99-CENSUS's clause-splitting method, tightened for
   the statline case. **Result: 10 records / 6 names / 8 armies — D329 exactly.** The discipline
   was worth keeping (D330 had to correct D329's Set A2 count), but this time the number held.

3. **The prompt's two open questions, answered before building.**
   - *Overlap with a Set A/A2/B/D effect?* None. No Set C key appears in
     `ENHANCEMENT_WEAPON_EFFECTS`, so nothing composes across the two tables.
   - *Does the bearer-attribution question arise?* Yes, and the answer is **better** than for
     weapons. The stat table renders one table per statline group, so a retinue group gets
     nothing rather than an asterisk. Four units exercise it and all four resolve exactly.

4. **Seven of the ten records carry a second, conditional clause.** The *Rites of War* family
   hands the same +1 Objective Control to the rest of the unit once per battle. The bearer half
   is unconditional and ships; the once-per-battle half is Set B and does not. The harness's
   first draft tested that *every* matching clause was unconditional and failed all seven — that
   failure is how the shape was found, not a guess corrected afterwards.

5. **Built.** `ENHANCEMENT_BEARER_STATS` (curated, B113/B99 key shape), `b119Compose`,
   `b119BearerStatMode`, `b119StatCtx`, and the `buildStatTable` changes that let the T and OC
   cells carry an override at all. The delta is applied **after** the set-value overrides,
   because 40K applies modifiers after characteristics that are set. Legend wording factored into
   one shared `enhModLegend` so the weapon table and the stat table cannot drift apart in wording;
   `b99Legend` delegates to it and its output is unchanged.

6. **Three harness bugs found by running it, not by reading it** — a `stat-asterisk` substring
   colliding with the `stat-asterisk-legend` class, the SV cell's `+` suffix inside the override
   span, and the over-strict conditional test above. All three fixed; `b119_check` is green.

7. **One gate went red mid-build and was reconciled, not worked around.** `rules_assertions.py`'s
   `B7b-1` pins `buildStatTable`'s signature as an exact string, and B119's fifth parameter broke
   it. The pin was updated to the new signature rather than loosened to a substring match — an
   exact pin is what surfaced the change, which is the behaviour wanted. This is the one file
   outside `index.html` and its harness that this engine turn touched, and it is touched *because*
   `index.html` changed shape, not as separate tooling work.

8. **Two populations D329's census never covered, found here and banked** (see Decisions below and
   D332). Neither was folded into this build.

9. **Close.** `SESSION_HANDOFF_238.md` and `b119_check.js` registered in GUARDED before
   `--write`. Baseline re-run, `--write`, then `--freshness-check` as the last command.

## What's in the build

- **Census, confirmed at build time:** 10 records / 6 names / 8 armies. *Brazen Form* (T+1),
  *Living Carapace* (W+1), *Master Artisan* (W+1), *Rites of War* / *Disciple of Rhetoricus* /
  *Iron Laurel* (OC+1).
- **The delta lands on a SET value, not the printed one.** A wargear-set Wounds of 6 plus a +1
  enhancement reads 7. Pinned.
- **T, W and OC compute; they do not compose** — the opposite of B99's A and D. Every T/W/OC value
  on every model group is a plain integer, re-checked by the harness each run so the assumption
  cannot rot.
- **Bearer attribution:** *Dark Apostle*, *Dark Commune* and *Traitor Enforcer* write to statline
  group 0 and nothing to group 1. *Ravenwing Command Squad* — one statline group, three models,
  one of them the CHARACTER — takes the asterisk and never a value. Both readings are exercised
  against real units, not fixtures.
- **Save, Leadership and Movement are unimplemented on purpose.** No source record confers a delta
  on them, and Save would need the AP sign rule's mirror image. `b119_check` fails if a record ever
  needs a characteristic the applier does not implement — a gate, not a guess.

## Ryan action required

- **Push this session's changed files** to the public repo. `repo_check` is red at close for
  `index.html`, `baseline.sh`, `pipeline_manifest.py`, `rules_assertions.py`, `b119_check.js`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md` and
  `SESSION_HANDOFF_238.md` — expected for
  unpushed work, not a regression. Reconcile at open.
- **The render needs your eyeball.** I cannot see the DOM. Worth checking one bearer of *Rites of
  War* (OC cell highlighted, "Modified by Rites of War" beneath the table) and one Ravenwing
  Command Squad (OC asterisked, printed value kept, "* bearer only — Rites of War").

## Decisions waiting on Ryan

- **B123 display precedence — NEW, and the one that blocks a build.** When an Enhancement and
  equipped wargear both set the same statline cell (Save, Feel No Pain), does the app show the
  better value, the Enhancement's value, or an asterisk? *Recommendation: the better of the two,
  cell marked* — by rule a model has one Save and one Feel No Pain and uses the best available.
  It sets a lasting display precedent, so it is yours rather than mine. 25 records wait on it.
- **B99 display, four decisions** — unchanged since S236, all still reversible. B119 followed the
  same idiom, so a change of mind now moves both. New Recruit screenshots would settle it.
- **B116** — unchanged. `DRUKHARI_BUILD_SCOPE.md` §6. Blocks nothing.
- **Next faction** — unchanged; the documented priority order is fully built and none is queued.
  Recommendation stands: clear the engine backlog first.

## Files (SHA-256, first 12)

Verify these at S239 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | `51bd0c0c3796` | v6.22; B119 engine half |
| `b119_check.js` | `43cb2009f58c` | **net new** — B119 harness |
| `baseline.sh` | `b72c2189a98e` | `b119_check` gate added |
| `pipeline_manifest.py` | `2341917ae694` | `b119_check.js` + `SESSION_HANDOFF_238.md` guarded |
| `rules_assertions.py` | `0098c104788a` | B7b-1's `buildStatTable` signature pin updated for B119's 5th parameter |
| `40K_Decision_Log.md` | `d27fc1f7964b` | D332 appended |
| `DECISION_INDEX.md` | `e0aa15992a48` | D332 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `f4ae139dd4d2` | B119 engine half recorded; B123, B124 opened; 21 → 23 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `SESSION_HANDOFF_238.md` | (this file) | not self-referential; checked by `--freshness-check` |

### Net New Files

`b119_check.js` only. Everything else is an update to a file the project already held.

## Backlog

21 open at S237 close; **23 open at S238 close** (B123 and B124 opened; nothing closed — B119's
tooling half is still outstanding, so the ticket stays open).

Beginning: B116, B119, B120, B122, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2,
P4, E23, B67b, E12, B17 (21).
Resolved: none (0).
Added: B123, B124 (2).
Ending: B116, B119, B120, B122, B123, B124, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70,
B75, P2, P4, E23, B67b, E12, B17 (23).
