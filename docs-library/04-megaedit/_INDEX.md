# MegaEdit Docs Library — Index

Documentation harvested from Infigo Academy on **MegaEdit** (Infigo's browser VDP editor) and adjacent pricing-script tutorials/references.

## Files

### MegaEdit core

| File | What it covers |
|------|----------------|
| [megaedit-overview.md](megaedit-overview.md) | Category index — full ME_001..ME_032 series, sub-categories under Editor Plugins MegaEdit (Basics, Core Components, Editor Tools, MegaEdit Topics, Photo Sources, Scripts, FAQ) |
| [megaedit-batch-csv-upload.md](megaedit-batch-csv-upload.md) | **ME_022 Batch data** — Two-switch setup (Batch source=CSVPlugin + Standard Batch Script), placeholder syntax `[++Name++]`, CSV upload mapping |
| [megaedit-scripts-config.md](megaedit-scripts-config.md) | **ME_026 Scripts config** — Per-product vs Global config, custom vs hardcoded scripts |
| [megaedit-barcodes.md](megaedit-barcodes.md) | **ME_029 Barcodes** — Barcode Field script, types (QR/Data Matrix/GS1), Auto Scale, Human Readable, color |
| [megaedit-sync-inputs-to-attributes.md](megaedit-sync-inputs-to-attributes.md) | Product Attribute Sync Script — tag fields with `save to attribute_<name>` to push MegaEdit input values into Infigo product attributes on Add to Basket |

### Pricing scripts (MegaEdit-adjacent VDP/batch)

| File | What it covers |
|------|----------------|
| [pricing-script-overview-toolbox.md](pricing-script-overview-toolbox.md) | Conceptual overview — one CSV in Global Additional Data drives many products |
| [pricing-script-generic-basics.md](pricing-script-generic-basics.md) | **GT_PR_001 Basics** — Attach GenericPricingScript, upload CSV, override filePath, common syntax pitfalls (trailing comma) |
| [pricing-script-tiered.md](pricing-script-tiered.md) | **GT_PR_002 Tier pricing** — `useTierPrice: true`, quantity column, bracket selection logic, debug mode |
| [pricing-script-multipart-csv.md](pricing-script-multipart-csv.md) | **GT_PR_003 Multi-part CSVs** — Split large pricing tables for performance via `subDirectory`/`baseFileName`/`separator`/`splitMapping` |
| [pricing-script-interface-docs.md](pricing-script-interface-docs.md) | Pointer to @infigo-official/types-for-pricing-script (NPM + GitHub Pages) — authoritative API reference |
| [megaedit-pricing-script-item-properties.md](megaedit-pricing-script-item-properties.md) | **Item.\* batch/VDP API quick-ref** — IsBatch, NumberOfRecords, Quantity, BatchTiers, HelperMethods.FindTier; reminder: return UNIT price only on batch (our shop hack) |
| [megascripts-types-documentation.md](megascripts-types-documentation.md) | Pointer to @infigo-official/types-for-megascript (the in-editor MegaEdit scripting API, distinct from pricing scripts) |

## Notes / gaps

- **GitHub Pages type-defs sites** (https://infigo-official.github.io/types-for-pricing-scripts/ and https://infigo-official.github.io/types-for-megascript/) returned binary/unrenderable content via WebFetch. Best approach: open in browser, or `npm install` the matching `@infigo-official/types-for-*` packages for full IntelliSense.
- **Zendesk MegaEdit articles** (https://infigosoftware.zendesk.com/hc/en-us/categories/200325159-MegaEdit) returned empty (JS-rendered SPA). Same content is generally available on academy.infigo.net.
- Several ME_NNN videos exist on Infigo's YouTube embeds inside the academy pages but were not separately harvested — see overview file for the full list of ME_001..ME_032 academy page URLs.
- Older Tutorial pages (e.g. iframe, 3D Preview Module, Form Builder, Upload UI, MegaEdit Variables, Invent, Connect: Switch) live under MegaEdit category but are out of scope here.
