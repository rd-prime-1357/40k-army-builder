- **D238** — CSM tooling turn shipped, per `CSM_BUILD_SCOPE.md` §8 step 4: three new assertions
  (`CSM-1` roster count 54/58, recorded honestly rather than rounded up; `CSM-2` detachment count 17;
  `CSM-3` the two MFM-only detachments' `text_source: none` pinned as documented shape, not a gap).
  `E4b-3`'s pinned collision census re-derived fresh from `detachments.json` rather than assumed from
  D237's handoff prose — confirmed 30 pairs / 6 names / 1 differing-price, the sixth colliding name is
  CSM-internal (Warp-Fuelled Thrusters), the differing-price collision is unrelated to CSM (Dark
  Angels/Deathwing Assault, unchanged). Literal and docstring updated in both the assertion statement
  and the function body. `pipeline_manifest.py --write` reissued (105 guarded files). Full
  `baseline.sh --no-repo` pass: 22/23 gates green, the sole failure is `rules_assertions.py`'s
  `E21a-5` (B74 — Chaos Cult's BATTLELINE grant has no `detachment_effects.json` row), correctly
  failing by design and explicitly out of scope this session per the S155 prompt. B74 remains open,
  filed for its own small data turn next. `40K_Decision_Log_v3_0.md` is still absent from the mounted
  project area this session (third session running); this entry banked standalone again pending
  Ryan's confirmation of the log file's real status — if it's genuinely missing, next session should
  rebuild the workspace-resident copy from the accumulated standalone entries (D231–D234, D237, D238)
  rather than assume it. Tooling-only: no engine logic changed, `index.html` untouched, no data file
  regenerated (S155)
