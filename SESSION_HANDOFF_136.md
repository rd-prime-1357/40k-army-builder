# Session 136 handoff — E21c/E22b shipped: forbid, allied unlock + points sub-cap, detachment Warlord ban

**Turn type: engine-only.** `index.html` **6.6 → 6.7**. Assertions **97/97 → 100/100**. Baseline
**22/22 at open → 23/23 at close** (the new gate is the 23rd). `detachment_effects.json` read as an
input and never edited (hash `e38c38dcef31` verified unchanged). Authoritative write-up is **D214**.

---

## Findings

**The three remaining effect kinds are now enforced, and one of them closed a live D0 violation.**
E21b had wired only `battleline`; `forbid`, `unlock` and `warlord` were unread by the engine. The
`unlock` case is the one that mattered most: the six Death Guard Plague Legions units B61 tagged were
sitting in the pool with no gate at all — freely addable under any detachment or none, no sub-cap,
Rotigus eligible as Warlord. The offer filter now hides them unless a detachment unlocks them, which
is the D0 leak D204 found, closed.

**All eleven S135 code/harness/manifest hashes matched at open.** The three doc mismatches
(`DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `NEXT_SESSION_PROMPT.md`) are the rolling docs D213
rewrote after the S135 handoff hash was captured — the addendum documents it. Not a bad sync.

**`e10_check.js` broke exactly as the prompt predicted.** It slices `duplicateUnit`, which now calls
`canAddUnitToList`, so it threw on the undefined helper. The E21c block was pulled into its slice
alongside the E21b one. `limit_check.js` did not break — it slices `unitLimit`, which E21c does not
touch. Repaired, not routed around.

---

## Decisions needed — one, and it is E21d's

**The stranded-allied case.** Deselecting or switching away from Tallyband Summoners while Plague
Legions units are in the list strands them: the engine rejects them (`offerableUnits`,
`canAddUnitToList`) but the roster shows no error, because rendering it is E21d's job, not this
engine turn's. **Recommendation: flag them as a visible error**, the same treatment the enhancement
over-state gets after a battle-size or detachment change — never a silent trim, and **not** by
blocking the deselect (that would contradict flag-don't-drop, a settled principle). Proceeding on that
recommendation into E21d, but it sets a precedent for how the tool treats a legal list a later
detachment change makes illegal, so **confirm the direction** before E21d builds it.

The **forbid already-in-list** call was directed by D204/the prompt (refuse, don't flag). The only
reversible choice left was *which* thing to refuse; chose to refuse the **detachment selection** with
a reason naming the unit, over auto-removing the player's unit. Recorded in D214, proceeded.

**D199's four batched calls remain unreviewed — since S127, now ten sessions.**

---

## Shipped / changed

**`index.html` — 6.6 → 6.7.** One marker-delimited `E21c / E22b` block, eight functions, no state of
its own — every answer derived live from `detachment_effects.json` and the current selection, the
discipline E21b set. `enforced:false` rows apply nothing. `forbiddenUnitNames` unions named units and
type-expanded units, removing `except_units` last so Be'Lakor survives; resolves to exactly fourteen
under Shadow Legion. `unlockedAlliedGroups` / `alliedPointsCap` / `alliedSubtotal` drive the offer
filter and the battle-size points sub-cap. `canAddUnitToList` is the add-path gate in E4b's
`{ ok, reason }` shape, layered on top of the count limit; `addRefusalText` renders the reason (a mute
refusal is a bug; polished prose is E21d's). `offerableUnits` removes forbidden and not-yet-unlocked
units from the roster. `detachmentForbidConflicts` refuses selecting a detachment over a forbidden
unit already present. `warlordBannedByDetachment` bars the allied group from Warlord (mode `cannot_be`
only; `must_be_if_present` stays Be'Lakor's unit flag, pinned by E21a-6).

Wired at six sites: the lightweight view carries `alliedGroup`; `renderRoster` offers through
`offerableUnits` and greys the sub-cap-spent card; `addUnitFromRoster` and both `duplicateUnit` pushes
(body and attached leader) go through `canAddUnitToList`; `toggleDetachment` consults
`detachmentForbidConflicts`; `eligibleWarlordEntries` filters on `warlordBannedByDetachment`.
`renderAll` already calls `recomputeWarlord`, so a toggle drops a now-ineligible Warlord live.

**`rules_assertions.py` — 97 → 100.** E21c-1 (the eight functions exist), E21c-2 (both add paths and
the roster offer route through the gate — honest that a third add path would not be caught), E21c-3
(the Warlord ban and the forbid-on-select refusal are wired to their call sites).

**`e21c_check.js` — net new.** 44 checks, seven sections: forbid resolves to fourteen with Be'Lakor
exempt; forbid gates offer + add and reverses on deselect; the already-in-list conflict (ghost
excluded); the unlock offer filter closing the D0 leak; the sub-cap arithmetic at **both** battle
sizes on one unit with a native unit shown not to count; the Warlord ban by group; and a synthetic
section for the two shapes no built row exercises (`must_be_if_present` must not ban; `enforced:false`
of every kind applies nothing).

**`e10_check.js`** — slice extended to include the E21c block. **`baseline.sh`** — `e21c_check`
registered as the 23rd gate. **`pipeline_manifest.py`/`.json`** — guarded set 40 → 41.

### Net New Files

* `e21c_check.js` — no file has played this role before.

---

## Files

Changed:

| File | SHA-256 (first 12) |
| --- | --- |
| `index.html` | `3d9a7673a764` |
| `rules_assertions.py` | `a9c3e8d2bdd7` |
| `e10_check.js` | `241905c39af4` |
| `baseline.sh` | `b13f1615e4f7` |
| `pipeline_manifest.py` | `5f833172d1a5` |
| `pipeline_manifest.json` | `c4b848e6721d` |
| `40K_Decision_Log_v3_0.md` | `762896f4e46b` |
| `DECISION_INDEX.md` | `910e4b194d95` |
| `OPEN_ITEMS_BACKLOG.md` | `30bd1ca2f6b0` |
| `NEXT_SESSION_PROMPT.md` | `0e1071db15cc` |
| `SESSION_HANDOFF_136.md` | *self* |

Net new:

| File | SHA-256 (first 12) |
| --- | --- |
| `e21c_check.js` | `240015e57809` |

**Repo custody.** All twelve are project-generated and repo-eligible. `e21c_check.js` names units and
detachments but reproduces no GW rules text. Excluded from any push as always: the Wahapedia CSV
export, the MFM `.txt` files, the faction web and pack files, `Army_Muster_Rules.txt` and
`wh40k_core_rules.md`.

## Backlog

**8 open:** B62, P2, P4, E21 (E21a/b/c shipped; E21d remains), E23, B60, E12, B17.

- Beginning tickets: B62, P2, P4, E21, E22, E23, B60, E12, B17 (9)
- Resolved tickets: E22 (E22b shipped; E22a was B61 — E22 closed)
- Added tickets: none
- Ending tickets: B62, P2, P4, E21, E23, B60, E12, B17 (8)
