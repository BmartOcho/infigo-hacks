---
title: "Other Configuration Options | CI_PrintIQ_007"
source: "printiq-kb"
url: "https://academy.infigo.net/p/345/other-configuration-options-ci_printiq_007"
type: "tutorial"
date: "2022-12-01"
tags: [connectid, account-manager, departments, customer-reference, order-submission, quoting]
relevance: "high"
---

## Summary
The "everything else" tab at the bottom of the plugin config: General Account Manager ID, per-Department Account Manager overrides, Default Customer Code, Customer Reference Type (OrderID vs PO Number), and the very important **Order Submission approach** which controls whether a multi-item Infigo cart produces one quote or many in PrintIQ. Tutorial video: https://www.youtube.com/embed/soIk08iP72Y

## Key takeaways
- **General Account Manager ID** — fallback printIQ Account Manager ID sent on every quote when no per-Department override exists.
- **Per-Department Account Manager:** admin search "department" → Departments → Connect Link on a Department → enter Account Manager ExternalId (e.g. `AccountManagerTest`). When that Department places an order, the per-Dept manager wins over the General fallback.
- **Default Customer Code** — storefront-wide fallback Customer Code used when the customer has no individual `External Id` mapping.
- **Customer Reference Type** — what Infigo puts into PrintIQ's `CustomerReference` field. Options: **OrderID** or **PO Number** (only meaningful if PO payment method is in use). Per FAQ: set to PO Number to preserve the original customer PO from being overwritten by Infigo's OrderID.
- **Order Submission approach** — load-bearing for multi-item carts:
  - **"Raise independent quotes for each order line item"** — Each Infigo cart line becomes its own PrintIQ quote, each auto-accepted and turned into its own job. Used when items are unrelated.
  - **"Append additional Order Line items to the same quote"** — First line creates a quote; subsequent lines append to it; quote is accepted once at the end and PrintIQ creates ONE job/group for all items. Use this when items should be batched/produced together.
- Note: the auto-accept flag is sent with each quote, which is why "unable to accept a quote that has unpriced lines" (FAQ) is fatal for the whole order.

## Related
[[connect-printiq-mapping-customers]]
[[connect-printiq-faq]]
[[printiq-getprice-live-pricing]]
