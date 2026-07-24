# Session 135 handoff — E21b shipped: `effectiveUnitType()` live, chapter exclusivity policed

**Turn type: engine-only.** `index.html` **6.5 → 6.6**. Assertions **95/95 → 97/97**. Baseline
**21/21 at open → 22/22 at close**. `detachment_effects.json` read as an input and never edited. No
parser, converter or data regeneration. Authoritative write-up is **D212**.

---

## Findings

**Two gates broke on the change and both were repaired, not routed around.**

`D115` matched the literal `instanceLimit(u.unit_type, POINTS_CAP)`, which E21b changed. Its substance
is untouched — the limit is still derived live from `POINTS_CAP` — so the matched string was updated
rather than loosened. `limit_check.js` and `e10_check.js` slice `unitLimit` out of `index.html` and
evaluate it standalone, so both threw on an undefined `effectiveUnitType`; both now pull the E21b
block in with an empty effects table and stay about what they were always about. This is the standing
cost of slicing the real source into harnesses, and it is the right cost to pay.

**Chapter exclusivity was never checked by anything, and is now.** 25 built detachments say the army
may include this Chapter and no other's; `resolveUnits()` has always made that unreachable by
construction and D203 recorded it in prose. **E21b-1** reads chapter membership from
`Datasheets_keywords.csv`'s `is_faction_keyword` flag rather than from `units.json` block membership —
deriving it from block membership would restate its own premise and pass unconditionally. Clean across
all fourteen built blocks: no unit in any resolved pool carries another chapter's FACTION keyword,
including the generic Adeptus Astartes block, which carries none at all.

**The prompt's assertion count was one behind, for a documented reason.** It said 94/94; open was
95/95. 94 was S134's close, and `P4-1` was filed after it in the same conversation, per D211. Six of
the eight S134 hashes differ from the files as received, same cause. **`detachment_effects.json`
matched exactly** — the one that mattered, being hand-authored with no repro gate behind it.

---

## Decisions needed — one, and it is P4's measurement

**P4 step 1 has not happened.** It is Ryan's action, not Claude's: remove `BACKLOG_ARCHIVE.md`
(174 KB) and the archive half of `40K_Decision_Log_v3_0.md` (~400 KB) from the project area, both
fully recoverable from the repo, with `DECISION_INDEX.md` and the backlog's pointer lines preserving
lookup. **Then report what the capacity percentage reads.** If ~574 KB moves it about 4.7 points the
metric is volume-linear and the rest of P4 can be planned against byte counts; if it barely moves, the
797 KB JSON-minification step is not worth re-banking three fixed points. The reading is the entire
point of doing the cheap step first — D211 has the reasoning.

On new files generally, since it was raised at session open: this session added one harness at ~9 KB.
That is noise against a ~12.3 MB area. The pressure comes from the ~5.95 MB Wahapedia export and the
pretty-printed runtime JSON, not from adding checks — so "stop adding files" remains the wrong lever.

**D199's four batched calls remain unreviewed — since S127, now nine sessions.**

---

## Shipped / changed

**`index.html` — 6.5 → 6.6.** `detachment_effects.json` is fetched at init into a `detachmentEffects`
table keyed like `detachmentDefs`; a missing file degrades to an empty table, i.e. under-enforcement
rather than over-enforcement. Two new functions in a marker-delimited block:
`detachmentBattlelineNames(keys)` unions every enforced `battleline` effect's named units across the
current selection, and `effectiveUnitType(unit, keys)` returns `'Battleline'` for a named unit and the
unit's own type otherwise. All three D204 call sites switched: `unitLimit()`, `groupByType` and the
roster's `typeGroups` build. **`unit_type` is never written to** — the elevation is derived on every
read, so a deselect unwinds it with no cleanup pass. No memoisation: it was written and removed, since
the cost is unmeasurable and a cache is state that can go stale.

**`rules_assertions.py` — 95 → 97.** `E21b-1` (chapter exclusivity, source-read) and `E21b-2` (all
three call sites go through the one predicate; no grouping expression falls back on a raw
`unit_type`). `D115`'s matched string updated. Two accessors added to `Sources`: `faction_keywords()`
and `taxonomy()`.

**`e21b_check.js` — net new.** Five sections: the table earns its keep (each named unit's own type is
not already Battleline, plus a negative-control key with no battleline row); elevation on including
grouping; elevation off after deselect and again after re-select; union across three keys plus an
unresolvable key that must be ignored rather than thrown on; the doubled cap at both battle sizes,
with a `limitOverride` case proving a datasheet's printed limit still outranks it. Section 3's fixture
selects three detachments from three factions — not a legal army, stated in the comments; the union
predicate is what is under test.

**`limit_check.js`, `e10_check.js`** — slices extended to include the E21b block.

**`baseline.sh`** — `e21b_check` registered as the 22nd gate. **`pipeline_manifest.py`/`.json`** —
guarded set 39 → 40.

### Net New Files

* `e21b_check.js` — no file has played this role before.

---

## Files

Changed:

| File | SHA-256 (first 12) |
| --- | --- |
| `index.html` | `43189b084695` |
| `rules_assertions.py` | `beebae686f04` |
| `limit_check.js` | `00a64e6e3c6b` |
| `e10_check.js` | `b10034e82bd2` |
| `baseline.sh` | `cd3d27c73dd2` |
| `pipeline_manifest.py` | `cf4e95fcdc38` |
| `pipeline_manifest.json` | `1360f1c91bb8` |
| `40K_Decision_Log_v3_0.md` | `3bf0d8270d6e` |
| `DECISION_INDEX.md` | `0a7fecb8aaed` |
| `OPEN_ITEMS_BACKLOG.md` | `5963462e10fb` |
| `NEXT_SESSION_PROMPT.md` | `c331dd067aeb` |
| `SESSION_HANDOFF_135.md` | *self* |

Net new:

| File | SHA-256 (first 12) |
| --- | --- |
| `e21b_check.js` | `6762446ab906` |

**Repo custody.** All thirteen are project-generated and repo-eligible. `e21b_check.js` names units
and detachments but reproduces no GW rules text. Excluded from any push as always: the Wahapedia CSV
export, the MFM `.txt` files, the faction web and pack files, `Army_Muster_Rules.txt` and
`wh40k_core_rules.md`.

## Backlog

**9 open:** B62, P2, P4, E21 (E21a/E21b shipped; c/d remain), E22 (E22a done, E22b remains), E23,
B60, E12, B17.

- Beginning tickets: B62, P2, P4, E21, E22, E23, B60, E12, B17 (9)
- Resolved tickets: none (E21b shipped; E21 stays open on c/d)
- Added tickets: none
- Ending tickets: B62, P2, P4, E21, E22, E23, B60, E12, B17 (9)
