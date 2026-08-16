# NEXT SESSION PROMPT — Session 254

## Read first

`SESSION_HANDOFF_253.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

State at S253 close: `index.html` **v6.26** (unchanged — S253 was a tooling turn), decision log through
**D350**, `SCHEMA_VERSION` **5**, baseline **all gates pass** (`repo_check` carried expected
mid-session staleness, resolves once Ryan pushes), **23 open** backlog items.

## Open

Run `./baseline.sh --fetch`. If this session ends up doing data work, re-run with `--data-turn` before
starting that portion — don't assume the turn type before reading the assignment below.

Then verify the S253 file hashes in `SESSION_HANDOFF_253.md`'s Files table against the fetched repo.
**Nine of those files (`Unit_Stats.csv` through `Weapon_Abilities.csv`) will be appearing in the public
repo for the first time this session** — confirm they're actually there and match, not just that the
fetch didn't error. If Ryan hasn't pushed yet, stop and say so rather than working around it; B138's
`GUARDED` entries for these nine will fail `pipeline_manifest` until the push happens.

## Assigned work: pick one of B90 or B93 — both large, both live-risk

Both are large (`L`, span sessions) and neither is reachable in a single sitting. This is a sequencing
call for whoever runs S254 — read both scope sections below before choosing, and say which one and why
before starting.

**B90 — SM-family chapter rosters union bug, engine+data, blocks further faction work.**
`resolveUnits()` unions the full generic Adeptus Astartes pool into every `is_subfaction` chapter, with
no distinction between the six vanilla chapters (correct to union) and the five dedicated-MFM chapters
— Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves — whose MFM is a complete,
self-contained roster that should never be unioned with generic. This is shipping wrong rosters today
for five already-built factions, not a blocker for unbuilt work.

**B93 — Enhancement/Upgrade eligibility, engine+data, live D0 gap, Ryan-flagged.** The engine checks
Character-vs-not instead of the Enhancement's own qualification requirement. Censused at 641 records /
363 names / 173 detachments / 13 armies bearer-restricted, with 369 records over-admitting today (mean
9.2 illegal bearers per record). This is a live D0 violation — an enhancement can currently be assigned
to a bearer the rules do not permit — which outranks B90's mispriced-roster defect on the D0 principle
alone, but B90 affects rosters players see immediately on list-build and B93's fix is larger. B93 is
gated on B125, B126 (shipped), B127, B128 (shipped) per its scope doc — check `B93_SCOPE.md` for
current gate status before committing to it; if any gate is still open, that may decide the choice for
you.

## Precedents from S253 that will matter again

**A ticket's build shape can be wrong even when its underlying problem is real.** B138 correctly
identified that nine files carried no integrity guard. It was wrong about which mechanism should
provide that guard (`pipeline_manifest.py`'s public-repo list, when the files weren't repo-resident at
all). Confirming a ticket's premise from source — here, actually cloning the repo and checking — caught
this before any code shipped on the wrong assumption. Re-derive scope, don't inherit it.

**A negation or exception in a hand-maintained policy file (`.gitignore`, an allowlist, a manifest) is
only as good as the code that reads it.** `repo_check.py` had silently no-op'd on `!name` lines for as
long as the comment "no negations in use today" was true. The moment that stopped being true, the gap
would have fired as a false CRITICAL on Ryan's own explicit decision. When adding an exception to a
policy file, check whether anything downstream actually consumes exceptions, not just the broad rule.

**`source_manifest.json`'s hashes don't self-update when the file they describe changes for an
unrelated reason.** S252 corrected `Unit_Points.csv`'s prices; nothing in that session's process
touched the source manifest's hash for it, because `Unit_Points.csv` wasn't guarded at the time. Now
that it is, this class of gap should be closed going forward — but check other guarded files for the
same kind of drift if a similar "fix the source, forget the manifest" pattern comes up again.

**Publishing something the app already shows in the UI is a smaller step than it first appears, but
it's still a one-way door.** Worth naming explicitly to Ryan every time, not just deciding quietly, even
when the app-parity argument is strong.

## Close

Four rolling documents updated (`40K_Decision_Log.md`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_254.md`), this file rewritten for S255, then:

1. add `SESSION_HANDOFF_254.md` to `pipeline_manifest.py`'s `GUARDED` list **before** writing
2. `python3 pipeline_manifest.py --write`
3. `python3 pipeline_manifest.py --freshness-check`

Those two commands are the literal last two of the session.

## Outstanding Ryan action carried forward from S248, S249 and S250

**A render check covering three sessions' UI.** S248's Tank Ace checkbox, S249's Mark of Chaos
selector, S250's silent truncation of an over-cap tally on size reduction. S253 shipped no UI, so the
backlog is still three deep. S250's is the one that matters most — it is the only one that edits a
saved list without telling the player. All three handoffs carry step-by-step scripts.
