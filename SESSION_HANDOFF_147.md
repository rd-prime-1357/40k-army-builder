# Session Handoff 147

## Baseline at open

S146's five hashes matched byte-for-byte. `./baseline.sh --no-repo` passed 23/23 gates, 104/104
assertions — clean, unchanged from S146's close. `repo_check.py` still absent from the mount; no
committed file was touched before this baseline check, so custody is unaffected.

## What happened — D229/D230, CSM turn A (data-only) + B68 opened

**D229 — CSM turn A shipped.** The transform selected 58 current-edition CSM datasheets, matching
D227's scoping exactly. Confirmed by source (the points parser's own validation report): four
cult-troop units (Khorne Berzerkers, Rubric Marines, Plague Marines, Noise Marines) have no price in
the CSM MFM — they're priced once, in their parent god-legion's own MFM. `convert_to_json.py` does
not exclude an unpriced unit; it ships it with `points: null`. Committing all 58 as-is would land four
new nulls against `b56a_residual_nulls`'s hard pin of exactly two — an uncosted, addable unit is
exactly the state D0 exists to make unreachable. Resolution: the four are filtered out of the
transform's own `Unit_Stats.csv` before pricing/conversion (build-orchestration inside the turn's
temp directory, not a hand-edit of any committed output, not a parser change — confirmed
`convert_to_json.py`'s `build_units()` keys entirely off `Unit_Stats.csv`, so an absent row is simply
absent from the output). Turn A ships exactly 54, all priced.

