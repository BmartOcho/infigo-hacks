---
title: "Connect: printIQ FAQ"
source: "printiq-kb"
url: "https://academy.infigo.net/p/2085/connect-printiq-faq"
type: "article"
date: "2026-03-31"
tags: [connectid, faq, infigo, pod, stock-products, reference-fields, errors, security]
relevance: "high"
---

## Summary
Infigo Academy FAQ for the Connect:printIQ plugin. Highest-signal page in the academy because it documents real failure modes, hard limitations, and the workaround patterns the author will hit in production. Covers customer/external-ID rules, the "Unable to accept a quote that has unpriced lines" error, reference-field mapping differences between POD and Stock products, stock sync semantics, and artwork-security behavior.

## Key takeaways
- **One-to-one customer mapping is hard-enforced.** A single Infigo customer on a single storefront can only have ONE printIQ External ID. No multi-ID per customer.
- **"Unable to accept a quote that has unpriced lines"** — when ConnectID submits an order, PrintIQ creates a quote and tries to auto-accept it. If any line failed to price in PrintIQ, the accept fails and the whole order errors. Fix: validate every product's pricing in PrintIQ before adding to Infigo.
- **Teaser pages cannot show live PrintIQ prices.** PrintIQ's quote-based pricing model is incompatible with Infigo's teaser pricing pipeline. The "Use Precalculated Price on Product Teaser" setting does NOT work with the PrintIQ plugin — that setting is only for plugins following Infigo's standard pricing architecture.
- **Stock Products in PrintIQ do NOT support Additional Reference Field Mapping** from Infigo — only POD products do. Workaround for Stock products: stuff the Infigo Order ID into the **Notes** field, which is searchable in PrintIQ for both POD and Stock.
- **Avoiding PO Number overwrite:** Set the Connect:PrintIQ plugin's *Customer Reference Type* to **PO Number** so the original customer PO is preserved; map Order ID to a separate reference field (POD only).
- **Stock sync is all-or-nothing for product creation/updates** — cannot sync stock for "just a few" products selectively. But live inventory levels do NOT require Product Sync enabled; per-product fetches work via the External Product Code link.
- **Category-view live stock** requires its own setting even if per-product stock tracking is on. A common misconfiguration: stock shows "10,000" in category view but correct on the product page → category-view live stock setting wasn't enabled.
- **Artwork security:** Infigo never sends physical files to PrintIQ or Switch. It sends secure, randomized download links. Default behavior, no extra config required, safe for confidential artwork. Same approach for PrintIQ Connect and Switch hotfolders.
- PrintIQ has confirmed that **Sales Order references for Stock Products** are "being considered" — not currently supported.

## Related
[[printiq-getprice-live-pricing]]
[[connect-printiq-basic-setup]]
[[connect-printiq-mapping-customers]]
[[connect-printiq-mapping-products]]
