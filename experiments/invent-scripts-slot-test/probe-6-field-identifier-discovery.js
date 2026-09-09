// ============================================================================
// PROBE 6 — Field identifier discovery (find the field→variable linkage
// without name-based lookup)
// ============================================================================
// Probes 4 & 5 blocked on empty `name=""` properties. This probe ignores name
// entirely and tries every other identifier mechanism we can think of, dumping
// rich diagnostic output for the support ticket either way.
//
// Strategy — six independent attempts, each logged separately:
//   A) Full property enumeration on every text field (Object.keys + recursive
//      dump of non-noisy keys). Looking for: customData, tags, metadata,
//      placeholder, placeholders, invent, variable, binding, source.
//   B) Job.Fields.ByTags() with candidate values: variable name, slugged
//      variant, lowercase, "First Name", "FirstName", "first_name".
//   C) Field text inspection — Invent's "Multiple placeholders" warning
//      proves placeholder markers exist IN field text. Regex-scan for
//      {{X}}, ${X}, [[X]], <<X>>, %X%, @X@ — whatever Invent uses.
//   D) Connector method introspection — log every method/property on
//      Editor.Invent and the returned connector. Look for getFieldsForVariable,
//      getVariableForField, fields, mapping, bindings, etc.
//   E) Window scope walk — sometimes Invent's helpers leak globally. Check
//      for getVariableLinkedToFields, InventBatch, InDesign on window.
//   F) Existing API shapes — call ByPagesAndTags with empty filters, dump
//      every page's field collection to see if pages carry binding info.
//
// Install:
//   Admin → MegaEdit Product Scripts → Create PROBE_6_FIELD_DISCOVERY
//   ExecutionType: Editor. Enabled. Paste this file. Save.
//
// Attach: Test product → Scripts tab → untick PROBE_4/5 → tick PROBE_6 → Save.
//   (Or reference PROBE_6_FIELD_DISCOVERY in the Invent Scripts slot and
//   re-import MEX — either works.)
//
// Test: open editor, watch console. Then upload CSV and watch again for any
// per-record changes. NO clicks needed — this probe is read-only.
//
// Output to capture for ticket: full console transcript. The dump from
// Attempt A is the most valuable — shows support EXACTLY what attributes
// their Invent-exported fields carry.
// ============================================================================

