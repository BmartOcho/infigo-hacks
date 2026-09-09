# Invent Scripts Slot — Phased Test Checklist

**Goal:** answer two questions empirically before Infigo support replies Tuesday:
1. Does the **Invent → Setup → Other → Scripts** field actually auto-attach a MegaScript to the exported product? (The undocumented field.)
2. Can a MegaScript reliably bridge **CSV batch upload → Invent Variable Logic** so backgrounds swap per-record?

**Test product:** the existing non-production product with the "First Name contains '?' → Background B" Variable Logic rule already wired.

**Test CSV:** `test-csv.csv` in this folder. 5 rows, two with "?" in First Name, three with normal names. Expected if the bridge works: rows 2 & 4 render with Background B, rows 1/3/5 with Background A.

---

## Phase 0 — Free observation (DONE)

**Result:** Scripts field expects the NAME of an existing MegaScript in Admin → MegaEdit Scripts. The Invent UI itself accepts any text, but the validation happens on MEX import: if the name doesn't resolve to a real script, import fails with `Admin.Mex.UiMessages.Scripts.Normal.NotFound`. "Normal" = custom (non-hardcoded). See `RESULTS.md`.

**Consequence for the rest of the plan:** Phase 4 (the Invent slot test) is now testable end-to-end in a single pass — create the MegaScript in Admin first, then reference it from the Invent slot. Phase 1 and Phase 4 can be done together; no need for the manual Scripts-tab attach as an isolation step (though we keep it as a fallback below).

---

## Phase 1+4 (combined) — Detect connector AND test Invent slot in one pass (15 min)

Phase 0 told us the slot expects a script name and validates on import. So we test both questions in one motion.

- [ ] Infigo Admin → MegaEdit Scripts → Create.
- [ ] Name: `PROBE_1_DETECT_CONNECTOR` (EXACT name — case-sensitive likely).
- [ ] Paste contents of `probe-1-detect-connector.js`. Save.
- [ ] InDesign → Invent panel → Setup → Other → Scripts field → type `PROBE_1_DETECT_CONNECTOR` → Enter.
- [ ] Re-export MEX to a local folder (not OneDrive/Dropbox — see `invent-mex-export-troubleshoot`).
- [ ] Infigo admin → upload the new MEX as a new product (or re-import to the test product).
- [ ] **Import success check:** MEX import should now succeed (no `NotFound` error).
- [ ] Open the imported product in admin → **Scripts tab** → is `PROBE_1_DETECT_CONNECTOR` auto-ticked?
- [ ] Open the storefront → open the product in MegaEdit editor → F12 console → look for `[PROBE 1]` messages.

**Capture in `RESULTS.md` (under "Phase 1+4 combined"):**
- [ ] MEX import succeeded? YES / NO
- [ ] Script auto-ticked on Scripts tab? YES / NO  ← this is the Invent slot answer
- [ ] Was `Editor.Invent` defined?
- [ ] Did `GetConnector` return a connector?
- [ ] Variable names listed (confirm "First Name" appears)?

**Gate:**
- If script did NOT auto-tick but import succeeded: the slot stores the reference but doesn't auto-enable. You'd need to manually tick. Still useful but less elegant.
- If `Editor.Invent` is undefined: stop and ticket Infigo.

**Fallback if anything fails:** manually tick PROBE_1 on the Scripts tab and proceed — that isolates whether the connector itself works, even if the Invent slot doesn't auto-wire it.

---

## Phase 2 — Does API set fire Variable Logic? (15 min)

The critical question. **Manual attach only.**

- [ ] Admin → MegaEdit Scripts → Create.
- [ ] Name: `PROBE_2_API_SET_FIRES_LOGIC`.
- [ ] Paste `probe-2-api-set-fires-logic.js`. Save.
- [ ] Open test product → Scripts tab → tick PROBE_2 → untick PROBE_1 → Save.
- [ ] Reload the editor. Look for two buttons: `Set First Name = ?` and `Set First Name = Alex`.
- [ ] Click `Set First Name = ?`. **Watch the canvas for a background swap.**
- [ ] Click `Set First Name = Alex`. **Watch for swap back.**

**Capture in `RESULTS.md`:**
- [ ] Did the form field value update?
- [ ] Did the background swap when the API set "?"?
- [ ] Did the listener log `Variable updated: First Name = ?`?

