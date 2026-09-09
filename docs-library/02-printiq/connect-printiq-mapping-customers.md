---
title: "Mapping Customers | CI_PrintIQ_002"
source: "printiq-kb"
url: "https://academy.infigo.net/p/340/mapping-customers-ci_printiq_002"
type: "tutorial"
date: "2022-12-01"
tags: [connectid, customers, mapping, external-id, default-customer-code]
relevance: "high"
---

## Summary
How to link Infigo customers to printIQ Customer Codes via the "Connect Link" / External ID UI, plus how to set a storefront-wide fallback customer code. Tutorial video: https://www.youtube.com/embed/CNh7zi1rVX4

## Key takeaways
- Every Infigo customer that will place orders needs a mapped printIQ Customer Code, OR the storefront needs a default code set.
- Per-customer mapping flow: Customers → Customer Management → Edit customer → click **Connect Link** (the green button) → enter printIQ Customer Code → **Save Connect External Id**.
- The Customer Code is passed to printIQ with every estimate AND every order placed by that customer.
- **Storefront-wide fallback:** in Connect Plugins → Configure Connect:PrintIQ → *Other Settings* → **Default Customer Code**. Used when an Infigo customer has no per-customer code assigned.
- The green "Connect Link" button is reused throughout Infigo admin for every MIS-mappable entity (customers, products, product groups, shipping options, attribute combinations).
- Hard limit (from FAQ): only ONE External ID per customer per storefront. No multi-mapping.

## Related
[[connect-printiq-mapping-products]]
[[connect-printiq-faq]]
