# PROJECT COLD STORAGE

Written at Session 259, the last working session before the project is set aside.

This file exists so that nobody has to read back through 134 session handoffs to understand what this
project is, what state it is in, and what picking it up again would actually cost. It assumes no prior
knowledge. If you are a future Ryan returning after a long gap, or a model opening the repo cold, read
this first and read nothing else until you have a question it does not answer.

Everything below was verified from command output during S259, not recalled. Where a number is a
belief rather than a check, it says so.

---

## 1. What the thing is

A browser-based army list builder for Warhammer 40,000, 11th Edition, Matched Play. You pick a
faction, pick a detachment, add units, configure their models and wargear, attach leaders, assign
enhancements, pick a warlord, and watch a points total. It runs entirely in the browser. There is no
server, no account, no database. Saved lists live in the browser's own local storage and travel
between machines only by the export/import buttons, which move a JSON file.

It is deployed on GitHub Pages out of the public repo `rd-prime-1357/40k-army-builder`. The whole
application is one file, `index.html`, currently **v6.27**, about 440 KB. That single-file shape is a
constraint of the deploy model, not a stylistic choice, and it is deliberately not being unpicked —
the one piece of code that was extracted out of it (`list_store.js`) went unused and silently diverged
for weeks until an assertion was written to police it.

### The one principle that explains the architecture

**D0: illegal army states must be unreachable, not merely flagged.**

Most list builders let you build something illegal and then show you a red warning. This one is meant
to make the illegal thing un-clickable in the first place. That is the product's whole reason to
exist, and it is why almost every design argument in the decision log resolves the way it does.

D0 also explains the thing a newcomer finds strange: the rules live in JavaScript inside `index.html`,
not in a rules-description data format. Enforcement needs to know about interactions — a mark of
chaos constrains which leader may attach, which constrains which enhancement may be taken, which
depends on which chapter roster resolved — and every attempt to express that as data ended up
expressing it as data-shaped code. Curated tables carry the facts; the engine carries the reasoning.
This works, and section 7 explains what it costs.

---

## 2. What actually works today

**Twenty armies are built**, holding 484 unit entries and 211 detachments between them.

- **Adeptus Astartes (12):** a generic Space Marines roster of 82 units, plus eleven chapters —
  Ultramarines, Iron Hands, Blood Angels, Dark Angels, Space Wolves, Deathwatch, Salamanders,
  Imperial Fists, Raven Guard, White Scars, Black Templars.
- **Imperium (1):** Grey Knights, 25 units.
- **Chaos (6):** Chaos Daemons (74), Chaos Space Marines (58), Death Guard (36), Thousand Sons (34),
  World Eaters (30), Emperor's Children (23).
- **Xenos (1):** Drukhari, 23 units.

Read the chapter counts carefully. Ultramarines shows 8 units and Iron Hands shows 2 because chapter
rosters are stored as **overlays on the generic Space Marines pool**, not as complete rosters. The
engine unions the generic pool into every chapter at runtime. For the six chapters with no dedicated
book that is correct. For the five with their own complete Munitorum Field Manual file — Black
Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves — it is wrong, and it is the largest
live D0 violation in the app. See B90 in section 5.

### What a user can do, end to end

Create and name a list; choose an army; choose a battle size (Incursion or Strike Force) which sets
the points target and the unit-count limits; choose a detachment and its Force Disposition; browse the
available units for that army and detachment; add units and set unit size within the datasheet's legal
range; open a unit's options pane and make model, weapon and wargear choices with the caps enforced;
attach Leader units to eligible bodyguard units; select Marks of Chaos where the detachment demands
them; check Tank Ace on eligible vehicles under Headhunter Task Force; assign enhancements, with
ineligible ones shown disabled and the reason stated; nominate a warlord; read a full datasheet modal
with weapon profiles, abilities, keywords and rules text; watch the running points total against the
target; save several lists; and export or import a list as JSON.

### What a user cannot do

