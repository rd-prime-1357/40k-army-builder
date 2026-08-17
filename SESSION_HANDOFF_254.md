# SESSION HANDOFF 254

**Turn type: data.** B93 turn 1 of 4 — parsing every enhancement's bearer-restriction clause into
`detachments.json`. No engine work; `index.html` is untouched at **v6.26**. The new `B93-CENSUS`
assertion ships with the data it describes, per `B93_SCOPE.md` §7.3.

## Session open — did not pass, and the cause was external

`./baseline.sh --fetch` reported **26/40 gates failed**. That was one cascade, not 26 problems.
S253's nine Chaos Daemons root CSVs had not reached the public repo, and `fetch-verify` aborts the
entire overlay when any guarded file is absent from the fetch — so `units.json`, `detachments.json`,
`unit_loadouts.json` and `abilities.json` were never brought into the workspace, and every gate that
reads them crashed with a bare Node stack trace that reads identically to a real failure.

Everything else from S253 was pushed and correct: all 230 other guarded files present and hash-matching
`pipeline_manifest.json`, `.gitignore`'s nine negation lines in place and correctly ordered after
`*.csv`, and zero drift between the project area and the manifest on all 95 locally-resident files.

**Diagnosed from the GitHub API rather than guessed at.** The 22:33 UTC commit `4122a6f8` ("Add files
via upload") is empty — 0 files, 0 additions, 0 deletions. At that moment the repo's `.gitignore` still
carried a bare `*.csv` with no exceptions, because the `.gitignore` uploaded at 22:25 had landed under
the filename `download` (the browser had saved it without its name; confirmed by fetching that file's
contents at that commit — byte-for-byte our `.gitignore`). The exceptions only landed at 22:39, by
direct web edit. Subsequent upload attempts were going to the **private** `rd-prime-1357-data-sources`
repo rather than the public `40k-army-builder` — three no-op commits there at 22:45, 23:16 and 23:18,
all zero-change because the files were already present. Ryan then pushed to the correct repo.

**After the push: clean fetch, `--fetch --data-turn`, 41/41 gates pass.** Work started from that state.

## What was found

**The S240 census reproduces exactly against today's data**, re-derived at open rather than inherited:
739 enhancement records, 641 carrying a bearer clause, 117 distinct clause strings, clause at sentence
position 0/1/2 for 439/183/19 records, 74 description-empty, 24 Chaos Daemons shorthand. Every figure
in `B93_SCOPE.md` §2 and §3 holds.

**B93 was chosen over B90 — a sequencing call the S254 prompt left open.** B93's stated gates are
effectively clear (B125 closed S243, B126 shipped S249, B128 shipped S248), and B127 — the one still
open — is a source-acquisition cap rather than a build blocker: its 74 records carry no clause to
parse, so they fall through to the existing Character default, which is correct. B90 turn 2 still needs
a per-chapter roster build path that does not exist and was deferred once at S186 for exactly that
reason; it needs its own scoping turn first. B93 also covers the wider live D0 surface — 369
over-admitting records across 13 of 14 armies against B90's five chapters in one family.

**Three corrections to `B93_SCOPE.md` §5, each checked at source, all recorded in D351.**
`Harlequins` is a real faction keyword in `Datasheets_keywords.csv` and needs no curation — it has no
bearers only because the faction is unbuilt, which is correct behaviour. `SPEEDER` is confirmed absent
from all 1,423 keywords and is the only genuinely unresolvable token. The `SPAWN` case is a GW source
inconsistency, not a naming mismatch on our side — across all seven Chaos Spawn datasheets, World
Eaters' carries `Spawn` and every other faction's carries `Chaos Spawn` — and per B129's own
re-derivation the alias buys a clean parse, not a bearer: Thousand Sons' Chaos Spawn is Beast-typed, so
under D335 the record stays zero-admit and keeps its B129 exemption. §5's framing of that alias as a fix
is wrong; B129's reading is right.

**The slash trap is one grammar rule, not a curated map.** `INFANTRY/MOUNTED THOUSAND SONS PSYKER` and
`SORCERER/EXALTED SORCERER` share a surface shape and parse differently. Treating the slash as
alternating the HEAD term over a shared tail is correct for both — the second simply has an empty tail,
because `Exalted Sorcerer` is itself a two-word keyword.

**A counting bug found mid-build.** The first cut counted restrictions inside the per-army loop, which
runs once per army SLOT (349) rather than per distinct record (739); seven armies share the same generic
Space Marines records, so totals came out at 1,261. The tell was that the total exceeded the known
population. Counters now derive from the deduplicated catalogue.

## Decisions made

**D351.** Full reasoning in `40K_Decision_Log.md`. The one call worth naming here: **`or` and `,`
alternation does not distribute a shared prefix** — `Adeptus Astartes Terminator or Gravis model only`
emits as (Adeptus Astartes AND Terminator) OR (Gravis). Verified, not assumed: both readings were
resolved against every army pool for all 13 army-scoped multi-alternative clauses and the admitted
bearer sets are identical in every case, because an enhancement is always scoped to one army and every
unit in it already carries the faction keyword. Non-distributing was chosen because it needs no rule
about how far a prefix reaches.

## What shipped

**`detachment_parser.py`.** A new section 3b emits a `bearer_restriction` per enhancement record —
`null`, or an object carrying the verbatim clause, its sentence index, a scope of `model` / `unit` /
`bare_name`, alternatives (each a conjunctive term list), exclusions, an optional ability qualifier, and
`resolution` of `parsed` / `curated`. The parser is **total**: every clause parses completely or the
build stops, because a partly-parsed restriction is indistinguishable from a correctly-parsed looser one
and loose is the direction that ships an illegal list. Two curations only, both commented and pinned:
SPEEDER (source-derived from the Adeptus Astartes datasheets whose name contains "Speeder", so a later
chapter build picks up its own without editing this file) and SPAWN. Two `_meta` counters added.

**It names terms, never units.** No roster resolution happens at build time, because which units satisfy
a term depends on chapter keyword restoration (B132), muster-time conferral (B128) and Marks of Chaos
(B126) — all engine-time state. Resolving here would bake a snapshot of all three.

**`detachments.json`.** Regenerated. 628 parsed, 13 curated, 98 no clause — 641 with a clause, matching
the census. Diff-guarded before promotion: the file differs from the committed copy in exactly two ways,
the new key on each enhancement and the two `_meta` counters. Zero other field changes across all 211
catalogue records; army index unchanged.

**`detachments_repro_check.py`.** `Datasheets_keywords.csv` and `Datasheets.csv` added to `REQUIRED` —
the term vocabulary. Both are read only to tokenise clauses; no unit, points or roster data is taken
from either.

**`rules_assertions.py`.** `B93-CENSUS` added (tier B). It re-derives clause detection from the
description text independently of the parser — deliberately not by importing it, since an assertion that
reuses the producer's extractor cannot detect the producer failing to extract — and checks coverage in
both directions, the pinned population, that every emitted term is a real `Datasheets_keywords.csv`
keyword or `Datasheets.csv` name, and that both curations still hold (including that SPEEDER is still
absent from source, so a refresh that adds it fails rather than leaving the curation shadowing real
data). **138 assertions, all pass.**

**`OPEN_ITEMS_BACKLOG.md`.** B93 progress note added and the next turn scoped; **B139 opened**; header
count 23 → 24.

**`40K_Decision_Log.md` / `DECISION_INDEX.md`.** D351 appended to both.

## Net New Files

None. `SESSION_HANDOFF_254.md` is a rolling document; every other file touched already existed.

## Verified directly, not just through the gate

Negative-tested `B93-CENSUS` per project precedent (S251/`B94-2`), twice and in both failure
directions: dropping one record's `bearer_restriction` was caught, and loosening one alternative into
two non-existent terms (`Adeptus` + `Astartes`) was caught by the term-reality check. Restored and
re-run clean.

`detachments_repro_check.py` reproduces the promoted `detachments.json` byte-for-byte from a fresh
parser run.

Full baseline after the change: **36/39 gates pass**, with the three failures being expected
mid-session staleness on exactly the four files edited this session (`pipeline_manifest`,
`rules_assertions`'s P3, and `repo_check`). Resolved by the manifest write at close and Ryan's push.

**Not verified this session:** nothing requiring a browser; no UI changed. The three-deep unseen-UI
backlog from S248/S249/S250 is unchanged.

## Files (SHA-256, first 12)

Verify these at S255 open.

| file | sha256:12 | note |
|------|-----------|------|
| `detachment_parser.py` | `46f0ee79706c` | section 3b: bearer-restriction parser, total, two curations |
| `detachments.json` | `fd160d4ae14b` | `bearer_restriction` on all 739 enhancement records; two `_meta` counters |
| `rules_assertions.py` | `ed31bf1764e2` | `B93-CENSUS` added (tier B); 138 assertions |
| `detachments_repro_check.py` | `3e4ff28de0fe` | `Datasheets_keywords.csv` + `Datasheets.csv` added to `REQUIRED` |
| `40K_Decision_Log.md` | `a35a71fcc602` | D351 appended |
| `DECISION_INDEX.md` | `8a4235bf94ce` | D351 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `9b4bfe8bfb31` | B93 progress; B139 opened; header 23 → 24 |
| `pipeline_manifest.py` | (regen at close) | `SESSION_HANDOFF_254.md` appended to `GUARDED` |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_254.md` | (this file) | not self-referential; checked by `--freshness-check` |

## Ryan action required

- **Push this session's changed files** to the public repo: `detachment_parser.py`,
  `detachments.json`, `rules_assertions.py`, `detachments_repro_check.py`, `40K_Decision_Log.md`,
  `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `SESSION_HANDOFF_254.md`, `NEXT_SESSION_PROMPT.md`. **Public `40k-army-builder`, not the private
  data-sources repo** — that mix-up cost most of this session.
- **B139 carries a recommendation that needs a yes or no** (drop the nine from `GUARDED` and let
  `source_manifest.json` own them alone). Not blocking; it decides whether the fetch cascade can recur.
- **The render check from S248/S249/S250 is still outstanding.** This session shipped no UI. S250's is
  still the one that matters — it silently edits a saved list.

## Decisions resolved this session

D351 — B93's data turn: every enhancement's bearer-restriction clause parsed into a structured field in
`detachments.json`, pinned by a new `B93-CENSUS` assertion, with three `B93_SCOPE.md` §5 corrections
and the alternation-distribution question settled by measurement.

## Backlog

23 open at S253 close; **24 open at S254 close**. B139 opened. B93 progressed and remains open.
