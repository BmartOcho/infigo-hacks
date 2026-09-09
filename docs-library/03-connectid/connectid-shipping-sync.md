---
title: "Synchronizing Shipping Costs from PrintIQ"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1997/synchronizing-shipping-costs-from-printiq"
type: "article"
date: "unknown"
tags: [connectid, printiq, shipping, delivery, rates, checkout, order-submission]
relevance: "medium"
---

## Summary
How to make Infigo pull live shipping rates from PrintIQ at checkout instead of using Infigo's manual delivery mapping table. Requires the `Use Print IQ Delivery Rates` setting and a specific Order Submission Approach.

## Key takeaways
- `Use Print IQ Delivery Rates` setting replaces the manual Delivery Mapping Table — once enabled, the manual mapping table is no longer used.
- Path: `Configuration > Plugins > Connect Plugins > Configure [Connect: PrintIQ] > Delivery Settings > Use Print IQ Delivery Rates`.
- `Order Submission Approach` **must** be set to **"Append additional order line items to the same quote"** for sync to work. Other options will not work.
- Path: `Configuration > Plugins > Connect Plugins > Configure [Connect: PrintIQ] > Other Settings > Order Submission Approach`.
- Only mapped delivery methods with valid rates will be displayed during checkout.
- Delivery methods in Infigo must still be mapped to PrintIQ delivery types using external IDs (the green Connect Link buttons on each Infigo Delivery Method).

## Related
[[connectid-printiq-overview]]
