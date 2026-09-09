---
title: "Budget Manager Workflow"
source: "infigo-helpdesk"
url: "https://infigosoftware.zendesk.com/hc/en-us/articles/115003512063-Budget-Manager-Workflow"
type: "article"
date: "2023-03-06"
tags: [budgets, budget-manager, customer-settings, prepay, enforcement, request-approve]
relevance: "high"
---

## Summary
A request-and-approve top-up flow. The budget manager is NOT like order approval — it only assigns new budget to a user. User runs short → requests budget → assigned manager applies it in admin.

## Key takeaways
- **Assign a budget manager** (must be a storefront admin; **only 1 per user**): Customers > Customer Management > [edit user] > **Department and Customer Relationships** tab > **Relationship types** dropdown.
- **Unhide the "PrePay" tab**: Configuration > Settings > Customer Settings (rename to "Budget" via language strings if desired). This is where users see balance + request more.
- **Tick "Checkout allowed only with sufficient budget"** (Customer Settings) — this is the HARD CAP that stops overspend (overrides the default "charge the difference" behaviour from [[budget-creating-and-using]]).
- Workflow: insufficient/zero budget at checkout → user redirected to PrePay/Budget tab → requests a value (e.g. £50) → manager applies amount in admin + saves → email template **1. Budget.BudgetApplied** fires to confirm.

## Related
[[budget-creating-and-using]]
[[budget-management-extended]]
