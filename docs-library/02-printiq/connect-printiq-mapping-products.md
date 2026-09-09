---
title: "Mapping Products | CI_PrintIQ_003"
source: "printiq-kb"
url: "https://academy.infigo.net/p/341/mapping-products-ci_printiq_003"
type: "tutorial"
date: "2022-12-01"
tags: [connectid, products, mapping, sku, attribute-combinations, product-groups, external-id]
relevance: "high"
---

## Summary
Three ways to map an Infigo product to a printIQ product code/SKU: (1) at the product/variant level, (2) per attribute combination (variant-specific SKU), or (3) via Product Groups for bulk inheritance. This is where the "Connect Link" greens up on the Product Variant, Attribute Combination, and Product Group screens. Tutorial video: https://www.youtube.com/embed/7ZuPOCkf03k

## Key takeaways
- **Path 1 — Single product to single SKU:** Catalogue → Products → Product Management → expand product (+) → click Connect Link on the variant row → enter printIQ product code as ExternalId → Save Connect External Id.
- **Path 2 — Per attribute combination:** Edit product → Attributes → Attribute combinations → create or pick combo → click Connect Link on that combo → enter the printIQ SKU specific to that combo. Use this when each variant in Infigo maps to a distinct printIQ SKU.
- **Path 3 — Product Groups (bulk):** Search "product groups" → Product Groups → create/edit group → Connect Link on the group → enter printIQ code → all products in that group inherit the same external ID. Useful for entire categories that resolve to a single printIQ SKU.
- The Connect Link mechanism is the same green button used for customers and shipping — it always opens a popup that takes a plugin-specific ExternalId.
- **Live pricing only works at SKU-to-SKU mapping level** today (per Live Pricing tutorial). Custom Quoting is the escape hatch when SKU explosion gets unmanageable.
- Stock products can use product-level mapping but cannot receive Additional Reference Fields from Infigo (see FAQ).

## Related
[[connect-printiq-faq]]
[[printiq-getprice-live-pricing]]
[[connect-printiq-custom-quoting]]
