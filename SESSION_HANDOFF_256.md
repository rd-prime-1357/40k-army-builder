# SESSION HANDOFF 256

**Turn type: engine.** B93 turn 2 shipped. `index.html` **v6.26 → v6.27**. No data file, parser or
pipeline script touched. `rules_assertions.py` stays at **138** assertions. Backlog **23 open**,
unchanged — B93 has two turns left.

## Session open — three gates failed, one cause

The project-area copy of `detachments_repro_check.py` was **stale**: four lines shorter than the repo
copy, missing the two source CSVs the B93 data turn added as tokenising inputs. The repo copy matches
`pipeline_manifest.json`; the project area was behind. Taking the repo copy cleared
`detachments_repro`, `rules_assertions` and `repo_check` together — 41/41 green before work started.

**Ryan action:** re-upload `detachments_repro_check.py` from the repo into the project area, or the
same three gates fail again at S257 open. Nothing else in the area diverged (`repo_check`: 236
byte-identical after the swap).

**One entry in S255's own hash table was wrong, and structurally always will be.**
`pipeline_manifest.py` reads `4b282eadd56a`, not the recorded `81c375310e9b` — the file was edited
once more after the table was written, when `SESSION_HANDOFF_255.md` was added to `GUARDED`. Fixed
here by adding the handoff to `GUARDED` **before** writing the Files table below, which is the order
the close sequence already implies but the docs did not spell out.

## What was found

**The assigned scope's item 2 contradicted itself, and I did not build it.** `B93_SCOPE.md` §7.2 and
`NEXT_SESSION_PROMPT.md` both said to demote `enhancementTypeEligible()` from gate to default,
"superseded when a record carries a clause", and in the same paragraph that **D335 governs, under
which the clause narrows *within* the Characters-only default**. §7 was written under D334 and never
rewritten when D335 reversed it the same session. **D335 governs; the Character gate is retained and
`enhancementTypeEligible()` is unchanged.** This was measured, not argued: under the retained gate
the resolver strands nothing that is not reachable another way.

*This is the second time in three sessions a stale premise in a prompt cost real work (D350 was the
first). When a prompt cites a decision and an instruction that disagree, the decision wins.*

**B113's `Bray Lord` curated row was refusing a legal bearer.** The clause is "Sorcerer or Infernal
Master model only". Both strings are real datasheet keywords, `Sorcerer In Terminator Armour` carries
`Sorcerer`, and "model only" is GW's keyword-scoped form throughout the 117-clause vocabulary. B113
curated it as two unit names. The resolver admits all three; the corrected set is pinned so it cannot
revert. **The other six B113 rows and all four B126 mark rows resolve identically** under the
resolver — checked one by one against the resolved pools, not assumed.

**53 zero-admit records, and none of them is a defect.** Over 1,145 army × record evaluations: 48
`Adeptus Astartes Vehicle model only` (12 armies × 4), reachable through the Tank Ace checkbox that
confers CHARACTER at muster — the case D334 got backwards; 4 Mark of Chaos records, reachable once a
mark is picked; and 1 Drukhari record, `Reaper's Cowl` / `Harlequins model only`, which has no bearer
because **Harlequins is not a built faction**. That one is honest and resolves itself when Harlequins
ships. 98 one-admit. Both figures pinned in the harness.

**No unit splits an exclusion keyword across model groups** — 24 multi-group units, four exclusion
terms, zero split cases. That is what makes a whole-unit exclusion reading equivalent to a per-group
one today, and it is now a gate rather than a belief.

## Decisions made

**D353.** Full reasoning in `40K_Decision_Log.md`. Three parts: the resolver ships and the curated
table is deleted; §7.2's type-gate demotion is not implemented (D335 governs); `Bray Lord`'s bearer
set is corrected.

**Product call made rather than asked, reversible in one line.** Bearer-ineligible rows stay in the
picker, **disabled with the clause as their reason**, rather than being dropped. That is the existing
E4c convention for every refusal except type-ineligibility, and a player who cannot see why a relic
is unavailable to this Character has been told less than nothing. Say the word and it flips.

## What shipped

**`index.html` v6.27.** `ENHANCEMENT_BEARER_RESTRICTIONS` and its eleven rows are **deleted**.
In their place a `── B93 ──` block: `bearerNorm` (case- and apostrophe-folding), `bearerTermSet`
(four namespaces — the three keyword fields via `markKeywordSet`, the datasheet name, and the entry's
effective Mark of Chaos), `bearerAbilitySet`, and rewritten `enhancementBearerRestriction` /
`enhancementBearerEligible` reading `detachments.json`'s structured field. `rawUnits` is already
chapter-resolved, so B132's restored Deathwing keyword is in scope. D199's fall-through is permissive
in all three places it arises; `bearerTermSet` skips empty strings deliberately, because a stray `''`
would make an unevaluable unit look evaluable and get it refused. `enhancementRefusalText` now shows
the clause verbatim — paraphrasing 117 clauses would be a second reading of the rule. Two stale
comment references to the deleted table, in the B99 and B119 blocks, updated.

