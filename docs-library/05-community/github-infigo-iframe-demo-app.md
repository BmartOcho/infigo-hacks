---
title: "Infigo-Official/iframe-demo-app (Vue.js + backend reference integration)"
source: "github"
url: "https://github.com/Infigo-Official/iframe-demo-app"
type: "code-repo"
date: "2026-02-16"
author: "Infigo-Official"
tags: [iframe, api, integration, vue, javascript, communicator-library, embed]
relevance: "medium"
---

## Summary
Reference implementation showing how to embed Infigo's editor inside a third-party (merchant) site via an iframe and the Infigo API. Includes a Vue.js front-end, a Node proxy/webhook collector backend, a Dockerfile, and a `resources/` sample script for setting inventory variables and product attributes. Live demo at https://demo-iframe-api.private.infigosoftware.rocks/.

## Key takeaways
- Requires Node.js v14+.
- Flow: (1) authenticate as an Infigo customer, (2) gather product details to pick editor/product, (3) API call requests a one-time editor URL, (4) embed that URL in your iframe — clicking logs the user in and loads the editor.
- **JavaScript Communicator Library** is the key piece on the host page — it lets you capture editor events like `Add to Basket` and `Save as Project` from inside the iframe.
- After editing, you call the API to place an order or create an output.
- Vue 63%, TypeScript 27%, JS 6% — easy to read as a reference.
- Public wiki: `wiki-iframe.private.infigosoftware.rocks` (likely behind customer auth, but referenced in the README).

## Related
[[github-infigo-megaedit-types]]
