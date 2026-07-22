# Session 125 handoff — E1c shipped, E1 closed

**Turn type: engine-only.** `detachments.json`, every parser and every CSV untouched.
`index.html` **6.2 → 6.3**. Authoritative write-up is **D196** in `40K_Decision_Log_v3_0.md`.

---

## Close state

| Gate | State |
|---|---|
| `repro_check.py` | byte-identical |
| `units_repro_check.py` | byte-identical (units.json + four merged lookups) |
| `detachments_repro_check.py` | byte-identical |
| `rules_assertions.py` | **75/75 — all pass** |
| `e1c_check.js` (new) | all pass — 12 scenarios + a sweep across all 143 catalogue keys |
| `bundle_check.js` | 2 pre-existing B36 failures, unchanged |
| `pipeline_manifest.py` | **36 guarded files, all match** |

---

## What shipped

**Left-panel picker.** A `Detachments` section renders at the top of `#roster` above the role
groups, reusing the E2 `.role-group` / `.role-label` / chevron pattern so collapse behaviour,
theming and hit targets are inherited rather than redone. Header shows `N of M DP`, coloured red
only when `dpState() === 'over'`, gold at budget, muted below — E3's rule, applied to detachments.
Below the header, one checkbox row per key from `detachmentKeysForFaction(currentFaction)`, showing
name, force disposition and (where present) Unique tag; each row carries a DP badge and an info
button. Clicking the row toggles selection; a click on the checkbox does the same. Rows that
`canAddDetachment()` refuses render disabled and spell out the reason — `Over the DP budget for
this battle size.` / `Clashes with GRACE tag: Angelic Inheritors.` / `Already selected.` /
`Not in the current catalogue.`

**Info detail per detachment.** The info button expands a `.det-detail` panel (B47's toggle-detail
pattern) with three sections when the data has them: **Detachment Rule** (name + text), then
**Enhancements** (name + points + description, one entry per enhancement), then **Stratagems**
(name + CP + type + description). Restrictions render when the record carries them. Only one
detail panel is open at a time — a second click just moves the panel, so the section does not grow
arbitrarily tall while browsing.

**Previous-edition marking is per item.** `detTier2Badge(source)` marks anything other than the
string `'faction_pack'` — including `null` and `undefined` — as previous edition. The rule tier is
independent of the enhancement description tier is independent of the stratagem tier, and each
carries its own source flag in the E1a record, so the badge appears exactly where the parser knew
the text tier changed.

**Centre panel.** Selected detachments render as a `Detachments` group at the top of the army
list, above every unit type group. Name, force disposition and Unique tag on the left; DP badge and
remove button on the right. Ghost keys render struck-through with a "removed" tag on the flag-
don't-drop precedent — the key is visible so it can be removed rather than disappearing on load.
Over-budget and Unique-tag clash render as warning rows at the top of the group so a player who
never opens the left panel still sees the problem.

**`hasGhosts` covers detachments now.** The load path ORs unresolved detachments into the flag, so
the banner's "list changed since saved" tag catches a detachment ghost alongside a unit ghost. The
handler for `toggleDetachment` also updates `hasGhosts` when a ghost is removed — the flag drops as
soon as the last ghost of either kind is gone.

**No re-implementation of the E1b rules.** Every legality question in the picker goes through
`canAddDetachment` or `detachmentSelectionState`. The picker holds one classifier,
`detachmentPickerRowState(key, keys, points)`, whose disabled flag is
`selected ? false : !canAddDetachment(key, others, points).ok` and nothing else. A selected row is
always toggle-off-able, whatever else is wrong with the set — flag-don't-drop applied to the
picker, so an imported list that arrives over budget or in a Unique-tag clash can always be
corrected.

---

## The structural guard

**`E1c-1` — the five legality helpers are defined once, inside the E1b block, and nowhere else in
`index.html`.** `dpUsed`, `duplicateDetachments`, `uniqueTagConflicts`, `detachmentPointBudget`,
`dpState`. A second definition anywhere is exactly the "picker growing its own rules" failure mode
and would be invisible to every other gate. The assertion locates the E1b block by its own
delimiters and greps the whole file for `^\s*function NAME(`; if any of the five is found outside
the block, the assertion names the file and the line.

**`E1c-2` — `e1c_check.js` executes the disable classification against real data.** 12 scenarios
covering every canAddDetachment refusal type, then a sweep across every one of the 143 catalogue
keys against an empty set at Strike Force, then an over-budget sweep across a real faction's 3 DP
detachments. The sweep exists because a picker that hard-codes the harness fixtures would pass the
scenarios and fail the sweep. Also asserts that a selected row is never disabled in the worst
possible state (over budget AND tag-clashing AND with a ghost).

Assertions **73 → 75**. Guarded set **35 → 36** (`e1c_check.js` added, manifest regenerated).

---

## Decisions made this session (flagged, all reversible)

1. **Picker panel is inside `#roster`, not above it as a separate strip.** That is what
   "collapsible on E2's existing pattern" implied cheapest to build — everything about E2's collapse
   already works, and the alternative meant a second scrollable region on the left.
2. **`detTier2Badge` flags `null` and `undefined` as non-current.** A missing source is treated
   defensively rather than reading as current. A data regression that dropped a source tag can
   never quietly promote tier-2 text to tier-1.
3. **One info panel open at a time.** Simpler state (`openDetachmentDetail` is one key or null) and
   the section stays short. A future prompt could ask for multi-open — small edit.
4. **Refusal text is prose, not codes.** The typed reason from `canAddDetachment` is preserved for
   the harness; the on-screen text is the projection.
5. **Info button uses B47's toggle-detail pattern with a fresh `.det-detail` class.** Reusing
   `.lo-detail` directly would have coupled the picker to the config-panel styling; a small mirror
   class keeps the two independent.

---

## Files

**Changed:** `index.html` (6.3), `rules_assertions.py`, `pipeline_manifest.py`,
`pipeline_manifest.json`, `OPEN_ITEMS_BACKLOG.md`, `40K_Decision_Log_v3_0.md`.

**Net new:** `e1c_check.js`, `SESSION_HANDOFF_125.md`, `NEXT_SESSION_PROMPT_126.md`.

**Unchanged:** `list_store.js` (schema was already v2), `detachments.json`, every parser, every CSV.

---

## Backlog

| | |
|---|---|
| **Beginning** | 10 — P2, E1, E1c, E1e, E21, E4, E12, B56, B17, H3 |
| **Resolved** | 4 — E1, E1c, E1e (all four closed together), plus no others |
| **Added** | 0 |
| **Ending** | 7 — P2, E21, E4, E12, B56, B17, H3 |
