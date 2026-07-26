# Session Handoff 149

## Baseline at open

S148's carried-forward hashes matched byte-for-byte (all eight: units.json, abilities.json,
rules.json, weapon_abilities.json, datasheet_wargear_abilities.json, units_repro_check.py,
rules_assertions.py, pipeline_manifest.json). `baseline.sh --no-repo` ran 21/23, the same seven B68
unit_ids as S148's open — the diagnosed, carried-forward state from D230, not a regression.

## What happened — D232, M0 built and proven (tooling-only, nothing evicted)

M0 was this session's full assignment per `NEXT_SESSION_PROMPT.md` and `P4_ARCHITECTURE_SCOPE.md`.
All five scoped deliverables shipped. Full reasoning in `D232_entry.md`; the shape:

- **`pipeline_manifest.py`** extended 41 → 101 guarded files (full public-repo coverage). Fixed a
  pre-existing gap: it never guarded itself, unlike every other gate script.
- **`baseline.sh`** gained `--fetch` (tarball fetch-verify-overlay against the manifest, area copy
  wins) and `--data-turn` (token-authed private-source fetch, zip fallback, loud refusal with
  neither). Tier detected live from `source_manifest.json`, never assumed from a flag.
- **`rules_assertions.py`** gained `--tier a`, auto-classified per assertion by walking reachable
  bytecode (names + GW filename constants) rather than hand-tagging ~150 entries. Testing against a
  sources-absent simulation caught two real gaps before they shipped: three assertions that open a
  GW file directly by filename (missed by a first, names-only pass) and one legitimate new census
  reference the extension itself introduced. Both fixed; re-verified clean.
- **`repo_check.py`** gained the `SOURCE_REPO_TOKEN.txt` custody guard (live-clone check,
  bound-file-list check, content scan) plus a `.gitignore` line.
- **`source_manifest.json`** created — 70 GW source files, not the 71 D231 stated (see Decisions
  needed).

**Exit test:** proven correct by simulation, not literally green this session — a structural
one-session gap, not a bug. `--fetch`'s only failing gate (`fetch-verify`) fails because the *real*
public repo hasn't received tonight's push yet, so it's still checked against the old 41-entry
manifest; copying this session's changes into a local copy of the fetched tree and re-running the
same check passes clean (101/101), proving the mechanism. `repo_check.py` shows 7 "differs" — six are
this session's own unpushed edits, and one (`40K_Data_Pipeline_Process_v0_6.md`) is a pre-existing,
previously-uncaught drift (area is ahead of the repo by a documented B56a step) that only surfaced now
because M0 brought `repo_check.py` back into the loop. Sources-absent behaviour (stash/restore all 70
GW files) independently verified: the three repro gates print loud, counted `SKIP` lines; `--tier a`
passes without touching anything missing.

### Decisions needing Ryan — none outstanding

The GW-source count question is resolved: 70, confirmed. A first screenshot pass appeared to show
three files absent (`MFM_Tau_Empire_v1_0.txt`, `MFM_Titan_Legions_v1_0.txt`,
`MFM_Thousand_Sons_v1_0.txt`), and `source_manifest.json` was briefly rebuilt to 67 on that basis.
Ryan re-checked and the screenshot pass had simply skipped a row — all three are genuinely present,
and the original 70-file count (and manifest) was correct the whole time. Restored to 70 entries;
full baseline re-run clean afterward.

Both items D231 carried into M0 are settled by this session's build and needed no further input:
the bulk-deletion screenshot amendment (M1/M2) and dropping `NEXT_SESSION_PROMPT.md` from the hash
list — done below, this handoff is the first to drop it.

## Net New Files

- `source_manifest.json` — SHA-256 of every GW-derived source file. No prior file plays this role.

## Shipped / changed

`pipeline_manifest.py`, `baseline.sh`, `rules_assertions.py`, `repo_check.py`, `.gitignore` — see
D232 for full detail on each. `DECISION_INDEX.md` and `OPEN_ITEMS_BACKLOG.md` updated (D232 entry;
P4's open-item body updated to reflect M0 built, M1 next). `D232_entry.md` delivered standalone (same
pattern as D231_entry.md) since the full decision log is repo-only.

## Files (SHA-256, first 12 chars)

- `pipeline_manifest.py` — `94c286eeb974`
- `pipeline_manifest.json` — `d35a74b66d0f`
- `rules_assertions.py` — `69378312d8d1`
- `repo_check.py` — `5117d96d201a`
- `baseline.sh` — `69ca093c5b23`
- `.gitignore` — `3abbe6bb68ae`
- `source_manifest.json` — `bd89c908cfdc` (70 entries, confirmed against Ryan's screenshots)
- `DECISION_INDEX.md` — `2e51cb2587d9`
- `OPEN_ITEMS_BACKLOG.md` — `c2c24c9e763c`
- `D232_entry.md` — `c6d072cea738`

**This is the first handoff to drop `NEXT_SESSION_PROMPT.md` from this list**, per D231/M0 item 6 —
it is legitimately edited after this handoff is finalized, so its hash could only ever false-alarm.

Unchanged this session (carried from S148, re-verify at S150 open): units.json `eb370386ccf7`,
abilities.json `051bdd9ceb08`, rules.json `b347222a3bc9`, weapon_abilities.json `ff4379837df4`,
datasheet_wargear_abilities.json `af5be2824e54`, units_repro_check.py `81cb0f825727`.

**Repo custody:** every changed/net-new file above is project-authored code, config, or prose — no
GW-derived text — and belongs in the next public-repo batch. `source_manifest.json` is hashes only
(no GW text) and is explicitly public-repo-eligible per its own design (P4 §5). Excluded as always:
the 70 GW source files themselves (Wahapedia CSV export, MFM `.txt` files, faction web/pack files) —
unchanged this session, still area-only, still the never-commit set.

**Capacity note:** area still at/near 100% — M0 built the fix, M1 (Ryan, no session, ~10 minutes)
applies it once tonight's push lands and S150 confirms `--fetch` is truly green against the live repo.

## Backlog summary

- **Beginning (8 open):** P2, P4, E23, E12, B17, B61, B67b, B68
- **Resolved (0):** none — M0 (P4's first migration step) shipped; P4 itself stays open through M1–M3
- **Added (0):** none
- **Ending (8 open):** P2, P4, E23, E12, B17, B61, B67b, B68
