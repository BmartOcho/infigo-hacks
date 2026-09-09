---
title: "Enabling and utilising barcodes in MegaEdit | ME_029"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1049/enabling-and-utilising-barcodes-in-megaedit-me_029"
type: "tutorial"
date: "2024-01-25"
tags: [megaedit, barcode, qr-code, data-matrix, gs1, fields, script]
relevance: "medium"
---

## Summary
The `Barcode Field` script must be enabled per-product on the Scripts tab. Once enabled, end users see a Barcode field in the Fields panel. Double-click a barcode field to configure type, value, auto-scale, human-readable display, font size, and color.

## Key takeaways
- Script name: `Barcode Field` (under Scripts tab of MegaEdit product).
- If not visible in the scripts list, contact Customer Support to enable.
- Two config scopes (same as any MegaEdit script): per-product Config button OR global Config — the global config link is also exposed from the per-product config screen.
- Extended barcode types (e.g. GS1 128, GS1 DataBar extended, GS1 DataBar extended stacked) are enabled via additional config.
- Barcode field config options:
  - **Type** (dropdown): STD-25, INT-25, QR Code, Data Matrix, plus extended types
  - **Value** = what's encoded into the barcode
  - **Encoding Mode** (Data Matrix only): BASE256 / ASCII / C40 / TEXT / X12
  - **Auto Scale** = fit barcode to field
  - **Show Human Readable** = render value as text below barcode
  - **Margin Human Readable** = pixel padding between barcode and text
  - **Font Size** for the human-readable text
  - **Barcode colour** picker
- Injecting external Infigo data into a barcode at output/edit time = chargeable custom MegaScript development. Default behavior only encodes the field's static Value.

## Related
[[megaedit-scripts-config]]
[[megaedit-batch-csv-upload]]
[[megascripts-types-documentation]]
