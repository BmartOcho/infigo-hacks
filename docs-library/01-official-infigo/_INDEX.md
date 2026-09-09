# Official Infigo Docs — Local Library Index

Harvested from `academy.infigo.net` (Infigo Academy) + `infigosoftware.zendesk.com` (Help Desk). All docs are public-facing tutorials, articles, FAQs, or developer references. 33 files total.

Grouped by topic. One-line hook per doc.

---

## Pricing Scripts (Generic + Custom)

- [Generic Pricing Script | The Basics](generic-pricing-script-basics.md) — `pricing-script, generic-pricing-script, csv, basics` — Foundational walkthrough: attach script to product variant, build CSV, upload to Global Additional Data; default error price = £10,000; trailing comma on last config line breaks scripts.
- [Generic Pricing Script | Tiered Pricing](generic-pricing-script-tiered.md) — `pricing-script, tiered-pricing, debug-mode` — Multiple CSV rows per attribute combo (one per quantity tier); `useTierPrice:true`, `debugMode:true`, Test button on variant page.
- [Generic Pricing Script | Multi-part CSV Pricing](generic-pricing-script-multipart-csv.md) — `pricing-script, performance, multi-part-csv` — Split CSVs >1000 entries across a subdirectory using `subDirectory`, `baseFileName`, `separator`, `splitMapping`; set `filePath:""`.
- [Generic Pricing Script Overview | Time-Saving Toolbox](generic-pricing-script-overview-toolbox.md) — `pricing-script, time-saver` — One CSV in Global Additional Data can drive many products; swap CSV to bulk-update all attached products.
- [Pricing Script Examples](pricing-script-examples.md) — `pricing-script, examples` — Live sample storefront at training.infigosoftware.com/pricingscripts.
- [Pricing Script Interface Documentation](pricing-script-interface-documentation.md) — `pricing-script, api-ref, typescript` — Dev reference at infigo-official.github.io/types-for-pricing-scripts + NPM types package for custom-script IntelliSense.
- [Pricing Scripts (Category Index)](pricing-scripts-category-index.md) — `pricing-script, navigation` — Curated reading order for the 6 pricing-script articles on Academy.

## Built-in Pricing (no scripts)

- [Quantity Based Pricing](quantity-based-pricing.md) — `pricing, tier-pricing, unit-price` — Quantity-tier setup via UI; price entered as order-line total (engine divides by quantity for unit display); set minimum basket qty to lowest tier.
- [Enhanced Tier Pricing with Attribute-Based Grouping](enhanced-tier-pricing-attribute-grouping.md) — `pricing, share-tiers, cart` — "Share Tiers on Cart" sums quantities across multi-line cart instances (same product, same product + attrs, or same product + selected attrs).
- [Rounding adjustment on pricing](rounding-adjustment-on-pricing.md) — `pricing, rounding, gotcha` — Banking vs Commercial rounding; **DISABLE rounding when using Quantity Based Pricing** or cart formatting breaks.
- [How to Control Pricing Visibility by Viewer](pricing-visibility-control.md) — `pricing, visibility, settings` — Bulk-hide all pricing via toggle; per-user-type hiding requires Infigo Support.
- [Setting Up Department-Specific Pricing](department-specific-pricing.md) — `pricing, departments, discounts` — Use a 100% discount with department-requirement, NOT a separate pricing system — head office free, stores pay normally.

## ConnectID / printIQ Integration

- [Connect: printIQ (Overview)](connect-printiq-overview.md) — `connectid, printiq, mapping, sync` — Canonical integration doc: plugin setup, customer/product/shipping mapping, tax-code matching, additional reference fields, status-update webhooks, POD/stock sync, live inventory + pricing.
- [Connect: printIQ FAQ](connect-printiq-faq.md) — `printiq, faq, troubleshooting` — Stock products do NOT support Additional Reference Field Mapping (POD only); use Notes field as workaround. Teaser pages can't show printIQ prices. 1:1 customer-to-external-ID only.
- [Connect: printIQ Product Sync](connect-printiq-product-sync.md) — `printiq, product-sync, master-storefront` — Master Storefront relay for multi-storefront sync; `MASTER_` prefix on template products/categories; v1 base64 token required for sync.
- [Connect: printIQ Custom Quoting](connect-printiq-custom-quoting.md) — `printiq, custom-quoting, attributes` — Custom UI builds GetPrice JSON without per-combination SKUs; 4-level inheritance hierarchy (variant > combo > attribute > attribute value).
- [Why are my PrintIQ shipping methods showing duplicates at checkout](printiq-shipping-duplicates.md) — `printiq, shipping, fixed-rate` — Disable Fixed Rate Shipping when using printIQ-rated shipping; OR enable `LegacyUseActiveShippingMethodsFiltering` + per-method `FixedRateIsActiveShippingMethodId{ID}` toggles.

## MegaEdit / VDP

