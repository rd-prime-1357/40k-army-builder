# SESSION HANDOFF 257

**Turn type: tooling.** B93 turn 3 shipped. `index.html` untouched — stays **v6.27**. No data file
or parser touched. `rules_assertions.py` **138 → 139** assertions. Backlog **23 open**, unchanged —
B93 has one turn left.

## Session open — the same stale file, again

`detachments_repro_check.py` in the project area was still the pre-S256 copy — Ryan's re-upload
did not happen between sessions. Took the repo copy again, same as S256. **This is now the second
consecutive session this has cost an open-time detour; see Ryan action below.** Baseline otherwise
clean: 42/42 gates, all eleven S256 file hashes verified byte-identical against the fetched repo.

## What was built — B93 turn 3, the independent second census

`b93_check.js` (S256) already pins the admit-count census from the engine side: 1,145 army x record
evaluations, 53 zero-admit across six known-cause clauses, 98 one-admit. Turn 3's job was the
independent second derivation — re-deriving the same numbers from `detachments.json` and
`units.json` directly, in Python, without loading any JavaScript, so a bug shared between the two
derivations cannot cancel out and pass silently.

**New `B93-ENGINE-CENSUS` assertion.** A fresh Python re-implementation (not a port) of
`bearerNorm`/`markKeywordSet`/`bearerAbilitySet`/`markEffect`/`unitInnateMark`/`unitNeedsMark`/
`entryEffectiveMark`/`enhancementBearerEligible`, evaluated against every **built faction's own**
`resolved_pool()` — all twelve Space Marines armies (mirroring the per-chapter union and both
per-chapter maps) plus all eight non-Astartes built factions. Entries carry no Tank Ace pick and no
player mark pick, matching `b93_check.js`'s own `entry()` helper exactly.

**The two derivations agree exactly.** 1,145 evaluated; 53 zero-admit in the same six clauses at the
same per-clause counts (48 Vehicle, 4 marks, 1 Harlequins); 98 one-admit. The one-admit set is pinned
by `(detachment_key, enhancement_name, bearer_name)` triple — 68 distinct triples, five of which
repeat exactly 7 times each across the Adeptus Astartes armies that share a detachment key with no
chapter override (Techmarine x2, Chaplain On Bike x3) — rather than by count alone, because a count
alone would not catch a resolver regression that swaps which unit an enhancement resolves to while
leaving the total unchanged.

## What was found — B129's own exemption list was stale, and passing for the wrong reason

Building the cross-check surfaced a real disagreement, one level down from the assigned task: this
new census and the older **B129** (S241) disagreed on one record. B129 carried
`Thousand Sons|SERVANTS OF CHANGE`'s `Thicket of Bladed Bone` (`SPAWN unit only`) as a named
zero-admit exemption, reasoning the target unit is Beast-typed and therefore not a Character — the
same framing D351 used at the data turn ("the alias buys a clean parse rather than a bearer"). **That
reasoning overlooked that the record is an Upgrade.** Upgrades bypass the Character gate entirely per
the Muster Rules' own exemption — they go to any unit type. A Spawn-only Upgrade reaching a
Beast-typed Spawn unit is exactly correct, not a gap.

The shipped resolver has always gotten this right, because it reads `detachments.json`'s own curated
SPAWN/Chaos Spawn alias directly. B129's separate, older from-scratch parser did not know that alias
and independently computed zero too — but for an unrelated reason (its tokeniser only recognises the
literal keyword "Spawn," a coincidental unrelated World Eaters keyword, not the "Chaos Spawn" the
Thousand Sons unit actually carries) — so the exemption's stated reasoning and the parser's actual
output happened to agree, and B129 kept passing while documenting a gap that was never real.

**Fixed in B129 itself**, not restated in the new assertion: `parse_clause`'s tokeniser now carries
the same one-entry SPAWN/Chaos Spawn alias `detachment_parser.py` already carries in the shipped
field, mirrored rather than re-derived. With it, B129's own independent derivation now finds the same
one bearer this session's census and `b93_check.js` both find — `Chaos Spawn Beast`. The exemption
entry is removed (**30 → 29** named exemptions, verified by re-running with the entry gone). B129's
registration text also had a second, smaller staleness — it claimed every checked record needs "a
Character bearer," which is wrong for the Upgrade records the function itself already evaluates
against any unit type — corrected in the same pass.

