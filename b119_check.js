// b119_check.js — B119. Enhancement-conferred BEARER STATLINE modifications.
//
// B99's sibling, and the traps are different ones:
//
//   1. The delta lands on top of a SET value, not on the printed one. 40K
//      applies modifiers after characteristics that are set, so a wargear-set
//      Wounds of 6 plus a +1 Enhancement is 7. Applying the delta to the
//      datasheet's printed number instead would silently show 5.
//   2. T, W and OC are plain integers everywhere in the shipped data, so this
//      applier computes where B99's composes. That is only safe while it stays
//      true, so it is re-checked against every model group each run.
//   3. The statline table is per STATLINE GROUP, which makes the bearer question
//      answerable more precisely than for weapons: a retinue group gets NOTHING,
//      not an asterisk. But a unit with one statline group and several models —
//      Ravenwing Command Squad — still cannot pin the bearer, and must never
//      write a value there.
//
// It also holds the curated table to the source it came from (every key resolves
// to a real record, every characteristic is named in that record's description,
// every record is unconditional) and fails if a source record ever needs a
// characteristic the applier does not implement — Save in particular, whose
// "improve" means a LOWER number, the mirror image of B99's AP sign rule.
//
// Build-time only; not part of the served app.
// Usage: node b119_check.js [index.html] [detachments.json] [units.json] [unit_loadouts.json]

const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex((l, i) => i > s && l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const parts = [
    slice(lines, '// ── B99 BEGIN', '// ── B99 END'),
    slice(lines, '// ── B119 BEGIN', '// ── B119 END'),
    slice(lines, 'function loMaxCount', '// Unit Options UI for loadout-defined units.'),
    slice(lines, 'function statGroupScopes', '// D105: how many models in the CONFIGURED statline group'),
    slice(lines, 'function unitMaxModels', '// ── B15 / D105: conferred wargear characteristics'),
    slice(lines, 'function buildStatTable', 'function buildWeaponSections')
  ];
  const prelude = `
const PROFILE_SEP=/\\s[\\u2013\\-\\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}
function escHtml(s){return String(s==null?'':s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');}
let allUnits=[], loadoutDefs={}, wargearPoints={}, armyList=[], rawUnits=[];
let detachmentDefs={};
function enhancementRecord(name,key){
  const d=detachmentDefs[key];
  if(!d||!Array.isArray(d.enhancements))return null;
  return d.enhancements.find(e=>e.name===name)||null;
}
function renderAll(){}
`;
  return new Function(prelude + parts.join('\n') + `
return {
  ENHANCEMENT_BEARER_STATS, enhancementBearerStatEffect, b119Compose,
  b119BearerStatMode, b119StatCtx, buildStatTable, enhModLegend,
  statGroupScopes, isSingleModelGroup, loGroupCounts, loOptCounts, loadoutSize,
  setDetachments: d => { detachmentDefs = d; },
  setUnits:       u => { allUnits = u; },
  setLoadouts:    l => { loadoutDefs = l; }
};`)();
}

const E     = loadEngine(process.argv[2] || 'index.html');
const DETS  = JSON.parse(fs.readFileSync(process.argv[3] || 'detachments.json', 'utf8'));
const UNITS = JSON.parse(fs.readFileSync(process.argv[4] || 'units.json', 'utf8'));
const LOADS = JSON.parse(fs.readFileSync(process.argv[5] || 'unit_loadouts.json', 'utf8'));
E.setDetachments(DETS.detachments);
E.setLoadouts(LOADS);

const ALLU = [];
for (const f of UNITS) for (const u of f.units) ALLU.push(Object.assign({ _army: f.army }, u));
E.setUnits(ALLU.map(u => ({ unit_name: u.unit_name, unit_id: u.unit_id, sizes: u.sizes || [] })));

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (msg, got, want) => ok(String(got) === String(want),
  `${msg}: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`);

// ── 1. The applier computes; it does not compose ─────────────────────────
console.log('delta arithmetic');
eq('T 4 add 1',        E.b119Compose(4, 1), '5');
eq('"4" add 1',        E.b119Compose('4', 1), '5');
eq('OC 0 add 1',       E.b119Compose(0, 1), '1');
eq('W 9 add 1',        E.b119Compose(9, 1), '10');
eq('a non-integer is not moved', E.b119Compose('D6', 1), null);
eq('an absent value is not moved', E.b119Compose(null, 1), null);

