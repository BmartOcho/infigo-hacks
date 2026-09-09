---
title: "Why are my PrintIQ shipping methods showing duplicates at checkout?"
source: "infigo-academy"
url: "https://academy.infigo.net/academy/p/2760/why-are-my-printiq-shipping-methods-showing-duplicates-at-checkout"
type: "article"
date: "unknown"
tags: [connectid, printiq, shipping, checkout, troubleshooting, fixed-rate, getprice]
relevance: "high"
---

## Summary
Diagnoses and fixes duplicate / zero-priced shipping methods at checkout when both PrintIQ-rated shipping and Fixed Rate Shipping methods are enabled simultaneously. Recommended fix is to disable Fixed Rate Shipping entirely. Advanced workaround uses the `LegacyUseActiveShippingMethodsFiltering` system setting and per-method `FixedRateIsActiveShippingMethodId{N}` toggles.

## Key takeaways
- The shipping flow: Infigo calls **GetPrice / GetPriceForProduct** with cart context → PrintIQ returns a list of eligible delivery types (with descriptions + sales prices) → Infigo intersects with mapped+active delivery methods → displays only the intersection.
- **PrintIQ only returns delivery methods it can actually price for the current cart context** — methods missing from the API response cannot be displayed.
- Duplicates / zero-priced methods appear when **Fixed Rate Shipping** methods remain enabled in parallel with PrintIQ-rated methods.
- **Recommended fix (Option 1):** Disable ALL Fixed Rate delivery computation methods. Leave only PrintIQ plugin delivery methods enabled. Clean, predictable UX.
- **Advanced (Option 2):** Keep some Fixed Rate methods active by enabling per-method visibility filtering:
  1. Confirm `LegacyUseActiveShippingMethodsFiltering` is `True` in Platform Settings > System Information (default ON; contact support if False).
  2. Under All Settings → Pattern, add `ShippingRateComputationMethod.FixedRateIsActiveShippingMethodId{ID}` = `True` or `False` for each Fixed Rate shipping method ID.
- **WARNING:** Setting values must be EXACTLY `True` or `False` (uppercase first letter). Wrong casing can BREAK the platform until fixed in the database directly.

## Code / config snippets

### Pattern setting for per-method Fixed Rate filtering
```
ShippingRateComputationMethod.FixedRateIsActiveShippingMethodId123 = True
ShippingRateComputationMethod.FixedRateIsActiveShippingMethodId124 = False
```
(Replace `123`, `124` with your Fixed Rate ShippingMethodId values. Remove the curly braces from the template.)

### System Information requirement
```
LegacyUseActiveShippingMethodsFiltering = True
```

## Related
[[connect-printiq-overview]]
[[connect-printiq-faq]]
