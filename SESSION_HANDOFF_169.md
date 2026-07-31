# Session handoff — Session 169

**Type: engine-only** (`index.html` v6.11 → v6.12; one new harness; one assertion updated). Decision
recorded: **D258.** Closes **B72** and **B80.**

---

## 1. Baseline at session open

`./baseline.sh --fetch` ran clean: 24/24 gates pass (3 tier-B skipped, sources not loaded — correct,
no data turn), 122 guarded files matched, `repo_check` clean (0 differs, 0 GW-derived material). No
reconciliation needed at open.

## 2. Triage — five Ryan-reported UI/data bugs, re-derived from source

All five (B69, B70, B72, B73, B80) were untriaged since S152. Each was traced against `units.json` /
`unit_loadouts.json` / `index.html` before deciding what to build. The turn-typing split is what drove
the session scope:

- **B72 — engine.** The Invader ATV's loadout data is already correct (`optional, max 1,
  non_consuming`, no size gate); the bug is in the engine.
- **B80 — engine.** A section-ID collision in the combined-popup renderer.
- **B70 — data/parser, tangled with B73.** "Wardens of Ultramar" (Epic Hero, unit_id in `units.json`)
  has `leader_ability_name: null` on both model groups — the "Heroes of Ultramar" ability was never
  captured as a leader ability by the parser — while its `leader_eligible_units` list is populated and
  itself carries `VANGUARD VETERAN SQUAD WHITE SCARS`, an out-of-faction entry that is the exact B73
  defect. Not an engine turn; belongs with the B73 source audit.
- **B69 — corrected and generalized (D259, this session).** Ryan flagged that his prior instruction
  never reached the record: remove the "(see left)" cue from Guilliman's *Author of the Codex* entirely
  and nest the granted abilities under it — not rewrite to "(see below)". Investigating generalized it to
  six units across four factions (Guilliman, Grimaldus, Mortarion, Abaddon, Magnus, Ulrik) with the same
  select-N-from-pool shape. The selector→pool link is absent from our data (source column-typing collapsed
  at B4/D155), and "(see below)" cues elsewhere are valid intra-text references that must be left alone, so
  no safe engine-only strip exists. Re-scoped S→M as a data turn (parser re-capture, asserted) + an engine
  turn; no hardcode shipped. Open scope choice for Ryan: all six or Guilliman-only.

Two clean engine bugs (B72, B80) made a coherent engine-only session; the rest are their own turns.

## 3. Turn shipped: B72 — Invader ATV offered at every legal squad size

The Outrider Squad's Invader ATV is the **only** `non_consuming` optional model group in the whole
dataset, so it is the only unit that exercises this path. `loGroupCounts` and `loOptHeadroom` already
exempt `non_consuming` groups from model reservation (they ride alongside the size bracket), but
`loOptMax` did not — it ran the general clamp `min(band, headroom - used)`. Headroom is 0 at the
3-model bracket (sergeant 1 + fill min 2 = 3), so `loOptMax` returned 0, the render's `noRoom` gate
read "no models left," and the ATV appeared only at size 6.

Fix in `loOptMax`: return the band directly for a `non_consuming` group, and stop counting a
`non_consuming` sibling toward `used` (no current group uses the sibling path, but it keeps the three
functions' semantics aligned). D0-facing — a legal option must be reachable. Blast radius: one unit.

## 4. Turn shipped: B80 — combined popup section IDs are now per-member

`buildModalConfigured` runs twice in the combined attached-unit popup (leader panel, then bodyguard
panel). Its collapsible sections used hardcoded IDs (`cfg-abilities`, `cfg-rules`,
`cfg-wargear-abilities`, and `cfg-leader` via `leaderSectionHtml(raw, 'cfg')`), so both panels emitted
the same IDs and `getElementById` returned the first — the leader's, rendered first. That is exactly
the reported symptom (bodyguard chevron opens the leader's content), confirmed generic across two
unrelated pairs.

Fix: `buildModalConfigured` gains an optional `idScope` parameter, woven into every section ID via
`sidBase = 'cfg' + (idScope ? '-' + idScope : '')`. The single-unit caller passes no scope and keeps
the exact original `cfg-...` IDs; `buildModalCombined` passes a distinct `'m' + listId` scope per
member. No extraction from `index.html` — single-file constraint respected.

## 5. Verification

New harness **`b72_check.js`** (21 checks), wired into `baseline.sh` after `b58_check` and guarded in
`pipeline_manifest.py`:
- B72 half pulls `loOptMax`/`loGroupCounts`/`loOptHeadroom` out of `index.html` and asserts the ATV is
  offerable at size 3 **and** 6, that taking it leaves the Outrider body at fill (2 at size 3, 5 at
  size 6), and that the band cap still holds at 1.
- B80 half is a static guard: `buildModalConfigured` scopes every section ID through `idScope`, no bare
  `cfg-...` literal remains in it, and `buildModalCombined` passes distinct per-member `listId` scopes.

`rules_assertions.py`'s `b7b_combined_popup` render check **fired at baseline open** — its literal
match on the old three-parameter `buildModalConfigured` signature caught the added parameter. That is
the guard working, not a false alarm; it was updated to the new four-parameter shape and extended to
assert the per-member `listId` scoping, so it now polices B80 rather than tolerating it. The rest of
the baseline was clean: 72/73 tier-A assertions (the one FAIL was P3 manifest drift on this session's
own changed files, expected pre-`--write`), all harnesses no regressions.

## 6. What's next

10 open after this session's two closes (12 counting P2 and B67b, which are Ryan-action process items):
B69, B70, B73, B75, B76, B77, E23, E12, B17, plus P4 the standing capacity lever.

- **B69** (D259) is re-scoped as a data+engine arc (see §2); awaiting Ryan's scope choice (all six
  select-N-from-pool units, or Guilliman-only). Data turn first (parser re-capture of selector→pool maps,
  asserted), then engine render. Not a quick engine tweak.
- **B70 + B73** are one linked data/audit arc: a source-level audit of Leader `leader_eligible_units`
  lists against actual Matched Play legality (B73), which also supplies the fix for B70's null
  `leader_ability_name` and out-of-faction eligibility entry. B73 is M-sized; start with the audit, not
  a build. Likely a parser fix (never hand-edit `units.json`).
- **B77** (SCINTILLATING LEGIONS keyword) and **B76** (drop version numbers from rolling-doc filenames)
  remain small fillers. **B75** stays blocked on Ryan's flag-count report.
- **P4/M2** (project-area capacity) remains a watch item — Ryan reported 79% at S166/167, unconfirmed
  since; he did not re-report this session.

---

## 7. Files

| File | SHA-256 (first 12) | Status |
|---|---|---|
| `index.html` | (see manifest) | updated — v6.11 → v6.12; `loOptMax` non_consuming exemption (B72); `buildModalConfigured` gains `idScope`, combined caller passes per-member scope (B80) |
| `b72_check.js` | (see manifest) | **net new** — B72/B80 harness (21 checks); added to `GUARDED` and to `baseline.sh` |
| `baseline.sh` | (see manifest) | updated — `b72_check` gate added after `b58_check` |
| `rules_assertions.py` | (see manifest) | updated — `b7b_combined_popup` signature match refreshed to 4 params, per-member scoping asserted |
| `pipeline_manifest.py` | (see manifest) | updated — `b72_check.js` and `SESSION_HANDOFF_169.md` added to `GUARDED` |
| `40K_Decision_Log_v3_0.md` | (see manifest) | updated (D258) |
| `DECISION_INDEX.md` | (see manifest) | updated — D258 one-liner |
| `OPEN_ITEMS_BACKLOG.md` | (see manifest) | updated — B72, B80 moved to Closed/Shipped; 12 open |
| `NEXT_SESSION_PROMPT.md` | (see manifest) | overwritten (S170) — not guarded, by design (D231) |
| `SESSION_HANDOFF_169.md` | (self) | new (rolling) |
| `pipeline_manifest.json` | (issued last — see §8) | regenerated, reflects the files this session changed |

**Net New Files:** `b72_check.js` — the project has never held a harness for this role before. The
handoff and next-session prompt are the usual rolling documents; every other file is an update.

**Ryan cannot download from the project Files panel** (S159 finding). All changed files are delivered
as outputs this turn for repo push and project-area upload.

## 8. Manifest reissued last, per D251's ordering rule — checked by `--freshness-check`

`SESSION_HANDOFF_169.md` and `b72_check.js` were appended to `pipeline_manifest.py`'s `GUARDED`, this
handoff's text and D258's decision-log entry were finalized, then `pipeline_manifest.py --write` ran,
then `pipeline_manifest.py --freshness-check` ran as the true last step. Nothing touched the decision
log or this handoff afterward.

## 9. Backlog

- **Beginning:** 14 open — B69, B70, B72, B73, B75, B76, B77, P2, P4, B80, E23, B67b, E12, B17
- **Resolved:** 2 — B72, B80
- **Added:** 0
- **Ending:** 12 open — B69, B70, B73, B75, B76, B77, P2, P4, E23, B67b, E12, B17
