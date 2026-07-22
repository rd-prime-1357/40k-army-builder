// limit_check.js — B41 + E3 + D115. Loads the real instanceLimit / limitState / canAddUnit
// out of index.html and asserts the datasheet-limit block: the limits track the BATTLE SIZE
// (Army_Muster_Rules.txt 25.03), the add is refused AT the limit, the roster badge reddens
// only PAST it, and every unit_type in units.json maps to a limit.
// Build-time only; not part of the served app.
// Usage: node limit_check.js index.html units.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const src = slice(lines, '// D115 — the unit limit depends', '// State');
  return new Function('let POINTS_CAP = 2000;\n' + src +
    '\nreturn { battleSizeUnitLimit, instanceLimit, unitLimit, limitState, canAddUnit,' +
    ' setCap: (p) => { POINTS_CAP = p; } };')();
}

const E = loadEngine(process.argv[2]);
const U = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };

// ── D115. The limits come from Army_Muster_Rules.txt 25.03 "Select Battle Size":
//    Unit Limit 2 at INCURSION (1000), 3 at STRIKE FORCE (2000). Footnote: Battleline and
//    Dedicated Transport are DOUBLE that; every Epic Hero is 1 regardless of battle size.
console.log('D115 — STRIKE FORCE (2000 pts): 3 / 6 / 1');
ok(E.battleSizeUnitLimit(2000) === 2 + 1,             'Strike Force base unit limit is 3');
ok(E.instanceLimit('Epic Hero', 2000) === 1,          'Epic Hero limit is 1');
ok(E.instanceLimit('Battleline', 2000) === 6,         'Battleline is double: 6');
ok(E.instanceLimit('Dedicated Transport', 2000) === 6,'Dedicated Transport is double: 6');
for (const t of ['Character', 'Infantry', 'Mounted', 'Beast', 'Monster', 'Vehicle', 'Fortification', 'Allied']) {
  ok(E.instanceLimit(t, 2000) === 3, `${t} limit is 3`);
}

console.log('D115 — INCURSION (1000 pts): 2 / 4 / 1');
ok(E.battleSizeUnitLimit(1000) === 2,                 'Incursion base unit limit is 2');
ok(E.instanceLimit('Epic Hero', 1000) === 1,          'Epic Hero is 1 REGARDLESS of battle size');
ok(E.instanceLimit('Battleline', 1000) === 4,         'Battleline is double: 4');
ok(E.instanceLimit('Dedicated Transport', 1000) === 4,'Dedicated Transport is double: 4');
for (const t of ['Character', 'Infantry', 'Vehicle']) {
  ok(E.instanceLimit(t, 1000) === 2, `${t} limit is 2 at Incursion`);
}

// The bug D115 fixes: v5.61 applied the Strike Force row at both battle sizes, so a third
// Captain was accepted in a 1000-point list. It must now be refused.
console.log('D115 — the v5.61 bug: a third Captain at Incursion');
ok(E.canAddUnit(2, E.instanceLimit('Character', 1000)) === false,
   'third Character REFUSED at Incursion (v5.61 wrongly allowed it)');
ok(E.canAddUnit(2, E.instanceLimit('Character', 2000)) === true,
   'third Character allowed at Strike Force');

// unitLimit() reads POINTS_CAP live, so changing battle size cannot leave a stale limit.
console.log('D115 — unitLimit tracks POINTS_CAP live');
const cap = { unit_type: 'Battleline', limitOverride: null };
E.setCap(2000); ok(E.unitLimit(cap) === 6, 'Battleline reads 6 at Strike Force');
E.setCap(1000); ok(E.unitLimit(cap) === 4, 'same object reads 4 after switching to Incursion');
E.setCap(2000);
ok(E.unitLimit({ unit_type: 'Infantry', limitOverride: 1 }) === 1, 'an explicit override still wins');

// ── B41: the add is refused at the limit, not accepted and flagged. ───────────
console.log('B41 — add refused at the limit');
ok(E.canAddUnit(0, 1) === true,  'Epic Hero: first copy allowed');
ok(E.canAddUnit(1, 1) === false, 'Epic Hero: second copy refused');
ok(E.canAddUnit(2, 3) === true,  'standard: third copy allowed');
ok(E.canAddUnit(3, 3) === false, 'standard: fourth copy refused');
ok(E.canAddUnit(5, 6) === true,  'Battleline: sixth copy allowed');
ok(E.canAddUnit(6, 6) === false, 'Battleline: seventh copy refused');

// ── E3: red means exceeded, never merely reached. ─────────────────────────────
console.log('E3 — badge state');
ok(E.limitState(0, 3) === 'ok',   '0 of 3 is ok');
ok(E.limitState(2, 3) === 'ok',   '2 of 3 is ok');
ok(E.limitState(3, 3) === 'at',   '3 of 3 is at-limit, not over');
ok(E.limitState(4, 3) === 'over', '4 of 3 is over');
ok(E.limitState(1, 1) === 'at',   'Epic Hero 1 of 1 is at-limit, not over');
ok(E.limitState(2, 1) === 'over', 'Epic Hero 2 of 1 is over');

// An over-limit count is still reachable from an imported or pre-v5.61 saved list,
// so 'over' must remain an error state rather than being treated as unreachable.
ok(E.limitState(7, 6) === 'over', 'legacy list past a Battleline limit still errors');

// ── Every unit_type actually present in the data resolves to a positive limit. ─
console.log('data — every unit_type has a limit');
const types = new Set();
for (const b of U) for (const u of b.units) types.add(u.unit_type);
let bad = [];
for (const t of types) {
  for (const pts of [1000, 2000]) {
    const l = E.instanceLimit(t, pts);
    if (!(l > 0)) bad.push(`${t} @ ${pts}`);
  }
}
ok(bad.length === 0, `all ${types.size} unit_types in units.json map to a limit${bad.length ? ' — missing: ' + bad.join(', ') : ''}`);

// Any unit carrying an explicit override must still be a positive integer.
const badOv = [];
for (const b of U) for (const u of b.units) {
  if (u.instance_limit_override != null && !(Number.isInteger(u.instance_limit_override) && u.instance_limit_override > 0)) {
    badOv.push(u.unit_name);
  }
}
ok(badOv.length === 0, `instance_limit_override, where present, is a positive integer${badOv.length ? ' — bad: ' + badOv.join(', ') : ''}`);

console.log(fail === 0 ? '\nall limit checks pass' : `\n${fail} limit check(s) FAILED`);
process.exit(fail === 0 ? 0 : 1);
