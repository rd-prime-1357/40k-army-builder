// e25_check.js — E25. Loads the real Force Disposition selection block out of
// index.html (and, for the output-line section, the real detachment-selection
// and Army List rendering blocks alongside it) and asserts the ticket's seven
// numbered points against real detachments.json records.
//
// Points covered:
//   1. available-set derivation (list-tolerant, [].concat(...))
//   2. auto-select on a singleton set
//   4. invalidation on detachment change (keep if still valid, else re-derive)
//   6. the army list output gains a Force Disposition line (info when chosen,
//      warning when more than one option exists and nothing is picked yet)
// (3 and 5 are persistence/UI-shape, covered structurally in section 4 below;
// point 7 is this file.)
//
// Build-time only; not part of the served app.
// Usage: node e25_check.js index.html detachments.json list_store.js
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadDerivation(path, defs) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const e25 = slice(lines, '// ── E25: Force Disposition selection', 'function renderForceDispositionPicker() {');
  const src = 'let detachmentDefs = DEFS; let selectedDetachments = []; let forceDispositionValue = null;\n' + e25
            + '\nreturn { availableForceDispositions, recomputeForceDisposition,'
            + ' getForceDisposition: () => forceDispositionValue,'
            + ' setForceDispositionValue: (v) => { forceDispositionValue = v; },'
            + ' setSelectedDetachments: (k) => { selectedDetachments = k; } };';
  return new Function('DEFS', src)(defs);
}

function loadOutput(path, defs, byArmy) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const limit = slice(lines, '// D115 — the unit limit depends', '// State');
  const e1b   = slice(lines, '// ── E1b: detachment selection rules', '// ── E1b block end');
  const out   = slice(lines, 'function renderSelectedDetachmentsHtml() {', '// ── Detail panel');
  const src = 'let detachmentDefs = DEFS; let detachmentsByArmy = BYARMY; '
            + 'let POINTS_CAP = 2000; let selectedDetachments = []; let forceDispositionValue = null;\n'
            + "function escHtml(s){ return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }\n"
            + "function escAttr(s){ return String(s==null?'':s); }\n"
            + limit + '\n' + e1b + '\n' + out
            + '\nreturn { renderSelectedDetachmentsHtml,'
            + ' setSelectedDetachments: (k) => { selectedDetachments = k; },'
            + ' setForceDispositionValue: (v) => { forceDispositionValue = v; } };';
  return new Function('DEFS', 'BYARMY', src)(defs, byArmy);
}

const idxPath   = process.argv[2] || 'index.html';
const detPath   = process.argv[3] || 'detachments.json';
const storePath = process.argv[4] || 'list_store.js';

