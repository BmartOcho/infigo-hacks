---
title: "How to Apply your MegaEdit Variables and Seeing Them in Action"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2662/how-to-apply-your-megaedit-variables-and-seeing-them-in-action"
type: "tutorial"
date: "unknown"
tags: [megaedit, variables, fields, image, text, interlinked-session, thumbnail, cross-product]
relevance: "high"
---

## Summary
Walks through assigning a MegaEdit Variable Set to multiple MegaEdit products so fields (text + image) stay synchronized across them. Once linked, edits made in one product (image upload, styled text) auto-propagate to other products AND to product thumbnails. Interlinked session context: products already in basket retain old values; new products adopt new values.

## Key takeaways
- Variable Sets are created separately (covered in companion video), then ATTACHED to MegaEdit products under **MegaEdit configuration > Variables tab > assign set + Save**.
- Same Variable Set on multiple products = those products share field values.
- Login as admin to access the **Advanced Details tab** of editor fields (Image / Text).
- In Advanced Details, set the **variable items** dropdown to the relevant variable. Dropdown is filtered by field type (image fields only see image variables, etc.).
- **CRITICAL: For styled text, apply styling BEFORE saving the product as default** — otherwise styling does NOT carry into the thumbnail.
- Both products must be saved as Product Default for variable linking + thumbnail propagation to work.
- **Interlinked session context behavior:**
  - Products already added to basket KEEP their saved values.
  - New product instances ADOPT the latest variable values.
  - Going back to a basket item does not re-pull current variable values — they're frozen at the time of add-to-basket.
- Use case: brand portals where a logo + tagline must stay consistent across business cards, letterheads, and signage — change once, propagate everywhere.

## Related
[[prepopulate-data-script-megaedit]]
