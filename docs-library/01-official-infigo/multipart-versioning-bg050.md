---
title: "Multi-version product ordering with Multipart (Upload) products | BG_050"
source: "infigo-academy"
url: "https://academy.infigo.net/p/932"
type: "tutorial"
date: "2023-12-14"
tags: [multipart, versioning, batch, upload, labels, spo, pricing-tiers, kinds-records-equivalent]
relevance: "high"
---

## Summary
**THIS IS THE INFIGO-NATIVE BATCH/MULTI-VERSION FLOW** — adds the "Enable versioning" toggle on a MultiPart product variant, letting one customer submit N different artwork uploads as N versions within ONE cart line. Total quantity is summed across versions for tier-pricing benefits (e.g. 4×250 labels priced as 1000). Each version becomes a separate SPO job.

## Key takeaways
- ONLY MultiPart product type supports versioning (as of doc creation, Dec 2023).
- Enable via: **Product variant settings > "Enable versioning" checkbox > Save**.
- On the storefront, customer specifies the number of versions, then each version gets:
  - A name (default "Version 1", "Version 2", etc. — customizable)
  - Its own quantity
  - Its own uploaded PDF
- Versions can be added or removed dynamically.
- **Attributes are SHARED across all versions** of the same MultiPart product — attribute selection cannot vary per version. Only artwork (PDF) and quantity per-version vary.
- Pricing benefit: total quantity across versions counts toward tier pricing — 4 × 250 labels = 1000 total = better unit price.
- Versions are displayed as a single basket line with an expand option showing each version.
- Customer "My Orders" page shows each version as a separate job within the order.
- **Shared Print Operations (SPO)**: admin sees each version as a SEPARATE job, allowing independent fulfillment and routing.
- This is the closest Infigo-native equivalent to the ConnectID "Kinds/Records per Kind" batch model, but it's MultiPart-specific (no MegaEdit personalization per kind).

## Related
[[multipart-config-builder]]
[[enhanced-tier-pricing-attribute-grouping]]
