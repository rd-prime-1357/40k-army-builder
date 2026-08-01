# Next-session prompt — Session 182

**Assigned: data-only — E23 confirmation turn, `HEADHUNTER TASK FORCE` source text across six armies.**
No engine change, no `index.html` change. The point is to confirm exact wording/cap and bank the
config-level facts a build turn will need; not to build the mechanism itself.

## Correction from S181, check before trusting anything inherited

**Thousand Sons is already fully built, not "in active progress."** `units.json` carries 362 units
(the THOUSAND_SONS_BUILD_SCOPE.md target — 328 + 34 TS), `detachments.json` carries 169 detachments
(160 + 9 TS), and `repro_check.py`/`detachment_parser.py`/`rules_assertions.py` (`TS-1`/`TS-2`/`TS-3`)
are all fully wired for TS. This was verified from source at S181 open, not carried forward — do not
re-open Thousand Sons build work without first checking whether whatever prompted the "in progress"
belief still holds. If genuinely nothing is left on TS, the next faction in the priority order with no
build started at all is **Emperor's Children** (no `EC`/`Emperor's Children` entries anywhere in
`repro_check.py`'s `FACTIONS`/`WEB_PASSES` or `detachment_parser.py`'s army tables) — that would need
its own `EMPERORS_CHILDREN_BUILD_SCOPE.md` scoping pass before a build, on the CSM/TS model, in a
session after this one.

## Open at session start

Read `SESSION_HANDOFF_181.md` first, then `40K_Decision_Log.md` D272 (E23's scoping) and D209 (E23's
original filing, embedded inside the D209 entry — not its own heading). Do not trust any
session/version/decision number from memory — re-derive from source.

Run the full baseline: `./baseline.sh --fetch --data-turn`. This is a data turn — it must load GW
sources (token first, `gw_sources.zip` fallback) and will FAIL rather than silently run tier-A-only if
neither is available. Expect the fetch-verify pass and a clean tier-all baseline if sources load.

## The ticket

`OPEN_ITEMS_BACKLOG.md` §E23, scoped S181 (D272). The mechanism is already decided: a new declarative
`detachment_effects.json` effect kind (fifth kind — schema has four today; the wording "sixth" in an
earlier document was wrong and corrected S181) for the detachment-scoped facts, plus a purely-additive
`list_store.js` pick-array field for the player's selections (no version bump). This session is
**data-only**: confirm the facts that new effect-kind row needs, do not build the engine or write the
row yet — that is a separate, later turn per turn-typing.

Confirm from GW source, per army, for all six (Space Marines, Black Templars, Blood Angels, Dark
Angels, Deathwatch, Space Wolves):
1. **Exact `HEADHUNTER TASK FORCE` grant wording** in each army's own faction pack / MFM text — do not
   assume identical wording across all six without checking each copy individually, the same standard
   D209 used when it first found this.
2. **The exact Tank Ace-eligible unit definition** — "most Adeptus Astartes Vehicles" implies a
   carve-out; confirm its exact membership (which Vehicle-type units, if any, are excluded) per army.
   The 28 Vehicle-type units in the generic Adeptus Astartes block are listed in D272 for reference —
   check against source, don't assume that list is the carve-out-free set.
3. **The count cap** — confirm "up to three" holds in all six copies rather than assuming uniformity.
4. **The detachment name/key** in each of the six armies' `detachments.json` records, to confirm the
   six keys this effect will need to be filed against.

Record findings in decision-log form (source-cited, army-by-army) — this session's job is the record,
not the schema row itself. If wording turns out to vary meaningfully between armies, that is a normal
scoping finding for this turn to surface, the same as D268 corrected D260's B73/E26 diagnosis in-session.

## After this

Once E23's data turn is banked:
- **E23 build turn** — write the fifth effect-kind row(s) into `detachment_effects.json`, add the
  `list_store.js` pick-array field, and wire `eligibleWarlordEntries()` /
  `canAssignEnhancement`/`enhancementTypeEligible`'s three call sites per D272's engine-touch-point
  list. Engine-only or data+engine depending on how the turn-typing shakes out — decide at that
  session's open, not now.
- **B69** (select-N ability pools) — needs a data + engine arc, M-sized.
- **B70** (Wardens of Ultramar join mechanic) — decided S175 (D266: build the join/Starting-Strength
  mechanic), still needs its own scoping turn before a build.
- **B75/B85** — blocked on real PDF access from Ryan.
- **Emperor's Children** — next unstarted faction in the priority order once Thousand Sons's completion
  is confirmed for real at this session's open; needs a build-scope document before a build, same as
  CSM and Thousand Sons got.

## Close protocol

Produce the four documents: `SESSION_HANDOFF_182.md`, overwrite `NEXT_SESSION_PROMPT.md`, append the
decision log + `DECISION_INDEX.md`, update `OPEN_ITEMS_BACKLOG.md` if E23's ticket text needs updating
with confirmed source facts. Every changed and net-new file carries a SHA-256 (first 12) in the handoff
Files section. `python3 pipeline_manifest.py --write` then `--freshness-check` at the very end, after
all text is finalized — reissue if anything touches the decision log or the handoff after the write.
Repo is public and flat — no GW-derived material committed; state the exclusions when listing files for
the repo (this session's own source-confirmation notes, if they quote faction-pack/MFM text at length,
may themselves need exclusion — check before listing). Remember to append `SESSION_HANDOFF_182.md`
itself to `GUARDED` in `pipeline_manifest.py` this same session, per D271's design.
