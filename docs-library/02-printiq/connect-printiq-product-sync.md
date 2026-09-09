---
title: "Connect: printIQ Product Sync | CI_printIQ_010"
source: "printiq-kb"
url: "https://academy.infigo.net/p/533/connect-printiq-product-sync-ci_printiq_010"
type: "tutorial"
date: "2023-05-30"
tags: [product-sync, category-sync, webhooks, v1, base64-token, master-storefront, stock, pod]
relevance: "high"
---

## Summary
Documents the V1-credentials path that lets PrintIQ push product and category creates/edits into Infigo automatically. Critically this is webhook-driven from the PrintIQ side and requires (a) V1 base64 token, (b) a "master storefront" relay on the Infigo side, and (c) PrintIQ Support to configure the actual webhooks on the PrintIQ instance. Sync is one-way only: PrintIQ → Infigo. Tutorial video: https://www.youtube.com/embed/bh8wuVITTiE

## Key takeaways
- **Auth = V1 Base64 token.** Obtained from PrintIQ Support. Required in addition to V0 creds for product sync to function.
- **Master storefront relay (critical):** PrintIQ historically only supported ONE webhook subscriber per instance. To allow multiple Infigo storefronts on the same Infigo platform to receive sync events, Infigo introduced a "switch context" setting:
  - Set at platform level: Connect Settings → **Storefront IDs allowed for switch context** → enter the storefront ID(s) of the master(s).
  - The master storefront is the single webhook target on PrintIQ's side; it then relays incoming notifications to the right storefront on the Infigo platform.
- **Two webhooks must be set up on PrintIQ:**
  - Print-on-demand products webhook
  - Stock products webhook
  - PrintIQ Support configures these.
- **Synced product types:** Stock products AND print-on-demand (static PDF) products. Each toggled independently in the plugin.
- **Fields synced (per PIQ → Infigo, listed by name only in the More Information popup):** name, description, activation status, SKU, dimensions, images, plus product-type-specific fields. Not every Infigo product field is synced.
- **Master Product / Master Category as templates:** because many Infigo settings are NOT brought over by the sync, you nominate template products/categories (prefix name with `MASTER_`) to fill in defaults for synced items.
- **Ignore Categories from Sync** toggle — if checked, the Master Category field flips to a **Default Product Category** field (all synced products go there). Useful if you want to control category hierarchy manually in Infigo.
- **Failure email** field — admins get notified when a sync fails.
- Sync is **one-way only: PrintIQ → Infigo**. Edits in Infigo do not push back.
- Pairs with inventory/stock-level sync (live stock fetch) — both rely on webhooks + base64 token.

## Related
[[connect-printiq-basic-setup]]
[[connect-printiq-faq]]
[[iqconnect-api-overview]]
