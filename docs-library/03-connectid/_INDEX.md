# ConnectID Docs Library — Index

Documentation harvested from Infigo Academy on the **Connect: PrintIQ** plugin (Infigo's ConnectID bridge to PrintIQ MIS).

## Files

| File | What it covers |
|------|----------------|
| [connectid-printiq-overview.md](connectid-printiq-overview.md) | Master setup guide: plugin install, customer/product/shipping/tax mapping, webhooks, paid flags, reference fields, live pricing, custom quoting prerequisites |
| [connectid-printiq-faq.md](connectid-printiq-faq.md) | Common gotchas — 1:1 customer ID, unpriced lines error, teaser limits, Stock-vs-POD reference field limitation, artwork security |
| [connectid-kinds-handling.md](connectid-kinds-handling.md) | **Kinds Handling**: No Handling / Number of records / Number of pages, records-per-kind divisor. Global + per-product |
| [connectid-preventing-duplicate-artwork.md](connectid-preventing-duplicate-artwork.md) | `Use Existing Artwork Reference` setting — sends ReplaceQQADAKey to avoid PIQ duplicate PDFs (relates to Trigger Post Artwork Logic) |
| [connectid-product-sync.md](connectid-product-sync.md) | Multi-tier sync: platform / master storefront / per-storefront. Master_ product + category blueprints. Inventory + Static POD field maps |
| [connectid-shipping-sync.md](connectid-shipping-sync.md) | Live PIQ delivery rates at checkout (`Use Print IQ Delivery Rates`) + required `Append additional order line items to the same quote` |
| [connectid-checkout-attribute-mapping.md](connectid-checkout-attribute-mapping.md) | Route a single Infigo login to multiple PIQ cost codes via Checkout Attributes mapped to PIQ reference fields |
| [connectid-teaser-page-pricing.md](connectid-teaser-page-pricing.md) | Auto-quote creation on Add to Basket from category teaser pages — the 3-setting combo |
| [connectid-custom-quoting-price-lists.md](connectid-custom-quoting-price-lists.md) | Sept 2025 upgrade: select WholesalePricelist / RetailPricelist globally or per product/variant/combination |

## Key references not yet harvested

- **Zendesk Help Desk articles** (https://infigosoftware.zendesk.com/hc/en-us/categories/360004277671-Connect-Plugins-Integrations) returned empty in WebFetch — likely JS-rendered. Open directly in browser if needed.
- **Connect: printIQ FAQ** page (https://academy.infigo.net/p/2085) was successfully harvested but FAQ entries are short — full Zendesk articles are richer.

## Notes / gaps

- Could not directly access several Zendesk article URLs (Dynamic Upload, Connect: printIQ Zendesk version) — they returned empty content. The Academy versions are the substantive ones.
- Pricing scripts pages live under MegaEdit folder (per scope rule) since they're VDP/batch-script related.
- Two of the deep-link academy URLs (e.g. `https://academy.infigo.net/c/532/connect-printiq` and `https://academy.infigo.net/c/75/connect-printiq`) were not in the provenance set; the content was instead pulled via the `c/360/printiq` and individual `p/NNNN` URLs.
