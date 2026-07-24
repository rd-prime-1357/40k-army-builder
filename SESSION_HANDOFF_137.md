# Session Handoff 137

## Baseline at open

`e21b_check.js` was absent from the project area at session open — three gates failed on it
(`rules_assertions`, `pipeline_manifest`, and the direct `baseline.sh` call). Per the standing rule,
this was reconciled before any new work started rather than worked around: Ryan re-uploaded the file
(likely deleted by mistake, confused with another lettered check), it was copied in, and its hash was
verified against the S135 manifest entry before trusting the sync. Full baseline then ran clean,
23/23, before E21d began.

## What shipped — E21d, pieces 1 and 2

**Piece 1 — refusal prose and the picker's forbid gate.**
- `addRefusalText` brought up to `enhancementRefusalText`'s standard: each reason now names the unit,
  the group, and (for the allied sub-cap) the used/cap/adding numbers.
- `detachmentPickerRowState` now also calls `detachmentForbidConflicts(key)` for a non-selected row —
  a key that would forbid a unit already in the list now disables **before** the click, not only after
  it inside `toggleDetachment`. New `detachmentForbidRefusalText` supplies the prose.
- **E1c-2 deliberately extended, not loosened** — the prompt's explicit instruction. A non-selected row
  is now disabled iff `canAddDetachment` refuses it OR the forbid gate does.
- `e1c_check.js` pulls in the E21c/E22b block (same slice-the-real-block pattern `e10_check.js` /
  `limit_check.js` already use) and gained a new section exercising the gate: no conflict before the
  unit is listed, disabled + named conflict once it is, re-enabled once removed, and a SELECTED row
  stays toggle-off-able throughout. One self-caught test bug: the synthetic forbid key needed a real
  (minimal) `detachmentDefs` entry, or `canAddDetachment` refused it as `'unknown'` independent of the
  gate under test — fixed by mutating the same object reference `detachmentDefs` aliases.

**Piece 2 — Battleline indicator (D204 ruling 2).** A detachment-elevated unit's roster row now shows
"Battleline — granted by selected detachment." Reads the same `detachmentBattlelineNames()` set
`effectiveUnitType` already uses for the grouping, computed once per render, so the indicator can never
disagree with which group the unit actually renders under.

**Piece 3 — NOT built.** The stranded-allied roster warning (D214's recommendation: flag as a visible
error, never a silent trim or a blocked deselect) is a lasting precedent and was deliberately held for
Ryan's confirmation per the prompt's own instruction. Still open. E21 does not close until this ships.

## What shipped — three UI tickets from a screenshot review (B64/B65/B66)

Logged as backlog items in the prior conversation turn from four screenshots Ryan supplied; built this
session since all three are UI-only against `index.html` and batch cleanly with E21d.

- **B64** — the detachment (i) button no longer expands detail inline in the left panel; it opens the
  shared centered `#stat-modal` (new `openDetachmentDetailModal`), the same popup the unit
  full-datasheet uses. Scope call stated but not blocking: all detail moves to the popup, the row keeps
  only name/battle trait/DP. Dead inline-expander state (`openDetachmentDetail`) and CSS removed.
- **B65** — a DP-budget-only refusal (not an illegal state) no longer renders in red. New
  `.det-refusal-neutral` (muted) class for budget/duplicate/tag-clash/unknown; `.det-refusal` (red)
  reserved for the forbid-conflict case, a real D0 guard. Direct application of E3/D114's existing
  convention — no new decision needed for the call itself.
- **B66** — the config panel's single-item detail button (`infoBtn()`) rendered an eye SVG. Since
  `infoBtn` is the one shared renderer for every configurable item's detail button across the whole
  panel (enhancement rows, loadout swaps, wargear options, bundle endpoints), swapping the glyph to an
  info-circle SVG fixed the entire panel in one place — matches B47's existing info-icon convention.

## Render needs Ryan's eyeball

Claude cannot see the DOM. In particular: the B64 modal's layout and content inside `.modal-body`, the
B65 colour distinction actually reading as intended against the theme, the B66 glyph rendering cleanly
at 13x13, and the Battleline indicator's placement in the sub-line not crowding the model-count text.

## Decisions needed

**E21d piece 3 — the stranded-allied direction.** D214's recommendation: flag a Plague Legions unit
stranded by deselecting/switching away from Tallyband Summoners as a visible roster error (the
enhancement over-state treatment), never a silent trim, and not by blocking the deselect. This sets a
lasting precedent for how the tool treats a legal list a later detachment change makes illegal.
Confirm before it's built.

**B64's scope assumption.** All detachment detail now lives only in the (i) popup; the row itself is
minimal (name/battle trait/DP). If a different balance is wanted — e.g. an inline summary retained for
the currently-selected detachment — say so and it's a small follow-up change, not a rebuild.

## Shipped / changed

`index.html` (6.7 → 6.8): `addRefusalText` rewritten; `detachmentPickerRowState` extended with the
forbid gate; new `detachmentForbidRefusalText`; new `openDetachmentDetailModal` replacing
`toggleDetachmentDetail`; `openDetachmentDetail` state and its dead CSS removed; `.det-refusal-neutral`
CSS added; `infoBtn()`'s single-item glyph swapped from an eye SVG to an info-circle SVG; Battleline
indicator added to the roster row's sub-line.

`e1c_check.js`: now pulls in the E21c/E22b block; new section 6 (six checks) exercising the forbid
gate end to end.

`rules_assertions.py`: E1c-2's description updated to state the extended disabled rule.

`pipeline_manifest.json`: reissued for the three guarded files above.

`40K_Decision_Log_v3_0.md`: **D215** appended. `DECISION_INDEX.md`: D215 indexed.
`OPEN_ITEMS_BACKLOG.md`: E21 header updated (pieces 1-2 shipped, piece 3 remains); B64/B65/B66 moved
from Open Items to Closed/Shipped; open count 11 → 8.

### Net New Files
None.

### Files (SHA-256, first 12 chars)
- `index.html` — `ba38463a8706`
- `e1c_check.js` — `f40924e4c4f6`
- `rules_assertions.py` — `18b90a74d74d`
- `pipeline_manifest.json` — `4a1b332d3fed`

## Backlog summary

- **Beginning (8 open):** B62, P2, P4, E21, E23, B60, E12, B17
- **Resolved (0 fully closed; E21 partially — pieces 1-2 of E21d shipped, piece 3 remains):** none
- **Added (0 new this session; B64/B65/B66 were logged last turn):** none
- **Ending (8 open):** B62, P2, P4, E21 (piece 3 only), E23, B60, E12, B17
