# Client Thank You Cards — Two-Version Static PDF Build Spec

PrintIQ product: **Client Thank You Cards + Blank Envelopes** (one ConnectID code; envelopes already included in the PrintIQ product — no envelope product/attribute needed in Infigo).

## Build

1. **Two Static PDF products** — Catalogue → Products → Product Management → Add new.
   - Product Type: `Static PDF`. Upload the version PDF. Name: `Client Thank You Card – Version A` / `– Version B`.
   - Set allowed quantities / min qty to match PrintIQ pack sizes. Add a product image (preview of the card) for each.
   - Do NOT try a "Version" radio attribute on one product — attributes/attribute combinations swap price/SKU/image, not the static PDF. Two products is the correct pattern.
2. **Single landing page (optional)** — Add new → Product Type `Custom` → Custom Product Type `Multi Product Custom`. Assign both Static PDF products as children. Customer picks Version A/B from one page; the chosen child is what goes to the basket.
3. **ConnectID mapping (one code, both products)** — Search "product groups" → Product Groups → Add new `Client Thank You Cards + Blank Envelopes` → add both Static PDF products → Connect Link → ExternalId = the PrintIQ product code → Save. Both children inherit. (Alt: Connect Link on each product variant row with the same code — Path 1.)
   - Map the CHILDREN, not the Multi Product Custom parent.
4. **Pricing** — SKU-to-SKU mapping = live GetPrice works. Verify price appears on both products at test quantities.
5. **Visibility** — assign both products (and parent) to the client's category/customer role; hide from other groups via department/pricing visibility.
6. **Test** — add Version A qty 100 → checkout → confirm PrintIQ job lands on the correct product, qty 100, correct PDF attached; envelopes come from the PrintIQ product definition.

## Caveats
- Envelope count = card count only because PrintIQ bundles them. If the client later wants envelopes optional, add a checkbox attribute with per-unit price delta (scales with qty) and map via Attribute Combination to a second PrintIQ code.
- Kit product was rejected: children become separate SPO jobs → would need a second ConnectID mapping for envelopes, and Kit has no "pick exactly one" radio.
- No native "product as attribute" auto-add-to-cart feature found in Academy/Zendesk (Sept 2026).

Related: businesscard-two-product-build-spec.md, docs-library/02-printiq/connect-printiq-mapping-products.md
