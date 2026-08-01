# Session handoff — Session 181

**Turn type:** Analysis-only (D272). E23 scoped from source; no engine, no data, no `index.html`
change. No ticket shipped.

## 1. Session open

- Read `SESSION_HANDOFF_180.md` and `NEXT_SESSION_PROMPT.md` first. The prompt pointed to D209 for
  E23's original filing and asked for a decision on "a sixth `detachment_effects.json` effect kind" —
  neither number was trusted without checking; see §2.
- Baseline run with `--fetch`: clean, 25/25 gates pass (3 tier-B skipped, sources not loaded — correct
  for an analysis-only session; no `--data-turn` requested or needed). `fetch-verify` pulled 58
  overlay-needed files from the repo, including `40K_Decision_Log.md`, which the project-area mount did
  not have resident at session start.

## 2. What shipped (D272)

**Corrected the S181 prompt's "sixth effect kind" claim.** `detachment_effects.json`'s live `_meta`
block and all 9 built entries carry exactly four kinds — `battleline`, `forbid`, `unlock`, `warlord` —
matching D204's four-kind schema. D209 (S134) called Headhunter Task Force a *fifth*-kind candidate;
nothing shipped a fifth kind between then and now. If built as a schema addition, Tank Ace's grant is
the fifth kind.

**The load-bearing finding: E4 and E9 test Character status two structurally different ways, and
neither has a per-list-entry hook — which Tank Ace's grant requires.**
- E9 (`isCharacter`, read by `eligibleWarlordEntries()`) is computed once per unique `unit_name` in the
  faction's unit index (off `keyword_names`) and shared by every copy of that name in the list.
- E4 (`enhancementTypeEligible`, three call sites — index.html ~3194, ~3375, ~3689) reads the raw
  `unit_type` field, copied onto the list entry at six separate construction sites, and never through
  `effectiveUnitType()` — D204's overlay function, which exists only for the blanket battleline grant
  and is not consulted anywhere in the enhancement code path.

Tank Ace's grant is up to **three player-picked instances**, not every copy of a name and not a
detachment-wide blanket — the shape neither existing mechanism represents. A data-only fix (append
"Character" to a unit's keyword list, or extend `effectiveUnitType()`'s blanket pattern) would either
elevate every copy of the vehicle army-wide or allow no player choice at all. Checked for a data
conflict this creates: none of the 28 `Vehicle`-type units in the generic Adeptus Astartes block are
already `unit_type: Character`, so no overlap case exists to reconcile.

**Mechanism decided (dev-manager call, reversible):**
1. A new declarative `detachment_effects.json` kind carries the detachment-scoped static facts —
   eligible unit_types/exceptions and the count cap (3) — the same shape `unlock`'s numeric
   `points_cap` field already uses.
2. The player's actual picks are new, purely-additive `list_store.js` state: an array of `listId`s,
   capped at the detachment's grant. Added the same way `warlord_entry_id` (v1) and `force_disposition`
   (v3) were — absence reads as "none elevated," exactly what an older record already meant, so **no
   schema version bump**.

**Storage/reset behaviour decided by existing precedent, not escalated to Ryan.** Both sub-questions
the S181 prompt flagged as possibly needing a product call turned out not to be ambiguous once checked
against two already-shipped mechanisms:
- *Does the selection reset on faction change / detachment deselect?* Continuous re-validation, the
  same shape as `recomputeWarlord()` — any picked `listId` that stops being eligible is silently
  dropped on every recompute, no confirmation dialog.
- *Can it be changed after Muster?* Checked whether the app models a Muster phase at all — it does not;
  `index.html` mentions "Muster" only inside rules-citation comments, never as a modelled step. Picks
  stay editable continuously, identical to Warlord and Enhancement selection today.

**Engine touch points identified for the build turn** (not built this session): `eligibleWarlordEntries()`
needs an OR against the new per-entry pick array alongside the existing `x.unit.isCharacter` test;
`canAssignEnhancement`/`enhancementTypeEligible`'s three call sites need an effective per-entry type
(raw `unit_type`, or `'Character'` when the entry's `listId` is a live pick) in place of the raw field —
mirroring `effectiveUnitType()`'s "compute an overlay, never touch the raw record" shape, but at
per-entry rather than per-detachment granularity, since no existing function does that today.

**Still blocked on a data turn, correctly not run this session** (turn-typed analysis-only; sources
were not loaded — `--data-turn` was neither requested nor needed for a scoping-only turn). Per D209's
own source-first standard, the exact keyword-grant wording needs confirming across all six armies
(Space Marines, Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves) before a build
turn starts — the "most Vehicles" carve-out's exact membership, and whether wording (including the
"up to three" cap) is identical across all six, is unconfirmed rather than assumed.

`index.html` stays at whatever version S180 left it (this session touched no engine file). Baseline
re-run after doc edits, `--no-repo` (local edits not yet pushed): 25/25 gates pass, 3 tier-B skipped —
unaffected, as expected for an analysis-only session.

## 3. Decisions still waiting on Ryan

- **B70 (Wardens of Ultramar)** — unchanged. Decided S175 (D266) to build the join/Starting-Strength
  mechanic; still needs a scoping turn before a build session. Not touched this session.

Nothing from E23's scoping needed Ryan this session — both sub-questions the prior prompt flagged as
possibly product-facing were resolved by existing precedent (see §2) and are recorded, not asked.

## 4. Process notes

Appended `SESSION_HANDOFF_181.md` to `pipeline_manifest.py`'s `GUARDED` list this session (136 guarded
files), per the S181 prompt's explicit instruction and D271's design — routine per-session close
bookkeeping, not a tooling-turn change to the checking logic itself.

## 5. Files

| File | Status | SHA-256 (first 12) |
|---|---|---|
| `40K_Decision_Log.md` | D272 appended | `82a0e60ff57b` |
| `DECISION_INDEX.md` | D272 index entry added | `c9f312ece6d5` |
| `OPEN_ITEMS_BACKLOG.md` | E23 ticket body rewritten with scoped plan; changelog entry added | `95c3b5214885` |
| `pipeline_manifest.py` | `SESSION_HANDOFF_181.md` added to `GUARDED` (136 guarded files) | `7a5c2b8adf79` |
| `pipeline_manifest.json` | reissued at close (not self-guarded — cannot guard itself) | `69fd0eaad1c1` |
| `NEXT_SESSION_PROMPT.md` | overwritten (S182) | `a2c28c30da4d` |
| `SESSION_HANDOFF_181.md` | new (rolling) | — |

No GW-derived material in this set — all files are project docs and pipeline tooling. No data file,
engine file, or `index.html` changed this session.

## 6. Backlog

- **Beginning:** 11 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17
- **Resolved:** none (scoping turn, no ticket closed)
- **Added:** none
- **Ending:** 11 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17
