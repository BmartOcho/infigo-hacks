---
title: "What's New in Infigo | July 2026"
source: "infigo-academy"
url: "https://academy.infigo.net/p/3731/whats-new-in-infigo-july-2026"
type: "article"
date: "2026-07-31"
tags: [release-notes, megaedit, justify, fit-to-box, mex, reorder, printiq, companies-contacts-sync, payment-reference, api, megascript, payment-method, openapi, attribute-combinations, mfa, permissions, impersonation, shared-print-operations, job-ticket, google-merchant, avalara, shipping]
relevance: "high"
---

## Summary
July 2026 release (no version number; harvested 2026-10-01). It is a large release. For this shop the important parts are: reorder is blocked once a job's output files are replaced; MegaEdit gets Justify alignment, which is carried in MEX; two-way PrintIQ company/contact sync; orders placed by API or Megascript can name a payment method; the API reference is now self-describing OpenAPI 3.0; and attribute combinations can be generated in one click. Also MFA, granular permissions, and combined job-ticket/invoice downloads.

## Key takeaways

### MegaEdit / MEX
- **Justify text alignment** — a fourth alignment option. Behaves the same on the canvas, in the generated PDF, and in **MEX import/export**. Optional **Justify Min Spacing** / **Justify Max Spacing** (Advanced Options) cap word spacing. **Justify and Fit to Box can't be combined**, and the editor enforces this. The last line of each paragraph stays left-aligned. → mexgen should model the new alignment value if it emits text fields ([[mex-file-format-anatomy]]).
- **Reorder blocked after output files are replaced** — once an operator uploads replacement output for a job, reorder is hidden on the account order list and order details, and API reorder returns an error. Automatic; jobs without replaced output are unaffected. → Another reorder-breaking path, alongside template replacement.

### PrintIQ / ConnectID
- **Bidirectional PrintIQ Companies & Contacts sync** — PrintIQ companies ↔ Infigo **departments**, PrintIQ contacts ↔ Infigo **customers**. Four directions, each toggled separately, **all off by default**. It updates matching records instead of duplicating them, works in pages, and one bad record doesn't stop the run. When PrintIQ activates a customer, Infigo marks it active and sends "Customer Set As Active". Has a **test mode** with per-run limits. Detail: https://academy.infigo.net/p/3727
- **Payment transaction reference → PrintIQ** — a universal placeholder resolves to each payment provider's transaction reference and is sent on quote acceptance. **Off by default.** Detail: https://academy.infigo.net/p/2689?tip=payment-transaction-reference-now-sent-to-printiq
- **Carrier preference** now goes to CERM, NetSuite, Radius, and LabelTraxx as text appended to their notes field (Flexlink already had dedicated fields).
- **Connect Flow** — the **"Data format type"** dropdown (JSON / XML / XSLT) replaces the old checkbox + XSLT combo. The webhook accepts JSON or XML status payloads. Existing configs migrate automatically.

### API / Megascripts
- **Payment method on API / Megascript order placement** — include a payment-method **system name** in the order-placement request and it is recorded on the order. If omitted, behaviour is unchanged. Detail: https://academy.infigo.net/p/3355?tip=specify-payment-method-for-api-and-megascript-order-placement
- **API docs** — every endpoint, field, and enum now has a description. The reference is generated as **OpenAPI 3.0** from the codebase and linked from each storefront's **API Explorer at `/services/api`**. (Raw spec: see [[api-order-line-attributes]].)

### Products / Attribute combinations
- **Generate attribute combinations** — a **Generate** button on Attribute Combinations (Product Variant and Product Group pages). Pick attributes (text-type excluded) and every missing combination is created; existing ones are skipped. Manual duplicates are now blocked. **"Max Generated Attribute Combinations"** (Limitation Settings) runs 1–1,000, default 1,000. New combinations get stock **10,000** and backorders off. Detail: https://academy.infigo.net/p/3726
- **Low-stock email per attribute combination** — new **"Notify admin for quantity below"** field on each combination. It is not inherited. Existing combinations default to **1**; set **0** to disable.

### Security / Permissions
- **Storefront MFA** — email one-time link, TOTP authenticator, FIDO2/WebAuthn. Required or optional per role. Trusted-device days default to **0**. MFA is **off by default** everywhere. Detail: https://academy.infigo.net/p/3724
- **Storefront Management permissions** — "Storefront Management - Current storefront only", "... - Allow to create Domain", "... - Allow to create Alias". Gotcha: a role that holds **neither** create permission is treated as **unrestricted**.
- **Impersonate without edit** — a new permission (granted to no role by default) allows search, filter, and impersonate but hides and blocks customer editing. Role weighting still applies.
- **Send templated email to a customer** — from admin customer edit or storefront Manage Users. Permissions: "Admin area. Send email to customers" and "Manage Customers. Send email". A template appears only when its **Customer Context** checkbox is ticked (off on all existing templates). `%CustomMessage%` token for a free-text note.

### Orders / Production
- **Combined downloads in Shared Print Operations** — a Downloads menu builds combined **Job Tickets / Packaging Slips / Invoices** as one merged PDF or a ZIP, as a background task. **"Maximum combined documents"** defaults to **50**. Cancelled jobs are excluded from combined job tickets.
- **View Related Jobs** button on Order Details opens Shared Print Operations pre-filtered to that order.
- **Relevant Orders** (My Account) redesigned: department members see pending/processing department orders, can edit notes, and can mark orders shipped.

### Storefront / Shipping / Tax / Other
- **Access Denied** and **"This content is not available"** pages (editable under Admin > Editable Content). Missing pages now return a real 404.
- **Ship-by-weight tiers** — optional state/province + postcode-pattern match, execution order, CSV export/import (one bad row fails the whole import), min/max weight checkout messages.
- **Google Merchant** — the Content API retired **2026-08-18**. Toggle **"Use new Google Merchant API"** (off by default) plus a one-time Google Cloud developer registration.
- **AvaTax** — **"Use more accurate tax calculation"**, off by default, per storefront.
- Finnish (fi-FI) language added (unpublished). Storefront JS is now bundled and CSS loads first. Plugins load faster in admin.

## Related
- [[infigo-release-notes-2026-08]] — next month
- [[infigo-release-notes-2026-06]] — previous month
- [[mex-file-format-anatomy]]
- [[api-order-line-attributes]]
- [[connect-printiq-mapping-customers]] — customer mapping that the new company/contact sync overlaps with
