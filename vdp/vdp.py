#!/usr/bin/python3
"""
vdp.py - config-driven variable-data PDF engine for static print templates.

Drives a designer's placement PDF with a CSV: redacts the placeholder text,
sets live text at configured baselines with embedded fonts, knocks out and
draws a vCard QR, writes one PDF per record plus a merged file, and verifies
every QR by decoding it back off a 600 dpi render.

Usage:
  py vdp.py build <layout.json> <data.csv> [--out DIR] [--spot-uv] [--no-verify]
  py vdp.py backgrounds <layout.json> [--out DIR]     # redacted pages for MegaEdit
  py vdp.py check <layout.json> [<data.csv>]           # validate layout (+ data) only

Layout JSON: see README.md. Field values use the same [#Column#] token syntax
MegaEdit uses, so one layout can feed both engines. An optional group
[?...?] is dropped when every token inside it is blank, and a line whose
tokens are all blank is suppressed.

Dependencies: pymupdf, qrcode, opencv-python-headless (+ numpy). See
requirements.txt. Python 3.9+.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path

import pymupdf as fitz
import qrcode

TOKEN_RE = re.compile(r"\[#(.+?)#\]")
GROUP_RE = re.compile(r"\[\?(.*?)\?\]", re.S)
SENTINEL = (1.0, 0.0, 1.0)          # pure magenta: what the spot pass draws in
SENTINEL_FILL = re.compile(r"(?<![\d.])1(?:\.0+)? 0(?:\.0+)? 1(?:\.0+)? rg\b")
SENTINEL_STROKE = re.compile(r"(?<![\d.])1(?:\.0+)? 0(?:\.0+)? 1(?:\.0+)? RG\b")
COLOR_OPS = re.compile(r"(?:^|\s)(?:rg|RG|g|G|k|K|cs|CS|sc|SC|scn|SCN)(?=\s|$)")


def die(msg):
    print("ERROR: " + msg, file=sys.stderr)
    sys.exit(1)


def warn(msg):
    print("WARN:  " + msg)


# ---------------------------------------------------------------------------
# tokens
# ---------------------------------------------------------------------------

def tokens_in(template):
    """Every [#token#] name in a template string, groups included."""
    return TOKEN_RE.findall(template)


def expand(template, record):
    """Resolve [#tokens#] and [?optional groups?] against one record.

    Returns (text, had_tokens, all_blank). all_blank is True when the template
    carried tokens and every one of them resolved to blank - the signal for
    blank-line suppression.
    """
    def value(name):
        return (record.get(name) or "").strip()

    def group(match):
        inner = match.group(1)
        names = tokens_in(inner)
        if names and all(not value(n) for n in names):
            return ""
        return TOKEN_RE.sub(lambda t: value(t.group(1)), inner)

    names = tokens_in(template)
    text = GROUP_RE.sub(group, template)
    text = TOKEN_RE.sub(lambda t: value(t.group(1)), text)
    all_blank = bool(names) and all(not value(n) for n in names)
    return text, bool(names), all_blank


def expand_lines(templates, record, suppress_blank=True):
    """Expand a list of line templates, dropping lines whose tokens are all blank."""
    out = []
    for template in templates:
        text, had, blank = expand(template, record)
        if suppress_blank and had and blank:
            continue
        out.append(text)
    return out


# ---------------------------------------------------------------------------
# transforms
# ---------------------------------------------------------------------------

def phone_dots(raw):
    """'(703) 555-0100' -> '703.555.0100'. Anything not 10 digits is kept as typed."""
    digits = re.sub(r"\D", "", raw or "")
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    if len(digits) == 10:
        return "%s.%s.%s" % (digits[:3], digits[3:6], digits[6:])
    return (raw or "").strip()


TRANSFORMS = {"phone_dots": phone_dots}


# ---------------------------------------------------------------------------
# layout + data
# ---------------------------------------------------------------------------

class Layout:
    def __init__(self, path):
        self.path = Path(path).resolve()
        if not self.path.is_file():
            die("layout not found: %s" % self.path)
        try:
            self.d = json.loads(self.path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            die("layout is not valid JSON: %s" % exc)
        self.base = (self.path.parent / self.d.get("base_dir", ".")).resolve()
        if not self.base.is_dir():
            die("base_dir does not exist: %s" % self.base)
        self.page = self.d["page"]
        self.template = self.d["template"]
        self.fields = self.d.get("fields") or []
        self.qr = self.d.get("qr")
        self.csv = self.d.get("csv") or {}
        self.headers = list(self.csv.get("headers") or [])
        self.defaults = self.d.get("defaults") or {}
        self.transforms = self.d.get("transforms") or {}
        self.output = self.d.get("output") or {}
        self.qc = self.d.get("qc") or {}
        self.spot = self.d.get("spot_uv") or {}
        self.colors = {k: self._color(v) for k, v in (self.d.get("colors") or {}).items()}
        self.font_files = {k: self.resolve(v["file"])
                           for k, v in (self.d.get("fonts") or {}).items()}
        self.check()

    def resolve(self, rel):
        return (self.base / rel).resolve()

    @staticmethod
    def _color(spec):
        hexcode = spec["hex"] if isinstance(spec, dict) else spec
        hexcode = hexcode.lstrip("#")
        return tuple(int(hexcode[i:i + 2], 16) / 255 for i in (0, 2, 4))

    # -- validation ----------------------------------------------------------

    def all_templates(self):
        """(where, template) for every string that may carry tokens."""
        out = []
        for f in self.fields:
            for key in ("value",):
                if f.get(key):
                    out.append(("field %s" % f.get("name"), f[key]))
            for line in f.get("lines") or []:
                out.append(("field %s" % f.get("name"), line))
        for line in (self.qr or {}).get("vcard") or []:
            out.append(("qr.vcard", line))
        for key in ("single", "merged"):
            if self.output.get(key):
                out.append(("output.%s" % key, self.output[key]))
        for name, tpl in ((self.d.get("megaedit") or {}).get("derived_columns") or {}).items():
            if isinstance(tpl, dict):
                continue   # {"vcard": true} reuses qr.vcard, checked above
            out.append(("megaedit.derived_columns.%s" % name, tpl))
        return out

    def check(self):
        problems = []
        if not self.headers:
            problems.append("csv.headers is empty")
        for where, template in self.all_templates():
            for name in tokens_in(template):
                if name not in self.headers:
                    problems.append("%s uses [#%s#], which is not in csv.headers"
                                    % (where, name))
        for name in self.transforms:
            if name not in self.headers:
                problems.append("transforms names column %r, not in csv.headers" % name)
            elif self.transforms[name] not in TRANSFORMS:
                problems.append("unknown transform %r (have: %s)"
                                % (self.transforms[name], ", ".join(TRANSFORMS)))
        tpl = self.resolve(self.template["file"])
        if not tpl.is_file():
            problems.append("template not found: %s" % tpl)
        for key, path in self.font_files.items():
            if not path.is_file():
                problems.append("font %r not found: %s" % (key, path))
        for f in self.fields:
            if not f.get("name"):
                problems.append("a field has no name")
            if bool(f.get("value")) == bool(f.get("lines")):
                problems.append("field %s needs exactly one of value / lines"
                                % f.get("name"))
            if f.get("lines") and len(f.get("baselines") or []) != len(f["lines"]):
                problems.append("field %s: lines and baselines differ in length"
                                % f.get("name"))
            if f.get("value") and f.get("baseline") is None:
                problems.append("field %s needs a baseline" % f.get("name"))
            font = f.get("font", self.defaults.get("font"))
            if font not in self.font_files:
                problems.append("field %s uses font %r, not declared" % (f.get("name"), font))
            color = f.get("color", self.defaults.get("color"))
            if color not in self.colors:
                problems.append("field %s uses color %r, not declared" % (f.get("name"), color))
        if self.qr:
            if self.qr.get("module_color") not in self.colors:
                problems.append("qr.module_color %r not declared" % self.qr.get("module_color"))
            if len(self.qr.get("box") or []) != 4:
                problems.append("qr.box must be [x0, y0, x1, y1]")
        for element in self.spot.get("elements") or []:
            kind = element.get("type")
            if kind == "field" and element.get("name") not in {f.get("name") for f in self.fields}:
                problems.append("spot_uv element names unknown field %r" % element.get("name"))
            elif kind == "rect" and len(element.get("rect") or []) != 4:
                problems.append("spot_uv rect element needs rect: [x0, y0, x1, y1]")
            elif kind not in ("field", "rect", "qr"):
                problems.append("spot_uv element type %r is not field | rect | qr" % kind)
        if problems:
            die("layout %s:\n  - %s" % (self.path.name, "\n  - ".join(problems)))


def read_records(layout, csv_path):
    """Records as dicts keyed by layout header, transformed and stripped.

    Dies on a missing column or a blank required cell - a silent skip would
    ship a card with a hole in it.
    """
    path = Path(csv_path)
    if not path.is_file():
        die("CSV not found: %s" % path)
    with open(path, newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        raw_headers = [h.strip() for h in (reader.fieldnames or [])]
        rows = list(reader)
    missing = [h for h in layout.headers if h not in raw_headers]
    if missing:
        die("CSV %s is missing column(s): %s\n       expected: %s"
            % (path.name, ", ".join(missing), ", ".join(layout.headers)))
    extra = [h for h in raw_headers if h not in layout.headers]
    if extra:
        warn("CSV carries column(s) the layout does not use: %s" % ", ".join(extra))

    skip_key = layout.csv.get("skip_row_if_blank")
    required = layout.csv.get("required") or []
    records, problems = [], []
    for number, row in enumerate(rows, start=2):   # 1 is the header line
        record = {h: (row.get(h) or "").strip() for h in layout.headers}
        if skip_key and not record.get(skip_key):
            continue
        for name, transform in layout.transforms.items():
            record[name] = TRANSFORMS[transform](record[name])
        for name in required:
            if not record.get(name):
                problems.append("row %d: required column %r is blank" % (number, name))
        record["_row"] = number
        records.append(record)
    if problems:
        die("CSV %s:\n  - %s" % (path.name, "\n  - ".join(problems)))
    if not records:
        die("CSV %s has no usable rows" % path.name)
    return records


# ---------------------------------------------------------------------------
# text layout
# ---------------------------------------------------------------------------

class Fonts:
    def __init__(self, layout):
        self.files = layout.font_files
        self.metrics = {k: fitz.Font(fontfile=str(p)) for k, p in self.files.items()}

    def width(self, key, text, size):
        return self.metrics[key].text_length(text, fontsize=size)

    def install(self, page):
        for key, path in self.files.items():
            page.insert_font(fontname="F_" + key, fontfile=str(path))

    @staticmethod
    def name(key):
        return "F_" + key


def wrap(text, fonts, key, size, width):
    """Greedy word wrap; a single word wider than the box still gets its line."""
    lines, current = [], ""
    for word in text.split():
        candidate = (current + " " + word).strip()
        if not current or fonts.width(key, candidate, size) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current or not lines:
        lines.append(current)
    return lines


def layout_field(field, record, fonts, layout, problems):
    """[(x, baseline, text, font key, size, color key)] for one field.

    Pure geometry - nothing is drawn here, so the spot-UV pass can reuse the
    exact same runs in a different colour.
    """
    d = layout.defaults
    x = field.get("x", d.get("x", 0))
    key = field.get("font", d.get("font"))
    size = field.get("size", d.get("size", 10))
    color = field.get("color", d.get("color"))
    leading = field.get("leading", d.get("leading", size * 1.2))
    runs = []

    if field.get("lines"):
        lines = expand_lines(field["lines"], record)
        baselines = list(field["baselines"])
        if field.get("align_v", "top") == "bottom":
            ys = baselines[len(baselines) - len(lines):]
        else:
            ys = baselines[:len(lines)]
        for y, text in zip(ys, lines):
            runs.append((x, y, text, key, size, color))
        return runs

    text, had, blank = expand(field["value"], record)
    if had and blank:
        return runs
    if field.get("wrap_width"):
        lines = wrap(text, fonts, key, size, field["wrap_width"])
        limit = field.get("max_lines")
        if limit and len(lines) > limit:
            problems.append("row %s: field %s needs %d lines (max %d): %r"
                            % (record.get("_row"), field["name"], len(lines), limit, text))
    else:
        lines = [text]
    for n, line in enumerate(lines):
        runs.append((x, field["baseline"] + n * leading, line, key, size, color))
    return runs


def draw_runs(page, runs, layout, override=None):
    for x, y, text, key, size, color in runs:
        page.insert_text((x, y), text, fontname=Fonts.name(key), fontsize=size,
                         color=override or layout.colors[color])


# ---------------------------------------------------------------------------
# QR
# ---------------------------------------------------------------------------

EC = {"L": qrcode.constants.ERROR_CORRECT_L, "M": qrcode.constants.ERROR_CORRECT_M,
      "Q": qrcode.constants.ERROR_CORRECT_Q, "H": qrcode.constants.ERROR_CORRECT_H}


def vcard_text(qr, record):
    lines = expand_lines(qr["vcard"], record, suppress_blank=qr.get("omit_line_if_blank", True))
    ending = "\r\n" if qr.get("line_ending", "CRLF").upper() == "CRLF" else "\n"
    return ending.join(lines)


def qr_matrix(qr, text):
    code = qrcode.QRCode(error_correction=EC[qr.get("error_correction", "L").upper()],
                         border=int(qr.get("quiet_zone_modules", 0)))
    code.add_data(text)
    code.make(fit=True)
    return code.get_matrix()


def module_rects(box, matrix):
    """Rects for the dark modules, edge to edge with a hairline overlap so
    adjacent modules never show a white seam when rasterised."""
    n = len(matrix)
    cell = box.width / n
    out = []
    for i, row in enumerate(matrix):
        for j, dark in enumerate(row):
            if dark:
                out.append(fitz.Rect(box.x0 + j * cell, box.y0 + i * cell,
                                     min(box.x0 + (j + 1) * cell + 0.05, box.x1),
                                     min(box.y0 + (i + 1) * cell + 0.05, box.y1)))
    return out


def draw_modules(page, rects, color):
    shape = page.new_shape()
    for rect in rects:
        shape.draw_rect(rect)
    shape.finish(color=None, fill=color)
    shape.commit()


# ---------------------------------------------------------------------------
# template preparation
# ---------------------------------------------------------------------------

def redact_text(page):
    count = 0
    for block in page.get_text("dict")["blocks"]:
        if "lines" in block:
            page.add_redact_annot(fitz.Rect(block["bbox"]))
            count += 1
    if count:
        page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=0)
    return count


def remove_vectors_inside(page, rect):
    """Drop vector art fully inside rect (graphics mode 1 = remove if covered)."""
    page.add_redact_annot(fitz.Rect(rect))
    page.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=1)


def knockouts_for(layout, page_number):
    return [fitz.Rect(r) for r in (layout.template.get("knockouts") or {}).get(str(page_number), [])]


def prepare_page(page, layout, page_number):
    """Placeholder text gone, knock-outs painted white, fonts installed."""
    if page_number in (layout.template.get("redact_text_pages") or []):
        redact_text(page)
    for rect in knockouts_for(layout, page_number):
        page.draw_rect(rect, color=None, fill=(1, 1, 1))


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

def safe_name(text):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", text).strip("_") or "record"


def build_record(layout, fonts, record, problems):
    """One record -> (document, qr text, matrix size, runs by field, module rects)."""
    doc = fitz.open(str(layout.resolve(layout.template["file"])))
    runs_by_field, modules, qr_text, size = {}, [], None, 0
    for page_number in layout.template.get("variable_pages") or [1]:
        page = doc[page_number - 1]
        prepare_page(page, layout, page_number)
        fonts.install(page)
        for field in layout.fields:
            if field.get("page", layout.defaults.get("page", 1)) != page_number:
                continue
            runs = layout_field(field, record, fonts, layout, problems)
            runs_by_field[field["name"]] = runs
            draw_runs(page, runs, layout)
        if layout.qr and layout.qr.get("page", 1) == page_number:
            box = fitz.Rect(layout.qr["box"])
            white = box
            for rect in knockouts_for(layout, page_number):
                white = white | rect
            page.draw_rect(white, color=None, fill=(1, 1, 1))
            qr_text = vcard_text(layout.qr, record)
            matrix = qr_matrix(layout.qr, qr_text)
            size = len(matrix)
            modules = module_rects(box, matrix)
            draw_modules(page, modules, layout.colors[layout.qr["module_color"]])
        page.clean_contents()
    return doc, qr_text, size, runs_by_field, modules


def build_spot(layout, fonts, doc, runs_by_field, modules):
    """A companion PDF: configured elements at 100% of a named spot colour,
    everything else knocked out, same page boxes as the print file."""
    spot = layout.spot
    name = spot.get("spot_name", "SpotUV")
    elements = spot.get("elements") or []
    if not elements:
        die("spot_uv.elements is empty - nothing to mask (status: %s)"
            % spot.get("status", "unspecified"))
    out = fitz.open()
    for source in doc:
        page = out.new_page(width=source.rect.width, height=source.rect.height)
        for setter, getter in (("set_cropbox", "cropbox"), ("set_trimbox", "trimbox"),
                               ("set_bleedbox", "bleedbox"), ("set_artbox", "artbox")):
            try:
                getattr(page, setter)(getattr(source, getter))
            except (ValueError, AttributeError):
                pass
        number = source.number + 1
        if number not in (layout.template.get("variable_pages") or [1]):
            continue
        fonts.install(page)
        for element in elements:
            kind = element.get("type")
            if kind == "qr" and layout.qr and layout.qr.get("page", 1) == number:
                draw_modules(page, modules, SENTINEL)
            elif kind == "field":
                field = next(f for f in layout.fields if f["name"] == element["name"])
                if field.get("page", layout.defaults.get("page", 1)) == number:
                    draw_runs(page, runs_by_field.get(element["name"], []), layout,
                              override=SENTINEL)
            elif kind == "rect" and element.get("page", 1) == number:
                page.draw_rect(fitz.Rect(element["rect"]), color=None, fill=SENTINEL)
        page.clean_contents()
        sentinel_to_spot(out, page, name)
    return out


def sentinel_to_spot(doc, page, name):
    """Rewrite the page's content so every sentinel colour becomes the named
    Separation. Verified afterwards: no other colour operator may remain."""
    contents = page.get_contents()
    if not contents:
        return
    xref = contents[0]
    stream = doc.xref_stream(xref).decode("latin-1")
    stream = SENTINEL_FILL.sub("/%s cs 1 scn" % name, stream)
    stream = SENTINEL_STROKE.sub("/%s CS 1 SCN" % name, stream)
    leftovers = [m.group(0).strip() for m in COLOR_OPS.finditer(stream)
                 if m.group(0).strip() not in ("cs", "scn", "CS", "SCN")]
    if leftovers:
        die("spot page still carries non-spot colour operators: %s" % sorted(set(leftovers)))
    doc.update_stream(xref, stream.encode("latin-1"))
    function = doc.get_new_xref()
    doc.update_object(function, "<</FunctionType 2 /Domain [0 1] /C0 [0 0 0 0] "
                                "/C1 [0 0 0 1] /N 1>>")
    colorspace = doc.get_new_xref()
    doc.update_object(colorspace, "[/Separation /%s /DeviceCMYK %d 0 R]" % (name, function))
    doc.xref_set_key(page.xref, "Resources/ColorSpace/%s" % name, "%d 0 R" % colorspace)


# ---------------------------------------------------------------------------
# verification
# ---------------------------------------------------------------------------

def decode_qr(pdf_path, layout, expected):
    """Decode the QR back off a render. Returns None on success, else a reason."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        return "opencv-python-headless / numpy not installed (pip install -r requirements.txt)"
    doc = fitz.open(str(pdf_path))
    page = doc[layout.qr.get("page", 1) - 1]
    box = fitz.Rect(layout.qr["box"])
    pad = box.width * 0.15
    clip = fitz.Rect(box.x0 - pad, box.y0 - pad, box.x1 + pad, box.y1 + pad) & page.rect
    detector = cv2.QRCodeDetector()
    decoded = ""
    for dpi in (int(layout.qc.get("decode_dpi", 600)), 300, 900):
        pix = page.get_pixmap(dpi=dpi, clip=clip, colorspace=fitz.csGRAY)
        image = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width)
        decoded, _, _ = detector.detectAndDecode(image)
        if decoded:
            break
    if not decoded:
        return "QR did not decode at any tried resolution"
    if decoded.replace("\r\n", "\n") != expected.replace("\r\n", "\n"):
        return "QR decoded to different text than encoded"
    return None


def font_key(name):
    return re.sub(r"[^a-z0-9]", "", name.lower())


def verify_record(pdf_path, layout, source, qr_text, problems):
    doc = fitz.open(str(pdf_path))
    row_tag = pdf_path.name
    if layout.qr and qr_text is not None:
        reason = decode_qr(pdf_path, layout, qr_text)
        if reason:
            problems.append("%s: %s" % (row_tag, reason))
    trim = layout.page.get("trim")
    for page in doc:
        if trim and list(page.trimbox) != [float(v) for v in trim]:
            problems.append("%s page %d: trim box %s != %s"
                            % (row_tag, page.number + 1, list(page.trimbox), trim))
    for page_number in layout.template.get("variable_pages") or [1]:
        page = doc[page_number - 1]
        # basefont names come back as "Barlow Regular" or "ABCDEF+Barlow-Regular"
        # depending on who embedded them; compare with punctuation stripped
        embedded = {font_key(f[3].split("+")[-1]) for f in page.get_fonts()}
        for key, path in layout.font_files.items():
            if font_key(path.stem) not in embedded:
                problems.append("%s page %d: font %s not embedded (have %s)"
                                % (row_tag, page_number, path.stem, sorted(embedded)))
    for page_number in layout.template.get("static_pages") or []:
        if doc[page_number - 1].read_contents() != source[page_number - 1].read_contents():
            problems.append("%s page %d: static page content changed" % (row_tag, page_number))


def duplicate_warnings(layout, record):
    for a, b in layout.qc.get("duplicate_warn") or []:
        if record.get(a) and record.get(a) == record.get(b):
            warn("row %s: %s == %s (%s)" % (record.get("_row"), a, b, record[a]))


# ---------------------------------------------------------------------------
# commands
# ---------------------------------------------------------------------------

def cmd_check(args):
    layout = Layout(args.layout)
    print("layout OK: %s (%d fields, qr=%s, headers=%d)"
          % (layout.path.name, len(layout.fields), "yes" if layout.qr else "no",
             len(layout.headers)))
    if args.csv:
        records = read_records(layout, args.csv)
        problems = []
        fonts = Fonts(layout)
        for record in records:
            for field in layout.fields:
                layout_field(field, record, fonts, layout, problems)
            duplicate_warnings(layout, record)
        if problems:
            die("data problems:\n  - " + "\n  - ".join(problems))
        print("data OK: %d record(s)" % len(records))


def cmd_build(args):
    layout = Layout(args.layout)
    records = read_records(layout, args.csv)
    fonts = Fonts(layout)
    out_dir = Path(args.out) if args.out else layout.base / "out"
    out_dir.mkdir(parents=True, exist_ok=True)
    source = fitz.open(str(layout.resolve(layout.template["file"])))
    suffix = layout.output.get("spot_uv_suffix", "_SpotUV")

    problems = []
    merged, merged_spot = fitz.open(), fitz.open()
    written = []
    for record in records:
        duplicate_warnings(layout, record)
        doc, qr_text, size, runs, modules = build_record(layout, fonts, record, problems)
        if problems:
            break
        single_name = safe_name(expand(layout.output.get("single", "record_[#_row#].pdf"),
                                       record)[0])
        single_path = out_dir / single_name
        doc.save(str(single_path), garbage=3, deflate=True)
        merged.insert_pdf(doc)
        if args.spot_uv:
            spot = build_spot(layout, fonts, doc, runs, modules)
            spot_path = out_dir / (Path(single_name).stem + suffix + ".pdf")
            spot.save(str(spot_path), garbage=3, deflate=True)
            merged_spot.insert_pdf(spot)
            spot.close()
        doc.close()
        if not args.no_verify:
            verify_record(single_path, layout, source, qr_text, problems)
        written.append(single_path)
        print("built %s  (QR %dx%d modules)" % (single_path.name, size, size))

    if problems:
        print("BUILD FAILED:")
        for problem in problems:
            print("  - " + problem)
        sys.exit(1)

    merged_name = safe_name(layout.output.get("merged", "merged.pdf"))
    merged.save(str(out_dir / merged_name), garbage=3, deflate=True)
    line = "%d record(s); %d page(s) in %s" % (len(records), len(merged), merged_name)
    if args.spot_uv:
        merged_spot.save(str(out_dir / (Path(merged_name).stem + suffix + ".pdf")),
                         garbage=3, deflate=True)
        line += "; spot mask %s" % (Path(merged_name).stem + suffix + ".pdf")
    print(line)
    print("verified: %s" % ("skipped (--no-verify)" if args.no_verify
                            else "QR decode, trim boxes, embedded fonts, static pages"))


def cmd_backgrounds(args):
    """One PDF per template page with placeholder text and knock-out art
    removed - the pages a MegaEdit product uses as backgrounds."""
    layout = Layout(args.layout)
    out_dir = Path(args.out) if args.out else layout.base / "backgrounds"
    out_dir.mkdir(parents=True, exist_ok=True)
    source = fitz.open(str(layout.resolve(layout.template["file"])))
    stem = Path(layout.template["file"]).stem
    for page_number in range(1, len(source) + 1):
        doc = fitz.open()
        doc.insert_pdf(source, from_page=page_number - 1, to_page=page_number - 1)
        page = doc[0]
        if page_number in (layout.template.get("variable_pages") or [1]):
            if page_number in (layout.template.get("redact_text_pages") or []):
                redact_text(page)
            for rect in knockouts_for(layout, page_number):
                remove_vectors_inside(page, rect)
            page.clean_contents()
        path = out_dir / ("%s_page%d.pdf" % (stem, page_number))
        # read the page before saving: garbage collection renumbers xrefs and
        # leaves this page object pointing at nothing
        remaining = len([b for b in page.get_text("dict")["blocks"] if "lines" in b])
        trim = list(page.trimbox)
        doc.save(str(path), garbage=3, deflate=True)
        print("wrote %s  (text blocks left: %d, trim %s)" % (path.name, remaining, trim))


def main():
    parser = argparse.ArgumentParser(description="Config-driven variable-data PDF engine")
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("build", help="render one PDF per record plus a merged file")
    p.add_argument("layout")
    p.add_argument("csv")
    p.add_argument("--out", help="output directory (default: <base_dir>/out)")
    p.add_argument("--spot-uv", action="store_true",
                   help="also emit a matching spot-colour mask per record")
    p.add_argument("--no-verify", action="store_true", help="skip QR decode and QC checks")
    p.set_defaults(func=cmd_build)
    p = sub.add_parser("backgrounds", help="redacted template pages for a MegaEdit product")
    p.add_argument("layout")
    p.add_argument("--out", help="output directory (default: <base_dir>/backgrounds)")
    p.set_defaults(func=cmd_backgrounds)
    p = sub.add_parser("check", help="validate a layout, and optionally a CSV against it")
    p.add_argument("layout")
    p.add_argument("csv", nargs="?")
    p.set_defaults(func=cmd_check)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
