// e21b_check.js — E21b (D204 ruling 2). Loads the real effectiveUnitType helper,
// the real unit-limit block and the real groupByType out of index.html and drives
// them against the real detachment_effects.json table.
//
// The claim under test is that a detachment-granted BATTLELINE keyword is a LIVE
// status derived from the current selection, never a property stamped on the unit
// record. Four behaviours carry that claim, and all four are executed rather than
// described:
//
//   1. elevation ON      — a named unit reports Battleline while its detachment is
//                          selected, and is grouped under Battleline
//   2. elevation OFF     — deselecting restores the unit's own type, its own group
//                          and its own cap, with no cleanup pass
//   3. union             — a unit named by ANY selected detachment is elevated
//                          (D203, unchanged by D204)
//   4. the doubled cap   — instanceLimit doubles for the elevated unit at both
//                          battle sizes, and the record is NOT mutated on the way
//
// Behaviour 2 is the one worth the harness. Stamping unit_type would pass every
// on-state test and fail only after a deselect, which is exactly the kind of bug
// that ships.
//
// Build-time only; not part of the served app.
// Usage: node e21b_check.js index.html detachment_effects.json units.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path, effects) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const body = [
    slice(lines, '// ── E21b: effective unit type', '// ── E21b block end'),
    slice(lines, '  const TYPE_ORDER = [', '// D115 — the unit limit depends'),
    slice(lines, '// D115 — the unit limit depends', '// State'),
    slice(lines, '  function groupByType(items, nameKey)', '  // B35 / D108.'),
  ].join('\n');

  const prelude = 'let POINTS_CAP = 2000; let detachmentEffects = EFFECTS; '
                + 'let selectedDetachments = [];\n';
  const exports = '\nreturn { effectiveUnitType, detachmentBattlelineNames, instanceLimit, '
                + 'unitLimit, groupByType, TYPE_ORDER, '
                + 'select: (d) => { selectedDetachments = d; }, '
                + 'setCap: (p) => { POINTS_CAP = p; }, '
                + 'sel: () => selectedDetachments };';
  return new Function('EFFECTS', prelude + body + exports)(effects);
}

const idxPath = process.argv[2] || 'index.html';
const effPath = process.argv[3] || 'detachment_effects.json';
const uniPath = process.argv[4] || 'units.json';

const EFF = JSON.parse(fs.readFileSync(effPath, 'utf8')).effects;
const U   = JSON.parse(fs.readFileSync(uniPath, 'utf8'));
const E   = loadEngine(idxPath, EFF);

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };

// ── fixtures, resolved out of the real data ──────────────────────────────────
const blocks = {};
U.forEach(b => { blocks[b.army] = b.units; });
const find = (army, name) => {
  const u = (blocks[army] || []).find(x => x.unit_name === name);
  if (!u) throw new Error(`fixture missing: ${army} / ${name}`);
  return { unit_id: u.unit_id, unit_name: u.unit_name, unit_type: u.unit_type, limitOverride: null };
};

const K_COH  = 'Dark Angels|COMPANY OF HUNTERS';       // elevates Outrider Squad
const K_SHAM = 'Death Guard|SHAMBLEROT VECTORIUM';     // elevates Poxwalkers
const K_LOST = 'Blood Angels|THE LOST BRETHREN';       // elevates both Death Company units
const K_NONE = 'Death Guard|TALLYBAND SUMMONERS';      // a real key with NO battleline row

const OUTRIDER = find('Adeptus Astartes', 'Outrider Squad');   // own type: Mounted
const POXWALK  = find('Death Guard', 'Poxwalkers');            // own type: Infantry
const DCM      = find('Blood Angels', 'Death Company Marines');
const INTERC   = find('Adeptus Astartes', 'Intercessor Squad');// a real Battleline control
const APOTH    = find('Adeptus Astartes', 'Apothecary Biologis'); // a Character control

// The table has to be worth reading before the helper is worth testing: an effect
// naming a unit that is ALREADY Battleline would be a silent no-op.
console.log('the table earns its keep');
ok(OUTRIDER.unit_type === 'Mounted',  'Outrider Squad\'s own type is Mounted, so the elevation is observable');
ok(POXWALK.unit_type === 'Infantry',  'Poxwalkers\' own type is Infantry');
ok(DCM.unit_type === 'Infantry',      'Death Company Marines\' own type is Infantry');
ok(EFF[K_NONE] && !(EFF[K_NONE].effects || []).some(e => e.kind === 'battleline'),
   'Tallyband Summoners is a real key carrying no battleline row (the negative control)');

// ── 1. elevation ON ──────────────────────────────────────────────────────────
console.log('\n1 — elevation while the detachment is selected');
E.select([K_COH]);
ok(E.effectiveUnitType(OUTRIDER, E.sel()) === 'Battleline', 'Outrider Squad reads Battleline under Company of Hunters');
ok(OUTRIDER.unit_type === 'Mounted',                        'and its unit_type on the record is untouched');
ok(E.effectiveUnitType(INTERC, E.sel()) === 'Battleline',   'a natively Battleline unit is unaffected');
ok(E.effectiveUnitType(APOTH, E.sel()) === 'Character',     'an unnamed unit keeps its own type');
ok(E.effectiveUnitType(POXWALK, E.sel()) === 'Infantry',    'another detachment\'s named unit is NOT elevated');

