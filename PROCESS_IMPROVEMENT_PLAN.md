# Process improvement plan — actions

**Superseded S126.** Every item below is now ticketed (T1–T6, H4) in `OPEN_ITEMS_BACKLOG.md` and
closed as of S126 (D198) — see there and `40K_Decision_Log_v3_0.md` for what actually shipped and
why. This document is kept for its record of the original eight-item plan; it is not maintained
further.

---

Written after S125 (E1 arc closed, `index.html` 6.3, assertions 75/75). Eight improvements were
identified; this is what it takes to land each one, split by who does it.

Nothing here changes app behaviour. All of it is custody, tooling and housekeeping.

---

## Ryan's actions

### R1 — Initial repo upload (one pass, ~10 minutes)

Upload the files in the **Commit** list below to `rd-prime-1357/40k-army-builder`. GitHub's web
uploader takes a multi-file drag-and-drop; put the scripts and docs at the repo root alongside
`index.html` unless you'd rather have folders, in which case `scripts/` and `docs/` are fine — tell
me which and the checks will look in the right place.

**Do not upload anything in the Exclude list.** Those are GW-derived source documents and the repo
is public.

Commit `.gitignore` (delivered with this plan) at the root at the same time. It doesn't stop the web
uploader, but it protects you the moment you or any tool uses real git.

### R2 — Per-session repo refresh (~2 minutes, most sessions)

After syncing my outputs into the project area, upload the same changed files to the repo. Usually
two or three files: `index.html`, the decision log, the backlog, the new handoff and prompt, plus
whatever script or harness changed. The handoff's Files section already lists exactly these, and
from now on it will carry a hash per file so you can confirm what landed.

### R3 — Decide on the model/effort flag scope (improvement 8)

Current project instruction makes me open every turn with a model/effort classification, including
one-line conversational answers where the model choice is irrelevant. Recommend scoping it to turns
that run tools or produce artifacts. Your instruction text, your call.

---

## My actions — S126 (tooling session, no engine, no data)

This is a clean session boundary: E1 just closed, so nothing is mid-flight. The whole tooling block
fits in one session and touches no app file.

### T1 — Repo custody check (improvement 1)

New script `repo_check.py`. Clones the public repo into a temp directory, hashes every file the
manifest guards, and compares against the project-area copy. Reports three states per file: match,
differs, missing from repo. This is what turns "the sync reverted my work" from an archaeology
finding into a first-minute failure.

*Risk, stated up front:* I have not yet proven `git clone` works from my sandbox — the network
allowlist includes `github.com` and `codeload.github.com`, so it should, but the GitHub API was
rate-limited when I tested. First five minutes of S126 answers it. If the clone fails, T1 becomes
`raw.githubusercontent.com` fetches of the guarded list, which is slower but works the same.

### T2 — Hashes in the handoff (improvement 2)

The handoff's Files section gains a SHA-256 per changed and new file. The next session's baseline
verifies them before anything else runs. Works even if T1 turns out not to be viable, and catches
the same class of failure one session later instead of instantly. Costs one line per file.

### T3 — One baseline runner (improvement 3)

New script `baseline.sh`. Knows every harness's argument shape, runs the three repro checks, the
assertions, all fourteen harnesses, the bundle check and the manifest, and prints one line per gate.
Session open becomes one command and one screen instead of twenty invocations with four different
argument conventions. T1 and T2 hang off it.

### T4 — Known-failure allowlist for `bundle_check.js` (improvement 4)

`bundle_check` has printed the same two B36 failures for many sessions. A check that is expected to
print red trains us to skim past red, which is how a third failure gets missed. Give it a
known-failures list keyed to B36 so it reads green until something new breaks, and empty the list
when B36 ships.

### T5 — Split the closed history out of the backlog (improvement 5)

`OPEN_ITEMS_BACKLOG.md` is 166 KB, mostly Closed/Shipped narrative. History stays intact — it moves
to `BACKLOG_ARCHIVE.md` in full, and the working backlog keeps open items plus a one-line pointer per
closed ticket. Same move, smaller, for the decision log: a `DECISION_INDEX.md` with one line per
D-entry (number, title, session). The 531 KB log stays untouched and authoritative; sessions grep the
index and read only the entries they need.

### T6 — Retire the module-extraction habit (improvement 6)

Policy, not code. `list_store.js` stays as it is with its E1b-2 guard. No further extraction from
`index.html` without a positive reason — the one extraction we did bought nothing yet and cost a
multi-week silent divergence. Recorded as a decision entry, not a ticket.

