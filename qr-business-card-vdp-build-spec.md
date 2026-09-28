# QR Business Card — CSV Batch Build Spec

_Infigo storefront · MegaEdit + the `vdp/` PDF engine · drafted 2026-09-28_

Customer: a firm ordering two-sided business cards for its staff, either as a
CSV batch (one upload, one card per row) or one at a time in the editor. Each
card carries a vCard QR code so the contact can be saved with one scan. The
approved artwork was first produced as a static PDF run driven by a CSV; this
spec makes that run repeatable and delivers the same product as a
self-service MegaEdit template.

Companion spec for the two-product pattern: `businesscard-two-product-build-spec.md`.

---

## 1. Architecture at a glance

| Part | Where | Job |
|---|---|---|
| Layout JSON | `vdp/customers/<customer>.json` | Single source of truth: page geometry, fonts, colours, field baselines, vCard template, CSV header contract. Field values use `[#Column#]` tokens |
| PDF engine | `vdp/vdp.py build` | Customer-approved output straight from the CSV: per-record singles, merged front/back, QR decode verification |
| MegaEdit template | built by `mexgen build` from a `.mex.json` config | Self-service editor product and CSV batch product on the storefront |
| CSV prep | `vdp/prep_csv.py` | Turns the customer's raw CSV into the batch CSV MegaEdit needs (see §5) |
| Spot mask | `vdp/vdp.py build --spot-uv` | Post-order: the spot-UV file MegaEdit cannot produce (see §7) |

One layout file drives both engines. The MEX config is derived from it
(baselines → frame centres, hex → CMYK) and the two builds share the same
token names, so a CSV that works in one works in the other.

---

## 2. Prerequisites

1. **Static fonts.** Both faces must be static TTF/OTF (no `fvar` table);
   MegaEdit renders variable fonts as a system fallback. Verify with
   `mexgen validate` (`FONT_VARIABLE`) before anything else. Declared names
   follow Invent's convention, `"Family - Style"`.
2. **Backgrounds.** `py vdp/vdp.py backgrounds <layout>` writes one PDF per
   template page with the placeholder text and the QR placeholder rectangle
   removed and the trim box intact. Page 1 is the variable side, page 2 the
   static back.
3. **A donor MEX with a native barcode field.** `mexgen build` clones field
   prototypes from a donor; the barcode prototype comes from any export that
   has one. The `skeleton` block replaces the donor's pages, fonts and
   backgrounds, so the donor's page count and fonts do not matter. Prefer a
   plugin 2.8.x donor: a 2.6.7 export predates batch-in-MEX and lacks six
   text-field keys the newer plugin writes. The generator's own
   `fixtures/barcode.mex` (2.8.1, batch on, one QR prototype) is enough.
   Watch what the prototype carries — a badge donor's text fields are
   `TextCase uppercase`, which a card drops with `"TextCase": null`.
4. **Generator.** The canonical `mexgen.py` (with `validate`, `skeleton` and
   BARCODE support). The copy in this repo's `mexgen/` is a frozen snapshot
   without those features.

---

## 3. Field table (front, 252×144 pt trim + 9 pt bleed)

Frames are MegaEdit frames: `x`/`y` are the frame **centre**, text column
left edge at 22.74 pt, width 160 pt so nothing reaches the logo. Baselines
below are the approved PDF's; frame tops were derived from them (ascent +
half-leading) and are first-pass — nudge in the editor if a line lands off.

**Coordinates in this table are on the bleed page** (the placement PDF's
270 × 162 origin), which is what the PDF engine uses. **MegaEdit's origin
is the trim corner**, so the `.mex.json` config subtracts the bleed from
every x and y — the first import landed every frame exactly 9 pt low and
right. The same import measured the derived frame tops 1.00 pt high on the
12 pt name and 0.07 pt high on the 7.8 pt lines; both are folded into the
config.

| Field | Type | Value | Baseline (pt) | Frame h | Font | Align | Notes |
|---|---|---|---|---|---|---|---|
| name | TEXT | `[#First Name#] [#Last Name#]` | 31.80 | 14 | Bold 12 pt, brand navy | left / top | |
| title | TEXT | `[#Title + Department#]` | 42.04 (+10 for line 2) | 20 | Regular 7.8 pt, gray | left / top | Wraps to 2 lines max; one CSV column |
| phones | TEXT | `[#Cell Line#]<br />[#Office Line#]` | 81.70 / 91.70 | 20 | Regular 7.8 pt, gray | left / **bottom** | Cell before office. A blank cell line drops out and the office line sits on the lower baseline, directly above the email |
| email | TEXT | `[#Email#]` | 105.08 | 10 | Regular 7.8 pt, gray | left / top | |
| url | TEXT | `[#URL#]` | 115.08 | 10 | Regular 7.8 pt, gray | left / top | |
| address1 | TEXT | `[#Address Line#]` | 128.64 | 10 | Regular 7.8 pt, gray | left / top | `Street, Suite,` — suite omitted when blank, trailing comma always |
| address2 | TEXT | `[#City#], [#State#] [#Zip#]` | 138.64 | 10 | Regular 7.8 pt, gray | left / top | |
| vcardQR | BARCODE (QR) | vCard 3.0, see §4 | box 194.96–246.60 × 87.00–138.64 | 51.64 sq | modules brand navy | — | Width = width of the logo's tagline, right edge = logo right edge, bottom = last address baseline |

