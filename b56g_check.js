// b56g_check.js — B56g phase 3. Loads loGroupCounts / modelGroupCost straight out of
// index.html and proves the Hunting Wolves escort (Wolf Guard Headtakers, 000004131) is
// reachable as a 0-or-N toggle in all four printed configurations, at both copy-tiers:
//   3 Headtakers alone, 3 Headtakers + 3 Wolves, 6 Headtakers alone, 6 Headtakers + 6 Wolves.
// Checks model counts and the added points (10 pts/wolf) — not the Headtaker base price,
// which b56g_headtaker_escort (rules_assertions.py) already covers on the data side.
// Usage: node b56g_check.js index.html unit_loadouts.json
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

const indexPath = process.argv[2] || 'index.html';
const loadoutsPath = process.argv[3] || 'unit_loadouts.json';
const lines = fs.readFileSync(indexPath, 'utf8').split('\n');
const block = slice(lines, 'function modelGroupCost', 'function ptsForEntry')
  + '\n' + slice(lines, 'function loOptCounts', 'requires_weapon: carrier counting');
const { loGroupCounts, modelGroupCost } = new Function(
  block + '\nreturn {loGroupCounts, modelGroupCost};'
)();

const loadouts = JSON.parse(fs.readFileSync(loadoutsPath, 'utf8'));
const def = loadouts['000004131'];
if (!def) { console.error('Wolf Guard Headtakers (000004131) missing from unit_loadouts.json'); process.exit(1); }

let pass = 0, fail = 0;
function check(label, got, want) {
  const g = JSON.stringify(got), w = JSON.stringify(want);
  if (g === w) { pass++; }
  else { fail++; console.error(`FAIL ${label}: expected ${w}, got ${g}`); }
}

const cases = [
  { size: 3, on: false, wantCounts: { 'Wolf Guard Headtakers': 3, 'Hunting Wolves': 0 }, wantCost: 0 },
  { size: 3, on: true,  wantCounts: { 'Wolf Guard Headtakers': 3, 'Hunting Wolves': 3 }, wantCost: 30 },
  { size: 6, on: false, wantCounts: { 'Wolf Guard Headtakers': 6, 'Hunting Wolves': 0 }, wantCost: 0 },
  { size: 6, on: true,  wantCounts: { 'Wolf Guard Headtakers': 6, 'Hunting Wolves': 6 }, wantCost: 60 },
];

for (const c of cases) {
  const optCounts = { 'Hunting Wolves': c.on ? 1 : 0 };
  const counts = loGroupCounts(def, c.size, optCounts);
  const label = `size ${c.size} escort ${c.on ? 'on' : 'off'}`;
  check(`${label} model counts`, counts, c.wantCounts);
  check(`${label} escort points`, modelGroupCost(def, c.size, optCounts), c.wantCost);
}

// Toggle defaults to off with no optCounts supplied at all (matches a freshly added entry).
check('default (no optCounts) size 3', loGroupCounts(def, 3, {})['Hunting Wolves'], 0);
check('default (no optCounts) size 6', loGroupCounts(def, 6, {})['Hunting Wolves'], 0);

console.log(`b56g_check: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
