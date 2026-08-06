# NEXT SESSION PROMPT — Session 198

## Turn type: data-only, unless the open question below forces a scope split. No exceptions otherwise.

Read `SESSION_HANDOFF_197.md` first, then this prompt. Session 197 shipped B89's **third** migration —
Chaos Daemons, via a direct hand-edit of the Gen-1 root `Unit_Points.csv` (D290) rather than a
source-file swap, since CD has no `_v1_0.txt`/`_v1.1.txt` selection to swap between.

## Ryan action pending — check before assuming source state
S197 left a genuine custody gap: `Unit_Points.csv` (CD's root file) was hand-edited locally and
`source_manifest.json`'s hash updated to match, but Claude's token to `rd-prime-1357-data-sources` is
read-only — Ryan needs to push the same 6-row edit to that private repo. **Confirm this happened before
trusting a clean `--fetch --data-turn` open.** If the push hasn't landed yet, the source-fetch gate will
hash-mismatch on `Unit_Points.csv` specifically — that is expected and means "wait for Ryan," not a
data corruption signal.

## Open question to resolve before picking today's faction

The remaining migration candidates are: Space Marines (base), Black Templars, Blood Angels, Dark Angels,
Deathwatch, Space Wolves. (Chaos Space Marines is still not a candidate — depends on World Eaters and
Emperor's Children, neither built.) This is S197's second open question, not investigated last session
since Chaos Daemons was the recommended, smaller-scoped pick.

**Space Marines base + its 5 chapter files are chained**: the five chapter files apply via
`--scope-to-army --append` on top of the base SM build (B56a). Before picking a faction, confirm whether
a single chapter can migrate to v1.1 while base SM stays on `_v1_0.txt`, or whether the chapter v1.1
files assume a v1.1 base — check `MFM_Black_Templars_v1.1.txt` (or another chapter) against its
`_v1_0.txt` for any change that only makes sense against an already-migrated base, before assuming
they're independent. This determines whether the six-file group must migrate as one large turn or can
be split faction-by-faction like every migration so far.

## If a faction is confirmed migratable this session

**Steps, mirroring S195/S196/S197's diff-and-verify discipline:**
1. Hash-verify the relevant MFM source file(s) against `source_manifest.json` before use.
2. Diff the `_v1_0.txt` vs `_v1.1.txt` pair directly to confirm the reconciliation report's claims
   independently — S196 and S197 each found the report wrong on at least one item; do not trust it
   verbatim.
3. Run the full documented pipeline, diff against committed `units.json`, confirm only the expected
   faction's units differ and only in `points` (plus `fourth_plus` where B94 applies).
4. Check `rules_assertions.py` for any pinned points values on the changed units, needing reconciliation.
5. Confirm all other armies and all four merged lookups stay byte-identical before promoting the
   regenerated file.

## Standing reminders
- Turn-typing strict: data only, unless the chaining investigation above concludes the six-file SM group
  needs new tooling to migrate cleanly — in that case, stop and hand off rather than mixing scope into
  this data-only session.
- Fix parsers/schema, never hand-edit output — except where a faction's own source file (like CD's root
  CSVs) is itself hand-authored, per D290's reasoning. Confirm which case applies before editing anything.
- Diff-guard before banking: any regenerated or hand-edited output is verified by key-level diff against
  the prior committed file before being accepted.
- `detachments.json` migrations (enhancement re-prices, force-disposition/unique-tag changes) stay
  tracked separately from `units.json` per faction, per D288/D289/D290's established practice — not this
  turn's scope unless explicitly picked up.
- Close by producing the four documents, regenerating the manifest with `--write` (remember to register
  the new `SESSION_HANDOFF_198.md` in `pipeline_manifest.py`'s GUARDED list **before** running `--write`,
  the way S196 and S197 did — the plain gate only catches an orphaned handoff after the fact), and
  running `pipeline_manifest.py --freshness-check` as the **last** command — after every other edit,
  including edits to the handoff itself (leave the handoff's own row in its Files table as "(this file)").