All text frames: `FieldGrowType fixed`, `FitTextToBox` **off** (the donor
had shrink-to-fit on, which would silently shrink a long title instead of
wrapping it), no `TextCase` element (text renders as typed), leading
128.2 % of 7.8 pt = 10 pt.

The back is static artwork; no fields.

---

## 4. vCard template

```
BEGIN:VCARD
VERSION:3.0
N:[#Last Name#];[#First Name#];;;
FN:[#First Name#] [#Last Name#]
ORG:<company name, literal>
TITLE:[#Title + Department#]
TEL;TYPE=CELL,VOICE:[#Cell Number#]
TEL;TYPE=WORK,VOICE:[#Office Number#]
EMAIL;TYPE=WORK:[#Email#]
URL:[#URL#]
ADR;TYPE=WORK:;[#Address2#];[#Address#];[#City#];[#State#];[#Zip#]
END:VCARD
```

This text is what the PDF engine encodes. In the MEX it travels
differently, for reasons learned from five imports:

- The barcode field is inert without the `Barcode Field` script under
  `<Resources><Scripts>`; the generator declares it with the field.
- A barcode whose value is this text with tokens renders, but MegaEdit
  resolves it **once, at save**: a batch put row 1's QR on every record,
  and the editor does not re-render it when a form value changes.
- Every real variable-driven barcode export binds the whole value to
  **one variable**. So the MEX has a `vCard` variable, the barcode is
  bound to it (`options.variable`), and `prep_csv.py` writes the whole
  vCard — these lines, blank ones dropped, LF-separated — as one
  multi-line cell in a derived `vCard` column. The storefront then encodes
  exactly what the PDF engine encodes, per record.
- Module colour goes to the XML `<Options><Color>c:m:y:k</Color>` as well
  as the JSON channels; the JSON alone rendered black.

The `options.vcard` map (card field → CSV column) that writes the
`ADVANCED` block a real vCard export carries is not needed for rendering;
it feeds the editor's vCard dialog and is left out of this product.

Cell is listed before office, on the card and in the vCard. Error
correction L, no quiet zone inside the box (the white knock-out around the
box is the quiet zone). At this size a full vCard is 61–65 modules, roughly
0.27 mm per module — dense but scannable; flagged to the customer once.

The PDF engine omits a `TEL` line whose number is blank. MegaEdit cannot
(see §6), so a blank number leaves `TEL;TYPE=CELL,VOICE:` with no value —
phones import such a line cleanly in the cases tested so far; confirm once
on the storefront (test plan §9, item 7).

---

## 5. Variables, required flags, prefill

| Variable | Required | Source in editor | In batch CSV |
|---|---|---|---|
| First Name | Yes | Prefill (account), editable | raw column |
| Last Name | Yes | Prefill | raw column |
| Title + Department | Yes | Prefill if stored, else typed | raw column |
| Office Number | No | typed | raw column |
| Cell Number | No | typed | raw column |
| Email | Yes | Prefill (account email) | raw column |
| URL | No | typed | raw column |
| Address | No | typed | raw column |
| Address2 | No | typed | raw column |
| City / State / Zip | No | typed | raw columns |
| Cell Line | No | typed as `C 703.555.0100` | **derived** by `prep_csv.py` |
| Office Line | No | typed as `T 703.555.0100` | **derived** |
| Address Line | No | typed as `Street, Suite,` | **derived** |
| vCard | No | pasted whole, or left blank (QR empty in the editor) | **derived**: the whole vCard of §4 as one multi-line cell; the barcode is bound to this variable |

- The twelve raw variables are **exactly the customer's CSV headers**, so
  the upload maps 1:1 with no renaming.
- `required` is set on the four variables above. Genuine exports only carry
  `validation.required` on dropdowns; whether MegaEdit enforces it on a
  text variable is unverified — check on import and set it in the editor if
  not (test plan item 4).
- Prefill is product-level (Prepopulate Data Script on the product's
  Scripts tab), nothing in the MEX. Same as the two-product spec §7.

---

## 6. Batch CSV instructions (for the customer, and for whoever runs the prep)

**Header row, exactly:**

```
First Name,Last Name,Title + Department,Office Number,Cell Number,Email,URL,Address,Address2,City,State,Zip
```

- UTF-8, straight quotes. Rows with a blank First Name are skipped.
- **Phones**: any 10-digit form is accepted (`(703) 555-0100`,
  `703-555-0100`); the prep step rewrites it to `703.555.0100`. A number
  that is not 10 digits is kept as typed and should be fixed in the sheet.