### T7 — Memory correction (improvement 7)

Done this turn. My cross-session memory described the project as of roughly S62; it now points at the
handoff chain as the sole authority for current state.

---

## Sequencing

S126 is the tooling session: T1 → T3 → T2 → T4 → T5, with T6 and the decision entry at the close.
T1 first because if the clone doesn't work I want to know before building `baseline.sh` around it.

R1 wants doing **before** S126 opens, so T1 has something to check against. R2 starts the session
after.

If T1 and T3 run long, T5 banks cleanly for a later session — it's independent housekeeping.

---

## Repo file lists

### Commit — our own code

**Pipeline and parsers (20):**
`loadout_parser.py`, `equipped_parser.py`, `wahapedia_transform.py`, `mfm_points_parser.py`,
`ds_wargear_abilities_parser.py`, `convert_to_json.py`, `merge_factions.py`, `detachment_parser.py`,
`mfm_reconcile.py`, `build_cd_ability_details.py`, `add_loadout_groups.py`, `add_co_leader.py`,
`add_bodyguard_stat_flags.py`, `add_chapter_point_overrides.py`, `pipeline_manifest.py`,
`repro_check.py`, `units_repro_check.py`, `detachments_repro_check.py`, `integrity_check.py`,
`rules_assertions.py`

**Harnesses and modules (16):**
`harness.js`, `sweep.js`, `bundle_check.js`, `pool_check.js`, `pts_check.js`, `stat_check.js`,
`default_check.js`, `limit_check.js`, `required_size_check.js`, `b18d_check.js`, `b31_check.js`,
`b56g_check.js`, `b58_check.js`, `e10_check.js`, `e1b_check.js`, `e1c_check.js`, plus `list_store.js`

**Fixtures and banked work (4):**
`B18c_repro_fixture.json`, `B18d_fixture.json`, `bundled_swaps.json`,
`equipped_parser_B18c_banked.py`

### Commit — our own docs

`40K_Decision_Log_v3_0.md`, `OPEN_ITEMS_BACKLOG.md`, `SESSION_HANDOFF_125.md`,
`NEXT_SESSION_PROMPT_126.md` (and every future handoff/prompt), `40K_Functional_Spec_v0_7.md`,
`40K_Architecture_Overview_v0_5.md`, `40K_Data_Dictionary_v2_0.md`,
`40K_Data_Pipeline_Process_v0_6.md`, `OUTPUT_FORMAT_SPEC_for_project_instructions.md`,
`E1_DETACHMENT_SCOPE.md`, `MFM_FW_Reconciliation.md`, `MFM_Standalone_Pass.md`,
`MFM_Chapter_Pass.md`, `pipeline_manifest.json`

### Already in the repo — no action

`index.html`, `units.json`, `unit_loadouts.json`, `detachments.json`, `wargear_points.json`,
`datasheet_wargear_abilities.json`, `abilities.json`, `keywords.json`, `rules.json`,
`weapon_abilities.json`, `core_glossary.json`, `faction_taxonomy.json`

### Exclude — GW-derived source, keep local

* **All 28 Wahapedia CSVs** — `Datasheets*.csv`, `Abilities.csv`, `Stratagems.csv`,
  `Enhancements.csv`, `Detachments.csv`, `Detachment_abilities.csv`, `Unit_*.csv`, `Rules.csv`,
  `Keywords.csv`, `Weapon_Abilities.csv`, `Factions.csv`, `Source.csv`, `Last_update.csv`,
  `Export_Data_Specs.csv`
* **All 39 `.txt` source files** — every `MFM_*.txt`, every `*_web.txt`, `Army_Muster_Rules.txt`,
  `Adeptus_Astartes_Unit_Info.txt`, `MFM_Instructions.txt`, `mfm_sm.txt`
* **Faction packs and rules text** — `Space_Marines_Faction_Pack_v1_0.md`,
  `Dark_Angels_Faction_Pack_June_2026.md`, `chaos_daemons_reference.md`, `wh40k_core_rules.md`
* **`NR_army_selection_windows__detachments.pdf`** — third-party product screenshots

Excluded files stay covered by `pipeline_manifest.py`, which hashes them locally. They change rarely
and are re-downloadable, so they are the safest things to leave out.

---

## What this does not fix

The excluded source data has no off-machine backup. If your local copy is lost, the CSVs and MFM
files are re-downloadable from Wahapedia and GW, but any hand-corrected source would be gone. If any
of that source has been hand-edited, it needs a private backup — a private repo, a cloud folder,
anything. Worth a five-minute check on your side.
