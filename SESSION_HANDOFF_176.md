# Session handoff — Session 176

**Type: data-only.** `mfm_points_parser.py` and `units.json` changed; one assertion added. No engine
(`index.html`) change. Decision recorded: **D267**. B73 shipped.

## 1. Session open

Cloned the repo before trusting the project area. Newest handoff in both places was 175 — no
staleness gap. Same finding as S175: `40K_Decision_Log.md` was absent from the project mount entirely
(content fine — verified via clone, ends at D266 matching S175). Baseline's `--fetch` overlay pulled
it back so the session wasn't blocked. Flagged to Ryan for a file-list screenshot. Also noted a stray
`40K_Decision_Log_v3_0.md` in the repo alongside the current file — stale, ends mid-B76; a repo-hygiene
candidate, not touched this data turn.

Ran `./baseline.sh --fetch --data-turn`: all gates pass, rules_assertions 110/110, sources loaded.

## 2. What shipped

**B73 — MFM made the source of truth for attach eligibility (D267).**

Two S175 assumptions were wrong and were corrected against source before any code ran:

1. **Support is not a separate mechanic.** Ryan supplied the core rules (19.01 / 24.22 / 24.34):
   Leader and Support are the *same* attach-and-form-an-attached-unit machinery, differing only in
   that a bodyguard may hold one Leader **and** one Support at once. A `SUPPORT` block is an
   attach-eligibility list exactly like a `LEADER` block — not B70's join mechanic.
2. **The engine is ability-blind.** `index.html` gates attachment on the eligible list being
   non-empty (line 4676), never on the ability name (only truthiness-checked at 6552). Pulling
   `SUPPORT` lists out of the attach field — as the S175 plan directed — would have silently broken
   attachment for every Support unit roster-wide. So both lists stay in the one `leader_eligible_units`
   field, MFM-sourced; the Leader/Support distinction is recorded in `leader_ability_name`. This
   reversed the "separate field" half of the S175 plan; confirmed with Ryan (Option 1) before
   regenerating.

**Parser rewrite (`mfm_points_parser.py`).** Captures both `LEADER` and `SUPPORT` blocks as exactly
one line each — which removes the D260 over-read that glued the following chapter divider ("WHITE
SCARS") onto the last unit. The MFM block *replaces* the stale 10th-edition Wahapedia ability name and
eligible list wherever the MFM has one; Wahapedia is kept only where the MFM has neither. Every list
entry must resolve to a real datasheet in the file's own stats block or it is dropped and flagged (the
executable guard against the glued token and any cross-faction straggler). Footer cleared when a unit
is overridden to Support. Wardens of Ultramar (000004188) carved out by datasheet id.

**Regeneration + diff-guard.** `units.json` rebuilt through the full documented pipeline (the
`units_repro_check` pipeline, driven to emit rather than only compare). Diff-guard clean: **43 units
changed, only three fields touched** — `leader_eligible_units` (32), `leader_ability_name` (14),
`leader_footer` (13). No unit added or dropped; the four merged glossary lookups are byte-identical.
`units_repro_check` now reproduces the new `units.json` byte-for-byte, confirming the parser change is
deterministic and the committed file is fresh.

The 14 ability flips are all Leader→Support (Ancient/Apothecary/Lieutenant family, Bladeguard Ancient,
Cato Sicarius, Sanguinary Priest, Castellan, Master of Executions, Masters of the Maelstrom). Epic
Heroes narrow to their MFM lists (Calgar 23→13, Kor'sarro Khan 13→6, Uriel Ventris 13→6 — the
cross-chapter 10th-ed extras D260 flagged); a few broaden where the MFM is wider (Watch Master 2→3).
The generic `LEADER` datasheets (Captain/Chaplain/variants) end unchanged in practice: the MFM's extra
entries (Assault Squad, Command Squad, Vanguard Veteran Squad, etc.) are Firstborn units not in the
current build, so they resolve to nothing and drop — exactly as the transform's own `if att in
selected` filter already did. The one real generic narrowing is Adeptus Astartes Librarian (14→12),
covered by "MFM is source of truth."

**Assertion `B73` added** (`rules_assertions.py`, 111 total, tier A): every eligible entry resolves to
a real unit_name, only Leader/Support values exist, Ancient/Apothecary/Lieutenant carry "Support",
Wardens is carved out.

## 3. Wardens conflict — flagged, handed to B70

Wardens' datasheet ability is `HEROES OF ULTRAMAR` (join one of three named units and raise Starting
Strength — B70's bespoke mechanic), but the MFM tags it `SUPPORT` with **six** units (the three plus
Assault Squad, Sternguard Veteran Squad, Vanguard Veteran Squad). MFM-as-source-of-truth would pick
six; the printed ability says three. This is the first identified MFM-vs-pack conflict. Rather than
ship either side, Wardens is carved out of B73 (empty list, no ability — the old glued 6-unit backfill
is gone too) and left for B70 to reconcile. The carve-out set in the parser is keyed by datasheet id
for future conflicts.

## 4. Ryan's stipulations → new tickets

Ryan agreed Option 1 with three stipulations, all logged (none delivered this data turn — they are
engine/UI work):

- **E26** (engine) — enforce one-Leader-one-Support stacking, with special-rule exceptions allowing
  more. Builds on the existing D157 co-leader cap-of-2 + `permitsCoLeader` machinery, which today is
  ability-blind. Stipulations 1+2.
- **E27** (UI) — state Leader vs Support correctly in the attach popups and any exported output; the
  popup heading currently hardcodes "Leader" (index.html 6568). Stipulation 3.

## 5. Decisions still waiting on Ryan

- **B70** — which list governs the Wardens join, MFM's six or the datasheet's three (batch into B70's
  scoping turn).
- **B75 + B85** — still need a local `faction_pack_transform.py` run against 2–3 packs (unchanged).

## 6. Files

| File | Status | SHA-256 (first 12) |
|---|---|---|
| `mfm_points_parser.py` | rewritten (LEADER+SUPPORT capture, MFM override, over-read fix, Wardens carve-out) | `0fa0f8e5810c` |
| `units.json` | regenerated (43 units, leader fields only) | `cebbae1ece16` |
| `rules_assertions.py` | assertion `B73` added (111 total) | `b249c7836990` |
| `40K_Decision_Log.md` | D267 appended | `b3999ac38895` |
| `DECISION_INDEX.md` | D267 index entry added | `f5d9a4e9e816` |
| `OPEN_ITEMS_BACKLOG.md` | B73 → Closed/Shipped; E26/E27 added; B70 updated; S176 count line | `db46a9268ffe` |
| `NEXT_SESSION_PROMPT.md` | overwritten (S177) | `e1df27b1fcff` |
| `SESSION_HANDOFF_176.md` | new (rolling) | — |
| `pipeline_manifest.json` | reissued at close (write + freshness-check) | — |

No GW-derived file is in this delivery set; all are pipeline code/output or project docs.

## 7. Backlog

- **Beginning:** 12 open — B69, B70, B73, B75, B85, B86, P2, P4, E23, B67b, E12, B17
- **Resolved:** B73
- **Added:** E26, E27
- **Ending:** 13 open — B69, B70, B75, B85, B86, P2, P4, E23, B67b, E12, B17, E26, E27
