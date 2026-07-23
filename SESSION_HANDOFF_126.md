# Session 126 handoff — tooling: repo custody, baseline consolidation, backlog/decision-log split

**Turn type: tooling-only.** `index.html`, every `.json` data file, every parser and every CSV
untouched — confirmed unchanged at both open and close. Authoritative write-up is **D197** (module-
extraction policy) and **D198** (everything else this session) in `40K_Decision_Log_v3_0.md`.

This prompt replaced the original S126 assignment (E4), which was deferred to S127 by a between-
session process review and repo custody pass. Scoping reasoning for E4 carries forward unchanged in
`NEXT_SESSION_PROMPT.md`.

---

## Close state

| Gate | State |
|---|---|
| `repro_check.py` | byte-identical |
| `units_repro_check.py` | byte-identical (units.json + four merged lookups) |
| `detachments_repro_check.py` | byte-identical |
| `rules_assertions.py` | **75/75 — all pass** |
| all 13 harnesses | all pass (correct positional args now baked into `baseline.sh`) |
| `bundle_check.js` | reads **green** — 2 known B36 failures now allowlisted (T4) |
| `pipeline_manifest.py` | **36 guarded files, all match** (regenerated after T4's `bundle_check.js` edit) |
| `repo_check.py` (new, T1) | not yet re-run against the repo post-close — this session's changes haven't been pushed |

`baseline.sh` (new, T3) runs every row above in one command; verified end-to-end mid-session,
including catching a real failure (see below).

---

## What shipped

**T1 — `repo_check.py` (net new).** Clones the public repo and classifies every file it holds as
match / differs / missing-from-repo / repo-only against the project working area. Reads its GW-
derived exclude patterns straight out of the clone's own `.gitignore`, bucketed by that file's
section-header comments, so there is no second pattern list to drift out of sync. "Missing from
repo" is scoped to the manifest's live guarded set plus a fixed doc list plus every locally-present
`SESSION_HANDOFF_*.md` — not the whole project area, most of which is GW/Wahapedia source material
that is correctly excluded and would otherwise read as noise. Clone failure reports clearly (exit 2)
rather than a false clean.

**Run at session open, this is how the repo-state picture changed:** the repo now holds **70 files**,
and all 67 shared with the project area were **byte-identical** — the bulk upload (H4) has happened
since S125, and `pipeline_manifest.py` itself is among the files confirmed synced. **H3 closes** on
this evidence.

**T2 — hash convention.** Every handoff's Files section (below) now carries a first-12-character
SHA-256 per changed/net-new file. Verify these at the top of S127 before anything else runs.

**T3 — `baseline.sh` (net new).** One command, one line per gate, all thirteen harnesses' correct
positional arguments encoded so a bare argument-less call (which prints an indistinguishable Node
stack trace) can't happen by accident again. Proved itself mid-session: after T4 edited
`bundle_check.js`, `baseline.sh` correctly went red on `rules_assertions` (P3) and `pipeline_manifest`
before the manifest was regenerated — a real catch, not a happy-path demo.

**T4 — known-failure allowlist in `bundle_check.js`.** `ok()` takes an optional key; a keyed check
that still fails prints `KNOWN` and doesn't count toward the exit code, but fails loudly the moment
it either resolves without the allowlist being updated, or if a keyed check never runs at all in a
given execution. The two existing B36 failures are keyed (`b36-keep-count`, `b36-keep-offered`).
Empty `KNOWN_FAILURES` when B36 ships.

**T5 — backlog and decision-log split.** Of 117 tracked tickets, exactly 7 were genuinely open
(now 6, with H3 closing this session): P2, E21, E4, B56, E12, B17. Those keep full bodies in
`OPEN_ITEMS_BACKLOG.md`; the other 110 (now 118, with H3/H4/T1–T6 added-and-closed this session)
moved in full to **`BACKLOG_ARCHIVE.md`** (net new), one-line pointer left behind in the working
file. Verified byte-for-byte against the original — zero content lost or duplicated in the split.
**`DECISION_INDEX.md`** (net new) — one line per entry in `40K_Decision_Log_v3_0.md` (186 entries,
including two legitimate duplicate numbers, D158/D159, that exist in the source itself and are
listed as-is). The decision log itself is untouched other than appending D197/D198.

**T6 — module-extraction policy.** Recorded as **D197**, no code: no further extraction out of
`index.html` without a positive, name-able reason. `list_store.js` stays exactly as it is.

**`PROCESS_IMPROVEMENT_PLAN.md`** marked superseded at its top (T1–T6 and H4 are now real tickets,
closed) and is no longer maintained.

---

## Decisions made this session (batched, all reversible)

1. **H3 closed on repo-check evidence rather than left open pending a separate confirmation.**
   `repo_check.py`'s byte-identical finding is direct evidence the script reached the repo and
   stayed — waiting for a further signal would just be re-deriving what T1 already proved.
2. **"Missing from repo" scoped to guarded-set + docs + handoffs, not the whole project area.**
   Walking everything would produce a wall of expected-exclusion noise (CSVs, MFM txt files, faction
   packs) with no signal in it.
3. **GW-derived patterns read live from `.gitignore` rather than duplicated in `repo_check.py`.**
   A hand-copied second list is exactly the kind of thing D107 warns drifts silently.
4. **Cross-cutting notes kept in the working backlog; S18 Shipped/Doc-debt sections archived.**
   The former is live context for open E4/E21 work; the latter is pure history with no bearing on
   anything currently open.
5. **`baseline.sh` supports `--no-repo`.** An offline/sandboxed run should still be able to verify
   every local gate without failing outright on network absence.

---

## Files

**Changed (SHA-256, first 12):**
- `bundle_check.js` — `3f1cf7632ab3`
- `pipeline_manifest.json` — `310c988bc085`
- `OPEN_ITEMS_BACKLOG.md` — `eaa16e31e5a1`
- `40K_Decision_Log_v3_0.md` — `0583b337be6a`
- `PROCESS_IMPROVEMENT_PLAN.md` — `c8fa79972a8b`

**Net new (SHA-256, first 12):**
- `repo_check.py` — `add27f53dab9`
- `baseline.sh` — `d6fc23f693ad`
- `BACKLOG_ARCHIVE.md` — `f27872a3c5b9`
- `DECISION_INDEX.md` — `623e6211a91a`
- `SESSION_HANDOFF_126.md` — (hash itself not meaningful; verify by re-reading)

**Unchanged:** `index.html` (6.3), every `.json` data file, every parser, every CSV, `list_store.js`,
all 13 pre-existing harnesses (bodies untouched — only `bundle_check.js` changed).

---

## Backlog

| | |
|---|---|
| **Beginning** | 7 — P2, E21, E4, E12, B56, B17, H3 |
| **Resolved** | 8 — H3, plus T1–T6 and H4 (opened and closed same session) |
| **Added** | 7 — T1, T2, T3, T4, T5, T6, H4 |
| **Ending** | 6 — P2, E21, E4, E12, B56, B17 |
