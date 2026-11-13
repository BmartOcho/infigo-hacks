---
title: "Invent image variables: what happens to clipart resource-set IDs on MEX import"
source: "author-session"
type: "hack-note"
date: "2026-11-11"
tags: [invent, mex, image-variable, clipart, resource-set, albums, media-albums, album-sharing, picker, import-test, hideFromUsers]
relevance: "high"
---

## Problem
Invent image variables carry `source.allowClipartResourceSets{<setId>: bool}` and `defaultValue.resourceSet`, but a MEX may hold no album or image names for those sets. On import, how do those IDs link to storefront albums, and what must be shared for the picker to show images?

## Test (LIVE, 2026-11-11)
- A different storefront from the one the MEX was built for. Album management version = **Standard (legacy)**, "can explicitly share" on.
- File: an event-flyer MEX (plugin 2.4.1) slimmed to under the 3.8 MB browser-upload cap by replacing every `.pdf` with a 1-page blank PDF. `template.xml`, fonts, variables and set IDs untouched; stored ZIP like the original.
- Created via Product Management > Add new > type MegaEdit > "Upload Invent Package", unpublished.
- Non-owner checks were done by impersonating a test customer (Registered role only) from Admin > Customers > Impersonate.

## What the flyer MEX contains [FILE]
- JSON `resources.Clipart = []`. No clipart set is declared.
- XML `Resources/Cliparts/Category name="Standard" hideFromUsers="true"` holds 9 `page_1_frame_N` items: static frame art placed by Invent, not the picker sets.
- The image variables reference 13 set IDs that appear nowhere else in the file. They are bare references.
- Every image variable has `allowUpload:false`, `allowMediaAlbums:true`, `allowAllClipartAlbums:true`, `allowExternalClipartAlbums:[]`.

## Results: set IDs on import [LIVE]
1. **Import succeeds with no warning and no Issues entry**, even though 13 set IDs point at nothing.
2. **Import creates one clipart category per product**, named `<Product Name> Standard`, holding the MEX `Standard` cliparts. Admin shows it on the MegaEdit product's Clipart tab under "Clipart resources managed by mex". It gets a new server GUID, not any Invent ID. The product's own Clipart grid stays empty.
3. **The referenced set IDs are dropped.** None appears in the editor page. No storefront album is created or matched for them.
4. **The picker** ("Select Image" on a form image variable) opens at Home with two folders, matching `allowMediaAlbums` + `allowAllClipartAlbums`:
   - **Cliparts** > only `<Product Name> Standard`. Because `allowAllClipartAlbums:true`, the dead set IDs don't empty the picker; it falls back to whatever clipart categories the product has.
   - **Images** > media albums. Media albums use integer IDs; clipart categories use GUIDs. The `SpecialHidden` album is returned by `/CF/Media/LoadAlbums` but not listed in the picker.
5. **`hideFromUsers="true"`** hides only the free-placement Clipart panel from customers (admins still see it). The same category still appears in the image-variable picker > Cliparts.

## Results: sharing a media album to the product [LIVE]
- **Where sharing lives (Standard/legacy albums):** storefront `/customer/albums` (may have no menu link; go by URL) > open the album > ⋮ menu > **Sharing Settings**. Scopes: Customer Role / **Product** / General / Category / Department / Not Shared. No album-sharing control exists on the admin product, variant or MegaEdit product pages.
- **Product scope is a checkbox list of MegaEdit products**, so one album can go to specific products only. Stock and static-PDF products aren't listed.
- **Owner view proves nothing:** the owner sees the album whether or not it is shared.
- **Non-owner view:** `/CF/Media/LoadAlbums` returned only the customer's own albums, yet the editor's Images dropdown listed the shared album **first**, opened on it and showed its image. A product share makes the album visible to other customers in that product's picker; shared albums load by a separate path.

## Conclusions
- Invent set IDs do **not** auto-link to storefront albums by ID or name. Anything not embedded in the MEX is lost on import into another storefront. [LIVE]
- To ship icons, logos or headers with the template, **embed them in the MEX** as clipart so they land in `<Product> Standard`. [INFERENCE]
- For images customers pick that aren't in the MEX: a **media album owned by an admin and shared to the specific MegaEdit products**. Every customer of those products sees it under picker > Images, listed first. [LIVE]
- A product-shared album shows **all** its images to **every** customer of that product. It is not a per-user filter.

## Gotchas [LIVE]
- **Deleting the catalog product leaves the MegaEdit product behind.** It vanishes from the MegaEdit Products list but its `/CA/Admin/DynamicProduct/Edit/<id>` page still loads, and its `<Product> Standard` clipart category presumably remains. No delete path found.
- Opening the editor creates a draft job/quote each time.
- The editor's "Leave site?" prompt blocks navigation away from a draft session.

## Open
- How a non-MEX clipart category gets onto a product (the product's Clipart grid has only Save/Cancel).
- Whether a set ID that matches a clipart category GUID on the *source* storefront resolves there.
- Customer Role / Department scope sharing (would allow per-group albums): not tested.
- How to remove an orphaned MegaEdit product and its MEX clipart category.

## Related
[[mex-file-format-anatomy]]
[[invent-faqs]]