**`b93_check.js` — net new.** Nine sections: field structure and the single-implementation check;
normalisation and the four namespaces; OR-of-AND alternatives, exclusions and the ability qualifier;
D199's fall-through in all three places **plus the negative control** that a unit with non-matching
keywords is still refused; the eleven formerly-curated records pinned to their resolved bearer sets;
the mark records (moved from `b126_check.js`); D335 proved through Tank Ace against real data; the
1,145-evaluation census pinned by cause; and the exclusion-split assumption.

**`rules_assertions.py` — E4b-7 restated in place**, same id, same 138 count, because the fact is
still legality-critical and only its subject moved. It now checks that
`ENHANCEMENT_BEARER_RESTRICTIONS` appears nowhere in `index.html`, that the resolver block is present
and still reads all four namespaces, that `Pact of Cursed Pinions` has not acquired a guessed clause,
and that `Butcher Lord`'s clause still resolves to the source-derived World Eaters Infantry
Characters.

**`b126_check.js`** loses item 8 (the four mark enhancements) and its slice of the deleted table.
That coverage lives in `b93_check.js` now, where the real enhancement records are loaded. One rule,
one test site.

**`baseline.sh`** gains the `b93_check` gate — 42 gates. **`pipeline_manifest.py`** gains
`b93_check.js` and `SESSION_HANDOFF_256.md` to `GUARDED`.

## Net New Files

`b93_check.js`. Everything else is a rolling document or a versioned update.

## Verified directly, not just through the gate

The eleven formerly-curated records were resolved against each army's real pool and compared unit by
unit with what the deleted table named. The 53 zero-admit records were each traced to a cause before
the reading was adopted, not after. The D335-versus-D334 question was decided by measuring both
readings against the whole population rather than by reading §7.2.

**Not verified this session: the render.** The picker's disabled-row behaviour changed for 641
records, and I cannot see the DOM.

## Files (SHA-256, first 12)

Verify these at S257 open.

| file | sha256:12 | note |
|------|-----------|------|
| `index.html` | `e03c1259f036` | **v6.27** — curated bearer table deleted, B93 resolver in its place |
| `b93_check.js` | `30a61d0f019d` | **net new** — nine sections, 42nd gate |
| `b126_check.js` | `4035c3257052` | item 8 moved to `b93_check.js` |
| `rules_assertions.py` | `70002af32614` | E4b-7 restated for the resolver; still 138 |
| `baseline.sh` | `78119b00c893` | `b93_check` gate added |
| `pipeline_manifest.py` | `f882821acd86` | `b93_check.js` + `SESSION_HANDOFF_256.md` guarded |
| `40K_Decision_Log.md` | `b5cb7ffcec8e` | D353 appended |
| `DECISION_INDEX.md` | `a9b18a068134` | D353 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `75344edc994b` | B93 turn 2 recorded; still 23 open |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_256.md` | (this file) | not self-referential; checked by `--freshness-check` |

Unchanged and not re-delivered: `detachments.json`, `detachment_parser.py`, `units.json`,
`detachment_effects.json`, `faction_taxonomy.json` — all as pushed after S255.

## Ryan action required

- **Re-upload `detachments_repro_check.py`** from the repo into the project area. The area copy is
  stale and fails three gates at open.
- **Push this session's files** to the public `40k-army-builder`: `index.html`, `b93_check.js`,
  `b126_check.js`, `rules_assertions.py`, `baseline.sh`, `pipeline_manifest.py`,
  `pipeline_manifest.json`, `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
  `SESSION_HANDOFF_256.md`, `NEXT_SESSION_PROMPT.md`.
- **The render check is now four sessions deep.** S248's Tank Ace checkbox, S249's Mark of Chaos
  selector, S250's silent truncation of an over-cap tally on size reduction, and now S256's
  enhancement picker. S250's is still the one that matters most — it is the only one that edits a
  saved list without telling the player. Scripts are in the three named handoffs; S256's script is in
  the next-session prompt.

## Decisions resolved this session

D353 — B93 turn 2. The resolver ships and the curated table is deleted; §7.2's type-gate demotion is
not implemented because D335 supersedes it; `Bray Lord`'s bearer set is corrected.

## Backlog

23 open at S255 close; **23 open at S256 close**. Nothing closed, nothing added — B93 stays open for
turns 3 and 4.
