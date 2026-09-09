---
title: "Infigo on the nopCommerce solution-partners directory"
source: "other"
url: "https://www.nopcommerce.com/en/infigo-software-limited"
type: "article"
date: "ongoing"
author: "nopCommerce (Infigo's underlying ecommerce framework)"
tags: [nopcommerce, infigo, stack, framework, history]
relevance: "low"
---

## Summary
nopCommerce officially lists Infigo Software Limited as a solution partner — confirmation that Infigo Catfish is built on top of nopCommerce. Useful when investigating quirks that turn out to be nopCommerce-native rather than Infigo-specific (the Capterra reviewer Dan A. flagged "the age of the e-commerce elements" as a concern in 2018; that's nopCommerce showing through).

## Key takeaways
- Confirms the stack reference our shop already has internally.
- When a Catfish bug looks like an e-commerce/cart/checkout/customer-management bug, it's worth grepping nopCommerce GitHub issues (https://github.com/nopSolutions/nopCommerce/issues) — examples found while researching: `#29` "Display 'From' prices for products with attributes/combinations with price adjustments", `#5888` "Computing final price based on Price/TierPrice — bug or breaking change?", `#6254` "No promotion discount applied for quantity (tier) pricing on product detail page". All are upstream issues that would surface in Catfish too.
- nopCommerce is .NET-based, source-available, very actively maintained — useful framing when arguing for or against bypass strategies.

## Related
[[github-infigo-pricing-script-types]]
[[capterra-infigo-reviews-aggregated]]
