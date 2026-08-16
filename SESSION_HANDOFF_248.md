# SESSION HANDOFF 248

**Turn type: data + engine.** B128 (D345) — Headhunter Task Force's capped Tank Ace selection.

## Session open

`./baseline.sh --fetch --data-turn`: **38/38 pass**, 85 source files verified against
`source_manifest.json`. Nothing was worked around.

S247's four changed files verified against a fresh clone before any work started, and every hash
matched the S247 handoff table — `rules_assertions.py`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`. `pipeline_manifest.json` was among what landed.

## What was found

Nothing beyond what the S247 handoff already flagged: `detachment_effects.json`'s six Headhunter
Task Force `tank_ace` rows were fully scoped (pool, cap, source citation, D273/S182) and needed
only an engine consumer and the `enforced` flip. No new discrepancy in the pool/cap facts turned up.

## Ryan's mechanism ruling

Asked before building, since this is a "how it works" product call: the Tank Ace keyword displays
on every qualifying Vehicle automatically (derived, never stamped onto the record); a checkbox in
the entry's own config panel, offered only to pool members, capped at 3 checked army-wide; checking
it is what grants Character (Enhancement + Warlord eligibility) — not a separate toggle. This is
the per-entry-field shape (`entry.tankAce`, listId-keyed, not detachment-keyed), matching how
`enhancement` already lives on the entry.

## What shipped

**`index.html`.** New `entry.tankAce` field, default false, never inherited on duplicate or
leader-copy (same rule `enhancement` follows). Persisted: SCHEMA_VERSION 3→4, migration adds
`tank_ace: false` to every existing entry on load, mirroring E4b's v2→v3 step exactly.

New E23/B128 block (own block, not folded into E21b's `effectiveUnitType` — that helper is
unit_name-keyed for uniform elevation across every entry of a name; this is listId-keyed, since two
entries of the same Vehicle can differ):
- `unitInTankAcePool(raw, keys)` — the only place the pool is computed; reads
  `detachment_effects.json`'s `target` shape directly rather than re-deriving it a second time
  (S247/D344's mirror-drift lesson, applied going forward rather than repeated).
- `entryTankAceActive(entry, keys)` — checked AND still in the pool under currently selected
  detachments. A checked-but-now-stale entry (detachment deselected) stays checked — S139,
  never silently discard a player's choice — but is inactive and flagged via `entryHasError`.
- `entryEffectiveType(entry, keys)` — 'Character' while active, else the entry's own `unit_type`.
  Threaded through `canAssignEnhancement`, the wrongType scan, `enhancementOfferedRowsForEntry`,
  `entryHasError`, and OR'd into `eligibleWarlordEntries`'s Character test.
- `canSetTankAce`/`setTankAce` — D0 gate: checking past the cap of 3 is refused at the click;
  unchecking is always allowed.

Keyword display: "Tank Ace" pill renders in both datasheet modals (`buildModalFull`,
`buildModalConfigured`) alongside real keywords, derived on every render — same convention as
Battleline's elevation (D204).

**`detachment_effects.json`.** All six Headhunter Task Force `tank_ace` rows flipped
`enforced: true`, `unenforced_reason` removed.

**`b128_check.js`** (new). 12 checks against the real engine functions: pool exclusions on both
except arms (Fly/Walker/Drop Pod via keywords, Fortification via unit_type), empty pool with no
detachment selected, cap gate refuses a 4th check but never an uncheck (including re-affirming an
already-checked entry against itself), staleness (checked-but-deselected goes inactive and frees
its cap slot, then reactivates on reselect with no re-click needed), the effective-type flip
driving `enhancementTypeEligible`, and the six shipped rows' `enforced`/`cap` facts. Wired into
`baseline.sh` and `pipeline_manifest.py`'s GUARDED list.

**`rules_assertions.py`.** New `E23-3` (all six rows carry `enforced:true`, `cap:3`, no stale
`unenforced_reason`). Updated `E21a-4`'s hard-pinned "unenforced inventory" fixture — previously
asserted the six Headhunter rows as the *only* permitted unenforced set; now asserts the set is
empty, since B128 was the last item on it. Updated `e1b_module_copies_agree`'s hard-pinned
`SCHEMA_VERSION` expectation from 3 to 4.

**Collateral fixes — two harnesses and one file had assumptions that no longer held once the entry
shape and SCHEMA_VERSION changed:**
- `list_store.js` had drifted from the newly-edited inlined copy in `index.html`, caught live by
  `E1b-2`'s byte-identity gate working exactly as designed. Resynced byte-for-byte; its
  schema-history header comment gained the v4/`tank_ace` note.
- `e1b_check.js`'s migration-chain test fixtures assumed the chain stopped at v3 (`Object.keys(up
  ).length === Object.keys(before).length + 1`, an explicit `schema_version === 3` "current
  version" case). Updated for the new v3→v4 step, added a v4-passthrough case, mirroring the
  existing v2→v3 pattern throughout.
- `e4b_check.js` and `e4c_check.js` both slice specific named blocks out of `index.html` via
  `new Function` rather than loading the whole file. B128 made `canAssignEnhancement` and
  `enhancementOfferedRowsForEntry` call `entryEffectiveType`, a function outside their existing
  slice — threw `ReferenceError` at harness load. Both now also slice the E23/B128 block and stub
  `rawUnits`/`detachmentEffects` as empty globals, which resolves to "never active" for every
  existing E4b/E4c fixture (correct — none of those fixtures involve Tank Ace).

**Backlog.** B128 moved Open → Closed/Shipped. The other 34 conferrals its original census found
(Heavy Transport ×6, Entrenched ×6, three faction keywords, Daemon/Soul Forge ×2) were out of
B128's scope from the start (D335: "eligibility or display inputs," not legality-critical).
**B134 opened** — scoping-only, S-sized, not D0 — so they aren't lost from the backlog now that
B128 closes. B134's own text flags the real open question: `detachment_effects.json`'s `_meta`
scopes the file to muster-time construction effects only, so whoever picks up B134 should confirm
these six actually affect list-construction legality before assuming they need an engine consumer
at all.

## Verified directly, not just through the gate

Re-ran `./baseline.sh --fetch --data-turn` after every fix: **38/38 pass**, including the new
`b128_check` gate. `python3 rules_assertions.py --tier all`: **129/129** (128 before B128's new
assertion, 129 after). Cap enforcement, staleness, and the effective-type flip were each exercised
directly by `b128_check.js` against the real `unitInTankAcePool`/`entryTankAceActive`/
`entryEffectiveType`/`canSetTankAce` functions, not a second implementation of them.

**Not verified this session:** no browser render check. The checkbox and keyword-pill HTML are
code-reasoned and covered by the harness's functional assertions, but nobody has looked at them on
screen.

## Files (SHA-256, first 12)

Verify these at S249 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | `2062d7b0bf8a` | entry.tankAce field; SCHEMA_VERSION 3→4 + migration; E23/B128 block; 4 enhancement-eligibility sites + eligibleWarlordEntries updated; Tank Ace checkbox + keyword pill rendering |
| `detachment_effects.json` | `44c8b343c8a0` | six Headhunter tank_ace rows: enforced:false→true, unenforced_reason removed |
| `rules_assertions.py` | `ac983aaa3916` | new E23-3; E21a-4 unenforced-inventory fixture now empty; e1b_module_copies_agree SCHEMA_VERSION 3→4 |
| `b128_check.js` | `0e7b88bded26` | **new file** — 12 checks against the real engine functions |
| `baseline.sh` | `001635e81194` | b128_check gate registered |
| `list_store.js` | `7ecc23cafa8a` | resynced to the edited inline copy in index.html; v4 schema-history note |
| `e1b_check.js` | `403f470d5a4d` | migration-chain fixtures updated for the v3→v4 step |
| `e4b_check.js` | `0c9904c64a9d` | loadEngine now also slices the E23/B128 block |
| `e4c_check.js` | `ee2fbecc2466` | loadEngine now also slices the E23/B128 block; rawUnits/detachmentEffects stubbed |
| `40K_Decision_Log.md` | `1b9f9196468e` | D345 appended |
| `DECISION_INDEX.md` | `7859dcded683` | D345 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `64d7340db1d5` | B128 moved Open → Closed/Shipped; B134 opened; 24 → 24 |
| `pipeline_manifest.py` | `b71e2d312fb8` | `b128_check.js` added to GUARDED; `SESSION_HANDOFF_248.md` registered |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_248.md` | (this file) | not self-referential; checked by `--freshness-check` |

