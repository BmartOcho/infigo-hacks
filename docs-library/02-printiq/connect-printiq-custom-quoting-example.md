---
title: "Example of Custom Quoting Configuration | CI_printIQ_013"
source: "printiq-kb"
url: "https://academy.infigo.net/p/1347/example-of-custom-quoting-configuration-in-connect-printiq-ci_printiq_013"
type: "tutorial"
date: "2024-07-30"
tags: [custom-quoting, example, size, material, embellishments, inheritance, finished-size, emboss-block, attributes]
relevance: "high"
---

## Summary
A walkthrough of a real Custom Quoting setup on a live demo product (live URL: https://core.infigosoftware.com/printiq/p/248). Shows exactly how Size, Material, and Embellishment attributes map to PrintIQ attributes/operations, with three fixed sizes + a Custom size that activates Length + Width sub-attributes. The most concrete example of how inheritance and overrides actually work in production. Tutorial video: https://www.youtube.com/embed/jB0N4VleNYI

## Key takeaways
- **Live demo URL:** https://core.infigosoftware.com/printiq/p/248 — Infigo's public Custom Quoting demo product.
- **Storefront UX:** customer picks attributes + quantity → clicks **Request Price** → Infigo calls PrintIQ → price returned + displayed.
- **Product structure used in example:**
  - **Size** attribute: 3 fixed sizes + 1 `Custom` option
  - When `Custom` is picked, it reveals **Length** + **Width** sub-attributes
  - **Material** attribute: 4 static values
  - **Embellishment** attribute: 3 static values
- **How fixed-size override works:** the Size attribute value's Connect Link only overrides `Finished Size` to a specific PrintIQ-known size; everything else is `Inherited` from the product variant base spec.
- **How the Custom size case works:** The `Custom` size attribute value leaves Finished Size as Inherited. Instead, the **Length** and **Width** attributes themselves override Finished Size with `Custom` sizing + the actual attribute value as the dimension.
- **How material override works:** stock-specific value chosen on each Material attribute value; rest inherited.
- **How embellishment override works:** an additional **Section Operation** is added in the Connect Link (e.g., `EMBOSS BLOCK` value drawn live from PrintIQ).
- The stock list, finished sizes, section operations, and all named operations come LIVE from the PrintIQ instance — they're not configured in Infigo, just selected.

## Related
[[connect-printiq-custom-quoting-config]]
[[connect-printiq-custom-quoting]]
[[printiq-getprice-live-pricing]]
