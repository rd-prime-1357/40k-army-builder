# Next-session prompt — Session 130

Session 129 shipped **E4c** (UI: config-panel picker, roster chip) as **D201** — E4 is now fully
shipped end to end. Session 129 also closed **B56** as **D202**, verified stale — the header had said
"78/81 closed" since S104 but the real count against `units.json` is 270 total units, exactly 2
null-points (both retired by Ryan already). `index.html` is **6.5**, assertions **80/80**, baseline
**21/21**. Read `SESSION_HANDOFF_129.md`, then **D201** and **D202**.

## Turn type

**Analysis/scoping.** No engine, data, or UI change this session — this is E4's pattern repeating:
E4 got a scoping session (S127, D199) before any build. E21 needs the same treatment before a line
of parser or engine code gets written against it.

## Baseline at open

Run `./baseline.sh` (`--no-repo` if offline). Verify the nine S129 hashes in
`SESSION_HANDOFF_129.md`'s Files section before trusting the sync. Two files — `repo_check.py` and
`BACKLOG_ARCHIVE.md` — were missing from the project area at S129's open and had to be recovered from
GitHub; check whether they've been re-uploaded directly, and if not, pull them the same way S129 did
(`raw.githubusercontent.com/rd-prime-1357/40k-army-builder/main/<file>`) rather than losing time
rediscovering the gap.

## The task: scope E21 — detachment-driven army-construction effects

Detachment rules that require or forbid units, unlock units from other factions, or elevate units to
Battleline (moving the count cap — Functional Spec §5). This is real and biting on day one for a
built faction: Chaos Daemons' *Shadow Legion* forbids Daemon Prince and Epic Hero units while
unlocking a list of HERETIC ASTARTES units. **34 detachment abilities across the full dump carry
require/forbid language, in free prose with no common shape** — this is a parsing-and-modelling
problem in its own right, deliberately kept out of E1c. Until it ships, the app knows about
detachments without enforcing their construction restrictions (recorded in D192, consistent with
D0's undetermined-legality default of leaning permissive — but every session it stays unshipped is
another session that gap sits open on a built faction).

Re-derive from source before designing anything — don't trust the "34" figure forward without
checking it, the same way D202 didn't trust "78/81" forward. Grep the actual detachment ability text
in `Detachment_abilities.csv` / the faction pack markdown for require/forbid language and classify
what shapes actually recur (unit-name lists, keyword-based forbids, faction-unlock text, Battleline
elevation) before proposing a data model. Produce a D-numbered scope entry in the mould of D199:
what the state shape looks like, what's data vs. parser vs. engine, and a session split (E21a/b/c or
similar) the way E4 got E4a (cancelled)/E4b/E4c.

## Why this over the other three open items

**P2** is process-only, softened since D123 — no urgency. **E12** (user accounts) is explicitly
deferred by Ryan until near the end of the roadmap. **B17** (Deathwatch loadout-completeness
remainder) is real but smaller and self-contained — a fine pickup for a later session, not blocking
anything. E21 is the largest standing legality gap on a faction already built, is fully unblocked
(E1c shipped S125), and — like E4 — is going to need its own scoping pass regardless of when it's
tackled, so there's no cost to doing that pass now rather than later. My call; flag it if you'd
rather sequence B17 or P2 first.

## Backlog

**4 open:** P2, E21 (this session), E12, B17.

## Ground rules

* Analysis/scoping only — no `index.html`, data file, or parser touched this session.
* Do not rename anything — project name still unsettled.
* T2 hashes in this session's handoff Files section for S131 to verify.
* If E21's scope turns out to need a data or parser turn to even assess cleanly (e.g. confirming
  the require/forbid text shapes against the raw CSV), that's still scoping — reading and
  classifying source data is not the same as writing a parser change.

## Standing inputs, neither blocking, worth more now than before

* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard** — enhancement
  descriptions are now genuinely visible in the UI (E4c's detail expander, S129), which makes the
  30 `none`-source and 265 `wahapedia_10e`-source descriptions more prominent than they were when
  this note was first written.
* A **single-column re-extraction of the Space Marines pack** — still flips 15 detachments'
  stratagems to current text.
* The project's file storage is reportedly near capacity. S129 found duplicate-version CSVs
  (differing row counts under the same filename) likely sitting in the underlying project knowledge
  store, invisible to the flat file listing — worth Ryan clearing directly from the project's file
  manager before anything else gets pruned.
