# Test Results — Invent Scripts Slot

Paste console output + brief observations as you go. Don't pretty it up — we'll synthesize at the end.

## Phase 0 — Field format probe

- **Scripts field accepts what format: existing-MegaScript NAME (validated on import).**
  Typed arbitrary text in the field, exported MEX, tried to import to a new product → import rejected with:
  `Import Error: Resources Scripts Node. Admin.Mex.UiMessages.Scripts.Normal.NotFound`
  The error key tells us: MEX import processes a Scripts node, looks up "Normal" (= custom, non-hardcoded) scripts by name in the storefront's MegaEdit Scripts list, and rejects the MEX if it can't find a match.
- **Hardcoded Scripts field accepts what format: name of an existing hardcoded (Infigo-built) script (validated on import).** Confirmed empirically — typed `testing`, MEX import failed with `Import Error: Resources Scripts Node. Hardcoded script testing was not found`. Same lookup pattern as the Normal field. Useful if you want to enable e.g. `Standard Batch Script` directly from Invent rather than ticking it on the product Scripts tab in admin. Requires the hardcoded script to actually exist (and likely be permission-enabled) in the storefront.
- **Localization note (minor Infigo bug):** Hardcoded error is fully English-localized but Normal error shows the raw translation key (`Admin.Mex.UiMessages.Scripts.Normal.NotFound`). Storefront language strings table is missing the Normal-path key.
- **Implication:** must create the MegaScript in Admin → MegaEdit Scripts FIRST, then put its exact name in the Invent Scripts field, then re-export MEX. Import will then succeed and (we hypothesize) the script will be auto-attached to the product on import.

## Phase 1+4 (combined) — Detect connector AND Invent slot auto-attach

**Setup:** PROBE_1_DETECT_CONNECTOR created in Admin (ExecutionType: Editor, Enabled), name typed into Invent → Setup → Other → Scripts field, MEX re-exported, re-imported as new product (id 346, job 10621).

**Result: SUCCESS on both questions.**

Auto-load sequence in console:
```
1: Loaded external script: 2570 name: InDesign
2: Loaded external script: 2571 name: PROBE_1_DETECT_CONNECTOR
3: Loaded external script: 2572 name: InDesign.Batch
```
PROBE_1 (id 2571) auto-attached on product import without manually ticking — confirms the Invent Scripts slot IS the auto-attach mechanism.

Connector output:
```
[PROBE 1] Script loaded at 2026-05-22T19:33:13.597Z
[PROBE 1] Editor.Invent exists, requesting connector...
[PROBE 1] Connector initialized: true
[PROBE 1] Variables found (6): ["First Name","Last Name","Dealership Name","Event Date","Team A","Team B"]
[PROBE 1]   First Name = ""
[PROBE 1]   Last Name = ""
[PROBE 1]   Dealership Name = ""
[PROBE 1]   Event Date = ""
[PROBE 1]   Team A = ""
[PROBE 1]   Event Date = ""
[PROBE 1]   Team A = ""
[PROBE 1]   Team B = ""
[PROBE 1] PROBE 1 complete.
```

**Bonus architectural discovery from batch-CSV upload stack traces:**

When user uploaded the CSV and clicked through preview records, console showed Invent's own `InDesign.Batch` script (id 2572) handling per-record rendering. Call chain on every record preview:

```
setupRecord (PreviewPlugin)
  → _GenerateClientSidePreview
  → BatchInfoRetriverFns.Text (InDesign.Batch)
  → getFieldData
  → replaceTextValue
  → replaceValue
  → PerformFieldDataReplacement
  → FieldHandlers.SetTextAsLimitedHtml
```

**Translation:** Invent's batch script writes CSV values **directly into field text** via `SetTextAsLimitedHtml`. It **never calls `Editor.Invent.Variables.Set()`**. This is the architectural cause of the Variable-Logic-doesn't-fire-on-batch gap — Invent's own batch handler bypasses the variable layer.

**Side warning observed** (worth a separate ticket): `Multiple placeholders found in text field, only one is supported when using validation` — fires from `InDesign.Batch:2249 getVariableLinkedToFields`. Limit of one placeholder per text field when validation is on.

Outcome: **PASS** — proceed to Phase 2.

## Phase 2 — API set fires Variable Logic?

