# NEXT SESSION PROMPT — Session 244

## Recommended pick: B131, correct B129's zero-bearer exemption list and docstring. Tooling-only,
small — mechanical, moderate effort is enough.

B125 (S243) closed with a hash-verified finding: `units.json` gives zero eligible Characters for
all 6 Deathwing-family enhancement records today (5 for the 4 `Deathwing model only` clauses, plus
the 2 "...with the Deep Strike ability only" clauses share the same root cause). B129's gate
currently excludes these 6 from its exemption list because D338's read used a raw-CSV check that
doesn't reflect what's actually in the built data. Fix: add the 6 records to
`b129_zero_bearer_gate`'s `EXEMPT` set (30 -> 36) and correct its docstring's D338 paragraph to
point at `B93_SCOPE.md` §12 instead of restating the now-superseded finding. Read `B93_SCOPE.md`
§12 and `40K_Decision_Log.md`'s D340 first — both already have the record names and the reasoning
written out; this should not need a re-derivation from source.

**Do not build B130 in the same session.** B130 (the actual keyword-restoration fix) is a data
turn — a different type from B131's tooling turn — and turn typing forbids mixing them. B130 is
next after B131, in its own session.

## Also open, at your discretion — 26 tickets

B126, B127, B128, B116, B120, B122, B124, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75,
P2, P4, E23, B67b, E12, B17, B130, B131. **Nothing is decision-blocked.**

- **B130** (Deathwing/Ravenwing keyword restoration) — do this right after B131, as its own data
  turn. `B93_SCOPE.md` §12 has the exact 6 records and the recommended mechanism (a small map
  mirroring `SUBFACTION_KEYWORD_ARMY` in reverse, applied when the Dark Angels union pool is
  resolved). After it ships, a small follow-up tooling pass should remove B131's now-unnecessary
  exemption entries — note that when scoping B130's session so it isn't forgotten.
- **B126** (Marks of Chaos) is a feature, not a fix — mark selection, list persistence, plus two
  unenforced D0 rules of its own (attachment and Transport must share a mark). Same shape as B128:
  a muster-time selection that changes a unit's keywords. Worth reading B128's re-scoped entry
  before writing B126's, so the two do not invent different mechanisms for the same problem.
- **B127** (74 records with no rule text in any held source) needs nothing from Claude until
  source exists — a Ryan-side acquisition item.
- **B120** still needs its own scoping turn before build; per S238's note, widen its census from
  Set D *weapons* to Set D effects generally so **B124** lands inside it.
- **B122** needs a scoping turn answering a source question first: does the held Chaos Daemons
  material contain the real enhancement text at all, or only shorthand summaries (distinct from
  B127's 74 records, which have none at all)?
- **B128** (muster-time detachment keyword conferral) — re-scoped smaller by D339 (S241).
  `detachment_effects.json` already models 7 `battleline` effects (`enforced: true`, live) and
  Headhunter Task Force's `tank_ace` (scoped since D273/S182). Read that file's `_meta` before
  re-censusing `rule_text` — most of the scoping work for the automatic conferrals is very likely
  already done; the genuine remaining gap is Headhunter's player-choice-with-a-cap mechanism.

## Standing reminders

- The last full `--fetch --data-turn` was **S240**, clean at 36/36. S241, S242 and S243 were
  tooling/engine/scoping turns and ran with only what each needed loaded. Run a full
  `--fetch --data-turn` at the next real data session (B130 qualifies).
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- **Manifest pushes need a real diff check going forward (D337).** Before trusting a handoff's
  Files table at session open, verify the actual pushed file's hash against the table, not just
  that the file exists.
- The project-area file mount silently strips apostrophes from filenames on upload. Before trusting
  a project-area filename as the real repo filename, especially for anything going into GUARDED,
  check a fresh clone.
- **Read `rule_text`, not just `restrictions`.** `restrictions` is a partial extraction of
  `rule_text`, not a substitute, and is `null` on plenty of detachments that do carry rules. Both
  are documented in `40K_Data_Dictionary.md`'s S241 addendum.
- **An impossible result means widen the read, never explain the result.** No inference about what
  GW must have intended while any field is still unread (D334/D336) — this is what closed B125:
  checking the actual built `units.json` instead of reasoning from either prior census's framing.
- **Field-coverage convention is written into `40K_Data_Dictionary.md`'s front matter (S241).**
  State every field on a record type and mark read/not-read, with a reason for each not-read,
  before censusing that file for a legality question.
- Turn typing stays strict. B131 is tooling-only; do not fold B130's data fix into it even though
  the combined change is small.
- **B123's precedence mechanism (D335) has no known live collision case yet.** If a future census
  (B120, B122, or a new faction build) turns up a record where wargear and an Enhancement really
  do compete for the same SV/FNP/W cell, `enh.condAbs` and the comparator (`B123_BETTER`) are
  already built and tested — extend the curated table, don't re-derive the mechanism.

## Ryan action required

- **Push S243's changed files** to the public repo: `B93_SCOPE.md`, `40K_Decision_Log.md`,
  `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `SESSION_HANDOFF_243.md`,
  `NEXT_SESSION_PROMPT.md`. Given D337, please verify `pipeline_manifest.py` specifically lands as
  edited.

## Decisions waiting on Ryan

**Resolved at S243, listed so they are not re-asked:** none new needing Ryan — D340 (B125 closed,
D338 reconciled) was grounded entirely in hash-verified source and the built JSON.

- **Next faction after Drukhari** — unchanged since S240. Recommendation stands: clear the engine
  backlog first. B116's reclassification means **Aeldari is now a production dependency** even
  though it is not in the priority order, and belongs on a release plan rather than being
  rediscovered later.

## Close

Produce the four documents, register `SESSION_HANDOFF_244.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
