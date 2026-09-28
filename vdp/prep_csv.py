#!/usr/bin/python3
"""
prep_csv.py - turn a customer's raw CSV into the MegaEdit batch CSV.

MegaEdit's Variable Logic does not fire in CSV batch, so a label that should
disappear with its value ("C " in front of a blank cell number) has to be
carried in the data instead. This step keeps every raw column as-is (so the
upload maps 1:1 onto the template's variables), applies the layout's
transforms (phone formatting), and appends the derived columns the layout
declares under megaedit.derived_columns - each blank when every token in it
is blank. A derived column declared as {"vcard": true} carries the layout's
whole vCard (qr.vcard, blank lines dropped) as one multi-line cell, for a
barcode bound to that variable.

Usage:
  py prep_csv.py <layout.json> <raw.csv> [--out FILE]

Default output: <raw>-megaedit.csv beside the input, UTF-8 with BOM.
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from vdp import Layout, expand, expand_lines, read_records  # noqa: E402


def prepared_rows(layout, records):
    derived = (layout.d.get("megaedit") or {}).get("derived_columns") or {}
    headers = list(layout.headers) + list(derived)
    rows = []
    for record in records:
        row = {h: record.get(h, "") for h in layout.headers}
        for name, template in derived.items():
            if isinstance(template, dict) and template.get("vcard"):
                # the whole vCard as one cell, so a MegaEdit barcode bound
                # to this variable gets its own contact per record; the
                # same line list and blank-line rule as the PDF engine's QR
                qr = layout.d.get("qr") or {}
                lines = expand_lines(qr.get("vcard") or [], record,
                                     suppress_blank=qr.get("omit_line_if_blank", True))
                ending = chr(13) + chr(10) if str(template.get("line_ending", "LF")).upper() == "CRLF" else chr(10)
                row[name] = ending.join(lines)
                continue
            text, had, blank = expand(template, record)
            row[name] = "" if (had and blank) else text
        rows.append(row)
    return headers, rows


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("layout")
    parser.add_argument("csv")
    parser.add_argument("--out", help="output CSV (default: <raw>-megaedit.csv)")
    args = parser.parse_args()

    layout = Layout(args.layout)
    records = read_records(layout, args.csv)
    headers, rows = prepared_rows(layout, records)
    out = Path(args.out) if args.out else Path(args.csv).with_name(
        Path(args.csv).stem + "-megaedit.csv")
    with open(out, "w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)
    print("wrote %s: %d row(s), %d column(s) (%d raw + %d derived)"
          % (out, len(rows), len(headers), len(layout.headers),
             len(headers) - len(layout.headers)))


if __name__ == "__main__":
    main()
