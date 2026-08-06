# NEXT SESSION PROMPT — Session 199

## Turn type: data-only, unless a genuine blocker forces a scope split. No exceptions otherwise.

Read `SESSION_HANDOFF_198.md` first, then this prompt. Session 198 shipped B89's fourth migration — the
six-file Space Marines group (base + Black Templars, Blood Angels, Dark Angels, Deathwatch, Space
Wolves) to MFM v1.1, as one atomic turn (confirmed the group can't split faction-by-faction — see D291).
It also found and stopgap-fixed a genuine source-text defect: a missing comma in
`MFM_Space_Marines_v1.1.txt`'s Marneus Calgar LEADER line.

## Ryan action pending — check before assuming source state
S198 left one open item: **the private repo's `MFM_Space_Marines_v1.1.txt` needs the missing-comma fix
pushed** (Marneus Calgar in Armour of Antilochus's LEADER line — insert a comma between "ERADICATOR
SQUAD" and "STERNGUARD VETERAN SQUAD"). Until that lands, `mfm_points_parser.py` carries a stopgap
(`_KNOWN_SOURCE_FIXES`) that patches the glued token at parse time and fails loudly if the source no
longer contains the expected substring. **Confirm with Ryan whether the private-repo fix has landed
before doing anything with this stopgap.** If it has landed: remove the `_KNOWN_SOURCE_FIXES` entry,
re-run `units_repro_check.py`, confirm still byte-identical (the fix produces the same corrected text
either way, so this should be a no-op swap, not a data change). If it hasn't landed: leave the stopgap
in place, it's still doing its job.

## Remaining B89 candidates (MFM v1.1 adoption)
- **Grey Knights** — own base MFM file, not part of the SM chapter chain (Grey Knights isn't one of the
  five chapters chained to the base SM file). Check `MFM_Grey_Knights_v1_0.txt` vs `v1.1` for the same
  kind of chaining question S198 just resolved for SM — Grey Knights is very likely fully self-sourced
  like TS/DG were (no chapter-override cross-referencing), but confirm from source before assuming.
- **Chaos Space Marines** — still not a candidate. Blocked on World Eaters and Emperor's Children
  (neither built/migrated). Check whether either has become buildable before ruling this out again.
- Remaining Heretic Astartes / Chaos Daemons / Drukhari factions continue after Astartes wraps, per
  standing priority order.

## Standing reminders
- Turn-typing strict: data only. If today's investigation turns up a genuine chaining or new-tooling
  need (mirroring S198's SM discovery), stop and hand off rather than mixing scope into this session —
  but don't assume it's needed without tracing the actual mechanism first, the way S198 did for SM.
- **Check sources directly, don't trust reconciliation-report prose or prior-session summaries at face
  value.** S196/S197/S198 each found something the report or a hardcoded assumption got wrong — treat
  that as the norm, not the exception, and budget time to verify rather than adopt.
- Fix parsers/schema, never hand-edit output — except where a faction's own source file is itself
  hand-authored (CD precedent, D290) or where a narrow, filename-and-substring-scoped stopgap for a
  known source-text transcription defect is the right call (SM precedent, D291) — both are documented
  exceptions, not a general license to patch around inconvenient source text.
- Diff-guard before banking: any regenerated or hand-edited output is verified by key-level diff against
  the prior committed file before being accepted.
- `detachments.json` migrations (enhancement re-prices, force-disposition/unique-tag changes) stay
  tracked separately from `units.json` per faction, per D288/D289/D290/D291's established practice — not
  this turn's scope unless explicitly picked up. Note: the SM chain's detachments side (Black Templars'
  new VENGEFUL HOSTS detachment, several enhancement re-prices) is still open and untouched.
- Close by producing the four documents, regenerating the manifest with `--write` (remember to register
  the new `SESSION_HANDOFF_199.md` in `pipeline_manifest.py`'s GUARDED list **before** running
  `--write`), and running `pipeline_manifest.py --freshness-check` as the **last** command — after every
  other edit, including edits to the handoff itself (leave the handoff's own row in its Files table as
  "(this file)").