There is no printing or formatted text output — export is JSON only. There is no account, no cloud
sync and no sharing link; lists are tied to one browser profile. There is no transport assignment, so
nothing can be enforced about who is embarked in what. Drukhari ships without its Harlequin and
Anhrathe allied units, so a legal Drukhari list using that allowance cannot be built here. Battle
sizes below Incursion and above Strike Force are not offered. And of the sixty-odd factions in the
game, forty are not built at all.

---

## 3. How it is built — the pipeline

Nothing in the data files is hand-written, and nothing in them should ever be hand-edited. Every
output file is produced by a script from source material, and a gate proves it can be reproduced.

The chain runs: **private GW-derived sources → parsers → JSON data files → `index.html` reads them at
runtime.**

The sources are Munitorum Field Manual text files (one per faction), a Wahapedia CSV export, GW
faction pack text, and the core rules text. They live in the **private** repo
`rd-prime-1357/rd-prime-1357-data-sources`, with a read-only access token stored at
`SOURCE_REPO_TOKEN.txt`. `source_manifest.json` declares 85 source files and their hashes; the private
repo currently holds 88 blobs, the three extras being ungated inputs.

**You need the private sources to regenerate the data. You do not need them to run the app.** The
deployed site serves the committed JSON and works with no sources present at all.

The main parsers are `mfm_points_parser.py` (points, unit lists, leader/support attachment),
`detachment_parser.py` (detachments, enhancements, unique tags, bearer restrictions),
`wahapedia_transform.py` and `convert_to_json.py` (datasheets, weapons, abilities, keywords),
`loadout_parser.py` and `equipped_parser.py` (model and wargear options), and `merge_factions.py`
(assembling `units.json` from the per-faction pieces).

The output data files are `units.json`, `unit_loadouts.json`, `detachments.json`,
`detachment_effects.json`, `wargear_points.json`, `datasheet_wargear_abilities.json`,
`faction_taxonomy.json`, `keywords.json`, `rules.json`, `abilities.json`, `weapon_abilities.json`,
`core_glossary.json` and `bundled_swaps.json`.

### The one command

`./baseline.sh` runs every gate. `--fetch` pulls a verified copy of the public repo first;
`--data-turn` additionally fetches the private sources and refuses to run tier-A-only in silence.

A documentation or engine turn runs 41 gates with 5 skipped for want of sources. A data turn runs 42.
**At S259 open, a full `--fetch --data-turn` run passed 41 of 42**, the only failure being
`repo_check` reporting the two files this session had already edited locally.

The gates and what each protects:

- **`repro_check`, `units_repro_check`, `detachments_repro` (tier B).** Re-run the parsers against the
  private sources and compare byte-for-byte with the committed JSON. These are what make the record
  self-reproducing. All three passed at S259. If one of these ever fails, the shipped data and the
  shipped parsers have parted company and you must find out which one moved.
- **`rules_assertions.py`.** 139 executable statements of fact about the data and the rules — 94 that
  run without sources, 45 more that need them. Every legality-critical claim the project makes is
  supposed to live here. All 139 passed at S259.
- **The JavaScript harness suite** (`b93_check.js`, `b126_check.js`, `e1b_check.js` and about thirty
  others). Each pins the engine behaviour for one ticket by loading the real `index.html` functions
  and the real shipped data. They are the regression net for the engine.
- **`b87_check` / `b88_check` (tier B).** Prove the points and detachment parsers still read the v1.1
  Field Manual format correctly.
- **`bundle_check`.** Guards the bundled-swap data.
- **`pipeline_manifest`.** Hashes 237 guarded files and fails if any changed without the manifest
  being rewritten. This is the file-custody backbone.
- **`repo_check`.** Compares the repo against the project file area and scans for GW-derived material
  that must not be public.

---

## 4. The rules that keep the project honest

These are process, not code, and they were each learned the hard way.

**Turn typing.** Every session is declared engine-only, data-only, or tooling-only, and mixing is
prohibited. When something breaks you want one class of change to bisect, not three.

**Fix the parser, never the output.** A hand-edit to a JSON file survives until the next regeneration
and then vanishes, usually silently, usually months later.

