// b99_check.js — B99. Enhancement-conferred weapon modifications.
//
// An assigned enhancement whose text changes the BEARER'S OWN weapon profile now
// reaches the weapon tables. Three things in that sentence are traps, and this
// harness exists to pin all three plus the table itself:
//
//   1. "Improve the Armour Penetration characteristic by 1" makes AP MORE
//      NEGATIVE (-1 -> -2), while on S/A/D "improve" and "add" both mean add. A
//      single generic "+N" is wrong for the most common modifier in the set.
//   2. A and D are stored as strings and are not always numeric (D6, D3+1,
//      2D6+2). Those compose — D6 improved by 1 is "D6+1" — they do not compute.
//   3. The rollup table shows one row per weapon with a count spanning every
//      model that holds it, but an enhancement reaches ONE model. Writing a
//      modified number into such a row asserts something false about the others,
//      so the D105/D112 three-way rule applies: value / asterisk / nothing.
//
// It also holds the curated table to the source it was derived from (every key
// resolves to a real record; every characteristic and ability named in the table
// is named in that record's description) and pins the assumption the carrier rule
// rests on — that a multi-statline-group CHARACTER's own group is group 0.
//
// Build-time only; not part of the served app.
// Usage: node b99_check.js [index.html] [detachments.json] [units.json] [unit_loadouts.json]

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
    slice(lines, 'function loMaxCount', '// Unit Options UI for loadout-defined units.'),
    slice(lines, 'function statGroupScopes', '// D105: how many models in the CONFIGURED statline group'),
    slice(lines, 'function unitMaxModels', '// ── B15 / D105: conferred wargear characteristics'),
    slice(lines, 'function loWeaponTable', '// ── B47: inline detail expanders'),
    slice(lines, 'function buildWeaponTable', '// ── Collapsible modal sections')
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
  ENHANCEMENT_WEAPON_EFFECTS, enhancementWeaponEffect, b99Selects, b99Compose,
  b99ApplyAp, b99WeaponMods, b99Cells, b99Legend, b99BearerScope, b99RollupCtx,
  loWeaponTable, buildWeaponTable, statGroupScopes, isSingleModelGroup,
  loGroupCounts, loOptCounts, loCarriers, loadoutSelections, loRollup,
  setDetachments: d => { detachmentDefs = d; },
  setUnits:       u => { allUnits = u; },
  setLoadouts:    l => { loadoutDefs = l; }
};`)();
}

const E    = loadEngine(process.argv[2] || 'index.html');
const DETS = JSON.parse(fs.readFileSync(process.argv[3] || 'detachments.json', 'utf8'));
const UNITS = JSON.parse(fs.readFileSync(process.argv[4] || 'units.json', 'utf8'));
const LOADS = JSON.parse(fs.readFileSync(process.argv[5] || 'unit_loadouts.json', 'utf8'));
E.setDetachments(DETS.detachments);
E.setLoadouts(LOADS);

const ALLU = [];
for (const f of UNITS) for (const u of f.units) ALLU.push(Object.assign({ _army: f.army }, u));

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (msg, got, want) => ok(String(got) === String(want),
  `${msg}: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`);

// ── 1. Armour Penetration: "improve" means more negative ───────────────────
// The single most common modifier in Set A, and the one a generic "+N" gets
// backwards. Every AP value in the shipped data is 0 or negative.
console.log('AP sign');
eq('AP  0 improved by 1', E.b99ApplyAp(0, 1), '-1');
eq('AP -1 improved by 1', E.b99ApplyAp(-1, 1), '-2');
eq('AP -4 improved by 1', E.b99ApplyAp(-4, 1), '-5');
eq('AP -1 improved by 2', E.b99ApplyAp(-1, 2), '-3');
eq('AP "None" untouched',  E.b99ApplyAp('None', 1), 'None');

// ── 2. A and D compose, they do not compute ───────────────────────────────
console.log('variable A / D composition');
eq('4 add 3',        E.b99Compose(4, 3), '7');
eq('"3" add 1',      E.b99Compose('3', 1), '4');
eq('D6 add 1',       E.b99Compose('D6', 1), 'D6+1');
eq('D3 add 1',       E.b99Compose('D3', 1), 'D3+1');
eq('D6+3 add 1',     E.b99Compose('D6+3', 1), 'D6+4');
eq('2D6+2 add 1',    E.b99Compose('2D6+2', 1), '2D6+3');
eq('3D3 add 1',      E.b99Compose('3D3', 1), '3D3+1');
eq('2D6 add 2',      E.b99Compose('2D6', 2), '2D6+2');
eq('"None" untouched', E.b99Compose('None', 1), 'None');

// ── 3. Selectors ──────────────────────────────────────────────────────────
console.log('weapon selectors');
const wMelee   = { weapon_name: 'Sword',  weapon_type: 'Melee',  A: '4', S: 4, AP: -1, D: '1', weapon_ability_names: [] };
const wExtra   = { weapon_name: 'Claw',   weapon_type: 'Melee',  A: '2', S: 4, AP: 0,  D: '1', weapon_ability_names: ['Extra Attacks'] };
const wRanged  = { weapon_name: 'Bolter', weapon_type: 'Ranged', A: '2', S: 4, AP: 0,  D: '1', weapon_ability_names: [] };
const wPsyMel  = { weapon_name: 'Staff',  weapon_type: 'Melee',  A: '3', S: 6, AP: -2, D: 'D3', weapon_ability_names: ['Psychic'] };
const wPsyRng  = { weapon_name: 'Bolt',   weapon_type: 'Ranged', A: 'D6', S: 5, AP: -1, D: '2', weapon_ability_names: ['Psychic'] };
ok( E.b99Selects('melee', wMelee)   && !E.b99Selects('melee', wRanged),  'melee picks Melee only');
ok( E.b99Selects('ranged', wRanged) && !E.b99Selects('ranged', wMelee),  'ranged picks Ranged only');
ok( E.b99Selects('all', wMelee)     &&  E.b99Selects('all', wRanged),    'all picks both types');
ok( E.b99Selects('psychic', wPsyMel) && E.b99Selects('psychic', wPsyRng)
    && !E.b99Selects('psychic', wMelee),                                 'psychic reads weapon_ability_names, not type');
ok( E.b99Selects('melee_no_extra', wMelee) && !E.b99Selects('melee_no_extra', wExtra),
    'melee_no_extra excludes Extra Attacks weapons');

// ── 4. Whole-profile application ──────────────────────────────────────────
console.log('profile application');
const effVortex = E.ENHANCEMENT_WEAPON_EFFECTS["Thousand Sons|GRAND COVEN::Eldritch Vortex of E'Taph"];
ok(!!effVortex, "Eldritch Vortex of E'Taph is in the table (the originally reported miss)");
const mV = E.b99WeaponMods(wPsyMel, effVortex);
eq('Vortex: Psychic staff S 6 -> 7', mV.vals.S, '7');
eq('Vortex: Psychic staff D D3 -> D3+1', mV.vals.D, 'D3+1');
ok(E.b99WeaponMods(wMelee, effVortex) === null, 'Vortex does not touch a non-Psychic weapon');

const effAncient = E.ENHANCEMENT_WEAPON_EFFECTS['Dark Angels|WRATH OF THE ROCK::Ancient Weapons'];
const mA = E.b99WeaponMods(wMelee, effAncient);
eq('Ancient Weapons: S 4 -> 6',  mA.vals.S,  '6');
eq('Ancient Weapons: AP -1 -> -2', mA.vals.AP, '-2');
eq('Ancient Weapons: D 1 -> 2',  mA.vals.D,  '2');

// A grant the weapon already carries is not added twice, and an effect that adds
// nothing at all reports nothing rather than an empty modification.
const wPrec = Object.assign({}, wMelee, { weapon_ability_names: ['Precision'] });
const effPrec = E.ENHANCEMENT_WEAPON_EFFECTS["Emperor's Children|SLAANESH'S CHOSEN::Slayer of Champions"];
ok(!!effPrec, 'Slayer of Champions is in the table');
eq('Precision granted to a plain weapon', (E.b99WeaponMods(wMelee, effPrec) || {}).gr, ['Precision']);
ok(E.b99WeaponMods(wPrec, effPrec) === null, 'a weapon that already has Precision is not modified');

// ── 5. Cell rendering: value vs asterisk vs nothing ───────────────────────
console.log('cell rendering');
const cAll  = E.b99Cells(wMelee, effAncient, 'all');
const cSome = E.b99Cells(wMelee, effAncient, 'some');
const cNone = E.b99Cells(wMelee, effAncient, 'none');
ok(cAll.wrote && !cAll.star && String(cAll.S).includes('>6<'),   "'all' writes the modified value");
ok(cSome.star && !cSome.wrote && String(cSome.S).includes('>4') === false
   && String(cSome.S).startsWith('4') && String(cSome.S).includes('stat-asterisk'),
   "'some' keeps the printed value and adds an asterisk");
eq("'none' leaves S alone",  cNone.S,  wMelee.S);
eq("'none' leaves AP alone", cNone.AP, wMelee.AP);
ok(!cNone.star && !cNone.wrote, "'none' reports neither a value nor an asterisk");
ok(E.b99Legend(effAncient, true, true, 'Ancient Weapons').includes('bearer only'),
   'an asterisk anywhere wins the legend wording');
ok(E.b99Legend(effAncient, false, true, 'Ancient Weapons').includes('Modified by'),
   'written values alone get the plain legend');
eq('no effect, no legend', E.b99Legend(null, false, false, 'x'), '');

// ── 6. The curated table against the source it came from ─────────────────
console.log('table vs source');
const keys = Object.keys(E.ENHANCEMENT_WEAPON_EFFECTS);
eq('record count', keys.length, 78);
const names = new Set(keys.map(k => k.split('::')[1]));
eq('distinct enhancement names', names.size, 43);

let orphans = 0, unnamedChar = 0, unnamedGrant = 0;
const CHARWORD = { S: 'strength', A: 'attacks', D: 'damage', AP: 'armour penetration' };
for (const k of keys) {
  const i = k.indexOf('::');
  const det = DETS.detachments[k.slice(0, i)];
  const rec = det && (det.enhancements || []).find(e => e.name === k.slice(i + 2));
  if (!rec || !rec.description) { orphans++; console.log('    orphan key: ' + k); continue; }
  const text = rec.description.toLowerCase();
  const eff = E.ENHANCEMENT_WEAPON_EFFECTS[k];
  for (const c of Object.keys(eff.mod || {}))
    if (!text.includes(CHARWORD[c])) { unnamedChar++; console.log(`    ${k}: mod.${c} not named in the description`); }
  for (const g of (eff.gr || []))
    if (!text.includes(String(g).toLowerCase())) { unnamedGrant++; console.log(`    ${k}: grant "${g}" not named in the description`); }
}
eq('every key resolves to a real enhancement record', orphans, 0);
eq('every modified characteristic is named in its description', unnamedChar, 0);
eq('every granted ability is named in its description', unnamedGrant, 0);

// The sign rule above assumes no source record ever ADDS to Armour Penetration —
// every one of them says "improve". If that ever stops being true this fails here
// rather than rendering the wrong number.
let addAp = 0;
for (const dk of Object.keys(DETS.detachments))
  for (const e of (DETS.detachments[dk].enhancements || [])) {
    const t = (e.description || '').toLowerCase();
    if (/\badd \d+ to the [^.]{0,80}armour penetration/.test(t)) {
      addAp++; console.log(`    "add … to the Armour Penetration" in ${dk}::${e.name}`);
    }
  }
eq('no source record adds to Armour Penetration', addAp, 0);

// ── 7. The carrier rule, against the shipped data ────────────────────────
console.log('bearer attribution');
const byName = (army, name) => ALLU.find(u => u._army === army && u.unit_name === name);
const mkEntry = (unit, enh) => ({
  listId: 1, unit_name: unit.unit_name, sizeIdx: 0, wargear: {},
  enhancement: enh
});
// allUnits is the lightweight view loadoutSize reads; sizes is optional there.
E.setUnits(ALLU.map(u => ({ unit_name: u.unit_name, unit_id: u.unit_id, sizes: u.sizes || [] })));

// A multi-statline-group CHARACTER: the bearer IS attributable, because the
// CHARACTER's own statline group maps to its own single-model loadout group.
const apostle = byName('Chaos Space Marines', 'Dark Apostle');
const apDef   = LOADS[apostle.unit_id];
const apEntry = mkEntry(apostle, { name: 'Cursed Fang', detachment_key: 'Chaos Space Marines|DECEPTORS' });
const apScope = E.b99BearerScope(apostle, apDef, apEntry);
ok(apScope && !apScope.single, 'Dark Apostle: bearer resolves to a group, not to "the only model"');
eq('Dark Apostle: bearer group', (apScope || {}).scope, ['Dark Apostle']);
const apCtx = E.b99RollupCtx(apostle, apDef, apEntry);
ok(!!apCtx, 'Dark Apostle: an assigned Set A enhancement produces a rollup context');
const crozius = apostle.weapons.find(w => w.weapon_name === 'Accursed crozius');
const ccw     = apostle.weapons.find(w => w.weapon_name === 'Close combat weapon');
eq('Accursed crozius (bearer only, ×1) is written', apCtx.modeFor(crozius, 1), 'all');
eq('Close combat weapon (2 Disciples, not the bearer) is left alone', apCtx.modeFor(ccw, 2), 'none');

// The unit the statline test would have got wrong: ONE statline group, THREE
// loadout groups, three models, only one of them the CHARACTER, and nothing in
// the data saying which. Must never write a value.
const rcs    = byName('Dark Angels', 'Ravenwing Command Squad');
const rcsDef = LOADS[rcs.unit_id];
const rcsEnt = mkEntry(rcs, { name: 'Ancient Weapons', detachment_key: 'Dark Angels|WRATH OF THE ROCK' });
ok(E.isSingleModelGroup(rcs), 'Ravenwing Command Squad reads as a single STATLINE group (the trap)');
ok(E.b99BearerScope(rcs, rcsDef, rcsEnt) === null, 'Ravenwing Command Squad: the bearer cannot be pinned');
const rcsCtx = E.b99RollupCtx(rcs, rcsDef, rcsEnt);
eq('Ravenwing Command Squad: every row is asterisked, never valued',
   rcsCtx.modeFor(rcs.weapons.find(w => w.weapon_type === 'Melee'), 3), 'some');

// The assumption b99BearerScope rests on, checked against every unit that could
// exercise it rather than against the three we happen to know about.
let badGroup0 = 0, multi = 0;
for (const u of ALLU) {
  if (u.unit_type !== 'Character') continue;
  if ((u.model_groups || []).length <= 1) continue;
  const def = LOADS[u.unit_id];
  if (!def) continue;
  multi++;
  const scopes = E.statGroupScopes(u, u.model_groups[0], def);
  const counts = E.loGroupCounts(def, (def.size_brackets || [0])[0], {});
  let n = 0;
  for (const g of (scopes || [])) n += counts[g] || 0;
  if (!scopes || n !== 1) { badGroup0++; console.log(`    ${u._army} / ${u.unit_name}: statline group 0 does not map to one model`); }
}
ok(multi > 0, `${multi} multi-statline-group Character units exercised`);
eq('statline group 0 is the CHARACTER on every one of them', badGroup0, 0);

// ── 8. The two weapon tables agree, and the browse view is untouched ─────
console.log('render surfaces');
const lord = { unit_name: 'Test Lord', unit_type: 'Character', model_groups: [{ model_group: 'All' }],
               weapons: [wMelee], unit_id: 'zz' };
const lordEntry = mkEntry(lord, { name: 'Ancient Weapons', detachment_key: 'Dark Angels|WRATH OF THE ROCK' });
const cfgHtml  = E.buildWeaponTable('Melee Weapons', [wMelee], 'configured',
  { activeBases: new Set(), replacedBases: new Set(), bundleAddBases: new Set(), hasWargear: false }, lord, lordEntry);
const rollHtml = E.loWeaponTable('Melee Weapons', [wMelee], { sword: 1 },
  { eff: effAncient, name: 'Ancient Weapons', modeFor: () => 'all' });
const cells = h => (h.match(/<td[^>]*>[\s\S]*?<\/td>/g) || [])
  .map(c => c.replace(/<td[^>]*>|<\/td>/g, '').replace(/<span class="lo-wcount">[\s\S]*?<\/span>/g, '').trim());
const cfgCells = cells(cfgHtml), rollCells = cells(rollHtml);
eq('both surfaces render the same S cell',  cfgCells[4], rollCells[4]);
eq('both surfaces render the same AP cell', cfgCells[5], rollCells[5]);
eq('both surfaces render the same D cell',  cfgCells[6], rollCells[6]);
ok(cfgHtml.includes('Ancient Weapons') && rollHtml.includes('Ancient Weapons'),
   'both surfaces name the enhancement in the legend');

const fullHtml = E.buildWeaponTable('Melee Weapons', [wMelee], 'full', null, lord, lordEntry);
ok(!fullHtml.includes('stat-override') && !fullHtml.includes('stat-asterisk'),
   'the unconfigured browse view is never modified');
ok(!E.buildWeaponTable('Melee Weapons', [wMelee], 'configured',
     { activeBases: new Set(), replacedBases: new Set(), bundleAddBases: new Set(), hasWargear: false },
     lord, mkEntry(lord, null)).includes('stat-override'),
   'an entry with no enhancement renders the printed profile');

// A multi-model-group unit on the per-model-group table falls to the asterisk.
const twoGroup = Object.assign({}, lord, { model_groups: [{ model_group: 'A' }, { model_group: 'B' }] });
const twoHtml = E.buildWeaponTable('Melee Weapons', [wMelee], 'configured',
  { activeBases: new Set(), replacedBases: new Set(), bundleAddBases: new Set(), hasWargear: false }, twoGroup, lordEntry);
ok(twoHtml.includes('stat-asterisk') && !twoHtml.includes('stat-override'),
   'a non-single model group takes the asterisk, never a value');

console.log(fail === 0 ? 'all B99 checks pass' : `b99_check: ${fail} failed`);
process.exit(fail === 0 ? 0 : 1);