- **Blank cells**: Cell Number or Office Number blank → that line is left
  off the card and its `TEL` line is dropped from the vCard (PDF engine) or
  left empty (MegaEdit). Address2 blank → the suite is omitted and the
  street line keeps its trailing comma. URL blank → the URL line is left off.
- **Title + Department** is one column and may wrap to a second line; a
  title that needs three lines fails the PDF build and must be shortened.
- Same cell and office number is only a warning; it printed that way once
  in an approved run.

**The MegaEdit product does not take the raw CSV.** Run

```sh
py vdp/prep_csv.py vdp/customers/<customer>.json raw.csv
```

and upload the resulting `raw-megaedit.csv`. It carries the twelve raw
columns unchanged plus `Cell Line`, `Office Line` and `Address Line`. This
is the workaround for a platform limit: **Invent Variable Logic does not
fire in CSV batch** (confirmed after nine probes, see `ROADMAP.md`), so a
label that should vanish with its value (`C ` before a blank number) cannot
be conditional in the template — it has to live in the data. In the editor,
a self-service user types those three lines themselves; the required
fields guarantee the card is never blank where it matters.

The alternative — accept an orphaned `C ` label in self-service and use raw
tokens — was rejected because it would print wrong cards from a valid CSV.

---

## 7. Spot UV — post-order step

MegaEdit output is the print file only; it cannot emit a spot separation.
The mask stays in the PDF engine:

```sh
py vdp/vdp.py build vdp/customers/<customer>.json order.csv --out order/ --spot-uv
```

writes `<record>_SpotUV.pdf` per record and a merged mask with the same
page count and boxes as the print file: the configured elements at 100 %
of a Separation colour named `SpotUV`, everything else empty. The build
refuses if any process-colour operator survives in the mask. Which
elements carry the UV (logo, QR, name) is set per layout under
`spot_uv.elements` — **not yet specified for this product**; the layout
carries a TBD note and `--spot-uv` fails with it until the list is filled.

Run it against the order's CSV (the prepped one works too, extra columns
are ignored with a warning). If the storefront output is the only source,
export its CSV from the order and use that.

---

## 8. Build steps (in order)

1. `py vdp/vdp.py check <layout> raw.csv` — layout and data sanity.
2. `py vdp/vdp.py backgrounds <layout>` — front and back background PDFs.
3. Write the `.mex.json` config (donor with a barcode field, `skeleton`
   with the two backgrounds and the fonts folder, `batch: true`, the
   variables and fields of §3 and §5, `logic: []`). `batch: true` is what
   makes it a CSV product: it writes the XML `BatchSource`, the JSON
   `config.batch.mode` and `batchSource: true` on every variable together —
   batch is a setting inside the MEX, not something admin adds afterwards.
4. `py mexgen.py build <config>` then `py mexgen.py validate <output.mex>`
   — zero errors, zero warnings expected.
5. Import into MegaEdit; run the test plan (§9); log the result in the
   generator's `TESTLOG.md`. Nothing is done until MegaEdit opens it and a
   scanned QR resolves to the right contact.
6. Enable Prepopulate Data Script; set required flags if the MEX's did not
   take; save as Product Default; publish.
7. On each batch order: `prep_csv.py` → upload → (post-order) `--spot-uv`.

---

## 9. Test plan

1. **Import** — accepted without error; both pages show the right art.
2. **Fonts** — both faces render as the declared family, not a fallback.
3. **Geometry** — name, title, phone, email, URL and address baselines match
   the approved PDF within a point or two; adjust and re-export otherwise.
4. **Required** — Add to Basket is blocked with First/Last/Title/Email blank.
5. **QR colour** — modules are brand navy. Black means the JSON-only colour
   was ignored; set it in the editor and note it in the log.
6. **QR content** — scan: name, title, both numbers, email, URL, address
   all present and correct. Literal `[#…#]` in the scan means the tokens
   were not resolved on the side MegaEdit rendered from; record which.
7. **Blank TEL** — clear Cell Number, scan again: the contact still imports.
8. **Batch** — the product opens with a CSV upload control and the mapping
   step lists every variable as a column (all raw columns plus the three
   derived ones). Upload the prepped CSV with one row that has no cell
   number: that card shows the office line alone on the lower baseline;
   every QR scans to its own row; the record count matches.
9. **Self-service** — as a customer, open the editor: prefilled name, title
   and email; type the three line fields; proof matches the batch card.
10. **PDF engine parity** — `vdp.py build` on the same CSV: every record's
    QR decodes to the encoded vCard, trim boxes and static back verified,
    output matches the approved run pixel for pixel on the text.

---

## Sources

- Invent Variable Logic and the batch firing gap (local: `docs-library/07-invent/invent-variable-logic.md`, `ROADMAP.md` "Closed / Won't Do")
- Prepopulate Data Script (local: `docs-library/01-official-infigo/prepopulate-data-script-megaedit.md`)
- Two-product business card pattern (local: `businesscard-two-product-build-spec.md`)
- MEX format: fonts, dual representation, barcode fields — the generator's `SPEC.md` §6, §7, §12, §18
- PDF engine layout schema (local: `vdp/README.md`)
