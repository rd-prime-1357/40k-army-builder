# Session 134 handoff — E21a shipped: `detachment_effects.json` authored and asserted

**Turn type: data-only.** One net-new hand-authored data file, six new assertions, one line added to
the manifest's guarded set. No parser, no converter, no engine, no `index.html`. `index.html` stays at
**6.5**. Assertions **88/88 → 94/94**, baseline **21/21** at open and at close. All ten S133 hashes
verified byte-identical before any work started. Authoritative write-up is **D209**; **D210** records
the `/mnt/project` mount finding.

---

## The finding: a seventh construction effect, on six built armies, that D203 missed

D203's list of six live cases was re-derived from source this session rather than carried forward —
all 143 built detachment records rescanned for Battleline, forbid, unlock, Warlord and points-sub-cap
language. **The six hold.** Around twenty extra matches are in-battle false positives from the word
"excluding". One is real.

`HEADHUNTER TASK FORCE` — present in **Space Marines, Black Templars, Blood Angels, Dark Angels,
Deathwatch and Space Wolves** — grants the Tank Ace keyword to most Adeptus Astartes Vehicles, then in
the Muster Armies step lets the player select **up to three** Tank Ace units to gain the **Character**
keyword. Its Designer's Note is explicit that this makes them Enhancement-eligible and Warlord-eligible.

**The app gets this wrong today.** Enhancement eligibility in `index.html` tests
`unit_type === 'Character'` and refuses everything else with *"Only Characters can be given this
enhancement."* Under this detachment that refusal is wrong on up to three vehicles per list, in six
armies.

**Direction matters.** This is **over-restriction, not a D0 violation** — the tool refuses something
legal rather than permitting something illegal — so it does not jump ahead of E21b/c/d or E22b. But it
is B61's shape again: a real rule the app doesn't know about, on built factions, found only because
the survey was redone from source. **Filed as E23**, with a scoping turn as its first step. It is a
fifth effect kind (a muster-time keyword grant with a count limit and a player choice of recipients),
so it is player state rather than a static table row, and it lands on two pieces of already-shipped
code — E4's enhancement eligibility and E9's Warlord eligibility. It was deliberately **not** squeezed
into `detachment_effects.json`'s four-kind schema on the way past.

---

## Decisions needed — one, and it is about capacity, not the build

**The project file area is at ~93% and E21a added a file.** Nothing is blocked, and E21b costs only a
harness, but this needs a plan before it becomes urgent mid-session. Three options, in the order I'd
rank them:

1. **Remove the GW-derived source files that no longer feed a gate.** The largest occupants by far are
   the MFM `.txt` files, the faction web files and the faction packs. Several are for factions not yet
   built. **I am not recommending any specific deletion** — D205 is exactly what happens when source
   material is removed on a guess, and per the standing rule I would need to check which files the
   repro gates actually open before naming any. I can do that check in a tooling turn and come back
   with a list and evidence.
2. **Prune old session handoffs from the project area only**, keeping every one in the repo. They are
   the record and reading back through several is routine, but the repo holds them all and the mount
   is not where that history needs to live.
3. **Accept the ceiling and stop adding files**, folding future net-new content into existing ones.
   Cheapest now, worst later — it is how `index.html` got to 6.5.

My recommendation is **(1), preceded by the check**, with **(2)** as the immediate low-risk relief.
Not proceeding on either without your word: both are deletions, and deletions are the one thing the
project instructions say I must not recommend without verified grounds.

Also still waiting, unchanged: **D199's four batched calls, unreviewed since S127 — now eight
sessions.**

---

## Shipped / changed

**`detachment_effects.json`** — net new. A `_meta` block plus an `effects` object keyed
`Army|DETACHMENT`, holding **seven effects across five detachments** on D204's four-kind schema
(`battleline`, `forbid`, `unlock`, `warlord`; `require` never written). Battleline elevation for Blood
Angels | THE LOST BRETHREN, Dark Angels | COMPANY OF HUNTERS and Death Guard | SHAMBLEROT VECTORIUM;
Shadow Legion's forbid; Tallyband Summoners' Plague Legions unlock plus its Warlord ban; and Shadow
Legion's HERETIC ASTARTES unlock flagged `enforced: false` with a reason. Points caps are keyed by the
army points total for the battle size (`1000`/`2000`/`3000`), matching how the engine already reads
`POINTS_CAP`, and Onslaught is carried even though the app doesn't offer it yet.

