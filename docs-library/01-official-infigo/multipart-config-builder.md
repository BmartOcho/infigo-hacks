---
title: "Infigo MultiPart Product Config Builder"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2203/infigo-multipart-product-config-builder"
type: "tutorial"
date: "unknown"
tags: [multipart, xml, config, preview, parts, brochure, label, 3d-preview, flipbook]
relevance: "high"
---

## Summary
Reference + visual builder tool for MultiPart product XML configuration. MultiPart products go far beyond "upload one PDF" — XML config controls preview mode, editor flow, page numbering, multi-language strings, advanced 3D / flipbook previews, and the "Parts" structure (e.g. front cover + interior + back cover for a brochure).

## Key takeaways
- MultiPart configuration is XML-based. The Config Builder generates the XML for you.
- **Four config sections:**
  - **Global Settings** — apply to all Parts (preview mode, editor mode, page numbers).
  - **Localization Settings** — translate Part names/descriptions per language.
  - **Advanced Settings** — 3D preview (licensed), flipbook view.
  - **Parts Config** — define upload areas (e.g. cover, content pages, back cover).
- Key Global Settings:
  - **Preview Mode Type:** `none`, `normal` (default), `minimumdummypages`, `mixrealanddummypages`
  - **Editor Mode:** `required` (default), `optional`, `bypasseditor`
  - **Preview Mode:** `booklet` (spreads) vs `single` pages
  - **Confirm Preview:** force user confirmation before checkout
  - **Add Page Numbers** + **Page Numbers At Content Pages Only** for fine-grain pagination
- Languages supported in localization: en-US, de-DE, es-ES, fr-FR, bg-BG, cs-CZ, nl-NL, he-IL, it-IT, pl-PL, pt-PT, pt-BR, cy-GB.
- Advanced Preview types: `standard`, `flip`, `3d`. 3D requires significant additional setup (not covered by this tool).
- XML output is split between `<PartConfiguration>` (print/page settings per part) + `<InputItem>` (upload areas) + an `<Output>` node controlling ordering of Parts.
- TOOL IS BETA — author must test thoroughly before publishing.

### Sample test PDFs (hosted by Infigo)
- Brochure Front Cover, Content Pages, Back Cover
- Brochure Prefix / Postfix examples
- Label samples (Navy / Yellow / Coral)

### MultiPart resources
- Product Examples: https://training.infigosoftware.com/productbuildworkshops/c/433/multipart-product-examples
- Webinar content: https://academy.infigo.net/p/2204

## Related
[[multipart-versioning-bg050]]
