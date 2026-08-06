// b101_check.js — B101. "You cannot select the same option more than once."
//
// loMaxCount caps how MANY picks a replacement_choices option takes; before v6.17
// nothing anywhere enforced that the picks DIFFER. Under D0 a duplicate on such an
// option has to be unreachable, not flagged, which means the ceiling must hold at
// three independent places — otherwise the one that is missing becomes the hole:
//
//   1. the selection path  (editLoadoutChoiceCount) — the source of truth for state
//   2. the renderer        (loChoiceGroupCap / loDistinctCap driving the stepper)
//   3. the rollup          (loRollup) — a list saved before the flag existed, or
//                           edited in storage, must not roll up illegal weapons or
//                           their points
//
// Both rollup branches are covered: the fixed-1 model group (a Sergeant/Champion
// scope) and the multi-model body group. They are separate code paths and a fix to
// one has historically not implied the other.
//
// The fixtures here are synthetic on purpose. No shipped unit carries distinct: true
// yet — the three live Chaos Space Marines cases and the two Grey Knights Nemesis
// Dreadknights all wait on a parser fix and a data regeneration. Pinning the engine
// against real data would therefore pin nothing today, and the assertion would only
// start meaning something at the moment the data landed, which is exactly backwards.
//
// Build-time only; not part of the served app.
// Usage: node b101_check.js [index.html]

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
  const editor = slice(lines, 'function editLoadoutChoiceCount', 'function editLoadoutAdd');
  const prelude = `const PROFILE_SEP=/\\s[\u2013\\-\u00e2]\\s/;
function stripProfile(n){return String(n||'').split(PROFILE_SEP)[0].trim();}
function weaponBase(n){return stripProfile(n).toLowerCase();}
let wargearPoints = {};
let armyList = [];
function renderAll(){}`;
  return new Function(prelude + rollup + '\n' + editor +
    '\nreturn { loRollup, loMaxCount, loDistinctCap, loChoiceGroupCap, loDistinctPicks,' +
    ' editLoadoutChoiceCount, setList:(l)=>{armyList=l;}, getList:()=>armyList };')();
}

const E = loadEngine(process.argv[2] || 'index.html');

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };
const eq = (msg, got, want) => ok(got === want, `${msg}: got ${JSON.stringify(got)} want ${JSON.stringify(want)}`);

// ── fixtures ───────────────────────────────────────────────────────────────
// Shape of the real Raptors option: a body group, up to 2 of 3, no duplicates.
const CHOICES3 = ['Flamer', 'Meltagun', 'Plasma gun'];
const bodyDef = (extra) => ({
  size_brackets: [5, 10],
  model_groups: [
    { name: 'Champion', count: { fixed: 1 }, default_weapons: ['Bolt pistol', 'Chainsword'] },
    { name: 'Troopers', count: { fills_to_size: true, min: 4 }, default_weapons: ['Bolt pistol', 'Chainsword'] }
  ],
  options: [Object.assign({
    id: 'cc_x', scope: 'Troopers', group: 'Chainsword Options', type: 'count',
    replaces: 'Chainsword', replacement_choices: CHOICES3.slice(),
    max_total_all: true, up_to: 2
  }, extra || {})]
});
// Same option parked on a fixed-1 group — the other rollup branch entirely.
const leaderDef = (extra) => ({
  size_brackets: [5],
  model_groups: [
    { name: 'Champion', count: { fixed: 1 }, default_weapons: ['Bolt pistol', 'Chainsword'] },
    { name: 'Troopers', count: { fills_to_size: true, min: 4 }, default_weapons: ['Bolt pistol', 'Chainsword'] }
  ],
  options: [Object.assign({
    id: 'cc_l', scope: 'Champion', group: 'Chainsword Options', type: 'count',
    replaces: 'Chainsword', replacement_choices: CHOICES3.slice(),
    max_total_all: true, up_to: 2
  }, extra || {})]
});
const sel = (counts) => ({ choiceById: {}, countById: counts || {}, addById: {} });
const w = (roll, name) => roll.weapons.get(name) || 0;

