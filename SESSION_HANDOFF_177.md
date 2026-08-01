# Session handoff — Session 177

**Turn type:** analysis-only (scoping). No code, no data, no `index.html` change. Nothing shipped
but the four close-out documents.

## 1. Session open

- Baseline run green with GW sources loaded: **29/29 gates**, 111/111 assertions, all three repro
  rebuilds (`unit_loadouts.json`, `units.json` + four merged lookups, `detachments.json`)
  byte-identical, 70 source files verified against `source_manifest.json`, repo custody clean.
- Repo newest handoff was 176, matching the project area — no staleness gap. Decision log present
  this session and identical to the repo copy.
- Opened as the E26 engine turn. The scoping pass turned into a source investigation because the
  S176 handoff implied a CSM data dependency that needed checking before any engine code.

## 2. What this session established (E26 re-scoped — D268)

The headline: **E26 is engine-only with no data dependency, and the CSM "data gap" does not exist.**
Everything below was derived from source this session (Wahapedia CSVs + MFM), not from inherited prose.

- **The real defect is in the engine, not the data.** `permitsCoLeader` (index.html 4271) returns
  false for a bare Support — empty `coLeaderWith`, `coLeaderAny` false — against every Leader. So
  Master of Executions and the whole SM Support family can attach as a *sole* leader but cannot
  co-attach today. No data flag fixes this; being Support must itself grant the pairing, in the engine.

- **The legality model is layered.** Base rule (one Leader slot + one Support slot, two total — already
  the D157/D158 cap) is the ceiling. The datasheets decide which pairings are legal within it, in three
  shapes: a **named list** on a Support (`co_leader_eligible_with` — Lieutenant → Captain/Chapter-Master
  rank, Cato → Calgar); a **generic flag** (`co_leader_any` — the six DG Plague characters = "second
  Leader"); and a **leader-rule cross-reference** where a Leader's own eligible list names an
  attach-capable character (**Huron Blackheart → Masters of the Maelstrom — the only such cross-reference
  in all 16 built factions**). Two Supports on one bodyguard is illegal by the base rule (Ryan's call),
  and the engine must actively refuse it because the legacy 10th-ed name lists cross-reference each other
  (Apothecary's list names Lieutenant) and would otherwise wave it through.

- **MoE's type is already governed — not a new decision.** The Wahapedia datasheet heads MoE's ability
  `LEADER`; the MFM types it `SUPPORT`; MoE was one of the 14 Leader→Support flips B73 shipped. D192 +
  D267 ("MFM is authoritative wherever both exist") settle it: **MoE is SUPPORT.** Its footer was
  correctly cleared by B73 (Support units don't carry the stale Leader clause).

- **Full CSM source pass:** only two CSM datasheets carry a co-attach footer — Master of Executions and
  Exalted Champion, both the generic "one other CHARACTER" shape. Exalted Champion is **not built** (no
  MFM points → never merged). MoE is correctly typed with a cleared footer. So **the CSM attach data is
  already right; there is nothing to regenerate.** The deferred D144 CSM `co_leader_any` population is
  resolved-as-unnecessary, verified from source.

- **Three of my own proposals were corrected against source during the session** (all logged in D268):
  (a) discarding the `co_leader_eligible_with` name lists as "dead" — wrong; they are the datasheet
  combination restriction. (b) adding MotM to Huron's `co_leader_eligible_with` — wrong; the MFM already
  carries it in Huron's `leader_eligible_units`, an engine read not a data change. (c) setting
  `co_leader_any = true` on MoE — wrong; being Support already grants the any-Leader pairing, and the
  flag would be the Leader reading that D267 discards.

## 3. E26, as re-scoped — the next engine session

Engine-only, `index.html` + `rules_assertions.py`. Builds on the D157 cap-of-2 + `permitsCoLeader`
machinery; does not replace it. Four requirements, each to land as an executable assertion:

1. A **Support-typed unit pairs with any single Leader** by the base rule — empty `coLeaderWith`, no
   `coLeaderAny` still permits it into the Support slot alongside one Leader. Fixes the bare-Support
   false.
2. Keep the **DG `co_leader_any` second-Leader path** — a Leader with the flag can be a second Leader,
   never two of the same datasheet.
3. Read a **Leader's `leader_eligible_units` naming an attach-capable character** as a co-attach permit
   (Huron → MotM). Narrow: it is the only such cross-reference in the whole build, so no risk of firing
   elsewhere.
4. **Same-type cap** — two Supports, or two Leaders without a `co_leader_any` lift, cannot stack, even
   when the legacy name lists cross-reference each other.

Legality cases to assert against, drawn from built data: Captain + Lieutenant (legal, Leader+Support);
Lieutenant + Librarian (illegal — Librarian not in Lieutenant's Captain-rank list); Lieutenant +
Apothecary (illegal — two Supports); Cato + anyone-but-Calgar (illegal); MoE + any one Leader (legal);
Huron + MotM (legal — via Huron's leader rule); MotM + any other Leader (illegal); two DG Plague Leaders
(legal, ≤2, not same datasheet); two of the same datasheet (always illegal).

## 4. Decisions still waiting on Ryan

- **B70 (Wardens of Ultramar)** — unchanged. MFM tags it `SUPPORT` with six units; the printed ability
  ("Heroes of Ultramar", join one of three named units + raise Starting Strength) is a bespoke mechanic,
  not the Support attach ability. Carved out of B73, empty list, awaiting Ryan's reconcile. Not touched
  this session.

## 5. Files

| File | Status | SHA-256 (first 12) |
|---|---|---|
| `40K_Decision_Log.md` | D268 appended | `d0dffd049861` |
| `DECISION_INDEX.md` | D268 index entry added | `1bc85c1c2ee5` |
| `OPEN_ITEMS_BACKLOG.md` | E26 re-scoped in place; S177 count line (13 → 13) | `d01f91f5609b` |
| `NEXT_SESSION_PROMPT.md` | overwritten (S178 — E26 engine) | `5244be5d2d9e` |
| `pipeline_manifest.json` | reissued at close (131 guarded files) | `a384f1941920` |
| `SESSION_HANDOFF_177.md` | new (rolling) | — |

No code, data, or `index.html` changed this session. No GW-derived file is in this set; all are project
docs. No `pipeline_manifest` reissue — no guarded file changed.

## 6. Backlog

- **Beginning:** 13 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, E26, E27
- **Resolved:** none
- **Added:** none
- **Ending:** 13 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, E26, E27

(E26 re-scoped in place — engine-only, no data dependency — not resolved and not re-added, so the count
holds at 13.)
