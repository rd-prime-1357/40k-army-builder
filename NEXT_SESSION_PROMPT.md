# Next-session prompt — Session 126 (revised)

Session 125 shipped **E1c**: `index.html` 6.2 → 6.3, new `e1c_check.js`, assertions 73 → 75 and all
75 passing. **E1, E1c and E1e all closed together** — the E1 arc is done. Read
`SESSION_HANDOFF_125.md`, then **D196** in the decision log.

**This prompt replaces the original S126 prompt, which assigned E4.** Between sessions, a process
review identified eight improvements and a repo custody pass was run against
`rd-prime-1357/40k-army-builder`. S126 is now a **tooling session**; **E4 moves to S127** and its
scoping reasoning below still stands unchanged.

## Turn type

**Tooling only.** No engine change, no data change. `index.html`, every `.json` data file, every
parser and every CSV stay untouched. New scripts and doc reorganisation only. If the work wants to
touch `index.html`, that is the signal it has drifted out of scope — bank it.

## Baseline at open

* `python3 repro_check.py` → byte-identical for `unit_loadouts.json`.
* `python3 units_repro_check.py` → byte-identical for `units.json` and its four merged lookups.
* `python3 detachments_repro_check.py` → byte-identical for `detachments.json`.
* `python3 rules_assertions.py` → **75/75**. If P3 fails with `pipeline_manifest.py not found`, the
  script did not sync — see **H3**, and say so rather than working around it again.
* Harness suite — `pool_check.js`, `e10_check.js`, `b18d_check.js`, `required_size_check.js`,
  `b31_check.js`, `stat_check.js`, `default_check.js`, `pts_check.js`, `limit_check.js`,
  `b56g_check.js`, `b58_check.js`, `e1b_check.js`, `e1c_check.js`. CLI args per each file's
  `Usage:` line — several take three or four arguments and fail with a bare Node stack trace if
  given none, which is not a real failure.
* `bundle_check.js index.html unit_loadouts.json units.json` — 2 pre-existing B36 failures.
* `python3 pipeline_manifest.py` → 36 guarded files, all match.

If any of the above is off, stop and reconcile before starting.

## Repo state at open — verified between sessions, do not re-derive

`git clone` from the sandbox works. As of the last check the repo held 43 files, every file shared
with the project area was **byte-identical**, and the only repo-only files were `README.md` and
`_headers` (which sets no-cache on the site — leave it alone).

Already done between sessions: `.gitignore` committed; the stale schema-v1 `list_store.js` replaced;
six GW-derived files (`Space_Marines_web.txt`, `Space_Wolves_web.txt`, `Black_Templars_web.txt`,
`Dark_Angels_web.txt`, `Unit_Stats.csv`, `Unit_Ability_Details.csv`) deleted; four junk files
(`MFM_Chapter_Pass (1).md`, `rules.json old`, `b56d_check.js`, `chaos-daemons.json`) deleted.

**Still expected to be missing** unless Ryan has done the bulk upload: ten harnesses (`harness.js`,
`sweep.js`, `bundle_check.js`, `pool_check.js`, `pts_check.js`, `stat_check.js`, `default_check.js`,
`limit_check.js`, `required_size_check.js`, `e1b_check.js`), two banked artifacts
(`B18c_repro_fixture.json`, `equipped_parser_B18c_banked.py`), and thirteen docs (decision log,
backlog, S125 handoff, this prompt, the four spec/architecture/dictionary/pipeline docs,
`OUTPUT_FORMAT_SPEC_for_project_instructions.md`, `E1_DETACHMENT_SCOPE.md`, and the three MFM
analysis `.md` files). Report which are still absent rather than treating absence as an error.

## The task: T1–T6

Work in this order. T1 first, because T3 is built around it.

### T1 — `repo_check.py` (net new)

Clones the public repo to a temp directory and compares it against the project area. Per file, one
of four states: **match**, **differs**, **missing from repo**, **repo-only**. Reports GW-derived
material found in the repo as a distinct and louder failure than ordinary drift — that is a
publication problem, not a sync problem, and it must not read like a routine diff line.

Scope it to the manifest's guarded set plus the docs, not to everything on disk. Keep the exclude
patterns in one place and make them match `.gitignore`'s intent, so the two cannot disagree.

The clone is confirmed working; if the network is unavailable at run time, fail clearly with that
reason rather than reporting a false clean.

### T2 — Hashes in the handoff

Every handoff's Files section gains a SHA-256 (first 12 characters is enough to read) per changed
and per net-new file. The next session's baseline verifies them before anything else runs. This
catches a bad sync one session later even when the repo is unreachable, so it is deliberately
redundant with T1 rather than replaced by it.

Add the convention to this session's own handoff so S127 inherits it.

### T3 — `baseline.sh` (net new)

One command, one line of output per gate. Runs the three repro checks, `rules_assertions.py`, all
thirteen harnesses with their correct arguments, `bundle_check.js`, `pipeline_manifest.py`, and
`repo_check.py`. Exit non-zero if any gate fails.

The argument shapes are the point of the exercise — several harnesses take three or four positional
arguments and produce a bare Node stack trace when called wrong, which currently reads identically to
a real failure. Encode them once here so nobody re-derives them again.

### T4 — Known-failure allowlist in `bundle_check.js`

`bundle_check` has printed the same two B36 failures for many sessions. A gate expected to print red
trains everyone to skim past red, which is how a third failure gets missed. Add a keyed allowlist so
it reads green while exactly those two known failures are present, and **fails loudly if a known
failure disappears** as well as if a new one appears — a silently-fixed known failure means the
allowlist is stale. Empty the list when B36 ships.

