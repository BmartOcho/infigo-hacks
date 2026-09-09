// ============================================================================
// PROBE 9 — Direct background field manipulation (bypass Variable Logic)
// ============================================================================
// PROBE 8 confirmed: Editor.Invent.Variables.Set commits successfully per
// record but Invent's Variable Logic engine does NOT re-evaluate visibility
// rules during batch preview. Pivot: apply the rule ourselves in JS.
//
// Same architecture as PROBE 8 (parse [#Var#] → Field.TextResorted hook),
// but instead of pushing values to Variables.Set, this probe directly
// toggles the two background ImageFields' .hidden property and calls
// Job.Fields.SaveFields([bgA, bgB]).
//
// Rule applied (matches your test product's Variable Logic):
//   if First Name === "?" or empty → show Background B, hide Background A
//   else → show Background A, hide Background B
//
// Install:
//   Admin → MegaEdit Product Scripts → Create PROBE_9_DIRECT_BG
//   ExecutionType: Editor. Enabled. Paste this file. Save.
//
// Attach: untick PROBE_8 → tick PROBE_9 → Save. Reload editor.
//
// Test: upload CSV, click through records. Expected:
//   - On normal-name rows ("Jane", "Pat", etc.) → Background A shows
//   - On "?" rows → Background B shows
//
// If this works, generalize in PROBE 10 by reading Invent's rule definitions
// from connector.variables.variableController.variables[].validation /
// .regexTextManipulations so we can run any rule, not just the hardcoded "?".
// ============================================================================

(function () {
  const TAG = '[PROBE 9]';
  const PLACEHOLDER_RX = /\[#([^#\]]+?)#\]/g;

  // Known field IDs from PROBE 3/6 — verify in console if you reuse on another product
  const BG_A_ID = '00000000-0000-0000-0000-000000000435';        // default background
  const BG_B_ID = '441719d1-9f53-4af0-8514-22f2c97ed9c4';        // alternate background
  // Trigger variable + rule
  const TRIGGER_VAR = 'First Name';
  function shouldShowBackgroundB(firstNameValue) {
    if (firstNameValue === null || firstNameValue === undefined) return false;
    const trimmed = String(firstNameValue).trim();
    return trimmed === '' || trimmed === '?';
  }

  function log() {
    var args = Array.prototype.slice.call(arguments);
    console.log.apply(console, [TAG].concat(args));
  }

  if (typeof Editor === 'undefined' || !Editor.Events || typeof Job === 'undefined' || !Job.Fields) {
    log('FAIL: required APIs missing'); return;
  }

  let triggerFieldId = null;     // text field bound to First Name
  let bgA = null, bgB = null;    // cached field refs
  let mapBuilt = false;
  let applying = false;
  let applyCount = 0;
  let lastTriggerValue = null;
  let lastDecision = null;

  function buildMap() {
    if (mapBuilt) return;
    try {
      const all = Job.Fields.All(null);
      all.forEach(function (f) {
        if (!f.text || typeof f.text.data !== 'string' || !f.text.data) return;
        const txt = f.text.data;
        PLACEHOLDER_RX.lastIndex = 0;
        let m;
        while ((m = PLACEHOLDER_RX.exec(txt)) !== null) {
          if (m[1].trim() === TRIGGER_VAR) {
            triggerFieldId = f.id;
          }
        }
      });
      bgA = Job.Fields.ById(BG_A_ID);
      bgB = Job.Fields.ById(BG_B_ID);
      mapBuilt = true;
      log('Trigger field ' + TRIGGER_VAR + ' → ' + (triggerFieldId || 'NOT FOUND'));
      log('Background A: ' + (bgA ? 'found (hidden=' + bgA.hidden + ')' : 'MISSING ' + BG_A_ID));
      log('Background B: ' + (bgB ? 'found (hidden=' + bgB.hidden + ')' : 'MISSING ' + BG_B_ID));
      if (!triggerFieldId || !bgA || !bgB) {
        log('FAIL: missing one or more required fields. Probe will not run.');
      }
    } catch (e) {
      log('buildMap error:', e.message);
    }
  }

  function readTriggerText() {
    try {
      const f = Job.Fields.ById(triggerFieldId);
      return (f && f.text && typeof f.text.data === 'string') ? f.text.data : null;
    } catch (e) { return null; }
  }

  function applyRule() {
    if (applying) return;
    if (!mapBuilt || !triggerFieldId || !bgA || !bgB) return;

    const txt = readTriggerText();
    if (txt === null) return;
    const decision = shouldShowBackgroundB(txt);

    // Dedup — skip if neither value nor decision changed
    if (txt === lastTriggerValue && decision === lastDecision) return;

    applying = true;
    applyCount++;
    log('Apply #' + applyCount + ': ' + TRIGGER_VAR + '="' + txt + '" → showBgB=' + decision);
    lastTriggerValue = txt;
    lastDecision = decision;

    try {
      // Re-fetch to make sure we have current field refs
      const a = Job.Fields.ById(BG_A_ID);
      const b = Job.Fields.ById(BG_B_ID);
      if (!a || !b) { log('  ✗ bg fields missing on apply'); applying = false; return; }

      const beforeA = a.hidden, beforeB = b.hidden;
      a.hidden = decision;        // hide A when showing B
      b.hidden = !decision;       // show B when showing B

      Job.Fields.SaveFields([a, b], function () {
        log('  ✓ SaveFields done: bgA.hidden ' + beforeA + '→' + a.hidden + ', bgB.hidden ' + beforeB + '→' + b.hidden);
        applying = false;
      });
    } catch (e) {
      log('  ✗ SaveFields threw:', e.message);
      applying = false;
    }
  }

  setTimeout(function () {
    log('Loading…');
    buildMap();

    // Hook the per-record event that PROBE 8 proved reliable
    Editor.Events.Register('Field.TextResorted', function () {
      // We don't care about the payload — just re-read the trigger field's text
      applyRule();
    });
    log('Hooked Field.TextResorted. Upload CSV (if not already) and click through records.');
    log('Rule: First Name === "" or "?" → show Background B; else show Background A');
  }, 500);

  log('PROBE 9 init.');
})();
