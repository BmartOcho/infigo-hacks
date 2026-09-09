---
title: "Budget Management (extended) — Auto Top-Up by Department"
source: "infigo-helpdesk"
url: "https://infigosoftware.zendesk.com/hc/en-us/articles/360043461131-Budget-Management-extended"
type: "article"
date: "2024-05-13"
tags: [budgets, megascript, department, auto-topup, cron, per-group, departments]
relevance: "high"
---

## Summary
The 'Budgets' MegaScript auto-tops-up budgets on a schedule, targeted at **All Users** or a **specific Department (by ID)**. This is THE mechanism for per-group/per-department budgets. Note: still applies a per-user budget to each member of the department — NOT a single shared department pot.

## Key takeaways
- **Prereq:** raise a support ticket to have Infigo **install the Budgets MegaScript** and **enable the MegaScript Instances menu** (cannot self-install).
- Enable: Configuration > MegaScripts > MegaScripts Management → enable **Budgets**.
- Create instance: Configuration > MegaScripts > MegaScripts Instances → select **Budget** → Create → set **Name**, enable **RunBackground** + **IsCronInterval**, set **Cron Expression** (UTC; validate at crontab.guru; `0 0 1 * *` = 00:00 on the 1st monthly).
- **Config JSON fields:**
  - `targetAudience.type`: `1` = all users; `2` = a department (then `data` = the Department ID, e.g. `'32'`).
  - `topUpMode`: `1` **TopUpOnly** (add £amount every period) · `2` **TopUpTo** (refill UP TO £amount; refunds can push above it) · `3` **TopUpStrict** (add, but never exceed £amount even after refunds).
  - `amount`: target budget (must be positive).
  - `sendEmails`: `true` fires **Budget.BudgetApplied** each run.
  - `logLevel`: `4` = full debug.
- **One instance PER department** — repeat create+config for each group, each with its own Department ID + amount.
- **Cron caveat:** run → disable → re-enable later = script runs "catch-up" outside schedule. Be deliberate about enable/disable.
- Enforcement (hard cap) + the PrePay/Budget tab come from [[budget-manager-workflow]] settings; this script only handles loading the credit.

## Sample config (specific department)
```
{
  logLevel: 4,
  targetAudience: { type: 2, data: '32' },
  topUpMode: 2,
  amount: 200,
  sendEmails: true
}
```

## Related
[[budget-creating-and-using]]
[[budget-manager-workflow]]
[[customer-budget-csv-import]]
[[department-specific-pricing]]
