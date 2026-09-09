# Custom Banner Upload — Auto-Size → Live PrintIQ Price

**Goal:** Customer uploads any-size PDF on a banner product page → system reads the finished size → shows it for confirmation → PrintIQ returns a **live price for that exact size before checkout** → the order carries the size into PrintIQ.

**Chosen path (from scoping):** auto-detect size, customer confirms, live price.

---

## The hard truth first

A plain Infigo **file-upload attribute** stores the PDF but **never reads its dimensions**. PDF is a supported upload extension, but the attribute is a dumb file store. "The product knowing the size" therefore *cannot* come from a plain upload product — it requires the **MegaEdit editor** (reads the placed PDF) and/or a **server MegaScript** (reads the PDF box at output). Both capabilities are confirmed in Infigo's own type packages (see Verified API facts).

---

## Architecture — the chain

1. **MegaEdit "upload-to-canvas" product** with **dynamic canvas size** enabled.
2. **Editor upload script:** on PDF upload, place it as a media item and resize the canvas to the PDF's box; read width/height into editor variables.
3. **Confirm UI:** show detected W×H as editable number fields. Customer corrects if the PDF is off (no trim box, wrong scale, etc.).
4. **Sync to order line:** `save to attribute_BannerWidth` / `save to attribute_BannerHeight` tags push the confirmed values onto Width/Height product attributes.
5. **Custom Quoting Connect Link:** Size attribute = `Custom` → the Width/Height attributes override PrintIQ **Finished Size = Custom**. PrintIQ GetPrice returns a live price.
6. **Live pricing on:** `Create quote automatically` + `Keep quote reference when ordering` → the placed order **is** that quote, with the custom size.
7. **(Belt-and-suspenders) Output MegaScript:** at output, read `PdfPage.TrimBox` and confirm the produced size matches the quoted size; flag mismatches to prepress.

---

## Build steps (Infigo admin)

### A. Create the MegaEdit product
- Catalogue > Products > Add New, product type **MegaEdit**. Set base stock / output type for banner material.

### B. Enable dynamic canvas size
- On the MegaEdit product config, turn on **dynamic canvas sizes** so each job can take the size of the uploaded art (Global object exposes a set-size in points; see API facts).

### C. Editor upload + auto-size script (custom MegaEdit script)
- Add an **Upload** control (`MEUIUpload`). On upload callback: add the file as a media item full-page (this **resizes the page to match the media**), then read the first page's dimensions.
- Write the dimensions into two editor variables (e.g. `BannerWidth`, `BannerHeight`). Convert points → your unit (mm or inches; 1 pt = 1/72 in).
- Decide the size box: prefer **TrimBox** if present, else **MediaBox**; subtract declared bleed if customer art includes it.

### D. Confirm fields
- Bind `BannerWidth` / `BannerHeight` to editable **Number** fields shown to the customer ("We detected 48 × 24 in — confirm or correct"). Clamp to min/max banner sizes.

### E. Width/Height product attributes
- Catalogue > Attributes > Product Attributes: create **Banner Width** and **Banner Height** (textbox control). Attach both to the product variant.

### F. Enable the attribute-sync script
- Admin > MegaEdit Scripts > enable the hardcoded **Product Attribute Sync Script** (ask Infigo support to activate if not visible). Enable it per-product on the **Scripts** tab.
- Tag the confirm fields (Details > Tags): `save to attribute_Banner Width` and `save to attribute_Banner Height` — names must match the attributes **exactly**.

### G. Custom Quoting Connect Link
- On the product variant, open the **Connect Link** popup → Product Type = **Custom**.
- Map the PrintIQ **Product Category**, **Section/Stock**, and set **Finished Size = Custom**, driven by the Banner Width / Banner Height attribute values (this is the documented "Custom size reveals Length + Width that override Finished Size" pattern).
- Save External Reference.

### H. Turn on live pricing
- Admin search **"quote settings"** → check **Create quote automatically** + **Keep quote reference when ordering** → Save.

### I. Optional — output-time size validation MegaScript
- Server MegaScript on output: open the artwork, read `PdfPage.TrimBox` (or MediaBox), compare to the attribute size; log/flag if they differ beyond tolerance.

---

## Verified API facts (for whoever writes the scripts)

**Editor — `@infigo-official/types-for-megaedit`:**
- Dynamic canvas sizes are first-class; Global object has a **set-size (width, height in points)**.
- Pages object exposes **first-page dimensions**; add-media-item helper **resizes the page to match the media** (incl. multi-page PDFs).
- **`MEUIUpload`** upload component; editor Events for upload/field changes.
- All geometry is in **points** (1 pt = 1/72 inch).

**Server — `@infigo-official/types-for-megascript`:**
- `PdfInstance.PageCount`; `PdfInstance.GetPageAt(i)` → `PdfPage`.
- `PdfPage.Width`, `.Height`, and boxes **`MediaBox / TrimBox / BleedBox / CropBox / ArtBox`**, each a `Rectangle { X, Y, Width, Height }`.

**Pricing — `@infigo-official/types-for-pricing-script`:** `Item.*` (IsBatch, Quantity, etc.).

---

## Gotchas

- **Units:** MegaEdit = points; PrintIQ finished size likely mm/inches. Convert explicitly.
- **TrimBox vs MediaBox:** customer art may carry bleed. Pick one box as "finished size" and document it; default TrimBox-if-present.
- **Cart multiplication (your known hack):** any pricing script must return **unit price only** — cart auto-multiplies × qty × records.
- **Live parametric price needs Custom Quoting.** Plain GetPrice is SKU-to-SKU only and can't price a free-form size.
- **POD only:** reference-field / custom-size mapping fires for **POD** products, not Stock.
- **Teaser pages don't support live PrintIQ pricing** — price shows on the product page, not teasers.
- **Bad PDFs:** no TrimBox, scaled-down art, or multi-page files — the confirm step is the guard; clamp + warn.

---

## Small decisions still open

1. Min/max size clamp + any over-size surcharge tier?
2. Behavior when PDF has no TrimBox or an odd aspect ratio (reject vs. fall back to MediaBox)?
3. Single- vs double-sided banners (affects PrintIQ section setup)?

---

*Built from the local docs-library (product-attributes, custom-quoting, getprice, sync-inputs-to-attributes, job-reference-data) and verified against the live npm type packages on 2026-06-19.*
