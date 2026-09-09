// ============================================================================
// PROBE 3 — Batch → Invent Variable bridge (THE REAL TEST)
// ============================================================================
// Purpose: actually wire CSV batch upload into the Variable Logic engine.
// Listens for the BatchDataSaved event, reads the mapped batch data via
// Job.Batch.LoadPreview, and for each record pushes the First Name value into
// the Invent variable.
//
// PRECONDITION: only run this if Probe 2 confirmed that Variables.Set() fires
// Variable Logic. If Probe 2 failed, we need a different strategy.
//
// Install:
//   Admin → MegaEdit Scripts → Create
//   Name:  PROBE_3_BATCH_BRIDGE
//   Paste this file as the script body. Save.
//
// Attach:
//   Same options as Probes 1 & 2. For real CSV testing, attach via the
//   Scripts tab on the test product.
//
// How to run:
//   Open the MegaEdit editor on the test product. Upload your test CSV that
//   has a "?" in the First Name column of at least one row. Watch the console
//   AND the preview rendering of each record.
//
// Success signal (the one we actually care about):
//   ✓ Records where First Name = "?" show Background B in the preview
//   ✓ Records with normal First Name show Background A
//   ✓ Console shows "[PROBE 3] Bridged row N: First Name=? → set"
//
// Caveat / known unknown:
//   Variable Logic evaluates the CURRENT variable state when it fires. Batch
//   renders N records sequentially. If the renderer doesn't re-evaluate
//   Variable Logic per record, this approach won't work — and we'd need to
//   either (a) use RegisterValueReplacer (per-value-use hook), or (b)
//   directly toggle Fields visibility per row inside the render loop.
//
// If this probe fails to swap backgrounds per-record despite the API calls
// working, capture which records DID render with which background, then we
// pivot to PROBE 4 (RegisterValueReplacer).
// ============================================================================

(function () {
  const TAG = '[PROBE 3]';
  const TARGET_VAR = 'First Name';
  const TRIGGER_VALUE = '?';

  function log(msg) { console.log(TAG, msg); }

  if (!Editor || !Editor.Invent || !Editor.Events || !Job || !Job.Batch) {
    log('FAIL: required APIs missing. Editor.Invent + Editor.Events + Job.Batch');
    return;
  }

  function bridgeBatchData() {
    log('BatchDataSaved fired — reading mapped preview...');

    // Pull a generous record count for preview
    Job.Batch.LoadPreview(1000, function (mappedData) {
      log('LoadPreview returned: ' + JSON.stringify(mappedData));

      // mappedData shape per the type defs: { [variableName]: string }
      // but it's a SINGLE record's mapping (the preview rendering).
      // For batch render, each record gets its own pass. So setting the
      // variable here only affects the current preview snapshot.
      // We log what we see so we can confirm shape empirically.

      if (mappedData && mappedData[TARGET_VAR] !== undefined) {
        const v = mappedData[TARGET_VAR];
        log('Mapped ' + TARGET_VAR + ' = ' + JSON.stringify(v));

        Editor.Invent.Variables.Set(TARGET_VAR, v, function () {
          log('Pushed value to Invent variable. Variable Logic should now evaluate.');
        });
      } else {
        log('WARN: ' + TARGET_VAR + ' not present in mappedData keys: '
            + JSON.stringify(Object.keys(mappedData || {})));
      }
    });
  }

  // Register the hook
  Editor.Events.Register(EditorEventType.BatchDataSaved, function (data) {
    log('Event received with data: ' + JSON.stringify(data));
    bridgeBatchData();
  });

  log('PROBE 3 ready. Upload a CSV to trigger BatchDataSaved.');
})();