// ── 1. the two helpers, directly ───────────────────────────────────────────
console.log('B101 — per-choice and group ceilings');
eq('distinct option caps each choice at 1', E.loDistinctCap({ distinct: true }), 1);
ok(E.loDistinctCap({}) === Infinity, 'a plain option has no per-choice cap');
ok(E.loDistinctCap(null) === Infinity, 'a missing option has no per-choice cap');
eq('group cap shrinks to the number of listed choices',
   E.loChoiceGroupCap({ distinct: true, replacement_choices: ['a', 'b'] }, 5), 2);
eq('group cap is untouched when the cap already binds',
   E.loChoiceGroupCap({ distinct: true, replacement_choices: ['a', 'b', 'c'] }, 2), 2);
eq('group cap is untouched on a non-distinct option',
   E.loChoiceGroupCap({ replacement_choices: ['a', 'b'] }, 5), 5);

// ── 2. selection path: the duplicate is refused, not stored ────────────────
console.log('B101 — the selection path refuses a second pick of the same choice');
{
  const entry = { listId: 1, wargear: {} };
  E.setList([entry]);
  E.editLoadoutChoiceCount(1, 'cc_x', 'Flamer', 1, 2, 1);
  eq('first Flamer is taken', entry.wargear.cc_x.Flamer, 1);
  E.editLoadoutChoiceCount(1, 'cc_x', 'Flamer', 1, 2, 1);
  eq('second Flamer is refused', entry.wargear.cc_x.Flamer, 1);
  E.editLoadoutChoiceCount(1, 'cc_x', 'Meltagun', 1, 2, 1);
  eq('a DIFFERENT choice is still allowed', entry.wargear.cc_x.Meltagun, 1);
  E.editLoadoutChoiceCount(1, 'cc_x', 'Plasma gun', 1, 2, 1);
  ok(!entry.wargear.cc_x['Plasma gun'], 'a third pick is refused — the group cap still binds');
  E.editLoadoutChoiceCount(1, 'cc_x', 'Flamer', -1, 2, 1);
  ok(!entry.wargear.cc_x.Flamer, 'clearing a pick is always allowed');
  E.editLoadoutChoiceCount(1, 'cc_x', 'Plasma gun', 1, 2, 1);
  eq('the freed slot can then be spent on something else', entry.wargear.cc_x['Plasma gun'], 1);
}
console.log('B101 — a non-distinct option is unaffected by the new argument');
{
  const entry = { listId: 1, wargear: {} };
  E.setList([entry]);
  // No perMax argument at all — exactly how every pre-existing caller invokes it.
  E.editLoadoutChoiceCount(1, 'cc_x', 'Flamer', 1, 3);
  E.editLoadoutChoiceCount(1, 'cc_x', 'Flamer', 1, 3);
  eq('duplicates still allowed with no per-choice cap', entry.wargear.cc_x.Flamer, 2);
  E.editLoadoutChoiceCount(1, 'cc_x', 'Flamer', 1, 3);
  eq('and the group cap alone stops it at 3', entry.wargear.cc_x.Flamer, 3);
  E.editLoadoutChoiceCount(1, 'cc_x', 'Meltagun', 1, 3);
  ok(!entry.wargear.cc_x.Meltagun, 'group cap blocks a further pick of any kind');
}

