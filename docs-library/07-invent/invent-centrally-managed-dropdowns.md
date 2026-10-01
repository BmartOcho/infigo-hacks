---
title: "How do I set up centrally managed dropdowns in Invent?"
source: "infigo-academy"
url: "https://academy.infigo.net/p/3366"
type: "tutorial"
date: "2026-03-31"
tags: [invent, custom-data, dropdown, text-library, resources, megaedit, mex, variables, release-notes]
relevance: "high"
---

## Summary
Shipped in the March 2026 release. An Invent **Text Library** resource can take its options from an admin **Custom Data** category instead of static values baked into the template. MegaEdit fetches the latest data when the product loads, so changing an address (or any repeated value) means editing it once in Admin. No template re-export is needed. Aimed at address and location lists reused across many templates.

## Key takeaways
- **Prerequisites:** access to **Admin → Custom Data** (if missing, Infigo Support enables it per role); a Custom Data category (e.g. "Addresses"); items with at least a **display field** (e.g. `Name`) and a **value field** (e.g. `FullAddress`).
- **Setup in Invent:**
  1. Resources → **Add Resource Set** → **Text Library** → open the **Editing Text Set** modal and name it.
  2. **External Data Source** dropdown: **None** (static, the default) / **Custom Data** / **API** (shown but **not active** in this release).
  3. With Custom Data selected, fill in **Category Id**, **Key Field** (dropdown labels) and **Value Field** (text put into the artwork).
  4. Tick **"Selecting this option will automatically create a dropdown variable for these resources"**.
  5. Select a text frame → **Link to new variable** → choose the resource.
  6. Export the MEX as usual. In MegaEdit the dropdown fills from Custom Data, and choosing an option writes the mapped value.
- **Fails safe:** if misconfigured (wrong Category Id, empty category, wrong Key/Value field names) it silently falls back to the **static** dropdown. An empty or stale dropdown means checking the Category Id and the field names first.
- Use readable Key values ("London Office", not internal codes), and keep Key/Value field names identical across all items.

## Hack angle — multi-location templates (not yet tested)
This looks like an Infigo-native answer to the "data baked into the template" problem. In that setup, every address and phone change forces a new product revision, because replacing a MEX breaks reorders. Questions to answer on a throwaway product before relying on it:
- **Reorders:** does a reorder keep the value the customer originally saw, or re-fetch the latest Custom Data value? The first is what you want for reprinting an approved proof.
- **Several values per key:** one dropdown choice (a location) needs to drive several frames (address, main phone, fax). Test whether several Text Library resources can share one Key Field and one dropdown variable, each with its own Value Field. If they can't, a Variable Logic rule ([[logic-rules-json-schema]]) would still be needed for the extra fields.
- **Batch CSV:** does a batch row's value get resolved against Custom Data? (Variable Logic doesn't fire on batch; see [[invent-variable-logic]].)
- **MEX shape:** export one test MEX and record how the external source is stored in the Text Library resource, so mexgen can emit it ([[mex-file-format-anatomy]]).
- This overlaps the Custom Data Category + `EditorData` editor-script approach. If the native route works, it removes the need for a custom script.

## Related
- [[infigo-release-notes-2026-03]] — the release that shipped it
- [[invent-variable-logic]]
- [[logic-rules-json-schema]]
- [[mex-file-format-anatomy]]
- [[invent-overview]]
