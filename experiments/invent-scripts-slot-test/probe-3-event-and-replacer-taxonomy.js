// ============================================================================
// PROBE 3 — Event taxonomy + RegisterValueReplacer behavior
// ============================================================================
// Purpose: figure out (a) what editor events fire when CSV is uploaded and
// when records are switched in preview, and (b) whether the Invent
// RegisterValueReplacer fires per-record-render. These answers will determine
// the architecture of the real bridge.
//
// What we learned from Probe 2:
//   - Invent.Batch initializes Invent Variables ONCE on CSV upload (record 1)
//   - Per-record preview switch only re-renders field text, not variables
//   - Variable Logic only evaluates once, locking the background to record 1's value
//
// What we need to confirm here:
//   1. Does ANY editor event fire on per-record switch in preview?
//   2. Does RegisterValueReplacer fire per-render (i.e., per-record), or only
//      on variable change?
//   3. If we return a different value from the replacer, does the rendered
//      output reflect it AND does Variable Logic re-evaluate?
//
// Install:
//   Admin → MegaEdit Product Scripts → Create
//   Name:  PROBE_3_EVENT_TAXONOMY
//   ExecutionType: Editor, Enabled
//   Paste this file. Save.
//
// Attach:
//   Test product → Scripts tab → untick PROBE_2 → tick PROBE_3 → Save.
//   (Keep using the Invent Scripts slot if you want — won't hurt either way.)
//
// How to run:
//   1. Open editor on test product
//   2. Open DevTools console
//   3. Upload your CSV
//   4. Click into preview mode
//   5. Click through records 1 → 2 → 3 → ...
//   6. Capture the [PROBE 3] log lines
//
// What to look for in the output:
//   - "Event fired: <name>" lines on per-record switch → tells us the hook
//   - "Replacer called: <var> = <val>" lines per record → tells us if replacer
//     fires per-render
//   - "Replacer returning <new val>" lines → confirms our intercept ran
//
// Notes:
//   - The replacer returns the SAME value, so behavior should be unchanged.
//     This is read-only instrumentation.
//   - If replacer fires per-record, Probe 4 can use it to inject per-record
//     values that fire Variable Logic.
// ============================================================================

(function () {
  const TAG = '[PROBE 3]';
  function log() {
    var args = Array.prototype.slice.call(arguments);
    console.log.apply(console, [TAG].concat(args));
  }

  if (!Editor || !Editor.Invent || !Editor.Events) {
    log('FAIL: required APIs missing');
    return;
  }

  // -- 1. Listen for every known EditorEvent -------------------------------
  const ALL_EVENTS = [
    'Upload.Started','Upload.Finished','Upload.Finalized','Upload.Failed','Upload.Process.Stop',
    'Field.TextFlowFinished',
    'Before.Editor.OutputTypeChanged','Editor.OutputTypeChanged',
    'Before.Editor.StockChanged','Editor.StockChanged',
    'Before.Editor.CanvasChanged','Editor.CanvasChanged',
    'Before.ToggleFullScreen','ToggleFullScreen',
    'Before.OpenPreview','OpenPreview',
    'Before.ClosePreview','ClosePreview',
    'Editor.ExternalDataUpdate','Editor.Loaded',
    'SaveAsProjectPreSave','SaveAsProject',
    'AddToBasketPreSave','AddToBasket',
    'MappingSaved','BatchDataSaved',
    'Before.PageChanged','PageChanged',
    'Before.PageAdded','PageAdded',
    'Before.PageMoved','PageMoved',
    'Before.PageDeleted','PageDeleted',
    'Page.SetFill',
    'Before.LayoutChanged','LayoutChanged',
    'SaveEmbeddedPreSave',
    'Editor.UpdateViewPort','Fabric.Modified',
    'Before.Field.Insert','Before.Field.Add','Field.Add',
    'Field.ImageChanged','Field.MoveAndSize',
    'Before.Field.Delete','Field.Delete',
    'Before.Field.ZIndex.Page','Field.ZIndex.Page',
    'Before.Field.ZIndex','Field.ZIndex',
    'TextField.Text.Edit.KeyPressed','TextField.Text.Edit.Start','TextField.Text.Edit.End',
    'Editor.Selection','Field.TextResorted'
  ];

  let eventCount = 0;
  ALL_EVENTS.forEach(function (eventName) {
    try {
      Editor.Events.Register(eventName, function (data) {
        eventCount++;
        log('Event fired:', eventName, '— count:', eventCount, '— data:', JSON.stringify(data).substring(0, 200));
      });
    } catch (e) {
      // some events may not be registrable — log and continue
      log('Register failed for', eventName, ':', e.message);
    }
  });
  log('Registered listeners for', ALL_EVENTS.length, 'event types.');

  // -- 2. Hook the Invent connector for variable updates AND replacer ------
  Editor.Invent.GetConnector(function (connector) {
    if (!connector) {
      log('FAIL: no Invent connector');
      return;
    }

    let updateCount = 0;
    connector.events.registerForVariableUpdates(function (name, value) {
      updateCount++;
      log('Variable updated #' + updateCount + ':', name, '=', JSON.stringify(value));
    });
    log('Variable update listener registered.');

    let replacerCount = 0;
    connector.events.registerValueReplacer(function (name, value) {
      replacerCount++;
      log('Replacer called #' + replacerCount + ':', name, '=', JSON.stringify(value), '→ returning unchanged');
      return value; // return-as-is — pure instrumentation
    });
    log('Value replacer registered (returning values unchanged).');

    log('PROBE 3 ready. Upload CSV, open preview, click through records.');
  });
})();
