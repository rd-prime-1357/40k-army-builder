# SESSION HANDOFF 250

**Turn type: engine.** B103 (D347) — the non-distinct `replacement_choices` rollup clamp.

## Session open

`./baseline.sh --fetch --data-turn`: **40/40 pass**, 85 source files verified against
`source_manifest.json`. Nothing was worked around.

All thirteen S249 changed files verified against the fetched repo before any work started; every
hash matched the S249 handoff table — `index.html`, `detachment_effects.json`,
`rules_assertions.py`, `b126_check.js`, `baseline.sh`, `list_store.js`, `e1b_check.js`,
`e4b_check.js`, `e4c_check.js`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`.

A `^### ` grep inside the backlog's Open Items section returned **24** against a stated 24. S249's
housekeeping held; no repeat of the three-stub discrepancy.

## What was found

**The ticket is accurate and the defect is still live.** Re-derived from the shipped engine and data
rather than carried from B103's S201 text, and reproduced against the real `loRollup` before
anything was touched. The multi-model branch pushed every tallied pick into `emit` in full and then
wrote `used = Math.min(used, cap)`. Because `chargeSource` was handed the **clamped** figure, the
per-source check below it never saw the overrun — `overAllocated` was `false` in every case tested,
while the emitted weapon counts were identical at a bracket whose cap had halved.

**Reachability is size reduction and nothing else, which is worth knowing precisely.**
`editLoadoutChoiceCount` refuses to step past the group cap, so the UI cannot build an over-cap
tally. `editSizeIdx` sets `sizeIdx`, re-prices, and **never touches `entry.wargear`** — and a
`per_n_models` cap scales with the bracket. Build big, fill to the ceiling, shrink. Two other routes
were checked and ruled out rather than assumed: no shipped option in this shape carries
`requires_weapon`, and exactly one (Deathwatch Veterans `cc_1`) carries a `pool_id`.

**Census, re-derived through the engine's own `loMaxCount`/`loGroupCounts` — not a second
implementation.** 64 count options carry `replacement_choices`; 49 sit on a multi-model group and
are non-distinct, which is the branch this fixes; 30 of those have a cap that shrinks between size
brackets, across 27 units in 12 factions. Two are worse than a partial overrun: **Grey Knights
Brotherhood Terminator Squad `cc_1`** and **Paladin Squad `cc_1`** both fall to a cap of **zero** at
their 4-model bracket, so the whole selection was being emitted and priced with no cap at all.

**Seven shipped units re-price, by 5–10 points each, always downward** — Centurion Devastator Squad,
Deathwatch Terminator Squad, Talos, Brotherhood Terminator Squad, Paladin Squad, Purifier Squad,
Thunderwolf Cavalry. Which units move depends on *how* the player spent the cap, since a priced
choice has to be among the picks truncated, so the census exercises three different fills of the
same cap rather than one. A single fill under-counted the affected set by two.

**A tally that fits its cap is byte-identical before and after** — same weapons, same equipment,
same points — across all 64 options at every bracket. That is the property the whole ticket rests
on and it is asserted directly rather than argued.

**`loCarriers` carries the same defect in a place nothing can reach yet. B136 opened.** It sums every
pick in a `replacement_choices` tally, in storage order, with no cap, when counting carriers for a
`requires_weapon` gate. A scan found **zero** shipped cases where any `requires_weapon` names a
weapon any `replacement_choices` option grants, so it is unreachable today. Deliberately not folded
in — a ticket beats a widened scope — and `B103-2` is scoped to `loRollup` alone so it does not fail
for this unrelated reason.

## Decisions made, not blocked on

**1. Truncation follows the option's own choice order.** Both branches previously used
`Object.keys(tally)` — storage insertion order, i.e. click order, which is not stable across an
export/reimport round trip, so the same saved list could price differently depending on how it was
serialised. Both now iterate `o.replacement_choices`, matching `loDistinctPicks` and for the same
stated reason. This is **free for legal lists** (when every pick fits, order cannot matter), so it
only changes which picks survive a truncation only an already-illegal list can reach.

*The one thing worth Ryan's eye:* priced options tend to sit later in a datasheet's option list, so
the priced pick is usually the one dropped. A Talos built at 2 models with a Stinger pod and a Twin
haywire blaster, shrunk to 1, keeps the Stinger pod. Reversible; say the word and it flips.

**2. The clamp is silent.** S201's reading, carried into the S250 prompt, and it holds up on three
grounds rather than one: the state was never legal (D0); the flag's own message is about contention,
not staleness; and silent clearing on a size change is **already the established precedent** — B34's
size-gated picks are cleared exactly this way in the same renderer. `overAllocated` still fires for
genuine same-source contention, and that is gated.

**3. Clamping the rollup alone would have left a D0 hole, so the stale state is healed.** The rollup
clamp fixes the weapons and the points; it does not fix the *state*. The stepper reads
`entry.wargear` raw, so a clamped-but-unhealed tally would show four psycannons while the rollup
priced two. New `loHealChoiceTallies` truncates the stored tally to the live cap, in the same place
and by the same pattern as the existing cluster heal.

## What shipped

**`index.html` — v6.26.** Three changes.

The multi-model non-distinct branch now bounds each pick against the remaining cap as it reads it,
exactly as the fixed-1 branch already did, and iterates the option's own choice order. The fixed-1
branch's iteration order was aligned to match; its clamping was already correct. The two branches
now agree on the same shape, which was half of what B103 asked for.

