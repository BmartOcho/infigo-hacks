# HANDOFF — infigo-hacks

**Updated:** 2026-09-28 16:25 CDT · **Branch:** `main` · **HEAD:** see `git log -1`
**State:** tree clean except pre-existing untracked `mexgen/MEXGEN-AGENT-PLAN.md` · **10 commits unpushed** · memory updated · repo is PUBLIC

## Next steps
1. **Location data outside the template — resume research.** First action: send Infigo
   support this question (a yes/no, not a custom-script request):
   > Can you enable/confirm access to Custom Data Categories on our storefront (the
   > `CustomDataCategory` API in types-for-megaedit), and confirm that adding a custom
   > Editor script to an existing MegaEdit product's Scripts tab does not affect reorders
   > of that product?
   Full context, the candidate design and blockers: memory `infigo-template-edit-breaks-reorders.md`
   + `megaedit-editor-data-apis.md`; public summary in `ROADMAP.md` "Next".
2. **Push, after the owner confirms.** Ten commits here and thirteen in the nested
   private `MexGen Agent/` repo are local only. Before pushing this one, consider
   renaming `qr-business-card-vdp-build-spec.md` (generic content, customer name in the
   filename; `README.md` and `ROADMAP.md` link it).
3. Docs-library write-ups queued in `ROADMAP.md` "Next": CSV image-swap album syntax
   and the Variable-Logic-in-batch ceiling (`experiments/invent-scripts-slot-test/RESULTS.md`).

## Open loops
- [ ] ROADMAP "Now" still carries the name-badge batch product ConnectID question from May 2026 (parent-pricing cart setting test vs routing-only). Confirm whether it was resolved on the storefront and close or update it. (carried 2x)
- [ ] Multi-location business card R13 is being built by hand (2026-09-28, new location added). Optional check once it's live: `python "Claude outputs/location-dropdowns/tools/diff_json_vs_mex.py" <R13 export.json> <R13.mex>` to confirm only the new location changed. Known data flags worth folding into a revision are listed in memory `infigo-template-edit-breaks-reorders.md`.
- [ ] QR business card edges (from ROADMAP "Now"): required flags on TEXT, blank cell-number rendering, whether the bound `vCard` variable must stay in the form; spot-UV element list still needed before `--spot-uv` runs.

## Gotchas
- Public repo. Before every commit: grep the staged diff for personal names, shop name, client names, storefront URLs, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory file `infigo-hacks-repo-is-public.md` has the full list and the established generic aliases (Field / Regional, "locations").
- `Claude outputs/location-dropdowns/` (CSVs + diff tools) holds real customer location data — it's ignored; keep it that way.
- The `types-for-megaedit` GitHub Pages site renders garbled; read the `.d.ts` files from jsDelivr instead (URLs in memory `megaedit-editor-data-apis.md`).
- `*.pdf` and `*.mex` are blanket-ignored. A reference PDF needs a `.gitignore` negation or, better, conversion to markdown.
- Commit author must be the GitHub noreply address (already set in this repo's git config).
- Session prompts (`NEXT.md`, `STARTER-PROMPT.md`, `MEX-GENERATOR-STARTER-PROMPT.md`), `Claude outputs/`, `Customer-CSV-Additions/`, and `mexgen/dump-*/` exist locally but are ignored. Don't un-ignore them.

## Pointers
- Memory: `infigo-template-edit-breaks-reorders.md`, `megaedit-editor-data-apis.md`, `infigo-hacks-repo-is-public.md`, `infigo-hacks-repo-gitignore.md`
- `ROADMAP.md` (public) — Now / Next / Later
- `docs-library/INDEX.md` — library entry point; `_FORMAT.md` — per-doc format

## Log
- 2026-09-28 16:25 CDT — Multi-location business card: extracted location/main/fax Label-Value CSVs, full-diffed the live JSON against the R12 MEX (only 3 main-number changes), researched keeping location data outside the template (Custom Data Category + Editor script). Deferred; R13 built by hand.
- 2026-09-28 — QR business card: `vdp/` engine + build spec added; MEX built six times against live import tests until it passed (per-record navy QRs, text exact). Docs-library anatomy note and Invent FAQ updated with the verified MEX facts. Nothing pushed.
- 2026-09-09 11:30 — Repo created private, cleansed of all personal/shop/client identifiers, history squashed to one commit, flipped PUBLIC, business-card example genericized to Field/Regional.
