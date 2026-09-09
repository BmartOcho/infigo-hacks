---
title: "Infigo Release Notes – August 2026"
source: "infigo-academy"
url: "https://academy.infigo.net/p/3747"
type: "article"
date: "2026-08-31"
tags: [release-notes, megaedit, invent, mex, job-ticket, fit-to-box, tracking, non-printing-fields, printiq, promo-code, customer-csv-import, api, deferred-payment, budget, stripe, cybersource, paged-pdf, performance]
relevance: "high"
---

## Summary
August 2026 platform release (version number not stated; received via email 2026-09-09). Headline items for a commercial shop: Job Tickets / Invoices / Packing Slips are now MegaEdit templates built in Invent and shipped as MEX; new Fit-Width-by-Tracking text option; non-printing preview fields; PrintIQ promo-code passthrough; Language/Currency columns on customer import; deferred-payment and budget APIs; paged-PDF upload performance.

## Key takeaways

### MegaEdit / Invent
- **MegaEdit Document Templates** — Job Tickets, Invoices, Packing Slips designed as custom MegaEdit templates in Invent for InDesign → export MEX → upload under Infigo Settings. Dynamic placeholders fill each order's details. Platform-level templates inherit to storefronts that have no custom upload; previous PDF documents remain as fallback. → MEX is script-generatable ([[mex-file-format-anatomy]]), so job-ticket templates are a natural mexgen extension.
- **Fit Width by Tracking** — new "Fit to Box" option: tracking tightens before font size shrinks, preserving designed size longer. Off by default, configured per text field, pre-configurable in Invent. Interacts with fitToBox / size-constraint behaviour (see text-field resize snap-back hack).
- **Non-printing preview fields** — "Show in preview when not printing": field visible in on-screen editor preview but excluded from final print. Set in MegaEdit or Invent. Use for helper/instruction text on templates.

### PrintIQ / ConnectID
- **Promo Code Integration** — two new settings: "Send Discount Name as PromoCode" and "Send Mapped Discount Name as PromoCode". Sends discount info to PrintIQ instead of the full pre-discount price. Both off by default. Order still completes if PrintIQ doesn't match the code; flagged for admin review.
- **Admin product grid** loads faster; PrintIQ-synced storefronts get thumbnail improvements.

### Customers / Import / API
- **Customer bulk import** — optional `Language` (culture code `en-US`, ISO `en`, or display name) and `Currency` (`USD`, `GBP`) columns. Invalid values reported per row; valid rows still import. Same fields on the customer API. → Extends [[customer-csv-bulk-import]].
- **Customer Budgets via API** — new endpoints read/adjust customer spending budgets; Customer V2 GetAll optionally returns total budget amounts. → Extends [[budget-management-extended]].
- **Deferred Payment via API** — order-recording API accepts external card methods (Authorize.Net, Stripe, PayPal, CyberSource, PayTrace, Square, AcceptBlue) with deferred payment. Order created pending; customer completes payment from My Account. API rejects requests marking orders as already-paid with external methods. No admin config beyond active payment method.

### Orders / Checkout / Email
- **Additional Recipients on Order Notifications** — new checkout attribute; customer enters comma-separated emails, validated at checkout, CC'd on placed/shipped/delivered/cancelled emails. Opt-in per storefront.
- **Approver comments in cancellation emails** — new email placeholder; cancelled status record names the approver rather than the customer. Default template auto-updated for new installs only.
- **Unified Print Operations "All" tab** — Shared Print Operations shows jobs across all product types; Phase 2 adds historical custom product names, print history links, production statuses; historical orders display alongside new.

### Payments
- **Stripe** — custom statement descriptor suffix (≤13 chars) on card statements; "Use Stripe successful payments" setting controls receipt email; descriptor recorded in order payment notes; metadata written before capture for payout reporting.
- **CyberSource 3D Secure** — inline challenge at checkout, reduces fraud liability. Off by default, per storefront in CyberSource plugin settings.

### Performance
- Category listing, product, and category pages load faster under high traffic.
- **"Use paged PDF media"** setting → large multi-page PDF uploads near-instant; first page preview immediate, remaining pages generated on demand.

## Related
- [[mex-file-format-anatomy]] — MEX structure (07-invent)
- [[customer-csv-bulk-import]]
- [[budget-management-extended]]
- [[connect-printiq-custom-quoting]] — pricing passthrough context for promo codes
