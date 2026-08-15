# NEXT SESSION PROMPT — Session 245

## Recommended pick: B130, restore Deathwing/Ravenwing keywords onto the 6 generic-pool Characters when consumed by Dark Angels. Data turn — needs a full `--fetch --data-turn` baseline.

B131 (S244) fixed `b129_zero_bearer_gate`'s bearer-eligibility check and added the 6 Deathwing-
family records to its exemption list — the gate now correctly reflects that these records
currently have zero eligible bearers. **B130 is the actual product fix**: restore the Deathwing
keyword onto 5 named units and Ravenwing onto 1, for the specific case of a Dark Angels list,
without changing the shared generic-pool record's own keywords. Recommended shape (from
`B93_SCOPE.md` §12): a small restoration map, structurally the mirror of `SUBFACTION_KEYWORD_ARMY`
(which strips a sub-faction keyword when `army_of != owner`) — add the keyword back onto these 6
records at the point the Dark Angels union pool is resolved.

The 6 named units: Captain/Chaplain/Librarian In Terminator Armour, Ancient In Terminator Armour,
Bladeguard Ancient (Deathwing); Chaplain On Bike (Ravenwing). Full derivation already on record —
`B93_SCOPE.md` §12 and Decision Log D340 — this should not need a re-derivation from source.

**After B130 ships, B131's EXEMPT block becomes stale and should be removed** — a small follow-up
tooling pass. Note that dependency when scoping B130's session so it isn't forgotten.

## Also open, at your discretion — 25 tickets

B126, B127, B128, B116, B120, B122, B124, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75,
P2, P4, E23, B67b, E12, B17. **Nothing is decision-blocked.**

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

- The last full `--fetch --data-turn` was **S240**, clean at 36/36. S241–S244 were tooling/engine/
  scoping turns and ran with only what each needed loaded. Run a full `--fetch --data-turn` at the
  next real data session — **B130 qualifies and should get one.**
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- **Manifest pushes need a real diff check going forward (D337) — this bit S244 for real.**
  S243's `--write` output (`pipeline_manifest.json`) was never pushed, so S244's session-open
  baseline failed both `rules_assertions` and `pipeline_manifest` on a stale manifest before any
  new work started. Before trusting a handoff's Files table at session open, verify the actual
  pushed file's hash against the table — and confirm `pipeline_manifest.json` itself is among
  what actually landed, not just the files a session's prose lists as "changed."
- The project-area file mount silently strips apostrophes from filenames on upload. Before trusting
  a project-area filename as the real repo filename, especially for anything going into GUARDED,
  check a fresh clone.
- **Read `rule_text`, not just `restrictions`.** `restrictions` is a partial extraction of
  `rule_text`, not a substitute, and is `null` on plenty of detachments that do carry rules. Both
  are documented in `40K_Data_Dictionary.md`'s S241 addendum.
- **An impossible result means widen the read, never explain the result.** No inference about what
  GW must have intended while any field is still unread (D334/D336). S244 extended this principle
  one level deeper: a *gate script's own internal logic* can carry the same read-the-wrong-field
  bug as a manual census. When a gate's own re-derivation contradicts a hash-verified prior
  finding, check what the gate is actually reading before trusting either side.
- **Field-coverage convention is written into `40K_Data_Dictionary.md`'s front matter (S241).**
  State every field on a record type and mark read/not-read, with a reason for each not-read,
  before censusing that file for a legality question.
- **B123's precedence mechanism (D335) has no known live collision case yet.** If a future census
  (B120, B122, or a new faction build) turns up a record where wargear and an Enhancement really
  do compete for the same SV/FNP/W cell, `enh.condAbs` and the comparator (`B123_BETTER`) are
  already built and tested — extend the curated table, don't re-derive the mechanism.
- **A ticket scoped as small can still turn out deeper (S244, B131).** When that happens: verify
  the deeper fix doesn't disturb anything already working (check individually, not just "gate
  still passes"), then ship it in full rather than a half-fix that fails its own gate — a
  stopped-and-reverted broken change was tried first this session and correctly not shipped.

## Ryan action required

- **Push S244's changed files** to the public repo: `rules_assertions.py`, `pipeline_manifest.py`,
  `pipeline_manifest.json`, `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
  `SESSION_HANDOFF_244.md`, `NEXT_SESSION_PROMPT.md`.
- **`pipeline_manifest.json` must be included this time.** Its omission from S243's push is what
  caused S244's baseline to fail at open. Please double-check it specifically lands as edited.

## Decisions waiting on Ryan

**Resolved at S244, listed so they are not re-asked:** none new needing Ryan — D341 (B131's gate
mechanism fixed, stale manifest reconciled) was a technical call, not a product one.

- **Next faction after Drukhari** — unchanged since S240. Recommendation stands: clear the engine
  backlog first. B116's reclassification means **Aeldari is now a production dependency** even
  though it is not in the priority order, and belongs on a release plan rather than being
  rediscovered later.

## Close

Produce the four documents, register `SESSION_HANDOFF_245.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