**A fact that is not an executable check does not hold.** Prose claims in handoffs go stale and then
get built upon. Legality claims belong in `rules_assertions.py` or a harness.

**Source-first.** Verify from the source file before acting. An absence in derived data is never
evidence of absence in the rules.

**Reconcile a failing gate before starting work, never around it.** Manifest work was reverted twice
without anyone noticing because a red gate was explained in prose and carried forward.

**Session close sequence.** Add the new handoff filename to `GUARDED` in `pipeline_manifest.py`
*first*, then run `pipeline_manifest.py --write`, then `--freshness-check`, as the literal last two
commands. The handoff's own hash is a row in its own Files table, which is why the order matters.

---

## 5. What is broken or missing

Twenty-three tickets are open. Grouped by what they mean rather than listed by number:

### Places the app is confidently wrong — the live D0 gaps

These matter more than the rest combined, because in each case the app permits or displays something
the rules do not, without saying so.

- **B90 — chapter rosters are unioned when five of them should be complete.** The engine adds the
  whole generic Adeptus Astartes pool to every chapter. For Black Templars, verified directly against
  its own Field Manual, this leaks 90 units that its own book excludes — every Librarian variant
  (Black Templars field no Psykers) and eleven named characters from other chapters. All are
  selectable today. Blood Angels, Dark Angels, Deathwatch and Space Wolves are assumed to have the
  same shape and each needs confirming against its own file during the fix. Scoped as three separate
  turns: an engine flag distinguishing complete from union rosters, a data rebuild of the five
  chapters from their own sources, and re-verification of their loadouts and wargear points.
- **B127 — 74 enhancement records have no rule text anywhere we hold.** Spread across all fourteen
  armies. Without the text there is no bearer restriction to parse and no effect to apply, so those
  enhancements are offered with no eligibility check behind them. This was chased down properly: 70 of
  the 74 have no match at all in the Wahapedia export, and the four that appear to match do so under
  10th-edition detachment names that 11th renamed, where the correct text already resolves elsewhere.
  This is a source-acquisition problem, not a build problem. Nothing can be built until the text
  exists.
- **B135 — transports are not modelled at all.** A saved list is a flat set of entries; nothing
  records which unit rides in which transport. The word "embark" does not appear in `index.html`.
  Under Pactbound Zealots the mark-matching embarkation restriction therefore cannot be expressed —
  not merely unenforced, unrepresentable. Two units are affected today (Chaos Rhino, Chaos Land
  Raider). It is recorded as an unmodelled restriction with an assertion so it cannot quietly vanish.
- **B120 — enhancements that change *other* models' weapons.** Nineteen records across eight armies
  modify weapons carried by models other than the bearer — "models in the bearer's unit",
  "Battleline models in the bearer's unit", and in one case models in a different unit entirely. The
  engine renders one entry's data at a time and has no cross-entry path. Needs its own scoping turn.
  **B124** (one enhancement that halves a unit-wide Toughness) folds into that scoping turn.
- **E23 — the Tank Ace Character keyword grant.** Headhunter Task Force exists in six built armies and
  lets the player nominate up to three Tank Ace vehicles to gain the Character keyword. The data is
  authored and asserted; the engine turn was never built. So the grant does not propagate to whatever
  else keys off Character.
- **B136 — an uncapped tally read in storage order.** A second copy of a defect fixed elsewhere
  (B103), living in `loCarriers`. Believed unreachable through the current UI, which is why it is
  filed here rather than at the top.

### Known limitations, deliberately accepted

- **B116 — Drukhari's allied Harlequin and Anhrathe units.** Drukhari carries an army rule permitting
  these up to a points cap that scales with battle size, and one detachment grants a larger version.
  Their points come from *Codex: Aeldari*, which is not built and is not in the priority order.
  Drukhari therefore ships without them: the tool under-represents legal options but creates no
  illegal state, which is the right trade under D0. **This ticket is still open**, and Ryan classified
  it as required before the product could be called production-ready — do not read Aeldari's absence
  as having closed it.