**Setup:** PROBE_2_API_SET_FIRES_LOGIC ticked on test product. Real CSV (52 mapped records) uploaded to test product.

**Button click test: inconclusive.** Buttons added to BatchArea per log (`Buttons added to BatchArea.`), but no `[PROBE 2] Setting…` or `Set callback fired` lines appeared in console. Either user didn't click, or click handlers didn't fire silently. Sidelined — CSV upload gave better data.

**The actual finding — Invent DOES use Editor.Invent.Variables.Set() during batch load:**

```
[PROBE 2] Listener registered for variable updates.
[PROBE 2] Buttons added to BatchArea.
[PROBE 2] PROBE 2 ready. Click the buttons in the editor.
...
[after CSV upload]
[PROBE 2] Variable updated: First Name = "Jane"
[PROBE 2] Variable updated: Last Name = "Doe"
[PROBE 2] Variable updated: Dealership Name = "Example Awards-100"
[PROBE 2] Variable updated: Event Date = "January 1st, 2026"
[PROBE 2] Variable updated: Team A = "team-100"
[PROBE 2] Variable updated: Team B = "team-4300"
```

So all 6 Invent Variables got set — to record 1's values — exactly once on CSV upload. **No subsequent Variable updates fired** as user clicked through records 2/3/4/etc., despite per-record `SetTextAsLimitedHtml` calls being visible in stack traces (the field text re-renders, but variables stay frozen on record 1).

**Revised model of the gap:**
1. CSV upload → InDesign.Batch initialization pushes record 1's values into Invent Variables
2. Variable Logic evaluates once with record 1's First Name ("Jane" — not "?")
3. Background A locks in for all subsequent records
4. Per-record preview switch only re-renders field TEXT via `SetTextAsLimitedHtml` — Invent Variables stay at record 1
5. Variable Logic never re-evaluates per record → background never swaps

The bridge IS plumbed, but only fires once. To make Variable Logic work per record, we need to call `Editor.Invent.Variables.Set('First Name', value)` on each preview record switch.

