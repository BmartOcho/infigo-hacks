---
title: "Batch data in MegaEdit | ID:ME_022"
source: "infigo-academy"
url: "https://academy.infigo.net/p/322/batch-data-in-megaedit-idme_022"
type: "tutorial"
date: "2023-01-10"
tags: [megaedit, batch, csv, vdp, placeholders, standard-batch-script, dynamic-upload]
relevance: "high"
---

## Summary
The canonical walkthrough for setting up a MegaEdit batch product driven by a CSV/TXT (or XLS/XLSX) upload. Two product-level switches are involved: Batch Source = `CSVPlugin` (on the Product Properties tab) AND the `Standard Batch Script` enabled on the Scripts tab. Optional `Standard Batch Upload options` script adds .xls/.xlsx support. Once enabled, end users see a Placeholders section in the MegaEdit toolbar where they Add placeholders, drop them onto canvas (format: `[++Name++]`), upload a CSV, and MegaEdit auto-maps column headers to placeholder names.

## Key takeaways
- **Two settings to enable**: 1) Batch Source = `CSVPlugin` on Product Properties tab, 2) `Standard Batch Script` checked on Scripts tab.
- Add `Standard Batch Upload` (separate script) for XLSX/XLS support beyond CSV/TXT.
- Placeholder field format on canvas: `[++Name++]` — can be replicated manually into any existing text field (don't have to use the auto-created text box).
- Re-use placeholders elsewhere via the Use button in the dropdown.
- CSV column names matching placeholder names = auto-mapping. If they don't match, user manually maps via checkbox + dropdown in the upload modal.
- Preview shows the first ~5 records by default before Add to Basket.
- Each row in the uploaded CSV = one record in the batch job.

## Code / config snippets
Path to enable on a MegaEdit product:
```
Product Edit > Product Properties tab > Batch source = CSVPlugin
Product Edit > Scripts tab > [x] Standard Batch Script
Product Edit > Scripts tab > [x] Standard Batch Upload    (optional, adds .xls/.xlsx)
```

Placeholder syntax inserted into any text field on canvas:
```
[++Name++]
[++Company Address++]
[++Phone++]
```

## Related
[[megaedit-pricing-script-item-properties]]
[[pricing-script-generic-basics]]
[[megaedit-scripts-config]]
[[connectid-kinds-handling]]
