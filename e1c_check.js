// e1c_check.js — E1c. Loads the real detachment-picker classifier out of
// index.html, and asserts that the picker's enable/disable is canAddDetachment's
// answer and not a second implementation of it. The point of the harness (per
// D107) is that this is a claim about BEHAVIOUR, so it is executed against the
// real catalogue rather than described in prose.
//
// Also asserts the two other structural things E1c must hold:
//   - the picker's ghost classification matches "key not in the catalogue"
//   - a selected row is always toggle-off-able, however over-constrained the
//     rest of the set is (flag-don't-drop: the picker must never lock a saved
//     list into an illegal state it cannot exit)
//
// Build-time only; not part of the served app.
// Usage: node e1c_check.js index.html detachments.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path, defs, byArmy) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const limit = slice(lines, '// D115 — the unit limit depends', '// State');
  const e1b   = slice(lines, '// ── E1b: detachment selection rules', '// ── E1b block end');
  const e1c   = slice(lines, '// ── E1c: detachment picker', '// ── E1c block end');
  const src = 'let detachmentDefs = DEFS; let detachmentsByArmy = BYARMY; '
            + 'let POINTS_CAP = 2000; let selectedDetachments = []; '
            + 'let openDetachmentDetail = null; let hasGhosts = false; '
            + 'let armyList = []; '
            + 'function renderAll(){} function renderRoster(){}\n'
            + limit + '\n' + e1b + '\n' + e1c
            + '\nreturn { detachmentPickerRowState, canAddDetachment, '
            + 'detachmentSelectionState, detachmentRefusalText, detTier2Badge, '
            + 'detachmentDefs };';
  return new Function('DEFS', 'BYARMY', src)(defs, byArmy);
}

const idxPath = process.argv[2] || 'index.html';
const detPath = process.argv[3] || 'detachments.json';

const DJ = JSON.parse(fs.readFileSync(detPath, 'utf8'));
const E  = loadEngine(idxPath, DJ.detachments, DJ.armies);

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (a, b, msg) => ok(JSON.stringify(a) === JSON.stringify(b), `${msg} (got ${JSON.stringify(a)})`);

// Concrete keys used across the scenarios. Chosen because they exercise every
// canAddDetachment refusal type against real catalogue records.
const K_SM3  = 'Space Marines|ARMOURED SPEARTIP';      // 3 DP
const K_SM1  = 'Space Marines|LIBRARIUS CONCLAVE';     // 1 DP
const K_SM1b = 'Space Marines|FULGURIS TASK FORCE';    // 1 DP
const BA_G_A = 'Blood Angels|ANGELIC INHERITORS';       // GRACE, 3 DP
const BA_G_B = 'Blood Angels|LEGACY OF GRACE';          // GRACE, 1 DP
const GHOST  = 'Space Marines|NO SUCH DETACHMENT';

// ── 1. The picker's disabled classification is canAddDetachment's answer ─────
// The claim: for a non-selected row, disabled === !canAddDetachment(...).ok. If
// that ever stopped being true, a second implementation of the three rules is
// living inside the picker and the whole "single read path" story is broken.
console.log('E1c — the picker is canAddDetachment, not a second copy of it');

function scenarios() {
  return [
    { name: 'empty selection, Strike Force',
      keys: [], pts: 2000,
      probe: [K_SM3, K_SM1, K_SM1b, BA_G_A, BA_G_B, GHOST] },
    { name: 'one 1 DP pick, Strike Force',
      keys: [K_SM1], pts: 2000,
      probe: [K_SM3, K_SM1, K_SM1b, GHOST] },
    { name: 'one 1 DP pick, Incursion (2 DP budget)',
      keys: [K_SM1], pts: 1000,
      probe: [K_SM3, K_SM1, K_SM1b] },
    { name: 'over-budget selection, Strike Force',
      keys: [K_SM3, K_SM1], pts: 2000,
      probe: [K_SM1b, K_SM3, K_SM1] },
    { name: 'GRACE-tagged pick, Strike Force',
      keys: [BA_G_A], pts: 2000,
      probe: [BA_G_B, BA_G_A, K_SM1] },
    { name: 'ghost in the selection',
      keys: [GHOST], pts: 2000,
      probe: [K_SM1, K_SM3, GHOST] },
  ];
}

for (const sc of scenarios()) {
  for (const key of sc.probe) {
    const st = E.detachmentPickerRowState(key, sc.keys, sc.pts);
    const others = sc.keys.filter(k => k !== key);
    const can = E.canAddDetachment(key, others, sc.pts);

    // (a) selected reflects membership in `keys`. Nothing else can flip this.
    ok(st.selected === (sc.keys.indexOf(key) >= 0),
       `${sc.name} / ${key}: selected matches membership in the set`);

    // (b) isGhost is "not in the current catalogue" and nothing else. Detachment
    //     records disappearing is the flag-don't-drop trigger — no rule about
    //     the SELECTION should be able to flip this.
    ok(st.isGhost === !DJ.detachments[key],
       `${sc.name} / ${key}: isGhost matches "not in the catalogue"`);

    // (c) canAdd is verbatim canAddDetachment's answer with `key` removed from
    //     the set. Reason and (for tag clash) tag + conflictsWith must match.
    eq(st.canAdd, can,
       `${sc.name} / ${key}: canAdd is canAddDetachment's answer, unmodified`);

    // (d) The DISABLED rule. A selected row is toggle-off-able whatever else is
    //     wrong with the set; a non-selected row is disabled iff canAdd is not
    //     ok. This is the one thing E1c-2 exists to guard.
    const expectedDisabled = st.selected ? false : !can.ok;
    ok(st.disabled === expectedDisabled,
       `${sc.name} / ${key}: disabled = selected ? false : !canAdd.ok`);
  }
}

