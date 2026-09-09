---
title: "Live Pricing (GetPrice) | CI_PrintIQ_008"
source: "printiq-kb"
url: "https://academy.infigo.net/p/346/live-pricing-ci_printiq_008"
type: "tutorial"
date: "2022-12-01"
tags: [getprice, api, live-pricing, quoting, connectid, sku, infigo]
relevance: "high"
---

## Summary
The closest thing to a public spec of the GetPrice flow. Infigo's Connect:PrintIQ plugin requests prices from PrintIQ on demand by passing **product code + quantity** and receives a price estimate back, which is rendered to the shopper. Pricing logic lives entirely in PrintIQ; Infigo just displays. Tutorial video: https://www.youtube.com/embed/65d7yXCGKcc

## Key takeaways
- **GetPrice flow (load-bearing for ConnectID):**
  1. Shopper picks a product (and quantity / variant) in Infigo.
  2. Infigo resolves the variant to a printIQ product code via the External ID mapping.
  3. Infigo calls printIQ GetPrice with `productCode` + `quantity`.
  4. printIQ creates an estimate (quote) and returns the price.
  5. Infigo displays the estimate as the live price.
- **Quantity semantics:** GetPrice takes a single `quantity` parameter. PrintIQ returns a TOTAL price for that quantity (see batch-pricing hack — Infigo cart multiplies, so script return values must be UNIT prices in custom contexts).
- **SKU-to-SKU only.** Live pricing currently does NOT work at the bare-product / option-attribute level — only when a fully resolved Infigo variant maps to a fully resolved printIQ SKU. To get parameterized pricing (size × material × stock combos), use Custom Quoting instead.
- **Enablement:** admin search "quote settings" → check **Create quote automatically** and **Keep quote reference when ordering** → Save.
  - "Create quote automatically" turns on the GetPrice path.
  - "Keep quote reference when ordering" preserves the printIQ quote number when the cart is checked out, so the resulting PrintIQ order is the same quote (not a fresh one). This matters for reporting and avoids re-pricing on checkout.
- **Teaser pages do NOT support live PrintIQ pricing** — see FAQ. PrintIQ's quote-based architecture is incompatible with Infigo's teaser-pricing pipeline; the "Use Precalculated Price on Product Teaser" toggle has no effect with this plugin.
- **Failure mode:** if any quote line fails to price in PrintIQ, the auto-accept on order placement throws "Unable to accept a quote that has unpriced lines" and the order errors out.

## Related
[[connect-printiq-faq]]
[[iqconnect-api-overview]]
[[connect-printiq-custom-quoting]]
[[connect-printiq-mapping-products]]
