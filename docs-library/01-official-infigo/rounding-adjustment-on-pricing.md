---
title: "Rounding adjustment on pricing"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1429/rounding-adjustment-on-pricing"
type: "article"
date: "2024-08-22"
tags: [pricing, rounding, banking, commercial, quantity-based-pricing, gotcha, settings]
relevance: "high"
---

## Summary
Toggles + modes for the "Round Price during calculation" setting. Banking rounding (default) rounds 0.5 to nearest EVEN. Commercial rounds 0.5+ up and 0.4- down. **Quantity Based Pricing can produce cart-display formatting errors when rounding is on — disable rounding in that case.**

## Key takeaways
- Path: **Configuration > Settings > Order Settings > "Round Price during calculation"**.
- When enabled, two modes:
  - **Banking** (default) — rounds 3+ decimal places to 2; 0.5 rounds to nearest EVEN number.
  - **Commercial** — 0.5 and above rounds UP; 0.4 and below rounds DOWN.
- **Critical gotcha:** Quantity Based Pricing divides tier totals by quantity to derive unit price. With rounding ON, this can produce incorrect formatting in the cart. **Solution: disable "Round Price during calculation" when using Quantity Based Pricing.**

## Related
[[quantity-based-pricing]]
