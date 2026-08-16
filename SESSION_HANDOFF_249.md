# SESSION HANDOFF 249

**Turn type: data + engine.** B126 (D346) — Pactbound Zealots' Marks of Chaos.

## Session open

`./baseline.sh --fetch --data-turn`: **39/39 pass**, 85 source files verified against
`source_manifest.json`. Nothing was worked around.

All twelve S248 changed files verified against the fetched repo before any work started; every hash
matched the S248 handoff table — `index.html`, `detachment_effects.json`, `rules_assertions.py`,
`b128_check.js`, `baseline.sh`, `list_store.js`, `e1b_check.js`, `e4b_check.js`, `e4c_check.js`,
`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`. `pipeline_manifest.json` was
among what landed.

## Correction to S248's handoff

S248 records both its open and its close as **38/38**. Its close added `b128_check` as a new gate,
so the close figure should have read **39/39**. Nothing is broken — `baseline.sh`'s hash matched,
the gate list is intact, and this session opened at 39/39 having changed nothing. But S248's number
is wrong and must not be used as a comparison baseline. This session's figures are 39/39 at open and
**40/40 at close** (`b126_check` added).

## What was found

**The ticket was larger than it needed to be and smaller than it looked.** Re-derived from source
rather than carried from B126's text:

- Exactly **one** detachment of the 211 built records carries the rule —
  `Chaos Space Marines|PACTBOUND ZEALOTS`, Wahapedia `Detachment_abilities.csv` id `000008362` —
  and `detachments.json`'s own `armies` index offers it to Chaos Space Marines alone. Death Guard,
  Thousand Sons, World Eaters and Emperor's Children carry their god as a fixed faction keyword and
  reference marks nowhere. **There is no cross-faction arc here.**
- Of 58 CSM units: 8 EPIC HERO, 11 carrying an innate mark, **45 requiring a selection**.
- The 21 Chaos Daemons units carrying `HERETIC ASTARTES` are B114's Shadow Legion Thralls, in the
  Chaos Daemons army, unable to reach this detachment. Out of scope.
- Cypher and Vashtorr the Arkifane are Epic Heroes carrying no mark at all. Both have no Leader
  ability and an empty `leader_eligible_units`, so "a markless Character can never attach" is
  unreachable and needs no carve-out.

**The embark restriction cannot be built and is not an unenforced effect — it is an unrepresentable
one.** The engine has no transport-assignment model: "embark" appears nowhere in `index.html`, and
"transport" only as a `unit_type` string for limit doubling. There is no state to gate. Recorded on
the effect under a new `unmodelled_restrictions` shape rather than `enforced: false`, which would
have falsified `E21a-4`'s legitimately-empty unenforced inventory. **B135 opened.**

**B128's keyword reader is too narrow to reuse, and both extra fields are load-bearing.**
`unitInTankAcePool` reads only `keyword_names`. `HERETIC ASTARTES` lives in `faction_keyword_names`
on all 58 CSM units, and `Masters of the Maelstrom` has an **empty** `keyword_names` with
`EPIC HERO`, `CHAOS UNDIVIDED` and `PSYKER` all in `model_keyword_names` — a single-field read would
have demanded a mark it already carries. `markKeywordSet` unions all three and documents why it
differs.

**`e4b_check.js` and `e4c_check.js` both passed with a latent `ReferenceError` in place.**
`enhancementBearerEligible` now calls `entryEffectiveMark`, outside their existing slices, but no
existing fixture reaches a `kind: 'mark'` rule so nothing threw. Found by reading the call graph,
not by a red gate — the same failure S248 hit, which that time announced itself. Worth generalising:
**a slice-based harness passing is not evidence that its slice is complete.**

## Ryan's rulings

**1. Keyword scoping.** A unit is a `PSYKER` unit if ANY of its models carries `PSYKER`, the same
way a unit containing a Character model is a Character unit. The only unit in the pool where this
bites is **Dark Commune**, whose `PSYKER` sits on the `MINDWITCH` model alone; it cannot take
`KHORNE`. Four others carry `PSYKER` unit-wide (Sorcerer, Sorcerer In Terminator Armour, Master Of
Possession, Nemesis Claw). Five in total, asserted by name.

No extra case arises from an attached Psyker conferring `PSYKER` on its bodyguard: a Psyker can
never hold `KHORNE`, and the attach rule already requires matching marks, so a Khorne unit can never
acquire a Psyker leader.

**2. The attach is gated; a later mark change is not.** Claude's first build refused a mark change
that would leave an attached pair mismatched, on a strict D0 reading. Overruled: that forces a
detach-change-change-reattach dance to re-mark a pair. Re-marking is a two-step edit and the
intermediate step is an **incomplete configuration**, the same class as an unchosen mark or an
unchosen Daemonic Allegiance — flagged on both halves via `entryMarkPairError`, not forbidden. The
ATTACH is still refused outright, so a mismatched pair is only reachable by editing a pair that was
legal when made.

