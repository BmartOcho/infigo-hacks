---
title: "Creating invoices, marking jobs as paid and tax codes | CI_PrintIQ_005"
source: "printiq-kb"
url: "https://academy.infigo.net/p/343/creating-invoices-marking-jobs-as-paid-and-tax-codes-ci_printiq_005"
type: "tutorial"
date: "2022-12-01"
tags: [connectid, invoice, paid, tax, taxjar, fallback-taxcode, po, payment]
relevance: "high"
---

## Summary
Three settings sent with every quote/order from Infigo into PrintIQ: invoice creation flag, paid flag, and tax code. Tax codes must be configured consistently in BOTH systems or jobs fail. Includes critical TaxJar interop guidance — use the magic value `UNCALC` as the Fallback Taxcode so both systems independently calculate (and cross-verify) tax. Tutorial video: https://www.youtube.com/embed/bo7ZOxpSm44

## Key takeaways
- **Create Invoice** dropdown — controls whether each job is created as Invoiced=Yes in PrintIQ:
  - `Never` — always Invoiced=No
  - `Always` — always Invoiced=Yes
  - `Always except when Purchase Order payment type` — PO orders → Invoiced=No, all others → Invoiced=Yes
- **Send Jobs marked as paid** dropdown — controls Paid flag:
  - `Never` — Paid=No always
  - `Always` — Paid=Yes always
  - `Always except when Purchase Order payment` — Recommended when offering both card and PO. Card/PayPal/SagePay/Authorize.Net → Paid=Yes, PO → Paid=No so PrintIQ can invoice and chase later.
- **Fallback Taxcode** — used when an Infigo product has no tax category. The name must exist as a Tax Code in PrintIQ. Common convention: a `ZERO` tax category that returns 0% in both systems.
- **Tax Category names** for the Fallback come from: admin search "tax" → Tax Providers → Configure primary provider → **Tax Category** column.
- **TaxJar integration (load-bearing for US shops):**
  - Both Infigo and PrintIQ have TaxJar integrations.
  - Set Fallback Taxcode to **`UNCALC`** to chain them.
  - Workflow: Infigo requests rate from TaxJar → calculates tax → passes values to PrintIQ → PrintIQ re-requests rate from TaxJar to verify the values match.
- Tax Code mismatches between the two systems are one of the more common causes of quote/order failures.

## Related
[[connect-printiq-faq]]
[[connect-printiq-other-config]]
