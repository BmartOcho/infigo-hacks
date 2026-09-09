---
title: "PrintIQ: Mapping Checkout Attributes to PrintIQ References"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2547/printiq-mapping-checkout-attributes-to-printiq-references"
type: "article"
date: "unknown"
tags: [connectid, printiq, checkout-attributes, reference-fields, cost-codes, departments, mapping]
relevance: "medium"
---

## Summary
Pattern for letting a single Infigo user route orders to different printIQ cost centers / departments via checkout attributes. Create an Infigo Checkout Attribute (e.g. "Cost Code"), add it to checkout, then map it into a printIQ reference field via the Connect: PrintIQ plugin's Additional Reference Fields Mapping section.

## Key takeaways
- Map by the **internal name** of the attribute, NOT the display name.
- Path: `Infigo Admin > Connect: PrintIQ Plugin > Configure Plugin > Additional Reference Fields Mapping`.
- One Infigo login can drive multiple printIQ cost codes via attribute selection.
- Does NOT merge orders — each reference still creates a separate order in printIQ.
- Same approach works for any per-order structured custom data (project numbers, job references, etc.).
- Reminder from FAQ: **POD products only** for this kind of reference field mapping. Stock products do not carry mapped custom fields into printIQ — use Notes field for Stock.

## Related
[[connectid-printiq-overview]]
[[connectid-printiq-faq]]
