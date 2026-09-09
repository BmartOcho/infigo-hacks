---
title: "Quantity Based Pricing"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1644/quantity-based-pricing"
type: "article"
date: "unknown"
tags: [pricing, tier-pricing, quantity-based, product, product-group, unit-price, rounding]
relevance: "high"
---

## Summary
Infigo's built-in (no-script) tier pricing system. Configure quantity tiers with an order-line price per tier; pricing engine internally divides by quantity to derive the unit price. Configurable on a per-product OR per-product-group basis. Best practice: set the minimum basket quantity to equal the lowest tier.

## Key takeaways
- Navigation per product: **Catalogue > Products > Product Management > Edit > Product Variant tab > Edit**.
- Navigation per product group: **Catalogue > Products > Product Groups > Edit** (same steps as per product after that).
- **Minimum basket quantity** should match the lowest quantity tier (e.g. if lowest tier is 25, set min basket qty = 25). Otherwise customers can add quantities below your lowest tier.
- Enable **"Use Quantity Based Pricing"** on the Tier Prices tab to activate tiered pricing.
- Each tier requires: Customer Role (dropdown), Quantity (input), Price For Order (input — order-line total, NOT unit price).
- The pricing engine divides `Price For Order` by `Quantity` to compute the displayed unit price.
- **Watch out for price rounding** — if rounding is on, unit-price math can drift. See companion doc on Price Rounding: https://academy.infigo.net/academy/p/1429.

## Code / config snippets
Example tier configuration:

| Customer Role | Quantity | Price For Order |
|---|---|---|
| All | 25  | 125.00 |
| All | 50  | 200.00 |
| All | 100 | 350.00 |
| All | 250 | 750.00 |

Internally: tier 100 → unit price = 350 / 100 = £3.50/unit.

## Related
[[enhanced-tier-pricing-attribute-grouping]]
[[generic-pricing-script-tiered]]
