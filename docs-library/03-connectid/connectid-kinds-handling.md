---
title: "Kinds Handling in Connect: PrintIQ"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2544/kinds-handling-in-connect-printiq"
type: "article"
date: "unknown"
tags: [connectid, printiq, kinds, batch, records, pages, data-mapping, plugin-settings]
relevance: "high"
---

## Summary
PrintIQ supports the concept of "Kinds" = number of versions of a job. A "kind" can come from either the number of records (a batch/CSV with multiple entries) or the number of pages (a multi-page MegaEdit artwork). This setting controls how Infigo computes and sends the Kinds value to PrintIQ. Configurable globally on the Connect: PrintIQ plugin or per product variant.

## Key takeaways
- Three modes for Kinds Handling:
  - **No Handling** — no Kinds value is sent. PrintIQ defaults to 1.
  - **Number of records** — send the job's record count as Kinds.
  - **Number of pages** — send the job's page count as Kinds.
- **Number of records/pages per kind** field appears only when Number of records or Number of pages is selected. Defines the divisor (e.g. set to 2 to send 1 kind for every 2 pages).
- Lives under Connect: PrintIQ Plugin Settings (Global) -> **Data mapping** group.
- Per-product override is available — that's the per-variant Kinds Handling field you see on individual products.
- Selection of Number of records is the relevant setting for batch/CSV (MegaEdit) jobs feeding into PrintIQ.

## Code / config snippets
Plugin path: `Admin > Connect Plugins > Configure [Connect: PrintIQ] > Data Mapping`

Fields:
- `Kinds handling` — dropdown: No Handling / Number of records / Number of pages
- `Number of records/pages per kind` — integer (only visible when not "No Handling")

## Related
[[connectid-printiq-overview]]
[[connectid-printiq-faq]]
[[connectid-preventing-duplicate-artwork]]