**The precedent, worth carrying forward: D0 forbids finished illegal armies, not intermediate steps
of a visibly-flagged multi-part edit.**

**3. Missing-mark fall-through is permissive** (D199) — accepted as proposed.

## What shipped

**`detachment_effects.json`.** New `mark_of_chaos` effect on
`Chaos Space Marines|PACTBOUND ZEALOTS`, `enforced: true`, carrying the five-mark vocabulary in
source order, the `Heretic Astartes` base keyword with all five marks plus `Epic Hero` in
`except_keywords`, the `Psyker → Khorne` exclusion, the attach restriction with its
attach-only enforcement note, and the embark rule under `unmodelled_restrictions`. `_meta` gains the
kind and the four new shapes.

**`index.html` — v6.25.** New `entry.mark` field (string or null). Persisted: SCHEMA_VERSION 4→5,
migration adds `mark: null` to every existing entry on load, mirroring the v3→v4 step. The field is
listId-keyed like `entry.tankAce`, but its *conventions* follow `entry.god` — **inherited** on
duplicate and leader-copy, absence is an entry error — because this is a required exclusive choice,
not an optional capped grant. B128's shape transferred only partly, as S248's sequencing note warned
it might.

New E29/B126 block: `markEffect`, `markKeywordSet`, `unitInnateMark`, `unitNeedsMark`,
`markOptionsForUnit`, `entryEffectiveMark`, `entryMarkStale`, `entryMarkMissing`, `markAttachBlock`,
`canSetMark`, `setMark`, `renderMarkSectionHtml`. Vocabulary, pool and exclusions are read out of the
data row, never as engine literals (S247/D344). `entryMarkPairError` sits with `entryHasError`.

`markAttachBlock` is applied at the bodyguard picker's filter and in `editLeaderTarget` — the same
two-point pattern `enhancementAttachBlock` uses. Kept separate from `canAttachLeader` rather than
folded in: that function is unit_name-keyed and cannot carry a per-entry mark, and folding it in
would have broken `e10_check.js`'s existing calls.

The four mark-restricted Pactbound Zealots enhancements (*Eye of Tzeentch*, *Intoxicating Elixir*,
*Orbs of Unlife*, *Talisman of Burning Blood*) enforce through a new `kind: 'mark'` in
`ENHANCEMENT_BEARER_RESTRICTIONS`, resolving via the same `entryEffectiveMark` — not a second
reading of the rule. B93's total resolver will subsume it.

Display: the mark selector renders with the Daemonic Allegiance chips (new `chosen-ChaosUndivided`
and `disabled` states added); only offerable options are rendered at all. The mark shows on the
roster sub-line for both leaders and bodyguards, and as a keyword pill in both datasheet modals —
derived on render, never stamped, same convention as Battleline (D204) and Tank Ace.

**`b126_check.js`** (new). The three-field pool reader including the `model_keyword_names`-only case,
detachment scoping, the Psyker/Khorne exclusion at unit and model level, innate marks, the attach
gate with permissive fall-through, D346's change-allowed asymmetry exercised end to end
(attach → change one half → both flag → change the other → both clear, no detach), staleness across
deselect/reselect, the four enhancements, and the shipped data facts. Its last section re-derives the
45/11 pool from the real `units.json` rather than asserting a remembered number. Wired into
`baseline.sh` and `pipeline_manifest.py`'s GUARDED list.

**`rules_assertions.py`.** New `E29-1` (coverage: the mark clause is scanned for across all 211
records, and each row's owning armies are checked against `detachments.json`'s index rather than
assumed from the key prefix), `E29-2` (the row's facts, including that the embark restriction is
recorded as unmodelled), `E29-3` (45/11 re-derived from `units.json`, sets disjoint, no pool unit
left with zero selectable marks, 5 Psyker-barred including Dark Commune by name), `E29-4` (harness
gate). `e21a_schema_valid` learns the `mark_of_chaos` kind; its two new checks are the ones that
catch a silently unsatisfiable table — every mark must also appear in `except_keywords`, and no
per-keyword exclusion may bar every option. `e1b_module_copies_agree`'s pinned `SCHEMA_VERSION`
4→5.

**Collateral.** `list_store.js` resynced byte-for-byte to the edited inline copy; its schema-history
header gained the v5 note **and the v4 note S248 shipped the bump without writing**.
`e1b_check.js`'s migration-chain fixtures updated for the v4→v5 step with a v5-passthrough case.
`e4b_check.js` and `e4c_check.js` each gained the E29 slice (see findings above).

