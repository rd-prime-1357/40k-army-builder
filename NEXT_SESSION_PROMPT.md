# Next-session prompt — Session 178

**Assigned: E26 — enforce one-Leader-one-Support stacking, engine-only (D268 re-scope).** This is an
**engine turn** in `index.html` + `rules_assertions.py`. It is **analysis-typed** — a wrong judgment
ships an illegal-list-reachable bug against D0 — so flag model/effort at open and let Ryan switch before
you write engine code. No data or tooling work; do not mix turn types. **13 open items.**

## Open at session start

Read `SESSION_HANDOFF_177.md` first, then **D268** in `40K_Decision_Log.md` (the E26 re-scope), then
D267 (B73, the data half). Do not trust any session/version/decision number from memory; the handoff
chain and the decision log are the only authorities. **S177 corrected three assumptions against source
mid-session — re-derive from source, do not build from remembered framing.**

**Verify you are not opening against a stale project area** — clone the repo and compare its newest
`SESSION_HANDOFF_*.md` against the project area before trusting the mount. Prior sessions found
`40K_Decision_Log.md` missing from the mount entirely (content fine, verified via clone). If that
recurs, ask Ryan for a file-list screenshot rather than re-diagnosing. Ryan deletes old handoffs as
routine housekeeping — their absence is expected, not data loss.

Run the full baseline: `./baseline.sh --fetch`. **E26 is engine-only — `--data-turn` is not needed**
(no MFM/source parsing; the CSM data is already correct, verified S177). Expect **111** rules
assertions including `B73`, and **29/29** gates if you do load sources. Reconcile any failing gate
before starting — never work around it.

## E26 — the build

S177 (D268) re-derived the whole thing from source. The CSM "data gap" the older prompt implied **does
not exist** — Master of Executions is correctly typed Support with a cleared footer, and no built CSM
unit needs a data change. The real defect is engine: `permitsCoLeader` (index.html 4271) returns false
for a bare Support (empty `coLeaderWith`, `coLeaderAny` false) against every Leader, so Support units
can attach only as a sole leader, never co-attach.

Build on the existing D157 cap-of-2 + `permitsCoLeader` machinery — extend, don't replace. Four
requirements, each landing as an executable assertion in `rules_assertions.py`:

1. **Support pairs with any single Leader** by the base rule. A Support-typed unit fills the Support
   slot and co-attaches with any one Leader even with an empty `coLeaderWith` and no `coLeaderAny`.
   This is the core fix. Read `leader_ability_name` off the unit view object — note it is **not**
   currently on `allUnits` (index.html ~2290 builds the view object without it), so adding it to the
   view object is part of the work.
2. **Keep the DG `co_leader_any` second-Leader path.** A Leader with `co_leader_any` (the six DG Plague
   characters) can be a second Leader, never two of the same datasheet.
3. **Leader-rule cross-reference as a co-attach permit.** When a Leader's own `leader_eligible_units`
   names an attach-capable character, that is the co-attach grant — **Huron Blackheart → Masters of the
   Maelstrom**, the *only* such cross-reference across all 16 built factions (verified S177). MotM's own
   sheet carries no self-grant, so Huron is the sole Leader it can share a unit with.
4. **Same-type cap.** Two Supports, or two Leaders without a `co_leader_any` lift, cannot stack — even
   when the legacy 10th-ed `co_leader_eligible_with` lists cross-reference each other (Apothecary's list
   names Lieutenant). This is the one place the base rule must actively override a stale name-list
   overlap.

**Do not discard the named `co_leader_eligible_with` lists** — they are the datasheet combination
restriction (Lieutenant → Captain/Chapter-Master rank; Cato → Calgar), not dead data. Ryan's principle:
the base rule sets the ceiling; the unit rules govern which combinations are legal within it.

### Legality cases to assert (all from built data)

- Captain + Lieutenant — **legal** (Leader + Support).
- Lieutenant + Librarian — **illegal** (Librarian not in Lieutenant's Captain-rank list).
- Lieutenant + Apothecary — **illegal** (two Supports).
- Cato Sicarius + any Leader but Marneus Calgar — **illegal**.
- Master of Executions + any one Leader — **legal** (bare Support, base rule).
- Huron Blackheart + Masters of the Maelstrom — **legal** (Huron's leader rule names MotM).
- Masters of the Maelstrom + any other Leader — **illegal** (no self-grant; only Huron).
- Two DG Plague characters (different datasheets) — **legal** (≤2, `co_leader_any`).
- Two of the same datasheet — **always illegal**.

Publish the index at a bumped version and state the version in the report.

## After E26

- **E27 (UI)** — the popup/output Leader-vs-Support wording (heading hardcodes "Leader" at index.html
  6568). Separate UI turn; do not fold into E26.
- **B70 (Wardens of Ultramar)** — still open, still needs Ryan's MFM-vs-datasheet reconcile (MFM tags
  it SUPPORT with six units; printed ability "Heroes of Ultramar" names three and is a bespoke Starting
  Strength mechanic). A product/rules call, not a build.
- B75/B85 wait on Ryan providing real faction-pack output. P4 (project-area eviction, area ~80% full)
  still open.

## Close protocol

Produce the four documents: `SESSION_HANDOFF_178.md`, overwrite `NEXT_SESSION_PROMPT.md`, append the
decision log + `DECISION_INDEX.md`, update `OPEN_ITEMS_BACKLOG.md` (move E26 to Closed/Shipped on ship).
Every changed and net-new file carries a SHA-256 (first 12) in the handoff Files section. Reissue
`pipeline_manifest.json` at close if any guarded file changed. Repo is public and flat — no GW-derived
material committed; state the exclusions when listing files for the repo.
