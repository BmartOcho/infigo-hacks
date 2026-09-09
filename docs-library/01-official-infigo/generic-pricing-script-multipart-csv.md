---
title: "Generic Pricing Script | Multi-part CSV Pricing | GT_PR_£_Pricing Scripts_003"
source: "infigo-academy"
url: "https://academy.infigo.net/p/812/generic-pricing-script-multi-part-csv-pricing-gt_pr_pricing-scripts_003"
type: "tutorial"
date: "2023-10-10"
tags: [pricing-script, performance, multi-part-csv, subdirectory, global-additional-data, large-csv]
relevance: "high"
---

## Summary
Performance optimization for large pricing tables — split a single large CSV into multiple smaller CSVs, each covering a slice of one attribute's values, stored together in a subdirectory in Global Additional Data. Infigo loads only the relevant slice per request, dramatically reducing lookup time on CSVs over ~1000 entries.

## Key takeaways
- **Rule of thumb: split CSVs that exceed ~1000 entries** to avoid noticeable lookup latency.
- Files must live in a SUBDIRECTORY inside Global Additional Data (create one via the name field + Create button).
- All files in the subdirectory must share a strict naming convention: `<prefix><separator><attribute-value>.csv` (e.g. `Subdirectory-1.csv`, `Subdirectory-2.csv`).
- Each file covers all combinations where the split attribute equals the file's suffix. So splitting on attribute B with 6 values → 6 files.
- Config switches from `filePath` to four new fields: `subDirectory`, `baseFileName`, `separator`, `splitMapping`. **You must also explicitly set `filePath: ""`** (blank) to disable the default.
- `splitMapping` names which attribute(s) you split by (matches the attribute name).
- Separator can be `-`, `_`, `&`, or anything consistent across all filenames.
- Storefront UX is identical — users see no difference, just faster load.

## Code / config snippets

Multi-part config block:

```
{
    subDirectory: "myPricingFolder",
    baseFileName: "Subdirectory",
    separator: "-",
    splitMapping: "B",
    filePath: ""
}
```

This expects files in Global Additional Data under `myPricingFolder/`:
```
Subdirectory-1.csv
Subdirectory-2.csv
Subdirectory-3.csv
...
```

Where each file's name suffix matches a value of attribute B.

## Related
[[generic-pricing-script-basics]]
[[generic-pricing-script-tiered]]
