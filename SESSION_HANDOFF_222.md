# SESSION HANDOFF 222

**Turn type:** scoping-only (Drukhari — first faction build pass). No `units.json`,
`unit_loadouts.json`, `detachments.json`, or parser file changed. Produces
`DRUKHARI_BUILD_SCOPE.md`, opens **B115** and **B116**.

## What happened

1. **Baseline reconciled at open.** `./baseline.sh --fetch --data-turn`: public repo fetched and
   verified (102 overlay-needed files verified, 80 already local); private source repo fetched and
   verified fresh (85/85 files byte-match `source_manifest.json`). Full baseline: 34/34 gates
   clean.

2. **Drukhari roster scoped from source, not assumed.** `MFM_Drukhari_v1.1.txt` lists 23
   current-edition units; `Datasheets.csv` holds exactly 23 rows for `faction_id == DRU` and
   `source_id == 000000031` (Drukhari's own current Faction Pack). Matched name-for-name both
   directions. 7 Legends exclusions (source `000000384`) match the MFM's own `LEGENDS` header list
   exactly. Zero SUPPORT units in the faction; 6 buildable LEADER units, a 7th (Urien Rakarth)
   Legends-only.

3. **All points/threshold shapes proven by direct parser execution, not code-reading.** Ran
   `mfm_points_parser.py --mfm MFM_Drukhari_v1.1.txt` against a dry-run `Unit_Stats.csv` (see
   finding below on why that stats file is itself contaminated) and confirmed all 30 unit rows
   (23 current + 7 Legends) price correctly, including Raider's and Venom's new `1st-to-3rd/4th+`
   tier shape (the same B87 `esc4` reader already ships) and Ravager's threshold removal. A
   `--wargear` harvest pass found all 4 wargear-cost items in the file correctly.

4. **Detachments scoped from both MFM versions directly.** 9 detachments in both v1_0 and v1.1,
   same names/DP (range 1–3). Three force-disposition changes (Covenite Coterie, Exhibition of
   Slaughter, Kabalite Agonysts), each carrying its own `UPDATED`/`FORCE DISPOSITION(S) CHANGED`
   banner in source. 30 enhancements total. Three Unique tags (COVENS, WYCH CULT, KABAL) each
   shared by two detachments — checked against `detachments.json` directly and confirmed this
   exact pattern is already precedented and enforced for Blood Angels, Death Guard, Chaos Space
   Marines, and Thousand Sons; not a new mechanism. B113 gains zero new instances (confirmed by
   direct text search — no `LEADER:` lines in the Drukhari `DETACHMENTS` block).

5. **Finding #1 — a real transform bug.** `wahapedia_transform.py --faction DRU` (dry run) selects
   37 datasheets, not 23. The extra 14 are Harlequins/Aeldari-Corsair units tagged `faction_id ==
   DRU` in Wahapedia's export but actually sourced from the Aeldari Faction Pack (`source_id ==
   000000186`, current-edition, not Legends) — the existing filter has no check for source
   belonging to a different faction's own pack. Independently confirmed by the
   `mfm_points_parser.py` dry run, which flags the same 14 as having no MFM points at all (absent
   from `MFM_Drukhari_v1.1.txt` entirely). **Opened as B115** — must be fixed before the Drukhari
   units data turn runs.

6. **Finding #2 — the 14 flagged units are not noise.** Drukhari's army-wide "Corsairs and
   Travelling Players" rule and the Reaper's Wager detachment's "Callous Competition" ability both
   legally permit including Harlequins/Anhrathe units, at points caps scaling by battle size
   (250/500/750 base rule; 500/1000/1500 via Reaper's Wager, mutually exclusive with the base
   rule), priced from a different, unbuilt faction's MFM (`MFM_Aeldari_v1_0.txt`). No built faction
   has this cross-book allied-inclusion shape — the existing Shadow Legion / Legions of Excess /
   Scintillating Legions / Plague Legions patterns all price inline in the host faction's own MFM,
   no cap, no battle-size scaling. **Opened as B116**, recommendation to defer past the initial
   Drukhari build — flagged for Ryan's call since it sets precedent, not decided unilaterally.

7. **Loadout scope bounded and separated from the contamination.** True-Drukhari-only manual
   authoring load (14 Harlequin/Corsair entries in the same dry-run report excluded from these
   counts): 13 wargear-option groups across 9 units, 8 compound replacements, 1 bundled
   two-weapon swap, 4 ambiguous weapon-name matches, 1 equip/add-no-profile item, 1
   multi-model-line split review (Incubi). On the same order as Grey Knights (4 flagged units)
   before it.

8. **Confirmed Drukhari's Wahapedia faction code (`DRU`) from source**, not guessed —
   `mfm_points_parser.py`'s `FACTION_BY_MFM` already carries both Drukhari MFM files mapped to
   `DRU` (wired ahead of time, nothing to add there). `detachment_parser.py`'s three registration
   maps (`ARMY_TO_MFM`, `MFM_SOURCE_NAME`, `ARMY_TO_WAHA_FACTION`) do NOT yet carry Drukhari —
   registration is real work for the units/detachments build turns, correctly not done this
   scoping session.

9. **No units or detachments build started**, per the scoping-only turn type and the explicit
   instruction in `NEXT_SESSION_PROMPT.md` not to begin the build this session.

10. **Full baseline re-run** — clean throughout; no committed pipeline file touched, so no
    regeneration or diff-guard step was needed this session.

## Also opened at the same session per prompt's "at your discretion" list

None of B113, B114, GK §6, or GK §7 were investigated further this session — the prompt marked
them all optional and none intersected with Drukhari scoping directly. B113 was checked
specifically for Drukhari (§4 above, zero new instances) as required scope, not as a standalone
investigation of the ticket itself.

## State at close

- `DRUKHARI_BUILD_SCOPE.md`: net new, full scoping writeup.
- `40K_Decision_Log.md`: D316 appended. `DECISION_INDEX.md`: D316 one-liner appended.
- `OPEN_ITEMS_BACKLOG.md`: ledger header updated to S222, count **22 → 24** (B115, B116 opened,
  nothing closed).
- `units.json`, `unit_loadouts.json`, `detachments.json`, `detachment_effects.json`,
  `faction_taxonomy.json`, `wahapedia_transform.py`, `mfm_points_parser.py`,
  `detachment_parser.py`: untouched this session — all findings from dry runs against throwaway
  temp directories only.
- `index.html`: untouched.
- `pipeline_manifest.py`: `SESSION_HANDOFF_222.md` registered in GUARDED before `--write`.

## Ryan action required

1. **B108 — remove `Thousand_Sons_web.txt` from the public repo** (still outstanding, unchanged).
2. **Push `OUTPUT_FORMAT_SPEC_for_project_instructions.md` to the public repo** (still outstanding
   from S220).
3. Push this session's new/changed files to the public repo (listed below).

## Decisions waiting on Ryan

**B116** — whether/when to build Drukhari's Harlequins/Anhrathe cross-book allied-inclusion
mechanic (see `DRUKHARI_BUILD_SCOPE.md` §6). My recommendation is to defer it past the initial
Drukhari build and open it as its own ticket, gated on Aeldari being prioritized — but this is
flagged rather than decided unilaterally because it sets precedent for how the tool handles
cross-book allied inclusion generally, which no built faction has needed yet.

## Files (SHA-256, first 12)

Verify these at S223 open.

| file | sha256:12 | note |
|------|-----------|------|
| `DRUKHARI_BUILD_SCOPE.md` | `8b51c59fd70a` | net new |
| `40K_Decision_Log.md` | `5563d3b4b98f` | D316 appended |
| `DECISION_INDEX.md` | `ed959f642a2d` | D316 one-liner appended |
| `OPEN_ITEMS_BACKLOG.md` | `32eccba518d1` | ledger header S222, 22 → 24 (B115, B116 opened) |
| `pipeline_manifest.py` | `2dc9c40348c9` | `SESSION_HANDOFF_222.md` appended to GUARDED, post-`--write` |
| `pipeline_manifest.json` | `5ebef0172a00` | `--write` at session close |
| `NEXT_SESSION_PROMPT.md` | `26032e92e57e` | S223 |
| `SESSION_HANDOFF_222.md` | (this file, hash not self-referential) | |

## Net New Files

**`DRUKHARI_BUILD_SCOPE.md`** — the project has never held a Drukhari scope document before. This
is the only net-new file this session; the rolling documents and `pipeline_manifest.py` are
updates, not new roles.

## Backlog

22 open at S221 close; **24 open at S222 close** (B115 opened — `wahapedia_transform.py`'s
Drukhari faction-selection bug, must fix before the units data turn; B116 opened — Drukhari's
Harlequins/Anhrathe allied-inclusion mechanic, scope TBD pending Ryan's call; nothing closed this
session — scoping-only turn, no build shipped).

Beginning: B114, B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2,
P4, E23, B67b, E12, B17 (22). Resolved: none (0). Added: B115, B116 (2). Ending: B116, B115, B114,
B113, B108, B99, B98, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4, E23, B67b,
E12, B17 (24).
