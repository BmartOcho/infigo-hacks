---
title: "printIQ v49 Release Notes (incl. v48.1 & v48.2)"
source: "printiq-docs"
url: "https://printiq.com/wp-content/uploads/2025/08/printIQ-v49v48.2v48.1-Release-Notes.pdf"
type: "pdf"
date: "2025-08-22"
tags: [release-notes, v49, v48, getprice, acceptquote, webhooks, api, capacity-planning, mass-shipping, switch, pageflex]
relevance: "high"
---

## Summary
Full release notes PDF covering printIQ v49 (+ rolled-up v48.1 / v48.2). Most release-note content is workflow polish, but the **Integration & Exports** section at the end is load-bearing for ConnectID and any API integrator — it confirms endpoint names (GetPrice, AcceptQuote), webhook capabilities, NodeJS migration for Switch, and new Pageflex integration via a "Kapua middleware" application.

## Key takeaways
- **API endpoint names confirmed:** PrintIQ's standard quoting endpoints are **`GetPrice`** and **`AcceptQuote`**. Both received v49 extensions to accept payment metadata.
- **GetPrice + AcceptQuote now accept payment info:** "We have extended both the GetPrice and AcceptQuote endpoints to optionally capture payment information when you are marking the order as invoiced and paid. You will be able to pass a payment type and reference, which will then be reflected on the payment on the invoice created for that order."
- **GetPrice now supports promotional products and apparel** (previously rejected).
- **New webhook: sales order item status change.** One webhook fires per item when sales order status changes. Confirms PrintIQ uses item-level (not order-level) webhook granularity to let receivers act per-item.
- **Capacity Planning API:** new endpoints added for building integrations between PrintIQ's Capacity Planner and external planning apps.
- **Switch scripts migrated to NodeJS** — PrintIQ rebuilt all standard Switch workflow scripts in NodeJS, but they don't auto-upgrade existing installs (most customers have modified scripts). Old scripts continue to work but may be disabled for editing within Switch.
- **Pageflex integration is new** — 2-way integration via a NEW middleware app called **Kapua**. Touchpoints: order creation, artwork linking, status updates. First mention of Kapua middleware on the public docs.
- **Mass Shipping / Distribution Lists** — quote and job level handle CSV upload of distribution lists. Status flow: `Awaiting Distribution` → `Distribution Ready`. Builds on Kinds/Version-based shipping from v48.1.
- **Kinds / Version-based shipping** (v48.1) — explicit tagging of kinds/versions to delivery addresses. This is relevant to the author's "batch cart multiplication" hack (batch cart multiplies records × kinds × qty wrong; PrintIQ now treats kinds/versions as first-class shipping entities).
- **NZ Post direct integration** (real-time API: address verify, pricing, consignment creation, PDF labels back to PrintIQ).
- **UPS/FedEx reference field push** — many common PrintIQ fields can now be pushed to specific UPS/FedEx label fields via Automated Shipping module.
- **Quoting performance** improvements for large-product quotes and big invoices (1000+ lines).
- **Carbon tracking:** CarbonConnect module records carbon used when a job is accepted.
- **Sage50 via HyperX** — new endpoint avoids penny rounding mismatches on VAT.

## Code / config snippets

API endpoints surfaced or extended in v49:

```
GetPrice         — quoting endpoint; now accepts payment type + reference; supports promo + apparel
AcceptQuote      — accepts a quote and creates job; now accepts payment type + reference
Capacity Planner — new endpoints for external integrations
Sales Order Item Status Webhook — fires per item, per status change
```

## Related
[[printiq-getprice-live-pricing]]
[[iqconnect-api-overview]]
[[connect-printiq-product-sync]]
[[printiq-enfocus-switch-integration]]