- **B67b** — an optional purge of two GW-derived files from old git history. Low priority.
- **E12** — user accounts. Deferred indefinitely; architectural.

### Display and usability

- **B69** — datasheet "select N abilities" pools render with no visible link to the selector that
  drives them.
- **B97** — Grand Coven's detachment rule text renders as one unbroken wall of text.
- **B70** — Wardens of Ultramar cannot be attached to a unit; the decision was made to build the
  join/Starting-Strength mechanic, and it needs a scoping turn.
- **B122** — Chaos Daemons' enhancement descriptions are shorthand summaries rather than rule text.
- **E28** — move detachment selection out of the centre list and into the right-hand configuration
  panel, Force Disposition included. Ryan-raised.

### Data and pipeline debt

- **B85** — the converter's faction-keyword detector produces noise rather than signal; a diagnostic
  exists, the fix does not.
- **B86** — one Chaos Daemons faction-pack page yields no extractable text. May be nothing.
- **B75** — faction-pack pages that cannot be resolved into columns.
- **B17** — remaining loadout completeness gaps; two parts and an engine turn are already done.
- **B134** — six automatic keyword conferrals found in a census that were never given a ticket. Not
  legality-critical.

### Process

- **P2** — `loadout_parser.py` custody, softened long ago and largely historical.
- **P4** — the project-area capacity problem and the long-term architecture response. Milestones 0 and
  1 shipped; M2 is next and unstarted. This is what produced `baseline.sh --fetch`.

### Not tickets, but outstanding: the render checks

Five UI checks have been written and never run, now six sessions old, because they need a human
looking at the deployed app. The scripts are preserved in full at the end of
`NEXT_SESSION_PROMPT.md`. **S250's is the one that matters** — it is the only case where the app edits
a saved list without telling the player: shrinking an over-capped unit silently drops weapon picks,
keeping the first two in the option's listed order rather than the first two clicked. Anyone reviving
the project should run that one before anything else.

---

## 6. The traps

Each of these cost multiple sessions at least once. They will cost them again.

**The project file area is not evidence of what exists.** The `/mnt/project` mount shows one entry per
filename, so duplicates are invisible, and it goes stale after files are added or removed. It is
reliable for file *contents* and worthless as evidence of presence or absence. Clone the repo to find
out what is real. Three consecutive sessions asked for a file to be re-uploaded because they trusted
the mount and the divergence ran the opposite way to what they assumed — the repo copy was the newer
one the whole time.

**A census result that looks impossibly small is an unread field, not a designer's choice.** Every
time a count came back surprisingly low and someone reasoned about why the game designers might have
done it that way, the real answer was that a source field had not been read. Widen the read; never
explain the number.

**Scope documents go stale and later decisions supersede them.** `B93_SCOPE.md` told a later session
to demote a type gate to a default; a decision made after the scope document was written had already
settled the opposite, and the session prompt had inherited the stale wording. Check the decision log's
date against the scope document's before following an instruction in a scope document.

**Hand-edited output files are lost on the next regeneration.** Always fix the parser.

**GW-derived material must never reach the public repo, and the test is content, not authorship.**
Several of the project's own pipeline outputs carry GW ability and rule text verbatim in their
description columns, and they are excluded on exactly the same grounds as the source files. When
producing any list of files bound for the public repo, apply the test explicitly and state what was
excluded.

**Do not rename anything.** The project's own name was never settled — "40K Army Builder" is a working
label and "ArmyForge" was considered and shelved. Nothing in files or UI was ever renamed, and it
should stay that way until a name is actually chosen.

---

## 7. Why it was set aside, and what a revival faces

Be clear-eyed about this: the project was not close to finished, and the backlog was not draining.

Over the twenty-six sessions from S232 to S257, twenty-four tickets closed and twenty-three opened.
That is a steady state, not progress toward zero. It is not a sign of bad work — the closes were real
and the opens were genuine discoveries, mostly found by censusing data that had never been read
completely before. But it means the finish line was not approaching at any rate worth waiting for.

