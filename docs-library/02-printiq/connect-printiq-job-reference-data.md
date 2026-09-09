---
title: "Sending Additional Job Reference Data | CI_PrintIQ_006"
source: "printiq-kb"
url: "https://academy.infigo.net/p/344/sending-additional-job-reference-data-ci_printiq_006"
type: "tutorial"
date: "2022-12-01"
tags: [connectid, reference-fields, placeholders, mapping, pod, stock-products]
relevance: "high"
---

## Summary
How to map arbitrary Infigo data into PrintIQ's "Job Reference Fields" using Infigo placeholders (e.g., `%JobId%`, `%CustomName%`). The mapping is key/value pairs where Key = exact PrintIQ Job Reference Field name and Value = a placeholder template. The FAQ notes this works for POD products only — Stock products do NOT carry mapped reference fields. Tutorial video: https://www.youtube.com/embed/VoJUVS2mQeE

## Key takeaways
- Enable: Configure Connect:PrintIQ → check **Send additional Reference fields** → mapping table appears.
- Each row:
  - **Key** = the PrintIQ Job Reference Field name, MUST match exactly (case-sensitive likely).
  - **Value** = Infigo placeholder string, e.g. `%JobId%`, `%CustomName%`. Multiple placeholders can be combined to build composite values.
- **Find placeholders:** admin search "placeholder" → **Placeholder Overview**. Expand `>` next to each placeholder for description and example. **Copy** button puts the placeholder on clipboard wrapped in `%...%`.
- **Two scopes of placeholder:**
  - **Order-specific** — officially supported for Invoices and Packing Slips (whole-order context).
  - **Orderline-specific** — officially supported for Job Tickets (per-line-item context).
  - Some cross-use works but is unsupported.
- **Hard limit (from FAQ):** Additional Reference Field Mapping only fires for POD products. Stock products won't pass mapped fields to PrintIQ — use the Notes field as a workaround.
- Don't forget to also click **Save** at the top of the plugin config screen — saving an individual row is not enough.

## Code / config snippets

Example mapping rows (Key → Value):

```
JobId           → %JobId%
CustomerOrder   → %OrderNumber%
EndUserName     → %CustomerFirstName% %CustomerLastName%
CustomName      → %CustomName%
```

## Related
[[connect-printiq-faq]]
[[connect-printiq-other-config]]
