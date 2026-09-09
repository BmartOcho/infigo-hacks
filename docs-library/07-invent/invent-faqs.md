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

## Related
[[invent-variable-logic]]
[[invent-setup-tab]]
[[invent-export-package]]
[[megaedit-batch-csv-upload]]
`experiments/invent-scripts-slot-test/RESULTS.md` (probe results for the Variable Logic + CSV batch gap)
