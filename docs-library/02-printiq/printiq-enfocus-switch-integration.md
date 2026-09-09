---
title: "IQ - Enfocus Switch Integration"
source: "printiq-docs"
url: "https://printiq.com/printiq-and-enfocus-switch-integration/"
type: "article"
date: "2018-03-22"
tags: [enfocus, switch, pitstop, prepress, hotfolders, automation, iqconnect-automate]
relevance: "medium"
---

## Summary
PrintIQ's marketing page for the IQconnect-Automate integration with Enfocus Switch + PitStop. Documents the full automated handoff from PrintIQ MIS to Enfocus Switch for preflight, proofing, RIP, and email workflows, with status flowing back to PrintIQ production boards. Relevant for understanding what happens to artwork after it leaves Infigo via ConnectID — the Switch hotfolder is the next stop in most production shops.

## Key takeaways
- **Data flow:** PrintIQ delivers artwork + job metadata to Enfocus Switch. Switch runs preflight (PitStop Server), generates proofs, dispatches emails, imposes, and routes to RIP. Switch passes status back to PrintIQ so production boards update automatically.
- **Hotfolders are PitStop Server-driven**, automatically checking and correcting incoming PDFs. Same secure download-link mechanism that Infigo uses to send artwork to PrintIQ is also used to feed Switch hotfolders (per Connect:PrintIQ FAQ).
- **What you can achieve out of the box:**
  - Automated preflight on submission
  - Automated proof delivery to/from customers
  - Job/artwork routing to queue based on job type
  - Auto imposition
  - Direct push to press RIP queue or onto the press
- This is part of the IQconnect-Automate module (one of the four IQconnect categories).
- Has been a shipping integration since at least 2018 (post date), so very mature.

## Related
[[iqconnect-api-overview]]
[[connect-printiq-faq]]
