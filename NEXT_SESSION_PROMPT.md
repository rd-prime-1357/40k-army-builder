# NEXT SESSION PROMPT — Session 256

## Read first

`SESSION_HANDOFF_255.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

State at S255 close: `index.html` **v6.26** (unchanged since S252 — S253, S254 and S255 were data and
tooling turns), decision log through **D352**, `SCHEMA_VERSION` **5**, `rules_assertions.py` at **138**
assertions, **23 open** backlog items.

## Open

Run `./baseline.sh --fetch --data-turn`, then verify the S255 file hashes in
`SESSION_HANDOFF_255.md`'s Files table against the fetched repo.

The S254 open-cascade is fixed (D352): one file missing from the fetch no longer withholds the rest of
the overlay, so a red `fetch-verify` should now be accompanied by a handful of related failures rather
than twenty-five unrelated stack traces. If you ever do see a large number of failures again, read the
`fetch-verify` line first and check how many files it says were withheld.

## Assigned work: B93 turn 2 — the engine turn

Turn 1 (data) shipped at S254. `detachments.json` carries a structured `bearer_restriction` on every
enhancement record: verbatim clause, sentence index, scope (`model` / `unit` / `bare_name`),
alternatives (each a conjunctive term list), exclusions, an optional ability qualifier, and
`resolution` of `parsed` / `curated`. **Nothing in `index.html` reads it yet, so the live D0 gap is
exactly as wide as it was** — 369 records still over-admit today. This turn closes it.

**Turn type: engine-only.** Do not touch `detachments.json`, `detachment_parser.py` or the data
pipeline in this session.

Scope, from `B93_SCOPE.md` §7.2 and D335:

1. `enhancementBearerEligible()` gains a structured-rule branch alongside B113's curated one. A unit
   qualifies if it satisfies ANY alternative (all terms in that alternative) and NO exclusion, plus the
   ability qualifier where present.
2. `enhancementTypeEligible()` demotes from **gate** to **default** — applied when a record carries no
   clause, superseded when it does. **D335 governs, not D334:** the clause NARROWS within the
   Characters-only default, it does not replace it. Epic Hero stays an unconditional refusal.
3. **D199's fall-through is mandatory.** A restriction that cannot be evaluated against a unit's data
   must fall through to permissive, never refuse — 8 Character-typed units carry no Character keyword
   and 6 have more than one model group. Refusing on absent data is how a legal pick gets blocked.
4. Term matching must cover the same namespaces the data was tokenised against: `keyword_names`,
   `faction_keyword_names`, `model_keyword_names` and the unit name, case-folded and
   apostrophe-normalised. `chapter_keyword_additions` must be applied first (B132) or Dark Angels'
   Deathwing records regress to zero bearers.
5. B113's seven curated rows and B126's four mark rows are **subsumed** by the resolver in this turn.
   Do not leave both live reading the same records — that is two implementations of one rule.
6. New harness on the `b119_check.js` / `b126_check.js` pattern.

**Do not attempt turn 3 in the same session.** Pinning the 35 zero-admit and 73 one-admit regression
sets needs the engine's own resolution semantics and is its own turn.

## Precedents that will matter again

**Check whether a guard already exists before offering to add one.** D350 asked Ryan to choose between
three ways of guarding nine files, one of which was already in force. The wrong premise cost two
sessions and a reverted decision (D352). Before presenting options, verify the current state of each.

**An impossible census result means widen the read, never explain the result.** S254's restriction
counter came out at 1,261 against a known population of 739, because it counted inside the per-army
loop — 349 army slots, seven sharing the same generic Space Marines records. The number being
impossible was the entire signal.

**A scope document written in a prior session can be wrong about source facts.** `B93_SCOPE.md` §5
named three unresolvable cases; checking each at source showed one needed no curation at all
(`Harlequins` is a real keyword) and one had its rationale backwards (the `SPAWN` alias resolves a token
but changes no legality, because the unit is Beast-typed — B129 had this right and §5 did not).

**A loose parse is more dangerous than a failed one.** `B93-CENSUS`'s term-reality check exists because
a dropped or mis-split token produces a term matching nothing, and a term matching nothing silently
WIDENS a restriction. When extending anything here, ask which direction a bug fails in.

## Close

Four rolling documents updated (`40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
`SESSION_HANDOFF_256.md`), this file rewritten for S257, then:

1. add `SESSION_HANDOFF_256.md` to `pipeline_manifest.py`'s `GUARDED` list **before** writing
2. `python3 pipeline_manifest.py --write`
3. `python3 pipeline_manifest.py --freshness-check`

Those two commands are the literal last two of the session.

## Outstanding Ryan actions carried forward

**A render check covering three sessions' UI.** S248's Tank Ace checkbox, S249's Mark of Chaos selector,
S250's silent truncation of an over-cap tally on size reduction. S253, S254 and S255 shipped no UI, so
the backlog is unchanged at three. S250's is the one that matters most — it is the only one that edits a
saved list without telling the player. All three handoffs carry step-by-step scripts. This turn ships
engine behaviour that changes which enhancements appear against which units, so it will add a fourth.
