---
title: "Per-record image swap in a batch CSV (AlbumName/ImageName.ext)"
source: "hack-note"
type: "pattern"
date: "2026-05-27"
tags: [megaedit, batch, csv, image-swap, album, background-swap, variable-logic-workaround]
relevance: "high"
---

## Summary
A MegaEdit batch (CSV) upload can swap an **image** per record. Bind an image field to a CSV column, and in each cell put the image's location as **`AlbumName/ImageName.ext`**: the media album name, a slash, then the image file name **with its extension**. Each record renders with its own image. Found empirically on 2026-05-27.

**Infigo's documentation says to leave the file extension off. In testing that was wrong: the swap only worked with the extension included.**

## Why it matters
Invent Variable Logic does not run during a CSV batch (see `07-invent/variable-logic-batch-ceiling.md`). So the obvious way to make a per-record background — "if the field is X, show background B" — fails in batch. This syntax covers the **image-swap part** of that gap without any logic: make the background a **full-bleed image field** and name the right image in each CSV row.

## Pattern
1. Upload the alternative images (backgrounds, logos, signatures) to a media album that is visible to the product's customers. Album scope and sharing behaviour: `07-invent/invent-image-variable-clipart-set-resolution.md`.
2. In the template, make the art an **image field** (full-bleed for a background), not a static background and not something toggled by a Variable Logic rule.
3. Map that field to a CSV column during the batch upload.
4. In each row, write `AlbumName/ImageName.ext`, for example `Backgrounds/Version-B.pdf`.

## Limits
- This covers **image** swaps only. Showing or hiding several **text** fields per record still needs the split-CSV + two-template workaround (ROADMAP "Next").
- Names are matched as plain text. Keep album and file names free of characters that CSV tools mangle; smart quotes and non-UTF-8 encodings cause trouble here too (`csv-apostrophe-encoding-mac-roman.md`).
- Not yet tested: names with spaces, case sensitivity, and images in nested albums.

## Related
- `megaedit-batch-csv-upload.md`: batch setup (Batch source = CSVPlugin + Standard Batch Script)
- `07-invent/variable-logic-batch-ceiling.md`: why Variable Logic can't do this in batch
- `07-invent/mex-file-format-anatomy.md`: name-based referencing is a CSV feature, not stored in the MEX
