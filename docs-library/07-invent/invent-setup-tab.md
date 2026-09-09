---
title: "Invent Setup Tab"
source: "infigo-academy"
url: "https://academy.infigo.net/academy/p/1712/invent-setup-tab"
type: "tutorial"
date: "2023-05-17"
tags: [invent, setup, megaedit-settings, editor-config, scripts, hardcoded-scripts, export-type, doc-stale]
relevance: "high"
---

## Summary
The Setup tab in the Invent plugin (v2.0+) lets you manage MegaEdit product settings from inside InDesign instead of after-the-fact in MegaEdit or the Infigo admin. Five sub-tabs: **Editor, Field, Image, Visual, Other**. Settings are baked into the exported MEX and applied automatically when imported into MegaEdit.

**⚠️ Doc is stale.** The 2023 article documents only the five sub-tabs and a few settings under Other (Show Clear Page, Profanity, Drawing Tools, Snap, Export Type). Current plugin (May 2026) Setup → Other also exposes **Scripts**, **Hardcoded Scripts**, **Variable set scope**, **Display margin mode**, **Page type**, **Export layers as single frames** — none of which appear in the Academy article. These newer fields are undocumented; behaviour must be confirmed empirically or via Infigo support.

## Key takeaways

### Editor sub-tab
- **Allow Add to basket** — checkbox; default on. Disable to remove the Add-to-Basket button.
- **Preview** — Standard Preview or No Preview.
- **Use direct preview mode** — when on, editor shows only the preview; all editing happens via the form.
- **Download Features** — allow PDF / Image / Both as direct downloads from MegaEdit. Watermark text + print-restriction options.

### Field sub-tab
- **Allow adding text fields** — toggles the "Add Text" button in MegaEdit.
- **Allow adding image fields** — same for image fields.

### Image sub-tab
- **Minimum Image Resolution** — low-res warning threshold.
- **Show Image Upload Area** — gallery tab visibility. Default: false.
- **Enable Direct Image Upload** — click image field → open file picker. Product-level toggle.
- **Ask for default album** — prompt customer to set default album on first upload. Default: false.

### Visual sub-tab
- **Show Bleed Lines** — default on.
- **Show Ruler** — default off.
- **Background Options** — Neutral Checker Pattern (default), Pattern, Solid Colour (+ colour picker).

### Other sub-tab (documented portion)
- **Show Option to Clear Page** — default off.
- **Profanity** — Check Profanity on/off; Mask Censored Words on/off.
- **Show Drawing Tools** — default off.
- **Snap Options** — Item / Grid / Off + sensitivity slider. Default: Item.
- **Export Type** — `Standard` (default; full export, fully interactive MegaEdit product) or `Bootstrap` (only exports fields).

### Other sub-tab (undocumented as of May 2026)
- **Display margin mode** — `Entire` or `Half`.
- **Export layers as single frames** — checkbox.
- **Variable set scope** — dropdown (e.g., `Shopping Session`).
- **Scripts** — text input "Press Enter to link new script". Likely attaches a custom MegaScript to the MEX so it auto-attaches on import. **Behaviour unconfirmed.**
- **Hardcoded Scripts** — text input "Press Enter to link new hardcoded script". Likely references Infigo-built MegaScripts (which normally require Customer Support permission to enable). **Behaviour unconfirmed.**
- **Page type** — `Single` (and presumably multi-page options).

## Related
[[invent-variable-logic]]
[[invent-export-package]]
[[megaedit-scripts-config]]
[[megascripts-types-documentation]]
