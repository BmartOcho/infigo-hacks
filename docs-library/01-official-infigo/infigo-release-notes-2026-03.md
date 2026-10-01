---
title: "What's New in Infigo | March 2026"
source: "infigo-academy"
url: "https://academy.infigo.net/p/3363/whats-new-in-infigo-march-2026"
type: "article"
date: "2026-03-31"
tags: [release-notes, invent, custom-data, dropdown, text-library, megaedit, batch, csv, vdp, non-batch-output-mode, multipart, pdf, approvals, artwork, customers, css, saml, metabase]
relevance: "high"
---

## Summary
March 2026 release (no version number; harvested 2026-10-01). The biggest item for this shop is **centrally managed Invent dropdowns**: a Text Library resource can pull its options from an admin **Custom Data** category, so data edits no longer need a template re-export. Also: a reworked MegaEdit batch CSV flow (template download, validation, preview, **Non-Batch Output Mode**), separate handling of multi-part PDF parts, admin access to pre-processed original artwork, and Advanced Rule Targets for approvals.

## Key takeaways

### Invent / MegaEdit
- **Centrally managed dropdowns (Invent Text Library → Custom Data)** — full write-up in [[invent-centrally-managed-dropdowns]]. Short version: the Text Library modal has a new **External Data Source** (None / **Custom Data** / API, which is not active yet) with **Category Id**, **Key Field**, and **Value Field**. MegaEdit fetches the latest data when the product loads. Admin → Custom Data access may need Infigo Support to enable it for your role. Detail: https://academy.infigo.net/p/3366
- **MegaEdit Batch rework** — download a ready-made CSV template, upload data earlier in the journey, built-in validation, and a preview before ordering. New **Non-Batch Output Mode** setting generates artwork **without** applying the CSV data (for proofing and approvals). Detail: https://academy.infigo.net/p/3365
- **MegaEdit performance** — faster editor load and step transitions. Automatic.

### Multi-part PDFs
- Each part (cover, inner, …) is previewed and output separately instead of being merged into one document. Mixed page sizes and orientations preview correctly. Details: https://academy.infigo.net/p/3375, https://academy.infigo.net/p/3376

### Artwork / Approvals / Customers
- **Pre-processed (original) artwork download** — admins can get the customer's file as uploaded, before PDF profiles or preflight run. Permission-controlled; **ask Infigo Support to enable it**. Detail: https://academy.infigo.net/p/3367
- **Advanced Rule Targets & Scopes for approval rules** — reusable targets built from product tags, categories, or groups, usable in product, order-quantity, and order-subtotal rules. Detail: https://academy.infigo.net/p/3373
- **Per-customer language, currency, and tax display type** on the admin customer record. Detail: https://academy.infigo.net/p/3370
- **Review shipping address on the final checkout step** (Order Settings).

### Storefront / Reporting / Auth
- **Appearance settings available as CSS variables** in custom CSS. Detail: https://academy.infigo.net/p/3369
- Metabase customer reports gain Customer Info address fields with an `Info_` prefix.
- SAML and CAS settings page reorganised; no change in behaviour.

## Related
- [[infigo-release-notes-2026-04]] — next month
- [[infigo-release-notes-2026-02]] — previous month
- [[invent-centrally-managed-dropdowns]]
- [[megaedit-batch-csv-upload]]
- [[multipart-versioning-bg050]]
