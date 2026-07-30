# Session handoff — Session 159

**Type: tooling.** No engine change, no product-data change banked. `units.json` and the merged lookups
were regenerated and verified but deliberately **not** banked — see "Thousand Sons turn A" below.

Decisions recorded: **D243–D247.** Baseline closed **26/26**.

---

## 1. Reconciliation closed (D243)

The 70-item GW-source deletion checklist is complete. Verified from file-list screenshots, not the
mount — the mount is not evidence of presence or absence. All 70 gone, nothing outside the checklist
touched, `SOURCE_REPO_TOKEN.txt` present and confirmed **not** in the public repo.

`MFM_Chapter_Pass.md`, `MFM_Standalone_Pass.md`, `MFM_FW_Reconciliation.md` **stay**. Our own analysis
write-ups about MFM parsing, no GW text, never on the checklist. `MFM_` means "about MFM", not "is an
MFM file".

Three gates failed at open and all traced to one cause: **S158's repo batch was never pushed.** Seven
files were ahead in the project area; the seventh, `40K_Decision_Log_v3_0.md`, is repo-only for capacity
and so existed in neither place. Walked all 12 historical versions in git to prove it was never pushed
rather than pushed-and-reverted. After Ryan pushed, it hashed exactly to the manifest's recorded
`b46bc24bd8aba4a0` — nothing lost, no reconstruction needed.

`gw_source_deletion_checklist.txt` was committed to the **public** repo despite `.gitignore`'s `*.txt`.
Content-checked (filename tick-list only, no GW text, nothing sensitive published) then untracked rather
than adding a re-include exception — `*.txt` is blunt on purpose.

**Process learning, build this into session close:** Ryan **cannot download from the project Files
panel.** Any repo sync needing a file held only there must route through Claude re-delivering it.

---

## 2. `faction_pack_transform.py` — NET NEW (D244)

Converts GW faction pack PDFs to markdown. Zero-argument: run it from the folder holding the PDFs and it
converts all of them, one `.md` per PDF. `--force` overwrites, `--dir` points elsewhere, or name a
single PDF.

Chosen over chat-assistant conversion because it is deterministic (re-runs byte-identically, which the
repro-check discipline requires), auditable, and keeps GW source out of a third-party service.

Three layout revisions, each failure found by testing:

1. **Midline split** — wrong. Landscape datasheet gutters sit near 60%; a 50% cut ran through stat
   columns and turned `48" 2 3+ 12 -3 D6+1` into `48" 2 3+ 1`. Silent corruption that reads as valid.
2. **Widest-whitespace band** — fixed tables, but flattened occupancy down the page, so one centred
   heading closed the gutter and the page fell back to interleaved full-width extraction.
3. **Row-aware occupancy + full-width band stripping, 4% threshold** — current.

### KNOWN LIMITATION — read before parsing anything

Portrait **Rules Updates** pages cannot be resolved. They mix a full-width title and intro with columns
starting at different heights. Five thresholds swept; none fixed Death Guard p7 while keeping Thousand
Sons correct, and one attempt regressed TS while fixing DG. Threshold tuning is exhausted. **Stopped
rather than half-finish.**

The converter now **flags** these pages — `single-SUSPECT` per page plus a KNOWN LIMITATION note naming
page numbers and stating the text is likely interleaved. **Do not parse flagged pages.** This matters:
the Rules Updates pages carry the keyword changes. Filed **B75**.

Verified good on both packs: all datasheet and detachment pages, stat tables intact, output
deterministic. Converter is repo-safe (no GW content). Converted `.md` files are GW-derived →
**private sources repo only.**

**Awaiting from Ryan:** the flag-count per pack across the full set, to size B75.

---

## 3. Thousand Sons turn A — ran clean, deliberately not banked (D245)

Mechanically fine: **328 → 362 units**, 34 TS units added, **zero existing units changed, zero
removed**, all 34 priced from the TS MFM with no gaps, fixed point reproduces byte-identically.
`unit_loadouts.json` untouched, confirming turns A and B are separable as scoped. `abilities.json` +43,
`weapon_abilities.json` +2 (Brayhorn, Herd Banner — Tzaangors), both purely additive.

`rules_assertions.py` then flagged six `allied_group` carriers outside Death Guard. **Nothing banked.**

### Corrections to wrong readings made during this session

Recorded because they were asserted confidently and would mislead a future session:

- **B61 is not open.** It shipped S133 (D208) and is what *created* `allied_group`, with four assertions
  (B61-1..4) pinning the census. **E22 closed S136 (D214)**; E22b already ships the offer filter, the
  battle-size points sub-cap and the detachment-scoped Warlord ban under
  `Death Guard|TALLYBAND SUMMONERS`.
- **Do not strip `allied_group` to a provenance-only field.** That was recommended in-session and is
  wrong — it would break four shipped assertions and disable E22b's gate, re-opening the D0 violation
  D204 found.
- **The six are not duplicates of Chaos Daemons entries.** That claim came from comparing names only.
  They have different `unit_id`s and differ in `model_groups`, `weapons`, `unit_ability_details`, and
  in points: **Pink Horrors 115 (TS) vs 150 (CD)**, **Blue Horrors 90 vs 125**. Drawing from the CD pool
  would have priced every Scintillating Legions list 35 points high per Horror unit — and looked right.
- **Daemonic Pact's constraints are already enforced**, by E22b, not missing.

### Established from source

`SCINTILLATING LEGIONS` is a **keyword**, not a detachment — TS Rituals and stratagems target "THOUSAND
SONS or SCINTILLATING LEGIONS" units, and allies do not receive the army's own psychic rituals. The real
TS detachments are Changehost of Deceit, Grand Coven, Warpforged Cabal, Warpmeld Pact, Hexwarp
Thrallband, Rubricae Phalanx, Ritual of Regeneration. Death Guard's pack uses `PLAGUE LEGIONS`
identically — one pattern, two factions. Daemonic Pact is a separate army-level mechanism for plain CSM
and Chaos Knights and does not bear on the TS build.

The TS roster is genuinely **34**. The scope doc's count was right; only its assumption that all 34 were
Rubric-side units was wrong.

### Sequencing consequence — turn C precedes turn A

Turn A needs the B61 census extended to the six TS carriers **and** a TS allied unlock in
`detachment_effects.json`. TS has **no detachments** in `detachments.json` until turn C, so there is no
detachment to hang the unlock on. Interim precedent: `Chaos Daemons|SHADOW LEGION` sits with
`enforced:false` until CSM is built. Filed **E24**, which blocks turn A.

The verified `units_repro_check.py` TS block (a per-faction transform → mfm-points → convert sequence
plus a fifth `--in` on the merge call, ~26 lines, mirroring the Death Guard block since TS is fully
self-sourced and needs no cross-file append) is **not banked** — with no TS units in `units.json` it
would break the gate. Cheap to rebuild.

---

## 4. Backlog housekeeping (D246, D247)

**Duplicate ticket ID found.** `B61` was in use twice: the shipped Plague Legions ticket (load-bearing —
four assertion IDs and two decision-log references) and a later Ryan-reported popup bug. The open one is
renumbered **B80**. Surfaced only because open tickets were being counted for this handoff; worth a
periodic ID-collision check.

**Rolling docs will drop filename versions (B76).** The decision log has 29 commits under `v3_0` and no
predecessor volume exists in repo history. Cost real time this session: a backup copy of
`40K_Data_Pipeline_Process_v0_6.md` was 16 lines short — missing Step 2b, the B56a chapter-points
procedure — under an identical version string. Clarity fix, not safety: the manifest hash already
handles content identity and is what caught the short backup. Sequenced behind the TS build.

---

## 5. Files

| File | SHA-256 (first 12) | Status |
|---|---|---|
| `faction_pack_transform.py` | `fa3a113d6204` | **NET NEW** |
| `40K_Decision_Log_v3_0.md` | `1c6205e1c761` | updated (D243–D247) |
| `OPEN_ITEMS_BACKLOG.md` | `fb459df949cf` | updated (+6 tickets, B61→B80) |
| `SESSION_HANDOFF_159.md` | (self) | new (rolling) |
| `NEXT_SESSION_PROMPT.md` | `ccac844dbd91` | overwritten (S160) |

GW-derived, **private sources repo only, never the public repo**: `thousand_sons-June_27th_2026.md`,
`death_guard-July-27th-2026.md`, and the faction pack PDFs themselves.

## 6. Backlog

- **Beginning:** 12 open — B69, B70, B71, B72, B73, P2, P4, B61, E23, B67b, E12, B17
- **Resolved:** none
- **Added:** 6 — B75, B76, B77, B78, B79, E24 (plus B61 → B80 renumber)
- **Ending:** 18 open — B69, B70, B71, B72, B73, B75, B76, B77, B78, B79, E24, P2, P4, B80, E23,
  B67b, E12, B17