// ── 2. The table against the source it was derived from ──────────────────
console.log('table vs source');
const keys = Object.keys(E.ENHANCEMENT_BEARER_STATS);
eq('record count', keys.length, 10);
eq('distinct enhancement names', new Set(keys.map(k => k.split('::')[1])).size, 6);
eq('distinct armies', new Set(keys.map(k => k.split('|')[0])).size, 8);

const CHARWORD = { T: 'toughness', W: 'wounds', OC: 'objective control',
                   SV: 'save', LD: 'leadership', M: 'movement' };
const IMPLEMENTED = new Set(['T', 'W', 'OC']);
let orphans = 0, unnamedChar = 0, unimplemented = 0, notDelta = 0;
for (const k of keys) {
  const i = k.indexOf('::');
  const det = DETS.detachments[k.slice(0, i)];
  const rec = det && (det.enhancements || []).find(e => e.name === k.slice(i + 2));
  if (!rec || !rec.description) { orphans++; console.log('    orphan key: ' + k); continue; }
  const text = rec.description.toLowerCase();
  for (const c of Object.keys(E.ENHANCEMENT_BEARER_STATS[k].mod || {})) {
    if (!IMPLEMENTED.has(c)) { unimplemented++; console.log(`    ${k}: mod.${c} is not an implemented characteristic`); }
    if (!text.includes(CHARWORD[c])) { unnamedChar++; console.log(`    ${k}: mod.${c} not named in the description`); }
  }
  if (!/\b(add|improve)\b/.test(text)) { notDelta++; console.log(`    ${k}: description carries no add/improve verb`); }
}
eq('every key resolves to a real enhancement record', orphans, 0);
eq('every modified characteristic is named in its description', unnamedChar, 0);
eq('every modified characteristic is one the applier implements', unimplemented, 0);
eq('every record is a delta, not a set-value', notDelta, 0);

