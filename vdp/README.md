# vdp — variable-data PDF engine

Drives a designer's static placement PDF with a CSV and writes print-ready
output: one PDF per record, a merged front/back file, and (optionally) a
matching spot-colour mask. The layout is a JSON file whose field values use
the same `[#Column#]` tokens MegaEdit uses, so one layout describes both the
PDF build and the MegaEdit template for the same product.

The first product built this way is a two-sided QR business card; its
layout is `customers/qr-business-card.json`, with the art, fonts and data in a
gitignored folder that the layout points at via `base_dir`.

## Usage

```sh
py -m pip install -r requirements.txt        # pymupdf, qrcode, opencv-python-headless

py vdp.py check  <layout.json> [<data.csv>]      # layout + data sanity, writes nothing
py vdp.py build  <layout.json> <data.csv> [--out DIR] [--spot-uv] [--no-verify]
py vdp.py backgrounds <layout.json> [--out DIR]  # redacted pages for a MegaEdit product
py prep_csv.py   <layout.json> <raw.csv> [--out FILE]   # MegaEdit batch CSV
```

On Windows use `py`; the shebang resolves to the launcher's default Python,
so install the requirements for that interpreter (`py -m pip …`).

`build` exits 1 and reports every problem when a QR fails to decode, a title
needs more lines than allowed, a required cell is blank, a font is not
embedded, a trim box drifts, or a static page changes. Nothing is
half-written: a failing record stops the run before the merged file exists.

## What `build` does per record

1. Opens the template and, on each variable page, redacts every text block
   (the designer's placeholder copy) and paints the configured knock-out
   rectangles white.
2. Embeds the layout's fonts and sets each field at its baseline. Fields
   are `value` (one string, optionally word-wrapped to `wrap_width` with a
   `max_lines` ceiling) or `lines` (a list with one baseline per line, and
   `align_v: bottom` to let a shorter stack sit on the lowest baselines).
3. Draws the QR: white field over the knock-out and QR box, then the dark
   modules edge to edge in the module colour. Content is the `vcard` line
   list, tokens resolved, blank-token lines omitted.
4. Saves the single, appends it to the merged file, and verifies it: the QR
   is rendered at `qc.decode_dpi` and decoded with OpenCV, and the decoded
   text must equal the encoded text exactly; trim boxes are compared to
   `page.trim`; declared fonts must be embedded; `static_pages` must be
   byte-identical to the template.

## Token rules

- `[#Column#]` — the cell value, stripped. Every token in the layout must
  name a column in `csv.headers`; `check` refuses otherwise.
- `[?…?]` — an optional group. Dropped when every token inside it is blank,
  otherwise expanded in place. `[#Address#][?, [#Address2#]?],` gives
  `1 Example Street, Suite 100,` or `1 Example Street,`.
- **Blank-line suppression** — a `lines` entry, a `vcard` line, or a whole
  `value` whose tokens all resolve blank is not drawn at all. With
  `align_v: bottom` the surviving lines take the lowest baselines, which is
  how a single phone number sits directly above the email line.
- `transforms` — `{"Cell Number": "phone_dots"}` rewrites a column before
  anything reads it: any 10-digit number becomes `123.456.7890`; anything
  else is kept as typed.

## Layout JSON

| Key | Meaning |
|---|---|
| `base_dir` | Folder every other path is relative to (relative to the layout file). Default `.` |
| `page` | `{width, height, bleed, trim: [x0, y0, x1, y1]}` in points; the bleed page is the PDF page |
| `template.file` | The placement PDF. `variable_pages` get text and a QR; `static_pages` are verified untouched |
| `template.redact_text_pages` | Pages whose text blocks are removed before drawing |
| `template.knockouts` | `{"<page>": [[x0, y0, x1, y1], …]}` rectangles painted white (build) or stripped of vector art (backgrounds) |
| `fonts` | `{key: {file, declared_name}}`. `declared_name` is the MegaEdit "Family - Style" string, recorded here so the two builds stay in step |
| `colors` | `{key: {hex, cmyk}}` or `{key: "#rrggbb"}`. The PDF build uses `hex`; `cmyk` is for the MegaEdit template |
| `defaults` | `{page, x, font, size, color, leading}` applied to any field that omits them |
| `fields[]` | `{name, value | lines, baseline | baselines, font, size, color, x, wrap_width, max_lines, align_v, leading, page}` |
| `qr` | `{page, box, module_color, error_correction, quiet_zone_modules, vcard[], omit_line_if_blank, line_ending}` |
| `csv` | `{headers[], required[], skip_row_if_blank}`. `headers` is the contract with the customer's file |
| `megaedit.derived_columns` | `{"Column": "template"}` appended by `prep_csv.py`; blank when all tokens blank |
| `output` | `{single, merged, spot_uv_suffix}`; `single` may carry tokens |
| `qc` | `{decode_dpi, duplicate_warn: [[a, b], …]}` |
| `spot_uv` | `{spot_name, elements: [{type: qr} | {type: field, name} | {type: rect, rect, page}]}` |

## `--spot-uv`

Emits `<single>_SpotUV.pdf` beside each record and a merged mask: same page
count and boxes as the print file, every configured element at 100% of the
named Separation colour, everything else empty. Elements are drawn in a
sentinel colour and the content stream is rewritten to the spot; the build
refuses if any other colour operator survives, so the mask cannot silently
carry a process-colour object. The element list is per layout; a layout
whose `elements` is empty fails `--spot-uv` with its `status` note.

MegaEdit cannot produce this file, so for a storefront product the mask is
a post-order step: run `build --spot-uv` against the order's CSV.

## `backgrounds`

Writes one PDF per template page with placeholder text removed and any
vector art fully inside a knock-out rectangle removed, trim boxes intact.
These are the page backgrounds for the MegaEdit product built from the
same layout. Static pages are copied unchanged.

## `prep_csv.py`

MegaEdit's Variable Logic does not fire in CSV batch, so a label that must
disappear with its value (`C ` before a blank cell number) has to travel in
the data. `prep_csv.py` keeps every raw column as-is — the upload still maps
1:1 onto the template's variables — applies the transforms, and appends the
`derived_columns`. Output is UTF-8 with BOM, `<raw>-megaedit.csv` by default.
