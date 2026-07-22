// required_size_check.js — B34 Piece 2. Loads the real loRollup out of index.html
// and proves the exact-match size gate on the two size-gated options in
// unit_loadouts.json: Wolf Scouts (000004182) at bracket 12, Blightlord
// Terminators (000001372) at bracket 3. At every non-matching bracket, the
// option must be inert (source weapon intact, replacement not emitted) even if
// the saved list has a stale countBy pick. At the matching bracket, the option
// must fire (source consumed, replacement emitted).
// Build-time only; not part of the served app.
// Usage: node required_size_check.js index.html unit_loadouts.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const rollup = slice(lines, 'function loMaxCount', '// Unit Options UI for loadout-defined units.');
  const prelude = `const PROFILE_SEP=/\\s[\\u2013\\-\\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}
let weaponAbilitiesLookup={};`;
  return new Function(prelude + rollup + '\nreturn {loRollup};')();
}

const E = loadEngine(process.argv[2]);
const L = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };

// Build a selection object with a stale pick on the size-gated option.
const selWithPick = (optId) => ({
  choiceById: {},
  countById: { [optId]: 1 },
  addById: {},
});
const selEmpty = () => ({ choiceById: {}, countById: {}, addById: {} });

const get = (map, name) => Number(map.get(name) || 0);

// ── Wolf Scouts 000004182 — cnt_4, required_size = 12.
//    Bracket 6: suppressed. Bracket 12: fires.
{
  const def = L['000004182'];
  const optId = 'cnt_4';
  const src = 'Plasma pistol';
  const repl = 'Instigator bolt carbine';

  // (a) size 6 — even with a stale pick, gate must suppress.
  const r6 = E.loRollup(def, 6, selWithPick(optId));
  ok(get(r6.weapons, repl) === 0, 'Wolf Scouts @6: instigator bolt carbine not emitted despite stale pick');
  ok(get(r6.weapons, src)  >= 1, 'Wolf Scouts @6: plasma pistol survives (source not consumed)');
  ok(r6.overAllocated === false, 'Wolf Scouts @6: no over-allocation (option is inert, not spurious)');

  // (b) size 12 — empty pick, option is idle but source is intact.
  const r12idle = E.loRollup(def, 12, selEmpty());
  ok(get(r12idle.weapons, repl) === 0, 'Wolf Scouts @12: no pick means no replacement');
  ok(get(r12idle.weapons, src)  >= 1, 'Wolf Scouts @12: plasma pistol carried by default');

  // (c) size 12 — pick fires: replacement emitted, one plasma pistol consumed.
  const r12pick = E.loRollup(def, 12, selWithPick(optId));
  ok(get(r12pick.weapons, repl) === 1, 'Wolf Scouts @12: instigator bolt carbine emitted with pick');
  ok(get(r12pick.weapons, src) === get(r12idle.weapons, src) - 1,
     'Wolf Scouts @12: exactly one plasma pistol consumed by the swap');
}

// ── Blightlord Terminators 000001372 — cnt_6, required_size = 3.
//    Brackets 5 and 10: suppressed. Bracket 3: fires.
{
  const def = L['000001372'];
  const optId = 'cnt_6';
  // Compound replaces "Combi-bolter + Bubotic blade" → "Plague spewer + Close combat weapon".
  const srcA = 'Combi-bolter', srcB = 'Bubotic blade';
  const replA = 'Plague spewer', replB = 'Close combat weapon';

  for (const sz of [5, 10]) {
    const r = E.loRollup(def, sz, selWithPick(optId));
    ok(get(r.weapons, replA) === 0, `Blightlord Terminators @${sz}: plague spewer not emitted despite stale pick`);
    ok(get(r.weapons, srcA)  >= 1, `Blightlord Terminators @${sz}: combi-bolter survives (source not consumed)`);
    ok(r.overAllocated === false, `Blightlord Terminators @${sz}: no over-allocation`);
  }

  const r3idle = E.loRollup(def, 3, selEmpty());
  ok(get(r3idle.weapons, replA) === 0, 'Blightlord Terminators @3: no pick means no plague spewer');
  ok(get(r3idle.weapons, srcA)  >= 1, 'Blightlord Terminators @3: combi-bolter carried by default');

  const r3pick = E.loRollup(def, 3, selWithPick(optId));
  ok(get(r3pick.weapons, replA) === 1, 'Blightlord Terminators @3: plague spewer emitted with pick');
  ok(get(r3pick.weapons, srcA) === get(r3idle.weapons, srcA) - 1,
     'Blightlord Terminators @3: exactly one combi-bolter consumed');
  ok(get(r3pick.weapons, srcB) === get(r3idle.weapons, srcB) - 1,
     'Blightlord Terminators @3: exactly one bubotic blade consumed');
}

console.log(fail === 0 ? '\nall required_size checks pass' : `\n${fail} required_size checks FAILED`);
process.exit(fail === 0 ? 0 : 1);