This edits a harness, not the engine. That stays inside a tooling turn.

### T5 — Split the closed history

`OPEN_ITEMS_BACKLOG.md` is 166 KB, mostly Closed/Shipped narrative that every session loads and
almost none reads. Move the closed section **in full** to `BACKLOG_ARCHIVE.md` (net new) — the
standing rule that closed items keep their complete history is unchanged, the history just moves.
The working backlog keeps the Open Items section plus a one-line pointer per closed ticket (ID,
title, session closed, decision reference).

Same move for the decision log: `DECISION_INDEX.md` (net new), one line per D-entry — number, title,
session. `40K_Decision_Log_v3_0.md` itself is **not** modified. It remains authoritative; the index
exists so sessions can find the three entries they need without reading 531 KB.

If T1 and T3 run long, T5 banks cleanly to a later session. Say so and stop rather than
half-splitting the backlog.

### T6 — Module-extraction policy

Policy, recorded as a decision entry, no code. `list_store.js` stays as it is with its E1b-2 guard.
No further extraction of code out of `index.html` without a positive reason: the one extraction the
project has done bought nothing that has been used yet, and cost a multi-week silent divergence that
needed a new assertion to police. The single-file architecture is a real constraint of the deploy
model, and partial modularisation fights it.

## New assertions

Per D107, whatever T1–T4 assert as true becomes an executable check. At minimum: that
`repo_check.py`'s exclude patterns cover every GW-derived file class named in the plan, and that
`bundle_check.js`'s allowlist matches the failures actually present.

## Backlog

Open the tooling items as real tickets at session start so they are tracked rather than living in a
plan document: **T1–T6**, plus **H4** for Ryan's per-session repo refresh becoming routine. Close
each as it ships. `PROCESS_IMPROVEMENT_PLAN.md` is superseded once these are ticketed — note it and
stop maintaining it.

One correction to carry into the ticket text: the plan document groups all 28 CSVs as Wahapedia
exports. Ten of them (`Unit_Stats.csv`, `Unit_Weapons.csv`, `Unit_Abilities.csv`,
`Unit_Ability_Details.csv`, `Unit_Points.csv`, `Unit_Wargear_Options.csv`, `Unit_Other_Options.csv`,
`Rules.csv`, `Keywords.csv`, `Weapon_Abilities.csv`) are our own pipeline outputs. They stay excluded
anyway, but on content grounds — they carry GW text verbatim in their description columns. The test
is what a file contains, not who generated it.

## Ground rules

* Tooling-only turn. If a fix wants an engine or data change, bank it.
* `index.html` does **not** version-bump this session. If it does, the turn typing was violated.
* Deliver code as files; describe designs in prose; findings-first reporting; batch anything needing
  Ryan and proceed on the recommendation unless irreversible.
* Do not rename anything in files or UI — the project name is still unsettled.
* **Naming convention adopted this session.** The next-session prompt is now the static file
  `NEXT_SESSION_PROMPT.md`, overwritten each session rather than numbered — at 6–8 sessions a day a
  numbered prompt accumulates thousands of consumed files with no value, and git history preserves
  every prior version anyway. Handoffs stay numbered and are all kept; in the repo they live in
  `sessions/`. Record this at session close, and write the close-out prompt to the static name.

## Also open

**H3** — `pipeline_manifest.py` custody. Ryan's action, unchanged. T1 is what finally makes this
class of failure visible rather than archaeological.

**H4** — the bulk repo upload and the per-session refresh. Ryan's action.

**Pending product decision** — repo layout, flat at root versus `scripts/` and `docs/` folders.
Recommendation is flat: the checks then need no path logic. T1 should read the layout from the clone
rather than hard-coding it, so this stays reversible.

---

## S127: E4 — carried forward unchanged from the original S126 prompt

With E1 shut, the open items are **P2** (backlog trimming from S18), **E4** (detachment enhancement
options in the config panel — now unblocked), **E21** (detachment-driven army-construction effects —
now unblocked), **E12** (a leader-system item), **B56**, **B17**.

The two natural next steps riding on E1c are **E4** and **E21**. E4 is thinner — enhancement records
already ship inside the E1a detachment record with name, points and the `(Upgrade)` flag, so E4 is an
assignment UI plus a per-unit enhancement field plus the 25.04 limit rules (2 at Incursion / 4 at
Strike Force; CHARACTER units only; no EPIC HEROES; no duplicate enhancement in an army; no unit with
more than one; `Upgrade`-tagged enhancements as the exception). One product question surfaces once we
start: the enhancement-assignment UI itself.

E21 is a parsing-and-modelling problem in its own right — 34 detachment abilities across the full
dump carry require/forbid language in free prose. Under D0's undetermined-legality default the app
leans permissive today; E21 is what closes that.

**Start E4.** Its scope is bounded, its data path is already in place, and it produces a visible
feature over the E1c picker. E21 wants its own scoping pass before build.

**If E4 opens as expected**, the split is likely: scoping/design turn (S127) → engine + persistence
turn (S128) → picker/config UI turn (S129), with a data turn only if a source flag needs adding.

## Standing inputs, neither blocking, worth more now

* Faction packs for **Black Templars, Blood Angels, Space Wolves, Death Guard** — takes the
  nine-detachment no-text gap to zero and upgrades 41 more from previous-edition to current text.
  Now that E1c renders that text with a per-item tier badge, upgrading these directly reduces visible
  `prev. ed.` marks.
* A **single-column re-extraction of the Space Marines pack** in the Dark Angels pack's form — flips
  15 detachments' stratagems from previous-edition fallback to current text and retires the
  column-splitter. Same story: parser re-run on E1a code as it stands.
