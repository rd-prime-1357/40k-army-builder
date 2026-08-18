# SESSION HANDOFF 258

**Turn type: tooling.** Custody audit ahead of the project being set aside. `index.html` untouched —
stays **v6.27**. No data file, parser or assertion touched; `rules_assertions.py` stays at **139**.
Backlog **23 open**, unchanged — no ticket was worked.

This session's purpose was different from the usual: not to advance the backlog, but to establish
that nothing exists only in the project file area, which is a working cache and goes stale. The
finding is that the record is essentially complete.

## Session open

Fresh clone of the public repo at `6660dcc`, 250 files. Baseline run twice against that clone: tier-A
only gives 35/35 with 5 tier-B gates skipped; `--fetch --data-turn` gives **42/42**, including the
three repro checks and B87/B88. That second run is the important one — it proves the committed
parsers plus the private sources still reproduce the shipped `units.json` and `detachments.json`
byte-for-byte. The repo holds a working chain, not just a pile of files.

`detachments_repro_check.py` in the project area was stale again, for the third consecutive session.
See below; the standing ask is being dropped rather than repeated.

## What was found

**99 of 104 project-area files are byte-identical to their repo counterparts.** Five are not, and
four of those five are correct:

| file | status |
|------|--------|
| `Thousand_Sons_web.txt` | GW-derived; correctly absent from public repo, present in private (B108 holding) |
| `SOURCE_REPO_TOKEN.txt` | credential; must never be committed |
| `EMPEROR_S_CHILDREN_BUILD_SCOPE.md` | in repo under its true apostrophe name, byte-identical; mount strips the apostrophe (D331) |
| `gw_source_deletion_checklist.txt` | deliberately deleted from repo (`8264590`); filename list only, no GW text; completed one-time checklist, left deleted |
| `Example_of_what_not_to_do.md` | **never in any commit — the one real gap.** Process reference, no GW material. Handed back for push. |

**`detachments_repro_check.py`'s divergence runs the opposite way to what three sessions assumed.**
The repo copy is four lines *longer* — it carries the B93 bearer-restriction term vocabulary
(`Datasheets_keywords.csv`, `Datasheets.csv`) in its tier-B source list; the project-area copy does
not. The repo copy is authoritative and nothing is at risk. S256 and S257 both asked Ryan to
re-upload it and both then took the repo copy anyway. **The ask is dropped.** Standing behaviour from
here: always take the repo copy at open, never ask.

**`SESSION_HANDOFF_203.md` was never committed.** The chain runs 125–257 with exactly one gap, and
the file appears in no commit on any branch. Sessions 1–124 pre-date the convention and were never
committed — expected, not a loss. S203 sits inside the covered range, so it is a genuine hole. If no
local copy survives it is unrecoverable. The loss is bounded: the decision log and `DECISION_INDEX.md`
both carry that session's substance.

**The private sources repo is complete.** All 85 files declared in `source_manifest.json` are present
among its 88 blobs. A one-in-seven sample was re-hashed from the API against the manifest's recorded
digests — 13 sampled, 13 matched. The three extra blobs (`Thousand_Sons_web.txt` and two dated faction
reference `.md` files) are undeclared but harmless; they are inputs the manifest does not gate on.

## What shipped

`40K_Decision_Log.md` / `DECISION_INDEX.md` — D355 appended. `pipeline_manifest.py` — this handoff
added to `GUARDED`, per the FILES-TABLE ORDERING note added at S257 (append first, then write the
table). No other file changed.

## Net New Files

None. `Example_of_what_not_to_do.md` is net new *to the repo*, but it has existed in the project area
throughout and is not newly created here.

## Ryan action required

**Push these to the public `40k-army-builder`:** `Example_of_what_not_to_do.md` (the custody gap),
`40K_Decision_Log.md`, `DECISION_INDEX.md`, `pipeline_manifest.py`, `pipeline_manifest.json`,
`SESSION_HANDOFF_258.md`, `NEXT_SESSION_PROMPT.md`.

**`SESSION_HANDOFF_203.md`** — if a local copy exists anywhere, push it. If not, it is gone; nothing
further to do.

**The five outstanding render checks are still outstanding**, now six sessions old: S248's Tank Ace
checkbox, S249's Mark of Chaos selector, S250's silent truncation of an over-cap tally, S256's
enhancement picker. S250's remains the one that matters — it is a silent wrong-number case. Scripts
are in `NEXT_SESSION_PROMPT.md`. Nothing this session touched rendered UI.

## What this means for setting the project aside

Once `Example_of_what_not_to_do.md` is pushed, the public repo plus the private sources repo are a
complete, self-reproducing record. The project file area can go stale or be cleared without
consequence. The deployed GitHub Pages app keeps serving `index.html` v6.27 indefinitely and does not
depend on any subscription.

The remaining wind-down item is the cold-storage document — a single orientation file for a future
reader covering what is shipped, what the 23 open tickets actually mean, where the traps are, and
what a revival would have to confront. That is S259's whole job.

## Decisions resolved this session

D355 — custody audit. The record is intact; one file was project-area-only; one handoff never reached
the repo; the `detachments_repro_check.py` re-upload ask is dropped as backwards.

## Backlog

23 open at S257 close; **23 open at S258 close**. Nothing closed, nothing added.

## Files (SHA-256, first 12)

Verify these at S259 open.

| file | sha256:12 | note |
|------|-----------|------|
| `Example_of_what_not_to_do.md` | `cfe030779f6e` | unchanged content; new to the repo |
| `40K_Decision_Log.md` | `efada01619a1` | D355 appended |
| `DECISION_INDEX.md` | `5b4636c178df` | D355 summary appended |
| `pipeline_manifest.py` | `f4242c50aba1` | `SESSION_HANDOFF_258.md` guarded |
| `pipeline_manifest.json` | (regen at close) | regenerated by `--write`; verified by its own gate |
| `NEXT_SESSION_PROMPT.md` | (never guarded) | documented exclusion, D231 |
| `SESSION_HANDOFF_258.md` | (this file) | not self-referential; checked by `--freshness-check` |

Unchanged and not re-delivered: `index.html`, all data files, all parsers, `rules_assertions.py`,
`baseline.sh`, every harness — all as pushed after S257.
