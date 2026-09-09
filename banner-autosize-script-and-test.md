# Banner Auto-Size — Editor Script + Validation Test

Companion to `banner-auto-size-upload-build-guide.md`. All API calls below are verified against
`@infigo-official/types-for-megaedit` v1 (install it for IntelliSense while writing the script).

---

## Product type decision

- **Must be a MegaEdit product.** Only a MegaEdit product carries the Custom Quoting Connect Link, dynamic canvas, and editor-script hooks. A plain product-attribute file upload can do none of these.
- **Upload UI is the right front end** (not the full design editor). It's a MegaEdit mode and natively **resizes the page to the uploaded artwork** — the docs describe the underlying helper (`Pages.AddMedia`) as *"add media full page… similar to the ME Upload UI… resize the pages to match the media."* So canvas auto-sizing is built in; you don't script it.
- **Unknown to test:** does the Upload UI run your custom editor script? Full editor = yes. Upload UI = confirm on your instance. Fallback if not: standard editor with design tools hidden (upload-only feel, guaranteed script execution).
- **Test order:** build as a **standard MegaEdit product first** → prove the loop → then switch front end to Upload UI and re-confirm the script fires.

---

## How the pieces connect

```
Customer uploads PDF (Upload UI)
        │  Upload UI / AddMedia resizes the canvas to the artwork  (built-in)
        ▼
Editor script reads the resulting page size
        │  Editor.Document.Pages.Info().firstPageDimension   (points)
        ▼
Script writes size onto product attributes
        │  Editor.Document.SetProductAttributes({Banner Width, Banner Length})
        ▼
Those attributes drive the Custom Product Type → Finished size = Custom (w × l)
        │  PrintIQ GetPrice with the custom finished size
        ▼
Script reads back the live price and shows it before checkout
        │  Editor.Document.Price(cb)
```

The Connect Link **never reads the PDF** — it only reads attribute values. The script is the PDF→attribute bridge.

---

## Editor script skeleton (verified accessors)

```javascript
/* Banner auto-size → attribute → live price.
   Attach on the MegaEdit product, Scripts tab (custom script).
   Verified against @infigo-official/types-for-megaedit v1. */

var PT_PER_IN = 72;
var MM_PER_IN = 25.4;

// Pick ONE converter to match the unit your PrintIQ "Finished size" expects:
function ptToUnit(pt) { return Math.round((pt / PT_PER_IN) * 100) / 100; }      // -> inches
// function ptToUnit(pt){ return Math.round((pt / PT_PER_IN) * MM_PER_IN); }    // -> mm

function pushSizeAndPrice() {
  var info = Editor.Document.Pages.Info();      // PageInfo (fast, no page enumeration)
  var dim  = info.firstPageDimension;           // Size { width, height } in POINTS
  if (!dim) return;

  var w = ptToUnit(dim.width);
  var h = ptToUnit(dim.height);

  // Attribute names MUST match the product attributes exactly.
  Editor.Document.SetProductAttributes(
    { "Banner Width": w, "Banner Length": h },
    function () {
      Editor.Document.Price(function (price) {
        // render `price` in a confirm label (MEUILabel) if you show it in a custom panel.
        // Note: setting attributes already refreshes the editor's built-in price display.
      }, /*unitPriceOnly*/ false, /*skipFormat*/ false);
    }
  );
}

// Fire once the customer's upload is placed on the (auto-resized) canvas:
Editor.Events.Register(EditorEventType.UploadFinalized, function () {
  pushSizeAndPrice();
});

// Optional confirm step: a MEUIButton + two MEUINumber fields prefilled with w/h.
// Let the customer correct, then call SetProductAttributes + Price on click.
```

### API anchors (so you can trust / extend it)
- `Editor.Events.Register(EditorEventType.UploadFinalized, cb)` → returns a handler id; `UnRegister(id)` to remove. Upload lifecycle events: `UploadStarted / UploadFinished / UploadFinalized / UploadFailed`.
- `Editor.Document.Pages.Info()` → `PageInfo.firstPageDimension : Size {width,height}` in **points** (1 pt = 1/72 in).
- `Editor.Document.SetProductAttribute(name, value, cb, createHidden)` / `SetProductAttributes({...}, cb)` — debounced AJAX; for dropdown/radio attributes the value must be the **option id**, for free-text it's the raw value.
- `Editor.Document.Price(cb, unitPriceOnly, skipFormat)` — recomputes from product config + quantity + **attributes**.

---

## Validation test (run in order)

### Test A — does Custom Quoting accept a *free-text numeric* size? (no editor needed)
This is the make-or-break for arbitrary uploaded sizes.
1. On the variant, create attributes **Banner Width** and **Banner Length** as **textbox** (free numeric), not dropdowns.
2. In the **Custom Product Type** Connect Link, set Size handling = **Custom** and bind **Finished size width / length** to those attribute values (the "Size = Custom reveals Length + Width" override pattern, set at the attribute level).
3. On the storefront, type an oddball size — e.g. **53.5 × 22.25** — and **Request Price**.
4. **PASS** if PrintIQ returns a size-correct quote and the price changes when you change the numbers.
   **FAIL** if the width/length fields only accept preset size options (then arbitrary upload sizes can't flow through — escalate to Infigo support on free-form custom-size binding).

### Test B — does the front end run the script + reprice?
1. Attach the script; on a **standard MegaEdit** build, upload a test PDF of a known size.
2. **PASS** if Banner Width/Length auto-populate and the price updates with **no manual entry**.
3. Repeat with the front end switched to **Upload UI**. If it no longer fires, fall back to the locked-down standard editor.

### Test C — TrimBox vs canvas size (accuracy)
- The editor canvas size = whatever MegaEdit set from the upload (may be MediaBox, i.e. includes bleed). Confirm whether your detected size matches the **finished** size you intend to quote.
- Belt-and-suspenders: server MegaScript at output reads `PdfPage.TrimBox` and flags any mismatch vs the quoted attribute size.

---

## Gotchas specific to this step
- **Unit mismatch:** editor returns points; PrintIQ finished size is mm or inches. Set the converter to match, then verify Test A numbers.
- **Attribute value type:** dropdown/radio need the option id; use **textbox** attributes for width/length so the raw number flows in.
- **Where the price shows:** live price surfaces **in the editor** (where the size is known), not on the pre-upload product landing page. That's expected and fine.
- **Cart multiplication:** if any pricing *script* returns a value elsewhere, return unit price only (your known hack).
```