console.log('   grouping follows the effective type');
{
  const g = E.groupByType([OUTRIDER, INTERC, APOTH], 'unit_name');
  const bl = g.find(x => x.type === 'Battleline');
  ok(!!bl && bl.items.some(i => i.unit_name === 'Outrider Squad'), 'Outrider Squad renders under Battleline');
  ok(!g.some(x => x.type === 'Mounted'),                           'and the Mounted group is gone entirely');
  ok(E.TYPE_ORDER.indexOf('Battleline') < E.TYPE_ORDER.indexOf('Mounted'), 'Battleline sorts ahead of Mounted');
}

// ── 2. elevation OFF ─────────────────────────────────────────────────────────
console.log('\n2 — deselect restores everything, with no cleanup pass');
E.select([]);
ok(E.effectiveUnitType(OUTRIDER, E.sel()) === 'Mounted', 'Outrider Squad is Mounted again with nothing selected');
{
  const g = E.groupByType([OUTRIDER, INTERC], 'unit_name');
  const mt = g.find(x => x.type === 'Mounted');
  const bl = g.find(x => x.type === 'Battleline');
  ok(!!mt && mt.items.some(i => i.unit_name === 'Outrider Squad'), 'it renders under Mounted again');
  ok(!!bl && !bl.items.some(i => i.unit_name === 'Outrider Squad'), 'and no longer under Battleline');
}
E.select([K_NONE]);
ok(E.effectiveUnitType(OUTRIDER, E.sel()) === 'Mounted', 'selecting a detachment with no battleline row elevates nothing');
E.select([K_COH]);
ok(E.effectiveUnitType(OUTRIDER, E.sel()) === 'Battleline', 'and re-selecting elevates it again — the read is live, not cached');

// ── 3. union across selected detachments ─────────────────────────────────────
// Not a legal army — these three belong to three different factions. What is
// under test is the union predicate itself, which has to hold for the two-Space-
// Marines-detachment case the app can actually reach.
console.log('\n3 — effects from multiple selected detachments union');
E.select([K_COH, K_SHAM, K_LOST]);
ok(E.effectiveUnitType(OUTRIDER, E.sel()) === 'Battleline', 'named by the first: elevated');
ok(E.effectiveUnitType(POXWALK, E.sel()) === 'Battleline',  'named by the second: elevated');
ok(E.effectiveUnitType(DCM, E.sel()) === 'Battleline',      'named by the third: elevated');
ok(E.effectiveUnitType(APOTH, E.sel()) === 'Character',     'named by none: unchanged');
ok(E.detachmentBattlelineNames(E.sel()).size === 4,         'the union names exactly the four units in the table');
E.select([K_NONE, K_COH]);
ok(E.effectiveUnitType(OUTRIDER, E.sel()) === 'Battleline', 'a no-effect key alongside an effect key does not suppress it');
ok(E.detachmentBattlelineNames([]).size === 0,              'nothing selected names nothing');
ok(E.detachmentBattlelineNames(['Nonsense|NO SUCH DETACHMENT']).size === 0, 'an unresolvable key is ignored, not thrown on');

// ── 4. the doubled cap ───────────────────────────────────────────────────────
console.log('\n4 — the unit limit follows the elevation at both battle sizes');
E.setCap(2000);
E.select([]);
ok(E.unitLimit(OUTRIDER) === 3, 'Strike Force, unelevated: 3');
E.select([K_COH]);
ok(E.unitLimit(OUTRIDER) === 6, 'Strike Force, elevated: 6');
E.setCap(1000);
ok(E.unitLimit(OUTRIDER) === 4, 'Incursion, elevated: 4');
E.select([]);
ok(E.unitLimit(OUTRIDER) === 2, 'Incursion, unelevated: 2');
ok(OUTRIDER.unit_type === 'Mounted', 'after all of the above the record still says Mounted');

// An override still wins: it is the datasheet's own printed limit and outranks
// both the battle-size table and the elevation.
E.setCap(2000);
E.select([K_COH]);
{
  const capped = Object.assign({}, OUTRIDER, { limitOverride: 1 });
  ok(E.unitLimit(capped) === 1, 'a datasheet limitOverride still beats the doubled Battleline cap');
}

// ── 5. every unit the table names resolves, and none is already Battleline ───
console.log('\n5 — the whole battleline half of the table, swept');
{
  let named = 0, unresolved = 0, noop = 0;
  for (const key of Object.keys(EFF)) {
    const rec = EFF[key];
    for (const eff of (rec.effects || [])) {
      if (eff.kind !== 'battleline') continue;
      for (const n of ((eff.target && eff.target.units) || [])) {
        named++;
        const own = (blocks[rec.army] || []).find(x => x.unit_name === n)
                 || (blocks['Adeptus Astartes'] || []).find(x => x.unit_name === n);
        if (!own) { unresolved++; console.log(`       unresolved: ${key} / ${n}`); continue; }
        if (own.unit_type === 'Battleline') { noop++; console.log(`       already Battleline: ${key} / ${n}`); }
        E.select([key]);
        if (E.effectiveUnitType({ unit_name: n, unit_type: own.unit_type }, E.sel()) !== 'Battleline') {
          fail++; console.log(`  FAIL ${key} / ${n} did not elevate`);
        }
      }
    }
  }
  ok(named === 7,       `the table names 7 units for elevation (${named})`);
  ok(unresolved === 0,  'every named unit resolves in its army\'s pool');
  ok(noop === 0,        'no effect names a unit that is already Battleline');
}

console.log(fail === 0 ? '\nall E21b checks pass' : `\n${fail} E21b check(s) FAILED`);
process.exit(fail === 0 ? 0 : 1);
