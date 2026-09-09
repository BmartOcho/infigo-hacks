---
title: "Basic Setup | CI_PrintIQ_001"
source: "printiq-kb"
url: "https://academy.infigo.net/p/339/basic-setup-ci_printiq_001"
type: "tutorial"
date: "2022-12-01"
tags: [connectid, setup, credentials, plugin, v0, v1, infigo]
relevance: "high"
---

## Summary
Step-by-step setup of the Connect:PrintIQ plugin inside Infigo admin. Documents the V0/V1 credential split, the dedicated-API-user pattern, and the "Check Connection" smoke test. Tutorial video: https://www.youtube.com/embed/6_-URTmqW8w

## Key takeaways
- Admin path: search "connect" → **Connect Settings** → enable **Connect: PrintIQ** → search "connect" again → **Connect Plugins** → **Configure** next to Connect:PrintIQ.
- **Required inputs (V0 credentials):**
  - printIQ instance URL
  - Username
  - Password
  - Application Name
  - Application Key
- All four V0 credentials must come from the **printIQ support team** — they provision them on the printIQ instance.
- **Best practice:** create a dedicated printIQ user for the integration rather than reusing a real user's login. Many integrators do this.
- **V1 credentials** are for the newer product/inventory sync feature (still rolling out at the time of writing). Safe to leave blank if you're only using V0 functionality.
- V1 unlocks: creating stock + static-PDF products in Infigo from printIQ, and live inventory/stock-level fetches.
- **Check Connection** button: green popup = success, red popup = misconfigured. If red, raise a ticket with Infigo support.
- Tutorial created Dec 2022 by Sam Webster.

## Related
[[connect-printiq-overview]]
[[connect-printiq-mapping-customers]]
