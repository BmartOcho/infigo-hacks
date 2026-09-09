---
title: "IQconnect - VDP (Chili Publish, Infigo, XMPie, Vpress)"
source: "printiq-docs"
url: "https://printiq.com/iqconnect-vdp/"
type: "article"
date: "2024-12-09"
tags: [iqconnect-vdp, vdp, chili-publish, xmpie, vpress, infigo, megaedit, variable-data]
relevance: "high"
---

## Summary
PrintIQ's VDP-tier integrations — partner editors that handle the document personalization piece, with PrintIQ doing pricing and production. Includes Infigo (the stack this library covers) plus Chili Publish, XMPie, and Vpress. This is the PrintIQ side's framing of the Infigo relationship: Infigo as a VDP partner whose MegaEdit-style web2print talks to PrintIQ via APIs.

## Key takeaways
- **Infigo VDP integration:** PrintIQ characterizes Infigo as a tightly integrated VDP editor that pushes template info + metadata + artwork into PrintIQ via APIs. This is the marketing-page mirror of the Connect:PrintIQ plugin docs on the Infigo side.
- **XMPie integration is the most automated of the bunch and worth noting:**
  - Two-way comms via XMPie API.
  - PrintIQ consumes XMPie data (XML) and generates a job OR Sales Order (pick 'n' pack) directly.
  - **No SKU-to-SKU mapping required** — PrintIQ creates a fully defined print job from XMPie orders without setup of SKUs in PrintIQ.
  - PrintIQ pushes status milestones back to XMPie automatically.
  - Customers stay in uStore; sales/production stay in PrintIQ.
- **Chili Publish:** PrintIQ pricing engine + ordering + Chili document editor via APIs.
- **Vpress Aspire B2B:** stock-level + price checks from Vpress B2B (or custom B2C), submits orders into PrintIQ MIS. Rich API, RFQ, DAM.
- All VDP integrations require the partner software to be purchased separately.

## Related
[[iqconnect-api-overview]]
[[iqconnect-automate-prepress]]
[[connect-printiq-overview]]
