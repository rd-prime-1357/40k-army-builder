# SESSION HANDOFF 240

**Turn type:** scoping-only. No data file, no `index.html`, no parser changed. One net-new
reference document, the four rolling documents, and `pipeline_manifest.py`'s GUARDED list.

## What happened

1. **Open.** Read `NEXT_SESSION_PROMPT.md` and `SESSION_HANDOFF_239.md`. All five S239 file hashes
   verified. Baseline `--fetch --data-turn`: **36/36 gates pass, no tier-B skips**. `repo_check`
   **green** — S238's and S239's unpushed sets have both landed, so that carried Ryan action is
   closed.

2. **B93 censused across all 739 enhancement records.** The prompt's instruction not to carry
   forward D332's six names was right: the real population is **641 records carrying a
   bearer-restriction clause** — 363 distinct names, 173 detachments, 13 of 14 armies, 87% of all
   enhancement records. B113's curated table holds seven rows.

3. **369 records over-admit today**, measured against each record's own clause over each army's
   real unit pool resolved through `faction_taxonomy.json` — 237 names, 13 armies, mean 9.2 illegal
   bearers per record. 12 of the 25 clause-bearing Upgrades are among them, confirming that
   `enhancementTypeEligible()` applies no restriction at all to Upgrades.

4. **The core rule was read from source, not remembered.** `Army_Muster_Rules.txt` states
   Characters-only, no Epic Heroes, no duplicates, Upgrades exempt — all "unless otherwise stated."
   Three of the four are already enforced correctly. The gap is that phrase.

5. **D334 recorded, then REVERSED at D335 in the same session, with nothing built on it.** D334
   read the clause as *replacing* the Characters-only default, on the strength of the 24
   `Adeptus Astartes Vehicle model only` records having no Character bearer. Ryan supplied
   Headhunter Task Force's rule text — which is present in our own `detachments.json`, in
   `rule_text`, and which the census did not read. It confers **Tank Ace** on qualifying Adeptus
   Astartes Vehicles and lets the player **select up to three to gain CHARACTER at muster**, with a
   Designer's Note saying that is exactly what lets them take Enhancements and be Warlord. So the
   clause **narrows within** the default after all. **The lesson is bigger than the decision:**
   bearer eligibility cannot be answered from enhancement text alone, because the detachment can
   change who counts as a Character. Re-tested across the whole population — narrowing strands only
   the 24 Vehicle (B128), 6 Deathwing (B125) and 4 Marks (B126) records, all already ticketed.

6. **B128 opened.** Censused after the reversal: **28 of 211 detachments confer a keyword during
   mustering, 35 conferrals in total** — Character, Tank Ace, Heavy Transport, Entrenched,
   Battleline, faction keywords, Daemon/Soul Forge. None is modelled. Headhunter's is the only one
   that is a **player choice with a hard cap** (up to three, one of which may be Warlord), so the
   only one that is legality-critical: a list with four Character Tank Aces is illegal and must be
   unreachable.

7. **Four blockers found — three are new tickets, and they are why nothing was built.**
   **B125**: chapter keywords are stripped from union rosters and never re-added, so Dark Angels'
   `Deathwing model only` resolves to zero eligible Characters (Deathwing 8 units held vs 27 in
   source, 5 Characters lost; Ravenwing 7 vs 16). Prerequisite. **B126**: Marks of Chaos are chosen
   at mustering and unmodelled — 4 enhancements depend on them, and so do two further unenforced
   D0 rules in the same detachment's `restrictions` (attachment and Transport must share a mark).
   **B127**: 74 records have no rule text in any held source; 70 have no name match in
   `Enhancements.csv` and the 4 that do match a *10th-edition* detachment name whose 11th-edition
   twin already resolves with full text — so the parser is right and must not be loosened. Fourth
   blocker, not a new ticket: **D199** already records that eligibility keys off `unit_type` and
   not keywords because keyword lists are uneven; re-verified at 8 Character-typed units with no
   Character keyword and 6 with multiple model groups, so an unevaluable restriction must fall
   through to permissive rather than refuse.

