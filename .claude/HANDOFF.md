# HANDOFF — infigo-hacks

**Updated:** 2026-11-18 (evening) CST · **Branch:** `docs/closeout-2026-11-18` (off `main`) · repo is PUBLIC
**State:** this closeout committed on top of open PR #9, new commit NOT pushed · MexGen Agent repo: branch `fix/variable-ui-label-and-form-groups` (open PR #3) has one new commit (SPEC §5 line model), NOT pushed · memory updated

## Next steps
1. **Push the two new commits when the owner says so.** Each goes onto its open PR: this repo's
   `docs/closeout-2026-11-18` (PR #9) and MexGen Agent's `fix/variable-ui-label-and-form-groups` (PR #3,
   which adds the SPEC §5 single-line text model, import-verified 2026-11-18). Never merge.
2. **Three-version postcard MEX: customer proof review** (sent 2026-11-16). Ask the owner whether
   alterations came back; otherwise import-test v-01. Memory `three-version-postcard-mex.md`.
3. Coupon card v-01 import test (memory `coupon-card-mex.md`). Apply the SPEC §5 line model
   (height ≥ 1.32 × size, top = baseline − 0.95 × size) before importing: its frames used the old hhea model.

## Open loops
- [ ] Multi-location business card redesign v3: import-verified 2026-11-18 and sent to the customer. Waiting on the customer to (a) add the missing license line to one location's front, and optionally (b) re-export the art with bleed. Either way it's just a clipart swap: rerun the job folder's `Working/assets-v2/tools/` scripts. Memory `location-bc-redesign-mex.md`
- [ ] Winter camp flyer (2-sided, 16 camp fields + URL QR): v-03 import-tested OK by the owner 2026-11-18 (groups, captions, per-side forms all good). Open: Bello Script -> Leckerli One substitution not yet confirmed with the customer; print-PDF baseline measurement not done. Memory `winter-camp-flyer-mex.md` (carried 2x)
- [ ] Three-version postcard v-01: customer review pending, then import test. First generated Show/Hide logic rule on the storefront. Memory `three-version-postcard-mex.md`; note `docs-library/04-megaedit/two-version-dropdown-show-hide-generated.md` (carried 2x)
- [ ] Coupon card v-01: import test + baseline measurement pending; font substitution unconfirmed — memory `coupon-card-mex.md` (carried 3x)
- [ ] New-storefront build: has publish-all import sheet (import 3, Drive `Product Imports`) been run? Then the four static PDF products; three PDFs need the owner to name their product. Detail in the Drive customer `HANDOFF.md` (storefront-build memory entry). (carried 4x)
- [ ] Owner decision: a cart note committed 2026-10-07 carried a client name, a storefront host and a customer name. Files fixed (PR #5); old text still in `main` history. (carried 4x)
- [ ] Infigo API ticket (2026-10-01): `orderlineitem/get` returns `ProductAttributes: []`. Record the reply in `docs-library/01-official-infigo/api-order-line-attributes.md` + memory `infigo-api-product-attributes-empty.md`; fallbacks are in that note. (carried 4x)
- [ ] Location data outside the template: send Infigo the yes/no question in memory `infigo-template-edit-breaks-reorders.md`. (carried 4x)
- [ ] Multi-location business card R13 is being built by hand (2026-09-28, new location added). Optional check once it's live: `python "Claude outputs/location-dropdowns/tools/diff_json_vs_mex.py" <R13 export.json> <R13.mex>` to confirm only the new location changed. Known data flags worth folding into a revision are listed in memory `infigo-template-edit-breaks-reorders.md`. (carried 6x)
- [ ] QR business card edges (from ROADMAP "Now"): required flags on TEXT, blank cell-number rendering, whether the bound `vCard` variable must stay in the form; spot-UV element list still needed before `--spot-uv` runs. (carried 6x)
- [ ] Docs-library write-ups queued in `ROADMAP.md` "Next": CSV image-swap album syntax and the Variable-Logic-in-batch ceiling (`experiments/invent-scripts-slot-test/RESULTS.md`). (carried 5x)

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
- 2026-11-18 evening — Five-location business card redesign: v1 MEX patched onto new customer art (fonts, left-aligned layout, separate label color set, synthesized bleed). v2 import showed single-line type shrunk to 92%; measured the 0.95/1.3 line model, and v3 landed every baseline at 0.00 pt. Sent to the customer.
- 2026-11-18 — Two-sided camp flyer MEX v-01..v-03: caption leak fixed in MexGen, form GROUPs, one form per page (`forms.pages[].pageIndex`), import-verified.
- 2026-11-16 10:20 CST — Three-version postcard MEX v-01 (dropdown Show/Hide rule, parent-linked inputs) built; `validate --strict` clean; proof sent to customer.
