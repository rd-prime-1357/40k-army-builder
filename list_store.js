/* ===========================================================================
 * 40K Army Builder — list storage + saved-list schema (Step 2)
 *
 * Self-contained. No DOM, no app globals. Splices into index.html's IIFE.
 * All persistence goes through a swappable async backend so localStorage v1
 * can become Drive/OneDrive later without touching callers.
 *
 * Three concerns, each independently testable:
 *   1. SavedList schema + (de)serialize  — pure, dependency-injected
 *   2. ListStore                          — async CRUD over a backend
 *   3. createLocalStorageBackend          — the v1 backend
 * ======================================================================== */

(function (root) {
  'use strict';

  var SCHEMA_VERSION = 1;
  var NS = '40kab:list:';   // one key per list: 40kab:list:<id>

  // ── ids ──────────────────────────────────────────────────────────────────
  function newListId() {
    if (typeof crypto !== 'undefined' && crypto.randomUUID) return crypto.randomUUID();
    return 'l-' + Date.now().toString(36) + '-' + Math.random().toString(36).slice(2, 10);
  }

  // ── schema: in-memory armyList <-> persisted record ──────────────────────
  //
  // The persisted entry uses snake_case names that are deliberately decoupled
  // from the runtime entry shape. Mapping field-by-field (not dumping the live
  // object) means a future refactor of the in-memory entry cannot silently
  // change the on-disk format — that contract is what schema_version guards.
  //
  // serializeEntries(armyList, primaryFaction, lookups)
  //   lookups.unitIdFor(faction_ref, unit_name) -> id | null   (resolve at save)
  function serializeEntries(armyList, primaryFaction, lookups) {
    return armyList.map(function (e) {
      var faction_ref = e.faction_ref || primaryFaction;
      var uid = e.unit_id ||
                (lookups && lookups.unitIdFor && lookups.unitIdFor(faction_ref, e.unit_name)) ||
                null;
      return {
        entry_id:      e.listId,
        faction_ref:   faction_ref,
        unit_id:       uid,
        unit_name:     e.unit_name,   // cached: display + name-fallback resolve
        unit_type:     e.unit_type,   // cached: grouping when unresolved
        size_idx:      e.sizeIdx,
        god:           e.god != null ? e.god : null,
        wargear:       e.wargear || {},
        other_options: e.otherOptions || {},
        attached_to:   e.attachedToListId != null ? e.attachedToListId : null,
        points_cache:  e.points != null ? e.points : null  // display-only; recomputed on load
      };
    });
  }

  // buildRecord(meta, armyList, lookups) -> full SavedList record
  //   meta: { id?, name, points_target, primary_faction, created? }
  function buildRecord(meta, armyList, lookups) {
    var now = Date.now();
    return {
      schema_version:  SCHEMA_VERSION,
      id:              meta.id || newListId(),
      name:            meta.name || 'Untitled',
      points_target:   meta.points_target != null ? meta.points_target : null,
      primary_faction: meta.primary_faction || null,
      created:         meta.created || now,
      modified:        now,
      entries:         serializeEntries(armyList, meta.primary_faction, lookups)
    };
  }

  // deserialize(record, resolvers) -> { armyList, warnings, maxEntryId }
  //   resolvers.resolveUnit(faction_ref, unit_id, unit_name) -> unit | null
  // Resolution order is id-first (survives renames), then cached name. A miss
  // produces a flagged ghost entry — never dropped (flag-don't-drop).
  function deserialize(record, resolvers) {
    var warnings = [];
    var maxEntryId = 0;
    var armyList = (record.entries || []).map(function (s) {
      if (s.entry_id != null && s.entry_id > maxEntryId) maxEntryId = s.entry_id;
      var unit = resolvers && resolvers.resolveUnit
        ? resolvers.resolveUnit(s.faction_ref, s.unit_id, s.unit_name)
        : null;
      var unresolved = !unit;
      if (unresolved) {
        warnings.push({
          type: 'unresolved_unit',
          entry_id: s.entry_id,
          unit_id: s.unit_id,
          unit_name: s.unit_name,
          faction_ref: s.faction_ref
        });
      }
      // On a successful id-match, prefer the unit's CURRENT name so a rename in
      // the data flows through to the loaded list; fall back to the cached name.
      var liveName = unit && unit.unit_name ? unit.unit_name : s.unit_name;
      return {
        listId:           s.entry_id,
        unit_name:        liveName,
        unit_type:        (unit && unit.unit_type) || s.unit_type || null,
        sizeIdx:          s.size_idx != null ? s.size_idx : 0,
        god:              s.god != null ? s.god : null,
        points:           null,               // recomputed by the app on render
        wargear:          s.wargear || {},
        otherOptions:     s.other_options || {},
        attachedToListId: s.attached_to != null ? s.attached_to : null,
        faction_ref:      s.faction_ref || null,
        unit_id:          s.unit_id || null,
        unresolved:       unresolved          // drives the ghost-row flag
      };
    });
    return { armyList: armyList, warnings: warnings, maxEntryId: maxEntryId };
  }

  // ── migration hook ───────────────────────────────────────────────────────
  // v1 is the only shape today; the hook exists so the first schema change has
  // a home and old blobs upgrade on load instead of crashing or misreading.
  function migrate(record) {
    if (!record || typeof record !== 'object') return null;
    var v = record.schema_version || 0;
    if (v === SCHEMA_VERSION) return record;
    if (v > SCHEMA_VERSION) {
      // Saved by a newer app build than this one. Surface, don't guess.
      return { __incompatible: true, found_version: v, expected_version: SCHEMA_VERSION, raw: record };
    }
    // v < current: future per-step upgrades go here, e.g.
    //   if (v < 2) { ...; record.schema_version = 2; }
    return record;
  }

  // ── ListStore: async CRUD over a swappable backend ───────────────────────
  // backend contract (all return Promises):
  //   getItem(key)->string|null  setItem(key,val)  removeItem(key)  keys()->string[]
  function ListStore(backend) {
    this.backend = backend;
  }
  ListStore.prototype._key = function (id) { return NS + id; };

  ListStore.prototype.put = function (record) {
    var self = this;
    return Promise.resolve().then(function () {
      record.modified = Date.now();
      var json = JSON.stringify(record);
      return self.backend.setItem(self._key(record.id), json).then(function () { return record; });
    });
  };

  ListStore.prototype.get = function (id) {
    var self = this;
    return Promise.resolve(self.backend.getItem(this._key(id))).then(function (raw) {
      if (raw == null) return null;
      var rec;
      try { rec = JSON.parse(raw); }
      catch (err) { return { __corrupt: true, id: id }; }
      return migrate(rec);
    });
  };

  ListStore.prototype.delete = function (id) {
    return Promise.resolve(this.backend.removeItem(this._key(id))).then(function () { return true; });
  };

  // list() -> [{id,name,primary_faction,points_target,modified,created,entry_count}]
  // Lightweight summaries for the browse surface. Scans namespaced keys; lists
  // are few and small so a scan beats maintaining a separate index that can
  // desync. Corrupt/incompatible records are skipped with a warning, not fatal.
  ListStore.prototype.list = function () {
    var self = this;
    return Promise.resolve(self.backend.keys()).then(function (keys) {
      var ours = keys.filter(function (k) { return k.indexOf(NS) === 0; });
      return Promise.all(ours.map(function (k) {
        return Promise.resolve(self.backend.getItem(k)).then(function (raw) {
          if (raw == null) return null;
          try {
            var r = JSON.parse(raw);
            return {
              id: r.id,
              name: r.name,
              primary_faction: r.primary_faction,
              points_target: r.points_target,
              modified: r.modified,
              created: r.created,
              entry_count: (r.entries || []).length
            };
          } catch (err) {
            if (typeof console !== 'undefined') console.warn('[ListStore] skipping corrupt record at', k);
            return null;
          }
        });
      })).then(function (rows) {
        return rows.filter(Boolean).sort(function (a, b) { return (b.modified || 0) - (a.modified || 0); });
      });
    });
  };

  // ── localStorage backend (v1) ────────────────────────────────────────────
  // Async-shaped over a synchronous store so the ListStore interface is
  // backend-agnostic. A cloud backend implements the same four methods async.
  function createLocalStorageBackend(storage) {
    var ls = storage; // injectable for tests; defaults to window.localStorage
    if (!ls && typeof localStorage !== 'undefined') ls = localStorage;
    return {
      getItem:    function (k) { return Promise.resolve(ls.getItem(k)); },
      setItem:    function (k, v) {
        return new Promise(function (resolve, reject) {
          try { ls.setItem(k, v); resolve(); }
          catch (err) { reject(err); }   // quota / private-mode failures surface to caller
        });
      },
      removeItem: function (k) { return Promise.resolve(ls.removeItem(k)); },
      keys:       function () {
        var out = [];
        for (var i = 0; i < ls.length; i++) out.push(ls.key(i));
        return Promise.resolve(out);
      }
    };
  }

  // ── export / import (JSON file portability) ──────────────────────────────
  // Single list or an array. exportRecords always emits an array for a stable
  // file shape; importRecords accepts either and re-ids to avoid clobbering.
  function exportRecords(records) {
    return JSON.stringify({ format: '40kab-lists', schema_version: SCHEMA_VERSION, lists: records }, null, 2);
  }
  function importRecords(jsonText) {
    var parsed = JSON.parse(jsonText);
    var list = Array.isArray(parsed) ? parsed
             : (parsed && parsed.lists) ? parsed.lists
             : (parsed && parsed.id) ? [parsed]
             : [];
    return list.map(migrate).filter(function (r) { return r && !r.__incompatible; });
  }

  var API = {
    SCHEMA_VERSION: SCHEMA_VERSION,
    NS: NS,
    newListId: newListId,
    serializeEntries: serializeEntries,
    buildRecord: buildRecord,
    deserialize: deserialize,
    migrate: migrate,
    ListStore: ListStore,
    createLocalStorageBackend: createLocalStorageBackend,
    exportRecords: exportRecords,
    importRecords: importRecords
  };

  if (typeof module !== 'undefined' && module.exports) module.exports = API;
  else root.ListStorage = API;

})(typeof self !== 'undefined' ? self : this);
