---
title: "Connect: printIQ"
source: "infigo-academy"
url: "https://academy.infigo.net/academy/p/1724/connect-printiq"
type: "article"
date: "unknown"
tags: [connectid, printiq, integration, plugin, product-sync, live-pricing, webhook, mapping]
relevance: "high"
---

## Summary
Comprehensive reference for the Connect: printIQ plugin — covers initial plugin setup, customer / product / shipping mappings, invoicing & paid-flag handling, tax-code matching, additional job reference fields, status-update webhooks, product sync (POD and stock), live inventory caching, and live pricing via `GetPrice`. This is the canonical official integration doc.

## Key takeaways
- Two admin pages run the integration: **Connect Settings** (enable plugin) and **Connect Plugins** (configure connection). Authentication needs printIQ instance URL, username, password, application name, application key from printIQ support.
- "Check Connection" button validates credentials with a green/red popup.
- Customer mapping uses the green "Infigo Connect Link" button on the customer record's Info tab; one Infigo customer maps to ONE printIQ Customer Code (1:1, see FAQ).
- Storefront default Customer Code is available as fallback when an individual customer has no Customer Code set.
- Product mapping options: Product Group → printIQ product code, directly on product variant, or via Attribute Combinations.
- Shipping mapping uses Key = Infigo ShippingMethodSystemName, Value = printIQ Shipping Type name. Find SystemName on Delivery Computation plugin > shipping options.
- Tax: Infigo Tax Categories must match printIQ Tax Codes EXACTLY by name. Set a "Fallback Taxcode" for products without a tax category assignment.
- "Send Jobs marked as paid" options: Never, Always, **Always except when Purchase Order payment** (recommended when offering both card and PO).
- Customer Reference Type controls whether OrderID or PO Number is passed as the CustomerReference field.
- Two checkout-attribute mappings: **Delivery Notes Checkout Attribute** and **Special Instructions Checkout Attribute** — name an Infigo Checkout Attribute to surface customer notes in printIQ.
- Additional Reference Fields mapping is **POD products only** — stock products will NOT pass mapped fields to printIQ. Workaround: use the Notes field, which IS passed for both POD and stock.
- Each additional Reference Field mapping = one extra API call to printIQ. More mappings = more latency.
- Departments can override General Account Manager ID via department External ID.
- Live Pricing: enable "Create quote automatically" + "Keep quote reference when ordering" in Quote Settings. Only SKU-to-SKU mapping supported. Live pricing only works on product landing page, NOT from basket — recommend disabling "Allow editable quantities" in cart.
- Live Inventory has a short-lived cache + a permanent "on-hold" cache for orders in approval. Display value = printIQ inventory - on-hold count.
- Product Sync requires a master product (static PDF type, with `Require Quote` enabled, `Show price as order total` if needed) AND a master category — both inherit default settings to all synced products/categories.
- Sync excludes: attributes, required product mappings, category mappings, related product mappings (these are not inherited from master).
- Multi-section PDFs from printIQ get synced as inventory stock items — only single-section/single-PDF static products create static PDF products in Infigo.

## Code / config snippets

### Webhook URL patterns
Storefront ID is auto-injected; the three status-update endpoints are:

```
Shipping / Dispatch:    /mishandler/{StorefrontID}/Mis.PrintIQ/changestatus
Job cancelled:          /mishandler/{StorefrontID}/Mis.PrintIQ/updatejobstatus
Stock line cancelled:   /mishandler/{StorefrontID}/Mis.PrintIQ/updateorderstatus
```

### Product-sync webhook URLs (registered in printIQ)
```
Static PDF / POD sync:    https://{storefront}/mishandler/{StorefrontID}/Mis.PrintIQ/syncprintondemandproducts
Stock items sync:         https://{storefront}/mishandler/{StorefrontID}/Mis.PrintIQ/syncstockproducts
```

### Inventory cache math (live inventory)
```
displayed_stock = printIQ_inventory - on_hold_cache
```

### Required settings for product sync + live pricing
Quote Settings:
- Create quote automatically (enabled)
- Keep quote reference when ordering (enabled)

Connect Settings:
- Connect Plugin to Handle Stock = Connect: printIQ
- Master Product mapping
- Master Category mapping
- Sync Print on Demand products (enabled)
- Sync stock products (enabled)
- Failure email

Connect: printIQ plugin:
- Base 64 token
- Use getPrice instead of createQuote (enabled)

### POD product field mapping (printIQ → Infigo)
| printIQ | Infigo |
|---|---|
| Name | Product Name |
| ProductCode | Product External ID + SKU |
| Weight | Product Unit Weight (grams) |
| QPDMinOrderQuantity | Minimum basket quantity |
| QPDMaxOrderQuantity | Maximum basket quantity |
| ThumbnailURL | Product Image |
| PricingItems.SPQuantity | Quantity Tiers (when method != Each) |
| ArtworkURL | Determines static PDF vs inventory product |

### Inventory product field mapping
| printIQ | Infigo |
|---|---|
| SIName | Product Name |
| SIActive | IsActive |
| SIAllowBackOrders | BackOrders |
| InventoryItem.IICode | Product External ID + SKU |
| InventoryItem.IISingleUnitWeight | Product Unit Weight |
| InventoryItem.ItemWidth/Height/Depth | Product width/height/depth |

### Category hierarchy (Level field)
- Level 0 = product's own category
- Negative levels = parents (-1 parent, -2 grandparent, etc.)
- TOP-level category name MUST equal the Infigo Storefront External ID for sync routing

## Related
[[connect-printiq-faq]]
[[connect-printiq-product-sync]]
[[connect-printiq-custom-quoting]]
[[printiq-shipping-duplicates]]