// ── 3. rollup, body group: a stale duplicate cannot survive a reload ───────
console.log('B101 — rollup clamps a stale duplicate on a body group');
{
  const def = bodyDef({ distinct: true });
  // A saved list that asked for two Flamers. Legal total (2), illegal distribution.
  const r = E.loRollup(def, 10, sel({ cc_x: { Flamer: 2 } }));
  eq('only one Flamer survives', w(r, 'Flamer'), 1);
  eq('the second slot is NOT silently spent elsewhere', w(r, 'Meltagun'), 0);
  // 9 body Chainswords, one consumed -> 8 remain, plus the Champion's = 9.
  eq('exactly one Chainsword was consumed', w(r, 'Chainsword'), 9);
}
{
  const def = bodyDef({ distinct: true });
  const r = E.loRollup(def, 10, sel({ cc_x: { Flamer: 1, Meltagun: 1 } }));
  eq('two different picks both survive (Flamer)', w(r, 'Flamer'), 1);
  eq('two different picks both survive (Meltagun)', w(r, 'Meltagun'), 1);
  eq('two Chainswords consumed', w(r, 'Chainsword'), 8);
}
{
  const def = bodyDef({ distinct: true });
  // Three distinct picks against up_to 2 — the total ceiling still binds, and it
  // truncates in the option's own choice order rather than storage order.
  const r = E.loRollup(def, 10, sel({ cc_x: { 'Plasma gun': 1, Meltagun: 1, Flamer: 1 } }));
  eq('total across distinct picks is capped at up_to', w(r, 'Flamer') + w(r, 'Meltagun') + w(r, 'Plasma gun'), 2);
  eq('truncation follows the option choice order — Flamer kept', w(r, 'Flamer'), 1);
  eq('truncation follows the option choice order — Meltagun kept', w(r, 'Meltagun'), 1);
  eq('truncation follows the option choice order — Plasma gun dropped', w(r, 'Plasma gun'), 0);
}
{
  // Fewer choices than the cap: the option can never reach up_to, and must not
  // manufacture a pick to get there.
  const def = bodyDef({ distinct: true, replacement_choices: ['Flamer', 'Meltagun'], up_to: 3 });
  const r = E.loRollup(def, 10, sel({ cc_x: { Flamer: 3, Meltagun: 3 } }));
  eq('capped by the number of listed choices', w(r, 'Flamer') + w(r, 'Meltagun'), 2);
}

// ── 4. rollup, fixed-1 group: the other branch, same rule ─────────────────
console.log('B101 — rollup clamps a stale duplicate on a fixed-1 group');
{
  const def = leaderDef({ distinct: true });
  const r = E.loRollup(def, 5, sel({ cc_l: { Flamer: 2 } }));
  eq('only one Flamer survives on the leader', w(r, 'Flamer'), 1);
  // The Champion carries one Chainsword and it is consumed; 4 Troopers keep theirs.
  eq('the leader Chainsword is consumed exactly once', w(r, 'Chainsword'), 4);
  ok(!r.overAllocated, 'a clamped duplicate is corrected, not reported as over-allocation');
}
{
  const def = leaderDef({ distinct: true });
  const r = E.loRollup(def, 5, sel({ cc_l: { Flamer: 1, Meltagun: 1, 'Plasma gun': 1 } }));
  eq('a fixed-1 group cannot exceed its one model', w(r, 'Flamer') + w(r, 'Meltagun') + w(r, 'Plasma gun'), 1);
}

// ── 5. non-distinct rollup behaviour is byte-for-byte unchanged ────────────
console.log('B101 — options without the flag behave exactly as before');
{
  const def = bodyDef();      // no distinct
  const r = E.loRollup(def, 10, sel({ cc_x: { Flamer: 2 } }));
  eq('a plain option still allows two of the same choice', w(r, 'Flamer'), 2);
  eq('and consumes two Chainswords', w(r, 'Chainsword'), 8);
}
{
  const def = leaderDef();    // no distinct, fixed-1
  const r = E.loRollup(def, 5, sel({ cc_l: { Flamer: 2 } }));
  eq('fixed-1 plain option is bounded by the group, not by distinctness', w(r, 'Flamer'), 1);
}

console.log(fail === 0 ? 'all B101 checks pass' : `b101_check: ${fail} FAILED`);
process.exit(fail === 0 ? 0 : 1);
