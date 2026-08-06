# NEXT SESSION PROMPT — Session 201

## Turn type: engine-only. No data, no tooling, no parser changes. No exceptions.

Read `SESSION_HANDOFF_200.md` and `GREY_KNIGHTS_BUILD_SCOPE.md` (§6 especially) first, then this
prompt. S200 scoped Grey Knights and found the engine gap that now blocks it.

## This session's job: B101 — enforce "cannot take duplicates"

`loMaxCount` in `index.html` caps the *total* number of picks for a `max_total_all` / `up_to` option
but nothing anywhere in the engine enforces that the picks differ. Under D0 that illegal state should
be unreachable, not merely undocumented.

**This is already live, not hypothetical.** Three shipped Chaos Space Marines units carry the
no-duplicate rule only as a literal string sitting inside their `replacement_choices` array, where it
also renders to the player as a fake selectable menu entry:

| unit | `up_to` | real choices |
|------|---------|--------------|
| Raptors | 2 | 3 |
| Legionaries | — | 9 |
| Traitor Guardsmen Squad | 3 | 5 |

Grey Knights' two Nemesis Dreadknights ("up to two of the following, but cannot take duplicates",
3 and 4 choices) cannot be authored around it, which is why B100's units turn waits on this.

Suggested shape, not binding — derive the real one from the code: a `distinct: true` flag on the
option, enforcement on the selection path so a second pick of the same choice is not offered rather
than offered-and-rejected, and the label strings stripped out of the `replacement_choices` arrays so
the rule stops rendering as an option. **Note the last part is a data edit** — if stripping the
labels turns out to require touching `unit_loadouts.json`, that is a separate data turn, not this
one. Land the engine capability first and let the data follow; do not mix.

Pin the behaviour in `rules_assertions.py` and/or a JS harness before closing — a prose-only claim
about distinctness will go stale exactly like the ones D0 exists to prevent.

## Standing reminders
- Turn-typing strict: engine only. If the fix turns out to need a schema change that forces data
  regeneration, stop and hand off rather than mixing scope — a banked, well-scoped item beats a
  partial change.
- **Check sources directly, don't trust prior-session prose.** S196–S200 each found something a
  report, a hardcoded assumption, or a session prompt got wrong. S200's own prompt was wrong about
  Grey Knights being a migration candidate. Treat that as the norm.
- Two Ryan actions are outstanding and neither is this session's to resolve: the Calgar missing-comma
  fix in the private repo (unpushed since S198), and two sessions' worth of public-repo changes
  (S199 and S200). `repo_check` will stay red until the latter lands — expected, not a new failure.

## After this session
B102 (`detachment_parser.py --report` `KeyError`, one line, XS) can ride with any tooling turn.
Then B100's two data turns: Grey Knights units, then Grey Knights detachments — separate, per the
B89 arc's convention. The units turn's first check is the open `Grey_Knights_web.txt` question in
`GREY_KNIGHTS_BUILD_SCOPE.md` §5; resolve it from the pipeline, don't assume it either way.

## Close
Produce the four documents, register `SESSION_HANDOFF_201.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command — after every other edit, including edits to the handoff itself (leave the handoff's own row
in its Files table as "(this file)").
