# NEXT SESSION PROMPT — Session 255

## Read first

`SESSION_HANDOFF_254.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

State at S254 close: `index.html` **v6.26** (unchanged — S254 was a data turn), decision log through
**D351**, `SCHEMA_VERSION` **5**, `rules_assertions.py` at **138** assertions, **24 open** backlog items.

## Open

Run `./baseline.sh --fetch --data-turn` — the assigned work below is an engine turn, but it reads
`detachments.json` closely enough that you want the repro gates live rather than skipped.

Then verify the S254 file hashes in `SESSION_HANDOFF_254.md`'s Files table against the fetched repo.

**If the baseline opens with a large number of failures, check for the cascade before believing any of
them.** `fetch-verify` aborts the whole overlay when any guarded file is missing from the fetch, so
`units.json`, `detachments.json`, `unit_loadouts.json` and `abilities.json` never arrive and roughly 25
gates crash with bare Node stack traces that look exactly like real failures. That is one problem, not
25. Read the `fetch-verify` line first. This is B139's item 3.

## Assigned work: B93 turn 2 — the engine turn

Turn 1 (data) shipped at S254. `detachments.json` now carries a structured `bearer_restriction` on
every enhancement record. Nothing in `index.html` reads it yet, so **the live D0 gap is exactly as wide
as it was** — 369 records still over-admit today.

**Turn type: engine-only.** Do not touch `detachments.json` or the parser in this session.

Scope, from `B93_SCOPE.md` §7.2 and D335:

1. `enhancementBearerEligible()` gains a structured-rule branch alongside B113's curated one. It reads
   the record's `bearer_restriction`: a unit qualifies if it satisfies ANY alternative (all terms in
   that alternative) and NO exclusion, plus the ability qualifier where present.
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

## Precedents from S254 that will matter again

**An impossible census result means widen the read, never explain the result.** The restriction counter
came out at 1,261 against a known population of 739, because it was counting inside the per-army loop —
349 army slots, seven of which share the same generic Space Marines records. The number being impossible
was the entire signal. Same lesson D334 learned expensively.

**A scope document written in a prior session can be wrong about source facts, even a careful one.**
`B93_SCOPE.md` §5 named three unresolvable cases; checking each at source showed one needed no curation
at all (`Harlequins` is a real keyword), and one had its rationale backwards — the `SPAWN` alias
resolves a token but changes no legality, because the unit is Beast-typed. B129 had this right and §5
did not. Re-derive from source, do not inherit.

**An assertion that reuses the producer's own extractor cannot detect the producer failing to extract.**
`B93-CENSUS` re-implements clause detection rather than importing `detachment_parser`. Keep that
separation if you extend it.

**A loose parse is more dangerous than a failed one.** The term-reality check exists because a dropped
or mis-split token produces a term matching nothing, and a term matching nothing silently WIDENS a
restriction. When extending anything in this area, ask which direction a bug fails in.

## Close

Four rolling documents updated (`40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
`SESSION_HANDOFF_255.md`), this file rewritten for S256, then:

1. add `SESSION_HANDOFF_255.md` to `pipeline_manifest.py`'s `GUARDED` list **before** writing
2. `python3 pipeline_manifest.py --write`
3. `python3 pipeline_manifest.py --freshness-check`

Those two commands are the literal last two of the session.

## Outstanding Ryan actions carried forward

**B139 needs a yes or no** — whether to drop the nine root CSVs from `pipeline_manifest.py`'s `GUARDED`
list and let `source_manifest.json` own them alone. Not blocking; it decides whether the S254 fetch
cascade can recur.

**A render check covering three sessions' UI.** S248's Tank Ace checkbox, S249's Mark of Chaos selector,
S250's silent truncation of an over-cap tally on size reduction. S253 and S254 shipped no UI, so the
backlog is unchanged. S250's is the one that matters most — it is the only one that edits a saved list
without telling the player. All three handoffs carry step-by-step scripts.
