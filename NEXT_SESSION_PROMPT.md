# NEXT SESSION PROMPT — Session 237

## Recommended pick: the B99 tooling turn, with B121 folded in. Both are tooling, both are small.

S236 shipped B99's engine half (`index.html` v6.21, D330). What is still owed is the
`rules_assertions.py` census assertion — the thing that stops the curated table rotting when a new
faction lands. Read `B99_SCOPE.md` §5 for the intent, then D330 for the numbers, which **supersede
§1's table**. Verify the S236 file hashes at open.

## Ryan action required

- **Push S236's changed files** to the public repo. `repo_check` is red at S236 close for
  `index.html`, `b99_check.js`, `baseline.sh`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md` and
  `SESSION_HANDOFF_236.md` — expected for unpushed work, not a regression. Reconcile at open.
- **B99's render still needs Ryan's eye.** Three shapes to look at, listed in
  `SESSION_HANDOFF_236.md` under "Ryan action required".

## The B99 tooling turn

Tooling-only. A source-derived census assertion in `rules_assertions.py` that re-derives the Set A
and Set A2 candidate set from `detachments.json` descriptions and **fails on any record matching
the shape that has no row in `ENHANCEMENT_WEAPON_EFFECTS`**. Direction matters: `b99_check.js`
already covers table → source (no orphan keys, every curated characteristic and ability named in
its own description), so this assertion is specifically source → table.

Pin **57 Set A / 23 Set A2 / 78 union / 43 names**, not S235's 57 / 17 / 72. The difference is
*Eye of the Primarch*; D330 explains why, and `B99_SCOPE.md` §1's table is stale on this point —
correct it in the same turn rather than leaving two numbers in circulation.

Two things the clause reader must get right or it will fail on good data:

- **`;` is not a clause boundary when the governing condition sits before it.** *Possessed Blade*
  is the case — "At the start of the battle, select one melee weapon equipped by the bearer; add 1
  to the Attacks characteristic of that weapon" — and it is correctly OUT of Set A. A splitter that
  treats the second half as unconditional will demand a table row for it.
- **Chaos Daemons' 29 records carry shorthand summaries, not rule text** (B122). They cannot match
  the shape and must not be counted as a pass by accident — the assertion should be able to say
  they were skipped and why, not silently agree with itself.

**B121 groups cleanly with this** — six scope documents missing from GUARDED, an XS tooling item.
Verify each of the six is actually in the repo before appending; a GUARDED entry for an absent file
turns the gate permanently red.

## Open, at your discretion

23 open: B116 (decision-blocked), B99 (tooling half), B119, B120, B121, B122, B97, B103, E28, B93,
B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17.

B119 (Set C, bearer statline) is a small engine follow-on and should come after the B99 tooling
turn so it can reuse the same curated-table-plus-census pattern. B120 (Set D, other models'
weapons) needs its own scoping turn — note that Set D effects apply uniformly to every model in the
unit, so unlike B99 they can be written into a rollup row without the three-way rule; that is worth
establishing in scoping rather than discovering in the build. B122 needs a scoping turn that
answers a source question first: does the held Chaos Daemons material contain the real enhancement
text at all? If yes it is a `detachment_parser.py` bug; if no it is a source-acquisition item.

## Standing reminders

- Keep running a data-turn baseline periodically even on non-data sessions.
- `40K_Decision_Log.md` has now been absent from the project-area mount for **four** sessions
  running and is recovered from the repo each time. The mount is not evidence of absence — ask for
  a file-list screenshot rather than assuming, but it is worth re-uploading.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- Turn typing stays strict. B99's engine and tooling halves are separate sessions by design.

## Decisions waiting on Ryan

- **B99 display** — four, shipped on their recommendations at S236 and all still reversible. New
  Recruit screenshots would settle the idiom.
- **B116** — unchanged. `DRUKHARI_BUILD_SCOPE.md` §6. Blocks nothing.
- **Next faction after Drukhari** — the documented priority order is fully built; none is queued.
  Recommendation stands: clear the engine backlog first.

## Close

Produce the four documents, register `SESSION_HANDOFF_237.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
