## D232 — M0 built and proven: fetch-open, tiered gates, source manifest, token custody guard (S149)

M0 (P4/D231's first migration step) built, tooling-only, nothing evicted. All five deliverables from
the M0 scope shipped:

**`pipeline_manifest.py` extended 41 → 101 guarded files** — from pipeline-output coverage to every
file the new fetch-open pulls from the public repo. Four files stay deliberately unguarded, documented
in the script itself: `NEXT_SESSION_PROMPT.md` (legitimately edited after the manifest that covered it
is finalized, same reasoning as its drop from the handoff hash list), `README.md`/`.gitignore`/
`_headers` (repo/hosting metadata nothing reads programmatically), and the manifest can't guard itself.
Also fixed a pre-existing gap unrelated to this extension: `pipeline_manifest.py` never guarded itself,
unlike every other gate script — now it does.

**`baseline.sh` gained `--fetch` and `--data-turn`.** `--fetch` pulls the public repo as one
`codeload.github.com` tarball, verifies the whole tree against `pipeline_manifest.py --dir`, and
overlays it into the workspace (area copy wins — anything already present locally is left alone).
`--data-turn` adds the private-sources fetch: `SOURCE_REPO_TOKEN.txt` first, `gw_sources.zip` fallback,
and refuses to start (exits non-zero, loud) if a data turn has neither and sources aren't already
local. Whether tier-B gates run is detected live from `source_manifest.json`'s own file list, never
assumed from which flag was passed — correct in a session where sources are simply still sitting in
the area (true throughout M0) without needing a special case.

**`rules_assertions.py` gained `--tier a`, tier auto-detected, not hand-tagged.** Hand-tagging ~150
assertions with a fifth tuple element was rejected on the same grounds this whole file exists —
prose-shaped tags drift the moment a helper function is edited. Instead `classify_tier` walks each
assertion's reachable bytecode (names AND string constants, one level of recursion into any
module-level function it calls) against a closed list of source-reading `Sources` methods, the three
embedded rebuild gates, and the actual GW filenames listed in `source_manifest.json`. Caught two real
gaps by testing rather than reading: (1) a first names-only pass missed three assertions (B41-3, E1b-1,
E4b-1) that `open()` `Army_Muster_Rules.txt` directly rather than through a `Sources` method — fixed by
adding the filename-constant check; (2) extending `pipeline_manifest.py`'s guarded list to include
`MFM_Standalone_Pass.md` tripped the existing P4-1 park-and-rerun census (a new, legitimate reference
to a project-authored, already-public reconciliation doc) — fixed by adding it to
`P4_REFERENCED_SOURCES`. With sources present, tier-a now correctly skips 37 tier-B assertions and
passes 67/67 of the rest; tier-all matches today's behaviour exactly (same carried-forward B68 finding,
same seven unit_ids, not a regression).

**`repo_check.py` gained the `SOURCE_REPO_TOKEN.txt` custody guard.** Three independent checks, each
named separately on failure: the token filename actually present in the live public clone (an active
leak); the filename appearing in any of the file lists this script already treats as public-repo-bound
(`DOC_FILES`, the discovered handoff set, or the manifest's guarded set); a token-shaped string
(`github_pat_...`) found inside any file this check already reads. `.gitignore` gained an explicit
line too, belt-and-braces alongside the broader `*.txt` pattern that already caught it.

**`source_manifest.json` created — NET NEW.** 70 entries: area-files-minus-repo-files (same method
D231 used), excluding one `__pycache__` sandbox artifact from the raw 71-file delta. Confirmed
against Ryan's real file-list screenshots (see the resolved decision below).

**Exit test — proven correct, not literally green this session, and that gap is structural, not a
bug.** `--no-repo` (old path): 21/23, the same carried-forward B68 state as S148's open — not a
regression. `--fetch` (new path): fails exactly one gate, `fetch-verify`, and only because the *real*
public repo hasn't received tonight's push yet — it still holds the old 41-entry manifest, so checking
the freshly-fetched tree against my new 101-entry `pipeline_manifest.py` correctly reports the old tree
as short 60 files. Confirmed this is the live remote being stale, not a code defect, by copying this
session's changed files into a local copy of the fetched tree and re-running the same check: it passes
clean (101/101). A live, literal green `--fetch` run is therefore only possible *after* the push lands
— an inherent one-session chicken-and-egg in the M0 design, not a divergence to route around. `repo_check.py`
similarly reports 7 "differs," all seven being exactly the files this session touched plus one
pre-existing, previously-uncaught drift (`40K_Data_Pipeline_Process_v0_6.md` — area is ahead of repo by
a documented B56a step the repo copy lacks; not caused this session, surfaced for the first time only
because M0 brought `repo_check.py` back into the loop after its long `--no-repo` absence). Sources-absent
behaviour independently verified by stashing all GW files and re-running: the three repro gates
print loud, counted `SKIP` lines; `--tier a` correctly passes without touching any missing file (after
the filename-constant fix above); restoring the files returns everything to the pre-stash state.

**Decision needed, carried to next session — RESOLVED same-day, count confirmed as 70.** A first
screenshot pass appeared to show three files absent — `MFM_Tau_Empire_v1_0.txt`,
`MFM_Titan_Legions_v1_0.txt`, `MFM_Thousand_Sons_v1_0.txt` — and `source_manifest.json` was
rebuilt to 67 on that basis. Ryan re-checked and found the screenshot pass had skipped a row; all
three are genuinely present. The mount's original 70-file count was correct throughout.
`source_manifest.json` restored to 70 entries, local workspace restored to match, full baseline
re-run clean afterward (still 21/23, same carried-forward B68 state).

**Not started, not blocking:** M0's scope is complete. M1 (Ryan, no session) is next once tonight's
push lands and S150 confirms `--fetch` truly comes back green against the live repo.
