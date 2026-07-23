// e1b_check.js — E1b. Loads the real detachment-selection block out of index.html
// and the real list-storage module out of list_store.js, and asserts the three
// constraints that govern a legal detachment set plus the schema migration chain.
//
// Three constraints, not one (D192 item 3, 25.04, D193):
//   1. combined DP within the battle-size budget
//   2. no detachment selected twice
//   3. no two selections sharing a Unique tag
//
// Also guards the thing that went wrong before E1b: list_store.js and the copy
// inlined into index.html are two files holding the same module, and they had
// silently drifted. Nothing else compares them.
//
// Build-time only; not part of the served app.
// Usage: node e1b_check.js index.html detachments.json list_store.js
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path, defs, byArmy) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const e1b   = slice(lines, '// ── E1b: detachment selection rules', '// ── E1b block end');
  const limit = slice(lines, '// D115 — the unit limit depends', '// State');
  const src = 'let detachmentDefs = DEFS; let detachmentsByArmy = BYARMY; let POINTS_CAP = 2000;\n'
            + limit + '\n' + e1b
            + '\nreturn { detachmentPointBudget, dpState, detachmentDp, dpUsed, duplicateDetachments,'
            + ' uniqueTagConflicts, unresolvedDetachments, detachmentSelectionState, canAddDetachment,'
            + ' detachmentKeysForFaction, battleSizeUnitLimit };';
  return new Function('DEFS', 'BYARMY', src)(defs, byArmy);
}

const idxPath  = process.argv[2] || 'index.html';
const detPath  = process.argv[3] || 'detachments.json';
const storePath = process.argv[4] || 'list_store.js';

