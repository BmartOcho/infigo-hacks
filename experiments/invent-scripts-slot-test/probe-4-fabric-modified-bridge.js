// ============================================================================
// PROBE 4 (v2) — Per-record bridge via Fabric.Modified hook (corrected API)
// ============================================================================
// Fixes Probe 4 v1's API guess: globals are `Job.Fields`, not
// `Editor.Document.Fields`. Text read via `field.text.data`.
// Backgrounds toggled via `field.hidden = true/false` + Job.Fields.SaveFields().
//
// Strategy:
//   1. On load, discover First Name + both background fields by ID/name
//   2. Hook Fabric.Modified (fires once per per-record render-complete)
//   3. Read First Name field's text.data
//   4. Push to Invent.Variables.Set → SHOULD fire Variable Logic
//   5. ALSO observe: read both backgrounds' `hidden` state before/after to
//      detect whether Variable Logic actually re-evaluated and toggled them
//
// Install:
//   Admin → MegaEdit Product Scripts → Create PROBE_4_FABRIC_BRIDGE
//   ExecutionType Editor, Enabled, paste this file, Save.
//   (If the script already exists, just paste the new code over the old.)
//
// Attach: Test product → Scripts tab → tick PROBE_4 → Save.
//
// Test: upload CSV, open preview, click through records. Watch console AND
// the actual background on canvas.
//
// Expected outcomes:
//   (a) Variable updates fire AND backgrounds swap per record → done, ship it
//   (b) Variable updates fire BUT backgrounds don't swap → Variable Logic
//       isn't re-evaluating on programmatic Variables.Set in batch mode.
//       Pivot to PROBE 5 (direct field manipulation).
//   (c) Variable updates fire and backgrounds swap but LAGGED by one record
//       → timing issue; we're updating post-render, need a BEFORE hook
// ============================================================================

(function () {
  const TAG = '[PROBE 4]';
  const VAR_NAME = 'First Name';
  const BG_A_ID = '00000000-0000-0000-0000-000000000435';        // observed in Probe 3
  const BG_B_ID = '441719d1-9f53-4af0-8514-22f2c97ed9c4';        // observed in Probe 3

  function log() {
    var args = Array.prototype.slice.call(arguments);
    console.log.apply(console, [TAG].concat(args));
  }

  if (typeof Editor === 'undefined' || !Editor.Invent || !Editor.Events) {
    log('FAIL: Editor / Editor.Invent / Editor.Events missing');
    return;
  }
  if (typeof Job === 'undefined' || !Job.Fields) {
    log('FAIL: Job / Job.Fields missing');
    return;
  }

  let firstNameFieldId = null;
  let bgA = null, bgB = null;

  function discover() {
    try {
      const all = Job.Fields.All(null);
      log('Total fields:', all.length);

      // First Name by name match
      const byName = Job.Fields.ByName(VAR_NAME, null, true);
      if (byName && byName.length > 0) {
        firstNameFieldId = byName[0].id;
        log('✓ Resolved First Name field by name:', firstNameFieldId);
      } else {
        log('✗ ByName lookup failed. Dumping field names for manual ID:');
        all.forEach(function (f) {
          log('  id=' + f.id + ' name="' + (f.name || '') + '" type=' + (f.type || '?'));
        });
      }

      bgA = Job.Fields.ById(BG_A_ID);
      bgB = Job.Fields.ById(BG_B_ID);
      log('Background A field:', bgA ? 'found (hidden=' + bgA.hidden + ')' : 'NOT FOUND at ' + BG_A_ID);
      log('Background B field:', bgB ? 'found (hidden=' + bgB.hidden + ')' : 'NOT FOUND at ' + BG_B_ID);
    } catch (e) {
      log('Discovery error:', e.message);
    }
  }

  let bridging = false;
  let bridgeCount = 0;
  let lastValueSeen = null;

  function readFirstNameText() {
    if (!firstNameFieldId) return null;
    try {
      const f = Job.Fields.ById(firstNameFieldId);
      if (!f) return null;
      return (f.text && typeof f.text.data === 'string') ? f.text.data : null;
    } catch (e) {
      log('readFirstNameText error:', e.message);
      return null;
    }
  }

  function snapshotBgState() {
    return {
      A: bgA ? { hidden: Job.Fields.ById(BG_A_ID) && Job.Fields.ById(BG_A_ID).hidden } : null,
      B: bgB ? { hidden: Job.Fields.ById(BG_B_ID) && Job.Fields.ById(BG_B_ID).hidden } : null
    };
  }

  function onFabricModified() {
    if (bridging) return;
    const txt = readFirstNameText();
    if (txt === null) return;
    if (txt === lastValueSeen) return;

    bridging = true;
    bridgeCount++;
    lastValueSeen = txt;
    const before = snapshotBgState();
    log('Bridge #' + bridgeCount + ': First Name text="' + txt + '" — before bgA.hidden=' + JSON.stringify(before.A) + ' bgB.hidden=' + JSON.stringify(before.B));

    Editor.Invent.Variables.Set(VAR_NAME, txt, function () {
      // Give Variable Logic a tick to react
      setTimeout(function () {
        const after = snapshotBgState();
        log('  After Variables.Set: bgA.hidden=' + JSON.stringify(after.A) + ' bgB.hidden=' + JSON.stringify(after.B));
        if (JSON.stringify(before) !== JSON.stringify(after)) {
          log('  ✓ Backgrounds CHANGED state — Variable Logic re-evaluated!');
        } else {
          log('  ✗ Backgrounds unchanged — Variable Logic did NOT re-fire on programmatic set. Need Probe 5.');
        }
        bridging = false;
      }, 100);
    });
  }

  setTimeout(function () {
    discover();
    Editor.Invent.GetConnector(function (connector) {
      if (!connector) { log('FAIL: no connector'); return; }

      connector.events.registerForVariableUpdates(function (name, value) {
        if (name === VAR_NAME) log('  ← variable update echo:', name, '=', JSON.stringify(value));
      });

      Editor.Events.Register('Fabric.Modified', onFabricModified);
      log('Hooked Fabric.Modified. Upload CSV + open preview to test.');
    });
  }, 500);

  log('PROBE 4 v2 loaded. Waiting 500ms for editor...');
})();
