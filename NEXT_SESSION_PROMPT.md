# Next-session prompt — Session 127

Session 126 was a **tooling session**: repo custody check, gate consolidation, known-failure
allowlist, and a backlog/decision-log split. Read `SESSION_HANDOFF_126.md`, then **D197** and
**D198** in the decision log. `index.html` did **not** version-bump — still 6.3.

## Turn type

**Analysis / scoping.** No engine change, no data change expected — this session decides E4's shape;
the split from here is likely engine + persistence (S128) → picker/config UI (S129), with a data
turn only if a source flag turns out to be missing. If the scoping pass finds E4 is thinner than
that, ship what's ready and say so rather than forcing the three-way split.

## Baseline at open

Run `./baseline.sh`. It covers every gate in one command now (T3, S126) — both repro checks, the
detachments repro check, `rules_assertions.py`, all thirteen harnesses with their arguments baked
in, `bundle_check.js`, `pipeline_manifest.py`, and `repo_check.py`. Use `--no-repo` if the network is
unavailable in this sandbox.

**Verify the S126 hashes** (T2 convention, first use this session) before trusting the sync: compare
the SHA-256 (first 12 chars) of each changed/net-new file in `SESSION_HANDOFF_126.md`'s Files section
against what's actually in the project area. A mismatch means a bad sync — stop and reconcile rather
than build on top of it.

If `repo_check.py` finds drift (this session's tooling changes haven't been pushed to the repo yet as
of S126 close), that is expected — not a reason to stop, just note it.

## The task: E4 — detachment enhancement options in the config panel

**Why this is next.** Enhancements already arrive inside the E1a detachment record with name, points
and the `Upgrade` flag — see `E1_DETACHMENT_SCOPE.md` §4. E4 is an assignment UI plus a per-unit
enhancement field plus the 25.04 limit rules, not a second data build. It's the natural next visible
feature riding on E1c, and it's bounded enough to scope and design in one session.

**The 25.04 rules to enforce:**
- 2 enhancements at Incursion battle size / 4 at Strike Force (mirrors the DP-budget battle-size
  split E1b already established).
- CHARACTER units only.
- No EPIC HEROES.
- No duplicate enhancement anywhere in the army.
- No unit (including a unit an attached leader is part of) carrying more than one enhancement.
- `Upgrade`-tagged enhancements are the exception: allowed on non-Characters, up to three of the
  same, and the 2nd/3rd copies don't count against the per-battle-size limit though they still cost
  points.

**What this session should produce:** a design write-up (decision-log entry) covering—
- Where the enhancement picker lives in the config panel, and how it's scoped to only the
  enhancements from the army's currently-selected detachment(s).
- The per-unit field shape: does an enhancement attach to the unit entry directly, or to the leader
  sub-record the way `co_leader` fields do? `Datasheets_leader.csv` / the existing leader-attachment
  fields are the reference point.
- How the five hard-block rules above map onto existing validation patterns — D114/D115's
  hard-block precedent for datasheet limits is the closest analog, not the older flag-and-warn line.
- The `Upgrade` exception's bookkeeping: it needs its own counter separate from the main limit, since
  it explicitly falls outside it.

**One real product question surfaces here and needs Ryan:** the enhancement-assignment UI itself —
where in the flow a player picks an enhancement for a unit (a control on the unit card vs. a modal vs.
something else). Bring a recommendation with a one-line why per the standing process; don't block the
session on it if a reasonable default lets scoping continue.

## New assertions

Per D107, whatever this session concludes about the 25.04 enforcement shape should land as an
executable check once E4 actually builds (S128), not just as prose here.

## Backlog

Open **E4**'s scoping as explicit sub-steps if the design pass reveals natural seams (e.g., an E4a
data-shape check, an E4b engine turn, an E4c UI turn) — same pattern E1 used. **6 open tickets**
carry forward unchanged: P2, E21, E12, B56, B17, plus E4 itself (now in active scoping).

## Ground rules

* Analysis/scoping turn — if the session's findings clearly call for touching `index.html` or a data
  file, that's fine (S128/S129 will do the actual build), but don't half-build this session; a clean
  design write-up beats a partial engine change.
* Deliver findings as prose/decision-log entry; batch anything needing Ryan with a recommendation.
* Do not rename anything — project name still unsettled.
* Hashes convention (T2) continues: this session's own handoff gets SHA-256s in its Files section
  for S128 to verify.

## Standing inputs, neither blocking, worth more now

* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard** — takes the
  nine-detachment no-text gap to zero and upgrades 41 more from previous-edition to current text.
  E1c already renders that text with a per-item tier badge, so upgrading these directly reduces
  visible `prev. ed.` marks.
* A **single-column re-extraction of the Space Marines pack** in the Dark Angels pack's form — flips
  15 detachments' stratagems from previous-edition fallback to current text and retires the
  column-splitter.
