---
title: "Understanding Storefront-Based Hotfolder Configuration"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2209/understanding-storefront-based-hotfolder-configuration"
type: "tutorial"
date: "unknown"
tags: [hotfolder, multi-storefront, output, admin, legacy-mode, storefront-based]
relevance: "high"
---

## Summary
Documents the platform-level toggle that controls whether hotfolders are matched platform-wide (Legacy / Shared mode) or scoped to the active storefront only (Storefront-Based mode). Default differs by platform age: existing platforms with orders default to Legacy; brand-new platforms default to Storefront-Based.

## Key takeaways
- The toggle setting: **"Enable Hotfolders Per Storefront"** in Platform Settings.
- **Location:** Log in as Platform Administrator > Switch Storefront > select the Platform level > admin search "Print Locations and Hotfolders" > Settings tab.
- **Legacy / Shared mode:** Hotfolders available platform-wide; orders from any storefront can match any active hotfolder.
- **Storefront-Based mode:** Hotfolders are filtered exclusively by the active storefront — orders only match hotfolders belonging to that storefront. Use this for per-brand isolation.
- **Default behavior:**
  - Existing platforms (with at least one order placed) = Legacy / Shared
  - Brand-new Infigo platforms (no orders) = Storefront-Based
- Setting can be changed at any time; switching modes does not delete hotfolders.

## Related
[[infigo-sync-faqs]]
