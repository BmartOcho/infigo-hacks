---
title: "Generic Pricing Script | The Basics | GT_PR_£_Pricing Scripts_001"
source: "infigo-academy"
url: "https://academy.infigo.net/p/810/generic-pricing-script-the-basics-gt_pr_pricing-scripts_001"
type: "tutorial"
date: "2023-10-10"
tags: [pricing-script, generic-pricing-script, csv, global-additional-data, basics]
relevance: "high"
---

## Summary
Foundational walkthrough of Infigo's Generic Pricing Script. Pricing scripts are activated per product variant, configured with a small JSON-style config block, and backed by a CSV in Global Additional Data. The CSV columns map to product attributes (matched by header name) plus a quantity column and a price column. For most non-niche cases, the built-in Generic Pricing Script avoids needing custom code.

## Key takeaways
- Pricing scripts are attached on the product variant in the "Attach a price script" dropdown — must save first before extra config options appear.
- The script has a default config shown in a blue box on the variant page; you override only the lines you need in the Pricing script configuration box.
- CSV columns whose headers match attribute names are auto-bound. There is also a configurable quantity column.
- CSV lives under admin > **Global Additional Data**. Upload files there, optionally rename via gear icon, and reference by filename (with extension) in `filePath`.
- Default fallback price when no row matches is **£10,000** (or storefront currency) — this is the "obvious something is wrong" signal.
- The error/diagnostic text on the storefront page tells you which attributes failed to resolve.
- SYNTAX GOTCHA: the LAST line in the config block must NOT have a trailing comma. This is the most common script error.
- Out of the box, attribute names on the product must match the CSV column headers exactly. Aliasing requires extra config covered in later tutorials.

## Code / config snippets
Minimal generic pricing script config — set `filePath` to the uploaded CSV name:

```
{
    filePath: "yourFile.csv"
}
```

A typical CSV (3-attribute example):

```
A,B,Quantity,Price
Red,Small,1,5.00
Red,Small,10,40.00
Blue,Large,1,12.50
```

## Related
[[generic-pricing-script-overview-toolbox]]
[[pricing-script-examples]]
