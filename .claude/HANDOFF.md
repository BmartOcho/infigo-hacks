# HANDOFF — infigo-hacks

**Updated:** 2026-11-18 · **Branch:** `docs/closeout-2026-11-18` (off `main`) · repo is PUBLIC
**State:** this closeout committed, NOT pushed · MexGen Agent repo: branch `fix/variable-ui-label-and-form-groups` (3 commits) NOT pushed · memory updated

## Next steps
1. **Push + PR both branches when the owner says so**: this repo's `docs/closeout-2026-11-18`, and MexGen
   Agent's `fix/variable-ui-label-and-form-groups` (ui.label caption fix, form GROUPs, per-page forms via
   `formPages`; all import-verified 2026-11-18). Never merge.
2. **Three-version postcard MEX: customer proof review** (sent 2026-11-16). Ask the owner whether
   alterations came back; otherwise import-test v-01. Memory `three-version-postcard-mex.md`.
3. Coupon card v-01 import test (memory `coupon-card-mex.md`): still pending.

## Open loops
- [ ] Winter camp flyer (2-sided, 16 camp fields + URL QR): v-03 import-tested OK by the owner 2026-11-18 (groups, captions, per-side forms all good). Open: Bello Script -> Leckerli One substitution not yet confirmed with the customer; print-PDF baseline measurement not done. Memory `winter-camp-flyer-mex.md`
- [ ] Three-version postcard v-01: customer review pending, then import test. First generated Show/Hide logic rule on the storefront. Memory `three-version-postcard-mex.md`; note `docs-library/04-megaedit/two-version-dropdown-show-hide-generated.md`
- [ ] Coupon card v-01: import test + baseline measurement pending; font substitution unconfirmed — memory `coupon-card-mex.md` (carried 2x)
- [ ] New-storefront build: has publish-all import sheet (import 3, Drive `Product Imports`) been run? Then the four static PDF products; three PDFs need the owner to name their product. Detail in the Drive customer `HANDOFF.md` (storefront-build memory entry). (carried 3x)
- [ ] Owner decision: a cart note committed 2026-10-07 carried a client name, a storefront host and a customer name. Files fixed (PR #5); old text still in `main` history. (carried 3x)
- [ ] Infigo API ticket (2026-10-01): `orderlineitem/get` returns `ProductAttributes: []`. Record the reply in `docs-library/01-official-infigo/api-order-line-attributes.md` + memory `infigo-api-product-attributes-empty.md`; fallbacks are in that note. (carried 3x)
- [ ] Location data outside the template: send Infigo the yes/no question in memory `infigo-template-edit-breaks-reorders.md`. (carried 3x)
- [ ] Multi-location business card R13 is being built by hand (2026-09-28, new location added). Optional check once it's live: `python "Claude outputs/location-dropdowns/tools/diff_json_vs_mex.py" <R13 export.json> <R13.mex>` to confirm only the new location changed. Known data flags worth folding into a revision are listed in memory `infigo-template-edit-breaks-reorders.md`. (carried 5x)
- [ ] QR business card edges (from ROADMAP "Now"): required flags on TEXT, blank cell-number rendering, whether the bound `vCard` variable must stay in the form; spot-UV element list still needed before `--spot-uv` runs. (carried 5x)
- [ ] Docs-library write-ups queued in `ROADMAP.md` "Next": CSV image-swap album syntax and the Variable-Logic-in-batch ceiling (`experiments/invent-scripts-slot-test/RESULTS.md`). (carried 4x)

## Gotchas
- Public repo. Before every commit, grep the staged diff for personal names, shop name, client names, storefront URLs, order/job ids, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory `infigo-hacks-repo-is-public.md` has the full list.
- `mexgen build` still refuses `logic`; the postcard build emits `logicRules[]` itself. Show/Hide action shape and the `defaultActions` (ruleItem with `conditions: []`) come from `mexgen/dump-event-flyer/InDesignData.json`.
- PyMuPDF lives in Python 3.13 (`C:\Python313\python.exe -P`); fontTools + mexgen builds run on 3.12 `-P`; `mexgen.py validate` runs via `py` WITHOUT `-P`.
- Customer PDFs with a `-9,-9` mediabox origin: normalise onto a zero-origin 414x324 page (`show_pdf_page`) before measuring. fitz reports the trimbox x unshifted.
- `*.pdf` and `*.mex` are blanket-ignored. Commit author must be the GitHub noreply address.

## Pointers
- Memory: `winter-camp-flyer-mex.md` (latest job), `three-version-postcard-mex.md`, `coupon-card-mex.md`, `infigo-hacks-repo-is-public.md`
- `ROADMAP.md` (public): Now / Next / Later
- `docs-library/07-invent/logic-rules-json-schema.md` + `MexGen Agent/SPEC.md` §9, §15 for logic/dropdown shapes

## Log
- 2026-11-18 — Two-sided camp flyer MEX v-01..v-03: v-01 import showed "Job Title" over every input (donor variable `ui.label` leaked through cloning) -> fixed in MexGen; v-02 added form GROUPs; v-03 one form per page (`forms.pages[].pageIndex` 0/1), first use of that shape, import-verified. Docs: `docs-library/07-invent/mex-file-format-anatomy.md`, MexGen `SPEC.md` §10.
- 2026-11-16 10:20 CST — Three-version postcard MEX v-01 (dropdown: two mailers + contact card, Show/Hide rule, parent-linked inputs) built from two live MEX files + new customer art; `validate --strict` clean; proof sent to customer.
- 2026-11-16 09:15 CST — Coupon card (8.5x3.5, 2-sided) MEX v-01 built with the MexGen builder: three editable back-side lines over a redacted background, `validate --strict` clean. Not import-tested yet.
- 2026-11-13 17:55 CST — Storefront build: rep magnet template built and verified from site PDFs; product list cross-checked against the customer's list; import sheets for new products, category moves and publish-all.