**Two authoring calls, both reversible, both proceeded on.** Shadow Legion's forbid is expressed as
`unit_types: ["Epic Hero"]` with `except_units: ["Be'Lakor"]` plus the two Daemon Princes named
explicitly — they are `unit_type: Character`, not Epic Hero, so a type rule alone would miss them, and
a name list of all twelve Epic Heroes would go stale the moment one is added. And Shadow Legion gets
**no `warlord` row**: Be'Lakor's `units.json` record already carries `must_be_warlord: true` from his
Supreme Commander ability, which is unconditional and army-wide and therefore strictly stronger than
the detachment's conditional version. A row as well would be two sources for one rule. Handled the way
D203 handled chapter exclusivity — enforced by construction, policed by an assertion.

**`rules_assertions.py`** — six assertions, E21a-1 through E21a-6: key referential integrity against
`detachments.json`; unit-name referential integrity against each army's **resolved** pool rather than
its own block; schema integrity, including that `require` never appears and every `points_cap` is
keyed `1000`/`2000`/`3000` with strictly increasing values; allied-target resolution, which also pins
the unenforced inventory at exactly one effect; coverage, re-derived by rescanning all 143 records
rather than compared against a remembered list; and the Be'Lakor Warlord check, which fails in both
directions. Gained a `Sources.resolved_pool()` helper mirroring `resolveUnits()`'s composition rule —
deliberate duplication, so that a change to unit-pool composition surfaces as a failure rather than as
agreement.

Outrider Squad is the case that made the resolved-pool distinction load-bearing: it is referenced by a
Dark Angels detachment and lives in the generic Adeptus Astartes block, so an assertion checking only
the Dark Angels block would have failed a correct file.

**`pipeline_manifest.py` / `.json`** — `detachment_effects.json` added to `GUARDED`, 38 → 39 files. It
is the first guarded file that **no repro gate can regenerate**, which is the argument for guarding it:
for every other data file a bad sync fails a reproduction check; for this one nothing would fire and
legality would change silently.

**Docs** — D209 and D210 appended to the decision log, both indexed; backlog updated (E21a marked
shipped, E23 opened, count 7 → 8); next-session prompt rewritten for S135.

### Net New Files

* `detachment_effects.json` — 7,649 bytes. No file has played this role before.

---

## Files

Changed:

| File | SHA-256 (first 12) |
| --- | --- |
| `rules_assertions.py` | `45d5454ebe84` |
| `pipeline_manifest.py` | `3212dc1d73c4` |
| `pipeline_manifest.json` | `2f72fc7208de` |
| `40K_Decision_Log_v3_0.md` | `4d58d2496bca` |
| `DECISION_INDEX.md` | `05fc20658ff9` |
| `OPEN_ITEMS_BACKLOG.md` | `91486e1226ef` |
| `NEXT_SESSION_PROMPT.md` | `976e6533c148` |
| `SESSION_HANDOFF_134.md` | *self* |

Net new:

| File | SHA-256 (first 12) |
| --- | --- |
| `detachment_effects.json` | `e38c38dcef31` |

**Repo custody.** All nine files above are project-generated and repo-eligible.
`detachment_effects.json` carries short rule names and unit names only — no GW rules text is
reproduced in it, deliberately; its `source` fields describe each rule rather than quoting it. No
GW-derived source material was written this session. Excluded from any push as always: the Wahapedia
CSV export, the MFM `.txt` files, the faction web and pack files, `Army_Muster_Rules.txt` and
`wh40k_core_rules.md`.

## Backlog

**8 open:** B62, P2, E21 (E21a shipped; b/c/d remain), E22 (E22a done, E22b remains), E23, B60, E12,
B17.

- Beginning tickets: B62, P2, E21, E22, B60, E12, B17 (7)
- Resolved tickets: none (E21a shipped; E21 stays open on b/c/d)
- Added tickets: E23
- Ending tickets: B62, P2, E21, E22, E23, B60, E12, B17 (8)
