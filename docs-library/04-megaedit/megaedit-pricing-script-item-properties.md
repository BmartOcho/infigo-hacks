---
title: "Pricing Script Item.* Properties (Batch/VDP Reference)"
source: "other"
url: "https://infigo-official.github.io/types-for-pricing-scripts/"
type: "api-ref"
date: "unknown"
tags: [pricing-script, item-api, batch, vdp, megaedit, helpermethods, batch-tiers]
relevance: "high"
---

## Summary
Consolidated reference for the `Item.*` properties most relevant to batch/MegaEdit/VDP pricing scripts at our shop — cross-referenced with Infigo's official interface docs. The canonical authoritative source is the GitHub Pages site for the @infigo-official/types-for-pricing-script package — this file is a quick local lookup.

## Key takeaways
- `Item.IsBatch` (bool) — true when the product is configured as a batch/CSV product. Gate your batch logic on this.
- `Item.NumberOfRecords` (int) — count of rows in the uploaded CSV (= number of records in the batch job).
- `Item.Quantity` (int) — the quantity entered by the customer (copies/records depending on product setup).
- `Item.BatchTiers` — the batch-specific tier pricing array (if the product is a batch product with tier pricing).
- `Item.PricePerRecord` — convenience accessor for per-record pricing.
- `Item.VersionsSumQuantity` — sum quantity across versions (multi-version jobs).
- `Item.getGlobalFileCsvContent(<filename>)` — helper to read a CSV from Global Additional Data into the script.
- Helper methods on the global `HelperMethods` object:
  - `HelperMethods.FindTier(tiers, qty)` — find the matching tier row for a qty.
  - `HelperMethods.InterpolatePrice(...)` — interpolate price between tiers.
- **Critical hack (see the batch cart multiplication section in `docs-library/INDEX.md`):** cart auto-multiplies script return × quantity × records. Pricing scripts on batch products MUST return the **unit price only**, not the total.

## Code / config snippets
Pattern for batch-aware pricing script (return unit price):
```javascript
if (Item.IsBatch) {
  // unit price logic for batch
  var records = Item.NumberOfRecords;
  var qty = Item.Quantity;
  var tier = HelperMethods.FindTier(Item.BatchTiers, records);
  return tier.UnitPrice;   // NOT tier.UnitPrice * records * qty
} else {
  // standard single-item logic
  return basePrice;
}
```

Reading a CSV from Global Additional Data:
```javascript
var csv = Item.getGlobalFileCsvContent("MyPricing.csv");
```

## Related
[[pricing-script-interface-docs]]
[[pricing-script-generic-basics]]
[[pricing-script-tiered]]
[[megaedit-batch-csv-upload]]
[[megascripts-types-documentation]]
