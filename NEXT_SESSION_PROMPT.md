# Next-session prompt — Session 184

**Assigned: B87 tooling turn — teach `mfm_points_parser.py` the MFM v1.1 page layout.**
Turn type is **tooling-only** — no engine, no data-file regeneration banked this session (parsing for
validation is fine; nothing derived from v1.1 ships until B89).

## Open at session start

Read `SESSION_HANDOFF_183.md` first, then `40K_Decision_Log.md` **D274** (the layout deltas, the
intake policy, and the arc sequencing). Do not trust session/version/decision numbers from memory —
re-derive from source. `index.html` is at **v6.14** (unchanged S183).

Run the full baseline: `./baseline.sh --fetch --data-turn` (sources must load — the v1_0 MFM files
are the regression fixture for the format sniff). Expect 29/29 green at open.

**No rename gate.** Per D275, filenames are accepted as-uploaded — dots for the GW version (`v1.1`)
and spaces where the faction name has them (`Chaos Daemons`). The parser and `source_manifest.json`
bank the actual repo filenames.

## The build (per D274 policy e)

One parser, per-file format sniff, per-layout readers. The v1.1 layout is self-identifying (leading
`UNITS` header, "▼" markers). Readers share everything downstream — output CSVs, name overrides,
validation report. v1.1 reader must handle: cost lines without bullet prefix ("1 model40 pts",
"3 models▼ (-10) 80 pts"); "▼" trailing unit names and model counts; stripping change annotations
("(-10)", "▲ (+10)") and flag lines ("UPDATED", "FORCE DISPOSITION(S) CHANGED") — final value only;
the blank line between LEADER/SUPPORT and the attach list; WARGEAR OPTIONS blocks ("per Twin
lascannon5 pts"); the DETACHMENTS section (DP, force disposition, enhancement name/cost pairs) parsed
into a structured form for B88. Watch the known comma-thousands gap — if any v1.1 file prices
`1,000+ pts`, fix it in the same reader, it is the same line grammar.

## Acceptance (facts as executable checks)

- All 15 banked v1.1 files parse with full cost coverage (no `no_costs` entries beyond genuinely
  uncosted MFM lines).
- SM v1.1 resolves ≥ the 179 v1_0 unit entries or every difference is explained by a real MFM roster
  change, not a detection miss — Rhino, Razorback, Drop Pod were the S183 canaries.
- v1_0 files still parse to identical output through the sniff path (byte-level on the emitted CSVs).
- Change annotations never reach an output value.
- Baseline 29/29 at close.

## After this

- **B88** — reconciliation reports across all built factions (next session).
- **B89** — per-faction adoption arc, standard priority order.
- **E23 build turn** — resumes after adoption; re-verify D273's per-army pool counts at open.

## Close protocol

Produce the four documents: `SESSION_HANDOFF_184.md`, overwrite `NEXT_SESSION_PROMPT.md`, append the
decision log + `DECISION_INDEX.md`, update `OPEN_ITEMS_BACKLOG.md`. Every changed and net-new file
carries a SHA-256 (first 12) in the handoff Files section. Append `SESSION_HANDOFF_184.md` to
`GUARDED` in `pipeline_manifest.py` this same session, then `python3 pipeline_manifest.py --write`
then `--freshness-check` at the very end, after all text is finalized. Repo is public and flat — no
GW-derived material committed; state the exclusions when listing files for the repo.
