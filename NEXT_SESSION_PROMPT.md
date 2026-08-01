# Next-session prompt — Session 181

**Assigned: analysis-only — E23 scoping turn, `HEADHUNTER TASK FORCE` Tank Ace Character keyword
grant.** No engine or data change this session; the point is to land on a scoped build plan Ryan
signs off on, or to identify what's still blocking one.

## Open at session start

Read `SESSION_HANDOFF_180.md` first, then `40K_Decision_Log.md` D271 and D209 (E23's original filing).
Do not trust any session/version/decision number from memory — re-derive from source.

Run the full baseline: `./baseline.sh --fetch`. Expect a clean pass — S180 closed with the
`pipeline_manifest.py` GUARDED gap fixed and `--freshness-check` green. If either fails, reconcile
before starting; do not work around a failing gate.

## The ticket

`OPEN_ITEMS_BACKLOG.md` §E23 (filed S134/D209): `HEADHUNTER TASK FORCE` exists in six built armies
(Space Marines, Black Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves) and grants the
Vehicle keyword Tank Ace to most Adeptus Astartes Vehicles, then in the Muster Armies step lets the
player select up to three Tank Ace units to gain the Character keyword — making them Enhancement- and
Warlord-eligible. `index.html` currently gates both on `unit_type === 'Character'` and refuses
everything else — an over-restriction (refuses something legal), not a D0 violation, on up to three
vehicles per list.

Needs, before a build turn can start:
1. **Data turn** (`--data-turn`) to confirm the exact keyword-grant text across all six armies from
   GW sources — don't assume the six armies' wording is identical without checking each.
2. **A decision on where the per-list Tank Ace selection lives** in the list record — player state,
   must survive save/load. This is a "how it works" question if the storage shape has any user-facing
   implication (e.g. does the selection reset on faction change, can it be changed after Muster); flag
   for Ryan if genuinely ambiguous, otherwise decide and proceed.
3. **A decision on mechanism** — a sixth `detachment_effects.json` effect kind vs. its own standalone
   mechanism. This touches E4's enhancement eligibility and E9's Warlord eligibility, so the choice
   has to compose cleanly with both, not just work in isolation.

Land on a scoped plan (data needs, storage shape, mechanism choice) this session. If the data turn or
any sub-decision surfaces something that changes E23's shape materially, that's a normal scoping
finding — record it and adjust, the same as D268 corrected D260's B73/E26 diagnosis in-session.

## After this

Once E23 is scoped (and, in a later session, built), or if this session finds a hard blocker:
- **B69** (select-N ability pools) — needs a data + engine arc, M-sized.
- **B70** (Wardens of Ultramar join mechanic) — decided S175 (D266: build the join/Starting-Strength
  mechanic), still needs its own scoping turn before a build.
- **B75/B85** — blocked on real PDF access from Ryan.
- Remaining faction builds per the priority order (Thousand Sons in progress; see
  `THOUSAND_SONS_BUILD_SCOPE.md`).

## Close protocol

Produce the four documents: `SESSION_HANDOFF_181.md`, overwrite `NEXT_SESSION_PROMPT.md`, append the
decision log + `DECISION_INDEX.md`, update `OPEN_ITEMS_BACKLOG.md` if E23's ticket text needs
updating with the scoped plan. Every changed and net-new file carries a SHA-256 (first 12) in the
handoff Files section. `python3 pipeline_manifest.py --write` then `--freshness-check` at the very
end, after all text is finalized — reissue if anything touches the decision log or the handoff after
the write. Repo is public and flat — no GW-derived material committed; state the exclusions when
listing files for the repo. Remember to append `SESSION_HANDOFF_181.md` itself to `GUARDED` in
`pipeline_manifest.py` this same session, the omission D271 just fixed.
