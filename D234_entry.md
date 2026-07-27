- **D234** — M1 confirmed already run (27 repo-resident guarded files absent from the area, matching
  the S151 prompt's own anticipation). Found and fixed a real M0 design gap along the way: the
  fetch-open's verify step checked the *entire* fetched tree unconditionally against
  `pipeline_manifest.json`, so any single mismatched file — including ordinary area-ahead-of-repo drift
  on a file that wasn't even part of the overlay — blocked recovering every evicted file, contradicting
  the stated "area copy wins" authority rule. `pipeline_manifest.py` gained `check_overlay()` /
  `--overlay-check`, scoping verification to only the guarded files absent locally; `baseline.sh`'s
  fetch-verify wired to it. Also closed a manifest-housekeeping gap: `SESSION_HANDOFF_149.md` and
  `.150.md` were never appended to `GUARDED` (S149 missed its own append-at-close step) — added, along
  with `.151.md`. `pipeline_manifest.json` regenerated to bless current state. Tooling-only (S151).
