# Session 129 handoff — UI-only: E4c shipped (D201), E4 fully closed; B56 closed (D202)

**Turn type: UI-only.** `index.html` 6.4 → **6.5**. No engine, data, or parser file touched.
Authoritative write-up is **D201** in `40K_Decision_Log_v3_0.md`.

**Baseline: opened 20/20, closed 21/21** (new `e4c_check.js` gate). Assertions unchanged at 80/80 —
E4c renders legality, it doesn't add any. All twelve S128 hashes verified byte-identical at open.

---

## The finding that mattered

**`repo_check.py` was missing from the project area for a second consecutive session,** exactly as
S128 flagged. It was never actually lost — pulled back byte-identical from the GitHub repo, so the
repo itself is intact — but it should be re-uploaded to project knowledge directly so this doesn't
recur a third time. Once recovered, the custody check ran clean: 72 files byte-matched the repo (68
after this session's own five changed files are counted separately), 7 repo-only files are expected
(old handoffs, `.gitignore`, `README.md`, `_headers`), no GW-derived material anywhere.

**A likely cause of the reported 97%-full project storage.** Several of the CSVs attached to this
session's opening message exist as two different versions under the same filename — Unit_Wargear_
Options.csv (16 rows vs. 13), Unit_Weapons.csv (140 vs. 142), Rules.csv (13 vs. 18). The flat
`/mnt/project` mount shows only one copy of each, so the duplication is sitting in the project's
underlying knowledge store, invisible from the file listing. This is very likely the biggest lever
on the 97% figure — worth checking the project's file manager for a stale second upload of each
before anything else gets pruned. Not something this session could act on directly.

**B56 was already fully resolved — its header had just gone stale.** While assigning S130's next
work I checked the "78/81 closed" claim against `units.json` directly rather than carry it forward.
A first pass used the wrong field and produced nonsense (82 apparent nulls for Adeptus Astartes
alone, including a unit as basic as Intercessor Squad) — caught before it went anywhere, since that
number couldn't be reconciled with a pipeline this thoroughly asserted. The corrected check against
the real `points` field: 270 total units, exactly 2 null — Judiciar Xacharus and Chaplain Kastiel,
both already retired by your S121 call. The header had never been updated after the last chapter
fixes landed. Closed as **D202**; no code or data touched, documentation only.

---

## Shipped

**The config-panel picker.** `enhancementOfferedRowsForEntry(entry, pointsTotal)` filters
`offeredEnhancements()` to `enhancementTypeEligible` for the unit, so a unit sees only rows it could
hold — an Epic Hero with nothing eligible gets no section at all. `renderEnhancementSectionHtml`
renders each as a single-select `option-item radio` row (name, points, detachment), matching the
existing wargear/other-options idiom in this same panel; a disabled row carries
`enhancementRefusalText`'s prose verbatim.

**Two calls beyond the S129 prompt's literal task list, both judgment calls made and recorded, not
asked up front:**
1. Whatever an entry currently holds stays in its row list even if it's gone stale (no longer type-
   eligible or no longer offered) — otherwise a unit holding an import-corrupted assignment would
   have no row in its own panel to click and clear. Direct consequence of the flag-don't-drop
   guarantee already built into E4b; not a new legality call.
2. Each row now carries the same expandable rules-text detail (`mkDetail`/eye icon) every other pick
   in this panel already has, with the previous-edition tier badge. The literal prompt only asked for
   "name + points + detachment," but every other row in this panel is readable before you pick it,
   and the prompt's own standing-input note anticipated enhancement descriptions "becoming visible in
   the UI" once E4c shipped — which only makes sense if a description surface exists. Added it rather
   than ship the one unreadable pick in the panel.

**The roster chip.** `renderEnhancementChipHtml()`, off `enhancementArmyState`, in the same
`list-type-group` idiom the DP display uses. Warning lines (never trimmed) for `over`, `notOffered`,
`wrongType`, `sharedUnits` — the states only an import or a battle-size/detachment change can reach —
each naming the carrying unit. `duplicate` is deliberately not surfaced at the roster level: nothing
in current data can produce a bare name-collision that survives to the roster without also tripping
`notOffered` or `wrongType`; recorded in D201 as a gap to revisit only if that stops being true.

**`e4c_check.js`** (net new, 75 checks, `e1c_check.js`'s mould): type-eligibility filtering; the
flag-don't-drop held-row case including an Epic Hero holding a stale regular pick; `disabled ===
(selected ? false : !canAssignEnhancement(...).ok)` across three scenarios; the section renders empty
for zero eligible rows; every disabled row's refusal text matches `enhancementRefusalText` verbatim;
a row's own description text surfaces in its detail panel; the chip's numbers match
`enhancementArmyState` and its warnings name the right carrier for `notOffered`/`wrongType`/
`sharedUnits`.

**E4 is now fully shipped** — D199 (scope, S127), D200 (engine, S128), D201 (UI, S129). Full history
consolidated and moved to `BACKLOG_ARCHIVE.md`; one-line pointer left in `OPEN_ITEMS_BACKLOG.md`.
D199's four batched calls remain formally unreviewed by Ryan; three of the four (name-keyed
duplicates, Epic-Hero-ban-on-Upgrades, inline picker over a modal) are now load-bearing in shipped
code.

---

## Still open for Ryan

D199's four batched calls, unreviewed since S127 — see D199/D200/D201 for what's load-bearing.

---

## Files

**Changed (SHA-256, first 12):**
- `index.html` — v6.5, E4c block + wiring — `5a6019d5876a`
- `baseline.sh` — `e4c_check` gate added — `eeb354e1c216`
- `pipeline_manifest.py` — `e4c_check.js` guarded — `2503b342e028`
- `pipeline_manifest.json` — regenerated, 38 files — `3fac413791bc`
- `40K_Decision_Log_v3_0.md` — appended D201, D202 — `014b8a7afc47`
- `DECISION_INDEX.md` — `c6aece6eeb7e`
- `OPEN_ITEMS_BACKLOG.md` — E4 and B56 closed out, open count 6→4 — `1298ddd111e7`
- `BACKLOG_ARCHIVE.md` — E4/E4b/E4c and B56 consolidated entries appended (this file was missing
  from the project area this session — recovered from GitHub, byte-identical; now updated) —
  `ba316f0c3450`

**Net new:**
- `e4c_check.js` — the E4c behaviour harness — `ace756aa9124`

Verify at S130 open per T2.

**Unchanged:** every `.json` data file except `pipeline_manifest.json`, every parser, every CSV, all
other harnesses.

**Repo custody:** every file above is project-generated and carries no GW text — all are
repo-eligible. Not yet pushed (repo uploads are batched); `repo_check.py` at close shows these eight
files differing from or missing off the last push, as expected pre-push. `repo_check.py` itself and
`BACKLOG_ARCHIVE.md` were both absent from the project area at this session's open and were both
recovered from GitHub byte-identical — worth a direct re-upload of both to project knowledge so S130
doesn't have to repeat the recovery. Excluded from any repo push as always: the Wahapedia CSV export,
the MFM `.txt` files, the faction web/pack files, `Army_Muster_Rules.txt` and `wh40k_core_rules.md`.

---

## Backlog

| | |
|---|---|
| **Beginning** | 6 — P2, E21, E4c, E12, B56, B17 |
| **Resolved** | 2 — E4c (closing E4), B56 |
| **Added** | 0 |
| **Ending** | 4 — P2, E21, E12, B17 |
