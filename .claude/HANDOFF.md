# HANDOFF — infigo-hacks

**Updated:** 2026-11-18 (night) CST · **Branch:** `docs/closeout-2026-11-18-coupon` (off `main`) · repo is PUBLIC
**State:** pushed · PRs infigo-hacks #10 / mexgen-agent #4 merged; tonight's work rides on two new PRs (see Next steps) · memory updated

## Next steps
1. **Review and merge tonight's two PRs** (owner only): infigo-hacks `docs/closeout-2026-11-18-coupon` (roadmap + handoff)
   and mexgen-agent `docs/spec5-leading-minus-quarter` (SPEC §5: baseline = top + (leading% − 0.25) × size). Never merge from Claude.
2. **Coupon card v-02: import it** (copy/rename/hide v-01 if it has orders), get a site PDF, and check the baselines
   (amount 94.55, store 218.28, expires 233.50 trim space). v-02 MEX sits in the job folder's `WebReady/`. Memory `coupon-card-mex.md`.
3. **Three-version postcard MEX: customer proof review** (sent 2026-11-16). Ask the owner whether alterations came back; otherwise import-test v-01. Memory `three-version-postcard-mex.md`.

## Open loops
- [ ] Multi-location business card redesign v3: import-verified 2026-11-18 and sent to the customer. Waiting on the customer to (a) add the missing license line to one location's front, and optionally (b) re-export the art with bleed. Either way it's just a clipart swap: rerun the job folder's `Working/assets-v2/tools/` scripts. Memory `location-bc-redesign-mex.md` (carried 2x)
- [ ] Winter camp flyer (2-sided, 16 camp fields + URL QR): v-03 import-tested OK by the owner 2026-11-18 (groups, captions, per-side forms all good). Open: Bello Script -> Leckerli One substitution not yet confirmed with the customer; print-PDF baseline measurement not done. Memory `winter-camp-flyer-mex.md` (carried 3x)
- [ ] Three-version postcard v-01: customer review pending, then import test. First generated Show/Hide logic rule on the storefront. Memory `three-version-postcard-mex.md`; note `docs-library/04-megaedit/two-version-dropdown-show-hide-generated.md` (carried 3x)
- [ ] Coupon card: v-01 printed the amount 36 pt low on its first order; that order's PDF was patched and reprinted OK (2026-11-18). v-02 built on the general line model, import pending. Canva Sans → Poppins swap still unconfirmed with the customer. Memory `coupon-card-mex.md` (carried 4x)
- [ ] Infigo API ticket (2026-10-01): `orderlineitem/get` returns `ProductAttributes: []`. Record the reply in `docs-library/01-official-infigo/api-order-line-attributes.md` + memory `infigo-api-product-attributes-empty.md`; fallbacks are in that note. (carried 5x)

## Gotchas
- Public repo. Before every commit, grep the staged diff for personal names, shop name, client names, storefront URLs, order/job ids, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory `infigo-hacks-repo-is-public.md` has the full list.
- **MegaEdit single-line text** ignores font metrics: baseline = frame top + (leading% − 0.25) × size (0.95 at 120 %), and a frame under 1.3 × size gets its type shrunk, even with fit-to-box off. The `0.25 × size` shift is visible as a `cm` before `BT` in the site PDF's content stream. Fonts with tall hhea metrics (script faces) go badly wrong under an hhea-based derivation. `MexGen Agent/SPEC.md` §5.
- A wrong line in an order's live-text PDF can be fixed by editing that frame's `cm` translate in the content stream (pikepdf), then re-measuring the baseline.
- Customer InDesign PDFs exported without bleed clip every frame at trim; lifting the MediaBox shows nothing. A mirrored CMYK edge raster under the vector page works.
- `python -I` hides the user site-packages where PyMuPDF lives; use `-P` instead for your own scripts.
- `*.pdf` and `*.mex` are blanket-ignored. Commit author must be the GitHub noreply address.

## Pointers
- Memory: `coupon-card-mex.md` (latest job), `location-bc-redesign-mex.md`, `winter-camp-flyer-mex.md`, `three-version-postcard-mex.md`, `infigo-hacks-repo-is-public.md`
- `ROADMAP.md` (public): Now / Next / Later
- `MexGen Agent/SPEC.md` §5 (geometry + text line model), §9, §15 for logic/dropdown shapes

## Log
- 2026-11-18 night — Coupon card v-01's first order printed the amount 36 pt low. Root cause: MegaEdit's line model is `top + (leading% − 0.25) × size`, font-agnostic, and v-01 used hhea leading (183 %). Order PDF patched and reprinted OK; v-02 built (validates 0/0); SPEC §5 generalised.
- 2026-11-18 late — Open loops triaged with the owner: storefront imports run (closed), old history accepted (closed), R13 check and QR edges dropped, location-data question deferred to ROADMAP Next, docs written. PRs infigo-hacks #10, mexgen-agent #4.
- 2026-11-18 evening — Five-location business card redesign: v1 MEX patched onto new customer art; measured the 0.95/1.3 line model, and v3 landed every baseline at 0.00 pt. Sent to the customer.
