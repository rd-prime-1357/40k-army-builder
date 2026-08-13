# NEXT SESSION PROMPT — Session 236

## Recommended pick: the B99 engine turn. It is fully specced and needs no further scoping.

S235 was scoping-only: B99 was censused from source and re-scoped, and three new tickets were
opened (B119, B120, B121). Read `B99_SCOPE.md` first — it is the authoritative spec — then
`SESSION_HANDOFF_235.md` if anything needs re-checking. Verify the S235 file hashes at open.

## Ryan action required

- **Push S235's changed files** to the public repo. `repo_check` is red at S235 close for
  `B99_SCOPE.md`, `40K_Decision_Log.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`,
  `pipeline_manifest.py`, `pipeline_manifest.json` and `SESSION_HANDOFF_235.md` — expected for
  unpushed work, not a regression. Reconcile at open before starting.

## The B99 engine turn

Engine-only. `B99_SCOPE.md` §7 has the plan; §4 has the three traps, and getting any of them wrong
ships a visibly wrong number, so re-read them rather than working from this summary. In short: a
curated `ENHANCEMENT_WEAPON_EFFECTS` table on the B113 key shape covering the 72 Set A + Set A2
records, a delta applier (AP sign inverted; variable `A`/`D` compose as strings), the D105/D112
three-way carrier rule for the 10 multi-model-group bearers, both render sites
(`buildWeaponTable` and `loWeaponTable` — separate code, must agree), and a new `b99_check.js`.

The tooling turn that follows it adds the `rules_assertions.py` census assertion (§5) — that is
what stops the curated table rotting when a new faction lands, so do not skip it or fold it in.

**Four display decisions are open for Ryan** (`B99_SCOPE.md` §6), all reversible and all with a
stated recommendation. Proceed on the recommendations unless he says otherwise — none blocks. If
he sends New Recruit screenshots first, they settle the display idiom.

## Open, at your discretion

22 open: B116 (decision-blocked, see below), B99, B119, B120, B121, B97, B103, E28, B93, B90, B94,
B85, B86, B69, B70, B75, P2, P4, E23, B67b, E12, B17.

B121 is an XS tooling item (six scope docs missing from GUARDED) that groups cleanly with the B99
census-assertion tooling turn — verify each of the six is actually in the repo before appending,
since a GUARDED entry for an absent file turns the gate permanently red. B119 is a small engine
follow-on to B99 and should come after it so it can reuse the same curated table. B120 needs its
own scoping turn.

## Standing reminders

- Keep running a data-turn baseline periodically even on non-data sessions — S233's finding is
  exactly the failure mode this guards against.
- `40K_Decision_Log.md` has now been absent from the project-area mount for three sessions running
  and is recovered from the repo each time. Worth re-uploading; the mount cannot be trusted for
  presence/absence per standing constraint, so ask for a file-list screenshot rather than assuming.
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- Turn typing stays strict.

## Decisions waiting on Ryan

- **B99 display decisions** — four, in `B99_SCOPE.md` §6. Non-blocking.
- **B116** — unchanged. Drukhari's Harlequins/Anhrathe cross-book allied-inclusion mechanic
  (`DRUKHARI_BUILD_SCOPE.md` §6). Does not block anything shipped.
- **Next faction after Drukhari** — the documented priority order is fully built; none is queued.
  Recommendation stands: clear the remaining engine backlog before revisiting which faction, if
  any, comes next.

## Close

Produce the four documents, register `SESSION_HANDOFF_236.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
