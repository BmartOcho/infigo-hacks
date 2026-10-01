---
title: "What's New in Infigo | September 2026"
source: "infigo-academy"
url: "https://academy.infigo.net/p/3778/whats-new-in-infigo-september-2026"
type: "article"
date: "2026-09-30"
tags: [release-notes, megaedit, svg, custom-name, stock-products, product-attributes, printiq, artwork, purchase-order, connect-link, mis, api, duplicate-job, search, category-tags, page-builder, cdn, webp, security, punchout, siteflow, veracore, avalara, password-reset]
relevance: "high"
---

## Summary
September 2026 platform release (no version number stated; harvested 2026-10-01). Headline items: a drag-and-drop storefront page builder, a MegaEdit **SVG Shape field** delivered as a MegaEdit script, **custom names on every product type** (with a product-attribute link that carries the value to the order line), a PrintIQ setting that auto-raises purchase orders for PrintIQ-managed artwork, and a DuplicateJob API that now works on jobs in any state. Plus search, CDN/WebP image delivery, login-IP auditing, and SVG/XML upload hardening. The "Go To Full Release Notes" page (`/p/3623`) is a JS filter app and does not render to a plain fetch.

## Key takeaways

### MegaEdit / Invent
- **MegaEdit SVG Shape field** — customers place vector shapes and recolour them per element. Ships with circle, rectangle, triangle; storefronts add their own by uploading SVGs to **User Media** and **Clipart** categories. Dropped shapes become **General Shape** fields (move, scale, rotate, colour, tiling). Shapes render server-side, so they appear in cross-sell previews, headless processing, and generated PDFs.
  - Delivered as a **MegaEdit script** available to all storefronts. Apply globally from the **MegaEdit Scripts** page, or per product from the **Scripts** tab of that product's MegaEdit settings. Only products launched with the script applied get the field.
  - Every uploaded SVG passes a new server-side validator that rejects scripts, event handlers, external references, **embedded text**, and other unsafe elements. An SVG that carries live `<text>` will be rejected, so convert text to outlines first.
  - Detail: https://academy.infigo.net/p/3773
- **Custom names for all product types, including stock products** — four settings under **Configuration > Settings > Catalogue Settings → Custom names**: enable custom names, make them mandatory (with a separate stock-products option), and choose whether custom names replace product names in admin and print views. You can **link a product attribute to the custom name field**, so the customer sets it on the product page and the value goes straight to the order line. → Possible route for per-line values that `orderlineitem/get` drops (see [[api-order-line-attributes]]). Check whether the custom name comes back through the API before relying on it. Detail: https://academy.infigo.net/p/3775

### PrintIQ / ConnectID / MIS
- **"Mark artwork as submitted on quote acceptance"** — PrintIQ plugin, **Artwork** group. **Off by default.** When on, quote acceptance tells PrintIQ the artwork is submitted and ready, so PrintIQ can raise the purchase order automatically. It applies only to lines whose artwork is **managed in PrintIQ** and that have outsource supplier details configured in PrintIQ. Lines with Infigo-uploaded artwork are evaluated separately and are unaffected. Detail: https://academy.infigo.net/p/2689?tip=automatic-purchase-orders-for-printiq-products-whose-artwork-is-managed-in-printiq
- **"Default Connect plugin in external reference popup"** — a new dropdown on the **Connect Settings** page. It sets which MIS plugin the Connect Link popup pre-selects on records that have no external reference yet. If the chosen plugin is disabled or removed, it falls back to the first available one. Records that are already linked keep their plugin.
- **Connect Link popup restyle** — the title is now `Connect Link: {EntityType} - {EntityName}` (falls back to the record ID). printIQ help text now wraps and renders as plain text, and the empty white box is fixed. No configuration needed. Detail: https://academy.infigo.net/p/3777
- **PunchOut → HP Siteflow extrinsic** — PunchOut plugin **"Extrinsic to checkout attribute mapping"** (multiple mappings) stores a named PunchOut session value as a checkout attribute. Siteflow plugin **"Source order id format (Infigo placeholders)"** puts it into the submitted order id, so it prints on the shipping label.
- **Veracore** — checkout-attribute fields are now dropdowns instead of free text. The delivery-method → Veracore Freight Code table has a simpler editor, and placeholder settings link to the Placeholders reference.

### API
- **DuplicateJob (V2)** — you can now duplicate a job in **any** workflow state: in basket, saved as a project, unattached, or in an order. Before this it only worked on placed-order jobs. Each duplicate gets a new unique Job ID and the source job is not changed. With no associated order, the original job owner is used. There is an option to create the duplicate directly **in-basket**. → Useful for reorder and "copy last job" automation.

### Catalogue / Search / Storefront
- **Drag-and-drop page builder** — enable the content overlay on the live storefront, click an editable area, and a full-screen builder opens (component palette, live canvas, properties panel). Components: titles, images, buttons, text blocks, sliders, embeds, sections, columns. Supports undo/redo, duplicate, reorder, and desktop/tablet/mobile preview. Detail: https://academy.infigo.net/p/3772
- **Search Terms field** — custom keywords per product. Included in product import/export and in copy product. A new catalogue setting extends search to **SEO meta fields, teaser content, and product group name**. Detail: https://academy.infigo.net/p/3371
- **Category tag filter mode** — per-storefront setting. **"Any selected tag"** (default, the old behaviour) or **"All tag categories must match"** (AND across tag groups, OR within a group). Takes effect immediately with no reindex. Standard and Elasticsearch search return consistent results.
- **"Hide Product details button for"** (Catalogue Settings) — now one checkbox per enabled product type. Stock and Static always appear; other types appear when they are enabled. Existing config is kept.
- **Product images: S3 + CDN + responsive `srcset` + WebP + lazy loading.** **Disabled by default**; enabled per deployment once Infigo provisions the cloud infrastructure. New uploads go to cloud storage, existing images backfill in the background, and disk originals are kept.

### Customers / Security / Support
- **Shared-email password reset** — on storefronts with usernames enabled, the forgot-password page asks for **username + keyphrase**. Admins can also generate an account-specific reset link from the customer record (one link per account, expires after **1 day**). New setting: **"Enable forgot password page"**. A Password Changed email template and an activity-log entry are added automatically.
- **Support Recordings** — admins record screen and mic from inside Admin and share a secure link with Infigo Support. A new **Support Recordings** page lists recordings with Download / Copy Link / Delete. Admin-only, **on by default**.
- **Login IP auditing** — every new login records the client IP (proxy/load-balancer aware), and it is copied to Metabase Insights. Historical logins have no IP. Always on.
- **Stored-XSS hardening** — uploaded SVG/XML files are sanitised on upload and served with a restrictive CSP header. Always on, nothing to configure.

### Tax / Analytics
- **Avalara AvaTax** — new **Common Carrier / FOB Destination (FR025000)** option in the existing **Shipping tax code** dropdown.
- **PunchOut GA/GTM** — checkout now waits for tracking before the PunchOut redirect (with two safety timeouts). PunchOut purchase events are no longer dropped.

## Related
- [[infigo-release-notes-2026-08]] — previous month
- [[api-order-line-attributes]] — the attribute values that the order-line API drops; custom-name attribute link is a candidate workaround
- [[megaedit-scripts-config]] — where the SVG Shape script gets attached
- [[connect-printiq-other-config]] — PrintIQ order submission / quote acceptance context
- [[product-attributes]]
