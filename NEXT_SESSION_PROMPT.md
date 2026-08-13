# NEXT SESSION PROMPT — Session 232

## No item is blocked on a Ryan decision. GK §6/§7 is the natural next pick.

B114 (Shadow Legion Thralls) shipped and closed at S231 (D325). Read
`SESSION_HANDOFF_231.md` first if any of this session's reasoning needs re-checking —
the short version is below.

Shadow Legion's Chaos Daemons detachment now correctly allies in 21 Chaos Space Marines
units (14 named + 7 built "Damned"), tagged `allied_group: "Shadow Legion Thralls"` in the
Chaos Daemons block of `units.json`, priced off their Chaos Space Marines native points
(no separate GW points table exists for this detachment — checked directly in both
factions' MFM files). `detachment_effects.json`'s unlock is `enforced: true`. Chaos Daemons
stays fully source-reproducible: the 21 units were appended into the project-root Gen-1
CSVs (`Unit_Stats.csv` and friends), not hand-patched into `units.json` — `units_repro_check`
and `repro_check` are both green. A real, previously-undocumented finding from this build:
the CD-faction Wahapedia datasheet rows this ticket sourced from are mistag duplicates
(D131/D132's pattern), not real GW book-variant reprints like Rotigus — worth remembering if
a similar-looking allied-unlock ticket comes up again, since the "check the ability text
before trusting a `Datasheets.csv` faction tag" step is what caught it.

## Open, at your discretion

- **GK §6/§7** — carried unchanged for several sessions; still not investigated. Read what
  exists of it first; if it turns out to need re-scoping from scratch, that's a normal
  scoping turn, not a problem.
- Remaining engine/data backlog (B108's Ryan action, B99/B98/B97/B103/E28/B93/B90/B94/B85/
  B86/B69/B70/B75/P2/P4/E23/B67b/E12/B17) — 21 open, no new priority signal this session.
  Pick in whatever order groups cleanly into a single turn type; none of them depend on
  B114 or on each other in a way that forces an order.

## Standing reminders

- Re-derive from source, don't trust prior-session prose — including this prompt's claims
  about what shipped. Verify S231's Files table hashes against `pipeline_manifest.json`
  before starting.
- Turn typing stays strict. If GK §6/§7 turns out to need both a scoping pass and a build,
  that's two sessions, not one.
- The B114 build touched `rules_assertions.py` fairly widely (five separate assertion
  areas). If a future baseline shows an unexpected assertion failure anywhere near allied
  groups, Character-keyword gaps, or the seeded-add count, check this session's changes
  first before assuming a new bug.

## Decisions waiting on Ryan

- **B116** — unchanged. Drukhari's Harlequins/Anhrathe cross-book allied-inclusion mechanic
  (see `DRUKHARI_BUILD_SCOPE.md` §6). Build as its own follow-on ticket once Ryan decides.
  Does not block anything shipped.
- **Next faction after Drukhari** — the documented priority order is fully built; no faction
  is queued. Recommendation stands: clear the remaining engine/scoping backlog (GK §6/§7
  and the rest) before revisiting which faction, if any, comes next.

## Close

Produce the four documents, register `SESSION_HANDOFF_232.md` in `pipeline_manifest.py`'s
GUARDED list **before** running `--write`, and run `pipeline_manifest.py --freshness-check`
as the **last** command.
