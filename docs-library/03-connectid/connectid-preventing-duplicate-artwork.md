---
title: "Preventing Duplicate Artwork in PrintIQ from Connect: PrintIQ"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2648/preventing-duplicate-artwork-in-printiq-from-connect-printiq"
type: "article"
date: "unknown"
tags: [connectid, printiq, artwork, qqadakey, pdf, replace-artwork, post-artwork, data-mapping]
relevance: "high"
---

## Summary
When a PrintIQ product already has a static PDF attached AND Infigo uploads artwork during order creation, you get two PDFs on the same job. Fix: enable `Use Existing Artwork Reference` in the Connect: PrintIQ plugin's Data Mapping section. Infigo will send `ReplaceQQADAKey` with the upload, telling printIQ to replace the existing artwork instead of attaching alongside it.

## Key takeaways
- **QQADAKey** = the artwork's internal identifier in printIQ.
- The `ReplaceQQADAKey` value is retrieved from the AcceptQuote API response.
- Feature is **disabled by default** — must be explicitly enabled.
- Multi-section products supported: each section is mapped to the correct QQADAKey so all PDFs in printIQ get replaced.
- Setting location: `Connect Plugins > Configure [Connect: PrintIQ] > Data Mapping > Use Existing Artwork Reference`.
- This setting is directly relevant to the author's per-variant **Trigger Post Artwork Logic** (Inherit / Disabled / Enabled) — the post-artwork logic is what fires the artwork upload that this setting governs.

## Code / config snippets
Plugin path:
```
Admin > Connect Plugins > Configure [Connect: PrintIQ] > Data Mapping > Use Existing Artwork Reference
  Enabled  -> Infigo sends ReplaceQQADAKey, replaces existing product PDFs in PrintIQ
  Disabled -> Infigo does not replace; uploaded file is added normally (DUPLICATE RISK)
  Default: Disabled
```

## Related
[[connectid-printiq-overview]]
[[connectid-kinds-handling]]
[[connectid-printiq-faq]]
