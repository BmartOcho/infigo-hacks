---
title: "IQconnect - Automate (Enfocus, Esko, FreeFlow Core, HP, Prinergy)"
source: "printiq-docs"
url: "https://printiq.com/iqconnect-automate/"
type: "article"
date: "2024-12-01"
tags: [iqconnect-automate, prepress, enfocus, esko, freeflow-core, hp-box, prinergy, xml, automation]
relevance: "medium"
---

## Summary
IQconnect-Automate is PrintIQ's umbrella for prepress/RIP integrations. Covers five named integrations: Enfocus Switch, Esko (Automation Engine + WebCenter), Xerox FreeFlow Core, HP Box (PrintOS), and Kodak Prinergy. All five share the same pattern: PrintIQ exports job XML + artwork → external system runs preflight/impose/RIP → status flows back to PrintIQ via API.

## Key takeaways
- **Common architecture for all integrations:** PrintIQ pushes artwork + job metadata; the prepress system processes (preflight, proof, impose, RIP); status updates flow back to PrintIQ via API to keep production boards synced. True two-way comms.
- **Enfocus Switch** — preflight (PitStop), proofs to/from customer, queue routing, impose, push to RIP/press.
- **Esko (Automation Engine + WebCenter)** — creates job in AE, runs workflow, soft-proofing via WebCenter, optional imposition via Layout module, interacts with Esko's artwork library for automated re-ordering.
- **Xerox FreeFlow Core** — push artwork + job data, imposition, transport to DFE/press RIP queue.
- **HP Box (PrintOS)** — preflight, imposition, RIP, email; jobs land in PrintOS queue.
- **Kodak Prinergy / PrePress module** — exports **Job XML** + PDFs to your prepress system. The XML can be auto-processed by Prinergy OR manually triggered via the **"Export Job XML"** button on the All Jobs Board / Production Board. This is the only documented manual XML export mechanism on the docs site.
- The "Export Job XML" function exists on the All Jobs Board and Production Board — useful detail for shops integrating with non-listed systems that can consume XML.
- "Connect Modules" are organized into 4 categories: API, Automate, Pre-Press, and VDP.

## Related
[[iqconnect-api-overview]]
[[iqconnect-vdp]]
[[printiq-enfocus-switch-integration]]
