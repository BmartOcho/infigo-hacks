---
title: "Import or Reset Customer Budgets with the CurrentBudget CSV Column"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2466/import-or-reset-customer-budgets-with-the-currentbudget-csv-column"
type: "article"
date: "2025-07-28"
tags: [customers, csv, budgets, ledger, bulk-update, monthly-reset, totals-rounding]
relevance: "high"
---

## Summary
The Customer CSV import supports an optional `CurrentBudget` column to mass-set customer spending budgets — either replacing the entire balance OR adding on top. Behind the scenes, the import writes ledger entries so deductions, audit logs, and reporting continue to work.

## Key takeaways
- Add `CurrentBudget` column to the standard customer-import template (far right is fine).
- Cell behavior:
  - Numeric value (e.g. `150.75`) = update budget
  - Blank cell = leave the customer's budget untouched
  - `0` = clears all existing budgets for that customer
- **Three import behaviors** chosen at upload time:
  - **Replace current budget** — exact new balance
  - **Add more budget** — increase by the amount
  - **Ignore budget import** — skip budget changes entirely (use when updating only contact details)
- Path: **Customers Management > CSV Import [tab] > Import**, then select Current Budget Behaviour in the popup.
- Values are rounded according to your platform's **Totals Rounding** setting.
- Use cases: monthly allowance reset (Replace), quarterly top-up (Add), zero-out departed users (set 0 + Replace).

## Related
[[customer-csv-bulk-import]]
[[rounding-adjustment-on-pricing]]
