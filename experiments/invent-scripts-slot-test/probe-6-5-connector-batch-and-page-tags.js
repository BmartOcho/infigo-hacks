// ============================================================================
// PROBE 6.5 — connector.batch + page.tags introspection
// ============================================================================
// PROBE 6 found: Invent embeds [#Variable Name#] in field.text.data BEFORE
// batch substitution. That's a viable linkage path. But two surfaces remained
// unexplored:
//   1. connector.batch — the connector has a `batch` key (visible in PROBE 6
//      Attempt D). What's inside?
//   2. page.tags — pages carry a `tags` array (visible in PROBE 6 Attempt F).
//      What's in it?
//
// If connector.batch exposes a supported method (e.g. getRecordForField,
// getFieldsForVariable, getCurrentValue), that's the official API and PROBE 7
// should use it. Otherwise PROBE 7 parses [#Var#] from text.data.
//
// Read-only. Logs everything and exits. Run before CSV upload.
//
// Install:
//   Admin → MegaEdit Product Scripts → Create PROBE_6_5_CONNECTOR_BATCH
//   ExecutionType: Editor. Enabled. Paste this file. Save.
//
// Attach: Scripts tab → untick all PROBE_*, tick PROBE_6_5 → Save.
// ============================================================================

(function () {
  const TAG = '[PROBE 6.5]';
  function log() {
    var args = Array.prototype.slice.call(arguments);
    console.log.apply(console, [TAG].concat(args));
  }

  function listKeys(obj) {
    if (!obj || typeof obj !== 'object') return [];
    var keys = [];
    try { keys = Object.keys(obj); } catch (e) { return []; }
    try {
      var proto = Object.getPrototypeOf(obj);
      if (proto && proto !== Object.prototype) {
        Object.getOwnPropertyNames(proto).forEach(function (k) {
          if (keys.indexOf(k) === -1 && k !== 'constructor') {
            keys.push(k + ' [proto/' + (typeof proto[k]) + ']');
          }
        });
      }
    } catch (e) {}
    return keys;
  }

  function safeStringify(v, depth) {
    depth = depth || 0;
    if (depth > 3) return '[depth>3]';
    if (v === null || v === undefined) return String(v);
    if (typeof v === 'function') return '[fn]';
    if (typeof v !== 'object') return JSON.stringify(v);
    if (Array.isArray(v)) {
      if (v.length === 0) return '[]';
      return '[' + v.slice(0, 10).map(function (x) { return safeStringify(x, depth + 1); }).join(', ') +
        (v.length > 10 ? ', ...+' + (v.length - 10) : '') + ']';
    }
    try {
      const keys = Object.keys(v);
      if (keys.length === 0) return '{}';
      return '{' + keys.slice(0, 20).map(function (k) {
        return k + ': ' + safeStringify(v[k], depth + 1);
      }).join(', ') + (keys.length > 20 ? ', ...+' + (keys.length - 20) : '') + '}';
    } catch (e) { return '[unstringifiable]'; }
  }

  setTimeout(function () {
    log('Starting…');

    // ============================================================ connector.batch
    if (!Editor || !Editor.Invent) { log('FAIL: Editor.Invent missing'); return; }
    Editor.Invent.GetConnector(function (connector) {
      if (!connector) { log('No connector'); return; }
      log('=== connector.batch deep dive ===');
      log('  connector.batch =', safeStringify(connector.batch));
      log('  connector.batch keys:', listKeys(connector.batch).join(', '));

      // Method-name candidates worth probing for field/variable linkage
      const candidates = [
        'getFieldsForVariable', 'getVariableForField', 'getVariableLinkedToFields',
        'fieldsForVariable', 'variableForField', 'mapping', 'getMapping',
        'getCurrentRecord', 'getRecord', 'currentRecord', 'records',
        'getValue', 'getValueForField', 'getCurrentValueForVariable'
      ];
      if (connector.batch && typeof connector.batch === 'object') {
        candidates.forEach(function (m) {
          if (typeof connector.batch[m] === 'function') {
            log('  ★ connector.batch.' + m + ' EXISTS — trying with "First Name"');
            try {
              const sync = connector.batch[m]('First Name');
              log('    sync result:', safeStringify(sync));
            } catch (e1) {
              try {
                connector.batch[m]('First Name', function (cb) {
                  log('    async callback:', safeStringify(cb));
                });
              } catch (e2) {
                log('    threw:', e1.message, '|', e2.message);
              }
            }
          }
        });
      }

      // Also dump connector.variables — may have lookup methods too
      log('=== connector.variables deep dive ===');
      log('  connector.variables =', safeStringify(connector.variables));
      log('  connector.variables keys:', listKeys(connector.variables).join(', '));
      candidates.forEach(function (m) {
        if (connector.variables && typeof connector.variables[m] === 'function') {
          log('  ★ connector.variables.' + m + ' EXISTS');
        }
      });
    });

    // ============================================================ page.tags
    if (Job && Job.Pages && typeof Job.Pages.All === 'function') {
      log('=== page.tags deep dive ===');
      const pages = Job.Pages.All(null);
      pages.forEach(function (p, i) {
        log('  Page #' + i + ' id=' + p.id);
        log('    tags =', safeStringify(p.tags));
      });
    }

    // ============================================================ Editor.Invent.Batch
    log('=== Editor.Invent.Batch deep dive ===');
    log('  Editor.Invent.Batch =', safeStringify(Editor.Invent.Batch));
    log('  Editor.Invent.Batch keys:', listKeys(Editor.Invent.Batch).join(', '));

    // ============================================================ Job.Fields.ByTags signature
    log('=== Job.Fields method signatures ===');
    log('  Job.Fields keys:', listKeys(Job.Fields).join(', '));

    log('PROBE 6.5 complete.');
  }, 500);

  log('Loaded. Waiting 500ms…');
})();
