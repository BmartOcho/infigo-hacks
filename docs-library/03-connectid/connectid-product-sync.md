---
title: "PrintIQ - Product Sync"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1715/printiq-product-sync"
type: "article"
date: "unknown"
tags: [connectid, printiq, product-sync, master-product, master-category, inventory, pod, webhooks, category-mapping]
relevance: "high"
---

## Summary
End-to-end setup for PrintIQ-driven product creation/update in Infigo. Covers the multi-tier architecture (platform-level, master storefront, individual storefronts), the Master Product/Category blueprint concept, and the PrintIQ-side webhook + Product Category code config needed to route products to the right Infigo storefront.

## Key takeaways
- **Master storefront** acts as the filter/landing point for incoming PIQ products before they're created on their real destination storefront. Recommended: dedicated, non-live storefront so misconfigured PIQ products land somewhere safe.
- **Platform-level setting**: add the Master storefront ID to `StorefrontIds allowed for switch context` in Connect Settings.
- **Platform-level Connect: PrintIQ plugin**: enable `Sync Print on Demand products` and `Sync stock products`.
- **Master Storefront-level PIQ plugin**: enter same V0/V1 (Base 64 token) creds as platform. Product Sync section: leave empty. Enable plugin under Connect Settings.
- **Each storefront**: create a `Master_` prefixed product (Stock product) and `Master_` category. Select these in PIQ plugin's Product Sync section as blueprints.
- **PIQ Product Category code** (4-digit) is set against each storefront's Connect Link in Storefront Management — NOT the PIQ customer ID. This routes products from the right PIQ customer category to the right Infigo storefront.
- Master product settings (display, pricing config) inherit to all created products. Excluded from inheritance: attributes, required product mappings, category mappings, related product mappings.
- Category hierarchy: top-level category in PIQ must be named the same as the Infigo Storefront External ID — this is what routes the product to the correct storefront.
- Products with PIQ pricing method = "Each" → free-type quantity box in Infigo. Otherwise → quantity tiers matching PIQ quantities (and Infigo pricing is ignored, restricts ordering to those tiers).
- Multi-section/multi-PDF PIQ products are treated as inventory stock items in Infigo. Only single-section single-PDF products create as Static PDF products.

## Code / config snippets
Inventory product field mapping (PIQ -> Infigo):
```
SIName                       -> Product Name
SIDescription                -> Product Description
SIActive                     -> IsActive (true=enabled)
SIAllowBackOrders            -> BackOrders
InventoryItem.IICode         -> Product External ID + SKU
InventoryItem.IISingleUnitWeight -> Product Unit Weight
InventoryItem.ItemWidth/Height/Depth -> Product width/height/depth
InventoryItem.ImageFullFilePath -> Product Image
Categories[].ID/Name/ParentID/Description/ImageURL -> category fields
Categories[].Level           -> 0=product category, -1=parent, -2=grandparent
```

Static POD product mapping (PIQ -> Infigo):
```
Name                         -> Product Name
QPDActive                    -> IsActive
ProductCode                  -> Product External ID + SKU
Weight                       -> Product Unit Weight (grams)
QPDMinOrderQuantity / QPDMaxOrderQuantity -> Min/Max basket qty
ThumbnailURL                 -> Product Image
PricingItems.SPQuantity      -> Quantity Tiers
TreeNodes[].* -> category structure (Level lowest = Storefront External ID)
ArtworkURL                   -> dictates static PDF (URL set) vs stock (null)
```

## Related
[[connectid-printiq-overview]]
[[connectid-printiq-faq]]
