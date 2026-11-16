# HANDOFF — infigo-hacks

**Updated:** 2026-11-16 09:15 CST · **Branch:** `docs/closeout-2026-11-16` (PR open into `main`) · repo is PUBLIC
**State:** PR #7 merged; local `main` pulled · this closeout is the only open PR · nested `MexGen Agent/` untouched

## Next steps
1. **Coupon card MEX import test (built 2026-11-16).** Memory `coupon-card-mex.md` has the paths. Ask
   the owner whether the product has been created and the v-01 `.mex` imported. If it has, download a site
   PDF, measure the three live-text baselines against the build values in that memory, and build v-02
   with the offsets folded in if any line is off by more than 0.3 pt. Also ask whether the customer is OK
   with Poppins Regular standing in for Canva Sans on the store line.
2. Check PR #8 (this closeout) is merged; if not, ask the owner. Never merge it yourself. Then
   `git switch main && git pull`.
3. Ask the open questions carried from 2026-11-13 (Open loops below): publish-all import 3, the cart-note
   history decision, and whether the (carried 3x+) loops should be dropped.

## Open loops
- [ ] Coupon card v-01: import test + baseline measurement pending; font substitution unconfirmed — memory `coupon-card-mex.md`
- [ ] New-storefront build: has publish-all import sheet (import 3, Drive `Product Imports`) been run? Then the four static PDF products; three PDFs need the owner to name their product. Detail in the Drive customer `HANDOFF.md` (storefront-build memory entry). (carried 2x)
- [ ] Owner decision: a cart note committed 2026-10-07 carried a client name, a storefront host and a customer name. Files fixed (PR #5); old text still in `main` history. (carried 2x)
- [ ] Infigo API ticket (2026-10-01): `orderlineitem/get` returns `ProductAttributes: []`. Record the reply in `docs-library/01-official-infigo/api-order-line-attributes.md` + memory `infigo-api-product-attributes-empty.md`; fallbacks are in that note. (carried 2x)
- [ ] Location data outside the template: send Infigo the yes/no question in memory `infigo-template-edit-breaks-reorders.md`. (carried 2x)
- [ ] Multi-location business card R13 is being built by hand (2026-09-28, new location added). Optional check once it's live: `python "Claude outputs/location-dropdowns/tools/diff_json_vs_mex.py" <R13 export.json> <R13.mex>` to confirm only the new location changed. Known data flags worth folding into a revision are listed in memory `infigo-template-edit-breaks-reorders.md`. (carried 4x)
- [ ] QR business card edges (from ROADMAP "Now"): required flags on TEXT, blank cell-number rendering, whether the bound `vCard` variable must stay in the form; spot-UV element list still needed before `--spot-uv` runs. (carried 4x)
- [ ] Docs-library write-ups queued in `ROADMAP.md` "Next": CSV image-swap album syntax and the Variable-Logic-in-batch ceiling (`experiments/invent-scripts-slot-test/RESULTS.md`). (carried 3x)

## Gotchas
- Public repo. Before every commit, grep the staged diff for personal names, shop name, client names, storefront URLs, order/job ids, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory `infigo-hacks-repo-is-public.md` has the full list.
- Python 3.12: use `-P` for scripts that need PyMuPDF/fontTools (user site), but run `MexGen Agent/mexgen.py` WITHOUT `-P`, or it can't import `mexgen_validate` from its own folder.
- Removing editable text from a supplied PDF: PyMuPDF `apply_redactions(images=NONE, graphics=LINE_ART_NONE, text=REMOVE)` with `fill=False` and rects trimmed to the ink band. Rects spanning full glyph bboxes would also take neighbouring lines.
- Product Excel import: an update row overwrites every column. Build update sheets from a fresh export only.
- `*.pdf` and `*.mex` are blanket-ignored. Commit author must be the GitHub noreply address.

## Pointers
- Memory: `coupon-card-mex.md` (latest job), the storefront-build entry, `infigo-hacks-repo-is-public.md`
- `ROADMAP.md` (public): Now / Next / Later
- Recipe used for MegaEdit text products: the rep-magnet `build_mex.py` (Drive storefront folder, `Sales Rep Magnets\Working\mexbuild\`)

## Log
- 2026-11-16 09:15 CST — Coupon card (8.5x3.5, 2-sided) MEX v-01 built with the MexGen builder: three editable back-side lines over a redacted background, `validate --strict` clean. Not import-tested yet.
- 2026-11-13 17:55 CST — Storefront build: rep magnet template built and verified from site PDFs; product list cross-checked against the customer's list; import sheets for new products, category moves and publish-all.
- 2026-11-13 — Genericized and committed the pending notes; fixed an already-public cart note that named a client; deleted merged local branches.
