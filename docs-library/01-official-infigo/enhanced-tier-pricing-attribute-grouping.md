---
title: "Enhanced Tier Pricing with Attribute-Based Grouping | BG_076"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1868/enhanced-tier-pricing-with-attribute-based-grouping-bg_076"
type: "tutorial"
date: "2024-09-25"
tags: [pricing, tier-pricing, share-tiers, multipart, cart, attributes, advanced]
relevance: "high"
---

## Summary
"Share Tiers on Cart" lets the same product (or product + matching attributes) accumulate quantities across multiple cart lines to push customers into better-priced tiers. Four sharing modes: No Share, Same Products, Same Products and Attributes, Same Products and Selected Attributes.

## Key takeaways
- Setting lives on the **Tier Prices** tab under product variant settings, alongside the regular tier configuration (see [[quantity-based-pricing]]).
- **Share Tiers on Cart dropdown options:**
  - **No share** — matching products are never grouped (legacy behavior).
  - **Same products** — sum of quantities for the same product regardless of attributes drives the tier.
  - **Same products and attributes** — sum of quantities for the same product AND identical values of ALL attributes.
  - **Same products and selected attributes** — like above, but only specified attributes count (additional UI lets you pick which attributes).
- Real example from doc: 100/£4 tier; two cart lines of qty 50 = qty 100 total → both lines drop from £5/unit to £4/unit when share mode is "Same Products".
- For "Same products and attributes" mode, lines with different attribute selections do NOT combine — they're treated as separate quantity buckets.
- "Same products and selected attributes" can only filter against attributes that exist on the specific product.
- After changing setting, an Update Basket action in the cart re-evaluates the tier price.

## Related
[[quantity-based-pricing]]
[[product-attribute-grouping]]
