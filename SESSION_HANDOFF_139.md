# Session Handoff 139

## Baseline at open

Four of S138's seven Files-section hashes verified byte-identical (`convert_to_json.py`,
`units.json`, `rules_assertions.py`, `pipeline_manifest.json`). The other three — the decision log,
`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md` — differed because **D217 was appended after S138's
handoff was written**; confirmed by reading D217, which matches what `NEXT_SESSION_PROMPT.md` already
recorded. Not a reconciliation problem. Full baseline ran clean, 23/23, assertions 101/101, before
any new work.

**Mount version note:** `index.html` was at **6.8** at open, not the 6.3 an old memory note implied —
the handoff chain is authority, as the standing rule says. Built on 6.8.

## Product decision confirmed at open

Ryan confirmed D214's recommendation for E21d piece 3: a unit made illegal by a later change stays
in the list as a **visible roster error**, never silently trimmed and never blocked from the deselect
that stranded it. His reasoning — a player may switch a detachment briefly to check something and
switch straight back, so the list must survive the round-trip — and he extended the ruling: the same
treatment is the tool's standing answer for the whole "was-legal, a-later-choice-made-it-illegal"
class, enhancement over-states included. This was the lasting-precedent call the ticket was held for.

## What shipped — E21d piece 3 (E21 closes)

**Turn type: engine (`index.html` only).** No data, parser, or CSV touched.

`entryAlliedError(unit)` added at the end of the E21c/E22b block (so `e21c_check.js` can drive it
against the real table and pool) and wired into `entryHasError`. It returns true in three cases, all
the same over-state shape:
- the unit's allied group is no longer unlocked by any selected detachment (`alliedPointsCap` -> null)
  — the core Tallyband-Summoners-deselected case;
- the group is unlocked but over its points sub-cap for the current battle size
  (`alliedSubtotal > cap`) — reachable by dropping battle size; **every** member of the over-cap
  group is flagged, not one arbitrary victim;
- the unit is forbidden by a selected detachment (`forbiddenUnitNames`) — reachable only by import;
  flagging it closes a small D0 visibility gap.

No new render path was needed: the existing `has-error` class and `!` flag on the roster row (main-unit
and attached-leader paths both) already flow from `entryHasError`, so making the predicate return true
is the entire change — deliberately the identical treatment the enhancement over-state already gets.

**Assertion.** New `E21d-1` pins the wiring: `entryAlliedError` must exist and `entryHasError` must
call it, so dropping either fails loudly. 101 -> 102 assertions.

**Harness.** `e21c_check.js` gains Section 8, driving all three branches against the real Tallyband
Summoners and Shadow Legion rows and the real pool — each a state that passes an on-state test and
fails only after a later toggle or battle-size change.

`pipeline_manifest.json` reissued for the three changed guarded files (`index.html`, `e21c_check.js`,
`rules_assertions.py`). Full baseline 23/23, assertions 102/102. **E21 closes**; backlog 7 -> 6.

## B60 investigated (nothing changed) — it is bigger than the ticket

While confirming the open branch, B60 was diagnosed and found to be more than the field-relabel it's
written as. Recorded in full in `NEXT_SESSION_PROMPT.md` so it isn't re-derived: the parser's header
detection is failing on four `rule_text` cases where `RESTRICTIONS` is actually present in source, and
two `restrictions` records (Dark Angels LION'S BLADE TASK FORCE, WRATH OF THE ROCK) are independently
corrupted. It's a parser turn worth a stronger model, not a mechanical relabel. No file touched for it
this session.

## Decisions needed

None blocking. E21 is closed. Next session is P4 step 2 (capacity lever) per the sequencing.

## Shipped / changed

`index.html` — `entryAlliedError` added, wired into `entryHasError`; 6.8 -> 6.9. `e21c_check.js` —
Section 8 + one export. `rules_assertions.py` — new `E21d-1` (102/102). `pipeline_manifest.json` —
reissued. `40K_Decision_Log_v3_0.md` — **D218** appended. `DECISION_INDEX.md` — D218 indexed.
`OPEN_ITEMS_BACKLOG.md` — E21 moved to Closed/Shipped, header 7 -> 6. `NEXT_SESSION_PROMPT.md` —
rewritten for S140.

### Net New Files
None.

### Files (SHA-256, first 12 chars)
- `index.html` — `19362f8a573d`
- `e21c_check.js` — `a62c4b8ecc02`
- `rules_assertions.py` — `8130862ea8dc`
- `pipeline_manifest.json` — `f5ac9bce809f`
- `40K_Decision_Log_v3_0.md` — `7d99bf499e25`
- `DECISION_INDEX.md` — `d9b19cdab039`
- `OPEN_ITEMS_BACKLOG.md` — `81be8c822b57`
- `NEXT_SESSION_PROMPT.md` — `83727b352c97`

## Backlog summary

- **Beginning (7 open):** P2, P4, E21 (piece 3 only), E23, B60, E12, B17
- **Resolved (1 fully closed):** E21 (D218) — piece 3 shipped, closing the arc
- **Added (0 new this session):** none
- **Ending (6 open):** P2, P4, E23, B60, E12, B17
