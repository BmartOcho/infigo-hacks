---
title: "Creating and Using Budgets"
source: "infigo-helpdesk"
url: "https://infigosoftware.zendesk.com/hc/en-us/articles/115002001666-Creating-and-using-budgets"
type: "article"
date: "2023-03-06"
tags: [budgets, customers, credit, checkout, per-user]
relevance: "high"
---

## Summary
A budget is credit added to an **individual customer** account that they spend in-store. This is the base/manual budget mechanism. Budgets are per-USER — there is no native shared department pool.

## Key takeaways
- Set per user: **Customers > Customer Management > [edit user] > Budgets tab > Add new record > Amount > Insert**.
- Edit/Delete anytime; click **Update** to save edits.
- Increasing a budget after spend: new balance = (original assigned + increase) − amount already spent.
- At checkout the user sees **"Your Credit"** (current) and **"New Credit Balance"** (after this purchase).
- **DEFAULT (gotcha):** Infigo uses the budget to pay, and if budget is insufficient it **charges the customer the outstanding** to another method — i.e. NOT a hard cap. To make budget a real limit, enable "Checkout allowed only with sufficient budget" (see [[budget-manager-workflow]]).
- Bulk-load/reset budgets via CSV instead: see [[customer-budget-csv-import]].

## Related
[[budget-manager-workflow]]
[[budget-management-extended]]
[[customer-budget-csv-import]]
