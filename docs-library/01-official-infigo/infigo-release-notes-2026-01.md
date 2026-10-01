---
title: "What's New in Infigo | January 2026"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2749/whats-new-in-infigo-january-2026"
type: "article"
date: "2026-01-31"
tags: [release-notes, pricing-script, tier-pricing, delivery-date, production-offset, catalogue, sorting, mis, direct-response, taxjar, accept-blue]
relevance: "medium"
---

## Summary
January 2026 release (no version number; harvested 2026-10-01). The item that matters here is **dynamic tier pricing from pricing scripts**: scripts now receive the tier table and can return recalculated tiers per attribute selection. Also: a Production Offset attribute for delivery dates, curated "Sort by" options, a Direct Response MIS integration, nexus-aware TaxJar, and the Accept.Blue gateway.

## Key takeaways

### Pricing
- **Dynamic tier pricing from pricing scripts** — the product-page tier table and quantity dropdown were static DB values before. Now pricing scripts receive the existing tier prices, apply attribute-based logic (colour, material, …), and return updated tiers in real time. The tier table then shows the price the customer will actually pay. → Relevant to every Generic Pricing Script setup using `useTierPrice` ([[generic-pricing-script-tiered]]). Detail: https://academy.infigo.net/p/2781

### Delivery / Catalogue
- **Production Offset attribute** — adds production days based on what the customer picks or on stock availability, feeding the delivery-date calculation. One product can cover several fulfilment scenarios. Detail: https://academy.infigo.net/p/2782
- **Curated "Sort by" options** for category/catalogue pages. Works alongside **"Allow product sorting"** (Catalogue Settings > Product Options). Detail: https://academy.infigo.net/p/2788

### Integrations / Payments / Tax
- **Direct Response MIS** — scheduled catalog/category sync, live stock checks with fallback and short caching, order submission with a test and re-trigger option, and webhook status/tracking updates. Guide: https://academy.infigo.net/p/2778 · Video: https://academy.infigo.net/p/2802
- **Accept.Blue gateway** — authorise, capture, refund, void, optional 3DS, hosted tokenised form. Detail: https://academy.infigo.net/p/2779
- **TaxJar nexus-aware mode** — an alternative to the old rate lookup. It respects sourcing rules, shipping taxability, and registered nexus. Detail: https://academy.infigo.net/p/2780

## Related
- [[infigo-release-notes-2026-02]] — next month
- [[generic-pricing-script-tiered]]
- [[pricing-script-interface-documentation]]
- [[quantity-based-pricing]]
