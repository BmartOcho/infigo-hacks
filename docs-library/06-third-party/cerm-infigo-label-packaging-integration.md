---
title: "CERM and Infigo Join Forces: A Seamless Integration for the Future of Label and Packaging Printing"
source: "vendor-blog"
url: "https://www.cerm.net/blog/cerm-and-infigo-join-forces-seamless-integration-future-label-and-packaging-printing"
type: "article"
date: "2023-10-30"
publisher: "CERM (Belgium-based label/packaging MIS vendor)"
tags: [infigo, cerm, label, packaging, w2p, mis-integration, w4l, w4p, api, artwork-upload, preflight]
relevance: "high"
---

## Summary
CERM's own write-up of the Connect: CERM integration. Worth keeping because the integration architecture is unusually well-described — CERM is reusing the same open APIs as their existing W4L (Web4Labels) / W4P frontend, meaning Infigo essentially plugs into CERM's first-party W2P slot. Strong analog for how PrintIQ's Connect: printIQ likely works under the hood.

## Key takeaways

**Architecture (the interesting bit):**
- "The CERM-Infigo interface uses the **same open APIs as used for our very own W4L/W4P solution**." Translation: Infigo is treated as a drop-in replacement for CERM's native frontend. Implies the API contract is feature-complete, not a watered-down side door.
- Same APIs handle: estimate retrieval, order creation, customer/contact database sync, artwork upload, preflight.

**Workflow contract:**
1. Customer configures packaging product in Infigo (options, material, finish, artwork upload).
2. Infigo pushes structured order data to CERM MIS.
3. CERM creates the job, links it to tooling, estimates cost and time.
4. Artwork flows from Infigo → CERM with automated preflight.
5. Reorders push directly back through Infigo.

**Database sync (often overlooked):**
- "Seamless sync between both customer and contact databases ensures data is always up-to-date and accurate across both platforms." Two-way customer/contact sync — not just one-way order push. Useful contrast: do we know whether ConnectID / Connect: printIQ does the same?

**Industry framing:**
- "Infigo, supplier of no-doubt one of the most sophisticated web-to-print software solutions" — third-party validation language from a peer MIS vendor.
- CERM-Infigo integration was launched globally at Labelexpo Europe 2023, then USA launch at Labelexpo Chicago.

**Why this matters for our shop (general-commercial, not labels):**
- The same Connect Flow pattern our shop uses for PrintIQ is what label shops use for CERM. Cross-reading helps when reverse-engineering Connect Flow capability.
- Helpful when arguing for two-way customer sync in PrintIQ ↔ Infigo via your own ConnectID setup.

## Code / config snippets
None published — architectural narrative only.

## Related
[[packagingimpressions-enfocus-infigo-connect-app]]
[[printiq-iqconnect-vdp-infigo-module]]
