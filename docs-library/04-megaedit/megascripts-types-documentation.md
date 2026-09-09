---
title: "Infigo MegaScripts Documentation (official type defs)"
source: "infigo-academy"
url: "https://academy.infigo.net/c/266"
type: "api-ref"
date: "unknown"
tags: [megaedit, megascripts, api-reference, typescript, types, intellisense, custom-scripts]
relevance: "high"
---

## Summary
Infigo Academy redirect page for the official **MegaScripts** type definitions. Points to https://infigo-official.github.io/types-for-megascript/ as the authoritative interface documentation for writing custom MegaEdit scripts. Mirrors the pattern of the pricing-script types package — separate package for the in-editor MegaEdit scripting API.

## Key takeaways
- Official MegaScripts reference: https://infigo-official.github.io/types-for-megascript/
- NPM package: `@infigo-official/types-for-megascript` for TS/JS IntelliSense.
- Distinct from pricing scripts (which are JSON config + a runtime returning a price). MegaScripts run inside the MegaEdit editor and can manipulate fields, output, batch upload behavior, etc.
- Custom MegaScripts can be enabled per-product on the Scripts tab. Hardcoded Infigo MegaScripts may require Customer Support to enable on your account/storefront.
- WebFetch did not return readable content for the GitHub Pages docs site directly — open in browser or install package for full type reference.

## Code / config snippets
```
npm install --save-dev @infigo-official/types-for-megascript
```

## Related
[[megaedit-scripts-config]]
[[megaedit-batch-csv-upload]]
[[megaedit-barcodes]]
[[megaedit-sync-inputs-to-attributes]]
[[pricing-script-interface-docs]]
