# PrintIQ Docs Library — Index

Local harvest of PrintIQ + Connect:PrintIQ documentation relevant to an Infigo storefront + PrintIQ MIS + ConnectID stack. Source mix: PrintIQ.com marketing/product pages, the v49 release notes PDF, and the Infigo Academy learning path for the Connect:PrintIQ plugin.

## Files

### Core API / Quoting (highest signal)
- [printiq-getprice-live-pricing.md](printiq-getprice-live-pricing.md) — `getprice, api, live-pricing, quoting, sku` — The GetPrice flow: productCode + quantity → estimate; SKU-to-SKU only.
- [iqconnect-api-overview.md](iqconnect-api-overview.md) — `api, iqconnect, integration, smartsite, punch-out, link` — Umbrella for the four IQconnect-API flavors (Integrate, Link, Punch-Out, SmartSite).
- [printiq-v49-release-notes.md](printiq-v49-release-notes.md) — `release-notes, getprice, acceptquote, webhooks, api` — Confirms endpoint names GetPrice + AcceptQuote, new webhooks, capacity-planner API, Pageflex/Kapua middleware, NodeJS Switch scripts.

### Connect:PrintIQ plugin (Infigo side — daily driver)
- [connect-printiq-faq.md](connect-printiq-faq.md) — `connectid, faq, errors, pod, stock-products, reference-fields` — The single most load-bearing doc: hard limits, "Unable to accept a quote that has unpriced lines", teaser pricing limitation, POD vs Stock reference field rules.
- [connect-printiq-learning-path.md](connect-printiq-learning-path.md) — `learning-path, setup` — Index of all 13 official CI_PrintIQ tutorials with codes.
- [connect-printiq-basic-setup.md](connect-printiq-basic-setup.md) — `setup, credentials, v0, v1` — Plugin install, V0/V1 credentials, Check Connection.
- [connect-printiq-mapping-customers.md](connect-printiq-mapping-customers.md) — `customers, external-id` — Customer Code mapping + storefront-default fallback.
- [connect-printiq-mapping-products.md](connect-printiq-mapping-products.md) — `products, sku, attribute-combinations, product-groups` — Three ways to map products to SKUs.
- [connect-printiq-shipping-mapping.md](connect-printiq-shipping-mapping.md) — `shipping, delivery, due-date` — ShippingMethodSystemName ↔ printIQ delivery method.
- [connect-printiq-invoices-paid-tax.md](connect-printiq-invoices-paid-tax.md) — `invoice, paid, tax, taxjar, fallback-taxcode` — Critical TaxJar `UNCALC` trick + paid-flag PO handling.
- [connect-printiq-job-reference-data.md](connect-printiq-job-reference-data.md) — `reference-fields, placeholders, pod` — Job Reference Field mapping via Infigo placeholders.
- [connect-printiq-other-config.md](connect-printiq-other-config.md) — `account-manager, customer-reference, order-submission` — Account managers + Order Submission approach (independent vs appended quotes).
- [connect-printiq-delivery-notes.md](connect-printiq-delivery-notes.md) — `checkout-attributes, notes` — Mapping Checkout Attributes to PrintIQ Delivery Notes / Special Instructions.
- [connect-printiq-product-sync.md](connect-printiq-product-sync.md) — `product-sync, webhooks, v1, base64-token, master-storefront` — V1 base64 token + master-storefront relay + webhook setup for PrintIQ → Infigo product sync.

### Custom Quoting (newer, replaces SKU explosion)
- [connect-printiq-custom-quoting.md](connect-printiq-custom-quoting.md) — `custom-quoting, parametric` — Concept overview.
- [connect-printiq-custom-quoting-config.md](connect-printiq-custom-quoting-config.md) — `custom-quoting, json, sections, job-operations, inheritance` — Full setup: PrintOnDemand/Stock/Custom modes, raw GetPrice JSON escape hatch, 4-level inheritance hierarchy.
- [connect-printiq-custom-quoting-example.md](connect-printiq-custom-quoting-example.md) — `custom-quoting, example, embellishments` — Worked example on a live demo product with size/material/embellishments.

### PrintIQ ecosystem (context for what's downstream of ConnectID)
- [iqconnect-automate-prepress.md](iqconnect-automate-prepress.md) — `prepress, enfocus, esko, freeflow-core, hp-box, prinergy, xml` — All five prepress/RIP integrations; mentions "Export Job XML" function on Production Board.
- [printiq-enfocus-switch-integration.md](printiq-enfocus-switch-integration.md) — `enfocus, switch, pitstop, hotfolders` — Switch + PitStop deep dive.
- [iqconnect-vdp.md](iqconnect-vdp.md) — `vdp, chili-publish, xmpie, vpress, infigo` — PrintIQ's framing of Infigo as a VDP partner.
- [printiq-third-party-integrations.md](printiq-third-party-integrations.md) — `integrations, partners, infigo, quickbooks, xero, avalara, windcave` — Master directory of partner integrations.

## Highest-priority finds (start here)
1. **`printiq-getprice-live-pricing.md`** + **`printiq-v49-release-notes.md`** — together they give you the GetPrice API: name + (productCode, quantity) signature + new v49 payment-info extension + the AcceptQuote sibling.
2. **`connect-printiq-faq.md`** — every failure mode you'll hit in production.
3. **`connect-printiq-custom-quoting-config.md`** — the escape hatch for batch/SKU explosion, including the raw GetPrice JSON field most people miss.
4. **`connect-printiq-other-config.md`** — Order Submission approach (independent quotes vs appended) controls how a multi-line cart becomes one or many PrintIQ quotes. Relevant to the cart-multiplication hack.
5. **`connect-printiq-product-sync.md`** — webhook architecture + master-storefront relay; relevant any time you wonder why a webhook isn't firing on a non-master storefront.

## Gaps (not findable on public web)
- **Full GetPrice / AcceptQuote schemas** — request/response shapes, error codes, full parameter lists. These live behind login in PrintIQ Support's docs portal. The v49 PDF and the Infigo Academy Live Pricing tutorial confirm the names + the high-level semantics (productCode, quantity, auto-accept flag, payment type/reference) but no JSON schema is public.
- **IQconnect API endpoint catalog** — no public list of endpoints. Credentials and full docs require PrintIQ Support provisioning.
- **PrintIQ KB / Zendesk** — printiq.zohodesk.com requires sign-in; the "kb article" tags throughout the v49 PDF link to it but content is gated.
- **Infigo Zendesk article 360047669051 (Connect: printIQ)** — fetched empty; appears to be JS-rendered or login-walled. The Infigo Academy learning path is the public equivalent.
- **PrintIQ Customer Portal / Kapua middleware** — only mentioned in v49 release notes (Pageflex integration); no detail page exists.
- **Webhook payload schemas** — confirmed webhooks exist (sales order item status; product sync; stock sync) but no payload examples public.

## Source mix
- `printiq-docs` — PrintIQ.com marketing/product pages (5 files)
- `printiq-kb` — Infigo Academy (the canonical public ConnectID how-to) (13 files)
- `printiq-api` — none directly; GetPrice/AcceptQuote facts pieced together from the Live Pricing tutorial and v49 PDF
- `printiq-blog` — none yielded high-signal content (mostly case studies)
- `printiq-youtube` — embedded throughout academy tutorials; URLs captured inline
