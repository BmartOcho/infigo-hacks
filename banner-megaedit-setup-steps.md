# Banner Upload — MegaEdit Setup (Simple Steps)

Goal: customer uploads any-size PDF → MegaEdit sizes the page to it → PrintIQ shows a live price → the size goes to PrintIQ on the order.

> **Heads up — there may be an easier way.** A pricing script can read the PDF size directly with
> `Item.getFileInfo(<uploadAttributeId>, false).Dimensions[0]` (Width/Height in points), so a plain upload
> product can price itself with no MegaEdit. Two catches: it only reads PDFs **under 10 MB** (banners often
> aren't), and the price is calculated **in Infigo**, not a live PrintIQ quote. Use the MegaEdit steps below
> when you want **PrintIQ** to do the quoting.

---

## Step 1 — Create the product
1. Catalogue → Products → **Add New**.
2. Name it: `Custom Banner – Upload`.
3. Product type: **MegaEdit**.
4. Save.

## Step 2 — Let the page be any size (dynamic canvas)
1. Open the product's **MegaEdit settings**.
2. Turn on **dynamic canvas size** (each job takes the size of the uploaded art).
3. Set a default size and a sensible **max** (e.g. your largest printable banner).

## Step 3 — Make it upload-style
1. In the MegaEdit product config, set the front end to **Upload UI** (customer just uploads, no design tools).
2. For the **first test**, use the normal editor instead — it's guaranteed to run scripts. Switch to Upload UI once the script works.

## Step 4 — Add two size boxes (attributes)
1. Catalogue → Attributes → Product Attributes → **Add New**: name `Banner Width`. Repeat for `Banner Length`.
2. Open the product → Variant → **Attributes** tab → Add each one. Control type: **Textbox** (must be free-typed numbers, not a dropdown).
3. You can mark them **hidden** so the customer doesn't type them — the script fills them.

## Step 5 — Turn on the attribute-sync script
1. Admin → **MegaEdit Scripts** → find **Product Attribute Sync Script** → enable it. (Don't see it? Ask Infigo support to switch it on.)
2. Open the product → **Scripts** tab → tick it on.

## Step 6 — Add the size-reading script
1. Product → **Scripts** tab → add a **custom script**.
2. Paste the read-size → set-attribute → price logic from `banner-autosize-script-and-test.md`.
   - In plain terms it: waits for the upload, reads the page width/height, writes them into `Banner Width`/`Banner Length`, then refreshes the price.

## Step 7 — Set up PrintIQ Custom Quoting (the Connect Link you saw)
1. Product → Variant → **Connect Link** (Set MIS external Id).
2. Connect Plugin: **Connect: PrintIQ**.
3. Product type: **Custom**.
4. Product category: pick your PrintIQ **banner** category.
5. **Add a Section** → choose the banner **stock**.
6. **Finished Size: Custom** → set width = `Banner Width`, length = `Banner Length` (bind to the attributes).
7. **Save External Reference**.

## Step 8 — Turn on live pricing
1. Admin search **"quote settings"**.
2. Tick **Create quote automatically** and **Keep quote reference when ordering**.
3. Save.

## Step 9 — Test
1. **Test A (do first):** before wiring the script, type an oddball size (e.g. 53.5 × 22.25) into the attributes on the storefront and **Request Price**. PrintIQ should return a size-correct quote. If it only accepts preset sizes, stop — that's the ceiling, ask Infigo.
2. **Test B:** attach the script, upload a test PDF. The size boxes should fill in and the price update by themselves — first in the normal editor, then in Upload UI.

---

### Quick glossary
- **Dynamic canvas** — lets the page be whatever size the PDF is.
- **Attribute** — an option box on a product; here it just holds the width/length number.
- **Connect Link / Custom Quoting** — the popup that tells PrintIQ how to quote; "Custom" = quote any size.
- **Points** — MegaEdit's unit (72 points = 1 inch); convert to mm/inches to match PrintIQ.
