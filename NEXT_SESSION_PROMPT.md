# NEXT SESSION PROMPT — Session 257

## Read first

`SESSION_HANDOFF_256.md` and this file are the only authority on current state. Do not trust
remembered session numbers, version strings or decision numbers — re-derive them.

State at S256 close: `index.html` **v6.27**, decision log through **D353**, `SCHEMA_VERSION` **5**,
`rules_assertions.py` at **138** assertions, **42** gates in `baseline.sh`, **23 open** backlog items.

## Open

**Before anything else: confirm `detachments_repro_check.py` in the project area matches the repo.**
The area copy was stale at S256 open — four lines short, missing the two source CSVs the B93 data
turn added — and it failed three gates. If Ryan has not re-uploaded it, take the repo copy and say so.

Then run `./baseline.sh --fetch --data-turn` and verify the S256 file hashes in
`SESSION_HANDOFF_256.md`'s Files table against the fetched repo.

## Assigned work: B93 turn 3 — the tooling turn

**Turn type: tooling.** Do not touch `index.html`, `detachments.json` or any parser this session.

Turn 2 shipped the resolver at S256 and closed the live D0 gap. `b93_check.js` already pins the
admit populations **from the engine side** — 53 zero-admit across six clauses, 98 one-admit, over
1,145 army x record evaluations. Turn 3 is the **independent second derivation**, in
`rules_assertions.py`, on the `B99-CENSUS` / `B119-CENSUS` / `B93-CENSUS` pattern:

1. Re-derive the admit counts from `detachments.json` and `units.json` **without** loading any
   JavaScript, so a resolver bug and a census bug cannot cancel out. Mirror `resolved_pool` for the
   unit side, exactly as `b93_check.js` mirrors `resolveUnits`.
2. Fail on any zero-admit clause outside the four known causes — Tank Ace conferral, mark selection,
   an unbuilt faction, or a clause with no bearer in a correctly-built roster.
3. Pin the one-admit set by name, not just by count. That is the set where a resolver regression
   turns into an unassignable enhancement rather than a mildly wrong list, and a count alone will not
   catch a swap.

The two derivations must agree. If they disagree, **the disagreement is the finding** — do not adjust
one to match the other before working out which is wrong.

## Also worth doing this turn if it fits

**`pipeline_manifest.py`'s hash-table ordering.** S255's handoff recorded a wrong hash for
`pipeline_manifest.py`, because the file is edited once more — adding the new handoff to `GUARDED` —
after the Files table is written. S256 worked around it by adding the handoff to `GUARDED` first.
That ordering belongs in the close sequence in writing, not in one session's memory.

## Precedents that will matter again

**When a prompt cites a decision and an instruction that disagree, the decision wins.** S256's
assigned scope said to demote the enhancement type gate *and* said D335 governs, which forbids it.
`B93_SCOPE.md` §7.2 was written under D334 and never rewritten when D335 reversed it the same
session. This is the second such case in three sessions — D350 was the first, and it cost two
sessions and a reverted decision.

**A curated table can be narrower than the rule it enforces, and nothing will say so.** B113's
`Bray Lord` row named two units where the clause names two keywords; `Sorcerer In Terminator Armour`
carries `SORCERER` and had been refused since S228. Curation hides this; a resolver over the real
vocabulary exposes it. When replacing a curated table, diff the old admits against the new ones unit
by unit rather than checking the new mechanism in isolation.

**Zero admits is not automatically a bug, and it is not automatically fine either.** Each of the six
zero-admit clauses at S256 was traced to a cause before the reading was adopted. `Reaper's Cowl`
resolves to nobody because Harlequins is not a built faction — correct today, and it fixes itself.

## Close

Four rolling documents updated (`40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
`SESSION_HANDOFF_257.md`), this file rewritten for S258, then:

1. add `SESSION_HANDOFF_257.md` to `pipeline_manifest.py`'s `GUARDED` list **before** writing the
   handoff's Files table — otherwise `pipeline_manifest.py`'s own recorded hash is wrong every time
2. `python3 pipeline_manifest.py --write`
3. `python3 pipeline_manifest.py --freshness-check`

Those two commands are the literal last two of the session.

## Outstanding Ryan actions carried forward

**A render check covering four sessions' UI.** S248's Tank Ace checkbox, S249's Mark of Chaos
selector, S250's silent truncation of an over-cap tally on size reduction, and S256's enhancement
picker. S250's still matters most — it is the only one that edits a saved list without telling the
player.

**S256's script.** Build a Space Marines list on **Headhunter Task Force**. Add a Captain and a
Rhino. On the Captain, open the enhancement section: all four enhancements should now be **visible
but disabled**, each reading "Adeptus Astartes Vehicle model only." — before S256 they were offered
and assignable, which was the bug. On the Rhino, check **Select as Tank Ace**, then open its
enhancement section: the same four should now be **enabled**. Uncheck Tank Ace and confirm they go
back to disabled. Then switch to **Thousand Sons / Warpmeld Pact** and confirm `Bray Lord` is
offered on `Sorcerer`, `Infernal Master` **and** `Sorcerer In Terminator Armour`, and disabled on any
other Character.
