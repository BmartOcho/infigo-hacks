# Infigo Hacks

A working reference library for the [Infigo](https://www.infigo.net/) web-to-print platform and the systems around it: MegaEdit, Invent, ConnectID, and printIQ. It collects harvested documentation, empirically verified workarounds, build specs, and small tools for problems that Infigo's own docs don't cover.

The goal is a living problem-solver for people running Infigo storefronts. Every hack here was verified against a real storefront and cart, not just read off a docs page.

## Start here

| If you want to... | Go to |
|---|---|
| Find official or community docs on a topic | [`docs-library/INDEX.md`](docs-library/INDEX.md) |
| See what's being worked on and what's been ruled out | [`ROADMAP.md`](ROADMAP.md) |
| Generate a cart-safe pricing script | [`pricing-generator.html`](pricing-generator.html) (open in a browser) |
| Build a `.mex` file from a JSON config | [`mexgen/README.md`](mexgen/README.md) |
| Read the Invent-in-batch investigation | [`experiments/invent-scripts-slot-test/RESULTS.md`](experiments/invent-scripts-slot-test/RESULTS.md) |

## Layout

```
docs-library/       Harvested docs, one markdown file per source, organized by origin
  01-official-infigo/   academy.infigo.net, infigo.net, official KB
  02-printiq/           printIQ docs, GetPrice API, IQconnect
  03-connectid/         ConnectID / printIQ integration
  04-megaedit/          MegaEdit editor and scripting
  05-community/         Forums, GitHub type defs, podcasts
  06-third-party/       Press, reviews, partner announcements
  07-invent/            InDesign plugin, MEX format, Variable Logic
experiments/        Probe scripts and results for open questions
mexgen/             Config-driven MEX generator (Python, stdlib only)
*.md (root)         Build specs and setup guides for specific product patterns
pricing-generator.html   Standalone pricing script generator
```

Each doc in `docs-library/` follows the format in [`docs-library/_FORMAT.md`](docs-library/_FORMAT.md). Per-folder `_INDEX.md` files list every doc with a one-line summary.

## Operating principles

- Verify behavior empirically against the actual cart and storefront. Infigo docs are thin and sometimes wrong.
- Search `docs-library/` before searching the web.
- Bypass printIQ live pricing for batch products. Use custom Infigo pricing scripts instead.
- Build reusable generators, not one-off fixes.
- Don't open support tickets for things Infigo would quote a custom script for. The cost-benefit rarely works at small project scale.

## What's not in this repo

This repo is public. `.mex` exports, PDF artwork, customer import CSVs, and full template dumps from `mexgen.py inspect` are intentionally excluded. They are local test artifacts or contain customer data. Client and product names in the specs and examples have been genericized. If an official PDF ever belongs here as reference, convert it to markdown in `docs-library/` to match the rest of the library.

## Contributing

Found a workaround that isn't documented? Add a markdown file to the relevant `docs-library/` folder following `_FORMAT.md`, update that folder's `_INDEX.md`, and note where and how it was verified. Don't include customer names, storefront URLs, credentials, or real user data in examples.
