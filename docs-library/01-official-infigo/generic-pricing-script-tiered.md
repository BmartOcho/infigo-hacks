---
title: "Generic Pricing Script | Tiered Pricing | GT_PR_£_Pricing Scripts_002"
source: "infigo-academy"
url: "https://academy.infigo.net/p/811/generic-pricing-script-tiered-pricing-gt_pr_pricing-scripts_002"
type: "tutorial"
date: "2023-10-10"
tags: [pricing-script, tiered-pricing, quantity-breaks, csv, debug-mode, test-mode]
relevance: "high"
---

## Summary
Adds quantity-based tier pricing to the Generic Pricing Script. Multiple CSV rows per attribute combination — one row per quantity break — and the script picks the row whose quantity is ≤ requested qty (with the highest tier as fallback for over-max). Also introduces the admin "Test" button and `debugMode` config flag.

## Key takeaways
- For tier pricing, the CSV has MULTIPLE ROWS per attribute combination — each row a different Quantity break for that combination.
- Lookup rule: quantity Q falls into the bracket where Q ≥ tier_quantity AND Q < next_tier_quantity. If Q exceeds the max tier, the max tier is used (no fallback to £10,000 in this case).
- Example with tiers 1, 10, 50: qty 8 uses tier 1, qty 25 uses tier 10, qty 70 uses tier 50.
- The "Test" button on the product variant page runs the script in admin context and shows return data — requires a default attribute config that can return a price (pre-selected attribute values).
- `debugMode: true` exposes detailed log output from Test mode — invaluable for diagnosing why a row didn't match.
- `useTierPrice: true` is required to enable tier-pricing behavior; otherwise the script treats each row independently.

## Code / config snippets

Tiered pricing config block (with debug):

```
{
    filePath: "yourTieredFile.csv",
    quantityColumnName: "Quantity",
    useTierPrice: true,
    debugMode: true
}
```

CSV format for tiered pricing (note repeating attribute combo across rows):

```
A,B,Quantity,Price
A1,B1,1,2.00
A1,B1,10,1.60
A1,B1,50,1.20
A2,B1,1,2.50
A2,B1,10,1.80
A2,B1,50,1.40
```

## Related
[[generic-pricing-script-basics]]
[[generic-pricing-script-multipart-csv]]
[[pricing-script-interface-documentation]]