// ── 2. A selected row is never disabled, even in the worst-case state ────────
// Over-budget AND tag-clashing AND with a ghost. Every currently-selected row
// must still be removable, or an imported list can strand the player.
console.log('E1c — a selected row is always toggle-off-able, however illegal the set');
const worst = [K_SM3, K_SM1, BA_G_A, BA_G_B, GHOST];
for (const k of worst) {
  const st = E.detachmentPickerRowState(k, worst, 2000);
  ok(st.selected === true,  `${k}: is selected in the worst-case set`);
  ok(st.disabled === false, `${k}: is still not disabled — the player can remove it`);
}
const worstState = E.detachmentSelectionState(worst, 2000);
ok(worstState.legal === false, 'the worst-case set is illegal on every axis');
ok(worstState.state === 'over', '  and specifically over budget');
ok(worstState.tagConflicts.length >= 1, '  and specifically carrying a tag clash');
ok(worstState.unresolved.length >= 1, '  and specifically carrying a ghost key');

// ── 3. detachmentRefusalText is a total function of canAdd ──────────────────
// The row's refusal string is a projection of the typed reason. No rule about
// budgets or tags is re-derived here; the point is that a disabled row is never
// mute (the failure mode B47 exists to fix).
console.log('E1c — every refusal reason has a prose form');
ok(E.detachmentRefusalText({ ok: true })  === '', 'an OK canAdd yields no text');
ok(E.detachmentRefusalText({ ok: false, reason: 'budget' }).length > 0, 'budget refusal has prose');
ok(E.detachmentRefusalText({ ok: false, reason: 'duplicate' }).length > 0, 'duplicate refusal has prose');
ok(E.detachmentRefusalText({ ok: false, reason: 'unknown' }).length > 0, 'unknown refusal has prose');
const tagText = E.detachmentRefusalText({ ok: false, reason: 'unique_tag', tag: 'GRACE', conflictsWith: [BA_G_A] });
ok(tagText.indexOf('GRACE') >= 0, 'unique-tag refusal names the tag');
ok(tagText.indexOf(DJ.detachments[BA_G_A].name) >= 0, 'unique-tag refusal names the other detachment');

// ── 4. detTier2Badge marks the tier per D192 ────────────────────────────────
console.log('D192 — the previous-edition badge is per item, not blanket');
ok(E.detTier2Badge('faction_pack') === '', 'faction_pack (current edition) carries no badge');
ok(E.detTier2Badge('wahapedia_10e').length > 0, 'wahapedia_10e is marked previous-edition');
ok(E.detTier2Badge('none').length > 0, 'a missing text source is marked, not silently blank');
ok(E.detTier2Badge(null).length > 0, 'null is treated as non-current');
ok(E.detTier2Badge(undefined).length > 0, 'undefined is treated as non-current');

// ── 5. The picker exercises every catalogue key, not just the fixtures ──────
// Randomly sample keys per army and confirm the disabled classification agrees
// with canAddDetachment. This catches a picker that special-cases the fixtures
// above without honouring the general rule.
console.log('E1c — every catalogue key, cross-checked against canAddDetachment');
const allKeys = Object.keys(DJ.detachments);
let checked = 0;
for (const k of allKeys) {
  // Against an empty set at Strike Force. A fresh add either fits or is refused
  // by one of the three rules; the picker's disabled flag must reflect the same.
  const st = E.detachmentPickerRowState(k, [], 2000);
  const can = E.canAddDetachment(k, [], 2000);
  if (st.disabled !== !can.ok) {
    ok(false, `${k}: picker disabled disagrees with canAddDetachment (empty set, 2000)`);
  }
  checked++;
}
ok(true, `swept ${checked} catalogue keys against an empty set at Strike Force`);

// Also against an over-budget set: every non-selected 3 DP pick must be
// disabled (nothing else can fit into a used-up budget) and every selected key
// must still be toggle-off-able. Uses a concrete faction's own keys so the set
// is realistic — the SM detachments.
const smKeys = DJ.armies['Space Marines'] || [];
const three  = smKeys.filter(k => Number(DJ.detachments[k].dp) === 3);
if (three.length >= 2) {
  const overSet = [three[0]];   // 3 DP already used
  for (const k of three.slice(1)) {
    const st = E.detachmentPickerRowState(k, overSet, 2000);
    ok(st.disabled === true, `${k}: a further 3 DP pick is disabled after 3 DP already used`);
  }
  const selfSt = E.detachmentPickerRowState(three[0], overSet, 2000);
  ok(selfSt.disabled === false, `${three[0]}: the row already selected is still toggle-off-able`);
}

console.log(fail === 0 ? '\nall E1c checks pass' : `\n${fail} E1c check(s) FAILED`);
process.exit(fail === 0 ? 0 : 1);
