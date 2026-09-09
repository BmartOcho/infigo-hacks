# Infigo Docs Library — Master Index

100 harvested docs organized by category. Per-folder `_INDEX.md` files have the full list; this file is the entry point with cross-cutting topic pointers and a "start here" shortlist.

See `_FORMAT.md` for the per-doc file format.

## Categories

| Folder | Docs | Scope |
|---|---|---|
| [`01-official-infigo/`](01-official-infigo/_INDEX.md) | 26 | academy.infigo.net, infigo.net, official blog/KB |
| [`02-printiq/`](02-printiq/_INDEX.md) | 21 | PrintIQ docs, GetPrice API, IQconnect, Connect: printIQ from the PrintIQ side |
| [`03-connectid/`](03-connectid/_INDEX.md) | 9 | Connect: printIQ plugin from the Infigo side — kinds handling, mappings, FAQ |
| [`04-megaedit/`](04-megaedit/_INDEX.md) | 7 | MegaEdit VDP editor — batch CSV, scripts config, Item.* properties |
| [`05-community/`](05-community/_INDEX.md) | 16 | PrintPlanet, Capterra, GitHub type defs, podcasts, YouTube |
| [`06-third-party/`](06-third-party/_INDEX.md) | 21 | Partner blogs, trade press, case studies, competitor comparisons |
| [`07-invent/`](07-invent/_INDEX.md) | 7 | Invent InDesign plugin — install, Setup tab, Variable Logic, exporting, FAQ |

## Start here — highest-relevance docs by topic

### Batch / cart multiplication (a recurring trap)
- `04-megaedit/megaedit-pricing-script-item-properties.md` — Item.IsBatch / NumberOfRecords / BatchTiers + the unit-price-only rule
- `04-megaedit/megaedit-batch-csv-upload.md` — two-switch requirement (CSV source + Standard Batch Script)
- `03-connectid/connectid-kinds-handling.md` — Kinds Handling / Records-per-Kind setting
- `03-connectid/connectid-preventing-duplicate-artwork.md` — Post Artwork Logic + QQADAKey plumbing
- `01-official-infigo/multipart-versioning-bg050.md` — Infigo-native equivalent of kinds/records flow

### Pricing scripts (Generic Pricing Script + custom)
- `01-official-infigo/generic-pricing-script-basics.md`
- `01-official-infigo/generic-pricing-script-tiered.md`
- `01-official-infigo/generic-pricing-script-multipart-csv.md`
- `01-official-infigo/generic-pricing-script-overview-toolbox.md`
- `01-official-infigo/pricing-script-interface-documentation.md`
- `01-official-infigo/pricing-script-examples.md`
- `05-community/github-infigo-pricing-script-types.md` — TypeScript defs + 4 paste-ready scripts

### ConnectID / PrintIQ integration
- `03-connectid/connectid-printiq-overview.md` — master reference
- `03-connectid/connectid-printiq-faq.md` — production gotchas
- `02-printiq/printiq-getprice-live-pricing.md` — GetPrice flow
- `02-printiq/connect-printiq-basic-setup.md` — credentials + plugin setup
- `02-printiq/connect-printiq-mapping-products.md` — SKU / attribute-combination mapping
- `02-printiq/connect-printiq-custom-quoting-config.md` — JSON config to escape SKU explosion
- `02-printiq/connect-printiq-other-config.md` — Order Submission (independent vs appended quote)
- `02-printiq/printiq-v49-release-notes.md` — GetPrice/AcceptQuote v49 extensions
- `01-official-infigo/infigo-release-notes-2026-08.md` — Aug 2026: MEX job-ticket templates, Fit-to-Box tracking, promo-code → PrintIQ, import Language/Currency, paged PDF media