8. **Two census traps worth carrying forward, both of which lose records silently rather than
   failing.** Splitting descriptions on `.` alone loses Thousand Sons' *Unravelled Fates*, whose
   flavour sentence ends in `?` — the first pass of this census reported 640 instead of 641 for
   exactly that reason, and was corrected by re-deriving rather than by patching the number. And
   the slash distributes over the shared tail: `INFANTRY/MOUNTED THOUSAND SONS PSYKER model only`
   means (Infantry or Mounted) and Thousand Sons and Psyker.

9. **`SPEEDER` confirmed absent from source, not assumed.** 12 records say `SPEEDER unit only`;
   there is no such keyword anywhere in `Datasheets_keywords.csv` across 1,423 distinct keywords.
   Needs a curated unit-name list, the B113 Pact-of-Cursed-Pinions shape.

10. **Close.** `B93_SCOPE.md` and `SESSION_HANDOFF_240.md` registered in GUARDED before `--write`.
   Baseline re-run, `--write`, then `--freshness-check` as the last command.

## Ryan action required

- **Push this session's changed files** to the public repo: `B93_SCOPE.md`, `pipeline_manifest.py`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_240.md`,
  `NEXT_SESSION_PROMPT.md`. `repo_check` is red at close for these — expected for unpushed work,
  not a regression.
- Nothing needs your eyeball — no render changed.

## Decisions resolved this session

- **D334 → D335.** Reversed on Ryan's evidence, nothing built on it. The clause narrows.
- **B123 display precedence — DECIDED, ticket unblocked.** Show the best **unconditional** value;
  if a conditional value would be better, show the unconditional one and mark the cell. Better than
  the recommendation it replaced, because "better" is ill-defined when one of the pair is
  contingent — a 2+ Save that only applies against ranged attacks is not comparable to an
  unconditional 3+. Generalises past B123 to the whole statline.
- **B99's four display decisions — closed as already shipped, not decided.** They were carried
  forward as open since S236 and re-listed at S239 and in this session's first close. That was
  wrong; `index.html` was read to confirm it. `b99Cells` and `enhModLegend` implement all four —
  modified value written and highlighted, base value plus asterisk where only some models in a row
  carry the effect, a legend line naming the enhancement, ability grants in the Abilities column,
  and no marker for conditional effects. Ryan can still change any of them; none blocks a build.
- **B116 — reclassified, not deferred indefinitely.** Required before the product is
  production-ready. Now gated on Aeldari being built far enough to price the 14 units, which makes
  it a release-plan dependency rather than a backlog item.

## Decisions waiting on Ryan

- **Next faction after Drukhari** — the documented priority order is fully built and none is queued.
  Recommendation stands: clear the engine backlog first. B116's reclassification adds a wrinkle —
  Aeldari is now a production dependency even though it is not in the priority order.

## Files (SHA-256, first 12)

Verify these at S241 open.

| file | sha256:12 | note |
|------|-----------|------|
| `B93_SCOPE.md` | `38e32bd4b407` | net new — B93 census, re-scope, and the D335 correction |
| `pipeline_manifest.py` | `20a81522f42a` | `B93_SCOPE.md` and `SESSION_HANDOFF_240.md` guarded |
| `40K_Decision_Log.md` | `a495a9fd5a84` | D334 and D335 appended |
| `DECISION_INDEX.md` | `e1e557a95700` | D334 and D335 one-liners appended |
| `OPEN_ITEMS_BACKLOG.md` | `29df29432975` | B125/B126/B127/B128 opened; B93 re-scoped; B123 decided; B116 reclassified; 22 → 26 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_240.md` | (this file) | not self-referential; checked by `--freshness-check` |

### Net New Files

`B93_SCOPE.md` — the project has never held a B93 scope document. Everything else this session is
an update to a file that already exists in that role.

## Backlog

22 open at S239 close; **26 open at S240 close** (B125, B126, B127, B128 opened; nothing closed).

Beginning: B116, B120, B122, B123, B124, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75,
P2, P4, E23, B67b, E12, B17 (22).
Resolved: none (0).
Added: B125, B126, B127, B128 (4).
Ending: B125, B126, B127, B128, B116, B120, B122, B123, B124, B97, B103, E28, B93, B90, B94, B85,
B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (26).

B123 is no longer decision-blocked and is now the cheapest buildable item in the set.