## Ryan action required

- **Push this session's changed files** to the public repo: `index.html`, `detachment_effects.json`,
  `rules_assertions.py`, `b128_check.js` (new), `baseline.sh`, `list_store.js`, `e1b_check.js`,
  `e4b_check.js`, `e4c_check.js`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `SESSION_HANDOFF_248.md`, `NEXT_SESSION_PROMPT.md`.
- **`pipeline_manifest.json` must be included.**
- **A render check is needed this session** — engine turn, and the checkbox/keyword-pill UI has not
  been looked at on screen. Suggest: open a Space Marines list, select Headhunter Task Force, add a
  qualifying Vehicle, confirm the "Tank Ace" pill shows in the datasheet modal and the checkbox
  appears in the config panel; check it, confirm the Enhancement section and Warlord picker both
  pick the entry up; add three more qualifying Vehicles and confirm the 4th checkbox is disabled
  with a cap message; uncheck one and confirm it re-enables.

## Decisions resolved this session

D345 — B128's mechanism (Ryan's ruling on the two-part rule: automatic display keyword +
capped, checkbox-driven Character grant) and every technical choice under it (per-entry field
shape, staleness handling, block placement, assertion strategy).

## Backlog

24 open at S247 close; **24 open at S248 close**. Resolved B128; added B134. Net zero — B128's
closure and B134's opening are the same event (splitting the ticket into its shipped legality-
critical piece and its unshipped non-critical remainder), not independent backlog movement.
