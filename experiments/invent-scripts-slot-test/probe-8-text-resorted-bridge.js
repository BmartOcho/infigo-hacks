// ============================================================================
// PROBE 8 — Bridge via Field.TextResorted (the real per-record event)
// ============================================================================
// PROBE 7 finding: Fabric.Modified only fires on canvas refreshes (mapping
// save, initial render). It does NOT fire on per-record preview clicks
// because preview switching happens in the PreviewPlugin iframe, which
// updates field text via postMessage → setTextAsLimitedHtml without
// triggering the editor canvas's Fabric event system.
//
// PROBE 3 found Field.TextResorted fires ~4–5x per switch (one per text
// field, after Invent.Batch writes the new record's value). That's exactly
// the trigger we need: the new substituted text is already in field.text.data
// when this event fires.
//
// This probe also adds a WIDE-NET event diagnostic — registers for every
// known editor event and logs which fire during per-record switches. If
// TextResorted isn't reliable, we'll see what is.
//
// Install:
//   Admin → MegaEdit Product Scripts → Create PROBE_8_TEXT_RESORTED
//   ExecutionType: Editor. Enabled. Paste this file. Save.
//
// Attach: untick PROBE_7 → tick PROBE_8 → Save. Reload editor.
//
// Test: upload CSV, click through records. Expected:
//   - "Bridge from event 'Field.TextResorted'..." log per text field per
//     record switch
//   - First Name = "Jane" for record 1, then changes to whatever record 2/3/4
//     has on each click
//   - When First Name = "?", watch the canvas: background should swap
//     (assuming Variable Logic re-evaluates on programmatic Variables.Set
//     during preview context — that's the question this probe answers)
// ============================================================================

