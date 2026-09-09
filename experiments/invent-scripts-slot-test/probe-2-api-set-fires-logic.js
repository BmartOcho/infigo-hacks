// ============================================================================
// PROBE 2 — Does Editor.Invent.Variables.Set() fire Variable Logic?
// ============================================================================
// Purpose: the KEY question. If we set First Name to "?" via the API (not via
// the form UI), does the existing Variable Logic rule fire and swap the
// background? If YES, the bridge is viable — we just need to call this from a
// batch hook in PROBE 3. If NO, Variable Logic only listens to UI events and
// we need a different bridging strategy.
//
// Install:
//   Admin → MegaEdit Scripts → Create
//   Name:  PROBE_2_API_SET_FIRES_LOGIC
//   Paste this file as the script body. Save.
//
// Attach:
//   Same as Probe 1 — either via Scripts tab or via Invent → Setup → Scripts slot.
//
// How to run the test:
//   Open the MegaEdit editor on the test product. Open DevTools console (F12).
//   The script adds two buttons to the editor toolbar:
//     [Set First Name = ?]   ← should trigger Background B per your rule
//     [Set First Name = Alex] ← should trigger Background A
//   Click them and watch the canvas.
//
// Success signals:
//   ✓ Clicking "Set First Name = ?" swaps to Background B on canvas
//   ✓ Clicking "Set First Name = Alex" swaps back to Background A
//   ✓ Console logs "Variable updated: First Name = ?" (registered listener fires)
//
// Failure signals:
//   ✗ Variable value updates in the form field but background doesn't swap
//     → Variable Logic only listens to form events, not API sets
//     → Bridging via Variables.Set() won't work; need RegisterValueReplacer
//       OR direct field show/hide via Fields API
//   ✗ Variable value doesn't even update
//     → API set is rejected; check console for errors
// ============================================================================

(function () {
  const TAG = '[PROBE 2]';
  const TARGET_VAR = 'First Name';   // <-- change if your variable is named differently

  function log(msg) { console.log(TAG, msg); }

  if (!Editor || !Editor.Invent) {
    log('FAIL: Editor.Invent unavailable. Run Probe 1 first.');
    return;
  }

  Editor.Invent.GetConnector(function (connector) {
    if (!connector) {
      log('FAIL: no connector. Run Probe 1.');
      return;
    }

    // Register an update listener so we can see when ANYTHING changes the var
    connector.events.registerForVariableUpdates(function (name, value) {
      log('Variable updated: ' + name + ' = ' + JSON.stringify(value));
    });
    log('Listener registered for variable updates.');

    // Build the test buttons
    const btnQ = new MEUIButton('Set First Name = ?', null, function () {
      log('Setting ' + TARGET_VAR + ' to "?" via API');
      Editor.Invent.Variables.Set(TARGET_VAR, '?', function () {
        log('Set callback fired for "?"');
      });
    });

    const btnAlex = new MEUIButton('Set First Name = Alex', null, function () {
      log('Setting ' + TARGET_VAR + ' to "Alex" via API');
      Editor.Invent.Variables.Set(TARGET_VAR, 'Alex', function () {
        log('Set callback fired for "Alex"');
      });
    });

    // Drop them into the editor's main toolbar / batch area — try both
    try {
      Editor.UI.Add(null, Editor.Constants.EditorUITarget.BatchArea, btnQ);
      Editor.UI.Add(null, Editor.Constants.EditorUITarget.BatchArea, btnAlex);
      log('Buttons added to BatchArea.');
    } catch (e) {
      log('BatchArea add failed: ' + e.message + ' — trying ToolbarArea');
      try {
        Editor.UI.Add(null, Editor.Constants.EditorUITarget.ToolbarArea, btnQ);
        Editor.UI.Add(null, Editor.Constants.EditorUITarget.ToolbarArea, btnAlex);
        log('Buttons added to ToolbarArea.');
      } catch (e2) {
        log('FAIL: Could not add buttons anywhere: ' + e2.message);
      }
    }

    log('PROBE 2 ready. Click the buttons in the editor.');
  });
})();
