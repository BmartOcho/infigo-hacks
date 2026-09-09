---
title: "Mapping Shipping Options | CI_PrintIQ_004"
source: "printiq-kb"
url: "https://academy.infigo.net/p/342/mapping-shipping-options-ci_printiq_004"
type: "tutorial"
date: "2022-12-01"
tags: [connectid, shipping, delivery, mapping, due-date]
relevance: "medium"
---

## Summary
How to map Infigo shipping methods (`ShippingMethodSystemName`) to PrintIQ shipping methods via the plugin's Delivery Settings table, and how to optionally pass the customer due date through to PrintIQ. Tutorial video: https://www.youtube.com/embed/uEV5UWWRYkg

## Key takeaways
- Mapping lives in: Connect Plugins → Configure Connect:PrintIQ → **Delivery Settings** → **Add new item**.
- Each row is a Key/Value pair:
  - **Key** = Infigo `ShippingMethodSystemName` (e.g. `FEDEX_1_DAY_FREIGHT`)
  - **Value** = the printIQ delivery method name (e.g. `sample_fedex_1day`)
- To find the Infigo system name: admin search "delivery" → Delivery Computation → Configure the provider → **Get Shipping Options** → copy the `ShippingMethodSystemName`.
- The mapped Value is what's passed into PrintIQ on the quote request.
- **Send Customer Due Date toggle:** if enabled, Infigo overrides whatever delivery date PrintIQ would have calculated with the date passed from Infigo. If disabled, PrintIQ determines timings itself as part of the quote/job.
- For controlling Infigo's delivery countdown logic see: https://infigosoftware.zendesk.com/hc/en-us/articles/360021200071-Delivery-Countdown

## Related
[[connect-printiq-basic-setup]]
[[connect-printiq-mapping-products]]
