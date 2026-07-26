# Next-session prompt — Session 149

Session 148 scoped P4 into a target architecture (D231, no build). This session is **M0 — build the
new session-open. Tooling-only. Nothing is evicted from the area.** Read `P4_ARCHITECTURE_SCOPE.md`
(the full design), `SESSION_HANDOFF_148.md`, and D231 before starting.

## Project-area state — READ THIS FIRST

The area is at/near 100%. `40K_Decision_Log_v3_0.md` is **not in the area** — it is repo-only
(removed S147 for capacity), current through **D231** in the repo (`rd-prime-1357/40k-army-builder`)
and Ryan's backup. `DECISION_INDEX.md` stays in the area as the lookup table; fetch full entries from
the repo when needed (D217 pattern). Do not read the mount's absence of the log as loss.

A second repo now exists: **`rd-prime-1357/data-sources`** — private, created S148, currently empty.
It is the future home of the 71 GW source files (populated at M2, not this session).

## Baseline at open

Run `baseline.sh --no-repo` (the fetch-open doesn't exist yet — that's what M0 builds). Expect the
same 21/23 as S148: the two failures name the seven B68 unit_ids (`repro_check` + its embedded P1).
That is the diagnosed, carried-forward B68 state — not a regression. Verify S148's delivered-file
hashes against the handoff Files section. Note: `NEXT_SESSION_PROMPT.md` (this file) is legitimately
edited after the handoff, so a hash mismatch on it is expected, not an alarm — M0 formalises dropping
it from the hash list.

## M0 — what to build (tooling-only)

The goal is a new session-open path that runs alongside the old one, both green in the same session,
with nothing moved out of the area yet. Deliverables:

1. **Extend `pipeline_manifest.py`** from its current pipeline-output coverage to every
   repo-resident file a session consumes, so the fetched public-repo tree can be verified whole
   against the area-resident manifest (the manifest is the pin — no commit SHAs).
2. **Add the fetch-unpack-verify-overlay stage to `baseline.sh`:** fetch the public repo as one
   tarball (`codeload.github.com/rd-prime-1357/40k-army-builder/tar.gz/main` — proven S148, 1.07 MB,
   102 files), unpack into the workspace, verify against the extended manifest, overlay the
   dual-resident working set (area copy wins; authority rule per P4 section 3). Add the
   **token-authed private-source fetch** (read `SOURCE_REPO_TOKEN.txt`, fetch `data-sources` with the
   token in the auth header, verify against `source_manifest.json`) with the **zip fallback**
   (`gw_sources.zip`). On data turns with no sources present, tier-B gates skip loudly and the turn
   refuses to start.
3. **Tier-tag the gates.** `rules_assertions.py` gains a `--tier a` mode (source-reading assertions
   and the embedded repro rebuild tagged out; everything against built data + `index.html` still
   runs). The three repro rebuilds (`repro_check.py`, `units_repro_check.py`,
   `detachments_repro_check.py`) are tier B. `baseline.sh` prints loud, counted skips for absent
   tier-B gates.
4. **Create `source_manifest.json`** — filename + SHA-256 for all 71 GW source files (build it from
   the area copies, which are still present this session). Goes in the *public* repo (hashes only, no
   GW text). **NET NEW.**
5. **Wire `repo_check.py` back in** as a standing tier-A gate (fetch it from the repo), and **add its
   `SOURCE_REPO_TOKEN.txt` fail-loud rule** — the session fails if the token filename (or a token
   pattern) ever appears in a public-repo-bound file list. Add the `.gitignore` line too.
6. **Codify close-protocol changes:** the handoff Files section gains a `pipeline_manifest.json` hash
   line and **drops `NEXT_SESSION_PROMPT.md`** from the hash list.

**Exit test (must pass before banking):** in this same session, with sources still in the area, the
*old* open path (`--no-repo`) and the *new* fetch-open path both come back green — tier B green too.
If they diverge, stop and hand off the divergence; do not route around it. Rollback is trivial —
nothing was moved.

**Do not** start M1 (eviction) this session. M0 is build-and-prove only; M1 is Ryan's ~10-minute
eviction after M0 banks, verified by before/after file-list screenshots.

## Decisions batched for Ryan (M0 proceeds on these unless he objects)

- Bulk-deletion verification amendment for M1/M2: full file-list screenshots before/after each
  eviction batch, replacing the per-file card (migration steps only).
- Dropping `NEXT_SESSION_PROMPT.md` from the handoff hash list (item 6 above).

## Turn type

**Tooling-only.** No engine, data, or parser changes. B68 (the parser fix) and the CSM data turns are
downstream in the migration sequence, not this session.
