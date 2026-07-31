// b72_check.js — locks two engine fixes shipped S169 (v6.12).
//
// B72: the Invader ATV is a non_consuming optional model group on the Outrider
// Squad (unit_id 000002712). It rides alongside the size bracket, so it must be
// offerable at EVERY legal squad size, not only at 6. Before the fix loOptMax
// applied the headroom clamp to it; headroom is 0 for the 3-model bracket
// (sergeant 1 + fill min 2 = 3), so the ATV read as "no models left" and the
// stepper hid it. The fix exempts non_consuming groups from the clamp, matching
// the exemption loGroupCounts and loOptHeadroom already carry. This is D0-facing:
// a legal option must be reachable. The ATV is the only non_consuming optional
// group in the data, so this is the unit that exercises the path.
//
// B80: the combined attached-unit popup renders buildModalConfigured twice
// (leader, then bodyguard). Its collapsible sections must carry per-member IDs,
// or getElementById returns the first match and the bodyguard's chevron toggles
// the leader's section. Static guard: buildModalConfigured must scope its section
// IDs through idScope, and the combined caller must pass distinct scopes.
//
// Usage: node b72_check.js index.html unit_loadouts.json
const fs = require('fs');
const src = fs.readFileSync(process.argv[2] || 'index.html', 'utf8');
const lines = src.split('\n');
function slice(a, b) {
  const s = lines.findIndex(l => l.includes(a));
  const e = lines.findIndex((l, i) => i > s && l.includes(b));
  return lines.slice(s, e).join('\n');
}

let pass = 0, fail = 0;
function check(label, got, want) {
  const ok = JSON.stringify(got) === JSON.stringify(want);
  if (ok) pass++; else { fail++; console.log('FAIL', label, 'got', JSON.stringify(got), 'want', JSON.stringify(want)); }
}
function assert(label, cond) {
  if (cond) pass++; else { fail++; console.log('FAIL', label); }
}

// ── B72: Invader ATV reachable at every legal Outrider Squad size ──
const block = slice('function loOptCounts', 'requires_weapon: carrier counting');
const E = new Function(block + '\nreturn {loOptCounts,loOptHeadroom,loOptMax,loGroupCounts};')();
const L = JSON.parse(fs.readFileSync(process.argv[3] || 'unit_loadouts.json', 'utf8'));
const OUTRIDER = '000002712';
const def = L[OUTRIDER];
assert('Outrider Squad loadout present', !!def);

// The ATV must be offerable at both brackets (this is the regression B72 fixes).
check('ATV offerable @3', E.loOptMax(def, 3, {}, 'Invader ATV'), 1);
check('ATV offerable @6', E.loOptMax(def, 6, {}, 'Invader ATV'), 1);

// Taking the ATV must NOT reduce the Outrider body (it rides alongside the
// bracket). Body stays at fill for the size; sergeant fixed at 1; ATV at 1.
{
  const c3 = E.loGroupCounts(def, 3, { 'Invader ATV': 1 });
  check('@3 sergeant', c3['Outrider Sergeant'], 1);
  check('@3 outriders (fill, undisturbed)', c3['Outriders'], 2);
  check('@3 ATV', c3['Invader ATV'], 1);
}
{
  const c6 = E.loGroupCounts(def, 6, { 'Invader ATV': 1 });
  check('@6 sergeant', c6['Outrider Sergeant'], 1);
  check('@6 outriders (fill, undisturbed)', c6['Outriders'], 5);
  check('@6 ATV', c6['Invader ATV'], 1);
}
// Band cap still holds — never more than one ATV.
check('ATV band cap @6', E.loGroupCounts(def, 6, { 'Invader ATV': 5 })['Invader ATV'], 1);

// ── B80: combined-popup section IDs are per-member, not shared ──
const cfgFn = slice('function buildModalConfigured', 'Shared modal helpers');
assert('buildModalConfigured takes idScope', /function buildModalConfigured\([^)]*idScope[^)]*\)/.test(cfgFn));
assert('buildModalConfigured derives sidBase from idScope', /sidBase\s*=\s*'cfg'\s*\+\s*\(idScope/.test(cfgFn));
assert('abilities section scoped', /sidBase\s*\+\s*'-abilities'/.test(cfgFn));
assert('rules section scoped', /sidBase\s*\+\s*'-rules'/.test(cfgFn));
assert('wargear-abilities section scoped', /sidBase\s*\+\s*'-wargear-abilities'/.test(cfgFn));
assert('leader section scoped', /leaderSectionHtml\(raw,\s*sidBase\)/.test(cfgFn));
// No bare 'cfg-...' literal may remain in the function — that is the collision.
assert("no bare 'cfg-abilities' literal", !/'cfg-abilities'/.test(cfgFn));
assert("no bare 'cfg-rules' literal", !/'cfg-rules'/.test(cfgFn));
assert("no bare 'cfg-wargear-abilities' literal", !/'cfg-wargear-abilities'/.test(cfgFn));

const combFn = slice('function buildModalCombined', 'function closeModal');
// Both members must pass an idScope, and the two must be distinct (built from
// each member's own listId).
assert('combined leader passes listId scope', /buildModalConfigured\(lraw,\s*leader,[^)]*leader\.listId/.test(combFn));
assert('combined bodyguard passes listId scope', /buildModalConfigured\(bgRaw,\s*bodyguard,[^)]*bodyguard\.listId/.test(combFn));

if (fail === 0) console.log('all B72/B80 checks pass (' + pass + ')');
else console.log(fail + ' FAILED, ' + pass + ' passed');
process.exit(fail === 0 ? 0 : 1);
