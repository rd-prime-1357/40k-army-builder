# Session Handoff 142

## Baseline at open

Three of S141's four Files-section hashes verified byte-identical against the mount
(`40K_Decision_Log_v3_0.md`, `DECISION_INDEX.md`, `NEXT_SESSION_PROMPT.md`). `OPEN_ITEMS_BACKLOG.md`
did **not** match — but on inspection its content was already ahead of S141 (Ryan's core-rules
deletion confirmed, capacity read at 90%, and a Ryan-side ticket B61 logged), i.e. Ryan had edited it
directly after S141 closed rather than a bad sync. Treated its content as current. `./baseline.sh
--no-repo` ran clean before any new work: 23/23 gates, 102/102 assertions. `repo_check.py` was not
present/runnable in this sandbox (no repo clone), so the repo custody gate was skipped this session —
flagged for S143 open.

Capacity confirmed at **90%** (from 92%), consistent with `wh40k_core_rules.md`'s removal (S141).
P4's recorded call — proceed to B60 rather than spend a turn on the decision-log split — stands.

## What shipped — B60 closed (D221)

**Turn type: data.** `detachment_parser.py` fix + `detachments.json` regeneration + manifest reissue.
No engine, UI or tooling change.

`restrictions` was populated by text-source accident, not content: 12 of 143 records carried it, 13
more carried the identical chapter-exclusivity sentence buried in `rule_text`, and two of the 12 were
separately corrupted. Root-caused to two independent defects, both fixed against source:

1. **Wahapedia tier folded the restriction into `rule_text` in two shapes** — a separate "Restrictions"
   ability row, and a `<span class="hi_custom">RESTRICTIONS</span>` section embedded inside a rule's
   own description. `waha_text` now skips the named row and splits descriptions on their `hi_custom`
   headers (verified header-only, never mid-sentence), lifting the RESTRICTIONS section out while
   leaving other sections (KEYWORDS, sub-rules) on the rule. Structural, so it caught phrase variants
   a sentence match would miss.
2. **The DA pack bled stratagem clauses into two records' `restrictions`** — on LION'S BLADE and
   WRATH OF THE ROCK the pack collates CP tokens at the page foot, defeating stratagem recognition, so
   each stratagem's inline `RESTRICTIONS:` clause re-opened detachment-restrict mode. `_da_consume`
   now marks where a detachment's stratagem region begins and refuses to open restrict mode past it.
   LION'S BLADE keeps only its exclusivity sentence; WRATH OF THE ROCK correctly keeps nothing; the 3
   already-clean DA records are unchanged.

**Result:** `restrictions` populated for all 25 chapter-exclusive detachments, zero left in
`rule_text`, no stratagem/CP debris. Change fully contained — 16 records, `restrictions` (16) and
`rule_text` (14) only, no key-set change, every `_meta` count identical. 23/23 gates, 102/102
assertions; fixed point re-banked, manifest reissued.

## Decisions needed

None blocking. One flag carried forward: the restriction consistency is not pinned as an executable
check. Adding one to `rules_assertions.py` is a tooling change and would break turn typing on this
data-only turn, so it is filed as **B60a** (tooling, S) rather than mixed in. Nothing is
under-enforced today — `restrictions` is not read for legality (enforcement is via
`detachment_effects.json`) — but per *facts as executable checks* the shape should be pinned before
anything consumes the field.

## Shipped / changed

`detachment_parser.py` — `waha_text` peels both restriction shapes via a new `_split_hi_sections`
helper; `_da_consume` gains a stratagem-region gate. `detachments.json` — regenerated, re-banked.
`pipeline_manifest.json` — reissued (parser + output hashes moved). `40K_Decision_Log_v3_0.md` — D221
appended. `DECISION_INDEX.md` — D221 indexed. `OPEN_ITEMS_BACKLOG.md` — B60 moved to Closed/Shipped,
B60a added, header count updated. `NEXT_SESSION_PROMPT.md` — rewritten for S143.

### Net New Files
None. (B60a is a backlog entry, not a file; its harness lands when B60a is built.)

### Files (SHA-256, first 12 chars)
- `detachment_parser.py` — `ecb29b0358a4`
- `detachments.json` — `0733236ecbcf`
- `pipeline_manifest.json` — `38a312d5577f`
- `40K_Decision_Log_v3_0.md` — `d883d6aa6967`
- `DECISION_INDEX.md` — `3f7a5a98bef7`
- `OPEN_ITEMS_BACKLOG.md` — `4d4752b84c16`
- `NEXT_SESSION_PROMPT.md` — `15df8c7d9d72`

**Repo custody:** `detachment_parser.py` and `pipeline_manifest.json` are repo-eligible.
`detachments.json` is **not** — it carries GW rule prose in `rule_text`, `restrictions` and
enhancement descriptions, excluded on the same content grounds as the other prose-bearing outputs.
The decision log, index and backlog are repo-eligible docs. `repo_check.py` unavailable this
session — verify custody at S143 open if the repo is reachable.

## Backlog summary

- **Beginning (7 open):** P2, P4, E23, B60, E12, B17, B61
- **Resolved (1):** B60 (D221)
- **Added (1):** B60a (tooling — pin the restriction consistency as an assertion)
- **Ending (7 open):** P2, P4, E23, E12, B17, B61, B60a
