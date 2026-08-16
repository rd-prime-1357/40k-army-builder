# NEXT SESSION PROMPT — Session 249

## Recommended pick: B126, Marks of Chaos. Data + engine turn — needs a full `--fetch --data-turn`
baseline (touches `detachment_effects.json`-adjacent territory and a new per-unit selection).

B128 (S248) closed. Its own sequencing note said to read B128's shipped shape before scoping B126,
since both are "a unit's keywords/eligibility depend on context" problems (the third being B132's
per-chapter restoration) — start there rather than re-deriving a mechanism from zero.

**B128's shipped shape, in case it's useful:** a per-entry field (`entry.tankAce`, boolean),
listId-keyed rather than detachment- or unit-name-keyed, persisted with a schema bump + migration,
gated at the pick (D0: cap enforced at the checkbox, not after). B126 is a different shape though —
Marks of Chaos is a **required, exclusive choice per eligible unit** (assign exactly one of
KHORNE/TZEENTCH/NURGLE/SLAANESH/CHAOS UNDIVIDED to every non-Epic-Hero HERETIC ASTARTES unit that
doesn't already carry one), not an optional capped pick — closer in shape to the existing God
selector (`entry.god`) than to `entry.tankAce`. Worth confirming which precedent actually fits
before building; don't assume B128's shape transfers unmodified.

B126 also carries two hard legality rules beyond the four enhancement bearer restrictions already
known: a CHARACTER can only attach to a unit sharing its mark, and a unit can only embark in a
TRANSPORT sharing its mark. Both need real attach/embark checks, not just a selector. There's also
a third restriction — KHORNE cannot be selected for a PSYKER unit — that's a constraint on the
selection itself, not on attach/embark.

## Also open, at your discretion — 24 tickets

B134, B127, B116, B120, B122, B124, B97, B103, E28, B93, B90, B94, B85, B86, B69, B70, B75, P2, P4,
E23, B67b, E12, B17. **Nothing is decision-blocked.**

- **B134** (new, S248) — the six non-legality-critical automatic keyword conferrals B128's original
  census found (Heavy Transport ×6, Entrenched ×6, three faction keywords, Daemon/Soul Forge ×2).
  Scoping-only: confirm whether any actually affect list-construction legality before assuming an
  engine consumer is needed at all — `detachment_effects.json`'s own `_meta.purpose` scopes the
  file to muster-time construction effects, and these may be pure in-battle flavor keywords with no
  place in this app.
- **B127** (74 records with no rule text in any held source) needs nothing from Claude until source
  exists — a Ryan-side acquisition item.
- **B120** still needs its own scoping turn before build; per S238's note, widen its census from
  Set D *weapons* to Set D effects generally so **B124** lands inside it.
- **B122** needs a scoping turn answering a source question first: does the held Chaos Daemons
  material contain the real enhancement text at all, or only shorthand summaries (distinct from
  B127's 74 records, which have none at all)?

## Standing reminders

- The last full `--fetch --data-turn` was **S248**, clean at 38/38 with 85 source files verified
  (after fixing several collateral test-fixture breaks the entry-shape/schema-version change
  caused — see S248's handoff). **B126 is data + engine — run the full `--fetch --data-turn`
  again**, don't assume S248's fetch is still fresh.
- **A schema-version bump or entry-shape change touches more than the block you're editing.**
  S248 found three places with hard-pinned assumptions about the old shape that broke silently
  until the harnesses were actually re-run: `list_store.js` drifted from the inlined copy (caught
  live by E1b-2's byte-identity gate — that gate is working as designed, not a bug), a Python
  assertion had `SCHEMA_VERSION` hard-pinned as a literal, and two JS harnesses (`e4b_check.js`,
  `e4c_check.js`) sliced named function blocks out of `index.html` without picking up a new
  cross-block dependency, throwing bare `ReferenceError`s instead of real failures. If B126 adds
  another per-entry field or another cross-block function call, re-run the FULL baseline, not just
  the gate for the block you touched, and read any bare stack-trace-shaped failure line as a
  harness needing an update, not a false alarm to explain away.
- **A Python "mirror" of an engine function is a second implementation, and it drifts.** B133
  closed one arc of this; B128 avoided opening a new one by having `rules_assertions.py`'s E23-3
  read `detachment_effects.json`'s flat facts (`enforced`, `cap`) directly rather than
  re-deriving `unitInTankAcePool`'s keyword logic in Python. If B126 needs a Python-side assertion
  reasoning about mark eligibility, prefer reading data facts over re-deriving engine logic,
  the same way.
- **Do not trust a scope document's or a handoff's population figure — re-derive it.** Standing
  rule, unchanged.
- **An assertion phrased as "X should be absent" is usually wrong.** Standing rule, unchanged
  (B132's negative-assertion lesson).
- Do not trust the GitHub API's repo `permissions` field for either repo as evidence of push
  access — verify with a real write attempt.
- **Manifest pushes need a real diff check (D337).** Verify the actual pushed file's hash against
  the handoff table at session open, and confirm `pipeline_manifest.json` itself is among what
  landed.
- The project-area file mount silently strips apostrophes from filenames on upload. Before trusting
  a project-area filename as the real repo filename, especially for anything going into GUARDED,
  check a fresh clone.
- **Read `rule_text`, not just `restrictions`.** `restrictions` is a partial extraction of
  `rule_text`, not a substitute, and is `null` on plenty of detachments that do carry rules.
- **An impossible result means widen the read, never explain the result** (D334/D336/D341).
- **Field-coverage convention is in `40K_Data_Dictionary.md`'s front matter (S241).** State every
  field on a record type and mark read/not-read, with a reason for each not-read, before censusing.

## Ryan action required

- **Push S248's changed files** to the public repo: `index.html`, `detachment_effects.json`,
  `rules_assertions.py`, `b128_check.js` (new), `baseline.sh`, `list_store.js`, `e1b_check.js`,
  `e4b_check.js`, `e4c_check.js`, `40K_Decision_Log.md`, `DECISION_INDEX.md`,
  `OPEN_ITEMS_BACKLOG.md`, `pipeline_manifest.py`, `pipeline_manifest.json`,
  `SESSION_HANDOFF_248.md`, `NEXT_SESSION_PROMPT.md`.
- **`pipeline_manifest.json` must be included.**
- **A render check is needed** — S248 was an engine turn and the Tank Ace checkbox/keyword-pill UI
  has not been looked at on screen. See S248's handoff for the specific steps to check.

## Decisions waiting on Ryan

**Resolved at S248, listed so they are not re-asked:** D345 — B128's two-part mechanism (automatic
display keyword + capped checkbox-driven Character grant), asked and answered this session.

- **Next faction after Drukhari** — unchanged since S240. Recommendation stands: clear the engine
  backlog first. B116's reclassification means **Aeldari is a production dependency** even though
  it is not in the priority order, and belongs on a release plan rather than being rediscovered
  later.
- **Grey Knights detachments** were never built despite its units being complete — still
  outstanding.

## Close

Produce the four documents, register `SESSION_HANDOFF_249.md` in `pipeline_manifest.py`'s GUARDED
list **before** running `--write`, and run `pipeline_manifest.py --freshness-check` as the **last**
command.