const DJ = JSON.parse(fs.readFileSync(detPath, 'utf8'));
const E  = loadEngine(idxPath, DJ.detachments, DJ.armies);
const S  = require('./' + storePath.replace(/^\.\//, ''));

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (a, b, msg) => ok(JSON.stringify(a) === JSON.stringify(b), `${msg} (got ${JSON.stringify(a)})`);

// ── 1. DP budget comes from the battle size ──────────────────────────────────
// Army_Muster_Rules.txt 25.03: Incursion 2 DP, Strike Force 3 DP. D192 item 2:
// 3,000 points is not in 25.03 and is treated as Strike Force.
console.log('D192 — DP budget by battle size');
ok(E.detachmentPointBudget(500)  === 2, '500 pts is Incursion: 2 DP');
ok(E.detachmentPointBudget(1000) === 2, '1000 pts is Incursion: 2 DP');
ok(E.detachmentPointBudget(2000) === 3, '2000 pts is Strike Force: 3 DP');
ok(E.detachmentPointBudget(3000) === 3, '3000 pts is treated as Strike Force: 3 DP');

// The DP budget and the unit limit are two functions reading the same battle-size
// table. They agree today because both were written to; this is what stops them
// drifting apart later, which is the only way this pair can go wrong.
console.log('D192 — the DP budget and the unit limit cannot disagree about battle size');
for (const p of [500, 1000, 1001, 2000, 3000]) {
  ok(E.detachmentPointBudget(p) === E.battleSizeUnitLimit(p),
     `${p} pts: DP budget matches battleSizeUnitLimit (${E.detachmentPointBudget(p)})`);
}

// ── 2. dpState mirrors limitState ────────────────────────────────────────────
console.log('E1b — dpState: red means exceeded, never merely reached');
ok(E.dpState(0, 3) === 'ok',   '0 of 3 is ok');
ok(E.dpState(2, 3) === 'ok',   '2 of 3 is ok');
ok(E.dpState(3, 3) === 'at',   '3 of 3 is at-budget, not over');
ok(E.dpState(4, 3) === 'over', '4 of 3 is over');
ok(E.dpState(9, 0) === 'ok',   'a zero budget is not enforced');

// ── 3. DP sums off real records ──────────────────────────────────────────────
console.log('E1b — DP sums against real detachments.json records');
const K_SM3 = 'Space Marines|ARMOURED SPEARTIP';       // 3 DP
const K_SM1 = 'Space Marines|LIBRARIUS CONCLAVE';      // 1 DP
const K_SM1b = 'Space Marines|FULGURIS TASK FORCE';    // 1 DP
ok(E.detachmentDp(K_SM3) === 3, 'Armoured Speartip is 3 DP');
ok(E.detachmentDp(K_SM1) === 1, 'Librarius Conclave is 1 DP');
ok(E.dpUsed([K_SM1, K_SM1b]) === 2, 'two 1 DP detachments cost 2 DP combined');
ok(E.dpUsed([]) === 0, 'an empty selection costs nothing');
ok(E.detachmentDp('Space Marines|NO SUCH DETACHMENT') === 0,
   'an unresolved key contributes 0 DP rather than an invented cost');

// ── 4. 25.04 — no detachment twice ───────────────────────────────────────────
console.log('25.04 — no detachment selected twice');
eq(E.duplicateDetachments([K_SM1, K_SM3]), [], 'a clean pair has no duplicates');
eq(E.duplicateDetachments([K_SM1, K_SM3, K_SM1]), [K_SM1], 'a repeat is caught and named');
ok(E.canAddDetachment(K_SM1, [K_SM1], 2000).reason === 'duplicate',
   'adding an already-selected detachment is refused as a duplicate');

// ── 5. D193 / E1e — the Unique tag ───────────────────────────────────────────
// MFM_Instructions.txt, DETACHMENTS legend: you cannot select more than one
// detachment carrying the same Unique tag. Live in the data for two built armies.
console.log('D193 — Unique-tag exclusion, against the real tagged records');
const BA_GRACE_A = 'Blood Angels|ANGELIC INHERITORS';   // GRACE, 3 DP
const BA_GRACE_B = 'Blood Angels|LEGACY OF GRACE';      // GRACE, 1 DP
const BA_DOOM_A  = 'Blood Angels|WRATH OF THE DOOMED';  // DOOMED, 1 DP
const BA_DOOM_B  = 'Blood Angels|THE LOST BRETHREN';    // DOOMED, 2 DP
const DG_FLY_A   = 'Death Guard|FLYBLOWN HOST';         // FLYBLOWN, 1 DP
const DG_FLY_B   = 'Death Guard|CHAMPIONS OF CONTAGION';// FLYBLOWN, 2 DP

ok(DJ.detachments[BA_GRACE_A].unique_tag === 'GRACE' &&
   DJ.detachments[BA_GRACE_B].unique_tag === 'GRACE',
   'the GRACE pair is still tagged GRACE in the data');
eq(E.uniqueTagConflicts([BA_GRACE_A]), [], 'one GRACE detachment alone is fine');
ok(E.uniqueTagConflicts([BA_GRACE_A, BA_GRACE_B]).length === 1,
   'two GRACE detachments together are one conflict');
ok(E.uniqueTagConflicts([BA_GRACE_A, BA_GRACE_B])[0].tag === 'GRACE',
   'the conflict names the tag');
ok(E.uniqueTagConflicts([BA_GRACE_A, BA_GRACE_B])[0].keys.length === 2,
   'the conflict names both sides, not just the second');
ok(E.uniqueTagConflicts([BA_DOOM_A, BA_DOOM_B]).length === 1, 'DOOMED clashes too');
ok(E.uniqueTagConflicts([DG_FLY_A, DG_FLY_B]).length === 1, 'FLYBLOWN clashes too');
eq(E.uniqueTagConflicts([BA_GRACE_A, BA_DOOM_A]), [],
   'different tags do not clash with each other');
eq(E.uniqueTagConflicts([K_SM1, K_SM1b, K_SM3]), [],
   'untagged detachments never clash, however many are chosen');

// Every tag that exists in the data must clash with itself and nothing else.
console.log('D193 — every tagged pair in the catalogue clashes, derived not hard-coded');
const byTag = {};
for (const [k, v] of Object.entries(DJ.detachments)) {
  if (!v.unique_tag) continue;
  (byTag[v.unique_tag] = byTag[v.unique_tag] || []).push(k);
}
ok(Object.keys(byTag).length > 0, `the catalogue carries Unique tags (${Object.keys(byTag).length})`);
for (const [tag, keys] of Object.entries(byTag)) {
  if (keys.length < 2) continue;
  const c = E.uniqueTagConflicts([keys[0], keys[1]]);
  ok(c.length === 1 && c[0].tag === tag, `${tag}: the first two tagged records clash`);
}

// ── 6. canAddDetachment — the hard block, with a reason ──────────────────────
console.log('D192 item 3 — hard-block, and it says which rule it broke');
ok(E.canAddDetachment('Space Marines|NOT A REAL ONE', [], 2000).reason === 'unknown',
   'an unknown key is refused as unknown');
ok(E.canAddDetachment(K_SM1, [], 2000).ok === true, 'a legal first pick is allowed');
// Budget: 3 DP at Strike Force. A 3 DP pick on top of a 1 DP pick is 4 and refused.
ok(E.canAddDetachment(K_SM3, [K_SM1], 2000).reason === 'budget',
   '1 DP + 3 DP exceeds the 3 DP Strike Force budget and is refused');
ok(E.canAddDetachment(K_SM1b, [K_SM1], 2000).ok === true,
   '1 DP + 1 DP fits the Strike Force budget');
// The same pair at Incursion: 2 DP budget, so 1 + 1 exactly fills it and a third is refused.
ok(E.canAddDetachment(K_SM1b, [K_SM1], 1000).ok === true,
   '1 DP + 1 DP exactly fills the 2 DP Incursion budget');
ok(E.canAddDetachment(K_SM3, [], 1000).reason === 'budget',
   'a 3 DP detachment does not fit an Incursion list at all');
// Unique tag beats a selection that would otherwise fit the budget. WRATH OF THE
// DOOMED (1 DP) + THE LOST BRETHREN (2 DP) is exactly 3, so the budget is not the
// thing refusing it — the shared DOOMED tag is.
const addDoom = E.canAddDetachment(BA_DOOM_A, [BA_DOOM_B], 2000);
ok(E.dpUsed([BA_DOOM_A, BA_DOOM_B]) === 3, 'the DOOMED pair costs exactly the Strike Force budget');
ok(addDoom.reason === 'unique_tag', 'a Unique-tag clash is refused even when the DP fits exactly');
ok(addDoom.tag === 'DOOMED', 'the refusal names the tag');
eq(addDoom.conflictsWith, [BA_DOOM_B], 'the refusal names what it clashes with');
// When both rules apply, the tag wins the message: a budget refusal is "not right
// now", a tag clash is "never together", and only one of those is worth acting on.
const both = E.canAddDetachment(BA_GRACE_B, [BA_GRACE_A], 2000);
ok(E.dpUsed([BA_GRACE_A, BA_GRACE_B]) === 4, 'the GRACE pair also breaks the budget');
ok(both.reason === 'unique_tag', 'when both rules apply the tag clash is reported, not the budget');

// ── 7. detachmentSelectionState — the single read path ───────────────────────
console.log('E1b — detachmentSelectionState is the one place legality is decided');
const clean = E.detachmentSelectionState([K_SM1, K_SM1b], 2000);
ok(clean.legal === true && clean.state === 'ok' && clean.used === 2 && clean.remaining === 1,
   'two 1 DP picks at Strike Force: legal, 2 of 3 used, 1 left');
const atCap = E.detachmentSelectionState([K_SM3], 2000);
ok(atCap.state === 'at' && atCap.legal === true, 'a 3 DP pick at Strike Force is at-budget and still legal');
const overCap = E.detachmentSelectionState([K_SM3, K_SM1], 2000);
ok(overCap.state === 'over' && overCap.legal === false,
   'over-budget is reachable and reported illegal, not silently trimmed');
const tagged = E.detachmentSelectionState([BA_GRACE_B, BA_DOOM_A], 2000);
ok(tagged.legal === true, 'two differently-tagged 1 DP picks are legal');
const clash = E.detachmentSelectionState([BA_GRACE_B, BA_GRACE_A], 2000);
ok(clash.legal === false && clash.tagConflicts.length === 1,
   'a Unique-tag clash makes the set illegal on its own');
const ghost = E.detachmentSelectionState(['Space Marines|GONE AWAY'], 2000);
ok(ghost.unresolved.length === 1 && ghost.used === 0 && ghost.legal === false,
   'an unresolved key is kept, costs 0 DP, and makes the set illegal until fixed');

// ── 8. per-faction key lists ─────────────────────────────────────────────────
console.log('D192 — every army resolves its own detachment list');
for (const army of Object.keys(DJ.armies)) {
  const keys = E.detachmentKeysForFaction({ data_army: army });
  ok(keys.length === DJ.armies[army].length && keys.every(k => !!DJ.detachments[k]),
     `${army}: ${keys.length} keys, all resolving`);
}
eq(E.detachmentKeysForFaction(null), [], 'no faction yields no options rather than throwing');
eq(E.detachmentKeysForFaction({ data_army: 'Nonexistent' }), [],
   'an unknown army yields no options rather than throwing');

// ── 9. the current schema: persistence carries the selection ─────────────────
// The version number moves as later tickets add fields (v3 = E4b enhancements),
// so this section reads it from the module rather than pinning a literal. What
// it asserts is that a NEW record is written at whatever the module declares —
// the failure worth catching is buildRecord stamping a stale number.
console.log('E1b — SavedList schema, current version');
const V = S.SCHEMA_VERSION;
ok(V >= 2, 'SCHEMA_VERSION is at least 2 (E1b added the detachment field)');
const meta = { id: 'l-test', name: 'T', points_target: 2000, primary_faction: 'Blood Angels',
               created: 1, warlord_entry_id: null, detachments: [BA_GRACE_A, BA_DOOM_A] };
const rec = S.buildRecord(meta, [], {});
eq(rec.detachments, [BA_GRACE_A, BA_DOOM_A], 'buildRecord carries the keys in selection order');
ok(rec.schema_version === V, 'a new record is written at the module version');
const dupeRec = S.buildRecord(Object.assign({}, meta, { detachments: [K_SM1, K_SM1, K_SM1b] }), [], {});
eq(dupeRec.detachments, [K_SM1, K_SM1b], 'duplicates are collapsed at the persistence boundary');
const junkRec = S.buildRecord(Object.assign({}, meta, { detachments: [null, '', 3, K_SM1] }), [], {});
eq(junkRec.detachments, [K_SM1], 'non-string junk is dropped rather than persisted');
eq(S.buildRecord(Object.assign({}, meta, { detachments: undefined }), [], {}).detachments, [],
   'a missing detachment list writes as empty, never undefined');

const back = S.deserialize(rec, { detachmentExists: k => !!DJ.detachments[k] });
eq(back.detachments, [BA_GRACE_A, BA_DOOM_A], 'deserialize returns the keys unchanged');
ok(back.warnings.filter(w => w.type === 'unresolved_detachment').length === 0,
   'resolving keys raise no warning');
const ghostRec = S.buildRecord(Object.assign({}, meta, { detachments: ['Blood Angels|GONE'] }), [], {});
const ghostBack = S.deserialize(ghostRec, { detachmentExists: k => !!DJ.detachments[k] });
eq(ghostBack.detachments, ['Blood Angels|GONE'],
   'a key that no longer resolves is kept, not dropped (flag-don\'t-drop)');
ok(ghostBack.warnings.filter(w => w.type === 'unresolved_detachment').length === 1,
   'and it raises exactly one warning');

// ── 10. the v1 -> current migration ──────────────────────────────────────────
// The claim E1b makes about behaviour: a v1 record loads at the current version
// with an empty detachment set and NOTHING ELSE ALTERED. The second half is the
// part that would be easy to break and hard to notice. E4b added a second step
// (v2 -> v3, enhancement: null per entry), so a v1 record now walks both.
console.log('E1b — v1 records upgrade to the current version with an empty detachment set');
const v1 = {
  schema_version: 1, id: 'old', name: 'Old List', points_target: 1000,
  primary_faction: 'Space Marines', warlord_entry_id: 7, created: 111, modified: 222,
  entries: [{ entry_id: 1, unit_name: 'Captain', unit_id: '000000073', size_idx: 0,
              wargear: { a: 1 }, other_options: {}, attached_to: null, points_cache: 80 }]
};
const before = JSON.parse(JSON.stringify(v1));
const up = S.migrate(v1);
ok(up.schema_version === V, 'schema_version becomes the module version');
eq(up.detachments, [], 'the detachment set is empty');
for (const f of ['id', 'name', 'points_target', 'primary_faction', 'warlord_entry_id', 'created', 'modified']) {
  ok(JSON.stringify(up[f]) === JSON.stringify(before[f]), `${f} is untouched by the migration`);
}
// E4b: the v2 -> v3 step ADDS `enhancement: null` to each entry and rewrites
// nothing. Compare with that field stripped, then assert it was added and is
// null — so a migration that touched any other entry field still fails here.
const stripped = JSON.parse(JSON.stringify(up.entries)).map(e => { delete e.enhancement; return e; });
eq(stripped, before.entries, 'no existing entry field is altered by the migration');
ok(up.entries.every(e => 'enhancement' in e && e.enhancement === null),
   'every entry gains exactly one field, enhancement, set to null');
ok(Object.keys(up).length === Object.keys(before).length + 1,
   'the migration adds exactly one field and removes none');

const v0 = S.migrate({ id: 'x', entries: [] });   // no schema_version at all
ok(v0.schema_version === V && v0.detachments.length === 0,
   'a record with no schema_version at all is treated as pre-v2 and upgraded');
const v2 = S.migrate({ schema_version: 2, id: 'y', entries: [{ entry_id: 1 }], detachments: [K_SM1] });
eq(v2.detachments, [K_SM1], 'a v2 record keeps its detachment set through the v3 step');
ok(v2.schema_version === 3 && v2.entries[0].enhancement === null,
   'a v2 record gains enhancement: null and becomes v3');
const v3 = S.migrate({ schema_version: 3, id: 'y3', entries: [], detachments: [K_SM1] });
eq(v3.detachments, [K_SM1], 'a current-version record passes through untouched');
const future = S.migrate({ schema_version: 99, id: 'z' });
ok(future.__incompatible === true, 'a newer-schema record is still surfaced, not guessed at');

// ── 11. export / import carry the field ──────────────────────────────────────
console.log('E1b — export and import carry the detachment set');
const env = JSON.parse(S.exportRecords([rec]));
ok(env.schema_version === V, 'the export envelope stamps the module version');
eq(env.lists[0].detachments, [BA_GRACE_A, BA_DOOM_A], 'the exported record carries the keys');
const round = S.importRecords(JSON.stringify(env));
eq(round[0].detachments, [BA_GRACE_A, BA_DOOM_A], 'a current-version file round-trips its keys');
const oldFile = S.importRecords(JSON.stringify({ format: '40kab-lists', schema_version: 1, lists: [before] }));
ok(oldFile.length === 1 && oldFile[0].schema_version === V && oldFile[0].detachments.length === 0,
   'a v1 export file imports at the current version with an empty set rather than being rejected');

// ── 12. the drift guard ──────────────────────────────────────────────────────
// list_store.js and the copy inlined in index.html are the same module in two
// files. They had drifted (the standalone lost E9b's warlord field) and nothing
// compared them. This is the check that would have caught it.
console.log('E1b — list_store.js and the copy inlined in index.html are identical');
const idxLines = fs.readFileSync(idxPath, 'utf8').split('\n');
const s = idxLines.findIndex(l => l.startsWith('/* ====='));
const e = idxLines.findIndex(l => l.startsWith("})(typeof self !== 'undefined'"));
const inlined = idxLines.slice(s, e + 1).join('\n').trim();
const standalone = fs.readFileSync(storePath, 'utf8').trim();
ok(s >= 0 && e > s, 'the inlined module block is locatable in index.html');
ok(inlined === standalone, 'the inlined copy matches list_store.js byte-for-byte');

console.log(fail === 0 ? '\nall E1b checks pass' : `\n${fail} E1b check(s) FAILED`);
process.exit(fail === 0 ? 0 : 1);
