# SESSION HANDOFF 241

**Turn type:** tooling-only. `detachments.json`, `units.json` and all other engine/data outputs
untouched; `index.html` untouched. Changed: `40K_Data_Dictionary.md`, `rules_assertions.py`,
`pipeline_manifest.py` (both the reconciliation fix and the routine registration of this
session's changed files), `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
this handoff, and `NEXT_SESSION_PROMPT.md`.

## What happened

1. **Open — gate failure, reconciled before starting (D337).** `SESSION_HANDOFF_240.md` states
   `B93_SCOPE.md` and itself were registered in GUARDED before `--write` ran. `pipeline_manifest.json`
   confirms this happened (both present, correct hashes). The pushed `pipeline_manifest.py` did not
   contain either entry, and its own hash did not match S240's table — the edited copy and the
   pushed copy were two different files. Re-added both entries, verified against a fresh clone.
   Baseline after the fix: 31/33 gates pass (3 tier-B repro checks skip, sources not loaded this
   session — tooling turn, not a data turn), the only "failures" being the expected self-referential
   hash mismatch on files this session edits, resolved by `--write` below.

2. **B129, part 1 — documented the four previously-undocumented outputs.** `40K_Data_Dictionary.md`
   gains a section for `detachments.json` (15 detachment-record fields, 6 enhancement-sub-record
   fields, 4 stratagem-sub-record fields — `rule_text`, `restrictions`, enhancement `description`
   and stratagem `description` flagged as rules-bearing free text), `detachment_effects.json`
   (structure documented; its own `_meta` already self-documents the rest, read rather than
   duplicated), `datasheet_wargear_abilities.json` (flat ability-description dict, flagged
   rules-bearing) and `wargear_points.json` (self-documenting via its own `_meta`/`_addons`, no
   rules-bearing field). None had an entry before this session despite `detachments.json` alone
   carrying 211 detachment and 739 enhancement records.

3. **B129, part 2 — field-coverage convention.** Written into the data dictionary's own front
   matter: before censusing any file for a legality question, state every field on the record type
   and mark each read or not-read, with a reason for each not-read.

4. **B129, part 3 — the gate, `rules_assertions.py`'s `B129`.** Independently re-derives bearer
   eligibility from source (not from the engine, which does not implement bearer-restriction
   clauses yet) and fails if any non-Upgrade enhancement resolves to zero eligible Characters
   without a named, commented exemption. Building it required an actual clause resolver —
   vocabulary-derived keyword tokenisation (a hand-picked phrase list undercounted badly; "Death
   Company," "Crusade Ancient," "Lord of Poxes" and more are themselves real multi-word keywords
   already in source), "/" slash-distribution over the shared tail (the INFANTRY/MOUNTED trap),
   and D335's narrow-within-Character rule applied exactly. Verified against the 641-record,
   117-string clause population `B93_SCOPE.md` already established, and negative-tested: removing
   the Vehicle exemption for Astartes Tank Ace made the gate fail and name that exact record.

5. **Two corrections surfaced by building the gate, not by re-auditing anything on purpose (D338,
   D339).** Re-deriving the exemption population, rather than copying the prompt's "24 + 6 + 4 = 34"
   figure, found it is **30, not 34**:
   - The 6 Deathwing records do not hold up. Direct read of `Datasheets_keywords.csv`
     (`S.all_keywords()`, the same method `b113_bearer_table_matches_source` already uses) finds 5
     Dark Angels Characters carrying the Deathwing keyword, all present in `units.json`. This
     contradicts `B93_SCOPE.md` §4.2's "resolves to zero eligible Characters." Left out of the
     gate's exemption list on that basis, and flagged for B125's scoping turn to reconcile rather
     than re-open from a blank page — either B125 finds the engine actually consults a different,
     stripped keyword representation at bearer-assignment time (in which case these 6 belong back
     in and this session's gate is wrong), or the original gap was narrower than stated.
   - The Spawn record's real cause is a cross-faction keyword homonym (Thousand Sons' own "Chaos
     Spawn" datasheet lacks the bare `Spawn` keyword that an unrelated World Eaters datasheet of
     the same display name carries — but it does carry the compound `Chaos Spawn`, so §5's
     recommended alias would in fact resolve it), not a unit-type gap as I first concluded and then
     corrected mid-build. Not built — a curation entry is data-turn work — but the docstring states
     the true cause rather than the original framing.

6. **Unplanned finding while documenting `detachment_effects.json` (D339).** It already carries 7
   `battleline` effects with `enforced: true` — live in the engine today — and Headhunter Task
   Force's `tank_ace` effect, fully scoped (pool, cap, source citation) back at **D273 (S182)**,
   re-verified S187. This contradicts S240's B128 census, which states "None is modelled." B128
   itself was not re-scoped this session (out of turn-type), but its entry in the backlog now
   carries this correction, and its next scoping turn should start from `detachment_effects.json`'s
   own `_meta` rather than re-censusing `rule_text` from zero.

7. **Close.** Baseline re-run clean (31/33, 2 tier-B skips — sources not needed for close).
   `--write`, then `--freshness-check` as the last two commands, in that order.

## Ryan action required

- **Push this session's changed files** to the public repo: `40K_Data_Dictionary.md`,
  `rules_assertions.py`, `pipeline_manifest.py`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_241.md`, `NEXT_SESSION_PROMPT.md`. Given D337, please
  double-check `pipeline_manifest.py` specifically lands as edited — that is exactly the file that
  went out of sync last time.
- Nothing needs your eyeball — no render changed, `index.html` untouched.

## Decisions resolved this session

- **D337.** Manifest reconciliation — S240's pushed `pipeline_manifest.py` was missing GUARDED
  entries its own handoff said were added. Fixed at open.
- **D338.** B129's zero-bearer gate built. Re-derived exemption population is 30 (not 34): the 6
  Deathwing records do not hold up against direct source verification; flagged for B125. Spawn's
  true cause corrected (cross-faction homonym, not unit-type).
- **D339.** B128's "None is modelled" does not hold — `detachment_effects.json` already models 7
  `battleline` effects (enforced) and Headhunter's `tank_ace` (scoped since D273/S182). B128's
  scoping turn should read that file first.

## Decisions waiting on Ryan

- **Next faction after Drukhari** — unchanged from S240. Recommendation stands: clear the engine
  backlog first; B116's Aeldari dependency belongs on a release plan.

## Files (SHA-256, first 12)

Verify these at S242 open.

| file | sha256:12 | note |
|------|-----------|------|
| `40K_Data_Dictionary.md` | `115ba549db2c` | detachments.json/detachment_effects.json/datasheet_wargear_abilities.json/wargear_points.json documented; field-coverage convention in front matter |
| `rules_assertions.py` | `63470a7fd6fa` | `B129` gate added, registered in ASSERTIONS |
| `pipeline_manifest.py` | `f225544a21fb` | D337 fix (B93_SCOPE.md, SESSION_HANDOFF_240.md restored) + SESSION_HANDOFF_241.md registered |
| `40K_Decision_Log.md` | `fc2f3b13744d` | D337, D338, D339 appended |
| `DECISION_INDEX.md` | `756b863ee11b` | D337, D338, D339 one-liners appended |
| `OPEN_ITEMS_BACKLOG.md` | `169b8ce245a9` | B129 moved to Closed/Shipped; B128 entry corrected; 27 → 26 |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_241.md` | (this file) | not self-referential; checked by `--freshness-check` |

### Net New Files

None. All seven changed files are updates to files the project already held in that role.

## Backlog

27 open at S240 close; **26 open at S241 close** (B129 resolved; nothing added).

Beginning: B125, B126, B127, B128, B129, B116, B120, B122, B123, B124, B97, B103, E28, B93, B90,
B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (27).
Resolved: B129 (1).
Added: none (0).
Ending: B125, B126, B127, B128, B116, B120, B122, B123, B124, B97, B103, E28, B93, B90, B94, B85,
B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17 (26).

Nothing is decision-blocked. B123 is next (statline precedence build, decided at D335, engine-only)
per S240's plan — B129 was the prerequisite tooling turn and is now done.
