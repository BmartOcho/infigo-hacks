---
title: "What's New in Infigo | May 2026"
source: "infigo-academy"
url: "https://academy.infigo.net/p/3611/whats-new-in-infigo-may-2026"
type: "article"
date: "2026-05-31"
tags: [release-notes, invent, batch, csv, regex, vdp, printiq, delivery-date, departments, registration, attribute-combinations, csv-import, stripe, easypost, shared-print-operations]
relevance: "high"
---

## Summary
May 2026 release (no version number; harvested 2026-10-01). Most relevant here: **Regex Text Manipulations for Invent batch** (CSV values reformatted at output time), PrintIQ delivery dates at checkout, **CSV import/export of attribute combinations**, a searchable department picker at registration (customers can create departments), and email-domain registration rules.

## Key takeaways

### Invent / Batch / VDP
- **Regex Text Manipulations for Invent batch orders** — CSV values can be cleaned or reformatted during batch output, for example a raw phone number turned into a formatted one in preview and output. Useful for phone numbers, reference codes, and IDs. → Reduces how much CSV pre-cleaning the batch VDP flow needs. Detail: https://academy.infigo.net/p/2688?tip=how-do-i-use-regex-text-manipulations-when-batch-uploading-data-into-invent

### PrintIQ
- **PrintIQ delivery dates at checkout** — delivery methods returned by PrintIQ can now carry a delivery offset, so Infigo calculates and shows an estimated delivery date. Detail: https://academy.infigo.net/p/2689?tip=how-do-i-display-printiq-delivery-date-calculations-during-checkout

### Products
- **Attribute combinations CSV import/export.** Tip from Infigo: export first, even with zero combinations, to get a correct template.
- **Bulk delete** of selected or all attribute combinations.

### Customers / Departments / Registration
- **Searchable department selector** on registration and My Account. Admins can optionally **let customers create a new department** during registration or account update. Detail: https://academy.infigo.net/academy/p/3356?tip=how-do-i-allow-customers-to-search-and-create-departments-during-registration
- **"Validation" registration action** — regex rules on the email address, and registration is blocked if they don't match. Restricts sign-up to approved domains. Detail: https://academy.infigo.net/academy/p/3356?tip=how-do-i-restrict-customer-registration-using-email-domain-validation

### Payments / Shipping / Admin
- **Stripe metadata** — custom key/value metadata using Infigo placeholders (customer name/ID, order number, customer external ID, product values).
- **EasyPost** — multiple sender/receiver tax identifiers (VAT, EORI, …).
- **Shared Print Operations "All Products" tab** — all product types in one screen.
- Countries/States admin pages use the modern table with bulk actions.

## Related
- [[infigo-release-notes-2026-06]] — next month
- [[infigo-release-notes-2026-04]] — previous month
- [[megaedit-batch-csv-upload]]
- [[product-attributes]]
