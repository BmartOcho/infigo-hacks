---
title: "Setting Up Department-Specific Pricing in Infigo"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1959/setting-up-department-specific-pricing-in-infigo"
type: "article"
date: "unknown"
tags: [pricing, departments, discounts, head-office, product-variant, no-coupon]
relevance: "high"
---

## Summary
Department-specific pricing in Infigo is implemented as a **Discount** with a department requirement, NOT as a separate pricing system. Use a 100% discount on selected SKUs (or order total) restricted to "Customer belongs to a specific department" so head office gets free items while store locations pay normally.

## Key takeaways
- Discount path: **Promotions > Discounts > Add New**.
- **Discount Type** options: assign to order total OR individual product variants/SKUs (most common for department-pricing scenarios).
- **Requires Coupon Code** — uncheck to auto-apply (no customer input).
- **Requirements tab** — set "Customer belongs to a specific department" and pick the department from dropdown.
- For per-SKU discounts: go to the product variant > Discounts tab and assign the discount per product.
- Discount can use any % (not just 100%) — same pattern works for "head office gets 50% off", "store locations pay full price", etc.
- Users must be properly assigned to departments (Departments screen > expand department > check users > Save) for the requirement to match.
- Multiple departments = multiple discounts, one per department.

## Related
[[pricing-visibility-control]]
[[quantity-based-pricing]]
