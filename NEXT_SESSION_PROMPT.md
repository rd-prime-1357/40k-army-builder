# NEXT SESSION PROMPT — Session 233

## No item is blocked on a Ryan decision. GK §6/§7 is still the natural next pick.

S232 was forced into a tooling-only turn by two session-open gate failures — no assigned build
happened. Read `SESSION_HANDOFF_232.md` first if any of this session's reasoning needs
re-checking — the short version is below.

Fixed a real bug in `rules_assertions.py`'s tier classifier (`classify_tier` couldn't see inside
`Sources` class methods, so one assertion, `E4b-6`, misclassified as tier A and crashed under
`--tier a` instead of skipping). Also fixed a doc-integrity gap: D324 and D325 had only ever been
written into `DECISION_INDEX.md`, never into the authoritative `40K_Decision_Log.md` — moved,
content unchanged. Neither of these touched `units.json`, `detachments.json`, `index.html`, or any
other shipped output — pure tooling/process, zero product change.

## Ryan action required (new)

- **B117** — six GW-derived Gen-1 Chaos Daemons CSVs are committed to the public repo despite
  matching its own `.gitignore` rule. Same shape as the still-outstanding B108. See the backlog
  entry for the exact file list. `repo_check` will keep flagging CRITICAL every session open until
  this lands.

## Open, at your discretion

- **GK §6/§7** — carried unchanged for several sessions; still not investigated. Read what exists
  of it first; if it turns out to need re-scoping from scratch, that's a normal scoping turn.
- Remaining engine/data backlog (B108's Ryan action, B117's Ryan action, B99/B98/B97/B103/E28/B93/
  B90/B94/B85/B86/B69/B70/B75/P2/P4/E23/B67b/E12/B17) — 22 open, no new priority signal this
  session. Pick in whatever order groups cleanly into a single turn type.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's claims about
  what shipped. Verify S232's Files table hashes against `pipeline_manifest.json` before starting.
- Turn typing stays strict. If GK §6/§7 turns out to need both a scoping pass and a build, that's
  two sessions, not one.
- Check both `40K_Decision_Log.md` and `DECISION_INDEX.md`'s own tails directly when opening
  either — S230/S231 wrote two entries into the wrong one; the fix is in, but it's worth spot
  re-checking rather than assuming a filing error can't recur.

## Decisions waiting on Ryan

- **B116** — unchanged. Drukhari's Harlequins/Anhrathe cross-book allied-inclusion mechanic (see
  `DRUKHARI_BUILD_SCOPE.md` §6). Build as its own follow-on ticket once Ryan decides. Does not
  block anything shipped.
- **Next faction after Drukhari** — the documented priority order is fully built; no faction is
  queued. Recommendation stands: clear the remaining engine/scoping backlog (GK §6/§7 and the
  rest) before revisiting which faction, if any, comes next.

## Close

Produce the four documents, register `SESSION_HANDOFF_233.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the
**last** command.
