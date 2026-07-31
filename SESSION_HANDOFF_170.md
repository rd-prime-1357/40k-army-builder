# Session handoff — Session 170

**Type: audit-only** (no `index.html` change, no parser change, no data change). Decision recorded:
**D260.** B70 and B73 investigated to a real root cause; neither shipped — both need a scope/legality
decision from Ryan first.

---

## 1. Baseline at session open

`./baseline.sh --fetch --data-turn` ran clean: 29/29 gates pass, sources loaded (data-turn requested
since the audit needed the real MFM/Wahapedia source files, not just `units.json`). No reconciliation
needed at open.

## 2. Why this was an audit, not a build

The S169 handoff and next-session prompt both flagged B70+B73 as "start with the audit, not a build."
That call was correct — the surface symptom (Wardens can't attach; Uriel's Leader list looks too broad)
turned out to be one shared root cause, only findable by actually rerunning the pipeline, not by reading
the parser code. My first pass at reading `wahapedia_transform.py` gave a wrong diagnosis (I thought the
parser no longer produces Wardens' populated `leader_eligible_units` at all); rerunning
`wahapedia_transform.py` and `mfm_points_parser.py` in isolation against real source files showed the
actual mechanism, and testing that against the whole roster rather than a single character is what
turned "Uriel looks wrong" into "13 characters show the identical pattern."

## 3. Root cause (D260)

`wahapedia_transform.py` leaves `Leader Eligible Units` blank when a datasheet has no Core-typed ability
literally named "Leader" — correct for Wardens of Ultramar, which has zero rows in `Datasheets_leader.csv`.
`mfm_points_parser.py` then backfills any blank cell from the MFM text's own per-unit list, but the MFM
carries two different headers — `LEADER` and `SUPPORT` — and the backfill treats them identically. Wardens'
MFM block is headed `SUPPORT`. The backfill also over-reads one line past the block boundary, so the next
faction's header ("WHITE SCARS") gets concatenated onto the last entry with no delimiter — the exact origin
of the bogus "VANGUARD VETERAN SQUAD WHITE SCARS" the S169 handoff flagged.

Separately, for characters that *do* have a real Leader ability (Uriel, Tigurius, Calgar, Titus, and nine
others), `leader_eligible_units` comes primarily from Wahapedia's `Datasheets_leader.csv` — a 10th-edition-
sourced file per its own URLs — and the MFM backfill never touches an already-populated cell, so it never
cross-checks a Wahapedia-derived list against the MFM's own current `LEADER` list for that same character,
even when they disagree. Checked all 13 built LEADER-typed Epic Heroes against their MFM `LEADER` entries:
every one carries the same handful of extra cross-chapter units (Crusader Squad, Deathwatch Veterans,
Decimus Kill Team, Fortis Kill Team, Inner Circle Companions, Sword Brethren Squad, plus Terminator-chapter
units for the characters that lead Terminators) that the MFM list doesn't have. Uniform across 13
independent characters — this is systemic, not a Uriel-specific slip.

## 4. B70 and B73 — status

- **B70** — very likely **not a bug**. Wardens has no Leader ability in any source; its actual ability
  (`HEROES OF ULTRAMAR`) is a "this unit joins another unit, increasing its Starting Strength" mechanic,
  which the engine has never had code for. Refusing to attach it as a Leader is correct as filed. The two
  parser bugs above (SUPPORT-vs-LEADER blindness, one-line over-read) are real and fixable, but fixing them
  doesn't make Wardens attachable — the actual ask is very likely a new, unbuilt game mechanic.
- **B73** — confirmed real and systemic, root cause identified, **not fixed**. Which source should govern
  Leader eligibility when Wahapedia and the MFM disagree is a rules-legality call with roster-wide blast
  radius (every Leader-typed unit across every SM-family chapter, not just Ultramarines built so far), and
  it would reverse a design choice `wahapedia_transform.py`'s own comments defend on purpose (the "generic
  Captain datasheet legitimately spans chapter bodyguards" rationale — which, on inspection, is about
  *shared* generic datasheets, not named Epic Heroes with their own datasheet id like Uriel).

