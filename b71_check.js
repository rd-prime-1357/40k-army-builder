// b71_check.js — B71. Loads the real B47/B71 expander block out of index.html
// (openDetailIds, _detIdFromKey, toggleDetail, infoBtn, mkDetail) and asserts
// the ticket's actual complaint against it directly: an expander opened via
// its own icon must still be open after the panel re-renders (a selection
// made elsewhere in the group forces a rebuild, which is not itself a toggle),
// and nothing except a call to toggleDetail may change open state.
//
// Build-time only; not part of the served app.
// Usage: node b71_check.js index.html
const fs = require('fs');

function slice(lines, startNeedle, endNeedle) {
  const s = lines.findIndex(l => l.includes(startNeedle));
  const e = lines.findIndex(l => l.includes(endNeedle));
  if (s < 0 || e < 0 || e <= s) throw new Error(`slice failed: ${startNeedle} .. ${endNeedle}`);
  return lines.slice(s, e).join('\n');
}

function loadExpanders(path) {
  const lines = fs.readFileSync(path, 'utf8').split('\n');
  const block = slice(lines, '// ── B47: inline detail expanders', 'function weaponProfilesFor(raw, name) {');
  // Minimal DOM stub: a registry of fake elements, each with a classList that
  // records toggle() history so the test can see both the click-driven path
  // (element exists, e.g. this expander is currently on-screen) and the
  // re-render path (element does not exist yet at toggle time, e.g. B71's
  // original bug — a class-only implementation would have silently no-opped).
  const elements = {};
  const document = {
    getElementById: (id) => elements[id],
    _register: (id) => {
      elements[id] = elements[id] || {
        classes: new Set(),
        classList: {
          toggle(c) { elements[id].classes.has(c) ? elements[id].classes.delete(c) : elements[id].classes.add(c); },
          contains(c) { return elements[id].classes.has(c); }
        }
      };
      return elements[id];
    }
  };
  const src = block + '\nreturn { mkDetail, toggleDetail, infoBtn, _detIdFromKey, openDetailIds,'
            + ' _registerEl: document._register, _hasEl: (id) => !!elements[id] };';
  const factory = new Function('document', src);
  return factory(document);
}

const idxPath = process.argv[2] || 'index.html';
const E = loadExpanders(idxPath);

let fail = 0;
const ok = (cond, msg) => { if (!cond) { fail++; console.log('  FAIL ' + msg); } else console.log('  ok   ' + msg); };

// ── 1. Same key -> same id, deterministically, across separate calls ────────
console.log('B71 — the same key always produces the same expander id');
const idA1 = E._detIdFromKey('list-99|wg-fam-eye|group_x|Bolt Pistol');
const idA2 = E._detIdFromKey('list-99|wg-fam-eye|group_x|Bolt Pistol');
ok(idA1 === idA2, `identical key hashes to the same id (${idA1})`);
const idB = E._detIdFromKey('list-99|wg-fam-eye|group_x|Boltgun');
ok(idA1 !== idB, 'a different key hashes to a different id');

// ── 2. mkDetail is a pure function of (kind, html, key) and current state ───
console.log('B71 — mkDetail renders the id from the key, not from call order');
const call1 = E.mkDetail('eye', '<p>a</p>', 'entry-1|lo-eye|opt-A');
const call2 = E.mkDetail('eye', '<p>a</p>', 'entry-1|lo-eye|opt-A');
const idMatch1 = /id="([^"]+)"/.exec(call1.panel)[1];
const idMatch2 = /id="([^"]+)"/.exec(call2.panel)[1];
ok(idMatch1 === idMatch2, `two mkDetail calls for the same key render the same id (${idMatch1})`);

// ── 3. Core B71 complaint: opening via the icon survives a rebuild ──────────
console.log('B71 — an expander opened via its icon is still open after a re-render');
E.openDetailIds.clear();
const key = 'entry-7|lo-eye|opt-Z';
// First render: closed by default.
let first = E.mkDetail('eye', '<p>detail</p>', key);
ok(!/class="lo-detail open"/.test(first.panel), 'first render: closed by default');
const id = /id="([^"]+)"/.exec(first.panel)[1];
E._registerEl(id);
// User clicks the icon (the only thing that is allowed to change state).
E.toggleDetail(id);
ok(E.openDetailIds.has(id), 'toggleDetail records the id as open');
// A selection elsewhere in the group forces a full rebuild: mkDetail runs
// again for the same key, as if the whole panel HTML were regenerated fresh.
let second = E.mkDetail('eye', '<p>detail</p>', key);
ok(/class="lo-detail open"/.test(second.panel),
   'B71: after a rebuild, the same expander renders pre-opened — this is the exact bug being fixed');

// ── 4. Toggling again (still via the icon) closes it, and that survives too ─
console.log('B71 — a second click closes it, and that also survives a rebuild');
E.toggleDetail(id);
ok(!E.openDetailIds.has(id), 'toggleDetail records the id as closed again');
let third = E.mkDetail('eye', '<p>detail</p>', key);
ok(!/class="lo-detail open"/.test(third.panel), 'rebuild after closing renders closed, not stuck open');

// ── 5. Independence: unrelated keys never share open state ──────────────────
console.log('B71 — opening one expander does not open an unrelated one');
E.openDetailIds.clear();
const keyX = 'entry-3|lo-eye|opt-X';
const keyY = 'entry-3|lo-eye|opt-Y';
const rx = E.mkDetail('eye', '<p>x</p>', keyX);
const idX = /id="([^"]+)"/.exec(rx.panel)[1];
E._registerEl(idX);
E.toggleDetail(idX);
const ry = E.mkDetail('eye', '<p>y</p>', keyY);
ok(!/class="lo-detail open"/.test(ry.panel), 'a sibling expander with a different key stays closed');

// ── 6. Regression guard: id is not derived from any global call counter ─────
console.log('B71 — id assignment does not depend on how many other calls happened first');
const before = E._detIdFromKey('fixed-key-for-order-test');
for (let i = 0; i < 25; i++) E.mkDetail('eye', '<p>filler</p>', `filler-${i}`);
const after = E._detIdFromKey('fixed-key-for-order-test');
ok(before === after, 'twenty-five intervening mkDetail calls for other keys do not shift this key\'s id');

console.log(fail === 0 ? '\nall B71 checks pass' : `\n${fail} B71 check(s) FAILED`);
process.exit(fail === 0 ? 0 : 1);
