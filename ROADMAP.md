# Infigo Hacks — Roadmap

Living hub for documenting and solving gaps in the Infigo storefront platform that Infigo itself hasn't addressed.

## Now
- **Product-attribute values via the REST API — Infigo ticket open (2026-10-01).** `orderlineitem/get` returns the right line but `ProductAttributes: []` for a Static (type 30), PrintIQ-quoted product whose dropdown attribute shows in the Order Line Detail report. That contradicts the spec. Checkout attributes don't fit (the codes are per-product, and the store has many departments). Fallbacks while waiting: parse the job-ticket PDF, or map the orderline `Attributes` placeholder into a PrintIQ Additional Reference Field (POD only). Write-up: `docs-library/01-official-infigo/api-order-line-attributes.md`.
- **QR business card, CSV batch — PASSED on the sixth import (2026-09-28).** Five-row batch on the storefront: every QR decodes to its own row, navy, text at 0.00 pt from the approved PDF. Six imports produced eight verified MEX facts, all in `docs-library/07-invent/mex-file-format-anatomy.md` and the generator's SPEC: trim-origin coordinates, batch as four in-file switches, the `Barcode Field` script, variable-bound barcodes, the XML colour carrier, exports never carrying editor changes. Spec: `qr-business-card-vdp-build-spec.md`. Left at the edges: required flags on TEXT, blank-cell-number rendering, whether the bound `vCard` variable must stay in the form. The `vdp/` engine still owns print and the spot-UV mask; the mask's element list is still to be specified.
- **Repo went public 2026-09-09.** Everything committed must stay free of personal, shop, and client identifiers (see README "What's not in this repo"). Next content push: turn the CSV image-swap finding below into a proper `docs-library/07-invent/` doc.
- **Name-badge batch product — final QA.** Pricing script regenerated with v2 generator (cart-multiplier safe), CSV image-swap via `AlbumName/ImageName.ext` confirmed working. Place a test order end-to-end and verify the $138 total holds through checkout + the correct image renders per record on the final PDF.

## Next
- **Location data outside the MegaEdit template (researched 2026-09-28, deferred).** Multi-location business cards bake every address and phone number into the template, and replacing a template breaks reorders, so each small data edit costs a full product revision (copy → rename → hide old but keep orderable; one product is on its thirteenth). Candidate fix: one last revision where Address/Main/Fax are plain text variables, filled by an Editor script that looks the chosen location up in an admin-managed Custom Data Category (`types-for-megaedit` `EditorData` + `Invent.Variables.Set`). Blocked on: Infigo confirming the Custom Data Category admin screen, and a throwaway-product test that attaching a script doesn't break reorders. Watch the batch caveat in Closed below (`Variables.Set` in CSV batch).
- Build the split-CSV + two-template workflow as a reusable pattern in `docs-library/` for the **non-image-swap** subset of the Variable Logic gap (multi-field show/hide from CSV still needs split-CSV).
- Document the CSV image-swap hack (`AlbumName/ImageName.ext`) as a positive pattern in `docs-library/07-invent/`.
- Document the architectural ceiling for Variable Logic in batch as a known limitation in `docs-library/07-invent/`.

## Later
- Host the Pricing Script Generator (`pricing-generator.html`) on Cloudflare Pages / Vercel / Railway so it can be iframed into the an internal team site.
- Build additional script generators for other recurring Infigo problem classes (one-off → reusable).
- Periodic docs-library refresh pass when Infigo / PrintIQ ship major versions.
- If the Variable-Logic-in-batch pattern recurs across enough projects, stub-test `types-for-megascript` (Server-Side ExecutionType) to definitively rule out the server-side path. Probably hits the same wall but worth knowing.

## Closed / Won't Do
- ~~Name-badge batch product: re-attach ConnectID.~~ Settled 2026-10-01 with custom Infigo pricing scripts, which avoid the batch cart-multiplication bug. Neither the parent-pricing cart setting nor routing-only ConnectID was needed.
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
