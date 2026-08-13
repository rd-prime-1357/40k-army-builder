# NEXT SESSION PROMPT — Session 235

## No engine/design item is blocked on a Ryan decision. Backlog is clear of Ryan-action items.

S234 was a data-only turn: session-open reconciliation found B108, B117, and B118 all already
resolved (Ryan pushed both repos ahead of the session — verified directly, not assumed), then B98
(Daemon Prince of Tzeentch "heliforged" typo) was built and closed. Read `SESSION_HANDOFF_234.md`
first if any of this needs re-checking.

## Ryan action required

None outstanding.

## Open, at your discretion

19 open total, no Ryan-action items among them: B99, B97, B103, E28, B93, B90, B94, B85, B86, B69,
B70, B75, P2, P4, E23, B67b, E12, B17, plus B116 (decision-blocked, see below). Pick in whatever
order groups cleanly into a single turn type. B99 (stat-bonus-to-equipped-weapon enhancements not
wired into the engine at all — see its Open Items entry) is the next item flagged as needing a
scoping turn before it can be built; worth picking up early since it's a census-then-decide shape
similar to past scoping turns.

## Standing reminders

- Keep running a data-turn baseline periodically even on non-data sessions — S233's finding (the
  private-repo gap sitting undetected for two sessions) is exactly the failure mode this guards
  against.
- `40K_Decision_Log.md` is not present in the project area mount as of S234 (fetched fresh from the
  repo this session, same as S233) — worth re-uploading if you haven't already; the mount can't be
  trusted for presence/absence per standing constraint.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push access
  — verify with a real write attempt.
- Turn typing stays strict.

## Decisions waiting on Ryan

- **B116** — unchanged. Drukhari's Harlequins/Anhrathe cross-book allied-inclusion mechanic (see
  `DRUKHARI_BUILD_SCOPE.md` §6). Build as its own follow-on ticket once Ryan decides. Does not
  block anything shipped.
- **Next faction after Drukhari** — the documented priority order is fully built; no faction is
  queued. Recommendation stands: clear the remaining engine/scoping backlog before revisiting which
  faction, if any, comes next.

## Close

Produce the four documents, register `SESSION_HANDOFF_235.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