New `loHealChoiceTallies(def, size, entry, optCounts, isSuppressed)` sits beside `loDistinctPicks`
and is called from `renderLoadoutOptions` immediately before the rollup. It was **factored into a
named function specifically so a harness can slice it** — S249's lesson that a new call path nothing
exercises is a latent failure regardless of what the gates say. This is not an extraction out of
`index.html`; the standing constraint concerns moving code into separate files, which this does not
do.

Two deliberate narrowings, both in the function's own comment. It skips suppressed options, whose
own clearing pass owns them. And it does **not** apply the shared-pool narrowing the stepper
applies, because that is read off a rollup that has not run yet — applying it would make the heal
stricter than the cap the player was last shown. `loRollup` remains the authority for what is
emitted and priced.

**`b103_check.js`** (new). Both branches clamped and truncating identically; insertion order proven
not to change the result; a cap of zero emitting nothing; the legal-tally-untouched property on
fixtures **and** across the whole shipped population; the selection path's refusal to build an
over-cap tally in the first place; genuine same-source contention still firing `overAllocated`; and
six cases on `loHealChoiceTallies` (heal-and-rollup agreement, the distinct per-choice cap, unlisted
keys dropped, suppressed options skipped, non-object values skipped). Its last two sections
re-derive the population and the seven re-pricing units from the real data rather than asserting a
remembered number. Wired into `baseline.sh` and `pipeline_manifest.py`'s GUARDED list.

**`rules_assertions.py`.** `B103-1` — every `replacement_choices` option carries an authored cap.
This one is not decoration: `loMaxCount` returns **0**, not Infinity, for an option with none, so an
uncapped option does not mean "no limit", it means the rollup silently emits nothing. The population
is pinned at 64/49 in the same assertion, so a parser change or a new faction that widens the
affected set fails here rather than passing quietly. `B103-2` — the defect line is gone, neither
rollup branch iterates in storage order, and `loHealChoiceTallies` is defined exactly once **and
actually called** (a heal that exists but is never invoked would clamp the points while leaving the
picks on screen). `B103-3` — the harness gate.

## Verified directly, not just through the gate

`./baseline.sh`: **41/41** with `b103_check` registered. `python3 rules_assertions.py --tier all`:
**136/136** (133 before, plus `B103-1`..`B103-3`).

**The new gate was negative-tested.** Against a copy of the engine with the single defect line
restored, `b103_check.js` fails **10** assertions, including the two Grey Knights cap-zero cases and
the whole re-pricing census. A gate that passes on the broken build is worthless; this one does not.

**Not verified this session:** no browser render check. **This is the third engine turn in a row
shipped unseen**, after S248's Tank Ace UI and S249's mark selector. B103 adds visible behaviour —
picks disappearing from the stepper when a saved unit is shrunk — so the backlog of unseen UI is now
three deep and one of them silently edits the player's list.

## Files (SHA-256, first 12)

Verify these at S251 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | `17e9f795ba5c` | **v6.26.** multi-model branch clamps per pick; both branches iterate choice order; new `loHealChoiceTallies` called from `renderLoadoutOptions` |
| `b103_check.js` | `bade1728bcec` | **new file** — behaviour gate for the clamp, the heal and the shipped census |
| `rules_assertions.py` | `1666accee2db` | `B103-1`..`B103-3` |
| `baseline.sh` | `e18803ff0f83` | `b103_check` gate registered |
| `pipeline_manifest.py` | `35a77ddd0bea` | `b103_check.js` added to GUARDED; `SESSION_HANDOFF_250.md` registered |
| `40K_Decision_Log.md` | `05a09f6b3b63` | D347 appended |
| `DECISION_INDEX.md` | `269bcd9a3fa8` | D347 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `eff60eb8755b` | B103 moved Open → Closed/Shipped; B136 opened; header count restated for S250; S250 ledger added; 24 → 24 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_250.md` | (this file) | not self-referential; checked by `--freshness-check` |

## Ryan action required

- **Push this session's changed files** to the public repo: `index.html`, `b103_check.js` (new),
  `rules_assertions.py`, `baseline.sh`, `pipeline_manifest.py`, `40K_Decision_Log.md`,
  `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.json`,
  `SESSION_HANDOFF_250.md`, `NEXT_SESSION_PROMPT.md`.
- **`pipeline_manifest.json` must be included.**
- **A render check covering S248, S249 and now this session.** Three engine turns unseen. For B103,
  one list is enough: create a **Grey Knights** list, add a **Purifier Squad** at **10 models**, open
  its wargear pane and fill the psycannon/psilencer/incinerator option to its ceiling of 4. Note the
  unit's points. Now change the size to **5 models**. Expect: the points fall, the stepper shows
  **2** picks rather than 4, and **no warning banner appears** — the correction is silent by design
  (decision 2 above). Then reopen the pane and confirm the two surviving picks are the first two in
  the option's listed order, not the first two you clicked. If a "Too many weapon swaps for this unit
  size" banner shows up at any point in that run, that is a real defect — tell me.
  Then the S248 Tank Ace pass and the S249 Marks of Chaos pass per those handoffs' scripts.

## Decisions resolved this session

D347 — B103's fix, the three calls above (choice-order truncation, silent clamping, healing the
state rather than only the rollup), the census, and B136's split.

## Backlog

24 open at S249 close; **24 open at S250 close**. Resolved B103; added B136. Net zero, and unlike
S249's net zero these are genuinely independent: B103 is fixed outright, and B136 is a separate
function carrying the same mistake in a place nothing can reach yet.
