---
title: "MEX File Format — Reverse-Engineered Anatomy"
source: "author-session"
type: "reference"
date: "2026-07-01"
tags: [invent, mex, file-format, zip, template-xml, indesigndata, json, generatability, reverse-engineered]
relevance: "high"
---

## Summary
Direct inspection of a real exported MEX (`INFIGO_Example BC_v-01.mex`, Invent pluginVersion 2.8.5, a 3.5x2" business card). A .MEX is a **plain ZIP** (compression = store, no manifest, no checksum, no signature). Verified round-trip: rebuilt the zip from its extracted parts → byte-identical size, valid archive. Everything semantic is human-readable text. **Conclusion: the format is script-generatable — templating is easy, from-scratch is doable for simple layouts with an import-test loop.**

## Container
```
backgrounds/            (folder)
backgrounds/background_1.pdf   front background, 270x162 pt
backgrounds/background_2.pdf   back background,  270x162 pt
cliparts/               (folder)
cliparts/Regional_back.pdf  ~10 MB embedded PDF
cliparts/Field_back.pdf       ~10 MB embedded PDF
template.xml            24 KB — ALL structure lives here
```
No manifest/hash file → nothing enforces integrity, so hand-edits repackage cleanly. File weight is 99% the embedded PDF assets (produced by InDesign export).

## template.xml tree
```
<Document pluginVersion="2.8.5">
  <Config>    Product, Content, Constraints, Appearance, Behaviour
  <Resources> Cliparts, Fonts, Backgrounds, Variables, SpotColors, DataItems, Scripts
  <Pages>     Page x2
```
- `Resources/Variables/VariableSet name="Default" scope="SHOPPING_SESSION"` — thin; the rich model is in the JSON below.
- `Resources/Scripts/Script name="InDesign" hardcoded="true" target="editor"`.
- `Pages/Page` attribs: `height=144 width=252 bleed=9 type=single` (points). Each has `<Background>` + `<Content>` with `<Field>` elements carrying `<Position>` + `<Information><Id>` + `CustomData.originalFieldId`.

## The real model: `Resources/DataItems/Item name="InDesignData"` (embedded JSON)
Top-level keys: `resources, variables[], forms, layouts, pages[], groups, fields[], logicRules[], config, pageType`.

**variables[]** — e.g.
```
{name:"Which Example Group?", dynamicName:"Which_Example_Group", type:"DROPDOWN",
 validation:{required:{enabled:true, message:"Please Select One"}},
 values:[{id,label:"Regional",value:"Regional"},{...,"Field"}], defaultValue:0}
{name:"First Name", dynamicName:"First_Name", type:"TEXT", ...}   # + Last Name, Title
```
Types seen: `DROPDOWN`, `TEXT`. Required lives at `validation.required.{enabled,message}`.

**fields[]** — placed frames:
```
{id:GUID, adobeId:234, layer:204, page:1,
 position:{x:126, y:72, width:269, height:161, angle:0},
 type:"IMAGE", image:{...}, field:{name,visible,placeholder,tags[],constraints{...}}}
```
- Coordinates are **points**; `x,y` is the frame **CENTER** (126,72 = center of a 252x144 page).
- `adobeId`/`layer` tie back to the InDesign document.

**logicRules[]** — Variable Logic (this is the conditional engine):
```
Rule "background selection":
  ruleItem(And): IF  {source:{id:<variableGUID>, type:"Variable"}, condition:"Equals", value:[<valueGUID>]}
                 THEN {target:{id:<fieldGUID>, type:"Field"}, action:"SetImage"}
  ruleItem(And): IF group Equals Field → SetImage(back field) = Field
```
Conditions reference a variable GUID + operator + value GUID; actions target a field GUID with a verb (`SetImage`, and presumably Show/Hide/SetValue per invent-variable-logic.md).

**forms.pages[].form[]** — the customer-facing field order: `{id, type:"ITEM", label}` list (dropdown, First, Last, Title).

**config.batch** — CSV/batch options (mode, uploadCsv, records, mapping).

## Generatability verdict
- **Template-and-modify: high confidence.** Plain zip + declarative JSON/XML. A generator can rewrite variables/fields/logic/forms and swap PDF assets from a config, then repack. Best path.
- **From-scratch: feasible for simple cards, needs a test-import loop.** Three catches:
  1. **Dual representation** — layout is stored in BOTH `template.xml` (Pages/Content/Field) AND `InDesignData.fields[]`; a generator must keep them consistent (linked by field GUID / originalFieldId / adobeId).
  2. **Geometry originates from InDesign** — new frames need correct point coords (x/y = center, +bleed). Computable for grid layouts; fiddly otherwise.
  3. **Import validation is invisible** until you actually import into MegaEdit — expect to iterate.
- GUID minting + cross-referencing (variable↔logic↔field↔value) is trivial programmatically but must be exact.

## Text fields & variable binding — CONFIRMED (2026-07-01, follow-up export + Claude round-trip)
**Binding = a token string, not an id link.** A text field's content is `[#Variable Display Name#]` (DISPLAY name, spaces allowed; multiple tokens + literals OK, e.g. `[#First Name#] [#Last Name#]`). It appears in TWO places that must agree:
- JSON: `field.fieldValue = "[#First Name#] [#Last Name#]"`
- XML: `<Data><Text isRichText="true"><![CDATA[[#First Name#] [#Last Name#]]]></Text>`
Type into the matching form input → the token renders live. There is NO field↔variable GUID binding; logic actions (SetImage/…) are a separate mechanism.

**Text field JSON** (`type:"TEXT"`): id, adobeId, layer, page, position{x,y,w,h,angle} (decimals fine), `fieldValue` (token), `text{format{textColor CMYK, fontSize{type:"INHERIT"|"VALUE",value}, font{type:"INHERIT"}}, options{textMode:"NORMAL", fieldGrowType:"FIXED", fitToBox, renderMode}, suppression}`, generic `field{name,visible,placeholder,tags,constraints{allowSelection:true,...}}`.

**Text field XML** `<Field type="text">`: `<Position/>` + `<Data><Text isRichText="true"><![CDATA[<token>]]></Text><Format><Font name=".." category="Standard" isBold/isItalic/><FontSize/><HorizontalAlignment/><VerticalAlignment/><CharSpacing/><Leading/><TextColor>c:m:y:k</TextColor><FitTextToBox/><FieldGrowType/><TextType/><RenderMode/></Format><Constraints><TextMode>normal</TextMode></Constraints></Data><Information><Id/><Name/><Visible/><CustomData originalFieldId/><FieldConfiguration/></Information>`.

**Variables live in JSON only** (`variables[]`); XML `<VariableSet>` stays empty. Show one as a form input via `forms.pages[0].form[] += {id:<variableId>, type:"ITEM", label:<name>}` — **the form ITEM id == the variable id**. TEXT variable: {id,name,dynamicName(spaces→_),type:"TEXT",mode:"SINGLE",validation{min/max chars+lines,regex},prepopulation{mode:"Nothing"|account-source},defaultValue}.

**Fonts:** `<Resources><Fonts><Category name="Standard"><Font name=".." isBuiltIn="false"><Normal><Print><BinaryReference mode="external">./fonts/X.otf</BinaryReference>…`. JSON `resources.Font` may be `[]`; a field's JSON font can be `INHERIT` while its XML `<Format><Font name=..>` names a declared font. To add a text field, reuse an existing declared font by name — no new asset needed.

**Generation proven:** Claude programmatically injected new variables (Phone, Email) + form items + bound text fields (`[#Phone#]`,`[#Email#]`) into BOTH representations, minted matching GUIDs/adobeIds, and repacked a valid MEX (`v-04`). ⇒ a config-driven MEX generator is viable. (Live-populate on import CONFIRMED 2026-07-01 — v-04's Claude-generated Phone/Email fields rendered from form input in MegaEdit. Full chain — image fields, text fields, variables, form inputs, live token binding — is now generatable programmatically.)

## Additional conventions — CONFIRMED (2026-07-01, mexgen build session, v-01 ground truth)
- **Field ids are zero-padded adobeIds**, not random GUIDs: `00000000-0000-0000-0000-000000000300` for adobeId 300. XML `Information/Id` == JSON `fields[].id` == `originalFieldId`. Variables, dropdown values, and logic rules DO use random-GUID-style ids.
- **JSON `fields[].page` is 0-BASED**; XML `<Pages>` document order supplies the mapping (JSON page 0 = first XML `<Page>`).
- **`Information/CustomData` is a JSON text blob** — `{"originalFieldId": "<id>"}` — not an XML attribute.
- **XML `<FontSize>` is authoritative** (`8`, `12`); the JSON `text.format.fontSize` stays `{"type":"INHERIT","value":12}` even when XML carries the real size.
- **Image fields can ship with `imageValue.type: "NONE"`** — v-01's back art was applied at runtime by Variable Logic `SetImage` with value `{value:<clipartItemId>, resourceSet:<clipartSetId>, option:"RESOURCE"}`, referencing `resources.Clipart[].items[]` (JSON) / `Resources/Cliparts/Category/Clipart` + `BinaryReference` (XML).
- **Art pinning without logic (verified-safe path):** byte-swap a background PDF's zip entry with the desired art instead of guessing `imageValue` shapes — backgrounds (`Pages/Page/Background` → `Resources/Backgrounds` → `./backgrounds/*.pdf`) are a proven render path. Used for the the client two-product split (each product's `background_2.pdf` = its division's back art; image field + rule stripped).
- **Removing assets requires pruning their XML/JSON resource declarations** (dangling `BinaryReference` entries risk import failure).
- Tooling: `mexgen/mexgen.py` (inspect/build/validate) encodes all of the above; both example v-05 products generated + structurally verified with it.

## Advanced features — harvested 2026-07-02 from production files
Sources: `INFIGO_Example Field BC_v-01.mex` (new BASELINE, production Field card) and `INFIGO_Event Flyer-English_02.mex` (complex retail event flyer, 17 logic rules). Dumps: `mexgen/dump-living-baseline/`, `mexgen/dump-event-flyer/`.

### Rich text (inline HTML in fieldValue)
`fieldValue` accepts HTML: `<br />` line breaks, `<span style="font-family:Body Font;font-size:8">…</span>` inline restyling, HTML entities (`&#x201C;`). Tokens mix freely with markup:
`[#Location Name#]<br /><span style="font-family:...;font-size:8">[#Address#]<br />[#City#], [#State#] [#Zip code#]</span>`
Same string sits in the XML CDATA. This is how one field carries a multi-size text block.

### fitToBox (JSON shape)
`text.options.fitToBox = {enabled: true, wrapping: true, limits: {enabled, max, min}}` with `fieldGrowType: "FIXED"`. XML twin: `<FitTextToBox enabled withWrap minFontSize maxFontSize>`. The baseline's stacked blocks use fit+wrap with limits disabled.

### BARCODE fields (type:"BARCODE")
`barcode: {type:"QR", value: {type:"VARIABLE", value:"[#URL#]", variableId:<GUID>, format:{type:"STANDARD"}}, size:{auto:true,...}, color/backgroundColor (CMYK), hri, quietZone, checksum, encoding:"ASCII", rectangular:false}`. NOTE: binding uses BOTH the token string AND the variableId. Logic verb `SetBarcodeFontColor` exists.

### Parent-linked variables = conditional form fields WITHOUT logic rules
`variable.parent = {enabled: true, variableId: <controlling dropdown>, value: [<valueIds that reveal it>]}` — e.g. "Custom Title" appears only when "Flyer Title" == "Custom". Declarative show/hide of FORM INPUTS; no Variable Logic involved, so no fire-on-change-vs-load concern. (Field visibility on the CANVAS still needs Show/Hide rules.)

### Form GROUPs (nested)
`forms.pages[0].form[]` items can be `{type:"GROUP", id, label, items:[...]}` with nested ITEMs/GROUPs. Inside groups, items reference variables via **`variableID`** (capital D) + `name`; top-level ITEMs use plain `id`. Top-level JSON `groups` stays `[]`.

### IMAGE variables (customer-swappable images as form inputs)
`type:"IMAGE"` variable: `control{standardFit:"NOCROP", transformation{translate,rotate,scale}, mask}`, `defaultValue{value, resourceSet}`, `source{allowUpload, allowMediaAlbums, allowAllClipartAlbums, allowClipartResourceSets{<setId>:bool}, clipartFilter, fileType}`. Used for icons/vendor logos; pairs with parent-linking to reveal 1..N logo slots.

### DATE variables
`type:"DATE"`: `constraints{min,max,weekdays{...}}`, `format{value:"MMM dd", option:"CUSTOM"}`, `relativeDate:true`, numeric `defaultValue` (relative days).

### Logic action verbs (observed)
`SetImage` (BC v-01), `Show`/`Hide` (53/16 in flyer), `SetText`, `SetFontColor`, `SetBarcodeFontColor`; rules may carry `defaultActions`. Layout VARIANTS (1/2/3-column icon sets) = parallel field groups named `1A-*/2A-*/3A-*` toggled by Show/Hide rules from an "Icon Sets" dropdown.

### Baseline anomaly (flag)
The production Field BC baseline still contains the "Which Example Group?" dropdown, BOTH back cliparts, and the background-selection rule with **empty actions[]** — and the back IMAGE field has `imageValue.type:"NONE"`. Either MegaEdit stripped the actions on export or they were removed manually; the back art binding must be re-checked before generating from this donor.

## Related
[[invent-variable-logic]]
[[invent-export-package]]
[[conditional-businesscard-template-pattern]]
