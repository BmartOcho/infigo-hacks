---
title: "Connect: printIQ Custom Quoting Configuration | CI_printIQ_011b"
source: "printiq-kb"
url: "https://academy.infigo.net/p/1348/connect-printiq-custom-quoting-ci_printiq_011b"
type: "tutorial"
date: "2024-01-29"
tags: [custom-quoting, getprice, json, sections, job-operations, attributes, inheritance, sku-explosion, advanced]
relevance: "high"
---

## Summary
The deep-dive on Infigo's Connect:PrintIQ Custom Quoting — including the three product-type modes (PrintOnDemand, Stock, Custom), the underlying GetPrice JSON, and the four-level inheritance hierarchy that lets attribute values override base product specs. Includes critical detail that a raw "additional GetPrice configuration JSON" field exists on every Connect Link popup for shops that need to hand-author the request. Tutorial video: https://www.youtube.com/embed/2JNqelV5kws

## Key takeaways
- **Product Type dropdown — three modes on the Connect Link popup:**
  - **PrintOnDemand** — classic mode. Single ExternalID → printIQ SKU. Used when there's a 1:1 mapping.
  - **Stock** — populated dropdown of available stock products from the PrintIQ instance. Pulls live data from PrintIQ. Includes an "Available stock product info" panel showing all current stock items.
  - **Custom** — activates the structured UI for Custom Quoting (replaces hand-authoring JSON).
- **Custom Quoting kills SKU explosion.** Before: 5 sizes × 2 stocks × 2 finishes = 20 SKUs in PrintIQ. After: 1 base spec + attribute overrides.
- **Custom mode UI fields (each maps to a PrintIQ concept):**
  - **Product Category** — PrintIQ category (NOT Infigo category) drives which Sections / Section Operations / Job Operations the UI pulls.
  - **Sections** — repeatable. Each Section has: Stock, pages, finish size, plus more. PrintIQ-native term.
  - **Section Operations** — nested under each Section. PrintIQ-native term.
  - **Finished Size** — either custom width/depth or pick from PrintIQ's pre-defined size list.
  - **Job Operations** — repeatable. PrintIQ-native term.
- **Raw JSON escape hatch:** Every Connect Link popup includes an **"Additional GetPrice configuration JSON"** field where you can hand-author the GetPrice request. This was the original Custom Quoting path before the UI shipped. Confirms the underlying API is JSON-based.
- **Four-level inheritance hierarchy** (highest priority first; lower levels inherit from higher unless overridden):
  1. Product Variant settings (base config — this is where you start)
  2. Product Variant Attribute Combinations
  3. Product Variant Attributes
  4. Product Attribute Value (lowest priority)
- Within the same entity, **higher Display Order overrides lower Display Order.**
- Fields default to `Inherited` — explicitly set a value at a lower level to override.
- Save button is **"Save External Reference"** in the popup.

## Code / config snippets

The Connect Link popup exposes a `GetPrice configuration JSON` field directly visible to admins — this is the wire format that PrintIQ's quoting endpoint consumes. The structured UI is literally a JSON builder. Fields the UI manipulates include `ProductCategory`, `Sections[]` (each with stock, pages, finish size, plus `SectionOperations[]`), and `JobOperations[]`.

## Related
[[connect-printiq-custom-quoting]]
[[printiq-getprice-live-pricing]]
[[connect-printiq-mapping-products]]
[[iqconnect-api-overview]]
