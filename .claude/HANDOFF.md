# HANDOFF — infigo-hacks

**Updated:** 2026-11-13 17:55 CST · **Branch:** `docs/closeout-2026-11-13` (PR open into `main`) · repo is PUBLIC
**State:** PRs #5 and #6 merged · this closeout is the only open PR · nested `MexGen Agent/` is on `main`, nothing unpushed

## Next steps
0. **New-storefront build (current job).** The customer-specific handoff is NOT in this repo. The
   storefront-build entry in the memory index points to `HANDOFF.md` in the Drive customer folder.
   First action next session: ask whether the publish-all import sheet (import 3, in the Drive
   `Product Imports` folder) has been run, then prepare the four static PDF products whose artwork
   matches clearly (print-ready files, thumbnails, import sheet). Three more PDFs need the owner to
   say which product they belong to.
0. **Owner decision:** a cart note committed 2026-10-07 carried a client name, a storefront host and a
   customer name. The files are fixed (PR #5), but the old text is still in `main` history.
1. **Check for Infigo's reply to the API ticket** (sent 2026-10-01): `orderlineitem/get` returns
   `ProductAttributes: []` for a line whose product attribute shows in the Order Line Detail report.
   Record their answer in `docs-library/01-official-infigo/api-order-line-attributes.md` (keep it
   generic) and in memory `infigo-api-product-attributes-empty.md` (which has the real ids). If they
   stall, try the fallbacks in that note: parse the job-ticket PDF, or map the orderline
   `Attributes` placeholder into a PrintIQ reference field.
2. **Location data outside the template — resume research.** Send Infigo support the yes/no
   question in memory `infigo-template-edit-breaks-reorders.md` (Custom Data Category access, and
   whether adding an Editor script breaks reorders). Context is in `ROADMAP.md` under "Next".

## Open loops
- [ ] Multi-location business card R13 is being built by hand (2026-09-28, new location added). Optional check once it's live: `python "Claude outputs/location-dropdowns/tools/diff_json_vs_mex.py" <R13 export.json> <R13.mex>` to confirm only the new location changed. Known data flags worth folding into a revision are listed in memory `infigo-template-edit-breaks-reorders.md`. (carried 3x)
- [ ] QR business card edges (from ROADMAP "Now"): required flags on TEXT, blank cell-number rendering, whether the bound `vCard` variable must stay in the form; spot-UV element list still needed before `--spot-uv` runs. (carried 3x)
- [ ] Docs-library write-ups queued in `ROADMAP.md` "Next": CSV image-swap album syntax and the Variable-Logic-in-batch ceiling (`experiments/invent-scripts-slot-test/RESULTS.md`). (carried 2x)

## Gotchas
- Public repo. Before every commit, grep the staged diff for personal names, shop name, client names, storefront URLs, order/job ids, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory `infigo-hacks-repo-is-public.md` has the full list.
- Product Excel import: an update row overwrites every column. Build update sheets from a fresh export only, and include only the rows being changed.
- The QR card `vdp` config in the repo (`vdp/customers/qr-business-card.json`) is genericized (ORG "Example Co"). For real print runs, use the private copy `Customer-CSV-Additions/qr-business-card-vdp/layout.private.json` with `/c/Python313/python.exe`. Memory `qr-business-card-product-status.md` has the details.
- Customer reports (Order Line Detail CSVs) contain real customer emails. They stay in Downloads; never copy them into the repo.
- Infigo's API docs site is a JS app. The raw OpenAPI YAML is at `https://api-lambda.public.infigosoftware.rocks/openapi`, and `/swagger.json`-style paths return 403.
- `*.pdf` and `*.mex` are blanket-ignored. Commit author must be the GitHub noreply address (already set in this repo's git config).
- Python: `C:\Program Files\Python312` has openpyxl, Pillow, PyMuPDF and reportlab, but in the user site, so `-I` hides them (use `-P`). Python 3.13 has no openpyxl or reportlab.

## Pointers
- Memory: the storefront-build entry in the memory index (current job), `infigo-api-product-attributes-empty.md`, `infigo-template-edit-breaks-reorders.md`, `infigo-hacks-repo-is-public.md`
- `ROADMAP.md` (public): Now / Next / Later
- `docs-library/01-official-infigo/prepopulate-data-script-megaedit.md` and `product-excel-bulk-import.md`: this week's findings

## Log
- 2026-11-13 17:55 CST — Storefront build: rep magnet template built and verified from site PDFs; product list cross-checked against the customer's list; import sheets for new products, category moves and publish-all. Docs: empty-form template works, category change on update replaces, update rows overwrite every column.
- 2026-11-13 — Genericized and committed the pending notes (Excel product import, Acrobat background-logo drop, image-variable clipart sets, mexgen agent plan, prefill spec correction). Fixed an already-public cart note that named a client. Deleted merged local branches.
- 2026-11-12 — Three-layout business card built with the MexGen builder and verified from site PDFs. Findings written to the prepopulate note and MEX anatomy note (PR #4): tag prefill needs `allowDirectText`, which strips span styling; hidden Invent variables prefill without it; download feature and field tags are XML-carried.
