---
title: "Prepopulate Data Script (MegaEdit)"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2053/prepopulate-data-script-megaedit"
type: "article"
date: "2026-10-16"
harvested: "2026-11-11"
tags: [megaedit, scripts, prepopulate, customer-account, custom-fields, avatar, business-card, personalization]
relevance: "high"
---

## Summary
MegaEdit script that fills text, barcode and image fields on a MegaEdit product from the logged-in customer's account every time the editor loads. Set up per product, then per field. Article was rewritten 16 Oct 2026 ("Fill MegaEdit Fields from Your Customer's Account") with the full field-level setup; this note replaces an earlier summary written from search snippets.

## Setup
1. **Enable on the product:** Catalogue > Product Types > MegaEdit > MegaEdit Products > Edit > **Scripts** tab > tick **Prepopulate Data** > Save changes.
2. **Open the template as a template editor** (a login allowed to manage MegaEdit templates): open the product on the storefront and click Start. A **Prepopulate Data** button appears in the top bar, greyed out until a field is selected.
3. **Select a field** (text, image or barcode) > click **Prepopulate Data** > choose from **Select the data type** > Save. One data type per field.
4. Repeat per field, then **Menu > Save as product default**.
5. **Test by impersonating a customer** who cannot manage templates.

## Data types
- Text/barcode fields: customer full name (and name parts), title, gender, email, company name, address lines, city, county, postal code, country, phone, mobile, fax, date of birth, language, plus Job Id and Product Id.
- Image fields: **Customer Avatar** is the only choice.
- **Custom fields:** type `prepopulate_Custom1`, `prepopulate_Custom2` or `prepopulate_Custom3` into the field's **Tags** box (double-click field > last tab, Details > Tags). Exact spelling; the capital `C` matters. These are not in the data-type dropdown.

## How the mapping is stored
- Each field's data type is a **tag** on the field, e.g. `prepopulate_postalcode`.
- To force one address for a field, insert `billing_` or `shipping_` after `prepopulate_`, e.g. `prepopulate_shipping_postalcode`. That field then uses only that address and is left empty if the address has no value.
- Re-saving a `billing_`/`shipping_` field through the Prepopulate Data dialog **removes the prefix**. Edit those via Tags only.
- A field with no `prepopulate_` tag keeps whatever text was saved in the product default.

## Where the data comes from
- If **any** address or contact detail is present on the customer's **Customer Info** tab (address, town, postcode, country, county, company, phone or fax), **every** field is filled from Customer Info (except `billing_`/`shipping_` fields). A country alone is enough.
- If none is present: name, email and address come from the billing address, or the first saved address if there is no billing address; title, date of birth, gender and language are left empty.
- Optional Config (Scripts tab > Config next to Prepopulate Data):
  - `{ "disableAddressValidation": true }` always uses Customer Info.
  - `{ "legacyMapping": true }` uses the older rules: name, email and language from the account, everything else from billing address > first saved address > Customer Info. `billing_`/`shipping_` tags have no effect.

## Behaviours to design around
- **Customer edits do not stick.** Fields are refilled on every editor load, so anything typed into a prepopulated field is replaced. Do not prepopulate fields the customer is expected to change; correct the account instead.
- **Missing text values clear the field** (the sample text is not shown).
- **A missing avatar keeps the sample image.** The template's sample image must be a neutral placeholder.
- **Template editors always see sample text** and the setup button, never their own details.
- Changes to the account show up the next time the product is opened.

## Exact tag strings (from a live product, Nov 2026)
Scripts tab > Config next to Prepopulate Data shows **Script MetaData** with `tagPrefix: "prepopulate_"` and the `tagKey` list. Tag = prefix + Value: `jobid`, `productid`, `Title`, `fullname`, `firstname`, `lastname`, `email`, `addressline1`, `addressline2`, `StreetAddress`, `StreetAddress2`, `DateOfBirth`, `Gender`, `street`, `city`, `companyname`, `country`, `county`, `fax`, `mobile`, `postalcode`, `preferredlocale`, `telephone`, `avatar` (image). The **Script config** box above it is empty by default; it only takes overrides. In a generated MEX the tags must be in the XML (`Information/Tags/Tag`), see [[mex-file-format-anatomy]].

