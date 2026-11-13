# Background Logo Drops Out in Acrobat but Shows in the Browser (Unbalanced Form XObject)

**Tags:** megaedit, mex, mexgen, background-pdf, logo, acrobat, pdfium, content-stream, q-Q, BDC-EMC, optional-content, illustrator

## Problem
The site PDF downloaded from a MegaEdit product (a business card, 2026-10-16) showed the back side with its rich-black flood and tagline but **no logo**. The same PDF looks correct in Chrome, in the MegaEdit editor and in every pdfium-based render check, so an earlier proof had been signed off as "back unchanged".

## Root cause
The logo is a Form XObject inside the background PDF the build script made, and its content stream was **unbalanced**: a `Q` and an `EMC` with no matching `q` / `BDC` before them.

The build script (its `band_split` step) sliced the Illustrator `.ai` content stream at the K100 band to separate the light (front) and dark (back) logos. Illustrator wraps the artboard in `/OC /MC0 BDC  q … Q EMC Q`, so a positional slice leaves:
- **front half:** an open `q` and an open `BDC` (viewers usually close these implicitly and draw it);
- **back half:** the closing `Q EMC Q` with no openers (q-depth and marked-content depth go to −1).

pdfium (Chrome, MegaEdit's preview, our Python checks) silently recovers. **Acrobat drops the whole unbalanced form**, so the logo vanishes while everything around it draws. MegaEdit does not touch the background: the logo form bytes in the site PDF were byte-identical to our build.

## Fix
Rebalance each half after slicing: append the missing closers to a half that leaves things open, and put the missing openers (`q`, or the source's own `/OC /MC0 BDC`) in front of a half that closes things it never opened. Rebuilt as v-03. It renders identically in pdfium; after re-uploading it, the author confirmed the back logo shows in Acrobat on a fresh site PDF (2026-10-16). `mexgen validate` now catches this shape (rule `PDF_CONTENT_UNBALANCED`).

Check any form you build by slicing a stream (this is the diagnostic that found it):

## Sample
```python
q = m = 0; qmin = mmin = 0
for _, op in pikepdf.parse_content_stream(form):
    o = str(op)
    q += (o == "q") - (o == "Q"); m += (o in ("BDC", "BMC")) - (o == "EMC")
    qmin, mmin = min(qmin, q), min(mmin, m)
# healthy: q end=0 min=0 | mc end=0 min=0
# v-02 back logo: q end=-1 min=-1 | mc end=-1 min=-1  -> dropped in Acrobat
```

## Caveats
- **pdfium-only QA cannot catch this.** If a background looks right in the browser but someone reports it missing, open it in Acrobat before anything else.
- Any `.mex` built from a sliced `.ai`/PDF stream carries this risk. This is the second bug from the same slice: v-02 also had to re-add the `cs` colour-space op, because the dark half lost it and its CMYK fills drew as DeviceGray.
- Products already uploaded with the bad background (v-02) keep producing the broken PDF until the `.mex` is replaced on the site.

