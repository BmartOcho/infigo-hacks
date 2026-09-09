# Docs Library — File Format

Every harvested doc lives in a category folder as a single `.md` file. Filenames are kebab-case.

## Required front matter

```yaml
---
title: "Original title of the article/video/thread"
source: "infigo-academy | infigo-blog | printiq-docs | connectid-kb | youtube | reddit | partner-blog | other"
url: "https://..."
type: "article | video | forum-thread | pdf | api-ref | tutorial"
date: "YYYY-MM-DD or 'unknown'"
tags: [batch, pricing-script, megaedit, connectid, printiq, vdp, ...]
relevance: "high | medium | low"
---
```

## Body sections (in this order)

1. **Summary** — 2-4 sentences, what it covers and who it's for.
2. **Key takeaways** — bulleted list of load-bearing facts (numbers, property names, API signatures, gotchas).
3. **Code / config snippets** — only if the source contains paste-ready code or config worth preserving.
4. **Related** — `[[link-to-related-doc]]` pointers if there's an obvious sibling doc.

## Naming

`<short-slug>.md` — e.g. `batch-pricing-script-basics.md`, `connectid-kinds-handling.md`.

## Why this format

Optimized for grep/search. A future Claude can `grep -l "batch" docs-library/**/*.md` and instantly find every relevant doc without loading them all. Front matter tags make multi-axis filtering trivial.