Diff-traced clean: 54 new unit_ids, 0 lost, 0 changed among the existing 270 — verified by flattening
old and rebuilt `units.json` and comparing every record. The three merged lookups drifted as expected
(abilities.json +94, rules.json +1, weapon_abilities.json +5 — CSM's own names) and are re-banked as
part of the same fixed point (B55/D164); keywords.json and faction_taxonomy.json didn't move.

**Scope gap closed.** `datasheet_wargear_abilities.json` (D105/B15) is restricted to the unit_ids in
`units.json` and needed regenerating too — a fourth regenerated output CSM_BUILD_SCOPE.md's §6 didn't
list. Regenerated (+7 datasheets, 0 lost, 0 changed), folded into this turn.

**E4B_KEYWORD_GAPS extended, not reinterpreted.** Three new CSM units (Dark Apostle, Dark Commune,
Traitor Enforcer) are typed Character with CHARACTER scoped to only one model group of a
multi-model-group unit — same shape as the existing Ravenwing Command Squad entry. Added to the
allowlist; the assertion's own docstring anticipated a third such unit.

**D230 — B68 opened, not fixed.** Building CSM's loadout-defaults pass surfaced a bug that predates
this session: Death Guard and CSM each carry their own datasheet for seven generic Chaos vehicles
(Chaos Rhino, Chaos Land Raider, both Predator variants, Chaos Spawn, Defiler, Helbrute) with
identical Unit Names. Proven, not suspected: running the unmodified production chain (CSM named
nowhere in `--factions` or the web passes) against a CSM-inclusive `units.json` still changed 23
pre-existing units' stored defaults. Isolating each step individually narrowed the trigger to mere
co-presence in the file, not any processing of CSM's own data — a name-keyed lookup somewhere in
`loadout_parser.py`/`equipped_parser.py`, not scoped by army or unit_id. This is a parser-level defect;
fixing it is an engine/parser change and cannot mix with this data turn. `unit_loadouts.json` and
`repro_check.py` are deliberately untouched — no partial edit, no workaround. Filed as **B68**;
blocks CSM_BUILD_SCOPE.md §5 (CSM's own loadout-defaults pass).

Manifest reissued (41 guarded files). End state: **21/23 gates pass.** `repro_check` and
`rules_assertions`'s own embedded P1 check are the two failures, both the identical root cause (B68),
both naming the same seven unit_ids — expected and diagnosed, not a new regression.

## Decisions needed

**D228 (carried from S146, still awaiting Ryan's explicit yes/no; precedent-setting).** Build the two
prose-less new CSM detachments (Devotees of Destruction, Murdertalon Raiders) selectable but
prose-incomplete. Recommendation stands; CSM turn C proceeds on it absent a "no."

Also still open, carried forward: D199's four batched calls (unreviewed since S127, twenty-one
sessions, three load-bearing); the `_web.txt` regeneration plan (D226 — pause and ask before each);
B67b.

## Shipped / changed

Data-only turn. `units.json` gains a Chaos Space Marines block (54 units, all priced). `abilities.json`,
`rules.json`, `weapon_abilities.json` re-banked as the same fixed point. `datasheet_wargear_abilities.json`
regenerated for the same 54 units' wargear abilities. `units_repro_check.py` updated with the CSM
per-faction block (transform → D229 filter → self MFM points → convert), `CSM_CULT_TROOP_IDS` and a
small CSV-filter helper added, `MFM_Chaos_Space_Marines_v1_0.txt` added to `REQUIRED`, merge call gains
a fourth `--in`. `rules_assertions.py` — `E4B_KEYWORD_GAPS` extended with the three CSM units.
`pipeline_manifest.json` reissued (41 guarded files). `40K_Decision_Log_v3_0.md` — D229, D230 appended.
`DECISION_INDEX.md` — both indexed. `OPEN_ITEMS_BACKLOG.md` — B68 opened (8 open items), header moved
to S147. `NEXT_SESSION_PROMPT.md` — rewritten for S148, B68 sequenced ahead of CSM turns B/C.

**Not touched, deliberately:** `unit_loadouts.json`, `repro_check.py`, `detachment_parser.py`,
`detachments.json`, `CSM_BUILD_SCOPE.md`. `index.html` unchanged (CSM uses only existing mechanisms).

### Net New Files
None. `NEXT_SESSION_PROMPT.md` and the decision log/backlog/index are rolling documents (updates, not
net-new) per the project's own rule; every other changed file is a versioned output or an existing
script gaining a per-faction block, not a new role.

### Files (SHA-256, first 12 chars)
- `units.json` — `eb370386ccf7`
- `abilities.json` — `051bdd9ceb08`
- `rules.json` — `b347222a3bc9`
- `weapon_abilities.json` — `ff4379837df4`
- `datasheet_wargear_abilities.json` — `af5be2824e54`
- `units_repro_check.py` — `81cb0f825727`
- `rules_assertions.py` — `f793cf479349`
- `pipeline_manifest.json` — `fa8073b131eb`
- `40K_Decision_Log_v3_0.md` — `774125079221`
- `DECISION_INDEX.md` — `7f75199c16a3`
- `OPEN_ITEMS_BACKLOG.md` — `28ebfb4f7c28`
- `NEXT_SESSION_PROMPT.md` — `6887b1de0389`

**Repo custody:** all twelve are either project-generated prose/config or already-repo-eligible
pipeline output (matching prior sessions' classification) — no GW rule/ability prose beyond what
`units.json` already carried pre-CSM (unit/ability/rule *names* and points, not GW's rule text bodies).
No GW-derived source introduced. Belongs in the next batch upload alongside this handoff. Excluded as
always: the Wahapedia CSV export, the MFM `.txt` files, the faction web/pack files.

**Capacity note (P4):** this turn added roughly 401 KB across the five regenerated JSON files
(`units.json` +366,676 bytes; `abilities.json` +31,610; `rules.json` +1,050; `weapon_abilities.json`
+1,215; `datasheet_wargear_abilities.json` +1,121). Ryan read 96% at this session's open. The
decision-log archive split remains the next lever and is worth doing before CSM's remaining three
turns add roughly another ~140 KB.

## Backlog summary

- **Beginning (7 open):** P2, P4, E23, E12, B17, B61, B67b
- **Resolved (0):** none
- **Added (1):** B68 — loadout-defaults parser bug (name-keyed matching bleeds across Death
  Guard/CSM's seven shared generic Chaos vehicle names), blocks CSM's loadout-defaults pass
- **Ending (8 open):** P2, P4, E23, E12, B17, B61, B67b, B68