**Decision point:**
- **Both swapped + listener fired** → Variable Logic listens to API sets. Proceed to Phase 3.
- **Form value updated but background didn't swap** → Variable Logic is form-event-only. Skip to Phase 4 (RegisterValueReplacer fallback).
- **Value didn't update** → API set is rejected. Check console; likely a permission or naming issue.

---

## Phase 3 — Real batch bridge (20 min, the actual prize)

Only run if Phase 2 succeeded.

- [ ] Admin → MegaEdit Scripts → Create.
- [ ] Name: `PROBE_3_BATCH_BRIDGE`.
- [ ] Paste `probe-3-batch-bridge.js`. Save.
- [ ] Open test product → Scripts tab → tick PROBE_3 → untick PROBE_2 → ensure Standard Batch Script is still ticked → Save.
- [ ] Open editor on test product. Upload `test-csv.csv` via the batch upload flow.
- [ ] Watch console for `[PROBE 3]` messages.
- [ ] Watch the per-record preview.

**Capture in `RESULTS.md`:**
- [ ] Did `BatchDataSaved` event fire? (look for the log line)
- [ ] What shape did `LoadPreview` data have? (paste the JSON it logged)
- [ ] Did records 2 & 4 (the "?" rows) render with Background B?
- [ ] Did records 1/3/5 render with Background A?
- [ ] Any backgrounds wrong? Note which rows.

**Possible outcomes:**
- **All correct** → bridge works. Promote to a clean production script. Document the fix in `RESULTS.md`.
- **All records rendered with the SAME background** (whichever the last API call set) → renderer doesn't re-evaluate Variable Logic per record. Fall back to Phase 4.
- **No swap at all** → BatchDataSaved fires too late or LoadPreview gives wrong data. Capture and we'll iterate.

---

## Phase 4 — Test the Invent Scripts slot itself (the original question)

If Phases 1–3 worked with manual attach, now test whether **Invent → Setup → Other → Scripts** auto-attaches the same script.

- [ ] Untick all three PROBE scripts from the test product's Scripts tab → Save. Confirm batch upload no longer swaps backgrounds.
- [ ] Open InDesign → Invent panel → Setup → Other → Scripts field.
- [ ] Type the script name (based on Phase 0 observation — name, ID, or whatever format the field accepts). For our case: `PROBE_3_BATCH_BRIDGE` or its admin ID.
- [ ] Re-export the MEX to a local folder (NOT cloud-synced — see `invent-mex-export-troubleshoot`).
- [ ] In Infigo admin, re-upload the new MEX to the test product.
- [ ] Open the test product → Scripts tab. **Is PROBE_3 auto-ticked?**
- [ ] Open editor → upload `test-csv.csv` → confirm bridge still works.

**Capture in `RESULTS.md`:**
- [ ] Did re-uploading the MEX auto-tick the script on Scripts tab?
- [ ] Did the bridge still work after MEX re-import?
- [ ] What did Invent put in the Scripts field — name? ID? other?

If this works: **the Invent Scripts slot IS the intended bridge mechanism**, and we've reverse-engineered the undocumented surface. Update memory + docs accordingly.

---

## Phase 5 — Cleanup

- [ ] Untick all PROBE scripts from test product. Save.
- [ ] Delete the three PROBE scripts from Admin → MegaEdit Scripts (optional — they're harmless if left).
- [ ] Empty/clear `test-csv.csv` upload from test product.
- [ ] If Phase 3 succeeded, rename/promote the working script to e.g. `INVENT_BATCH_BRIDGE` and document.

---

## What to capture in `RESULTS.md`

Just paste console output blocks and a one-line outcome per phase. Don't write a report — we'll synthesize into the hack file together once results are in.

Format:
```
## Phase 0
- Scripts field: accepted/rejected — [paste behavior]
- Hardcoded Scripts: same

## Phase 1
[paste console output]
Outcome: pass / fail / partial

## Phase 2
[paste console output]
Did background swap on API set? YES / NO

## Phase 3
[paste console output]
Records that rendered Background B: row numbers
Records that rendered Background A: row numbers

## Phase 4
Auto-tick on Scripts tab? YES / NO
Bridge still works? YES / NO
```
