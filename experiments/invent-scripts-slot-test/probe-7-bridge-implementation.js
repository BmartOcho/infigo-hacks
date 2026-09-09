// ============================================================================
// PROBE 7 — The actual bridge: parse [#Var#] linkage, push per-record values
// to Editor.Invent.Variables.Set on Fabric.Modified
// ============================================================================
// Backed by PROBE 6 + 6.5 empirical findings:
//   - Invent embeds [#Variable Name#] in field.text.data BEFORE batch
//     substitution. After CSV upload, placeholders are gone (substituted with
//     record values).
//   - field.text.internalText sometimes carries weird encodings (null bytes,
//     newlines in long variable names) — prefer text.data for parsing.
//   - Editor.Invent.Variables.Set(name, value, cb) is confirmed working
//     (PROBE 2 — fired Variable Logic exactly once on record 1's CSV-upload
//     values).
//   - Fabric.Modified fires ~1x per record switch (PROBE 3).
//   - The supported v1.0.19 API path may also be Editor.Invent.Batch.Set or
//     connector.variables.set — we log both available shapes for future
//     reference but USE Editor.Invent.Variables.Set as the primary because
//     it's already empirically validated.
//
// CRITICAL TIMING: This script MUST capture the field→variable map BEFORE
// any CSV upload happens. If the user uploads CSV first then attaches this
// script, the placeholders are already substituted and parsing fails. The
// Invent Scripts slot auto-attach is the safest install path because the
// script loads with the editor on first open.
//
// Install:
//   Admin → MegaEdit Product Scripts → Create PROBE_7_BRIDGE
//   ExecutionType: Editor. Enabled. Paste this file. Save.
//
// Attach: Test product → Scripts tab → untick all other PROBE_* scripts →
//   tick PROBE_7 → Save.
//
// IMPORTANT: When testing, do NOT have a prior CSV mapping cached. Either:
//   (a) clear the batch mapping on the product before reloading the editor,
//   (b) or use a fresh test product where no CSV has ever been uploaded.
// Otherwise the script can't see [#Var#] placeholders because they've been
// substituted already on prior batch load.
//
// Test: reload editor → confirm "Captured N field→variable bindings" log →
//   upload CSV → click through records 1–5 → watch Background swap on the
//   rows where First Name = "?".
//
// Expected outcomes:
//   (a) Backgrounds swap correctly per record → SHIP IT. Rename to
//       INVENT_BATCH_LOGIC_BRIDGE, update Invent Scripts slot, document.
//   (b) Variables.Set fires but backgrounds don't swap → Variable Logic
//       doesn't re-evaluate on programmatic set during batch preview.
//       Fall back to PROBE 5's direct background manipulation, now feasible
//       because we have the field→variable map.
//   (c) Variables.Set throws → try connector.variables.set or
//       Editor.Invent.Batch.Set (both logged but unused in this probe).
// ============================================================================