The cause is structural. Encoding rules as engine code plus curated tables is what makes D0
achievable; it is also what caps throughput at one maintainer's rate. Every new faction and every new
detachment interaction needs someone to read the rule, decide how it interacts with everything already
modelled, write the enforcement, and write the assertion that pins it. Twenty armies took the sessions
they took. Forty remain.

So a revival that seriously intends to cover the game is not a continuation of this backlog. It is a
rules-as-data rebuild: an authoring format expressive enough to state restrictions declaratively, an
evaluator that resolves them, and enough tooling that adding a faction is a data task rather than an
engineering one. That is a different project which could reuse this one's parsers, its source custody,
its gate discipline and its accumulated rules knowledge — the twenty-three open tickets are, read
correctly, a specification of what such an evaluator must be able to express.

A revival that merely intends to keep twenty armies correct and current is much smaller and is
genuinely tractable: fix B90, acquire B127's missing text, run the render checks, and thereafter track
each new Field Manual release through the existing pipeline.

The deployed app needs nothing from anyone. It keeps serving v6.27 from GitHub Pages indefinitely and
depends on no subscription, no key and no running service.

---

## 8. Where everything lives

**Public repo — `rd-prime-1357/40k-army-builder`.** Flat; every file sits at the root. Holds the app,
every data file, every parser, every gate and harness, every document, and every session handoff.
GitHub Pages serves `index.html` from it.

**Private repo — `rd-prime-1357/rd-prime-1357-data-sources`.** All GW-derived source material. A
read-only token is stored at `SOURCE_REPO_TOKEN.txt`, which lives in the project working area and is
never committed anywhere.

**Living documents** — updated as the project moves:

- `40K_Decision_Log.md` — the full reasoning behind every decision, D1 through D356. This is the real
  history; the handoffs are its working notes.
- `DECISION_INDEX.md` — one paragraph per decision. Read this to find which decision to read in full.
- `OPEN_ITEMS_BACKLOG.md` — split into Open Items and Closed / Shipped. Closed entries keep their full
  history rather than being trimmed.
- `NEXT_SESSION_PROMPT.md` — overwritten each session; git history holds every prior version. Also
  carries the five outstanding render-check scripts.
- `40K_Functional_Spec.md`, `40K_Architecture_Overview.md`, `40K_Data_Pipeline_Process.md`,
  `40K_Data_Dictionary.md` — reference documents, some sections predating what shipped. Trust the
  decision log over these where they disagree.

**Archival documents** — done, kept for the record: the per-faction build scope documents, `B93_SCOPE.md`,
`B99_SCOPE.md`, `E1_DETACHMENT_SCOPE.md`, `P4_ARCHITECTURE_SCOPE.md`, the MFM reconciliation passes,
`PROCESS_IMPROVEMENT_PLAN.md`, `Example_of_what_not_to_do.md`.

**Session handoffs.** `SESSION_HANDOFF_125.md` through `SESSION_HANDOFF_259.md`, one per session,
every one kept. Sessions 1 to 124 pre-date the convention and were never committed; they are gone and
that is expected rather than a loss. **The 125–259 chain is complete.** Handoff 203 was believed
unrecoverable from S206 to S258 — it had never been committed and no copy could be found — and it was
recovered from a local copy and pushed ahead of S259. If you read an older document claiming 203 is
missing, that claim is superseded.

---

## 9. If you are picking this up again

1. Clone the public repo. Put `SOURCE_REPO_TOKEN.txt` next to `baseline.sh`.
2. Run `./baseline.sh --fetch --data-turn`. Expect 42 of 42, or 41 of 42 if the project file area is
   not in sync with the repo, which is normal and is what `repo_check` is telling you.
3. Read the last three session handoffs and the tail of `DECISION_INDEX.md`.
4. Run the five render checks from `NEXT_SESSION_PROMPT.md`, S250's first.
5. Before building anything, decide which revival you are attempting — maintain twenty armies, or
   rebuild rules-as-data. Section 7 is the honest input to that choice.
