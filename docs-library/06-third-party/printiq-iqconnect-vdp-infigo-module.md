---
title: "IQconnect — VDP (printIQ's connector range, including Infigo module)"
source: "vendor-blog"
url: "https://printiq.com/iqconnect-vdp/"
type: "technical-guide"
date: "2025-01-31"
publisher: "printIQ"
tags: [printiq, infigo, iqconnect, vdp, chili-publish, xmpie, vpress, integration, architecture]
relevance: "high"
---

## Summary
PrintIQ's own product page describing the IQconnect-VDP module family. Confirms Infigo is one of FOUR sanctioned printIQ VDP editor integrations (alongside CHILI publish, XMPie uStore, and Vpress) — our shop is on the most-deeply-integrated branch.

## Key takeaways
- **The four sanctioned printIQ VDP integration partners:**
  1. **CHILI publish** — document editor over API
  2. **Infigo** — "Infigo document editing … tightly integrating Infigo via APIs to deliver template information, metadata, and artwork files within printIQ"
  3. **XMPie uStore** — XML-based, no SKU mapping required, status updates push back to uStore
  4. **Vpress** — full B2B/B2C with DAM, RFQ, file checking
- **From PrintIQ's POV, "printIQ is both the ordering system and the MWS"** — so the job is "sitting in production once the order is completed" via Infigo's API push. Confirms the design intent: PrintIQ side wants Infigo orders to land already-priced and production-ready, not as raw web requests needing re-quoting.
- **Architectural note:** PrintIQ markets these as parallel options — customers pick the one matching the editor strength they need. Infigo is positioned as the "all-in-one" choice (storefront + editor + integration), versus CHILI/XMPie which are pure editors.
- **Caveat (explicit on the page):** "Please note that the Infigo software must also be purchased" — confirms PrintIQ doesn't bundle Infigo licensing.
- **IQconnect range structure:** 4 categories — API, Automate, Pre-Press, VDP. VDP is the editor-integration bucket where Infigo sits.

## Code / config snippets
None — product overview, not technical doc. Mentions "tightly integrating via APIs to deliver template information, metadata, and artwork files" but no specifics.

## Related
[[dlpmag-infigo-printiq-extend-relationship]]
[[digitalprinter-infigo-printiq-partnership]]
[[printweek-infigo-strong-year-us-demand]]