### Invent (InDesign plugin → MEX → MegaEdit)
- `07-invent/invent-overview.md` — handoff model + category index
- `07-invent/invent-variable-logic.md` — conditional rules engine (Conditions + Actions, if/elseif/else). **Form-driven only — does NOT fire on CSV batch upload**
- `07-invent/invent-setup-tab.md` — Setup tab (5 sub-tabs); Scripts/Hardcoded Scripts fields are undocumented in Academy
- `07-invent/invent-faqs.md` — Master Pages static-only, rectangle frames only, batch+Invent integration gap acknowledged
- `07-invent/invent-export-package.md` — Export tab flow, validation gotchas
- `07-invent/invent-mex-export-troubleshoot.md` — OneDrive/Dropbox folders silently swallow exports
- `07-invent/invent-install.md` — Anastasiy / AEScripts Extension Manager flow

### MegaEdit editor + scripts
- `04-megaedit/megaedit-overview.md`
- `04-megaedit/megaedit-scripts-config.md`
- `04-megaedit/megaedit-sync-inputs-to-attributes.md`
- `01-official-infigo/megaedit-editor-interface.md`
- `01-official-infigo/megaedit-variables-applying.md`
- `01-official-infigo/prepopulate-data-script-megaedit.md`
- `04-megaedit/megascripts-types-documentation.md`
- `05-community/github-infigo-megaedit-types.md`

### Tier pricing / variant pricing / rounding
- `01-official-infigo/quantity-based-pricing.md`
- `01-official-infigo/enhanced-tier-pricing-attribute-grouping.md`
- `01-official-infigo/department-specific-pricing.md`
- `01-official-infigo/rounding-adjustment-on-pricing.md`
- `01-official-infigo/pricing-visibility-control.md`

### Real-world deployment context (case studies + reviews)
- `06-third-party/capterra-infigo-verified-reviews.md` — 17 admin reviews, named pain points
- `06-third-party/piworld-how-printers-win-with-w2p.md` — Talient case study + metrics
- `06-third-party/wtt-cober-print-on-demand-20pct-growth.md` — Cober deployment
- `06-third-party/aijourn-businesswire-infigo-2025-growth.md` — 2025 growth + LPi/Superior Packaging
- `05-community/printiq-aggregate-reviews.md` — PrintIQ review themes (back-end support weakness)

## Coverage gaps to revisit

Notes from the harvest agents on what couldn't be fetched cleanly:

- **Infigo Zendesk** (`infigosoftware.zendesk.com`) — JS-rendered SPA returns empty content via WebFetch. Academy.infigo.net covers most of the same ground.
- **Invent Scripts / Hardcoded Scripts fields** (Setup → Other in current plugin) — undocumented on Academy. 2023 Setup Tab article is stale. Behaviour must be confirmed empirically or via Infigo support.
- **GitHub Pages type-def sites** (`infigo-official.github.io`) — returned binary/garbled content. Use NPM install or open URLs in a browser.
- **PrintIQ Zoho desk** (`printiq.zohodesk.com`) — gated. GetPrice/AcceptQuote full request/response schemas not available publicly.
- **PrintPlanet anonymous fetches** — modern UI returns near-empty HTML. Worth re-scraping with a login.
- **Reddit** — zero Infigo/MegaEdit/PrintIQ hits across r/printing, r/Printers, r/printshop, r/PrintTech. Demographic lives elsewhere.
- **Trade press JS-shells** — printweek.com, whattheythink.com, printAction.com, labelsandlabeling.com — content reconstructed from search snippets only.
- **Infigo Academy** — MegaEdit Crash Course, MegaScripts category root, API Documentation category, Infigo Sync install guides all had fetch issues.

## Conventions

- Filenames: kebab-case
- Every file has front matter (see `_FORMAT.md`)
- Cross-references between docs use `[[other-doc-slug]]`
- Tags are lowercase, hyphenated, in a YAML array

## Workflow for grep

```bash
# Find every doc tagged with "batch"
grep -l "batch" docs-library/**/*.md

# Find every doc mentioning the cart multiplier
grep -lri "numberofrecords\|qty.*records\|cart.*multipl" docs-library/

# Get just the high-relevance docs across all categories
grep -l 'relevance: "high"\|relevance: high' docs-library/**/*.md
```