**Backlog housekeeping.** Three closed-pointer stubs (B111, B89, B100) were sitting in the Open Items
section, which the section's own rule forbids. Removed; B100's pointer moved to Closed / Shipped
since its full body was not already there. The recorded counts were never wrong, but a `^### ` grep
inside the section returned 27 against a stated 24 — exactly the sort of mismatch that invites an
explanation instead of a check.

## Verified directly, not just through the gate

`./baseline.sh --fetch --data-turn` after every fix: **40/40 pass**, including the new `b126_check`
gate. `python3 rules_assertions.py --tier all`: **133/133** (129 before, plus E29-1..E29-4). The pool counts, the Psyker exclusion, the attach gate and D346's asymmetry
were each exercised against the real engine functions, not a second implementation.

**Not verified this session:** no browser render check. The mark selector, the roster sub-line and
the two modal pills are code-reasoned and covered functionally, but nobody has looked at them on
screen. **This is now two engine turns in a row with no render check** — S248's Tank Ace UI is still
unseen too.

## Files (SHA-256, first 12)

Verify these at S250 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | `4244cde82174` | **v6.25.** entry.mark; SCHEMA_VERSION 4→5 + migration; E29/B126 block; entryMarkPairError; attach gate at picker + editLeaderTarget; four `kind:'mark'` bearer rows; selector, roster sub-line and both modal pills; v4/v5 schema-history notes |
| `detachment_effects.json` | `df50dd86fe53` | new mark_of_chaos row on Pactbound Zealots; `_meta` gains the kind and four shapes incl. `unmodelled_restrictions` |
| `rules_assertions.py` | `ac98e6b4bd86` | E29-1..E29-4; `e21a_schema_valid` learns mark_of_chaos; `e1b_module_copies_agree` pin 4→5 |
| `b126_check.js` | `86535a8417d0` | **new file** — behaviour gate for the whole mark rule |
| `baseline.sh` | `83270f9f34fc` | b126_check gate registered |
| `list_store.js` | `fc3a210e0838` | resynced to the edited inline copy; v4 + v5 schema-history notes |
| `e1b_check.js` | `cf8dfb7d6915` | migration-chain fixtures updated for the v4→v5 step |
| `e4b_check.js` | `e547004f6f1d` | loadEngine now also slices the E29/B126 block |
| `e4c_check.js` | `678da7a3b66d` | loadEngine now also slices the E29/B126 block |
| `40K_Decision_Log.md` | `92d9ceaf5b8b` | D346 appended |
| `DECISION_INDEX.md` | `0a32e95faa96` | D346 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `5b1656f89310` | B126 moved Open → Closed/Shipped; B135 opened; three closed stubs removed from Open Items; 24 → 24 |
| `pipeline_manifest.py` | `ce053f403455` | `b126_check.js` added to GUARDED; `SESSION_HANDOFF_249.md` registered |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_249.md` | (this file) | not self-referential; checked by `--freshness-check` |

## Ryan action required

- **Push this session's changed files** to the public repo: `index.html`, `detachment_effects.json`,
  `rules_assertions.py`, `b126_check.js` (new), `baseline.sh`, `list_store.js`, `e1b_check.js`,
  `e4b_check.js`, `e4c_check.js`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `SESSION_HANDOFF_249.md`, `NEXT_SESSION_PROMPT.md`.
- **`pipeline_manifest.json` must be included.**
- **A render check covering BOTH S248's and this session's UI.** Two engine turns have now shipped
  unseen. Suggested run, one list: create a Chaos Space Marines list, select **Pactbound Zealots**,
  add Legionaries and a Chaos Lord. Confirm both show "! Choose Mark of Chaos" and a five-chip
  selector. Pick Khorne on both, attach the Lord — the attach should be offered. Change the
  Legionaries to Nurgle: the change must be **allowed**, and both entries must then flag the
  mismatch. Change the Lord to Nurgle and confirm both clear with no detach. Add a **Dark Commune**
  and confirm only four chips render, with Khorne absent. Add **Khorne Berzerkers** and confirm no
  selector appears and "Khorne" shows on its roster line. Deselect Pactbound Zealots and confirm the
  picks are kept but flagged; reselect and confirm they revive with no re-click. Then the S248 Tank
  Ace pass per that handoff's steps.

## Decisions resolved this session

D346 — B126's population, the mark mechanism, Ryan's two rulings (Psyker keyword scoping; attach
gated but a later mark change allowed), and the embark restriction's reclassification from
unenforced to unrepresentable.

## Backlog

24 open at S248 close; **24 open at S249 close**. Resolved B126; added B135. Net zero — B126's
closure and B135's opening are the same event (splitting the ticket into its shipped half and the
half that needs a feature the app does not have), not independent backlog movement.
