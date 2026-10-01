---
title: "Variable Logic lives in the MEX as plain JSON — logicRules[] schema (SetValue lookup table)"
source: "author-session"
type: "hack-note"
date: "2026-09-28"
tags: [invent, mex, variable-logic, logicRules, setvalue, dropdown, lookup-table, mexgen, generatable]
relevance: "high"
---

## Problem
Can a generated MEX carry the same conditional logic an Invent export does, without InDesign
in the loop? Checked against a production business-card export (Invent 2.8.x) whose
"Location Numbers" rule auto-fills Main/Fax phone dropdowns from a 48-option location dropdown.

## Root cause / finding
Yes. Invent's Variable Logic is **not** compiled into anything opaque. The whole rules engine
ships as `logicRules[]` inside the embedded JSON at
`template.xml → Resources/DataItems/Item[name=InDesignData]`. Nothing else in the MEX
references it: the XML `<VariableSet>` is empty, `<Resources><Scripts>` holds only the
stock `InDesign` editor script, and the fields carry no rule links. MegaEdit reads the
rules straight from the JSON. So generating logic = generating JSON with the right GUID
cross-references, exactly like variables and form items already are.

One rule item = one `if` branch. 47 items with identical shape:

```json
"logicRules": [{
  "id": "<GUID>", "name": "Location Numbers",
  "description": "Auto-fill of location main and fax phone numbers.",
  "invalid": false,
  "ruleItems": [{
    "id": "<GUID>", "conditionMode": "And",
    "conditions": [{
      "id": "<GUID>",
      "source": {"id": "<Location dropdown variable id>", "type": "Variable"},
      "condition": "Equals",
      "value": ["<option id inside that dropdown's values[]>"]
    }],
    "actions": [
      {"id": "<GUID>", "invalid": false,
       "target": {"id": "<Main Number variable id>", "type": "Variable"},
       "action": "SetValue",
       "value": "<option id inside Main Number's values[]>"},
      {"id": "<GUID>", "invalid": false,
       "target": {"id": "<Fax Number variable id>", "type": "Variable"},
       "action": "SetValue",
       "value": "<option id inside Fax Number's values[]>"}
    ]
  }, "... one item per location ..."],
  "defaultActions": []
}]
```

Key facts for a generator:
- `condition.value` is an **array** of option ids (Equals with one entry here); `action.value` for a
  SetValue onto a DROPDOWN is a **bare** option id. Both are ids from `variables[].values[].id`,
  never labels.
- SetValue onto a dropdown can only pick an existing option, so the Main/Fax targets are DROPDOWNs
  with one option per location (49 = 48 locations + a blank/other) — the "lookup table" is really
  three parallel dropdowns stitched by ids. That is why a phone-number fix touches the option
  label, the option value, and nothing in the rule (the rule only holds ids).
- `ruleItems` order = `if / else if` order (first match wins); `defaultActions` = the `else` branch.
- `conditionMode` is `And` / `Some` / `Any`; verbs seen across exports: `SetValue`, `SetText`,
  `SetImage`, `Show`, `Hide`, `SetFontColor`, `SetBarcodeFontColor`. Targets are
  `{"type":"Variable"}` or `{"type":"Field"}` (field ids are the zero-padded adobeId form).
- Every `id` is a random GUID-shaped string; only the cross-references must line up.

## Fix
`mexgen build` currently refuses any config with `logic` populated (`check_logic` in
`mexgen/mexgen.py`, plan Phase 6). Implementing it is a JSON emit plus validation:
resolve `{when: {var, equals: label}, set: {var: label, ...}}` to ids, mint GUIDs, append to
`logicRules[]`, and check every referenced variable/option/field id exists. Import into
MegaEdit on a throwaway product to confirm, as with every other generated part.

Done once already (2026-09-28, local `Claude outputs/location-dropdowns/tools/build_location_mex.py`,
gitignored because it carries customer data): donor MEX + three Label/Value CSVs → new revision with
the three dropdowns, the text library and the 48-branch rule rebuilt. Existing option/branch ids are
reused by label so the JSON diff against the donor is only the rows that changed; the resulting file
was byte-identical to the donor outside the JSON blob. Note the address frame binds to the dropdown
by variable id (`textValue: {type: "VARIABLE", value: {value: <variableId>}}`), not by token, so a
rebuilt option list needs no field edits.

## Sample
Decoded first branch of the production rule: IF `Location Addresses` Equals `Location A` THEN
SetValue `Main Number` = option "(555) 010-0100", SetValue `Fax Number` = option "" (blank).

## Caveats
- Form-driven only: rules fire on a form change in the editor and **not** on CSV batch upload
  (see [[invent-variable-logic]]). A lookup-table rule is therefore useless for batch; derive the
  columns before upload instead.
- Because the location data is encoded three times (location dropdown, Main dropdown, Fax
  dropdown) plus the rule, a data edit is four coordinated JSON edits. Generating from one
  CSV of `location,main,fax` removes the hand-sync errors seen in the live file (wrong-city
  numbers, trailing spaces, corrupted en dash).
- Only `Equals` on a single option was observed for dropdown sources; `Contains` and friends are
  documented for TEXT sources but their JSON shape (probably a literal string in `value[]`) is
  unverified.

## Related
[[mex-file-format-anatomy]] [[invent-variable-logic]] [[conditional-businesscard-template-pattern]]
