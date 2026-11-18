# HANDOFF — infigo-hacks

**Updated:** 2026-11-18 (evening) CST · **Branch:** `docs/closeout-2026-11-18` (off `main`) · repo is PUBLIC
**State:** pushed · PRs #9 / #3 already merged earlier on 2026-11-18. The evening commits ride on new PRs (see Next steps) · memory updated

## Next steps
1. **Review and merge the two evening PRs** (owner only): infigo-hacks `docs/closeout-2026-11-18` → main
   (closeout + roadmap), and mexgen-agent `fix/variable-ui-label-and-form-groups` → main (SPEC §5
   single-line text model, import-verified 2026-11-18). Never merge from Claude.
2. **Three-version postcard MEX: customer proof review** (sent 2026-11-16). Ask the owner whether
   alterations came back; otherwise import-test v-01. Memory `three-version-postcard-mex.md`.
3. Coupon card v-01 **is imported**. Get its site PDF from the owner, measure the baselines against the build values
   (amount 94.55, store 218.28, expires 233.50 trim space), and build v-02 with the SPEC §5 line model if they're off.

## Open loops
- [ ] Multi-location business card redesign v3: import-verified 2026-11-18 and sent to the customer. Waiting on the customer to (a) add the missing license line to one location's front, and optionally (b) re-export the art with bleed. Either way it's just a clipart swap: rerun the job folder's `Working/assets-v2/tools/` scripts. Memory `location-bc-redesign-mex.md`
- [ ] Winter camp flyer (2-sided, 16 camp fields + URL QR): v-03 import-tested OK by the owner 2026-11-18 (groups, captions, per-side forms all good). Open: Bello Script -> Leckerli One substitution not yet confirmed with the customer; print-PDF baseline measurement not done. Memory `winter-camp-flyer-mex.md` (carried 2x)
- [ ] Three-version postcard v-01: customer review pending, then import test. First generated Show/Hide logic rule on the storefront. Memory `three-version-postcard-mex.md`; note `docs-library/04-megaedit/two-version-dropdown-show-hide-generated.md` (carried 2x)
- [ ] Coupon card v-01: imported (confirmed 2026-11-18); baseline measurement from the site PDF pending; Canva Sans → Poppins swap unconfirmed with the customer. Memory `coupon-card-mex.md` (carried 3x)
- [ ] Infigo API ticket (2026-10-01): `orderlineitem/get` returns `ProductAttributes: []`. Record the reply in `docs-library/01-official-infigo/api-order-line-attributes.md` + memory `infigo-api-product-attributes-empty.md`; fallbacks are in that note. (carried 4x)

## Gotchas
- Public repo. Before every commit, grep the staged diff for personal names, shop name, client names, storefront URLs, order/job ids, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory `infigo-hacks-repo-is-public.md` has the full list.
- **MegaEdit single-line text** ignores font metrics: baseline = frame top + 0.95 × size, and a frame under 1.3 × size gets its type shrunk, even with fit-to-box off. Size frames `size × leading%` and they come out about 92% scale. `MexGen Agent/SPEC.md` §5.
- Customer InDesign PDFs exported without bleed clip every frame at trim; lifting the MediaBox shows nothing. A mirrored CMYK edge raster under the vector page works (rasterize a text-free copy, or the lettering mirrors into the bleed).
- `python -I` hides the user site-packages where PyMuPDF lives; drop `-I` for your own scripts.
- `mexgen build` still refuses `logic`; the postcard build emits `logicRules[]` itself. Show/Hide shape comes from `mexgen/dump-event-flyer/InDesignData.json`.
- `*.pdf` and `*.mex` are blanket-ignored. Commit author must be the GitHub noreply address.

## Pointers
- Memory: `location-bc-redesign-mex.md` (latest job), `winter-camp-flyer-mex.md`, `three-version-postcard-mex.md`, `coupon-card-mex.md`, `infigo-hacks-repo-is-public.md`
- `ROADMAP.md` (public): Now / Next / Later
- `MexGen Agent/SPEC.md` §5 (geometry + text line model), §9, §15 for logic/dropdown shapes

## Log
- 2026-11-18 late — Open loops triaged with the owner: storefront imports run (closed), old history accepted (closed), R13 check and QR edges dropped, location-data question deferred to ROADMAP Next, docs written (`04-megaedit/csv-image-swap-album-syntax.md`, `07-invent/variable-logic-batch-ceiling.md`). PRs infigo-hacks #10, mexgen-agent #4.
- 2026-11-18 evening — Five-location business card redesign: v1 MEX patched onto new customer art (fonts, left-aligned layout, separate label color set, synthesized bleed). v2 import showed single-line type shrunk to 92%; measured the 0.95/1.3 line model, and v3 landed every baseline at 0.00 pt. Sent to the customer.
- 2026-11-18 — Two-sided camp flyer MEX v-01..v-03: caption leak fixed in MexGen, form GROUPs, one form per page (`forms.pages[].pageIndex`), import-verified.
