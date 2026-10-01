---
title: "What's New in Infigo | June 2026"
source: "infigo-academy"
url: "https://academy.infigo.net/p/3656/whats-new-in-infigo-june-2026"
type: "article"
date: "2026-06-30"
tags: [release-notes, megaedit, grid, scripting-events, customers, inactivity, checkout, name-limits, connect-flow, multipart, easypost, gift-card, saved-project, impersonation, tharstern, google-merchant]
relevance: "medium"
---

## Summary
June 2026 release (no version number; harvested 2026-10-01). Main items: a configurable snap grid in MegaEdit (it raises scripting events), automatic warnings and deactivation for inactive customers, character limits and a full-name option on name/company fields, multipart asset files in Connect Flow XML, and a few notification and integration fixes.

## Key takeaways

### MegaEdit
- **Configurable visible grid** — enabled per product. Settings: anchor (Top left / Centre), unit (Points, Inch, Millimeter, canvas % with or without bleed), cell width/height, snap distance, line colour/weight/style. End users get a toolbar toggle, and their choice is saved in browser storage. **Scripting events fire when the grid config or visibility changes**, so MegaEdit scripts can react. Detail: https://academy.infigo.net/p/3626

### Customers / Checkout
- **Inactive customer warnings + deactivation** — two warning emails (early warning and final reminder) with the deactivation date and a login link. A background task, **off by default**, marks customers inactive once they pass the threshold. All timing lives on the **Cleanup Settings** page. Detail: https://academy.infigo.net/p/3627
- **Name / company field limits** — under Admin > Configuration > Settings > **Customer Settings**: **"Use full name field"** per section (replaces First/Last across checkout, address book, and registration), plus character limits for Full Name and Company, set separately for address forms and for registration/account pages. Fixes carrier label truncation (UPS/FedEx merge name fields).
- **Gift cards** — a **Save and Notify** button on Admin > Gift Cards > Create. An invalid email blocks creation.
- **"Saved Project Created for Customer (Impersonation)"** email template — sent when an admin creates a saved project while impersonating. **Inactive by default**, per storefront (Content Management > Email Message Templates).

### Integrations
- **"Include generic job files"** — Connect: Flow (Job Configuration, global and per-supplier) and Connect Switch. Adds a `GenericJobFiles` XML section per order line listing working-folder asset files with download links. **Off by default.** Link lifetime follows **"Delete Short Lived Download After X Hours"**. Also fixes multipart asset-part thumbnails (PDF/image) in cart and product preview.
- **EasyPost "Use accurate customs info"** — groups customs items by HS tariff, uses qty × unit weight/price and the store currency, and enables international AutoBuy. Off by default.
- **Google Merchant "Mark unpublished products as out of stock"** — optional.
- **Tharstern "Always send contact"** (Node Mapping group) — always sends the customer name as Contact on invoice, delivery, and item-level addresses.

## Related
- [[infigo-release-notes-2026-07]] — next month
- [[infigo-release-notes-2026-05]] — previous month
- [[megaedit-scripts-config]] — the grid scripting events are relevant to editor scripts
