// b123_check.js — B123. Enhancement-conferred BEARER STATLINE ABSOLUTE values,
// and the D335 precedence rule for when wargear and an Enhancement both set
// the same cell.
//
// B119's sibling, same discipline, different trap:
//
//   1. B119 composes a delta on top of a set value; B123 IS a set value, and
//      can collide with another set value already sitting in `ov` (wargear's
//      own SET, not a delta). D335: the numerically better UNCONDITIONAL
//      value wins the cell — lower for SV/FNP, higher for W.
//   2. A conditional Enhancement value (no shipped record has one — the table
//      is curated to unconditional bearer-self clauses only) must never
//      overwrite the cell even when it would be better, but must mark it.
//      Exercised here via a synthetic fixture, not shipped data.
//   3. The star can now appear ALONGSIDE a written value — every earlier star
//      source only ever fired on an UNwritten cell.
//
// Build-time only; not part of the served app.
// Usage: node b123_check.js [index.html] [detachments.json] [units.json] [unit_loadouts.json]

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
    // B123 (including enhBetterLegend) is nested inside B119's own markers.
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
  ENHANCEMENT_BEARER_STATS, ENHANCEMENT_BEARER_ABSOLUTE, B123_BETTER,
  enhancementBearerStatEffect, b119Compose, b119BearerStatMode, b119StatCtx,
  buildStatTable, enhModLegend, enhBetterLegend,
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

// ── 1. The table against the source it was derived from ──────────────────
console.log('table vs source');
const keys = Object.keys(E.ENHANCEMENT_BEARER_ABSOLUTE);
eq('record count', keys.length, 25);
eq('distinct enhancement names', new Set(keys.map(k => k.split('::')[1])).size, 11);
eq('distinct armies', new Set(keys.map(k => k.split('|')[0])).size, 11);

const CHARWORD = { SV: 'save', FNP: 'feel no pain', W: 'wounds' };
const IMPLEMENTED = new Set(['SV', 'FNP', 'W']);
let orphans = 0, unnamedChar = 0, unimplemented = 0, notAbsolute = 0;
for (const k of keys) {
  const i = k.indexOf('::');
  const det = DETS.detachments[k.slice(0, i)];
  const rec = det && (det.enhancements || []).find(e => e.name === k.slice(i + 2));
  if (!rec || !rec.description) { orphans++; console.log('    orphan key: ' + k); continue; }
  const text = rec.description.toLowerCase();
  for (const c of Object.keys(E.ENHANCEMENT_BEARER_ABSOLUTE[k].abs || {})) {
    if (!IMPLEMENTED.has(c)) { unimplemented++; console.log(`    ${k}: abs.${c} is not an implemented characteristic`); }
    if (!text.includes(CHARWORD[c])) { unnamedChar++; console.log(`    ${k}: abs.${c} not named in the description`); }
  }
  if (!/\bhas\b.*\b(characteristic of|ability)\b/.test(text)) {
    notAbsolute++; console.log(`    ${k}: description carries no "has ... characteristic of/ability" set-value verb`);
  }
}
eq('every key resolves to a real enhancement record', orphans, 0);
eq('every set characteristic is named in its description', unnamedChar, 0);
eq('every set characteristic is one the applier implements', unimplemented, 0);
eq('every record is a set-value, not a delta', notAbsolute, 0);

