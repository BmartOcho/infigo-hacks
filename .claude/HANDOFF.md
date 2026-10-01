# HANDOFF — infigo-hacks

**Updated:** 2026-10-01 12:50 CDT · **Branch:** `main` · **HEAD:** see `git log -1`
**State:** 11 commits unpushed · pre-existing uncommitted work left untouched (see Gotchas) · memory updated · repo is PUBLIC

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
3. **Push, after the owner confirms.** Eleven commits here and thirteen in the nested private
   `MexGen Agent/` repo exist only locally. Before pushing, consider renaming
   `qr-business-card-vdp-build-spec.md`: the content is generic but the filename has a customer name.

## Open loops
- [ ] ROADMAP "Now" still carries the name-badge batch product ConnectID question from May 2026 (parent-pricing cart setting test vs routing-only). Confirm whether it was resolved on the storefront and close or update it. (carried 3x)
- [ ] Multi-location business card R13 is being built by hand (2026-09-28, new location added). Optional check once it's live: `python "Claude outputs/location-dropdowns/tools/diff_json_vs_mex.py" <R13 export.json> <R13.mex>` to confirm only the new location changed. Known data flags worth folding into a revision are listed in memory `infigo-template-edit-breaks-reorders.md`. (carried 2x)
- [ ] QR business card edges (from ROADMAP "Now"): required flags on TEXT, blank cell-number rendering, whether the bound `vCard` variable must stay in the form; spot-UV element list still needed before `--spot-uv` runs. (carried 2x)
- [ ] Docs-library write-ups queued in `ROADMAP.md` "Next": CSV image-swap album syntax and the Variable-Logic-in-batch ceiling (`experiments/invent-scripts-slot-test/RESULTS.md`).

## Gotchas
- Public repo. Before every commit, grep the staged diff for personal names, shop name, client names, storefront URLs, order/job ids, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory `infigo-hacks-repo-is-public.md` has the full list.
- Uncommitted work this session didn't make, left as found: `docs-library/INDEX.md`, `docs-library/07-invent/_INDEX.md`, `docs-library/07-invent/logic-rules-json-schema.md`, `mexgen/MEXGEN-AGENT-PLAN.md`. Ask before committing them.
- Customer reports (Order Line Detail CSVs) contain real customer emails. They stay in Downloads; never copy them into the repo.
- Infigo's API docs site is a JS app. The raw OpenAPI YAML is at `https://api-lambda.public.infigosoftware.rocks/openapi`, and `/swagger.json`-style paths return 403.
- `*.pdf` and `*.mex` are blanket-ignored. Commit author must be the GitHub noreply address (already set in this repo's git config).

## Pointers
- Memory: `infigo-api-product-attributes-empty.md`, `infigo-template-edit-breaks-reorders.md`, `megaedit-editor-data-apis.md`, `infigo-hacks-repo-is-public.md`
- `ROADMAP.md` (public): Now / Next / Later
- `docs-library/01-official-infigo/api-order-line-attributes.md`: where customer-entered values live in the API

## Log
- 2026-10-01 12:50 CDT — Traced empty `ProductAttributes` on `orderlineitem/get` using Infigo's raw OpenAPI spec. Ruled out a wrong id against the report CSV; checkout attributes rejected (per-product codes, many departments). Infigo ticket sent; write-up added to docs-library.
- 2026-09-28 16:25 CDT — Multi-location business card: extracted location/main/fax Label-Value CSVs, full-diffed the live JSON against the R12 MEX (only 3 main-number changes), researched keeping location data outside the template (Custom Data Category + Editor script). Deferred; R13 built by hand.
- 2026-09-28 — QR business card: `vdp/` engine + build spec added; MEX built six times against live import tests until it passed (per-record navy QRs, text exact). Docs-library anatomy note and Invent FAQ updated with the verified MEX facts. Nothing pushed.
