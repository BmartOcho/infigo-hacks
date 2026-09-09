---
title: "Infigo-Official/types-for-pricing-scripts (TypeScript type defs + worked examples)"
source: "github"
url: "https://github.com/Infigo-Official/types-for-pricing-scripts"
type: "code-repo"
date: "2026-04-15"
author: "Infigo-Official (vendor org, MIT license, community-installable)"
tags: [pricing-script, github, typescript, npm, batch, csv, vdp, file-info, helper-methods, sample-code]
relevance: "high"
---

## Summary
Official-but-community-installable TypeScript declarations for the Infigo Pricing Script engine, published as `@infigo-official/types-for-pricing-script` on npm and MIT-licensed on GitHub. README contains the most concrete public reference of `Item.*`, `HelperMethods.*`, `Session`, `CheckoutItem`, and `Configuration` plus paste-ready examples for tier pricing, customer-role pricing, CSV-based pricing, and file-based (per-page / per-MB) pricing. Far more useful than Infigo Academy for a dev who wants to write a script without IntelliSense.

## Key takeaways
- Install: `npm i -D @infigo-official/types-for-pricing-script` then point `tsconfig.json` at it for IntelliSense in pricing-script files.
- **Global objects:** `Item`, `Session`, `CheckoutItem`, `Configuration`, `HelperMethods`.
- **Output functions:** `debug()` (admin testing only), `alert()`, `warning()`, `error()`, `console()`.
- **Item pricing properties:** `Price`, `OldPrice`, `UnitPrice`, `FinalPrice`, `ProductCost`, `SpecialPrice`, `AdditionalShippingCharge`.
- **Quantity/packaging:** `Quantity`, `PackQuantity`, `IsBatch` (boolean), `NumberOfPages`, `NumberOfRecords`.
- **Pricing tiers:** `PricingTiers: Tier[]`, `BatchTiers: Tier[]`, `PricePerRecord: number` — note distinct batch tier list.
- **Item methods:** `getFileInfo(attributeId, readContent?)`, `getAttributeValue(name)`, `setAttributeValue(name, value)`, `getGlobalFileContent(filename)`, `getGlobalFileCsvContent(filename)`.
- **Helpers:** `FindTier(qty, tiers, roles?)`, `GetAttributePriceAdjustment(qty, roles?)`, `InterpolatePrice(qty, tiers)`, `CSV.parse(csv, options?)`, `CSV.stringify(data, options?)`, `LogObject(data)`, `Contains(arr, val)`, `IsObject`/`IsArray`, `MergeObject(target, source)`.
- **File-content limits (gotcha):** file content only available for files under 50 KB; page count limited to PDFs under 10 MB.
- Script must `return` a number; on exception, system falls back to normal price. `Item.Price = …` does NOT work for assignment — return the value instead.
- 47 commits, v1.0.3 as of Apr 2026 — actively maintained. Only 2 stars / 2 PRs — very little community uptake, so docs are essentially the README + auto-generated TypeDoc site at `https://infigo-official.github.io/types-for-pricing-scripts/`.

## Code / config snippets

Tier + attribute combo (canonical pattern):
```typescript
function calculatePrice(): number {
    const tier = HelperMethods.FindTier(
        Item.Quantity,
        Item.PricingTiers,
        Item.CustomerRoles
    );
    if (tier) {
        return tier.Price + HelperMethods.GetAttributePriceAdjustment(Item.Quantity);
    }
    return Item.Price;
}
return calculatePrice();
```

Customer-role discount (Wholesale 20%, VIP additional 10%):
```typescript
function calculatePrice(): number {
    let price = Item.Price;
    if (HelperMethods.Contains(Item.CustomerRoles, "Wholesale")) {
        price *= 0.80;
        alert("Wholesale discount applied: 20% off");
    }
    if (HelperMethods.Contains(Item.CustomerRoles, "VIP")) {
        price *= 0.90;
        alert("VIP discount applied: 10% off");
    }
    return price;
}
return calculatePrice();
```

CSV-driven matrix lookup (Global Additional Data file):
```typescript
function calculatePrice(): number {
    const csvData = Item.getGlobalFileCsvContent("pricing-matrix.csv");
    if (!csvData || csvData.length === 0) {
        warning("Pricing matrix not found, using default price");
        return Item.Price;
    }
    const size = Item.getAttributeValue("Size");
    const material = Item.getAttributeValue("Material");
    for (let i = 1; i < csvData.length; i++) {
        const row = csvData[i];
        if (row[0] === size && row[1] === material) {
            return parseFloat(row[2]);
        }
    }
    return Item.Price;
}
return calculatePrice();
```

File-attribute pricing (PDF page count + per-MB over threshold):
```typescript
function calculatePrice(): number {
    let price = Item.Price;
    const fileInfo = Item.getFileInfo("artwork", true);
    if (fileInfo.Error) return price;
    if (fileInfo.MimeType === "application/pdf") {
        price += fileInfo.NumberOfPages * 0.25;
        console(`Added $${(fileInfo.NumberOfPages * 0.25).toFixed(2)} for ${fileInfo.NumberOfPages} pages`);
    }
    const sizeMB = fileInfo.Size / (1024 * 1024);
    if (sizeMB > 5) {
        price += (sizeMB - 5) * 1.00;
    }
    return price;
}
return calculatePrice();
```

## Related
[[github-infigo-megaedit-types]]
[[github-infigo-megascript-types]]
[[capterra-infigo-reviews-aggregated]]