(function () {
  const TAG = '[PROBE 6]';
  const VAR_NAME = 'First Name';
  const VAR_CANDIDATES = [
    'First Name', 'FirstName', 'firstname', 'first name', 'first_name',
    'FIRST NAME', 'first-name', 'FirstNameField'
  ];
  // Keys that are universally noisy on field objects — skip in dumps
  const NOISE_KEYS = new Set([
    'fabricObject', '_fabricObject', '__proto__', 'parent', 'page',
    'pages', 'document', 'job', '_listeners', 'eventEmitter'
  ]);

  function log() {
    var args = Array.prototype.slice.call(arguments);
    console.log.apply(console, [TAG].concat(args));
  }

  function safeStringify(v, depth) {
    depth = depth || 0;
    if (depth > 2) return '[depth>2]';
    if (v === null || v === undefined) return String(v);
    if (typeof v === 'function') return '[function]';
    if (typeof v !== 'object') return JSON.stringify(v);
    try {
      const keys = Object.keys(v).filter(function (k) { return !NOISE_KEYS.has(k); });
      if (keys.length === 0) return '{}';
      return '{' + keys.slice(0, 15).map(function (k) {
        var val = v[k];
        if (val && typeof val === 'object') {
          return k + ': ' + safeStringify(val, depth + 1);
        }
        if (typeof val === 'function') return k + ': [fn]';
        return k + ': ' + JSON.stringify(val);
      }).join(', ') + (keys.length > 15 ? ', ...+' + (keys.length - 15) : '') + '}';
    } catch (e) {
      return '[unstringifiable: ' + e.message + ']';
    }
  }

  function listKeys(obj) {
    if (!obj || typeof obj !== 'object') return [];
    var keys = [];
    try { keys = Object.keys(obj); } catch (e) { return []; }
    // Also walk prototype for own-property-missing methods
    try {
      var proto = Object.getPrototypeOf(obj);
      if (proto && proto !== Object.prototype) {
        Object.getOwnPropertyNames(proto).forEach(function (k) {
          if (keys.indexOf(k) === -1 && k !== 'constructor') keys.push(k + ' (proto)');
        });
      }
    } catch (e) {}
    return keys;
  }

  if (typeof Editor === 'undefined' || !Editor.Invent) {
    log('FAIL: Editor.Invent missing'); return;
  }
  if (typeof Job === 'undefined' || !Job.Fields) {
    log('FAIL: Job.Fields missing'); return;
  }

  // ---------------------------------------------------------------- ATTEMPT A
  function attemptA_propertyEnumeration() {
    log('=== ATTEMPT A: Property enumeration on every text field ===');
    try {
      const all = Job.Fields.All(null);
      log('Total fields:', all.length);
      all.forEach(function (f, i) {
        log('--- Field #' + i + ' id=' + f.id + ' type=' + (f.type || '?') + ' ---');
        const keys = listKeys(f);
        log('  Top-level keys (' + keys.length + '):', keys.join(', '));
        // Highlight keys that LOOK linkage-related
        ['customData', 'CustomData', 'customdata', 'tags', 'metadata',
         'binding', 'bindings', 'variable', 'variables', 'invent',
         'placeholder', 'placeholders', 'source', 'data'].forEach(function (k) {
          if (k in f) log('  >>> ' + k + ' =', safeStringify(f[k]));
        });
        // Dump field.text shape (placeholders may live here)
        if (f.text) {
          log('  text keys:', listKeys(f.text).join(', '));
          log('  text =', safeStringify(f.text));
        }
      });
    } catch (e) {
      log('Attempt A error:', e.message, e.stack);
    }
  }

  // ---------------------------------------------------------------- ATTEMPT B
  function attemptB_tagLookup() {
    log('=== ATTEMPT B: Job.Fields.ByTags() with candidate values ===');
    if (typeof Job.Fields.ByTags !== 'function') {
      log('  Job.Fields.ByTags is not a function — skipping'); return;
    }
    VAR_CANDIDATES.forEach(function (tag) {
      try {
        const result = Job.Fields.ByTags([tag], null, true);
        log('  ByTags(["' + tag + '"]) →', result ? (result.length + ' results') : 'null');
        if (result && result.length > 0) {
          result.forEach(function (r) { log('    id=' + r.id + ' name="' + (r.name || '') + '"'); });
        }
      } catch (e) {
        log('  ByTags(["' + tag + '"]) threw:', e.message);
      }
    });
    // Also try without filter array — different signature?
    try {
      const noFilter = Job.Fields.ByTags(VAR_CANDIDATES, null, true);
      log('  ByTags(ALL candidates) →', noFilter ? noFilter.length : 'null');
    } catch (e) { log('  ByTags(ALL) threw:', e.message); }
  }

  // ---------------------------------------------------------------- ATTEMPT C
  function attemptC_placeholderScan() {
    log('=== ATTEMPT C: Placeholder marker scan in field text ===');
    const patterns = [
      /\{\{([^}]+)\}\}/g,    // {{First Name}}
      /\$\{([^}]+)\}/g,      // ${First Name}
      /\[\[([^\]]+)\]\]/g,   // [[First Name]]
      /<<([^>]+)>>/g,        // <<First Name>>
      /%([A-Za-z][^%\s]*)%/g, // %FirstName%
      /@([A-Za-z][^@\s]*)@/g  // @FirstName@
    ];
    try {
      const all = Job.Fields.All(null);
      all.forEach(function (f) {
        if (!f.text || typeof f.text.data !== 'string') return;
        const txt = f.text.data;
        patterns.forEach(function (rx, i) {
          rx.lastIndex = 0;
          const matches = [];
          let m;
          while ((m = rx.exec(txt)) !== null) matches.push(m[1]);
          if (matches.length > 0) {
            log('  Field ' + f.id + ' pattern[' + i + ']:', matches);
          }
        });
        if (txt.indexOf('First Name') !== -1 || txt.indexOf('first') !== -1) {
          log('  Field ' + f.id + ' literal text contains "First/first":', JSON.stringify(txt));
        }
      });
    } catch (e) { log('Attempt C error:', e.message); }
  }

  // ---------------------------------------------------------------- ATTEMPT D
  function attemptD_connectorIntrospection() {
    log('=== ATTEMPT D: Connector + Editor.Invent introspection ===');
    log('  Editor.Invent keys:', listKeys(Editor.Invent).join(', '));
    Editor.Invent.GetConnector(function (connector) {
      if (!connector) { log('  No connector'); return; }
      log('  connector keys:', listKeys(connector).join(', '));
      if (connector.events) {
        log('  connector.events keys:', listKeys(connector.events).join(', '));
      }
      if (connector.fields) {
        log('  connector.fields keys:', listKeys(connector.fields).join(', '));
        // Try calling it if it's a function-shaped thing
        try {
          log('  connector.fields() →', safeStringify(connector.fields));
        } catch (e) {}
      }
      // Hunt for any method whose name suggests linkage
      const candidateMethods = ['getFieldsForVariable', 'getVariableForField',
        'getVariableLinkedToFields', 'getBindings', 'getMapping', 'fieldsForVariable',
        'fieldsByVariable', 'getFieldByVariable', 'lookupField'];
      candidateMethods.forEach(function (m) {
        if (typeof connector[m] === 'function') {
          log('  ★ Found connector.' + m + ' — trying with "' + VAR_NAME + '"');
          try {
            connector[m](VAR_NAME, function (result) {
              log('    ' + m + ' callback:', safeStringify(result));
            });
          } catch (e) {
            try {
              const sync = connector[m](VAR_NAME);
              log('    ' + m + ' sync result:', safeStringify(sync));
            } catch (e2) {
              log('    ' + m + ' threw:', e.message, '|', e2.message);
            }
          }
        }
      });
    });
  }

  // ---------------------------------------------------------------- ATTEMPT E
  function attemptE_windowScopeWalk() {
    log('=== ATTEMPT E: Window-scope walk for leaked Invent helpers ===');
    if (typeof window === 'undefined') { log('  no window'); return; }
    const candidates = [
      'getVariableLinkedToFields', 'InventBatch', 'InDesign',
      'InDesignBatch', 'InventConnector', 'PerformFieldDataReplacement',
      'BatchInfoRetriverFns', 'FieldHandlers', 'PreviewPlugin'
    ];
    candidates.forEach(function (k) {
      if (k in window) {
        log('  ★ window.' + k + ' exists:', typeof window[k]);
        if (typeof window[k] === 'object' && window[k]) {
          log('    keys:', listKeys(window[k]).slice(0, 20).join(', '));
        }
      }
    });
  }

  // ---------------------------------------------------------------- ATTEMPT F
  function attemptF_pageBindings() {
    log('=== ATTEMPT F: Page-level field binding inspection ===');
    try {
      if (!Job.Pages || typeof Job.Pages.All !== 'function') {
        log('  Job.Pages.All not available'); return;
      }
      const pages = Job.Pages.All(null);
      log('  Pages:', pages.length);
      pages.forEach(function (p, i) {
        log('  Page #' + i + ' keys:', listKeys(p).join(', '));
        if (p.fields) log('    page.fields:', safeStringify(p.fields));
      });
    } catch (e) { log('Attempt F error:', e.message); }
  }

  // ---------------------------------------------------------------- ORCHESTRATOR
  setTimeout(function () {
    log('PROBE 6 starting. All read-only — no canvas mutations.');
    attemptA_propertyEnumeration();
    attemptB_tagLookup();
    attemptC_placeholderScan();
    attemptD_connectorIntrospection();
    attemptE_windowScopeWalk();
    attemptF_pageBindings();
    log('PROBE 6 sync attempts complete. (Attempt D may log asynchronously.)');
    log('Next: upload CSV — script will re-run Attempt A + C after BatchDataSaved fires.');

    // Re-run A + C after CSV upload — field text may change shape
    if (Editor.Events && typeof Editor.Events.Register === 'function') {
      Editor.Events.Register('BatchDataSaved', function () {
        log('=== BatchDataSaved fired — re-running A + C ===');
        attemptA_propertyEnumeration();
        attemptC_placeholderScan();
      });
    }
  }, 500);

  log('PROBE 6 loaded. Waiting 500ms for editor...');
})();