// Every row must rest on a clause that is BOTH unconditional AND about the
// bearer itself. Two of the eleven (Iron Resolve, Intoxicating Elixir) carry
// a second, conditional clause that hands the same ability to the rest of the
// unit — that half is deliberately not rendered, so the test is that a
// qualifying clause EXISTS, not that every clause qualifies.
const COND = /\b(once per|each time|while|until the end|at the start of|at the end of|instead|when|after|if|is selected to|can use this Enhancement)\b/i;
const BEARER_SELF = /\bthe bearer\b(?!'?s\s+unit)|\bbearer'?s(?!\s+unit)/i;
let conditionalOnly = 0;
for (const k of keys) {
  const i = k.indexOf('::');
  const rec = (DETS.detachments[k.slice(0, i)].enhancements || []).find(e => e.name === k.slice(i + 2));
  const text = (rec && rec.description) || '';
  const chars = Object.keys(E.ENHANCEMENT_BEARER_ABSOLUTE[k].abs || {})
                      .map(c => CHARWORD[c]).join('|');
  const charRe = new RegExp('(' + chars + ')', 'i');
  const good = text.split(/\.\s+/).some(
    c => !COND.test(c) && BEARER_SELF.test(c) && /\bhas\b/i.test(c) && charRe.test(c));
  if (!good) { conditionalOnly++; console.log(`    ${k}: no unconditional bearer-self clause found`); }
}
eq('every record rests on an unconditional bearer-self clause', conditionalOnly, 0);

// ── 2. B123 does not reach across into B99's or B119's own fields ────────
console.log('separation from B99/B119');
let stray = 0;
for (const k of keys) {
  const eff = E.ENHANCEMENT_BEARER_ABSOLUTE[k];
  if (eff.gr || eff.sel || eff.mod) { stray++; console.log(`    ${k}: carries a B99/B119 field`); }
}
eq('no absolute-value row carries a weapon selector, grant or delta field', stray, 0);

// ── 3. Effect lookup merges both tables ───────────────────────────────────
console.log('effect lookup (merge with B119)');
const mkEntry = (unit, enh) => ({
  listId: 1, unit_name: unit.unit_name, sizeIdx: 0, wargear: {}, otherOptions: {},
  enhancement: enh
});
const absOnly = E.enhancementBearerStatEffect(mkEntry({ unit_name: 'x' },
  { name: 'Artificer Armour', detachment_key: 'Space Marines|GLADIUS TASK FORCE' }));
ok(!!absOnly && !!absOnly.abs && !absOnly.mod, 'an absolute-only record returns {abs}, no mod');
eq('Artificer Armour: abs.SV', absOnly.abs.SV, '2');
eq('Artificer Armour: abs.FNP', absOnly.abs.FNP, '5');

const deltaOnly = E.enhancementBearerStatEffect(mkEntry({ unit_name: 'x' },
  { name: 'Rites of War', detachment_key: 'Space Marines|1ST COMPANY TASK FORCE' }));
ok(!!deltaOnly && !!deltaOnly.mod && !deltaOnly.abs, 'a delta-only record returns {mod}, no abs (B119 unaffected)');

ok(E.enhancementBearerStatEffect(mkEntry({ unit_name: 'x' }, null)) === null,
   'no assignment resolves to nothing');
ok(E.enhancementBearerStatEffect(mkEntry({ unit_name: 'x' },
     { name: 'Artificer Armour', detachment_key: 'No Such|DETACHMENT' })) === null,
   'an assignment whose record no longer resolves contributes nothing');

// ── 4. Rendering: the four scenarios D335 has to resolve ─────────────────
console.log('precedence rendering');
const mg = { M: '6"', T: 4, SV: '3+', INV: '', INV_Condition: '', FNP: '', FNP_Condition: '',
             W: 5, LD: '6+', OC: 1 };
const ctx = (abs, mode, name, condAbs) => ({ abs: abs, condAbs: condAbs, mode: mode, name: name });

// Scenario 1: an Enhancement absolute beats an unconditional wargear value.
// Wargear already set SV to 3+ (a storm shield's own SET text, say); the
// Enhancement's 2+ is better and must win the cell.
const h1 = E.buildStatTable(mg, { SV: '3' }, {}, null, ctx({ SV: '2' }, 'all', 'Artificer Armour'));
ok(h1.includes('<span class="stat-override">2+</span>'), 'Enhancement SV 2+ beats wargear SV 3+, and is shown');
ok(h1.includes('Modified by Artificer Armour'), 'the written value names its cause');
ok(!h1.includes('conditional value here'), 'no discarded-conditional legend when nothing was discarded');

// Reverse: wargear's unconditional value already beats the Enhancement's —
// the better (wargear) number stays, and nothing about the Enhancement shows,
// since the Enhancement never had a candidate worth naming.
const h1r = E.buildStatTable(mg, { SV: '2' }, {}, null, ctx({ SV: '3' }, 'all', 'Artificer Armour'));
ok(h1r.includes('<span class="stat-override">2+</span>'), 'a better wargear SV 2+ is kept over a worse Enhancement SV 3+');

// Scenario 2: an unconditional wargear value beats a CONDITIONAL Enhancement
// one. The unconditional (wargear) value is shown, and the cell is marked —
// synthetic condAbs, since no shipped record needs this path yet.
const h2 = E.buildStatTable(mg, { FNP: '4' }, {}, null,
  ctx({}, 'all', 'Some Future Enhancement', { FNP: '2' }));
ok(h2.includes('<span class="stat-override">4+</span>'), 'the unconditional wargear FNP 4+ is shown');
ok(h2.includes('<sup class="stat-asterisk">'), 'the cell is marked even though a value is already written');
ok(h2.includes('also has a conditional value here'), 'the legend discloses the discarded conditional alternative');

// Scenario 3: a Feel No Pain grant where no wargear speaks to the cell.
const h3 = E.buildStatTable(mg, {}, {}, null, ctx({ FNP: '5' }, 'all', 'Iron Resolve'));
ok(h3.includes('<span class="stat-override">5+</span>'), 'Iron Resolve: FNP —  -> 5+, highlighted');
ok(h3.includes('Modified by Iron Resolve'), 'the written value names its cause');
ok(!h3.includes('<sup class="stat-asterisk">'), 'a clean grant with no collision carries no asterisk');

// Scenario 4: legend wording agrees with B99's and B119's — same div class,
// same "Modified by <name>" phrasing, and 'some' mode still asterisks rather
// than ever writing a value the bearer cannot be pinned to.
ok(h3.includes('<div class="stat-asterisk-legend">'), 'the legend uses the same div class as B99/B119');
const h4 = E.buildStatTable(mg, {}, {}, null, ctx({ FNP: '5' }, 'some', 'Iron Resolve'));
ok(h4.includes('<sup class="stat-asterisk">') && !h4.includes('stat-override'),
   "'some' asterisks the FNP cell and never writes a value (B123 extends B119's FNP star support)");
ok(h4.includes('bearer only') && h4.includes('Iron Resolve'),
   "'some' names the cause in the asterisk legend, same wording as B119");

// W: a Wounds set-value that beats a lower wargear-set W.
const hW = E.buildStatTable(mg, { W: '3' }, {}, null, ctx({ W: '5' }, 'all', 'Flowing Flesh'));
ok(hW.includes('<span class="stat-override">5</span>'), 'Flowing Flesh: W 5 beats a lower wargear-set W of 3');

// 'none' and no-enhancement are indistinguishable from the pre-B123 render.
const hBase = E.buildStatTable(mg, {}, {}, null, null);
const hNone = E.buildStatTable(mg, {}, {}, null, ctx({ SV: '2' }, 'none', 'Artificer Armour'));
eq("'none' renders exactly the unmodified table", hNone, hBase);

// The caller's override object is never mutated.
const shared = { SV: '3' };
E.buildStatTable(mg, shared, {}, null, ctx({ SV: '2' }, 'all', 'Artificer Armour'));
eq('the caller\'s overrides object is not mutated', shared.SV, '3');

// ── 5. B123's comparator ──────────────────────────────────────────────────
console.log('comparator');
ok(E.B123_BETTER.SV('2', '3'),  'SV: 2+ is better than 3+');
ok(!E.B123_BETTER.SV('3', '2'), 'SV: 3+ is not better than 2+');
ok(E.B123_BETTER.FNP('4', '5'), 'FNP: 4+ is better than 5+');
ok(E.B123_BETTER.W('6', '5'),   'W: 6 is better than 5 (higher wins)');
ok(!E.B123_BETTER.W('5', '6'),  'W: 5 is not better than 6');

console.log(fail === 0 ? 'all B123 checks pass' : `b123_check: ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
