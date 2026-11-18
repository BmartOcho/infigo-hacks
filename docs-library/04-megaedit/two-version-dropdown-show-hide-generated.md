---
title: "Two art versions in one MegaEdit product — dropdown + Show/Hide, generated without Invent"
source: "author-session"
type: "hack-note"
date: "2026-11-16"
tags: [megaedit, mex, logicRules, dropdown, show-hide, clipart, versions, parent-variable, mexgen, generated]
relevance: "high"
---

## Problem
Customer wants one postcard product with two full art versions (front and back both differ),
picked from a dropdown in the editor, with shared editable address lines and a contact line
that only exists on one version. Static PDF + "Version" attribute can't swap art
(see `thankyoucard-two-version-build-spec.md`), and two products wasn't what was asked.

## Root cause / constraints
- Page backgrounds are fixed per page; logic can't swap them.
- `mexgen build` refuses `logic` (Phase 6), so the rule is emitted directly in the build script.

## Fix
- Version A art = page backgrounds. Version B art = full-bleed **static clipart image fields**
  (`<ClipartImage name>` in XML, JSON `imageValue: NONE`, JSON `resources.Clipart` stays `[]` —
  same as a live 2.4.4 export) layered over them, resting `visible:false` (JSON `field.visible`
  and XML `Information/Visible`).
- `DROPDOWN` variable, `mode: "VALUE"`, `resourceSet: null`, `defaultValue` = option id.
- One rule: `ruleItems[0]` IF dropdown Equals [offer option id] → `Show` each B field;
  `defaultActions` (ruleItem shape, `conditions: []`) → `Hide` the same fields.
  Action shape `{id, invalid:false, target:{id:<padded field id>, type:"Field"}, action, value:""}`
  copied from a 2.4.1 production export (event flyer icon-set rules).
- Inputs only meaningful on version B use `parent: {enabled:true, variableId:<dropdown>,
  value:[<option id>]}` so they only appear in the form when it's selected.
- Shared text fields appended after the B back image so they stack above it.

## Sample
Build kit: job folder `Working\mexbuild\` (`prep_art.py` normalises + redacts the variable
runs, `build_mex.py . <name>.mex`). `mexgen validate --strict`: 0/0.

## Caveats
- **Not yet import-tested** (2026-11-16; extended to 3 versions with a second ruleItem the same day — the ELSE-IF pattern from the event-flyer export). First generated logic rule on this storefront — check
  that switching the dropdown toggles both pages and that hidden fields stay out of the print PDF.
- Resting `visible:false` covers the default even if rules don't fire on load (unconfirmed, SPEC §18).
- Logic is form-driven only — no CSV batch on this product.

## Related
[[logic-rules-json-schema]] [[conditional-businesscard-template-pattern]]