## What shipped

**`rules_assertions.py`.** New `b93_engine_bearer_census()` / `B93-ENGINE-CENSUS` (138 → 139).
`b129_zero_bearer_gate()` corrected: SPAWN/Chaos Spawn alias added to its tokeniser, the stale
exemption removed, docstring and registration text both rewritten to explain the finding rather than
the earlier (now-wrong) framing.

**`pipeline_manifest.py`.** New FILES-TABLE ORDERING doc section (the "worth doing if it fits" item
from S256's prompt): this file is edited twice at close — once for the GUARDED append, and its own
hash is also a row in the handoff's Files table — so the append must land before the table is
written, or the recorded hash is wrong the moment the append happens next (S255's mistake, S256's ad
hoc fix). Written down instead of relying on session memory a third time. `SESSION_HANDOFF_257.md`
added to `GUARDED`.

**`40K_Decision_Log.md` / `DECISION_INDEX.md`.** D354 appended, covering both the new census and the
B129 correction.

## Net New Files

None. Every file this session touched already existed in the project.

## Verified directly, not just through the gate

The independent Python census was run standalone before being wired into `rules_assertions.py`,
confirmed to reproduce 1,145 / 53 / 98 exactly against the shipped `detachments.json`. B129 was run
standalone before and after the fix — before: passing with the stale exemption; after: passing with
29 exemptions and the SPAWN record resolving to one real bearer, not zero. Full baseline re-run after
both changes: 42/42 (the mid-session run showed the expected P3/manifest/repo_check cascade from the
unregenerated manifest — that clears at close per the documented order above).

## Ryan action required

**`detachments_repro_check.py` re-upload is now two sessions overdue.** S256 asked for this; it had
not happened by S257 open, and the repo copy was taken again. If this is a five-minute task that
keeps getting missed, say so and I'll drop it from the ask entirely and just always pull the repo
copy at open — the current pattern costs a detour every session for no benefit, since the repo copy
is always taken anyway.

**Same outstanding render check, one session further along — five sessions now.** S248's Tank Ace
checkbox, S249's Mark of Chaos selector, S250's silent truncation of an over-cap tally, S256's
enhancement picker. S250's is still the one that matters most. Script is in S256's handoff and the
prior `NEXT_SESSION_PROMPT.md`; nothing new to check from this session, since it touched no rendered
UI.

**Push this session's files** to the public `40k-army-builder`: `rules_assertions.py`,
`pipeline_manifest.py`, `pipeline_manifest.json`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
`OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_257.md`, `NEXT_SESSION_PROMPT.md`.

## Decisions resolved this session

D354 — B93 turn 3. The independent Python census agrees exactly with `b93_check.js`'s engine-side
derivation. Cross-checking it exposed a stale B129 exemption (an Upgrade record mistakenly reasoned
under the Character gate); fixed in B129, not restated.

## Backlog

23 open at S256 close; **23 open at S257 close**. Nothing closed, nothing added — B93 stays open for
turn 4.

## Files (SHA-256, first 12)

Verify these at S258 open.

| file | sha256:12 | note |
|------|-----------|------|
| `rules_assertions.py` | `77590840a0a5` | 139 assertions — new B93-ENGINE-CENSUS, B129 corrected |
| `pipeline_manifest.py` | `126f77b74600` | FILES-TABLE ORDERING note; SESSION_HANDOFF_257.md guarded |
| `40K_Decision_Log.md` | `2abadf104710` | D354 appended |
| `DECISION_INDEX.md` | `2755e6d3f218` | D354 summary appended |
| `OPEN_ITEMS_BACKLOG.md` | `3e68575bafa0` | B93 turn 3 recorded; still 23 open |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_257.md` | (this file) | not self-referential; checked by `--freshness-check` |

Unchanged and not re-delivered: `index.html`, `detachments.json`, `units.json`,
`detachment_effects.json`, `faction_taxonomy.json`, `b93_check.js`, `b126_check.js`, `baseline.sh` —
all as pushed after S256.
