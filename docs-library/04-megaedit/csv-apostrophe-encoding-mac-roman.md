# CSV Apostrophe → Õ in MegaEdit Proof (Encoding Mismatch)

**Tags:** megaedit, csv, spreadsheet-upload, encoding, apostrophe, smart-quotes, mac-roman, windows-1252, vdp

## Problem
A customer's last name "O'Brien" rendered in the MegaEdit proof as **"OÕBrien"** after uploading via the CSV/Spreadsheet-upload product. The customer reported the apostrophe "keeps turning into a quote mark." Re-typing "an apostrophe" did not fix it.

## Root cause (with evidence)
The apostrophe was a **curly/smart apostrophe** `'` (U+2019), not a straight one — that's the default produced by Excel/Word AutoCorrect and Mac keyboards.

The exact corruption `' → Õ` is the diagnostic fingerprint of a **Mac-Roman-encoded file being read as Windows-1252**:

- Curly apostrophe **U+2019** is stored as byte **`0xD5`** in Mac Roman.
- Byte **`0xD5`** in **Windows-1252 / Latin-1** = **`Õ`** (Latin capital O with tilde, U+00D5).

So a Mac-saved file passed through a Windows-1252 read step turns the apostrophe into `Õ`. MegaEdit is not at fault — it renders whatever byte the upload pipeline hands it. The damage happens at save/encoding time, before MegaEdit sees the data. The `Õ` specifically implicates a Mac somewhere in the save chain.

## Fix
1. **Bulletproof:** Use a plain **straight apostrophe** `'` (ASCII `0x27`). It's a single low byte, identical in every encoding, so it can't break on any round trip.
   - Disable Excel smart quotes: Options → Proofing → AutoCorrect Options → AutoFormat As You Type → uncheck **"Straight quotes" with "smart quotes."**
   - On Mac: System Settings → Keyboard → Text → uncheck **"Use smart quotes."**
2. **Workflow fix (vendor-recommended):** Keep the **XLSX as the reusable template** (also resolves prior date auto-format issues). When the list is ready, **Save As → CSV** and upload the CSV. Saving to CSV **re-encodes** the curly apostrophe into the byte MegaEdit expects (Windows-1252 on Windows), which is what cleans up the preview.

## Sample
| Input (as saved) | Stored byte | Read as | Proof shows |
|---|---|---|---|
| `'` curly, Mac Roman | `0xD5` | Windows-1252 | `Õ` ❌ |
| `'` straight (ASCII) | `0x27` | any | `'` ✅ |
| `'` curly, CSV re-saved on Windows | `0x92` (1252) | Windows-1252 | `'` ✅ |

## Caveats / interactions
- The "Save As CSV fixes it" advice is **encoding-luck-dependent**, NOT because CSV strips characters. The curly apostrophe survives into the CSV — it just gets re-written in a friendlier encoding.
- On a **Mac**, Excel-for-Mac's CSV export can re-emit Mac encoding → `Õ` returns. Confirm the user's machine before promising this fix; **CSV UTF-8** export is the safer save option.
- The **straight apostrophe** is the only encoding-independent fix and should be the default guidance.
- Same root cause will hit any high-byte/typographic character (em dash —, curly double quotes " ", accented letters) — not just apostrophes.
- Candidate tooling: a CSV pre-flight checker that flags smart quotes + non-UTF-8 encoding before upload. See related: `04-megaedit/` CSV image-swap note.
