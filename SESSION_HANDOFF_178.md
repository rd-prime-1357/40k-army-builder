# Session handoff — Session 178

**Turn type:** engine-only (E26 shipped). `index.html` v6.12 → v6.13, `rules_assertions.py` +1
assertion, `pipeline_manifest.json` reissued. No data or tooling work.

## 1. Session open

- Baseline green with `--fetch`: **25/25 gates** (3 tier-B skipped, correct — engine turn, no
  `--data-turn`), 74/74 tier-A assertions. Repo newest handoff was 177, matching the project area —
  no staleness gap. `40K_Decision_Log.md` missing from the `/mnt/project` mount listing again (same
  recurring pattern as S177); content confirmed correct via clone, no action needed.
- D268 confirmed via clone — all session-prompt claims verified against the actual decision log text.
- Source data verified against D268's legality-case requirements before coding:
  - All 14 Support-typed units checked: 12 SM/chapter Supports with named `co_leader_eligible_with`
    lists, plus 2 bare Supports — Master Of Executions (CHARACTER, empty list) and Masters of the
    Maelstrom (non-CHARACTER, empty list).
  - All 6 DG Plague characters confirmed Leader-typed with `co_leader_any: true`.
  - Huron Blackheart confirmed as the sole Leader whose `leader_eligible_units` names another
    attach-capable character (MotM) — no other such cross-reference exists across all 16 built factions.
  - MotM confirmed non-CHARACTER (empty `keyword_names` list, `unit_type: "Other"`).

## 2. What shipped (D269)

**`permitsCoLeader` rewritten** with the four D268 requirements, building on the existing D157
cap-of-2 + `canAttachLeader` machinery:

- **R1 (bare CHARACTER Support → any Leader):** A Support with the CHARACTER keyword and an empty
  `coLeaderWith` list pairs with any Leader by the base rule. Fixes MoE and all future bare CHARACTER
  Supports.
- **R2 (DG second-Leader):** Two Leaders allowed only when at least one has `coLeaderAny`. Same
  datasheet still refused (line 1 of the function).
- **R3 (Leader cross-reference):** A non-CHARACTER Support (MotM: no CHARACTER keyword, empty
  `coLeaderWith`) can only pair via a Leader whose `leaderEligible` names it. Only Huron qualifies.
- **R4 (same-type cap):** Two Supports always refused. Two Leaders refused unless R2 applies. This
  actively overrides the stale Apothecary→Lieutenant `co_leader_eligible_with` cross-listing.
- **Named-list restriction preserved:** A Support with a non-empty `coLeaderWith` (Lieutenant,
  Apothecary, Cato, Ancient variants, etc.) can only pair with units named in that list — the
  datasheet combination restriction, not dead data.

**`leaderAbilityName` added to the `allUnits` view object** (read from `mg.leader_ability_name`;
values: "Leader", "Support", or null for non-leader units). The `isCharacter` field (already on the
view object, derived from the CHARACTER keyword) is what distinguishes MoE (CHARACTER Support → R1
path) from MotM (non-CHARACTER Support → R3 path).

**Assertion E26 added** — two-part check:
- Part A: 9 structural shape fragments in `permitsCoLeader`'s source code (leaderAbilityName checks,
  isCharacter base-rule path, leaderEligible cross-reference, coLeaderWith named-list, coLeaderAny,
  same-type refusals) plus confirmation `leaderAbilityName` is wired into `setActiveUnits`.
- Part B: 10 legality cases modeled in Python against actual unit data, all tested with symmetry:
  Captain+Lieutenant (legal), Lieutenant+Librarian (illegal), Lieutenant+Apothecary (illegal),
  Cato+Captain (illegal), Cato+Calgar (legal), MoE+Captain (legal), Huron+MotM (legal),
  MotM+Captain (illegal), Noxious Blightbringer+Foul Blightspawn (legal), same datasheet (illegal).

**75/75 tier-A assertions pass (112 total including 37 tier-B skipped).**

## 3. Decisions still waiting on Ryan

- **B70 (Wardens of Ultramar)** — unchanged. MFM tags it `SUPPORT` with six units; the printed ability
  ("Heroes of Ultramar", join one of three named units + raise Starting Strength) is a bespoke mechanic,
  not the Support attach ability. Carved out of B73, empty list, awaiting Ryan's reconcile. Not touched
  this session.

## 4. Files

| File | Status | SHA-256 (first 12) |
|---|---|---|
| `index.html` | v6.12 → v6.13 (E26 engine) | `c981bd181ff2` |
| `rules_assertions.py` | +1 assertion (E26), +1 function (`e26_co_attach_stacking`) | `295f8c0e0d43` |
| `pipeline_manifest.json` | reissued at close (131 guarded files) | `7c3e94dbde16` |
| `40K_Decision_Log.md` | D269 appended | `06197e9f121c` |
| `DECISION_INDEX.md` | D269 index entry added | `4250aaaf2f76` |
| `OPEN_ITEMS_BACKLOG.md` | E26 → Closed/Shipped; count 13 → 12 | `b3dbb328c56b` |
| `NEXT_SESSION_PROMPT.md` | overwritten (S179) | `6cc02256c00c` |
| `SESSION_HANDOFF_178.md` | new (rolling) | — |

No GW-derived material in this set — all files are project docs and engine code. No data file changed.

## 5. Backlog

- **Beginning:** 13 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, E26, E27
- **Resolved:** E26
- **Added:** none
- **Ending:** 12 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, E27