(function () {
  const TAG = '[PROBE 7]';
  // Regex for [#Variable Name#] — variable names may contain spaces, capitalize
  // any character class. Lazy match to handle [#A#][#B#] back-to-back.
  const PLACEHOLDER_RX = /\[#([^#\]]+?)#\]/g;

  function log() {
    var args = Array.prototype.slice.call(arguments);
    console.log.apply(console, [TAG].concat(args));
  }

  // --- guards
  if (typeof Editor === 'undefined' || !Editor.Invent || !Editor.Events) {
    log('FAIL: Editor / Editor.Invent / Editor.Events missing'); return;
  }
  if (typeof Job === 'undefined' || !Job.Fields) {
    log('FAIL: Job / Job.Fields missing'); return;
  }
  if (!Editor.Invent.Variables || typeof Editor.Invent.Variables.Set !== 'function') {
    log('FAIL: Editor.Invent.Variables.Set missing — incompatible Infigo version'); return;
  }

  // --- state
  // fieldId → array of variable names that field references (a field can
  // reference multiple variables, e.g. "[#Team A#] vs. [#Team B#]")
  const fieldVariableMap = new Map();
  // variableName → array of fieldIds (reverse lookup, useful for templates
  // where one variable drives multiple fields)
  const variableFieldMap = new Map();
  // last-seen text per field (re-entry guard, dedup)
  const lastSeenText = new Map();

  let mapBuilt = false;
  let bridging = false;
  let bridgeCount = 0;

  function buildMap() {
    if (mapBuilt) return;
    try {
      const all = Job.Fields.All(null);
      let bindings = 0;
      all.forEach(function (f) {
        if (!f.text || typeof f.text.data !== 'string') return;
        const txt = f.text.data;
        // Skip empty fields — likely already substituted (post-CSV state)
        if (!txt) return;
        const matches = [];
        PLACEHOLDER_RX.lastIndex = 0;
        let m;
        while ((m = PLACEHOLDER_RX.exec(txt)) !== null) {
          matches.push(m[1].trim());
        }
        if (matches.length > 0) {
          fieldVariableMap.set(f.id, matches);
          matches.forEach(function (varName) {
            if (!variableFieldMap.has(varName)) variableFieldMap.set(varName, []);
            variableFieldMap.get(varName).push(f.id);
            bindings++;
          });
        }
      });
      mapBuilt = true;
      log('Captured ' + bindings + ' field→variable bindings across ' + fieldVariableMap.size + ' fields:');
      fieldVariableMap.forEach(function (vars, fid) {
        log('  ' + fid + ' → [' + vars.join(', ') + ']');
      });
      if (fieldVariableMap.size === 0) {
        log('WARNING: zero bindings found. Either fields have no placeholders, or CSV was already uploaded (placeholders substituted). Reload editor with no prior batch mapping.');
      }
    } catch (e) {
      log('buildMap error:', e.message, e.stack);
    }
  }

  function readCurrentText(fieldId) {
    try {
      const f = Job.Fields.ById(fieldId);
      if (!f || !f.text) return null;
      return typeof f.text.data === 'string' ? f.text.data : null;
    } catch (e) { return null; }
  }

  function pushAllVariables() {
    if (bridging) return;
    if (!mapBuilt || fieldVariableMap.size === 0) return;

    bridging = true;
    bridgeCount++;

    // Collect current text per field, dedup by variable
    const updates = {}; // varName → text
    fieldVariableMap.forEach(function (vars, fid) {
      const currentText = readCurrentText(fid);
      if (currentText === null) return;
      // Only push if changed since last seen (re-entry / no-op guard)
      const lastKey = fid;
      if (lastSeenText.get(lastKey) === currentText) return;
      lastSeenText.set(lastKey, currentText);

      // For single-variable fields, push currentText directly.
      // For multi-variable fields (e.g. "[#Team A#] vs. [#Team B#]"), we
      // can't know which token corresponds to which variable from the
      // substituted value alone — skip those for now and log.
      if (vars.length === 1) {
        updates[vars[0]] = currentText;
      } else {
        log('  Skip multi-var field ' + fid + ' (text="' + currentText + '") — can\'t deconstruct ' + vars.join('+'));
      }
    });

    const varNames = Object.keys(updates);
    if (varNames.length === 0) {
      bridging = false;
      return;
    }

    log('Bridge #' + bridgeCount + ': pushing ' + varNames.length + ' variable updates:');
    varNames.forEach(function (vn) { log('  ' + vn + ' = "' + updates[vn] + '"'); });

    // Push sequentially via callbacks. Use simple counter to release the
    // bridging flag when all are done.
    let pending = varNames.length;
    varNames.forEach(function (vn) {
      try {
        Editor.Invent.Variables.Set(vn, updates[vn], function () {
          pending--;
          if (pending === 0) {
            log('  ✓ All variable updates committed for bridge #' + bridgeCount);
            bridging = false;
          }
        });
      } catch (e) {
        log('  ✗ Variables.Set(' + vn + ') threw:', e.message);
        pending--;
        if (pending === 0) bridging = false;
      }
    });
  }

  // --- entry
  setTimeout(function () {
    log('Loaded. Building initial field→variable map…');
    buildMap();

    // Hook per-record render-complete event
    Editor.Events.Register('Fabric.Modified', pushAllVariables);
    log('Hooked Fabric.Modified. Upload CSV (if not already) and click through records.');

    // ALSO log what other Set APIs exist for future reference
    try {
      Editor.Invent.GetConnector(function (connector) {
        if (!connector) return;
        const apis = [];
        if (Editor.Invent.Variables && typeof Editor.Invent.Variables.Set === 'function')
          apis.push('Editor.Invent.Variables.Set (USED)');
        if (Editor.Invent.Batch && typeof Editor.Invent.Batch.Set === 'function')
          apis.push('Editor.Invent.Batch.Set (untried)');
        if (connector.variables && typeof connector.variables.set === 'function')
          apis.push('connector.variables.set (untried, proto)');
        if (connector.batch && typeof connector.batch.set === 'function')
          apis.push('connector.batch.set (untried, proto)');
        log('Available Set APIs:', apis.join(' | '));
      });
    } catch (e) {}
  }, 500);

  log('PROBE 7 init.');
})();