- [Introducing the MegaEdit editor interface](megaedit-editor-interface.md) — `megaedit, editor, basics, bleed` — UI tour: Back/Menu, canvas switcher, snap modes, page-bleed black-and-red boxes, left tabs (Fields/Images/Pages/Tools).
- [How to Apply MegaEdit Variables](megaedit-variables-applying.md) — `megaedit, variables, cross-product` — Same variable set on multiple products = linked field values + thumbnails; apply text styling BEFORE saving as default or thumbnails won't reflect it; interlinked session = basket items keep old values.
- [Prepopulate Data Script (MegaEdit)](prepopulate-data-script-megaedit.md) — `megaedit, scripts, personalization` — Auto-fill MegaEdit text fields from customer-account fields; enable per-product on Scripts tab.
- [MegaScripts: Form-to-Order Automation](megascripts-form-to-order.md) — `megascripts, api, automation` — Turn an HTML form submission into an Infigo order (no login, no checkout); JSON config maps form fields to customer + order data via `${...}` placeholders.

## MultiPart Products (Upload + Batching)

- [Multi-version product ordering with Multipart Upload](multipart-versioning-bg050.md) — `multipart, versioning, batch, spo` — **Infigo's native batch flow**: "Enable versioning" on MultiPart variant; N versions per cart line with their own quantities + PDFs; total qty drives tier pricing; each version becomes a separate SPO job.
- [Infigo MultiPart Product Config Builder](multipart-config-builder.md) — `multipart, xml, parts, preview` — UI tool that generates MultiPart XML config — global settings (preview mode, editor mode, page numbers), localization, advanced 3D/flipbook previews, Parts definitions.

## Product Attributes

- [Product Attributes](product-attributes.md) — `product, attributes, control-types` — Two-step model: create attribute group at Catalogue > Attributes, then attach to product variant with prompt + control type. File upload supports jpg/jpeg/png/gif/bmp/pdf/csv/txt/tiff/tif/xls/xlsx/ai.
- [Product Attribute Grouping](product-attribute-grouping.md) — `product, attributes, html, css` — Wrap related attributes in a single `<div>` for CSS targeting; one group per attribute per product; group display order = lowest member display order.

## Customers / Bulk Ops

- [Customer CSV Bulk Import](customer-csv-bulk-import.md) — `customers, csv, bulk-import` — Bulk create/update customers via CSV; column headers case-sensitive; Departments and Regions must exist on system first; double-quote in passwords must be escaped (`"test""*2"`).
- [Import or Reset Customer Budgets with CurrentBudget Column](customer-budget-csv-import.md) — `customers, csv, budgets, ledger` — Add `CurrentBudget` column to customer-import CSV; choose Replace/Add/Ignore at upload time; writes ledger entries.

## Budgets

- [Creating and Using Budgets](budget-creating-and-using.md) — `budgets, credit, per-user` — Budget = credit on an INDIVIDUAL user (Budgets tab); **gotcha:** default behaviour charges the overspend to another method — not a hard cap unless you enable "sufficient budget" enforcement.
- [Budget Manager Workflow](budget-manager-workflow.md) — `budgets, budget-manager, enforcement` — Request-and-approve top-ups; assign budget manager (admin, 1 per user); unhide PrePay tab; **tick "Checkout allowed only with sufficient budget" = the hard cap.**
- [Budget Management (extended)](budget-management-extended.md) — `budgets, megascript, department, cron` — **Per-group budgets:** Budgets MegaScript auto-tops-up by Department ID on a cron; TopUpOnly/TopUpTo/TopUpStrict; one instance per department; support must install the script. Still per-user, NOT a shared pot.

## Output / Hotfolders / Sync

- [Infigo Sync FAQs](infigo-sync-faqs.md) — `infigo-sync, hotfolder, filename, status-update` — **CRITICAL filename rule:** files must START with `%TypeLetter%_%OrderID%_%JobID%_` for SPO status updates. Polls every 30s minimum. Windows-only (Mac requires VM).
- [Understanding Storefront-Based Hotfolder Configuration](storefront-based-hotfolder-config.md) — `hotfolder, multi-storefront, admin` — Platform-level "Enable Hotfolders Per Storefront" toggle isolates hotfolder matching to active storefront only. New platforms default ON; existing platforms with orders default OFF (Legacy/Shared).

---

## Release Notes

- [Infigo Release Notes – August 2026](infigo-release-notes-2026-08.md) — `release-notes, mex, job-ticket, fit-to-box, promo-code, customer-csv-import, api` — Job Tickets/Invoices/Packing Slips as Invent-built MEX templates; Fit Width by Tracking; non-printing preview fields; PrintIQ promo-code passthrough; Language/Currency import columns; deferred-payment + budget APIs; "Use paged PDF media" perf.

## Coverage gaps / known issues

- The **Prepopulate Data Script** page had a large base64 image embedded that exceeded fetch limits — wrote summary doc from search snippets + companion academy index nav.
- **MegaEdit Crash Course (IV_#Intro_002)** and the **MegaEdit category landing page** were not in the WebFetch provenance set (search returned only as a result, no direct fetch path) — would need a fresh search round to capture.
- **Infigo Megascripts Documentation** (academy.infigo.net/c/266) — only fetched one sample script (Form-to-Order); the full Megascripts reference category was not crawled.
- **API Documentation** (academy.infigo.net/c/262) — surfaced in nav but not fetched. Likely contains the platform's REST API reference.
- **Infigo Sync install / setup guide** (`/p/488` and `/p/1462`) — referenced by FAQ doc but not separately fetched.
- The Connect: printIQ overview's "Custom Quoting" and "Data sent to IQ" sections are summarized at high level — full custom-quoting JSON schema is on the dedicated Custom Quoting tutorial page.
