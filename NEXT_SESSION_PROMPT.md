# Next-session prompt — Session 179

**Assigned: E27 — Leader vs Support wording in popups and output, engine-only (UI turn).** This is an
**engine turn** in `index.html` + `rules_assertions.py`. It is **mechanical** — the data already
carries the distinction (`leaderAbilityName` on the view object, shipped E26/S178), and the wording
change is UI, not legality logic. No data or tooling work; do not mix turn types. **12 open items.**

## Open at session start

Read `SESSION_HANDOFF_178.md` first, then `40K_Decision_Log.md` D269 (E26 ship). Do not trust any
session/version/decision number from memory; the handoff chain and the decision log are the only
authorities.

Run the full baseline: `./baseline.sh --fetch`. E27 is engine-only — `--data-turn` is not needed.
Expect **75** tier-A rules assertions (plus 37 tier-B skipped) and all other gates green. Reconcile
any failing gate before starting.

## E27 — the build

The attach popup (`leaderSectionHtml` / the Leader Assignment section in `renderDetail`) hardcodes the
heading "Leader" and generic body text regardless of whether the unit's `leaderAbilityName` is "Leader"
or "Support". After E26, the view object carries `leaderAbilityName` — use it to:

1. **Change the detail-panel section heading** from "Leader Assignment" to "Leader Assignment" or
   "Support Assignment" per the unit's actual ability name.
2. **Change the hint text** (the "Add an eligible bodyguard unit first: ..." line) to match.
3. **Anywhere the exported/printed list labels a unit as "Leader"** — check whether it should say
   "Support" instead. The list-panel attached-leader row and the JSON export are the likely sites.

This is a wording/UI consistency pass, not a legality change. No `permitsCoLeader` logic changes. The
assertion should verify the heading references `leaderAbilityName` rather than a hardcoded string.

Publish the index at a bumped version and state the version in the report.

## After E27

The next natural pick from the backlog is dev-manager's call. Candidates by priority:
- **B69** (select-N ability pools) — needs a data + engine arc, M-sized.
- **B70** (Wardens of Ultramar join mechanic) — still waiting on Ryan's MFM-vs-datasheet reconcile.
- **E23** (Tank Ace Character keyword grant) — needs a scoping turn.
- **B75/B85** — blocked on real PDF access from Ryan.
- Remaining faction builds per the priority order.

## Close protocol

Produce the four documents: `SESSION_HANDOFF_179.md`, overwrite `NEXT_SESSION_PROMPT.md`, append the
decision log + `DECISION_INDEX.md`, update `OPEN_ITEMS_BACKLOG.md` (move E27 to Closed/Shipped on ship).
Every changed and net-new file carries a SHA-256 (first 12) in the handoff Files section. Reissue
`pipeline_manifest.json` at close if any guarded file changed. Repo is public and flat — no GW-derived
material committed; state the exclusions when listing files for the repo.
