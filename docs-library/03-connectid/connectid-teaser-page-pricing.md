---
title: "Enabling and Troubleshooting Quote Creation from Teaser Pages with PrintIQ"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2208/enabling-and-troubleshooting-quote-creation-from-teaser-pages-with-printiq-integration"
type: "article"
date: "unknown"
tags: [connectid, printiq, teaser, category-page, quote, auto-quote, add-to-basket]
relevance: "medium"
---

## Summary
When customers Add to Basket directly from a category (teaser) page, Infigo can auto-create or update a PrintIQ quote so the item enters the basket at the correct price instead of $0.00. Requires three settings together: Price Handling on Teaser Pages, Show quantity selector on Product Teaser, and Auto Create Quote.

## Key takeaways
- Setting 1: `Admin > Configuration > Settings > Integrations > Connect Settings > Price Handling on Teaser Pages` — enable.
- Setting 2: `Admin > Configuration > Settings > Catalog Settings > Show quantity selector on Product Teaser` — enable.
- Setting 3: `Admin > Configuration > Settings > Quote Settings > Auto Create Quote` — enable.
- The Connect: PrintIQ plugin must already be active and configured.
- Conflicts with the FAQ note that "teaser pages don't support real-time PrintIQ pricing" — this article describes the supported workaround via auto-quote creation at Add-to-Basket time, not real-time display while browsing.

## Related
[[connectid-printiq-overview]]
[[connectid-printiq-faq]]
