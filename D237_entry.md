## D237 — CSM turn C: detachment build shipped, closing the CSM build arc

**Session 154, data-only.**

`detachment_parser.py` gained Chaos Space Marines' three config lines: `ARMY_TO_MFM` ("Chaos Space
Marines" → `MFM_Chaos_Space_Marines_v1_0.txt`), `MFM_SOURCE_NAME` (that file → "Chaos Space Marines"),
and `ARMY_TO_WAHA_FACTION` ("Chaos Space Marines" → "CSM"). `detachments_repro_check.py` gained the
CSM MFM file in its required-inputs list.

Regenerated `detachments.json`: +17 CSM detachments (143 → 160 records, 14 → 15 armies, 275 → 292
army-detachment slots). Diff-traced key-by-key against the previously-committed file: every added key
belongs to Chaos Space Marines, zero existing records changed, zero removed, and no other army's
detachment-slot list moved. Matches CSM_BUILD_SCOPE.md §3/§6 and D192's ruling exactly — MFM is the
source of record for the roster; the two MFM-only detachments (Devotees of Destruction, Murdertalon
Raiders) came through with no rule prose, enhancement names/points only; the three Wahapedia-only
detachments were dropped as stale. The other 15 CSM detachments sourced their prose from Wahapedia's
tier-2 text, since CSM has no faction-pack tier-1 source. `detachments_repro_check.py` reproduces the
regenerated file byte-for-byte.

Per the standing sequence, M2 (Ryan, evict the 71 GW sources) is now unblocked — CSM turn C's clean
diff-trace was the last piece of CSM build work gating it.

**Two real gaps surfaced, both filed for the tooling turn rather than fixed here (turn-typing: this
was a data-only turn, config lines plus the regeneration they drive, no assertion or effects-file
edits):**

1. **E4b-3's literal is now stale.** The same-army cross-detachment enhancement-name collision census
   moved 29 → 30 reachable collisions (5 → 6 distinct names) once CSM's own enhancements entered
   `detachments.json`. The rule the count supports (name-keyed duplicate detection, army-wide) is
   unaffected — only the pinned literal needs updating, in the CSM tooling turn alongside the
   detachment-count and roster-count assertions already scoped there.

2. **New ticket B74 — Chaos Cult grants BATTLELINE with no `detachment_effects.json` row.** CSM's Chaos
   Cult detachment's rule text ("TRAITOR GUARDSMEN SQUAD units from your army gain the BATTLELINE
   keyword") is a real construction effect of the same shape E21a already polices for other armies, and
   it has no row yet. `rules_assertions.py`'s E21a-5 (coverage) fails correctly the moment
   `detachments.json` carries CSM's Chaos Cult text — this is the assertion doing its job, not a false
   positive. Needs its own small data turn against `detachment_effects.json`, once the tooling turn's
   CSM assertions are in and the file's shape is fresh in view; not attempted this session to keep the
   turn data-only and single-purpose.

**Housekeeping / anomaly noted, not acted on:** `40K_Decision_Log_v3_0.md` is absent from the mounted
project area this session, and `D231_entry.md`–`D234_entry.md` are still present there — the reverse of
what S153's handoff recorded (log workspace-resident, those four folded in and deleted). Read as the
project-area mount going stale after S153's uploads rather than a real regression, per the standing
constraint that the mount is a point-in-time snapshot and not authoritative for presence/absence. Not
treated as grounds to reconstruct the log from scratch — this entry is banked standalone instead,
reviving the pre-S152 `D2NN_entry.md` fallback pattern for exactly this situation, pending Ryan
confirming the log's real state with a fresh upload. If the log is genuinely intact elsewhere (his
local copy or the repo), fold D237 in there directly, same treatment as D231–D234 got at S153.

Full baseline outside `--fetch`/repo gates: `detachments_repro_check.py` green. `rules_assertions.py`'s
E4b-3 and E21a-5 fail as described above — both expected, both scoped to the tooling turn, neither a
sign of a bad regeneration. `index.html` untouched — CSM's detachment picker uses only existing
mechanisms, matching CSM_BUILD_SCOPE.md §6's "no change expected."

**Turn type: data-only.** Config-list additions plus the parser/check-script output they regenerate and
prove. No engine logic change to either file beyond the config lines; no assertion, effects-file, or
`index.html` edit.
