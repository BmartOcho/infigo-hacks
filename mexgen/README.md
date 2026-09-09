# mexgen — config-driven MEX generator

Generates ready-to-import `.mex` files (Invent → MegaEdit) from a JSON config +
a donor MEX scaffold. Keeps the dual XML/JSON representations in sync, mints
GUIDs/adobeIds, restores CDATA, packs a store-zip (built in temp, copied out,
never overwrites an existing file).

Requires Python 3.9+ (stdlib only). On Windows use `py`, elsewhere `python3`.

## Workflow

```powershell
cd mexgen

# 1. Inventory the donor + dump its guts for Claude to read
py mexgen.py inspect "..\INFIGO_Example BC_v-01.mex" --dump donor-dump

# 2. Fill the TODO_AFTER_INSPECT values in living.json / communities.json
#    (back-art field name from the inspect field list; keepFields for any
#    static art fields that must survive the strip)

# 3. Build (validates first; writes nothing on validation failure)
py mexgen.py build living.json
py mexgen.py build communities.json

# 4. Import the v-05 files into MegaEdit — import errors are invisible until
#    tested, so this is the real validation.
```

Step 1's `--dump` writes `donor-dump/template.xml` + `donor-dump/InDesignData.json`
into this folder — hand those to Claude to finalize configs precisely.

## Config reference

| Key | Meaning |
|---|---|
| `donor` / `output` | paths relative to the config file; output must not already exist |
| `mode` | `replace` (strip donor variables/fields/logic/form, keep artwork+fonts+backgrounds), `add` (additive), or `edit` (surgical — donor kept intact, see edit keys) |
| `removeVariables` | *(edit)* variable display names to delete — also pruned from the form, incl. nested GROUPs |
| `formAdd` | *(edit)* `[{name, after}]` — insert a form ITEM after an existing item (searches nested groups) |
| `editFields` | *(edit)* `[{adobeId, value}]` — rewrite a field's fieldValue in both XML+JSON (HTML rich text OK) |
| `clipartRename` | *(edit)* `{"OldName":"NewName"}` — renames XML Clipart + every ClipartImage ref; pair with assetsRemove (old pdf) + assetsAdd (new `<NewName>.pdf`) |
| `keepFields` | donor field names (JSON `field.name`) that survive a replace strip — static logos/art |
| `assetsRemove` / `assetsAdd` | zip entries to drop / local files to add |
| `stacks` | named auto-layout columns: `{x, yStart, lineHeight, width, height}` (points, x/y = frame **center**, card 252×144 + 9 bleed) |
| `variables` | `{name, type: TEXT\|DROPDOWN, required, message, default, values[], defaultIndex}` — cloned from a donor variable of the same type |
| `form` | customer-facing input order (variable display names) |
| `fields` | see below |
| `logic` | must stay `[]` — rule generation not implemented yet |

Field entries:

- **TEXT**: `{name, page, value, position{x,y,width,height} | positionFrom:"DonorFieldName" | stack:"stackName", font{name:"AUTO"|"INHERIT"|"<declared font>", size, hAlign, vAlign, colorCMYK:"c:m:y:k"}, xmlFormat{<RawTag>:<value>}}`.
  `value` = literals + `[#Variable Display Name#]` tokens. `AUTO` = first declared donor font.
- **IMAGE**: `{name, cloneFrom:"<donor image field name>", asset:"cliparts/X.pdf", replaceAsset:"<old path if ambiguous>", page, position…}`.
  Clones the donor image field and deep-swaps the asset reference.

## Notes

- Prefill (First/Last/Title/Email) is **product-level** via the Prepopulate Data
  Script — nothing in the MEX. Enable it per product per the build spec §7.
- Geometry in the current configs is first-pass; nudge frames in MegaEdit after
  import, or export the adjusted template and diff.
- Validator checks: token↔variable match, form-id↔variable-id match, XML/JSON
  field-id parity, XML/JSON text agreement, referenced assets present, no
  duplicate variable names. Exit code 2 = validation failure, nothing written.
