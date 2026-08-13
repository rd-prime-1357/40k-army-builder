# NEXT SESSION PROMPT — Session 234

## No engine/design item is blocked on a Ryan decision. B98 is scoped and ready to build.

S233 was a data-only source-integrity turn: confirmed GK §6/§7 is already fully shipped (the prior
prompt's recommendation was stale — don't re-check it), found and fixed a real gap where B114's
21-unit Shadow Legion Thralls append never reached the private source repo, reconstructed and
verified the six affected CSVs byte-for-byte, but could not push them — see the Ryan action below.
Read `SESSION_HANDOFF_233.md` first if any of this needs re-checking.

## Ryan action required (new)

- **B118** — push the six CSVs delivered at S233 (`Unit_Stats.csv`, `Unit_Points.csv`,
  `Unit_Weapons.csv`, `Unit_Wargear_Options.csv`, `Unit_Other_Options.csv`,
  `Unit_Ability_Details.csv`) to `rd-prime-1357-data-sources`, replacing the current files of the
  same names. **Until this lands, any `baseline.sh --data-turn` run will fail `source-fetch` with
  a hash mismatch — expected and correct, not a regression.** If a data turn is genuinely needed
  before B118 lands, the six corrected files are also sitting in the project area from S233 and can
  be used directly rather than fetched, with the source-fetch step skipped/noted.

## Open, at your discretion

- **B98** — Daemon Prince of Tzeentch (both size variants): fully diagnosed, not yet built. Root
  cause is a literal typo (`heliforged` for `hellforged`) in `Thousand_Sons_web.txt`'s source text,
  affecting exactly two records (`000001036`, `000004120`). Fix is a small, scoped correction inside
  `equipped_parser.py`'s `resolve()` (a `SOURCE_TYPO_CORRECTIONS` lookup keyed to this exact known-bad
  string, not a general auto-correct) — mirrors the project's established "targeted fix, not broad
  generalization" precedent (B115). Requires a full `unit_loadouts.json` regen + diff-guard once
  built; data-only turn.
- Remaining backlog (B117's Ryan action, B99, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70,
  B75, P2, P4, E23, B67b, E12, B17) — 23 open total, no new priority signal this session. Pick in
  whatever order groups cleanly into a single turn type.

## Standing reminders

- `40K_Decision_Log.md` was absent from the project area mount at S233 open — the file itself is
  fine (verified via a fresh public-repo clone, matches every claim in prior handoffs), but it's
  worth re-uploading to the project area if you haven't already, since the mount can't be trusted
  for presence/absence per standing constraint.
- This session's finding is a reminder to actually run a data-turn baseline periodically, not just
  when a data ticket is on deck — the private-repo gap sat undetected for two full sessions because
  nothing forced GW sources to load. Worth doing at least every few sessions even on tooling/engine
  turns, time permitting.
- Do not trust the GitHub API's repo `permissions` field for either the public or private repo as
  evidence of push access — S233 found it claims full admin/push access for a token that a real
  `git push` rejected as read-only. Test with an actual write attempt before relying on it.
- Turn typing stays strict.

## Decisions waiting on Ryan

- **B116** — unchanged. Drukhari's Harlequins/Anhrathe cross-book allied-inclusion mechanic (see
  `DRUKHARI_BUILD_SCOPE.md` §6). Build as its own follow-on ticket once Ryan decides. Does not
  block anything shipped.
- **Next faction after Drukhari** — the documented priority order is fully built; no faction is
  queued. Recommendation stands: clear the remaining engine/scoping backlog before revisiting which
  faction, if any, comes next.

## Close

Produce the four documents, register `SESSION_HANDOFF_234.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