const DJ = JSON.parse(fs.readFileSync(detPath, 'utf8'));
const D  = loadDerivation(idxPath, DJ.detachments);
const O  = loadOutput(idxPath, DJ.detachments, DJ.armies);
const S  = require('./' + storePath.replace(/^\.\//, ''));

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (a, b, msg) => ok(JSON.stringify(a) === JSON.stringify(b), `${msg} (got ${JSON.stringify(a)})`);

// Concrete real keys, one per Force Disposition, so the dedupe/mix tests are
// against actual catalogue records rather than synthetic ones.
const byDisp = {};
for (const [k, v] of Object.entries(DJ.detachments)) {
  if (v.force_disposition && !byDisp[v.force_disposition]) byDisp[v.force_disposition] = k;
}
const DISPS = Object.keys(byDisp);
ok(DISPS.length === 5, `detachments.json carries all five Force Disposition values (got ${DISPS.length})`);
const K_A = byDisp[DISPS[0]];
const K_B = byDisp[DISPS[1]];

// A second key sharing K_A's own disposition, for the "two detachments, one
// disposition" singleton case (E25 point 2).
const K_A2 = Object.keys(DJ.detachments).find(k => k !== K_A && DJ.detachments[k].force_disposition === DISPS[0]);
ok(!!K_A2, `a second detachment shares ${DISPS[0]} for the two-detachments-one-disposition case`);

// ── 1. Available-set derivation ──────────────────────────────────────────────
console.log('E25 point 1 — available set: deduplicated, list-tolerant, unknown keys ignored');
eq(D.availableForceDispositions([]), [], 'no detachments selected: empty set');
eq(D.availableForceDispositions([K_A]), [DISPS[0]], 'one detachment: its own disposition');
eq(D.availableForceDispositions([K_A, K_A2]), [DISPS[0]],
   'two detachments sharing a disposition: deduplicated to one');
eq(D.availableForceDispositions([K_A, K_B]), [DISPS[0], DISPS[1]],
   'two detachments, different dispositions: both, in selection order');
eq(D.availableForceDispositions(['Nonexistent|GHOST']), [],
   'an unresolved key contributes nothing rather than throwing');
eq(D.availableForceDispositions([K_A, 'Nonexistent|GHOST']), [DISPS[0]],
   'a mix of a real and a ghost key: only the real one counts');

// list-tolerance: [].concat(v) must handle both a scalar (today's real shape)
// and an array (a future 1-to-many MFM print) without an engine change.
console.log('E25 point 1 — [].concat(...) reads a future array-valued field with no engine change');
const arrayDefs = Object.assign({}, DJ.detachments, {
  'Synthetic|MULTI': { force_disposition: ['DISRUPTION', 'RECONNAISSANCE'] }
});
const D2 = loadDerivation(idxPath, arrayDefs);
eq(D2.availableForceDispositions(['Synthetic|MULTI']), ['DISRUPTION', 'RECONNAISSANCE'],
   'an array-valued force_disposition contributes every value it carries');
eq(D2.availableForceDispositions(['Synthetic|MULTI', K_A]).sort(),
   Array.from(new Set(['DISRUPTION', 'RECONNAISSANCE', DISPS[0]])).sort(),
   'an array-valued record still dedupes against a scalar one sharing a value');

// ── 2. Auto-select on a singleton set ────────────────────────────────────────
console.log('E25 point 2 — auto-select when the available set has exactly one member');
D.setSelectedDetachments([K_A]);
D.setForceDispositionValue(null);
D.recomputeForceDisposition();
ok(D.getForceDisposition() === DISPS[0], 'a single detachment auto-selects its own disposition');

D.setSelectedDetachments([K_A, K_A2]);
D.setForceDispositionValue(null);
D.recomputeForceDisposition();
ok(D.getForceDisposition() === DISPS[0],
   'two detachments sharing a disposition also auto-select it (singleton available set)');

console.log('E25 point 2 — more than one option requires an explicit pick');
D.setSelectedDetachments([K_A, K_B]);
D.setForceDispositionValue(null);
D.recomputeForceDisposition();
ok(D.getForceDisposition() === null, 'two detachments with different dispositions do not auto-select');

// ── 4. Invalidation on detachment change ─────────────────────────────────────
console.log('E25 point 4 — a still-valid selection survives a detachment change');
D.setSelectedDetachments([K_A, K_B]);
D.setForceDispositionValue(DISPS[1]);
D.recomputeForceDisposition();
ok(D.getForceDisposition() === DISPS[1], 'the existing pick is kept when still in the available set');

console.log('E25 point 4 — a selection that falls outside the new set is cleared, then re-derived');
D.setSelectedDetachments([K_A, K_B]);
D.setForceDispositionValue(DISPS[1]);
D.setSelectedDetachments([K_A]);   // K_B (and its disposition) removed
D.recomputeForceDisposition();
ok(D.getForceDisposition() === DISPS[0],
   'losing the detachment that carried the old pick clears it and re-derives the new singleton');

D.setSelectedDetachments([K_A, K_A2, K_B]);
D.setForceDispositionValue(DISPS[1]);
D.recomputeForceDisposition();
ok(D.getForceDisposition() === DISPS[1],
   'a pick still present after a detachment change (still 2 options) is left untouched');

console.log('E25 point 4 — clearing all detachments clears the selection with nothing to re-derive');
D.setSelectedDetachments([K_A]);
D.setForceDispositionValue(DISPS[0]);
D.setSelectedDetachments([]);
D.recomputeForceDisposition();
ok(D.getForceDisposition() === null, 'zero detachments selected leaves nothing chosen');

// ── 5 / 6. Missing selection and the army list output line ──────────────────
// Zero detachments selected -> no picker and no output section at all
// (E25 point 5's explicit carve-out) — the whole detachments block is empty.
console.log('E25 points 5/6 — zero detachments: no output section, no warning');
O.setSelectedDetachments([]);
O.setForceDispositionValue(null);
ok(O.renderSelectedDetachmentsHtml() === '', 'no detachments selected: renders nothing at all');

console.log('E25 point 6 — a resolved selection renders as an info line naming the disposition');
O.setSelectedDetachments([K_A]);
O.setForceDispositionValue(DISPS[0]);
let html = O.renderSelectedDetachmentsHtml();
ok(html.indexOf('det-list-info') >= 0, 'a chosen disposition renders on the neutral info line');
ok(html.indexOf('det-list-warning">Force Disposition not selected') < 0,
   'no missing-selection warning fires once a value is set');
const label = DISPS[0].toLowerCase().replace(/\b\w/g, c => c.toUpperCase());
ok(html.indexOf(label) >= 0, `the info line names the chosen disposition (${label})`);

console.log('E25 points 5/6 — more than one option and nothing chosen: flag-and-warn, not a hard block');
O.setSelectedDetachments([K_A, K_B]);
O.setForceDispositionValue(null);
html = O.renderSelectedDetachmentsHtml();
ok(html.indexOf('det-list-warning">Force Disposition not selected') >= 0,
   'an unresolved choice surfaces the same det-list-warning surface as other detachment-selection problems');
ok(html.indexOf('det-list-info') < 0, 'the warning and the info line are mutually exclusive');

// ── 3. Persistence: additive field inside the v1(v3) envelope ───────────────
console.log('E25 point 3 — force_disposition rides inside the existing schema, no version bump');
const V = S.SCHEMA_VERSION;
const meta = { id: 'l-test', name: 'T', points_target: 2000, primary_faction: 'Space Marines',
               created: 1, warlord_entry_id: null, detachments: [K_A],
               force_disposition: DISPS[0] };
const rec = S.buildRecord(meta, [], {});
ok(rec.schema_version === V, 'a record carrying force_disposition still writes at the unbumped module version');
ok(rec.force_disposition === DISPS[0], 'buildRecord carries the chosen disposition');
const noneRec = S.buildRecord(Object.assign({}, meta, { force_disposition: undefined }), [], {});
ok(noneRec.force_disposition === null, 'a missing force_disposition writes as null, never undefined');

const back = S.deserialize(rec, {});
ok(back.forceDisposition === DISPS[0], 'deserialize returns the stored disposition');
const oldRec = Object.assign({}, rec); delete oldRec.force_disposition;
const oldBack = S.deserialize(oldRec, {});
ok(oldBack.forceDisposition === null,
   'a record saved before E25 (no force_disposition at all) reads as "none chosen", not a crash');

console.log(fail === 0 ? '\nall E25 checks pass' : `\n${fail} E25 check(s) FAILED`);
process.exit(fail === 0 ? 0 : 1);
