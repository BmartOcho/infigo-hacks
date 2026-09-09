---
title: "Connect: printIQ FAQ"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2085/connect-printiq-faq"
type: "article"
date: "unknown"
tags: [connectid, printiq, faq, troubleshooting, stock-vs-pod, teaser, security, references]
relevance: "high"
---

## Summary
Q&A page covering common Connect: printIQ gotchas: customer-to-external-ID is strictly 1:1 per storefront, the "unpriced lines" quote error, teaser-page pricing limits, the Stock vs POD limitation for Additional Reference Fields, the Order ID overwriting PO Number issue, and how Infigo handles artwork security (secure download links, not raw files).

## Key takeaways
- **One customer, one external ID per storefront.** No multi-mapping.
- "Unable to accept a quote that has unpriced lines" = part of the quote failed to price in printIQ. Fix the product price in PIQ first.
- Teaser pages **do not support** real-time PrintIQ pricing (quote-based architecture). The `Use Precalculated Price on Product Teaser` setting does NOT work with PrintIQ.
- **Additional Reference Field Mapping is POD-only.** Stock Products do not carry mapped custom reference fields into printIQ.
- To still pass the Order ID for Stock Products, use the **Notes field** (supported for both POD and Stock; searchable in printIQ).
- To stop Infigo Order ID from overwriting PO Number, set **Customer Reference Type = PO Number** in the plugin. Then map Order ID to a separate reference field (POD only).
- Stock cancellations: currently only initiated **in printIQ** (not Infigo).
- Stock sync is all-or-nothing for product creation/updates. Live stock can be fetched per product if linked via External Product Code, no full Product Sync required.
- Category-view live stock requires enabling the category-view live stock setting in addition to product-level stock tracking; otherwise category view shows 10,000.
- **Artwork security**: Infigo sends secure randomized download links to printIQ/Switch, NOT the actual files. Default behavior, no extra setting required. Applies to both PrintIQ Connect and Switch hotfolders.

## Related
[[connectid-printiq-overview]]
[[connectid-teaser-page-pricing]]
[[connectid-kinds-handling]]
