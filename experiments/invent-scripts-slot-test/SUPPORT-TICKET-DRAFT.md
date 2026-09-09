# Infigo Support Ticket — Draft

**Subject:** MegaScript API for Invent field-to-variable linkage + CSV batch + Variable Logic bridge

**Context paragraph (paste at top):**

I'm building an editor-runtime MegaScript (`@infigo-official/types-for-megaedit`, ExecutionType: Editor) to bridge MegaEdit CSV batch upload → Invent Variable Logic. Empirical testing has confirmed the architectural gap: `InDesign.Batch` writes CSV values directly into field text via `FieldHandlers.SetTextAsLimitedHtml` and never calls `Editor.Invent.Variables.Set()` per record, so Variable Logic only evaluates against record 1's values and conditional artwork (e.g., "First Name contains '?' → swap background") doesn't re-fire per record. I have `Editor.Invent.Variables.Set()` working, `Fabric.Modified` firing reliably once per record switch, and the script auto-attaching via Invent → Setup → Other → Scripts. The remaining block is identifying which text field corresponds to which Invent Variable.

---

## The five questions

**1. Field → Variable linkage: what is the supported MegaScript API?**
All seven text fields on our Invent-exported product have empty `name=""` properties, so `Job.Fields.ByName('First Name')` returns nothing. Stack traces during batch preview show Invent's internal `getVariableLinkedToFields` method resolving the linkage during `InDesign.Batch` rendering. Is there a public MegaScript API (in `types-for-megaedit` v1.0.19 or later) that exposes the field→variable mapping at runtime? If not, what is the supported identifier path for a script that needs to read "the text field bound to Invent Variable X"?

**2. Tags or CustomData as the supported identifier?**
`Job.Fields.ByTags()` and a `CustomData` property both exist in the type definitions. Does Invent populate either of these on export so a MegaScript can resolve linkage? If yes, what is the convention (variable name as tag? CustomData key?). If no, which attribute is the intended hook?

**3. Is `getVariableLinkedToFields` (or equivalent) callable from a custom MegaScript?**
The method clearly exists in `InDesign.Batch`. Is it surfaced through `Editor.Invent`, `Job.Fields`, or any other public namespace? If it's internal-only, is there an alternative we should call instead, or is exposing it a roadmap item?

**4. Hardcoded Scripts slot — permission model?**
The Invent Setup → Hardcoded Scripts field accepts the name of an Infigo-built script and validates on MEX import. Which roles/permissions can reference hardcoded scripts? Does a storefront admin need Customer Support permission, or is this an Infigo-internal slot? A list of available Hardcoded script names would help us evaluate whether one of them already does what our bridge attempts.

**5. Two side bugs surfaced during testing:**
   - `Admin.Mex.UiMessages.Scripts.Normal.NotFound` ships as raw translation key (not localized English) when an Invent Scripts slot references a non-existent custom script. The Hardcoded equivalent is fully localized. Missing string in the language table.
   - `Multiple placeholders found in text field, only one is supported when using validation` fires constantly from `InDesign.Batch:2249` `getVariableLinkedToFields` during batch preview. Is this a real limitation (one placeholder per text field when validation is on) or a stale check we should ignore? It surfaces on every record switch.

---

## Attachments to consider including

- `RESULTS.md` (Phase 0–3 empirical findings — gives them the architectural context fast)
- A short Loom or annotated screenshot of the CSV batch preview showing the background not swapping per record
- The console transcript showing `[PROBE 2] Variable updated:` firing exactly 6 times on CSV upload then never again

## Tone note

Polite, technical, reads like a developer talking to a developer. We've done the homework — they should be able to answer (1) and (2) in one sentence each if the API exists.
