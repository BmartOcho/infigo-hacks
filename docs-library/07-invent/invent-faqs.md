---
title: "Invent FAQs"
source: "infigo-academy"
url: "https://academy.infigo.net/academy/p/1792/invent-faqs"
type: "article"
date: "2023-08-09"
tags: [invent, faq, limitations, master-pages, batch-gap, log-files, supported-versions, frame-types, fonts]
relevance: "high"
---

## Summary
Catch-all FAQ that surfaces several non-obvious Invent limitations. Most load-bearing: Invent supports **rectangle frames only** (no ellipse/polygon), does **not** include **Adobe Cloud Fonts** in exports, supports only a **uniform line height** per text frame, and the comment thread confirms **Invent + Batch CSV is a known integration gap** that Infigo has acknowledged but not shipped a fix for as of Aug 2023.

## Key takeaways

### Frame / typography limits
- **Master Pages** support static content only. Variable fields placed on Master Pages are **ignored**.
- **Rectangle frames only** — no ellipse, no polygon frames.
- **Single uniform line height per Text Frame** (line-height-to-text-height ratio must be consistent within a frame; works the same as MegaEdit's percentage model).
- **Adobe Cloud Fonts not supported** in export packages.

### Versioning / install
- Supported InDesign: latest version actively (16+ as of doc).
- Version check: Invent panel → burger menu → About.
- Update flow: download new plugin → open Anastasiy → highlight InDesign → Install → pick new plugin file → done.

### Log file locations
- **Windows**: `C:\Users\<user>\AppData\Roaming\InfigoInvent`
- **Mac**: `~/Library/Preferences/InfigoInvent`
- Files: `infigo-combined.log`, `infigo-error.log`
- Also linkable from the About popup.

### Edit-after-import (load-bearing)
- You CAN create a product in Invent then make further changes in MegaEdit directly.
- **BUT** uploading a new MEX overwrites those direct-MegaEdit changes. Invent is the source of truth for everything it owns.

### Invent vs Infigo Designer
- Invent is the strategic direction. Infigo Designer not yet retired but feature parity is the eventual goal.

### Invent + Batch (the gap)
- FAQ body: "Batch, which is coming, but you could use Invent to create your product and then from admin enable and configure batch directly."
- Comment from Rob Whitney (Aug 2023): set Batch Source = CSVPlugin on the Invent-created product but no batch upload appeared in the live product area.
- **Status as of May 2026**: still no native Invent + Batch path. Variable Logic does not fire on CSV batch upload (see [[invent-variable-logic]] and `experiments/invent-scripts-slot-test/RESULTS.md` (probe results for the Variable Logic + CSV batch gap)).
- **Resolved by plugin 2.8.x (verified Sep 2026 by diffing exports):** a 2.8.1 Invent export of a batch-enabled product carries the batch setting *inside the MEX* — three switches that move together: XML `<Config><Product><BatchSource>csv</BatchSource>`, JSON `config.batch.mode = "Batch"` (plus `batchSource: {csv: true, excel: true}`), and `batchSource: true` on every variable that maps to a CSV column. A 2.6.7 export of a single-record product has none of the three. So the Aug-2023 "set Batch Source in admin and nothing appears" symptom is the pre-2.8 plugin not writing these; on 2.8.x, export from Invent with batch on (or set the three in the MEX — `mexgen build` does this from one `batch: true` key and refuses a file where they disagree). Full key list in [[mex-file-format-anatomy]]. The Variable Logic gap is separate and still stands: derive any conditional text as CSV columns before upload.

## Related
[[invent-variable-logic]]
[[invent-setup-tab]]
[[invent-export-package]]
[[megaedit-batch-csv-upload]]
`experiments/invent-scripts-slot-test/RESULTS.md` (probe results for the Variable Logic + CSV batch gap)
