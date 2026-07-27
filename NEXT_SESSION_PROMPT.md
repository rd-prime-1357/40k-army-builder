# Next-session prompt — Session 151

S150 confirmed `--fetch` comes back live-green against the real public repo (D233) — only the one
pre-existing, already-diagnosed drift (`40K_Data_Pipeline_Process_v0_6.md`) shows, not a new problem.
**M1 is unblocked.**

## Read this first

`SESSION_HANDOFF_150.md`, `D233_entry.md`, and the P4 body in `OPEN_ITEMS_BACKLOG.md` before starting.
Do not trust remembered session/version numbers — this file's own header is the only thing to check
against `SESSION_HANDOFF_150.md`.

## M1 status

M1 (evict the repo-resident set, ~3.9 MB) is Ryan's task, not a session — no session should attempt it.
If S151 opens and M1 has already run, the baseline will look different from S150's (`--no-repo` may no
longer find its old copies locally; `--fetch` becomes the only path). Reconcile against whatever
`baseline.sh` actually reports at open rather than assuming M1 did or didn't happen.

## Baseline at open

Run `baseline.sh` (try `--fetch` first now that it's confirmed live; fall back to `--no-repo` only if
`--fetch` itself fails for a new reason, not the known `40K_Data_Pipeline_Process_v0_6.md` drift).
Verify S150's carried-forward files match — nothing was built or changed in S150 itself, so this
should match S149's set byte-for-byte plus `DECISION_INDEX.md`/`OPEN_ITEMS_BACKLOG.md`/`D233_entry.md`.

## What's next after M1

Per the standing sequence: B68 (engine — `loadout_parser.py`/`equipped_parser.py` resolve by unit name
not army+unit_id, blocking CSM's loadout-defaults pass) → CSM turn B as the M2 dress rehearsal → M2
(evict the 71 GW sources) → CSM turn C. Pick whichever of these is actually next given what M1's state
turns out to be at open — this is a sequencing call, not one that needs Ryan's input.

## Two small items carried from S150

- Recommend pushing the area's `40K_Data_Pipeline_Process_v0_6.md` to the repo in the next upload
  batch, closing the one remaining drift. Proceed on this unless Ryan objects.
- A batch of CSVs matching files already in the project area was attached to S150's opening message
  and was not added to the area (flagged, not actioned). If Ryan re-sends them intentionally, confirm
  what they're meant to replace before treating them as anything other than duplicates.

## Turn type

Depends on what's picked. B68 is engine-only. CSM turn B is data-only. M2 (if reached) is tooling-only.
Whichever is chosen, hold to single-type discipline — no mixing.
