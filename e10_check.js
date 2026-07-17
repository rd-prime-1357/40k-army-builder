// e10_check.js — E10 (D148). Loads the real duplicateUnit + its dependency chain
// (getAttachedLeaders, ptsForEntry, unitLimit family) out of index.html and drives
// it against synthetic armyList scenarios: a plain unit, a unit with one non-Epic-Hero
// leader attached, a unit with an Epic Hero leader attached, and a unit already at its
// instance limit. wargearCostForEntry is stubbed to 0 (points-tier math is not what
// this checks — structural duplication + Epic Hero exclusion + limit enforcement are).
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s === -1 || e === -1) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadEngine(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const body = [
    slice(lines, 'function battleSizeUnitLimit', 'function limitState'),
    slice(lines, 'function limitState', 'function canAddUnit'),
    slice(lines, 'function canAddUnit', '// State'),
    slice(lines, 'function ptsForEntry', 'function refreshPoints'),
    slice(lines, 'function getAttachedLeaders', 'function addUnitFromRoster'),
    slice(lines, 'function duplicateUnit', '// ── Edit operations'),
  ].join('\n');

  const prelude = `
    let armyList = [];
    let allUnits = [];
    let nextId = 1;
    let selectedListId = null;
    let POINTS_CAP = 2000;
    function wargearCostForEntry() { return 0; }
    function flashBanner(msg) { flashed.push(msg); }
    let flashed = [];
    function renderAll() { /* no-op for test */ }
  `;
  return new Function(prelude + body + `
    return {
      setArmyList: (l) => { armyList = l; },
      getArmyList: () => armyList,
      setAllUnits: (u) => { allUnits = u; },
      setNextId: (n) => { nextId = n; },
      duplicateUnit,
      getFlashed: () => flashed,
    };
  `)();
}

const E = loadEngine(process.argv[2] || 'index.html');

let failures = 0;
function check(label, cond) {
  console.log(`  ${cond ? 'ok  ' : 'FAIL'} ${label}`);
  if (!cond) failures++;
}

// unit_type limits: default 3 at 2000pts, Epic Hero always 1
function unit(name, type) { return { unit_name: name, unit_type: type, sizes: [{ size: 5, first_unit: 100, second_unit: 90, third_plus: 80 }] }; }

// ── Scenario 1: plain unit, no leaders ──────────────────────────────────────
{
  E.setAllUnits([unit('Plague Marines', 'Infantry')]);
  E.setNextId(10);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: { a: 'x' }, otherOptions: {}, attachedToListId: null },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  check('scenario 1: two entries after duplicate', list.length === 2);
  const copy = list.find(e => e.listId !== 1);
  check('scenario 1: copy has new listId', copy && copy.listId === 10);
  check('scenario 1: copy inherits wargear (deep, not same ref)', copy.wargear.a === 'x' && copy.wargear !== list[0].wargear);
  check('scenario 1: copy priced as second copy (90)', copy.points === 90);
  check('scenario 1: copy not attached', copy.attachedToListId === null);
}

// ── Scenario 2: unit with one non-Epic-Hero leader attached ────────────────
{
  E.setAllUnits([unit('Plague Marines', 'Infantry'), unit('Tallyman', 'Character')]);
  E.setNextId(20);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 2, unit_name: 'Tallyman', unit_type: 'Character', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: 1 },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  check('scenario 2: four entries after duplicate (body+leader x2)', list.length === 4);
  const bodyCopy = list.find(e => e.unit_name === 'Plague Marines' && e.listId !== 1);
  const leaderCopy = list.find(e => e.unit_name === 'Tallyman' && e.listId !== 2);
  check('scenario 2: leader duplicated', !!leaderCopy);
  check('scenario 2: leader copy attached to body copy', leaderCopy && bodyCopy && leaderCopy.attachedToListId === bodyCopy.listId);
}

// ── Scenario 3: unit with an Epic Hero leader attached — NOT duplicated ────
{
  E.setAllUnits([unit('Plague Marines', 'Infantry'), unit('Typhus', 'Epic Hero')]);
  E.setNextId(30);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 2, unit_name: 'Typhus', unit_type: 'Epic Hero', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: 1 },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  check('scenario 3: only three entries (Epic Hero not duplicated)', list.length === 3);
  const epicCopies = list.filter(e => e.unit_name === 'Typhus');
  check('scenario 3: still exactly one Typhus', epicCopies.length === 1);
  const bodyCopy = list.find(e => e.unit_name === 'Plague Marines' && e.listId !== 1);
  check('scenario 3: body copy has no leader attached to it', !list.some(e => e.attachedToListId === bodyCopy.listId));
}

// ── Scenario 4: unit already at its instance limit — duplicate refused ─────
{
  E.setAllUnits([unit('Plague Marines', 'Infantry')]);
  E.setNextId(40);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 2, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 90, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 3, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 80, wargear: {}, otherOptions: {}, attachedToListId: null },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  check('scenario 4: refused at limit (still 3 entries)', list.length === 3);
  check('scenario 4: banner shown', E.getFlashed().length === 1 && E.getFlashed()[0].includes('Limit reached'));
}

// ── Scenario 5: Epic Hero leader already at its own limit (1) elsewhere ────
// duplicating the SECOND copy of a bodyguard whose leader is a non-Epic-Hero already
// at that leader's own instance limit — leader copy silently skipped, body still copies.
{
  E.setAllUnits([unit('Plague Marines', 'Infantry'), unit('Foul Blightspawn', 'Character')]);
  E.setNextId(50);
  E.setArmyList([
    { listId: 1, unit_name: 'Plague Marines', unit_type: 'Infantry', sizeIdx: 0, god: null, points: 100, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 2, unit_name: 'Foul Blightspawn', unit_type: 'Character', sizeIdx: 0, god: null, points: 60, wargear: {}, otherOptions: {}, attachedToListId: 1 },
    { listId: 3, unit_name: 'Foul Blightspawn', unit_type: 'Character', sizeIdx: 0, god: null, points: 60, wargear: {}, otherOptions: {}, attachedToListId: null },
    { listId: 4, unit_name: 'Foul Blightspawn', unit_type: 'Character', sizeIdx: 0, god: null, points: 60, wargear: {}, otherOptions: {}, attachedToListId: null },
  ]);
  E.duplicateUnit(1);
  const list = E.getArmyList();
  const bodyCopy = list.find(e => e.unit_name === 'Plague Marines' && e.listId !== 1);
  check('scenario 5: body still copies despite leader being at its own limit', !!bodyCopy);
  check('scenario 5: leader copy silently skipped (still only 3 Foul Blightspawn)', list.filter(e => e.unit_name === 'Foul Blightspawn').length === 3);
  check('scenario 5: body copy left with no leader attached', !list.some(e => e.attachedToListId === bodyCopy.listId));
}

console.log(failures === 0 ? '\nall E10 checks pass' : `\n${failures} E10 check(s) FAILED`);
process.exit(failures === 0 ? 0 : 1);