## Invent (MEX) products need `allowDirectText` [LIVE, Nov 2026]
On a product imported from an Invent MEX, correctly tagged fields still showed sample text for an impersonated customer until `{ "allowDirectText": true }` was pasted into the **InDesign** script's config box (Scripts tab > Config next to InDesign) and saved. Without it the InDesign script redraws every text box from the template's stored values on load, which also wipes customer-typed edits on saved projects. With it, `prepopulate_Custom1`, `prepopulate_Custom3`, `prepopulate_email` and `prepopulate_telephone` all filled. `prepopulate_telephone` read the customer import's `Phone` column.

- **The InDesign config resets on every MEX re-upload**, even when the MEX carries `Config='{"allowDirectText": true}'` on its InDesign `<Script>`; paste it back each time. [LIVE, Nov 2026]
- **Markup can't be stored in a customer field.** Saving `<span …>` into Custom Field 2 in admin is blocked with "Dangerous Request". Mixed sizes on one line have to come from markup in the template around variables, not from the account data. [LIVE, Nov 2026]

## Not covered by the article
- Where a customer's avatar is set. An older Zendesk article ("Add Avatar to Variable products", #201460955, 2022) gives it: enable **Configuration > Settings > Customer Settings > "Allow customers to upload avatars"**; the customer then uploads under **My Account > Avatar**. [LIVE, Nov 2026] The upload page states jpeg/png/bmp/gif up to 19.1 MB; a 2888×3610 JPEG (5 MB) is stored and printed at full resolution, but a 6250×6250 PNG (10 MB, under the stated limit) was rejected with "The file was not uploaded", so there is an unstated second limit (pixel count or format; not isolated). Resizing to ≤3000 px JPEG is the safe prep. No bulk-load path known (the customer import CSV template has no avatar column).
- Which import CSV column feeds the "mobile" data type (the import template has `Phone` and `Fax` only).
- How this interacts with Invent variable-level `prepopulation` settings in a MEX. Partly answered [LIVE, Nov 2026]: on a product with this script ticked and tagged fields, Invent TEXT variables with `prepopulation` set also filled from the account, both when the variable is on the form and when it is not. `mode: "Full Name"` gave the customer's name; `mode: "Other"` with `otherValue: "Custom2"` gave Custom Field 2.
- **`allowDirectText` strips inline span styling** [LIVE, Nov 2026]. Same template, same field: with the product's InDesign config empty, `[#Name#] <span style="font-family:…;font-size:5.5">[#Credentials#]</span>` rendered in two sizes and two fonts; with `{ "allowDirectText": true }` pasted in, the whole line came out in the field's base style. So a field cannot have both tag prefill (needs the setting) and mixed sizes (needs it off).
- **Variable prefill does not need `allowDirectText`**; tag prefill of text does. With the config empty, variable-driven lines showed account data while tagged text fields showed sample text. The `prepopulate_avatar` image tag filled either way. For a card with mixed sizes: drive all text from hidden variables, keep the avatar tag, leave the InDesign config alone.
- **Phone via variables** [LIVE, Nov 2026]: Invent has no "telephone" mode, but `mode: "Other"` + `otherValue: "Phone"` and the built-in `mode: "Mobile"` both returned the account phone (the import CSV `Phone` column). `Other` + `Custom1`/`Custom3` and `mode: "Email"` also work. A whole card (name, credentials, title, email, cell) filled from hidden variables with no field tags and no `allowDirectText`.
- **Shrink-to-fit flattens span sizes** (font-family survives, font-size does not). Turn fit off on a mixed-size field. [LIVE, Nov 2026]
- The InDesign config popup also shows a **Global Script config** (site-wide default, here `{ "allowDirectText": true }`). After a MEX import the product config reads `// MEX Imported` plus an empty string, and the product behaved as if the setting were off, so the per-product box wins over the global one.

## Troubleshooting
- No Prepopulate Data button: script not ticked/saved on the product, or the login cannot manage MegaEdit templates.
- Sample text when testing: logged in as a template editor; impersonate a customer.
- Wrong address used: see "Where the data comes from"; force with `billing_`/`shipping_`.
- Field stopped filling: its `prepopulate_` tag was removed; set the data type again and save the product default.
- Field empty for some customers: their account has no value for that data type.

## Related
[[megaedit-variables-applying]]
[[megascripts-form-to-order]]
