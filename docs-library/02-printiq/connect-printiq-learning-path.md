---
title: "Connect: PrintIQ — Learning Path"
source: "printiq-kb"
url: "https://academy.infigo.net/c/532/connect-printiq"
type: "article"
date: "2026-03-31"
tags: [connectid, learning-path, setup, mapping, live-pricing, product-sync, custom-quoting]
relevance: "high"
---

## Summary
Infigo Academy's end-to-end learning path for setting up the Connect:printIQ plugin. Indexes 13 tutorials covering plugin install, customer/product/shipping mapping, invoices and tax codes, job reference data, live pricing, delivery notes, product/category sync, and custom quoting. This is the canonical "official" admin onboarding sequence — every named tutorial code (CI_PrintIQ_001 through CI_printIQ_013) is referenced in support tickets.

## Key takeaways
- **Tutorial inventory (with codes):**
  - CI_PrintIQ_001 — Basic Setup (plugin URL + V0 creds)
  - CI_PrintIQ_002 — Mapping Customers (Infigo customer → printIQ Customer Code)
  - CI_PrintIQ_003 — Mapping Products (Infigo product/variant/attribute combo → printIQ SKU)
  - CI_PrintIQ_004 — Mapping Shipping Options
  - CI_PrintIQ_005 — Creating invoices, marking jobs as paid and tax codes
  - CI_PrintIQ_006 — Sending Additional Job Reference Data
  - CI_PrintIQ_007 — Other Configuration Options
  - CI_PrintIQ_008 — Live Pricing (GetPrice quote calls)
  - CI_PrintIQ_009 — Sending delivery notes and special instructions to printIQ
  - CI_printIQ_010 — Product sync (printIQ → Infigo catalog import)
  - CI_printIQ_011b — Custom Quoting setup
  - CI_printIQ_012 — What is Custom Quoting?
  - CI_printIQ_013 — Example Custom Quoting Configuration
- **Custom Quoting** is the newer, more powerful pricing path: instead of mapping each Infigo SKU to a static PrintIQ SKU, Infigo exposes PrintIQ's product attributes/combinations as live options, eliminating SKU explosion.
- **V0 vs V1 creds:** The plugin has two credential pairs. V0 = current production. V1 = the newer product/inventory sync path. Both can coexist.
- Listed as "Advanced, ~3 hours." Last updated 2026-03-31.
- Linked written documentation page: https://academy.infigo.net/p/1724

## Related
[[connect-printiq-basic-setup]]
[[connect-printiq-mapping-products]]
[[printiq-getprice-live-pricing]]
[[connect-printiq-custom-quoting]]