Full trace and evidence are in D260 (`40K_Decision_Log_v3_0.md`). Nothing here needs re-deriving next
session — the audit is done; what remains is Ryan's call.

## 5. Decisions needed (Ryan)

1. **B70** — is the correct outcome (a) close as not-a-bug and park it, or (b) build the "join" mechanic
   (new feature, likely M/L-sized: a distinct attach-type separate from Leader, engine support for
   "counts as part of that unit," a data turn to capture which units it can join)? My read: (a) unless
   Ryan specifically wants Wardens playable as originally imagined, in which case it's a real scope item,
   not a quick fix riding on B70's ticket size.
2. **B73** — when the MFM's `LEADER` list for a character disagrees with Wahapedia's broader list, which
   should the app treat as legal? Two shapes, not mutually exclusive: (a) MFM's list wins outright wherever
   both exist (a data turn: re-derive `leader_eligible_units` from the MFM text as primary, Wahapedia only
   as fallback when the MFM has no `LEADER` block for that unit); (b) some intersection/union logic — e.g.
   trust Wahapedia's list but only for units the selected army's own roster can actually reach, so the
   cross-chapter entries are harmless dead weight rather than wrong (this doesn't fix the display list Ryan
   is seeing, only its practical reachability). My recommendation is (a) — MFM is already the project's
   established 11th-Ed-authoritative source for points and DP; extending that same precedent to Leader
   eligibility is consistent, not a new principle — but this is exactly the kind of call the project's own
   rules route to Ryan, not something to decide silently given the roster-wide reach.
3. Whichever way #2 goes, it will also fix Wardens' SUPPORT-vs-LEADER bleed and the one-line over-read as a
   side effect of the same data turn, once (1) is resolved (B70's own list would be null again, matching
   what "no Leader ability" should mean, unless the join mechanic gets built).

## 6. What's next

Same 12 open as S169: B69, B70, B73, B75, B76, B77, P2, P4, E23, B67b, E12, B17 — none closed this session,
none added. B70/B73 now carry a real diagnosis and are blocked on Ryan's two decisions above rather than on
further investigation. Next viable picks without waiting on Ryan: B77 (SCINTILLATING LEGIONS keyword,
small parser fix) or B76 (rolling-doc filename cleanup, small/low-risk). B75 stays blocked on Ryan's flag
count report. B69 stays blocked on Ryan's six-vs-one scope choice (D259).

## 7. Files

| File | SHA-256 (first 12) | Status |
|---|---|---|
| `40K_Decision_Log_v3_0.md` | (see manifest) | updated (D260) |
| `DECISION_INDEX.md` | (see manifest) | updated — D260 one-liner |
| `OPEN_ITEMS_BACKLOG.md` | (see manifest) | updated — B70/B73 rewritten with audit findings; open count unchanged at 12 |
| `NEXT_SESSION_PROMPT.md` | (see manifest) | overwritten (S171) — not guarded, by design (D231) |
| `SESSION_HANDOFF_170.md` | (self) | new (rolling) |
| `pipeline_manifest.json` | (issued last — see §8) | regenerated, reflects the files this session changed |

**Net New Files:** none. This session touched only rolling documents (decision log, decision index,
backlog, handoff, next-session prompt) — no harness, parser, or data file was created. `index.html`,
`units.json`, and every pipeline script are byte-identical to S169.

**Ryan cannot download from the project Files panel** (S159 finding). All changed files are delivered
as outputs this turn for repo push and project-area upload.

## 8. Manifest reissued last, per D251's ordering rule — checked by `--freshness-check`

`pipeline_manifest.py --write` then `pipeline_manifest.py --freshness-check` are the literal last two
commands, after this handoff's text and D260's decision-log entry were finalized.

## 9. Backlog

- **Beginning:** 12 open — B69, B70, B73, B75, B76, B77, P2, P4, E23, B67b, E12, B17
- **Resolved:** 0
- **Added:** 0
- **Ending:** 12 open — B69, B70, B73, B75, B76, B77, P2, P4, E23, B67b, E12, B17