**Outcome: partial pass.** API set fires Variable Logic (proven by record 1 swap working in the original use case where First Name on record 1 was "?" — the user's earlier "non-batch test" with form input was structurally identical to record 1 of a batch). But per-record re-evaluation is the missing piece. Proceed to Phase 3 with a per-record-switch hook.

## Phase 3 — Event taxonomy + replacer behavior

**Definitive findings — clears the path for Probe 4:**

1. **`RegisterValueReplacer` is one-shot, not per-render.** Fired exactly 8 times immediately after `MappingSaved` (one per variable, including a duplicate on Team A/B), then ZERO times during 130+ subsequent preview events. Not viable as a per-record hook.

2. **Per-record preview switch fires field-level events (the bridge hooks we need):**
   - `Field.TextResorted` × ~4–5 per switch (one per text field, after Invent.Batch writes the new record's text)
   - `Field.ImageChanged` × ~4–6 per switch (BOTH background fields re-evaluate every switch — IDs `00000000-0000-0000-0000-000000000435` and `441719d1-9f53-4af0-8514-22f2c97ed9c4`)
   - `Fabric.Modified` × 1 per switch (render complete)

3. **Notably absent on per-record switch:** `BatchDataSaved`, `MappingSaved`, `OpenPreview`, `PageChanged`, any record-specific event. Preview iframe handles record switching internally.

4. **Text field IDs (in canvas order):** `...304`, `...331`, `...356`, `...380`, `...403` — five text fields matching 6 variables (First Name, Last Name, Dealership Name, Event Date, Team A, Team B — likely Team A and Team B share a field or one is image-based).

5. **Background field IDs:** `00000000-0000-0000-0000-000000000435` (likely Background A — zIndex 0) and `441719d1-9f53-4af0-8514-22f2c97ed9c4` (likely Background B — zIndex 6). Both fire ImageChanged on every record switch — suggests both ARE being re-evaluated per record, but with stale variable values.

**Bridge architecture (for Probe 4):**
- Hook `Fabric.Modified` (one event per switch, post-render)
- Read First Name text field's current text (Invent.Batch already wrote the new record's value there)
- Call `Editor.Invent.Variables.Set('First Name', textValue)` → triggers Variable Logic re-evaluation
- Use re-entry guard to prevent infinite loops
- Fallback: if Variable Logic doesn't re-evaluate, manipulate the two background fields' visibility directly

**Outcome: pass — clear path to Probe 4.**

## Phase 4 — Invent Scripts slot auto-attach

- Scripts field value entered:
- Auto-ticked on Scripts tab after MEX re-import? YES / NO
- Bridge still works post re-import? YES / NO
- Notes:

---

## Phase 6 — Field identifier discovery (2026-05-26)

**Setup:** PROBE_6_FIELD_DISCOVERY ticked on test product (job 10640). Editor opened, CSV uploaded. No record clicks before logs captured.

**Outcome: BREAKTHROUGH — Attempt C found the linkage.**

Invent embeds placeholders directly in `field.text.data` and `field.text.internalText` using the syntax `[#Variable Name#]`. Pre-batch state (before CSV upload):

| Field ID | text.data | Bound to |
|---|---|---|
| `00000000-0000-0000-0000-000000000304` | `[#Event Date#]` | Event Date |
| `00000000-0000-0000-0000-000000000331` | `[#Team A#] vs. [#Team B#]` | Team A + Team B |
| `00000000-0000-0000-0000-000000000356` | `[#First Name#]` | **First Name** |
| `00000000-0000-0000-0000-000000000380` | `[#Last Name#]` | Last Name |
| `00000000-0000-0000-0000-000000000403` | `[#Dealership Name#]` | Dealership Name |

The "Multiple placeholders found in text field" warning fires precisely on field `...331` — that's the Team A/Team B compound field. Confirms the warning correlates with `[#X#] ... [#Y#]` patterns.

Field `...356` has an internal quirk: `internalText: "[#First \nName#]"` (null byte + newline encoding inside). `data` is clean. Parse `data`, not `internalText`.

**Attempt-by-attempt:**
- **Attempt A (property enumeration):** No `customData`, `tags`, `metadata`, `binding`, or `invent` keys on any field. Top-level keys uniform across all 7 fields.
- **Attempt B (ByTags lookup):** 0 results for every candidate. Not the mechanism.
- **Attempt C (placeholder regex):** WIN. Detected `[#First Name#]` in field `...356`.
- **Attempt D (connector introspection):** `Editor.Invent` keys = `GetConnector, Variables, Events, Batch`. Connector keys = `_initialized, variables, events, batch, initialized (proto), ready (proto)`. `connector.events` exposes `updateCallbacks, replaceCallbacks, registerForVariableUpdates (proto), registerValueReplacer (proto), replaceValue (proto), variableUpdated (proto)`. `connector.batch` — keys not yet dumped, see PROBE 6.5.
- **Attempt E (window scope):** Nothing leaked. `getVariableLinkedToFields` is internal to InDesign script only.
- **Attempt F (page-level):** Pages carry a `tags` key — content not dumped in this probe, see PROBE 6.5.

**Post-batch state:** After CSV upload, `text.data` is empty string (or substituted value). Placeholders are stripped during batch substitution. **Linkage MUST be captured at script load, before any record is rendered.**

**Critical implication for PROBE 7:** Build the fieldId→variableName map exactly once on script init by parsing `[#...#]` from each text field's `data`. Cache it. Then `Fabric.Modified` hook reads current text from the cached First Name field ID and pushes to `Editor.Invent.Variables.Set`.

**Side findings:**
- `connector.batch` exists but contents unexplored — possibly a more supported API path than text parsing. PROBE 6.5 explores this.
- `BatchDataSaved` event DOES fire after CSV upload (re-ran Attempt A on this event successfully). Earlier RESULTS.md claim that "BatchDataSaved doesn't fire" — needs re-check.
- After CSV upload, `internalText` for the Team A field is `" vs. "` — placeholders stripped, only the literal " vs. " between them survives. Confirms substitution is destructive of the linkage signal post-upload.

**Ticket status:** Original ticket draft (5 questions) is now overkill. Two questions remain worth asking eventually:
1. Is `connector.batch` (or any of its methods) a supported field/variable lookup API?
2. Side bugs: `Admin.Mex.UiMessages.Scripts.Normal.NotFound` localization + `Multiple placeholders` warning legitimacy.

Hold the ticket until PROBE 7 ships. If the bridge works end-to-end, side bugs can ship as a small low-priority ticket later.

---

## Phase 6.5 — connector.batch + page.tags introspection (2026-05-26)

**Setup:** PROBE_6_5_CONNECTOR_BATCH ticked on test product. Editor loaded, CSV uploaded, clicked through several records.

**Findings:**

### `page.tags = []`
Pages carry the `tags` key but it's empty for the test product. Not the linkage mechanism.

### `Editor.Invent.Batch` is public
- `Editor.Invent.Batch = { Set: [fn] }` — a single `Set` method, available without `GetConnector`.
- This is the documented v1.0.19 public API surface.
- Not yet exercised, but possibly the preferred call vs. `Editor.Invent.Variables.Set`.

### `connector.batch` is rich
- `connector.batch` keys: `batchController, set [proto/function]`
- `connector.batch.batchController` contains:
  - `dataController` — manages job/document data
  - `variableController` — owns the variables collection
  - `documentBatch`, `editorUI`, `config`
- `connector.batch.batchController.variableController.variables` = array of 6 variable objects, each with keys: `id, name, dynamicName, ui, parent, variableScope, batchSource, type, mode, validation, prepopulation, defaultValue, regexTextManipulations`
- `connector.batch.batchController.variableController.mapping` = type-keyed function map: `{ NONE, TEXT, COLOR, DROPDOWN, DATE, BOOLEAN, NUMBER, IMAGE, TIME }`. Likely the per-type value conversion / set handlers.

### `connector.variables` — the supported proto methods
Most important finding from this probe:
- `connector.variables.listVariableNames()` (proto, fn)
- `connector.variables.get()` (proto, fn)
- `connector.variables.set()` (proto, fn)

**Three SetVariable APIs now known:**
| Path | Confirmed working? |
|---|---|
| `Editor.Invent.Variables.Set(name, value, cb)` | ✓ PROBE 2 confirmed |
| `Editor.Invent.Batch.Set(...)` | untried — signature unknown |
| `connector.variables.set(...)` | untried — signature unknown |
| `connector.batch.set(...)` | untried — signature unknown |

### `Job.Fields` method inventory
`Constants, Map, All, ById, ByIds, ByName, ByPagesAndTags, ByTags, ByPages, CreateCustomField, CreateField, DeleteField, CopyField, GetTextFlowChain, SaveFields, MeasureFieldText, GetTextAsHtml, SetTextAsLimitedHtml, SetImageScale, GetFitToBoxFontSize, RenderCustomField, SaveFieldResource, ClearFieldResourceCategory, DeleteFieldResource, GetFieldResourceLinks, Render`

No `ByVariable` or similar. Confirms the field→variable lookup must come from text-parsing or from walking the internal variable controller.

### Stack traces confirm the architectural gap
During the user's per-record clicks, `getVariableLinkedToFields` (the internal method at InDesign:2249) fires repeatedly, called from `setupRecord → _GenerateClientSidePreview → BatchInfoRetriverFns.Text → getFieldData → replaceTextValue → replaceValue → PerformFieldDataReplacement → SetTextAsLimitedHtml`. Confirms what PROBE 1 found: Invent.Batch re-resolves the linkage per record, but only feeds the text-substitution layer — never the Variables layer.

### Decision
PROBE 7 will:
1. Parse `[#Var Name#]` from text.data at load (PROBE 6 method)
2. Hook `Fabric.Modified` (PROBE 3 found this is the only clean per-switch event)
3. Push current text per field to `Editor.Invent.Variables.Set(varName, value)` (PROBE 2 confirmed this fires Variable Logic)
4. Log the three untried Set APIs for future reference

If `Variables.Set` doesn't re-fire Variable Logic during preview context (different from initial CSV-upload context), fall back to direct background manipulation now that we have the field map.

---

## Phase 7 — Bridge implementation via [#Var#] linkage (2026-05-26)

**Setup:** PROBE_7_BRIDGE ticked on test product. Map built correctly at script load (6 bindings across 5 fields). Re-entry guard discovered to be too aggressive but worked out — async Variables.Set callback fires fast enough that subsequent Field.TextResorted events catch the next field.

**Outcome: half-success — bridges fire but Variable Logic doesn't re-evaluate.**

Bridge fired exactly twice during initial load + CSV upload:
- Bridge #1 (pre-CSV): all 4 vars = ""
- Bridge #2 (post-Mapping saved): record 1 values pushed (Jane, Doe, January 1st 2026, Example Awards-100)

Then user clicked through records. **Fabric.Modified was the wrong hook** — it doesn't fire on per-record preview switches because the preview iframe is a separate context that updates field text via postMessage → setTextAsLimitedHtml without triggering the editor canvas's Fabric event system.

---

## Phase 8 — Bridge via Field.TextResorted (2026-05-26)

**Setup:** PROBE_8 with diagnostic event counters across 14 candidate events.

**Outcome: bridge fires reliably per record, but Variable Logic still doesn't re-evaluate.**

Field.TextResorted = correct hook. 131 fires over ~12 record switches (~11 per switch = ~5 text fields × 2 passes). 67 bridges committed, including First Name = "?" three times (Bridges #21, #29, #37). Re-entry guard worked: async Variables.Set callback fires fast enough that subsequent events catch next field.

**Visual confirmation:** background did NOT swap on "?" records. Variable Logic engine ignores programmatic Variables.Set during batch preview context.

**Diag confirmed event taxonomy:**
- `Field.TextResorted` = 131 (the reliable hook)
- `Field.ImageChanged` = 81
- `Fabric.Modified` = 12 (fires on macro events only — mapping save, initial render)
- `BatchDataSaved` = 1 (post CSV upload)
- `MappingSaved` = 1

---

## Phase 9 — Direct background manipulation (2026-05-26)

**Setup:** PROBE_9. Hooks Field.TextResorted. On each fire, reads First Name text, decides Background A vs B, sets `field.hidden` + `SaveFields([bgA, bgB])`. Trigger: `First Name === '' || '?'` → show B.

**Outcome: SaveFields commits cleanly but preview iframe doesn't reflect the change.**

21 Applies fired across ~10 record clicks. Three "?" records correctly identified (Apply #8, #10, #12). All SaveFields callbacks fired successfully with logged transitions like `bgA.hidden: false→true`. **But the preview iframe still showed Background A on every record.**

**Bonus diagnostic — record-switch text fetching pattern:**

Between every record click, the bridge fires an interim Apply reading "Jane" (record 1's value) BEFORE the actual new record's Apply. Pattern across the run:
```
Apply #4: Pat (record 2)
Apply #5: Jane ← interim, record 1 baseline reset
Apply #6: Sam (record 3)
Apply #7: Jane ← interim
Apply #8: ? (record 4)
Apply #9: Jane ← interim
Apply #10: ? (record 5)
...
```
Cause: stack traces show `switchRecord → shutDownPreview → setupRecord`. shutDownPreview apparently resets field text to record-1 baseline ("Jane"), then setupRecord applies the new record's text. Field.TextResorted fires for both passes. Cosmetic noise — last write wins with correct value.

**The architectural finding:**

Per-record preview rendering goes `setupRecord → _requestPreview → postMessage → getPreview (XHR)`. The preview iframe asks the SERVER to render record N. Server has its own copy of the design and renders from CSV data in the XHR payload. **Local `Job.Fields.SaveFields()` only mutates the editor's local Job model — server-render pipeline never sees it.**

InDesign.Batch's `replaceTextValue` works because it's done in `_GenerateClientSidePreview` BEFORE the XHR — text values become part of the request payload. Field `hidden` state is NOT in that payload.

**Implication:** Direct field manipulation from Editor-runtime scripts cannot fix per-record preview rendering. The only viable paths involve either (a) server-side MegaScript at render/output time, (b) monkey-patching InDesign.Batch's XHR construction, or (c) pre-processing the CSV server-side. To be confirmed by checking whether the actual final PDF output reflects SaveFields or shares the same architectural deafness.

---

## Open verification needed

- Pull the actual final PDF/output file from the editor with PROBE 9 attached. Check whether SaveFields propagates at render time (preview is just cosmetically broken) OR whether the whole pipeline ignores local hidden state (need server-side approach).
- If editor canvas (not preview iframe) shows correct background, SaveFields IS working locally — confirms the preview iframe is the only broken surface.
