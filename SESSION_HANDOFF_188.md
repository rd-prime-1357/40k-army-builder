# SESSION HANDOFF 188

**Turn type:** doc-only. Ryan gave no answer to B90's blockers (D279) or B91 this session, and
did not ask for E23's engine turn; instead he reported two new gaps and asked for a design opinion
on one of them. Logged both as scoped backlog tickets rather than starting either build (E28's
mechanism isn't designed yet; B93 explicitly isn't scoped for build until a source pass runs).
**Outcome:** shipped (doc-only). Live behaviour unchanged.

## What happened
1. **Baseline opened green.** `./baseline.sh --fetch --data-turn`, 30/30 gates. Verified S187's
   Files-section hashes: `detachment_effects.json`, `rules_assertions.py`, `DECISION_INDEX.md`,
   `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py` all matched exactly. `pipeline_manifest.json`
   did **not** match the S187-stated hash (`889415b3f838` claimed vs `8c9fedd205e7` found on the
   area copy) — re-running `--write` against the current guarded files reproduced the on-disk file
   byte-for-byte (zero diff), so the manifest content is internally correct against what's actually
   present; the S187 handoff's recorded hash for that one line reads as a transcription slip in the
   document, not a live data problem. Pulled the live `40K_Decision_Log_v3_0.md` manually from the
   repo per the standing B91 gap; hash matched S187's record.
2. **E28 opened (D281) — Detachment selection UI placement.** Ryan asked whether selected
   Detachments/Force Disposition should move from their current always-on centre-list widget to a
   right-panel click-to-configure view, matching the unit mechanic. Checked against the original
   UI decision (D192 item 5, `E1_DETACHMENT_SCOPE.md` §5) before answering: the shipped layout
   already diverges from that plan too — D192 called for a per-row info control opening collapsible
   detail, and E25 later bolted Force Disposition on as its own standalone widget instead. Gave
   Ryan a direct recommendation: move it, keep DP/points visible in the centre list unchanged, and
   attach Force Disposition to a Detachments group-level view rather than under each row, since it
   is one value for the whole selection, not a per-detachment property. Logged as a scoped ticket,
   not designed in engine detail — sized M.
3. **B93 opened (D281) — Enhancement/Upgrade eligibility gap.** Ryan reported that every
   Enhancement's description opens with its qualification requirement, and Enhancements are
   Character-only unless stated otherwise. Checked `enhancementTypeEligible()` against
   `detachments.json`'s 607 enhancement records before logging rather than taking the report at
   face value. Confirmed two real gaps: Upgrades (`is_upgrade: true`) get **zero** type check today
   — live, reachable, not gated behind unbuilt work — and regular Enhancements that name a specific
   keyword/sub-type/unit are over-admitted to any Character army-wide. Also found the qualification
   clause is **not** reliably the description's first sentence as reported — it typically follows a
   sentence of flavour text — and two records have no usable qualification text at all yet
   (Thousand Sons' Stave Abominus: empty description; Chaos Daemons' Leaping Shadows: description is
   just the name). Logged with that correction attached; explicitly not scoped for build — needs a
   full source pass across all 607 records first. Sized L, spans sessions.
4. **No engine, data, parser, or assertion touched.** `index.html` unchanged, still v6.15.
   `rules_assertions.py` unchanged, still 116/116.

## State
- Baseline: green, 30/30 gates at close (verified after the manifest `--write` below).
- `index.html` unchanged, still **v6.15**.
- Live behaviour: unchanged. B93 describes a real, already-live gap (Upgrade type-checking) but
  nothing was built this turn to close it.
- `repo_check` will show four files differing from the committed repo until this session's changes
  are pushed: `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.json`,
  `pipeline_manifest.py` — expected, not a problem. `40K_Decision_Log_v3_0.md` also differs
  (unguarded, repo-only per B91 — push it manually alongside the others).

## Decisions still waiting on Ryan (unchanged from S186/S187)
1. **B90 (D279):** points edition (v1_0 vs adopt v1.1 first, B92) and roster target (confirm
   BT≈90 not 76, and whether Legends/Forge-World datasheets count).
2. **B91:** which decision log is canonical, so the live `_v3_0` gap stops widening.

## Files (SHA-256, first 12)
| file | sha256:12 | note |
|------|-----------|------|
| `40K_Decision_Log_v3_0.md` | ba5357d90d06 | appended D281 (live log; unguarded — B91) |
| `DECISION_INDEX.md` | cc4c4e82f0d4 | D281 index entry |
| `OPEN_ITEMS_BACKLOG.md` | 988a9750311f | +E28, +B93 bodies and summary line; 17→19 open |
| `pipeline_manifest.py` | 310b6e2c79e2 | `SESSION_HANDOFF_188.md` appended to GUARDED |
| `pipeline_manifest.json` | b46bb74236aa | regenerated, `--write` (144 guarded files) |
| `NEXT_SESSION_PROMPT.md` | (see next file) | S189 (unguarded by design) |
| `SESSION_HANDOFF_188.md` | (this file) | net-new; hash banked in the manifest by `--write` |

## Backlog
19 open, up from 17. Beginning: B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, B87, B88,
B89, B90, B91, B92. Resolved: none. Added: E28, B93. Ending: B69, B70, B75, B85, B86, P2, P4, E23,
B67b, E12, B17, B87, B88, B89, B90, B91, B92, E28, B93.
