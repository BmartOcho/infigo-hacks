---
title: "Product Attribute Grouping"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1989/product-attribute-grouping"
type: "article"
date: "unknown"
tags: [product-attributes, ui, layout, html, css, display-order, admin]
relevance: "medium"
---

## Summary
Wraps related product attributes inside a single HTML `<div>` on the product page so admins can apply CSS to a logical group instead of each attribute individually. Attribute Logic for show/hide still works inside groups.

## Key takeaways
- New entity: **Product Attribute Groups** (Admin > Catalogue > Attributes > Product Attribute Groups).
- Create a group with a **System Name** (backend) and optional **Friendly Name** (UI).
- Attributes get assigned to a group in the product's Attributes tab via the **Group** column.
- One attribute can only belong to ONE group per product.
- Attributes without a group display individually (no wrapper) — same as before.
- Groups display order = lowest display order of any attribute inside; ties broken by group creation date.
- Attributes inside a group still follow their own per-attribute display order.
- Group visibility works alongside existing Attribute Logic — hide/show rules still apply inside grouped wrappers.
- CSS targeting requires manual styling knowledge — the system only adds wrappers, not styles.

## Related
[[enhanced-tier-pricing-attribute-grouping]]