// Every row must rest on at least one clause that is BOTH unconditional AND
// about the bearer itself. Seven of the ten carry a second, conditional clause
// that hands the same characteristic to the rest of the unit once per battle
// ("…the bearer can use this Enhancement. If it does, … add 1 to the Objective
// Control characteristic of all other models in the bearer's unit") — that half
// is deliberately not rendered, so the test is that a qualifying clause EXISTS,
// not that every clause qualifies.
const COND = /\b(once per|each time|while|until the end|at the start of|at the end of|instead|when|after|if|is selected to|can use this Enhancement)\b/i;
const BEARER_SELF = /\bthe bearer\b(?!'?s\s+unit)|\bbearer'?s(?!\s+unit)/i;
let conditional = 0;
for (const k of keys) {
  const i = k.indexOf('::');
  const rec = (DETS.detachments[k.slice(0, i)].enhancements || []).find(e => e.name === k.slice(i + 2));
  const text = (rec && rec.description) || '';
  const chars = Object.keys(E.ENHANCEMENT_BEARER_STATS[k].mod || {})
                      .map(c => CHARWORD[c]).join('|');
  const charRe = new RegExp('(' + chars + ')', 'i');
  const good = text.split(/\.\s+|,\s+and\s+|;\s*/).some(
    c => !COND.test(c) && BEARER_SELF.test(c) && /\b(add|improve)\b/i.test(c) && charRe.test(c));
  if (!good) { conditional++; console.log(`    ${k}: no unconditional bearer-self clause found`); }
}
eq('every record has an unconditional bearer-self statline clause', conditional, 0);

// The applier's integer assumption, against every model group in the data.
let nonInt = 0;
for (const u of ALLU) for (const g of (u.model_groups || []))
  for (const c of ['T', 'W', 'OC'])
    if (!/^-?\d+$/.test(String(g[c]))) {
      nonInt++;
      if (nonInt <= 3) console.log(`    ${u.unit_name} / ${g.model_group}: ${c} = ${g[c]}`);
    }
eq('T, W and OC are integers on every model group', nonInt, 0);

// ── 3. Bearer attribution, against the shipped data ──────────────────────
console.log('bearer attribution');
const byName = (army, name) => ALLU.find(u => u._army === army && u.unit_name === name);
const mkEntry = (unit, enh) => ({
  listId: 1, unit_name: unit.unit_name, sizeIdx: 0, wargear: {}, otherOptions: {},
  enhancement: enh
});

// A multi-statline-group CHARACTER: group 0 is the bearer and is written; the
// retinue group gets nothing at all, not an asterisk.
const apostle = byName('Chaos Space Marines', 'Dark Apostle');
const apEntry = mkEntry(apostle, { name: 'Living Carapace',
                                   detachment_key: 'Chaos Space Marines|CREATIONS OF BILE' });
eq('Dark Apostle: statline group 0 is the bearer',
   E.b119BearerStatMode(apostle, apostle.model_groups[0], 0, apEntry), 'all');
eq('Dark Apostle: the Dark Disciples group is not the bearer',
   E.b119BearerStatMode(apostle, apostle.model_groups[1], 1, apEntry), 'none');

const commune = byName('Chaos Space Marines', 'Dark Commune');
eq('Dark Commune: the Cult Demagogue group is the bearer',
   E.b119BearerStatMode(commune, commune.model_groups[0], 0,
     mkEntry(commune, { name: 'Living Carapace',
                        detachment_key: 'Chaos Space Marines|CREATIONS OF BILE' })), 'all');

const enforcer = byName('Chaos Space Marines', 'Traitor Enforcer');
eq('Traitor Enforcer: the Enforcer group is the bearer',
   E.b119BearerStatMode(enforcer, enforcer.model_groups[0], 0,
     mkEntry(enforcer, { name: 'Living Carapace',
                         detachment_key: 'Chaos Space Marines|CREATIONS OF BILE' })), 'all');

// The trap: ONE statline group, THREE models, only one of them the CHARACTER.
const rcs = byName('Dark Angels', 'Ravenwing Command Squad');
const rcsEnt = mkEntry(rcs, { name: 'Rites of War',
                              detachment_key: 'Dark Angels|1ST COMPANY TASK FORCE' });
ok(E.isSingleModelGroup(rcs), 'Ravenwing Command Squad reads as a single STATLINE group (the trap)');
eq('Ravenwing Command Squad: the bearer cannot be pinned',
   E.b119BearerStatMode(rcs, rcs.model_groups[0], 0, rcsEnt), 'some');

// A plain single-model Character is written without ceremony.
const capt = ALLU.find(u => u.unit_type === 'Character' && (u.model_groups || []).length === 1
                            && !LOADS[u.unit_id]);
if (capt) eq(`${capt.unit_name}: a statline-only Character is the bearer`,
             E.b119BearerStatMode(capt, capt.model_groups[0], 0, mkEntry(capt, null)), 'all');

// Every eligible bearer resolves to a mode; none of them silently falls through.
let modes = { all: 0, some: 0, none: 0 };
for (const u of ALLU) {
  if (u.unit_type !== 'Character') continue;
  const m = E.b119BearerStatMode(u, u.model_groups[0], 0, mkEntry(u, null));
  modes[m] = (modes[m] || 0) + 1;
}
ok(modes.all > 0 && modes.some > 0,
   `bearer modes across every Character unit: ${JSON.stringify(modes)} — both readings exercised`);

// ── 4. Rendering: value, asterisk, nothing ───────────────────────────────
console.log('stat cell rendering');
const mg = { M: '6"', T: 4, SV: '3+', INV: '', INV_Condition: '', FNP: '', FNP_Condition: '',
             W: 5, LD: '6+', OC: 1 };
const ctx = (mod, mode, name) => ({ mod: mod, mode: mode, name: name });

const hT = E.buildStatTable(mg, {}, {}, null, ctx({ T: 1 }, 'all', 'Brazen Form'));
ok(hT.includes('<span class="stat-override">5</span>'), 'Brazen Form: T 4 -> 5, highlighted');
ok(hT.includes('Modified by Brazen Form'), 'the written value names its cause');
ok(!hT.includes('<sup class="stat-asterisk">'), 'a written value carries no asterisk');

const hOC = E.buildStatTable(mg, {}, {}, null, ctx({ OC: 1 }, 'all', 'Rites of War'));
ok(hOC.includes('<span class="stat-override">2</span>'), 'Rites of War: OC 1 -> 2, highlighted');

const hW = E.buildStatTable(mg, {}, {}, null, ctx({ W: 1 }, 'all', 'Living Carapace'));
ok(hW.includes('<span class="stat-override">6</span>'), 'Living Carapace: W 5 -> 6, highlighted');

// Trap 1: the delta lands on the SET value, not on the printed one.
const hSet = E.buildStatTable(mg, { W: '6' }, {}, null, ctx({ W: 1 }, 'all', 'Living Carapace'));
ok(hSet.includes('<span class="stat-override">7</span>'),
   'a wargear-set W of 6 plus a +1 Enhancement reads 7, not 6');

// 'some': the printed value stays and the cell is asterisked.
const hSome = E.buildStatTable(mg, {}, {}, null, ctx({ OC: 1 }, 'some', 'Rites of War'));
ok(hSome.includes('<sup class="stat-asterisk">') && !hSome.includes('stat-override'),
   "'some' asterisks the cell and never writes a value");
ok(hSome.includes('bearer only') && hSome.includes('Rites of War'),
   "'some' names the cause in the asterisk legend");

// 'none' and no-enhancement are indistinguishable from the pre-B119 render.
const hBase = E.buildStatTable(mg, {}, {}, null, null);
const hNone = E.buildStatTable(mg, {}, {}, null, ctx({ OC: 1 }, 'none', 'Rites of War'));
eq("'none' renders exactly the unmodified table", hNone, hBase);
ok(!hBase.includes('stat-override') && !hBase.includes('<sup class="stat-asterisk">'),
   'a table with no enhancement and no wargear is completely unmarked');

// The pre-existing wargear/aura paths still behave: an override on W or SV is
// still written and still suppresses its own asterisk.
const hWargear = E.buildStatTable(mg, { W: '6', SV: '2' }, { W: true, SV: true }, null, null);
ok(hWargear.includes('<span class="stat-override">6</span>')
   && hWargear.includes('<span class="stat-override">2+</span>'),
   'wargear set-values still render (B15 path unchanged)');
const hFlagOnly = E.buildStatTable(mg, {}, { W: true }, null, null);
ok(hFlagOnly.includes('<sup class="stat-asterisk">') && hFlagOnly.includes('see Wargear Abilities'),
   'a wargear flag with no value still asterisks and keeps its own legend');
const hAura = E.buildStatTable(mg, {}, {}, ['T', 'OC'], null);
ok(hAura.includes('<sup class="stat-asterisk">') && hAura.includes('see Abilities'),
   'B7b aura stars on T and OC still render');

// An enhancement value and an aura star on the same cell: the value wins, the
// same way it already does for W and SV.
const hBoth = E.buildStatTable(mg, {}, {}, ['T'], ctx({ T: 1 }, 'all', 'Brazen Form'));
ok(hBoth.includes('<span class="stat-override">5</span>'),
   'an Enhancement value on a cell that also carries an aura star writes the value');

// The caller's override object is never mutated — one group's delta must not
// leak into the next group's table.
const shared = { W: '6' };
E.buildStatTable(mg, shared, {}, null, ctx({ W: 1 }, 'all', 'Living Carapace'));
eq('the caller\'s overrides object is not mutated', shared.W, '6');

// ── 5. Effect lookup ─────────────────────────────────────────────────────
console.log('effect lookup');
ok(!!E.enhancementBearerStatEffect(mkEntry({ unit_name: 'x' },
     { name: 'Rites of War', detachment_key: 'Space Marines|1ST COMPANY TASK FORCE' })),
   'a real assignment resolves to a table row');
ok(E.enhancementBearerStatEffect(mkEntry({ unit_name: 'x' }, null)) === null,
   'no assignment resolves to nothing');
ok(E.enhancementBearerStatEffect(mkEntry({ unit_name: 'x' },
     { name: 'Rites of War', detachment_key: 'No Such|DETACHMENT' })) === null,
   'an assignment whose record no longer resolves contributes nothing');
ok(E.enhancementBearerStatEffect(mkEntry({ unit_name: 'x' },
     { name: 'Iron Resolve', detachment_key: 'Blood Angels|1ST COMPANY TASK FORCE' })) === null,
   'a real enhancement with no bearer-statline delta contributes nothing');

// ── 6. B119 does not reach across into B99's table ───────────────────────
console.log('separation from B99');
let shared2 = 0;
for (const k of keys) {
  const eff = E.ENHANCEMENT_BEARER_STATS[k];
  if (eff.gr || eff.sel) { shared2++; console.log(`    ${k}: carries a B99 weapon field`); }
}
eq('no bearer-statline row carries a weapon selector or grant', shared2, 0);

console.log(fail === 0 ? 'all B119 checks pass' : `b119_check: ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
