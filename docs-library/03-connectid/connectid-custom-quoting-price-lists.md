---
title: "Custom Quoting: Wholesale/Retail Price Lists from printIQ"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2647/upgraded-custom-quoting-select-wholesaleretail-price-lists-from-printiq-using-connect-printiq"
type: "article"
date: "2025-09"
tags: [connectid, printiq, custom-quoting, price-lists, wholesale, retail, custom-product]
relevance: "medium"
---

## Summary
Sept 2025 upgrade to Custom Product quoting in Connect: printIQ. Previously, if no price list was passed in the `getprice` API call, printIQ used its default — which could differ from intent. Now you can explicitly select Wholesale or Retail price tables, globally on the plugin or per product/variant/attribute combination.

## Key takeaways
- Two new fields: `WholesalePricelist` and `RetailPricelist`.
- Configurable at three levels (in selection priority order):
  1. Product (or Attribute Combination) — overrides storefront fallback
  2. Storefront (Connect plugin) — fallback if product is blank
  3. Both blank → property not sent → printIQ uses its default (legacy behavior)
- Updates only the **Custom Product** external popup configuration.
- Applies at Product, Product Variant/Group, and Product Attribute Combination levels.
- Setting group on product variant: `Price settings > Wholesale Price list` and `Retail Price list`.

## Related
[[connectid-printiq-overview]]
