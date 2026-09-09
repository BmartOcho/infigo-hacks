# Infigo Multi-Group Budget Setup — Client Build Guide

Goal: a new client storefront where multiple groups (departments) each get their own budgets, on top of the existing per-department product separation.

---

## Read this first — the one architectural fact that drives everything

**Infigo budgets are per-USER, not a shared department pot.**

A budget is credit attached to an individual customer account. There is **no native "shared wallet"** where everyone in a group draws from one balance. The "department" option in the extended budget tool just applies the *same per-user budget* to every user in that department and tops each of them up on a schedule.

So decide up front which the client actually means:

| Client wants | Infigo native fit | How |
|---|---|---|
| Each person in a group gets £X to spend, refilled monthly | ✅ Direct fit | Extended Budget MegaScript, target = department |
| One shared pot of £X for the whole group | ⚠️ Not native | No clean native option — needs a single shared login, a custom build, or manual reconciliation. Flag to client / raise with Infigo. |

If they want a true shared pot, stop and confirm scope before building — it changes the approach.

---

## The three budget mechanisms (pick per client need)

1. **Manual budgets** — set credit per user by hand. Fine for small/static groups.
2. **Budget Manager workflow** — users request more budget; an assigned admin approves. Good when spend needs human control.
3. **Extended Budget MegaScript** — automatic top-ups by department on a schedule (cron). **This is the one for "budgets per group."**

You can combine: e.g., extended script for automatic monthly allowances + budget manager for ad-hoc top-up requests.

---

## Setup sequence

### Step 0 — Departments (you mostly have this)
Each group = its own department, with the right users assigned. You already separate products by department, so reuse those same departments as budget targets. Confirm every user is in exactly the right department, and note each **Department ID** (you need the numeric IDs for the script).

### Step 1 — Turn on budget enforcement
`Configuration > Settings > Customer Settings`:

- **Unhide the "PrePay" tab** (rename to "Budget" via language strings if you like). This is where users see their balance and request more.
- **Tick "Checkout allowed only with sufficient budget."** This is the hard cap. Without it, Infigo's default behaviour is to use the budget and then **charge the customer the overspend** to another payment method — i.e., no real limit. Tick it so a group can't spend past its allowance.

### Step 2 — Choose how budgets get loaded

**Option A — Automatic per-group (recommended):** Extended Budget MegaScript
1. Raise an Infigo support ticket: ask them to **install the "Budgets" MegaScript** and **enable the MegaScript Instances menu** on this storefront. (Required — you can't self-install it.)
2. `Configuration > MegaScripts > MegaScripts Management` → enable **Budgets**.
3. `Configuration > MegaScripts > MegaScripts Instances` → select **Budget** → **Create**.
4. Name it (e.g., "Monthly Budget – Group A"), enable **RunBackground** and **IsCronInterval**.
5. Set the **Cron expression** (UTC). `0 0 1 * *` = 00:00 on the 1st of each month. Validate at crontab.guru.
6. Paste the config, set to the department:
   ```
   {
     logLevel: 4,
     targetAudience: { type: 2, data: '32' },
     topUpMode: 2,
     amount: 200,
     sendEmails: true
   }
   ```
   - `targetAudience.type`: `1` = all users, `2` = a department (then `data` = that Department ID).
   - `topUpMode`: `1` TopUpOnly (add £amount each period) · `2` TopUpTo (refill *up to* £amount) · `3` TopUpStrict (add, but never exceed £amount even after refunds).
   - `amount`: target budget (positive number).
   - `sendEmails`: fires `Budget.BudgetApplied` to users on each run.
7. **Repeat steps 3–6 for every department** — one instance per group, each with its own Department ID and amount.

> Cron caveat: if you run an instance, disable it, then re-enable it later, it runs "catch-up" outside the schedule. Be deliberate about enabling/disabling.

**Option B — Manual / one-off:**
- Per user: `Customers > Customer Management > [edit user] > Budgets tab > Add new record > Amount > Insert`.
- In bulk: customer CSV import with the `CurrentBudget` column (Replace / Add / Ignore at upload). Good for an initial load or a manual monthly reset.

### Step 3 — (Optional) Budget Manager workflow for top-up requests
If groups should request more rather than auto-refill:
- Assign a budget manager (must be a storefront admin, **1 per user**): `Customers > Customer Management > [edit user] > Department and Customer Relationships tab > Relationship types dropdown`.
- With "Checkout allowed only with sufficient budget" on (Step 1), a user who runs short is sent to the PrePay/Budget tab to request an amount; the manager applies it in admin; `Budget.BudgetApplied` email confirms.

### Step 4 — Test before handing over
- Impersonate a user in each group; confirm the balance shows at checkout ("Your Credit" / "New Credit Balance").
- Place an order that exceeds the balance → confirm checkout is blocked (enforcement working).
- Manually trigger / wait for the cron once → confirm each department's users top up to the right amount and only those users.

---

## Quick decision checklist for this client
- [ ] Per-user allowance or shared group pot? (If shared → confirm scope, likely non-native.)
- [ ] Department IDs noted for each group.
- [ ] Enforcement on ("sufficient budget" ticked)?
- [ ] Auto-refill (extended script) or manual/CSV or request-based (manager)?
- [ ] Top-up mode per group: TopUpOnly / TopUpTo / TopUpStrict?
- [ ] Refill cadence (cron) confirmed in UTC?
- [ ] Support ticket raised to install Budgets MegaScript?

---

## Sources
- [Creating and using budgets](https://infigosoftware.zendesk.com/hc/en-us/articles/115002001666-Creating-and-using-budgets) — Help Desk
- [Budget Manager Workflow](https://infigosoftware.zendesk.com/hc/en-us/articles/115003512063-Budget-Manager-Workflow) — Help Desk
- [Budget Management (extended)](https://infigosoftware.zendesk.com/hc/en-us/articles/360043461131-Budget-Management-extended) — Help Desk
- [Import or Reset Customer Budgets with CurrentBudget Column](https://academy.infigo.net/p/2466/import-or-reset-customer-budgets-with-the-currentbudget-csv-column) — Academy
- [Departments (category)](https://academy.infigo.net/c/288/departments) — Academy