(function () {
  const TAG = '[PROBE 8]';
  const PLACEHOLDER_RX = /\[#([^#\]]+?)#\]/g;

  // Per-text-field-update events worth hooking. TextResorted is the primary;
  // others are belt-and-suspenders fallbacks.
  const PRIMARY_EVENTS = ['Field.TextResorted'];
  // Wide-net diagnostic: register for ALL editor events to see which fire on
  // per-record switches. Useful if TextResorted doesn't fire reliably.
  const DIAGNOSTIC_EVENTS = [
    'Field.TextResorted', 'Field.ImageChanged', 'Field.Updated',
    'Field.Modified', 'Field.Refreshed', 'Field.TextChanged',
    'Fabric.Modified', 'Preview.RecordChanged', 'Preview.Updated',
    'Batch.RecordChanged', 'BatchDataSaved', 'MappingSaved',
    'Document.Changed', 'Canvas.Rendered'
  ];

  function log() {
    var args = Array.prototype.slice.call(arguments);
    console.log.apply(console, [TAG].concat(args));
  }

  if (typeof Editor === 'undefined' || !Editor.Invent || !Editor.Events ||
      !Editor.Invent.Variables || typeof Editor.Invent.Variables.Set !== 'function') {
    log('FAIL: required APIs missing'); return;
  }
  if (typeof Job === 'undefined' || !Job.Fields) {
    log('FAIL: Job.Fields missing'); return;
  }

  // --- state
  const fieldVariableMap = new Map();
  const variableFieldMap = new Map();
  const lastSeenText = new Map();
  let mapBuilt = false;
  let bridging = false;
  let bridgeCount = 0;
  // Event diagnostics
  const eventCounters = new Map();
  let lastDiagLogTime = 0;

  function buildMap() {
    if (mapBuilt) return;
    try {
      const all = Job.Fields.All(null);
      let bindings = 0;
      all.forEach(function (f) {
        if (!f.text || typeof f.text.data !== 'string' || !f.text.data) return;
        const txt = f.text.data;
        const matches = [];
        PLACEHOLDER_RX.lastIndex = 0;
        let m;
        while ((m = PLACEHOLDER_RX.exec(txt)) !== null) matches.push(m[1].trim());
        if (matches.length > 0) {
          fieldVariableMap.set(f.id, matches);
          matches.forEach(function (vn) {
            if (!variableFieldMap.has(vn)) variableFieldMap.set(vn, []);
            variableFieldMap.get(vn).push(f.id);
            bindings++;
          });
        }
      });
      mapBuilt = true;
      log('Map built: ' + bindings + ' bindings across ' + fieldVariableMap.size + ' fields');
      fieldVariableMap.forEach(function (vars, fid) {
        log('  ' + fid + ' → [' + vars.join(', ') + ']');
      });
    } catch (e) {
      log('buildMap error:', e.message);
    }
  }

  function readText(fieldId) {
    try {
      const f = Job.Fields.ById(fieldId);
      return (f && f.text && typeof f.text.data === 'string') ? f.text.data : null;
    } catch (e) { return null; }
  }

  // Called by per-field event handlers. Reads the field's current text,
  // determines its bound variable(s), pushes value to Variables.Set if
  // single-variable. Re-entry guarded.
  function bridgeOneField(fieldId, eventName) {
    if (bridging) return;
    if (!mapBuilt) return;
    const vars = fieldVariableMap.get(fieldId);
    if (!vars || vars.length === 0) return;
    if (vars.length > 1) {
      // Multi-var field — log and skip
      const txt = readText(fieldId);
      if (lastSeenText.get(fieldId) !== txt) {
        log('  Multi-var field ' + fieldId + ' text="' + txt + '" — can\'t deconstruct ' + vars.join('+'));
        lastSeenText.set(fieldId, txt);
      }
      return;
    }
    const txt = readText(fieldId);
    if (txt === null) return;
    if (lastSeenText.get(fieldId) === txt) return;
    lastSeenText.set(fieldId, txt);

    bridging = true;
    bridgeCount++;
    const varName = vars[0];
    log('Bridge #' + bridgeCount + ' [' + eventName + ']: ' + varName + ' = "' + txt + '"');

    try {
      Editor.Invent.Variables.Set(varName, txt, function () {
        log('  ✓ committed ' + varName);
        bridging = false;
      });
    } catch (e) {
      log('  ✗ Variables.Set threw:', e.message);
      bridging = false;
    }
  }

  // Inspect an event payload to extract field id if present. MegaEdit events
  // tend to be either: a field object directly, an object with .field, .id,
  // .fieldId, etc.
  function extractFieldId(payload) {
    if (!payload) return null;
    if (typeof payload === 'string') return payload;
    if (payload.id && typeof payload.id === 'string') return payload.id;
    if (payload.fieldId) return payload.fieldId;
    if (payload.field && payload.field.id) return payload.field.id;
    return null;
  }

  // Wide-net diagnostic handler — counts events per type so we can identify
  // which events fire on per-record switches. Logs a summary on a debounced
  // schedule to avoid console spam.
  function diagnosticHandler(eventName) {
    return function (payload) {
      const c = (eventCounters.get(eventName) || 0) + 1;
      eventCounters.set(eventName, c);
      // Debounced summary
      const now = Date.now();
      if (now - lastDiagLogTime > 1000) {
        lastDiagLogTime = now;
        const summary = [];
        eventCounters.forEach(function (v, k) { summary.push(k + '=' + v); });
        if (summary.length > 0) log('[diag] event counts:', summary.join(', '));
      }
    };
  }

  setTimeout(function () {
    log('Loading…');
    buildMap();

    // Primary bridge hooks — these are the events we trust to fire per record
    PRIMARY_EVENTS.forEach(function (evt) {
      try {
        Editor.Events.Register(evt, function (payload) {
          const fid = extractFieldId(payload);
          if (fid) {
            bridgeOneField(fid, evt);
          } else {
            // No field id in payload — fall back to walking all mapped fields
            fieldVariableMap.forEach(function (_, mappedFid) {
              bridgeOneField(mappedFid, evt + '(fallback)');
            });
          }
        });
        log('Hooked primary event: ' + evt);
      } catch (e) {
        log('Failed to hook ' + evt + ':', e.message);
      }
    });

    // Diagnostic hooks — register every candidate event, just count
    DIAGNOSTIC_EVENTS.forEach(function (evt) {
      try {
        Editor.Events.Register(evt, diagnosticHandler(evt));
      } catch (e) { /* silently skip unsupported events */ }
    });
    log('Registered ' + DIAGNOSTIC_EVENTS.length + ' diagnostic event hooks.');
    log('Upload CSV (if not already) and click through records 1–5.');
    log('Watch for: Bridge #N lines (the actual fix) AND [diag] event counts (which events actually fire per switch).');
  }, 500);

  log('PROBE 8 init.');
})();
