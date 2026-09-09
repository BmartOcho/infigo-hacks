# Recording Runbook — Pre-Ticket Re-Verification

Goal: produce one screen recording + one fresh `RESULTS-rerun.md` console transcript that proves every claim in the support ticket. ~25 min total.

## Setup (do once, before recording)

1. **Storefront admin → MegaEdit Product Scripts**. Confirm five scripts exist:
   - `PROBE_1_DETECT_CONNECTOR`
   - `PROBE_2_API_SET_FIRES_LOGIC`
   - `PROBE_3_BATCH_BRIDGE` (or the event-taxonomy variant)
   - `PROBE_4_FABRIC_BRIDGE`
   - `PROBE_5_DIRECT_MANIPULATION`
   - `PROBE_6_FIELD_DISCOVERY` ← new, create from `probe-6-field-identifier-discovery.js`
2. **Test product**: untick ALL probe scripts → Save. Clean slate.
3. **Recording app**: OBS / ScreenPal / whatever. 1080p, capture browser window + console. Mic off unless you want narration.
4. **Browser**: dedicated incognito window, F12 console open, Console filter set to default (no filtering — we want everything).

## Recording structure (one continuous take)

Open the recording with this slate visible in console (paste manually):
```
console.log('=== INFIGO HACKS — INVENT/CSV/VARIABLE LOGIC BRIDGE — RE-VERIFICATION ' + new Date().toISOString() + ' ===');
```

### Segment 1 — PROBE 1 (connector sanity) — 2 min
- Test product → Scripts tab → tick PROBE_1 only → Save
- Open editor on test product
- Console should show: `[PROBE 1] Editor.Invent exists`, `Connector initialized: true`, `Variables found (6)`
- Speak/note: "Confirms the Invent connector is reachable and lists 6 variables."

### Segment 2 — PROBE 2 (variables on CSV upload) — 4 min
- Scripts tab → untick PROBE_1, tick PROBE_2 → Save
- Reload editor
- Confirm `Listener registered for variable updates` in console
- Upload `test-csv.csv`
- **Expected:** exactly 6 `Variable updated:` lines fire, all with record-1 values
- Click through preview records 2 → 3 → 4 → 5
- **Expected:** NO additional `Variable updated:` lines. Background does NOT swap on the "?" rows.
- Speak/note: "This is the gap — Invent pushes record 1 once, then goes silent."

### Segment 3 — PROBE 3 (event taxonomy) — 4 min
- Scripts tab → untick PROBE_2, tick PROBE_3 (event taxonomy variant) → Save
- Reload editor, upload CSV
- Click through records 2 → 3 → 4 → 5
- **Expected per record switch:** `Fabric.Modified × 1`, `Field.TextResorted × ~4–5`, `Field.ImageChanged × ~4–6`, NO `BatchDataSaved` or `MappingSaved`
- Speak/note: "Fabric.Modified is the only clean per-switch hook."

### Segment 4 — PROBE 4 (blocked: name-based ByName) — 3 min
- Scripts tab → untick PROBE_3, tick PROBE_4 → Save
- Reload editor
- **Expected:** `✗ ByName lookup failed. Dumping field names for manual ID:` followed by field list where every `name=""`
- Upload CSV, click through records
- **Expected:** PROBE 4 cannot identify First Name field; bridge never engages
- Speak/note: "This is the block. Field names are empty."

### Segment 5 — PROBE 5 (blocked: same name issue) — 2 min
- Scripts tab → untick PROBE_4, tick PROBE_5 → Save
- Reload editor
- **Expected:** `FAIL: First Name field not found by name`
- Speak/note: "Direct manipulation also blocked — same identifier problem."

### Segment 6 — PROBE 6 (discovery — the new work) — 6 min
- Scripts tab → untick PROBE_5, tick PROBE_6 → Save
- Reload editor
- **Expected:** Console fills with Attempts A–F output. Focus on:
  - **Attempt A:** Look for any non-noise key on text fields that resembles linkage (`customData`, `tags`, `placeholders`)
  - **Attempt B:** `ByTags` results — even one hit is gold
  - **Attempt C:** Placeholder regex matches — if `{{First Name}}` is embedded in field text, we have an identifier
  - **Attempt D:** Connector methods — any `★ Found connector.X` line is gold
  - **Attempt E:** Window-scope leaks
- Upload CSV
- **Expected:** Attempt A + C re-run on `BatchDataSaved` — observe whether field text shape changes
- Speak/note: outcome — "Found a viable identifier path: X" OR "All six attempts dead — ticket is warranted."

### Segment 7 — Cleanup & wrap — 1 min
- Untick PROBE_6 → Save
- Console: `console.log('=== RE-VERIFICATION COMPLETE ' + new Date().toISOString() + ' ===');`
- Stop recording.

## After recording

1. **Save console output**: right-click console → Save as... → `RESULTS-rerun-2026-05-26.txt` in this folder
2. **Save recording**: name it `invent-bridge-reverification-2026-05-26.mp4` (or whatever your tool exports)
3. **Update `RESULTS.md`**: append a "Re-verification 2026-05-26" section pointing at the new files
4. **Update PROBE 6 outcome**: if Attempt A/B/C/D found a path, draft PROBE 7 to exploit it. If all dead, paste the relevant Attempt-D output into the support ticket as the "we exhausted public APIs" exhibit.

## Decision points after recording

- **PROBE 6 found a viable identifier (tags / customData / placeholder / connector method)** → cancel/de-prioritize the ticket OR send a much shorter ticket (just the side bugs). Write PROBE 7 to exploit and ship the bridge.
- **PROBE 6 found nothing** → send ticket as drafted, attach recording + console transcript. The recording is exactly the evidence the ticket needs.
- **PROBE 6 found partial info** (e.g., a method exists but throws) → send ticket with a more targeted Q1: "We found `connector.X` but it threw `Y` — what's the supported way to call it?"
