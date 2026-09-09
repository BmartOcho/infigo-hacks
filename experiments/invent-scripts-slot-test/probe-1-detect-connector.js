// ============================================================================
// PROBE 1 — Detect Invent connector + dump current variable state
// ============================================================================
// Purpose: confirm Editor.Invent is reachable from a custom MegaScript on this
// product, list all Invent variables it can see, and dump their current values.
//
// How to install:
//   Admin → MegaEdit Scripts → Create
//   Name:  PROBE_1_DETECT_CONNECTOR
//   Paste this entire file as the script body
//   Save.
//
// How to attach (two ways — TEST BOTH):
//   A. Manual: open the test product → Scripts tab → tick PROBE_1_DETECT_CONNECTOR → Save
//   B. Via Invent: open InDesign → Invent panel → Setup → Other → Scripts field
//      → type "PROBE_1_DETECT_CONNECTOR" → press Enter → re-export MEX
//      → re-upload MEX to the test product → check Scripts tab to see if it
//      auto-ticked.
//
// How to read the result:
//   Open the MegaEdit editor on the test product. Open browser DevTools console
//   (F12). Look for messages prefixed "[PROBE 1]".
//
// Success signals:
//   ✓ "Connector initialized: true"  → Invent bridge is live on this product
//   ✓ "Variables found: [...]"       → script can SEE Invent vars by name
//   ✓ "First Name = ..."             → script can READ current values
//
// Failure signals to capture:
//   ✗ "GetConnector returned null"   → bridge unavailable (likely a non-Invent product)
//   ✗ "Editor.Invent is undefined"   → API not exposed in this Infigo version
//   ✗ No console output at all       → script never ran (scripts tab issue or syntax error)
// ============================================================================

(function () {
  const TAG = '[PROBE 1]';

  function log(msg) {
    console.log(TAG, msg);
  }

  log('Script loaded at ' + new Date().toISOString());

  if (typeof Editor === 'undefined') {
    log('FAIL: Editor global is undefined');
    return;
  }

  if (typeof Editor.Invent === 'undefined') {
    log('FAIL: Editor.Invent is undefined — Invent API not exposed in this build');
    return;
  }

  log('Editor.Invent exists, requesting connector...');

  Editor.Invent.GetConnector(function (connector) {
    if (!connector) {
      log('FAIL: GetConnector returned null — Invent script not loaded on this product');
      return;
    }

    log('Connector initialized: ' + connector.initialized);

    const names = connector.variables.listVariableNames();
    log('Variables found (' + names.length + '): ' + JSON.stringify(names));

    names.forEach(function (n) {
      const v = connector.variables.get(n, false);
      log('  ' + n + ' = ' + JSON.stringify(v));
    });

    log('PROBE 1 complete.');
  });
})();
