# NEXT SESSION PROMPT — Session 238

## Recommended pick: B119 (Set C, bearer statline). Engine-only.

B99 closed at S237 (D331) — both its engine and tooling halves are shipped. B119 is the natural
next pick: same curated-table-plus-census pattern B99 and B113 already proved, and D329's census
(`B99_SCOPE.md` §1, Set C) already did the scoping work — 10 enhancement records across 8 armies,
6 distinct names (*Brazen Form*, *Disciple of Rhetoricus*, *Iron Laurel*, *Living Carapace*,
*Master Artisan*, *Rites of War*), an unconditional change to the bearer's own statline
(Toughness, Wounds, Objective Control, Save) that never reaches `buildStatTable`.

Materially cheaper than B99: `conferredStats`, `activeStatOverrides` and
`activeOtherOptionOverrides` already merge overrides into the stat table and already render an
asterisk-and-legend. `statOverrideFromText` handles only absolute "characteristic of N" sets, so it
needs a delta path alongside the set path — read the B99-CENSUS clause-splitting logic in
`rules_assertions.py` before writing a new one; the marker vocabulary and the bearer-possessive
regex (`by the bearer\b|bearer'?s(?!\s+unit)|\bthose weapons\b`, tested against the real source
text at S237) are directly reusable, not something to re-derive from scratch.

## Ryan action required

- **Push S237's changed files** to the public repo. `repo_check` is red at S237 close for
  `rules_assertions.py`, `pipeline_manifest.py`, `B99_SCOPE.md`, `40K_Decision_Log.md`,
  `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, the six newly-guarded scope docs, and
  `SESSION_HANDOFF_237.md` — expected for unpushed work, not a regression. Reconcile at open.

## The B119 engine turn

Engine-only. A curated table (same key shape as `ENHANCEMENT_WEAPON_EFFECTS` and
`ENHANCEMENT_BEARER_RESTRICTIONS`: `detachment_key + '::' + name`) mapping each of the 6 names to
its statline delta, a delta applier feeding `activeStatOverrides` (or the equivalent path
`buildStatTable` already reads), and a `b119_check.js` harness. Re-verify the 10/6/8 population
against source at build time rather than trusting D329's number carried forward — B99's own
experience (D330 corrected D329's Set A2 count) is the reason for that discipline, not a formality.

Two things worth checking directly rather than assuming from the Set C label:
- Confirm none of the 6 names' statline deltas are conditional-only or share a record with a
  Set A/A2/B/D effect already in `ENHANCEMENT_WEAPON_EFFECTS` — if one does, the render needs to
  compose rather than overwrite.
- Confirm the bearer-attribution question (D105/D112/B99's three-way rule) applies the same way to
  a statline row as it does to a weapon row for any of the 6 names' bearer units, or state plainly
  if none of them hit a multi-model-group Character and the question doesn't arise this ticket.

**Tooling half.** A `rules_assertions.py` census assertion in B99-CENSUS's shape, in its own
session, not folded into the engine turn — B99's own turn-typing violation risk was exactly this.

## Open, at your discretion

21 open: B116 (decision-blocked), B119, B120, B122, B97, B103, E28, B93, B90, B94, B85, B86, B69,
B70, B75, P2, P4, E23, B67b, E12, B17.

B120 (Set D, other models' weapons) needs its own scoping turn before build — Set D effects apply
uniformly to every model in the unit, so unlike B99/B119 they can be written into a rollup row
without the three-way rule; worth establishing that in scoping rather than discovering it in the
build. B122 needs a scoping turn that answers a source question first: does the held Chaos
Daemons material contain the real enhancement text at all? If yes it is a `detachment_parser.py`
bug; if no it is a source-acquisition item.

## Standing reminders

- Keep running a data-turn baseline periodically even on non-data sessions.
- `40K_Decision_Log.md` has now been absent from the project-area mount for **five** sessions
  running and is recovered from the repo each time — this recovered copy already had D330 at
  S237 open, meaning the mount's absence does not imply the repo is behind. Worth re-uploading if
  convenient, but not a signal of anything wrong on its own.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- The project-area file mount silently strips apostrophes from filenames on upload
  (`EMPEROR'S_CHILDREN_BUILD_SCOPE.md` → `EMPEROR_S_CHILDREN_BUILD_SCOPE.md` was the case found
  at S237). Before trusting a project-area filename as the real repo filename, especially for
  anything going into GUARDED, check a fresh clone.
- Turn typing stays strict.

## Decisions waiting on Ryan

- **B99 display** — four, shipped on their recommendations at S236 and all still reversible. New
  Recruit screenshots would settle the idiom.
- **B116** — unchanged. `DRUKHARI_BUILD_SCOPE.md` §6. Blocks nothing.
- **Next faction after Drukhari** — the documented priority order is fully built; none is queued.
  Recommendation stands: clear the engine backlog first.

## Close

Produce the four documents, register `SESSION_HANDOFF_238.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
