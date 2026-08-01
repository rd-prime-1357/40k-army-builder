# Session handoff — Session 182

**Turn type:** Data-only (D273). E23's source facts confirmed across all six armies; no engine, no
data-file change, no `index.html` change (`index.html` stays **v6.14**). No ticket shipped — E23's data
dependency is cleared and the build turn is next.

## 1. Session open

- Read `SESSION_HANDOFF_181.md` and `NEXT_SESSION_PROMPT.md` (S182) first. The prompt pointed to D272
  (E23 scoping) and D209 (E23's original filing, embedded in the D209 entry); both read directly from
  the decision log, not trusted from the prompt's paraphrase.
- Baseline `./baseline.sh --fetch --data-turn`: clean, **29/29 gates pass** with GW sources loaded
  (`fetch-verify` 59 overlay files; `source-fetch` 70 source files verified; all three repro rebuilds,
  `rules_assertions` 113/113, every harness, manifest, repo custody). Correct tier-all state for a data
  turn. Confirmed the S182 prompt's premise that Thousand Sons is fully built holds — no TS build work
  re-opened.

## 2. What was confirmed (D273)

The turn's job was the record a build turn will consume, not the schema row. **All four E23 facts
confirmed from source, and D209/D272's "most Adeptus Astartes Vehicles" paraphrase corrected to a
precise predicate.**

1. **Grant wording is identical across all six armies — structurally, not coincidentally.** It is one
   Space Marines detachment shared by six armies' detachment pools, not six independently-worded
   copies. The full Tank Ace grant is verbatim in exactly one authoritative source (Space Marines
   Faction Pack v1.0, `## p7 — HEADHUNTER TASK FORCE`) and once in Wahapedia `Detachment_abilities.csv`
   under `faction_id=SM` (rule "Target Sighted"); the two agree word-for-word. The Dark Angels Faction
   Pack does not reproduce it; the Space Wolves web file's only "headhunter" match is an unrelated Wolf
   Guard Headtakers unit ability; every army's MFM carries only the detachment name plus its enhancement
   points, never the grant. In the built data, `detachments.json` `rule_text` is **byte-identical across
   all six records** (SHA-256 `cadd53c18131`, 922 chars).

2. **The carve-out is a precise keyword predicate, not "most Vehicles."** Exact rule: Adeptus Astartes
   Vehicle units *excluding Fortifications, Drop Pods, Walkers and units that can Fly* get Tank Ace.
   Fully computable from built data — `Fly`/`Walker`/`Drop Pod` are unit keywords in model-group
   `keyword_names`, `Fortification` is a `unit_type`.

3. **Cap "up to three" holds in all six** (same source text, same byte-identical `rule_text`).

4. **Detachment keys — all six confirmed:** `<Army>|HEADHUNTER TASK FORCE` for Space Marines, Black
   Templars, Blood Angels, Dark Angels, Deathwatch, Space Wolves — each `dp:2`,
   `force_disposition: "PRIORITY ASSETS"`.

**Per-army eligible pool, resolved from source (pool = army block ∪ generic Adeptus Astartes block for
a subfaction; Space Marines maps to the Adeptus Astartes block alone).** Generic Adeptus Astartes
block: 28 `unit_type: Vehicle` units → **16 eligible**, 12 carved out (5 Walkers: Ballistus / Brutalis
/ Dreadnought / Invictor Tactical Warsuit / Redemptor Dreadnought; 6 Fly: three Storm Speeders,
Stormhawk Interceptor, Stormraven Gunship, Stormtalon Gunship; plus Drop Pod). The 16 eligibles:
Firestrike Servo-turrets, Gladiator Lancer, Gladiator Reaper, Gladiator Valiant, Impulsor, Land Raider,
Land Raider Crusader, Land Raider Redeemer, Predator Annihilator, Predator Destructor, Razorback,
Repulsor, Repulsor Executioner, Rhino, Vindicator, Whirlwind. **Resolved counts differ per army —
Blood Angels is the only one not 16:** SM 16, Black Templars 16 (no own vehicles beyond the block),
**Blood Angels 17** (adds Baal Predator; Death Company Dreadnought excluded, Walker), Dark Angels 16
(its four own vehicles all Fly, excluded), Deathwatch 16 (Corvus Blackstar excluded, Fly), Space Wolves
16 (its four own vehicles all Walker Dreadnoughts, excluded). No eligible unit in any pool is already
`unit_type: Character`/`Epic Hero`, so the grant is never a redundant no-op.

**Three build-turn design notes banked (dev-manager calls, not Ryan-facing):**
- (a) Base eligibility on the Vehicle **keyword**, not `unit_type: Vehicle` — so the rule's "excluding
  Fortifications" clause does real work: it catches Hammerfall Bunker (Vehicle keyword, `unit_type:
  Fortification`), its only Adeptus Astartes case. A `unit_type` base would silently pre-exclude it and
  leave the Fortification clause dead.
- (b) Encode the carve-out as a **per-entry exclusion predicate** on the effect row (exclude keywords
  `Fly`/`Walker`/`Drop Pod` + `unit_type` `Fortification`), evaluated on each list entry's own
  keywords — **not** a per-detachment name list. The per-army lists above are ground truth for the
  build's assertion, not data the engine enumerates.
- (c) The "Adeptus Astartes" qualifier is satisfied by pool construction today, not a keyword check
  (built `keyword_names` drop faction keywords). Safe now — every unit these six can field is Adeptus
  Astartes — but the build turn should add an assertion that no non-Adeptus-Astartes vehicle can enter
  these pools and silently become Tank Ace-eligible.

## 3. Decisions waiting on Ryan

None from this turn. The rule is unambiguous; the predicate-vs-name-list and keyword-vs-type-base
choices are build-mechanism and were decided here. **B70 (Wardens of Ultramar)** remains as before —
decided S175 (D266) to build the join/Starting-Strength mechanic, still needs a scoping turn.

## 4. Process notes

`SESSION_HANDOFF_182.md` appended to `pipeline_manifest.py`'s `GUARDED` list this session (137 guarded
files), per the S182 prompt and D271's design — routine per-session close bookkeeping.

Repo/custody: the decision log and this handoff paraphrase the GW rule and quote only the short
operative exclusion clause ("excluding Fortifications, Drop Pods, Walkers and units that can Fly"),
matching how D209 handled the same text — no substantial GW-derived material, so both remain
repo-committable. Unit names and counts are facts, not GW creative text. No GW source file, MFM, web
file, or Wahapedia CSV was edited; those stay out of the public repo as always.

## 5. Files

| File | Status | SHA-256 (first 12) |
|---|---|---|
| `40K_Decision_Log.md` | D273 appended | `2cb62b3f3292` |
| `DECISION_INDEX.md` | D273 index entry added | `cd032907b584` |
| `OPEN_ITEMS_BACKLOG.md` | E23 ticket updated with confirmed facts; header changelog + heading marker | `2299f8a473d4` |
| `NEXT_SESSION_PROMPT.md` | overwritten (S183 — E23 build turn) | `b707bac92eb1` |
| `pipeline_manifest.py` | `SESSION_HANDOFF_182.md` added to `GUARDED` (137 guarded files) | `4be576c208fd` |
| `pipeline_manifest.json` | reissued at close (not self-guarded — cannot guard itself) | — |
| `SESSION_HANDOFF_182.md` | new (rolling) | — |

No GW-derived material in this set — all project docs and pipeline tooling. No data file, engine file,
or `index.html` changed this session.

## 6. Backlog

- **Beginning:** 11 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17
- **Resolved:** none (data-confirmation turn; E23's data dependency cleared, ticket ships on the build turn)
- **Added:** none
- **Ending:** 11 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17
