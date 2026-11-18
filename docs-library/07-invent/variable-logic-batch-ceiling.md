---
title: "Variable Logic in CSV batch: the architectural ceiling"
source: "hack-note"
type: "limitation"
date: "2026-05-26"
tags: [invent, variable-logic, batch, csv, megascript, editor-script, limitation, show-hide]
relevance: "high"
---

## Summary
**Invent Variable Logic cannot be made to run per record in a MegaEdit CSV batch, from either the editor or an Editor-runtime MegaScript.** Nine probes in May 2026 went from "can a script fix it?" to "the architecture rules it out". Both the batch preview and the output PDF render with record 1's logic outcome. Don't spend another week trying to build a bridge. Use the workarounds below.

Raw probe log and scripts: `experiments/invent-scripts-slot-test/` (`RESULTS.md`, `probe-*.js`).

## The mechanism
1. When the CSV is uploaded, `InDesign.Batch` pushes **record 1's** values into the Invent Variables once. Variable Logic evaluates once, on record 1, and its result (for example which background shows) holds for every record.
2. Switching records doesn't touch the Variables. It writes each record's values straight into field text (`setupRecord → _GenerateClientSidePreview → … → SetTextAsLimitedHtml`). Placeholders are text substitution, not variable assignment, so Logic never re-evaluates.
3. Each per-record preview is **rendered on the server** (`setupRecord → _requestPreview → postMessage → getPreview` XHR). The request carries the substituted text but not field state such as `hidden`, so changes an editor script makes to fields never reach the render.

## What was tried (and why each fails)
| Probe | Approach | Result |
|---|---|---|
| 2 | `Editor.Invent.Variables.Set()` after CSV upload | Does fire Logic, but only once (record 1) |
| 3–4 | `RegisterValueReplacer` / `Fabric.Modified` as a per-record hook | Replacer is one-shot; `Fabric.Modified` doesn't fire on a record switch |
| 7–8 | Re-push each record's text to `Variables.Set` on `Field.TextResorted` (fires reliably per record) | The bridge fires ~67 times; **Logic ignores programmatic sets in batch preview** |
| 9 | Skip Logic: toggle `field.hidden` + `SaveFields()` per record | Commits locally; **the server-rendered preview and the output PDF ignore it** |

## What remains
- **Server-side MegaScript at render or output time.** Not tested; probably hits the same wall. Worth a stub test only if this pattern keeps coming up (ROADMAP "Later").
- **Patching `InDesign.Batch`'s XHR construction.** Possible in principle, but it is unsupported internals that an Infigo release could break.

## Workarounds that do work
- **Image or background differs per record:** use an image field and the CSV cell syntax `AlbumName/ImageName.ext`. See `04-megaedit/csv-image-swap-album-syntax.md`.
- **Several fields shown or hidden per record:** split the CSV by case and upload each part to its own template (one product per layout variant).
- **Single-record (form) products:** Variable Logic works normally, including generated rules (`04-megaedit/two-version-dropdown-show-hide-generated.md`).

## Side findings
- The Invent **Scripts** field in Setup → Other must name an existing Admin MegaScript, which is attached automatically on MEX import. An unknown name fails the import (`Admin.Mex.UiMessages.Scripts.Normal.NotFound`; the translation key is shown raw, a minor Infigo bug).
- `Multiple placeholders found in text field, only one is supported when using validation` fires for fields such as `[#Team A#] vs. [#Team B#]`.
- To map a field to its variable at script load, parse `[#Var#]` from `field.text.data`. Read it before any record renders, because batch substitution erases the placeholders.

## Related
- `invent-variable-logic.md`: the official Variable Logic article (form-driven only)
- `logic-rules-json-schema.md`: how rules are stored in the MEX
- `04-megaedit/megaedit-batch-csv-upload.md`
