# Next-session prompt — Session 171

**Assigned: development-manager's call, but two items are blocked on Ryan.** B70 and B73 were audited to a
real root cause (S170/D260) — not fixed. Both need a decision from Ryan before any build. 12 open items,
unchanged from S169/S170.

## Open at session start

Read `SESSION_HANDOFF_170.md` first, then D260 in `40K_Decision_Log_v3_0.md`. Do not trust any
session/version/decision number from memory; the handoff chain is the only authority. `index.html` is
still at **v6.12** — nothing shipped S170.

Run the full baseline before any new work: `./baseline.sh --fetch`. It closed at 29/29 gates (sources
loaded, all tiered gates ran) at the end of S170. Nothing was changed in code or data this session — only
`40K_Decision_Log_v3_0.md`, `DECISION_INDEX.md`, `OPEN_ITEMS_BACKLOG.md`, plus the two rolling files
(`SESSION_HANDOFF_170.md` new, `NEXT_SESSION_PROMPT.md` overwritten). `repo_check` will show differs for
exactly those until pushed — expected, not a new failure.

## Decisions waiting on Ryan (do not build past these without an answer)

**B70 — Wardens of Ultramar.** Confirmed: it has no Leader ability in any source (zero rows in
`Datasheets_leader.csv`, no Core-typed "Leader" ability). Its real ability, `HEROES OF ULTRAMAR`, is a
"joins another unit, increases its Starting Strength" mechanic — not Leader-attach — and nothing in the
engine implements it. The engine correctly refuses to let it attach as a Leader; B70 as filed describes
intended behavior, not a bug. **Ask Ryan:** close as not-a-bug, or build the join mechanic as new scope
(likely M/L — a distinct attach-type from Leader, "counts as part of that unit" engine support, a data turn
to capture which units it can join)? Do not start a build on B70 until this is answered.

**B73 — Ultramarine (and other) Leader lists include out-of-chapter units.** Confirmed systemic across all
13 currently-built LEADER-typed Epic Heroes, not a Uriel-only issue — every one carries the same handful of
extra cross-chapter entries (Crusader Squad, Deathwatch Veterans, Decimus Kill Team, Fortis Kill Team,
Inner Circle Companions, Sword Brethren Squad, plus Terminator-chapter units where relevant) that the
current MFM's own `LEADER` list for that same character does not have. Root cause: `leader_eligible_units`
is populated primarily from Wahapedia's `Datasheets_leader.csv` (10th-edition-sourced), and
`mfm_points_parser.py`'s MFM backfill only fills a *blank* cell — it never checks a populated cell against
the MFM's own current list, even when they disagree. **Ask Ryan:** should the MFM's `LEADER` list be
authoritative wherever both exist (recommended — consistent with the project's existing "MFM-first,
11th-Ed-authoritative" precedent for points/DP), falling back to Wahapedia only where the MFM has no
`LEADER` block for that unit? Or does Ryan have reason to trust Wahapedia's broader per-character list
instead? This is roster-wide (every SM-family Leader, not just Ultramarines) and reverses a design choice
`wahapedia_transform.py`'s comments currently defend on purpose — a real precedent-setting call, not a
quick parser tweak. Do not start a build on B73 until this is answered.

Once B73 is answered, fixing it (a data-turn re-derivation of `leader_eligible_units` from the MFM, parser
change, asserted) will likely also resolve the SUPPORT-vs-LEADER bleed and the one-line MFM-block over-read
that caused Wardens' bogus "VANGUARD VETERAN SQUAD WHITE SCARS" entry, as a side effect of the same fix —
unless B70 goes the join-mechanic route, in which case Wardens' list should go back to null/empty instead.

## Candidates that don't need Ryan first

- **B77** — emit the `SCINTILLATING LEGIONS` keyword properly (parser fix, regenerate output; retain
  `allied_group` — it feeds E22b's gate). Small, self-contained. Good pick if B70/B73 answers aren't in yet.
- **B76** — rolling documents drop version numbers from filenames. Small, low-risk filler; touches many
  cross-references and is a repo delete-plus-add. Clarity only, no safety gain.
- **B75** — Rules Updates column resolution. Still blocked on Ryan's flag counts across the pack set — do
  not start without them.
- **E23** — HEADHUNTER TASK FORCE Tank Ace Character grant. M-sized, needs a scoping turn first.
- **P4** — Project-area capacity → long-term architecture, M2 next. Watch, not blocking; Ryan reported 79%
  at S166/167, unconfirmed since — worth asking again given it's been several sessions.

## Standing reminders

- Turn typing is absolute: engine, data and tooling never mix in one session. S170 was audit-only (no code
  changed at all) — the eventual B73 fix, once scoped, is a data/parser turn; keep it apart from any
  engine work.
- Fix parsers, never hand-edit `units.json` / `unit_loadouts.json`.
- Facts not expressed as executable checks do not hold — legality-critical claims go in
  `rules_assertions.py`; harness-testable engine logic goes in a `*_check.js` gate.
- GW-derived material never enters the public repo.
- No further extraction of code out of `index.html` without a positive reason.
- Session close ends with `pipeline_manifest.py --write` then `pipeline_manifest.py
  --freshness-check`, in that order, as the literal last two commands (B81/D257).
- Diagnoses from prior sessions are re-derived from source before building on them. S170 is itself a
  reminder of why: reading `wahapedia_transform.py` alone gave a wrong first answer on Wardens; only
  rerunning the real pipeline against real source files surfaced the actual mechanism.
