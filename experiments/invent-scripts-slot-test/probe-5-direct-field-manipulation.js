// ============================================================================
// PROBE 5 — Direct background field manipulation (bypass Variable Logic)
// ============================================================================
// If Probe 4 shows variable updates fire but backgrounds don't swap, Variable
// Logic doesn't re-evaluate on programmatic set in batch mode. This probe
// bypasses Variable Logic entirely — directly toggles the two background
// fields' `hidden` property based on First Name text.
//
// Trade-off: less elegant, doesn't use Invent's rules engine, but GUARANTEED
// to work if the field IDs are correct.
//
// Install:
//   Admin → MegaEdit Product Scripts → Create PROBE_5_DIRECT_MANIPULATION
//   ExecutionType Editor, Enabled, paste this file, Save.
//
// Attach: Test product → Scripts tab → untick PROBE_4 → tick PROBE_5 → Save.
//   (Important: untick PROBE_4 so they don't fight each other.)
//
// Test: upload CSV, open preview, click through records. Background should
// swap directly per record now.
// ============================================================================

(function () {
  const TAG = '[PROBE 5]';
  const FIRST_NAME = 'First Name';
  const BG_A_ID = '00000000-0000-0000-0000-000000000435';
  const BG_B_ID = '441719d1-9f53-4af0-8514-22f2c97ed9c4';
  const TRIGGER_VALUE = '?';

  function log() {
    var args = Array.prototype.slice.call(arguments);
    console.log.apply(console, [TAG].concat(args));
  }

  if (typeof Job === 'undefined' || !Job.Fields || !Editor || !Editor.Events) {
    log('FAIL: required APIs missing');
    return;
  }

  let firstNameFieldId = null;
  let bridging = false, bridgeCount = 0, lastSeen = null;

  function discover() {
    const byName = Job.Fields.ByName(FIRST_NAME, null, true);
    if (byName && byName.length > 0) {
      firstNameFieldId = byName[0].id;
      log('Resolved First Name id:', firstNameFieldId);
    } else {
      log('FAIL: First Name field not found by name');
    }
    const a = Job.Fields.ById(BG_A_ID);
    const b = Job.Fields.ById(BG_B_ID);
    log('BG A:', a ? 'found' : 'MISSING', '| BG B:', b ? 'found' : 'MISSING');
  }

  function readText() {
    if (!firstNameFieldId) return null;
    const f = Job.Fields.ById(firstNameFieldId);
    return (f && f.text && typeof f.text.data === 'string') ? f.text.data : null;
  }

  function setBgState(showB) {
    const a = Job.Fields.ById(BG_A_ID);
    const b = Job.Fields.ById(BG_B_ID);
    if (!a || !b) { log('Cannot toggle — bg field missing'); return; }
    a.hidden = showB;  // hide A when showing B
    b.hidden = !showB; // show B when showing B
    try {
      Job.Fields.SaveFields([a, b]);
      log('  → Set bgA.hidden=' + a.hidden + ', bgB.hidden=' + b.hidden + ' (showB=' + showB + ')');
    } catch (e) {
      log('SaveFields error:', e.message);
    }
  }

  function onFabricModified() {
    if (bridging) return;
    const txt = readText();
    if (txt === null) return;
    if (txt === lastSeen) return;

    bridging = true;
    bridgeCount++;
    lastSeen = txt;
    const shouldShowB = (txt === TRIGGER_VALUE || txt.trim() === '');
    log('Switch #' + bridgeCount + ': First Name="' + txt + '" → ' + (shouldShowB ? 'Background B' : 'Background A'));
    setBgState(shouldShowB);

    setTimeout(function () { bridging = false; }, 100);
  }

  setTimeout(function () {
    discover();
    Editor.Events.Register('Fabric.Modified', onFabricModified);
    log('Hooked Fabric.Modified. Upload CSV + open preview to test direct manipulation.');
  }, 500);

  log('PROBE 5 loaded.');
})();
