---
title: "What is Connect: printIQ Custom Quoting? | CI_printIQ_012"
source: "printiq-kb"
url: "https://academy.infigo.net/p/1346/what-is-connect-printiq-custom-quoting-ci_printiq_012"
type: "video"
date: "unknown"
tags: [custom-quoting, attributes, live-pricing, sku-explosion, parametric, infigo]
relevance: "high"
---

## Summary
Custom Quoting is Infigo's newer integration mode with PrintIQ that exposes PrintIQ product attributes and combinations as live options on the Infigo storefront, instead of requiring a separate Infigo SKU for every PrintIQ combo. Eliminates SKU explosion and keeps all pricing logic centralized in PrintIQ. Tutorial video: https://www.youtube.com/embed/0iviL18vMgg

## Key takeaways
- **Problem it solves:** Without Custom Quoting, every PrintIQ size/material/stock combination needs its own Infigo SKU mapped via Attribute Combinations. Catalog explodes; maintaining duplicated pricing data across two systems is brittle.
- **How it works:** Operations/attributes in Infigo are sourced LIVE from PrintIQ. Shopper can pick from preset combinations (e.g., set sizes + material list) OR enter a custom width/size combination. Infigo sends the request to PrintIQ, PrintIQ calculates a price in real time, Infigo displays it. No precalculation, no caching.
- **Demonstration from the video:** "Bizarre" custom sizes and weird material/size combos are calculated live by PrintIQ and displayed instantly in the storefront. When the order is placed, the quote already lives in PrintIQ.
- **Single source of truth:** pricing logic, combination rules, and material knowledge stay inside PrintIQ. Infigo becomes a thin interface — the value-prop pitch is "the logic and the knowledge stays in the system rather than people's heads."
- This is the recommended path for shops with parametric/configurable products. SKU-to-SKU mapping is still supported for simple fixed-config products.

## Related
[[printiq-getprice-live-pricing]]
[[connect-printiq-mapping-products]]
[[connect-printiq-faq]]
