# Infigo Hacks — Roadmap

Living hub for documenting and solving gaps in the Infigo storefront platform that Infigo itself hasn't addressed.

## Now
- **Name-badge batch product — ConnectID re-introduction.** Test order with custom pricing script worked. Investigating whether ConnectID can be re-attached for PrintIQ order routing without re-triggering the batch cart-multiplication bug. Confirmed 2026-05-27: with pricing script OFF + ConnectID GetPrice ON, 22-record CSV produces ~$7,000 (multiplier still fires). Two remaining paths: (a) test **"Use parent pricing for versioned uploads"** cart setting on a clone, or (b) commit to **routing-only** architecture (custom script for pricing + empty GetPrice JSON + ConnectID for checkout submission only). See the batch / cart multiplication section in `docs-library/INDEX.md`.
- **Name-badge batch product — final QA.** Pricing script regenerated with v2 generator (cart-multiplier safe), CSV image-swap via `AlbumName/ImageName.ext` confirmed working. Place a test order end-to-end and verify the $138 total holds through checkout + the correct image renders per record on the final PDF.

## Next
- Build the split-CSV + two-template workflow as a reusable pattern in `docs-library/` for the **non-image-swap** subset of the Variable Logic gap (multi-field show/hide from CSV still needs split-CSV).
- Document the CSV image-swap hack (`AlbumName/ImageName.ext`) as a positive pattern in `docs-library/07-invent/`.
- Document the architectural ceiling for Variable Logic in batch as a known limitation in `docs-library/07-invent/`.

## Later
- Host the Pricing Script Generator (`pricing-generator.html`) on Cloudflare Pages / Vercel / Railway so it can be iframed into the an internal team site.
- Build additional script generators for other recurring Infigo problem classes (one-off → reusable).
- Periodic docs-library refresh pass when Infigo / PrintIQ ship major versions.
- If the Variable-Logic-in-batch pattern recurs across enough projects, stub-test `types-for-megascript` (Server-Side ExecutionType) to definitively rule out the server-side path. Probably hits the same wall but worth knowing.

## Closed / Won't Do
- ~~Editor-runtime MegaScript bridge for Invent Variable Logic in CSV batch.~~ Confirmed impossible after 9 probes. SaveFields doesn't propagate to render. Variables.Set doesn't trigger Variable Logic in batch context. Both preview AND output PDF render with the wrong background.
- ~~CSV-driven image swap research.~~ Solved 2026-05-27 — `AlbumName/ImageName.ext` syntax in CSV cell works for per-record image swap (Infigo docs say no file extension; empirically wrong). Solves the image-swap subset of the Variable Logic gap. Background swap should now use a full-bleed image field, not Variable Logic.
- ~~Pricing generator v2.~~ Universal cart-safe formula `(unitPrice × totalQty + SETUP_FEE) / (orderQty × recordCount)` works for all 3 modes. Replaces v1 which silently broke Per Record / Per Copy modes. Lives at `pricing-generator.html`.
- ~~Auto-add "Blanks" static PDF to cart on MegaEdit add.~~ Researched — NopCommerce Required Products auto-adds but customer can't set qty; cross-sell allows qty but requires click. Best path for "include N blanks" is a single product with a qty attribute, not a bundle. Held pending re-prompt from customer.
- ~~File the 5-question Infigo support ticket.~~ Held — Infigo would quote ~$3k for a custom script; not worth it for this project scale.
- ~~Two minor side bugs.~~ Noted here, not worth a ticket on their own: `Admin.Mex.UiMessages.Scripts.Normal.NotFound` raw translation key; `Multiple placeholders found in text field` warning.

## Operating principles
- Verify behavior empirically against actual cart/storefront — Infigo docs are thin.
- Grep `docs-library/` BEFORE web searching.
- Bypass PrintIQ live pricing for batch products — use custom Infigo pricing scripts.
- Build reusable generators, not one-off fixes.
- When working in editor scripts: pick the right NPM package (`types-for-megaedit` for browser, `types-for-megascript` for server) and the right ExecutionType on Admin → MegaEdit Product Scripts.
- Don't ticket Infigo for non-bugs they'd quote a custom script for — the cost-benefit rarely works for our project sizes.
