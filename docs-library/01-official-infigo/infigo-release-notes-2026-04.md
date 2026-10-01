---
title: "What's New in Infigo | April 2026"
source: "infigo-academy"
url: "https://academy.infigo.net/p/3430/whats-new-in-infigo-april-2026"
type: "article"
date: "2026-04-30"
tags: [release-notes, printiq, job-title, custom-name, approvals, departments, shipping, checkout, processing-fee, siteflow, tharstern, email-templates]
relevance: "medium"
---

## Summary
April 2026 release (no version number; harvested 2026-10-01). Most relevant here: the **PrintIQ "Job Title value"** setting (custom name / product name / none sent as the quote title), department-level approvers, country-based shipping rules, a cap on the delivery options shown, processing fees on the full order total, and a reworked PrintIQ settings page.

## Key takeaways

### PrintIQ
- **"Job Title value"** (PrintIQ plugin settings) — choose what Infigo sends as the PrintIQ quote title: **none**, **custom name**, **product name**, or **custom name with fallback to product name**. **New setups default to none** (PrintIQ uses its own SKU/title). **Existing setups keep their previous behaviour.** → Pairs with Sep 2026 custom names on all product types. Detail: https://academy.infigo.net/p/2689?tip=how-to-control-job-titles-sent-to-printiq
- **PrintIQ settings page** reorganised with field guidance and better connection-test validation. Detail: https://academy.infigo.net/p/2689?tip=how-to-understand-the-updated-printiq-settings

### Approvals / Departments
- **Department-level approvers** — set an approver on the department and its users inherit it. A user-specific approver still overrides. Built for SSO + department setups. Detail: https://academy.infigo.net/p/3433

### Checkout / Shipping / Fees
- **Shipping methods by destination country** — usage rules show or hide methods per shipping country (for example fixed local rates plus live international rates).
- **Limit delivery options shown** — only the cheapest N appear first, sorted by price, with an optional "show more".
- **Order processing fee on the full order total** (including shipping and tax), not only the product subtotal.

### Integrations / Admin
- **Tharstern** — at order time, looks up the customer by email, links an existing one, or creates a new one (instead of a generic web-customer code).
- **SiteFlow** — **specification attributes** can now be mapped as well as product attributes, using searchable dropdowns.
- Registration notification emails can include a **direct link to the customer's admin profile**.
- Product Groups list redesigned; API security and multi-instance scalability improvements.

## Related
- [[infigo-release-notes-2026-05]] — next month
- [[infigo-release-notes-2026-03]] — previous month
- [[connect-printiq-other-config]]
- [[budget-manager-workflow]] — approval/department context
