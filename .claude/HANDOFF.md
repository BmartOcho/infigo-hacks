# HANDOFF — infigo-hacks

**Updated:** 2026-10-01 13:25 CDT · **Branch:** `main` · **HEAD:** see `git log -1`
**State:** `main` pushed to origin · pre-existing uncommitted work left untouched (see Gotchas) · memory updated · repo is PUBLIC

## Next steps
1. **Check for Infigo's reply to the API ticket** (sent 2026-10-01): `orderlineitem/get` returns
   `ProductAttributes: []` for a line whose product attribute shows in the Order Line Detail report.
   Record their answer in `docs-library/01-official-infigo/api-order-line-attributes.md` (keep it
   generic) and in memory `infigo-api-product-attributes-empty.md` (which has the real ids). If they
   stall, try the fallbacks in that note: parse the job-ticket PDF, or map the orderline
   `Attributes` placeholder into a PrintIQ reference field.
2. **Location data outside the template — resume research.** Send Infigo support the yes/no
   question in memory `infigo-template-edit-breaks-reorders.md` (Custom Data Category access, and
   whether adding an Editor script breaks reorders). Context is in `ROADMAP.md` under "Next".
3. **Nested private `MexGen Agent/` repo:** 13 commits still local. Push it once the owner confirms.

## Open loops
- [ ] Multi-location business card R13 is being built by hand (2026-09-28, new location added). Optional check once it's live: `python "Claude outputs/location-dropdowns/tools/diff_json_vs_mex.py" <R13 export.json> <R13.mex>` to confirm only the new location changed. Known data flags worth folding into a revision are listed in memory `infigo-template-edit-breaks-reorders.md`. (carried 2x)
- [ ] QR business card edges (from ROADMAP "Now"): required flags on TEXT, blank cell-number rendering, whether the bound `vCard` variable must stay in the form; spot-UV element list still needed before `--spot-uv` runs. (carried 2x)
- [ ] Docs-library write-ups queued in `ROADMAP.md` "Next": CSV image-swap album syntax and the Variable-Logic-in-batch ceiling (`experiments/invent-scripts-slot-test/RESULTS.md`).

## Gotchas
- Public repo. Before every commit, grep the staged diff for personal names, shop name, client names, storefront URLs, order/job ids, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory `infigo-hacks-repo-is-public.md` has the full list.
- Uncommitted work this session didn't make, left as found: `docs-library/INDEX.md`, `docs-library/07-invent/_INDEX.md`, `docs-library/07-invent/logic-rules-json-schema.md`, `mexgen/MEXGEN-AGENT-PLAN.md`. Ask before committing them.
- The QR card `vdp` config in the repo (`vdp/customers/qr-business-card.json`) is genericized (ORG "Example Co"). For real print runs, use the private copy `Customer-CSV-Additions/qr-business-card-vdp/layout.private.json` with `/c/Python313/python.exe`. Memory `qr-business-card-product-status.md` has the details.
- Local branch `backup/pre-genericize-2026-10-01` still has the customer name in it. Never push it; delete it once the push is confirmed good.
- Customer reports (Order Line Detail CSVs) contain real customer emails. They stay in Downloads; never copy them into the repo.
- Infigo's API docs site is a JS app. The raw OpenAPI YAML is at `https://api-lambda.public.infigosoftware.rocks/openapi`, and `/swagger.json`-style paths return 403.
- `*.pdf` and `*.mex` are blanket-ignored. Commit author must be the GitHub noreply address (already set in this repo's git config).

## Pointers
- Memory: `infigo-api-product-attributes-empty.md`, `infigo-template-edit-breaks-reorders.md`, `megaedit-editor-data-apis.md`, `infigo-hacks-repo-is-public.md`
- `ROADMAP.md` (public): Now / Next / Later
- `docs-library/01-official-infigo/api-order-line-attributes.md`: where customer-entered values live in the API

## Log
- 2026-10-01 13:25 CDT — Genericized the 13 unpushed commits (customer name, a real phone number) by rewriting local history only, then pushed `main`. Closed the name-badge QA item.
- 2026-10-01 13:05 CDT — Closed the name-badge ConnectID loop: settled with custom pricing scripts.
- 2026-10-01 12:50 CDT — Traced empty `ProductAttributes` on `orderlineitem/get` using Infigo's raw OpenAPI spec. Ruled out a wrong id against the report CSV; checkout attributes rejected (per-product codes, many departments). Infigo ticket sent; write-up added to docs-library.
