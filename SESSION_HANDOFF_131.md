# Session 131 handoff — recovery: three Chaos Daemons source CSVs rebuilt (D205); Soul Grinder allegiance gating found dead (D206)

**Turn type: tooling/recovery.** No parser, engine, harness or data-pipeline script changed.
`index.html` stays at **6.5**, assertions **80/80**, baseline **21/21** at close. Authoritative
write-up is **D205** and **D206** in `40K_Decision_Log_v3_0.md`.

**B61 did not start.** This session was consumed by recovery. B61 is unchanged and still open.

---

## What happened

Three Chaos Daemons source CSVs — `Unit_Weapons.csv`, `Unit_Wargear_Options.csv`, `Rules.csv` — were
deleted from the project area while clearing space. They are pipeline inputs named in
`units_repro_check.py`'s `CD_ROOT_CSVS`; without them the fixed point cannot run.

The deletion followed a stale framing in S130's next-session prompt, which described them as duplicate
junk. That framing was repeated to Ryan without first checking whether anything read them. The
verification failure is mine and is recorded in D205 rather than left in conversation.

**The repo was never a backup.** Confirmed against the live repo: 82 files, zero CSVs. `index.html`
and `units.json` fetch normally at the same path, so the 404s are real. The standing GW-text exclusion
working as designed — but it means the project file area was these files' only copy.

**Restoring from the original build conversation did not work.** The June-21 generation was wrong four
ways: 94 en dashes in `Unit_Weapons.csv` and 12 in `Unit_Wargear_Options.csv` against a dataset that
uses plain hyphens throughout; a different data model splitting Daemon Princes by god with no Soul
Grinder rows at all (167 rows against the correct 142); a `Rules.csv` missing five rules, carrying four
drifted descriptions and having lost its trailing blank column (13 against 18); and a row order that
produced a content-identical but not byte-identical `rules.json`, since `merge_factions.py` unions the
lookups on first-wins insertion order.

**The three files were rebuilt from the committed `units.json` and `rules.json` instead.** That
inverts the pipeline, and the limitation is permanent: anything the CSVs held that the converter never
consumed is gone. It was accepted because the rebuild proves itself — `units_repro_check.py` reports
byte-identical reproduction of `units.json` and all four merged lookups, which is impossible if any
consumed field is wrong. A file recovered from history would only prove someone once saved it.

---

## The finding that mattered more than the recovery

**Soul Grinder's god weapons have never been gated.** Chasing the one column the rebuild could not
recover — `Allegiance_Condition` — turned up a live D0 violation that predates this session entirely.

`index.html` filters on `w.allegiance_condition` at lines 6580 and 6604. `convert_to_json.py` never
reads that column, so it never reaches `units.json`; the deployed file has zero allegiance data and
the app's filter is dead code. Soul Grinder ships with torrent of burning blood, warp gaze, phlegm
bombardment and scream of despair **all flagged as base equipment at once**.

The data is fully recoverable — `chaos_daemons_reference.md` carries the Daemonic Allegiance line
verbatim, and D25/D26 confirm Soul Grinder is the column's only user.

**Ryan ruled:** exactly one god weapon is added, set by the allegiance chosen at list-building. The
four become allegiance-tagged conditionals, not base equipment. Base equipment is Harvester cannon,
Iron claw and Warpsword; Warpclaw stays the existing swap against Warpsword; one god weapon is added
on top and replaces nothing.

Filed as **B63** and sequenced ahead of B61 — the illegal state is worse and the app side already
exists, so the fix is a converter turn with no engine work.

---

## Fidelity detail worth carrying forward

Keeper of Secrets' Shining Aegis and Soul Grinder's Warpclaw carry the literal string `FALSE` in the
Is Base Equipment column rather than `Yes`/`No`. The converter passes it through unrecognised, so
`units.json` ships the string `"FALSE"` where every other weapon carries a boolean. Reproducing that
quirk faithfully was the last six bytes between fail and pass. Filed as **B62** along with the missing
presence-and-parse assertion over the nine CD CSVs.

---

## Decided

* Rebuild from shipped output rather than from conversation history, accepting the inversion in
  exchange for a self-proving result (D205).
* B63 sequenced ahead of B61; both are D0 violations, B63 has the worse illegal state and no engine
  dependency (D206).
* Ryan keeps a local backup folder for GW-derived and GW-text-carrying files. The repo cannot hold
  them, so nothing else will catch this next time.

## Still open for Ryan

* D199's four batched calls remain unreviewed since S127.
* Project file store is at capacity. `Adeptus_Astartes_Unit_Info.txt` (402K, read by no script) and
  `NR_army_selection_windows__detachments.pdf` (173K) are the cleanest removals if space is needed.

---

## Files

Changed:

| File | SHA-256 (first 12) |
| --- | --- |
| `Unit_Weapons.csv` | `ec2aa6796e51` |
| `Unit_Wargear_Options.csv` | `b871712effa1` |
| `Rules.csv` | `0f4bcc0d5e66` |
| `40K_Decision_Log_v3_0.md` | `22888301604f` |
| `DECISION_INDEX.md` | `73df6b9e8a8b` |
| `OPEN_ITEMS_BACKLOG.md` | `0e232f352ed4` |
| `SESSION_HANDOFF_131.md` | *self* |
| `NEXT_SESSION_PROMPT.md` | `6b14153be5d0` |

Net new: none.

**Repo custody.** The five documents are project-generated prose and are repo-eligible. **The three
CSVs are not** — they carry GW rule, ability and weapon text verbatim and are excluded on the same
grounds as the Wahapedia export, the MFM `.txt` files, the faction web and pack files,
`Army_Muster_Rules.txt` and `wh40k_core_rules.md`. Their loss this session is precisely why the local
backup folder now exists.

## Backlog

**9 open:** B63, B62, B61, P2, E21, E22, B60, E12, B17.
