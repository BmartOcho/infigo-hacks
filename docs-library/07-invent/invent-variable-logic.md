---
title: "Variable Logic (Invent v2.0)"
source: "infigo-academy"
url: "https://academy.infigo.net/academy/p/1544/variable-logic"
type: "tutorial"
date: "2023-05-17"
tags: [invent, variable-logic, conditional-rules, if-else, show-hide, set-value, form-driven, batch-gap]
relevance: "high"
---

## Summary
Invent v2.0's conditional-rules engine. A **Rule** is a named collection of `Condition + Action` blocks with `if / else if / else` flow. Conditions evaluate against Invent **Variables**; Actions target Invent Variables or Fields. Three action types: **Set Value**, **Show**, **Hide**. Works as a true rules engine — multiple conditions per statement (ALL / ANY / SOME), multiple else-ifs, optional catch-all else.

**⚠️ Load-bearing limitation:** Variable Logic is form-driven — it fires when a user changes a variable's value through the MegaEdit form UI. **It does NOT fire when MegaEdit's CSV batch upload populates placeholders.** CSV batch substitution writes directly into MegaEdit placeholders, bypassing Invent Variables entirely. Confirmed empirically by the author (May 2026): a rule "if First Name contains '?', show Background B" works perfectly in single-record form mode but fails on CSV batch upload — the "?" renders as literal text and the background does not swap. See `experiments/invent-scripts-slot-test/RESULTS.md`.

## Key takeaways

### Structure
- **Rule** = Name + optional Description + at least one `if` block.
- **Condition** = Variable + comparison operator + value, OR `Always`, OR `Never`.
- **Action** = target (Variable or Field) + action type (Set Value / Show / Hide) + value (for Set Value).
- Max **10 Conditions per Rule**, max **50 Actions per Rule**.
- `else if` chain: ordered, first-match wins.
- `else` (catch-all): Actions only, no Condition.

### Condition operators
- `Equals`, `Does not equal`, `Contains`, `Does not contain`, etc.
- For multi-condition statements: All / Some / Any join modes.

### Action types
| Action | Effect |
|---|---|
| Set Value | Override target Variable's or Field's value |
| Show | Make target visible (variable in form, field on canvas) |
| Hide | Make target invisible |

### Canonical use case (from doc)
Dual-brand business card: if `Dual Branding` variable = `No` → Hide `Logos 2` variable + Hide `Logo 2 image` field. `else` → Show both. Same pattern works for swapping backgrounds, alt logos, optional address blocks, conditional disclaimers, etc.

### Setup flow
1. Create Invent Variables first (Variables tab).
2. Variables tab → `Setup Logic` button → `Add Logic`.
3. Name + description → `Add Condition` → pick Variable + operator + value.
4. `Add Action` → pick target (Variable or Field) + action type.
5. Repeat for `else if` chain; add `else` for catch-all.
6. Save → export MEX → import into MegaEdit. Logic ships baked in.

### What it CANNOT do (as of May 2026)
- Fire on CSV batch upload (placeholders bypass Variables).
- Reach external assets — can only Show/Hide/Set fields and variables already defined in the InDesign file.
- Conditional access to MegaScripts or external services.

## Code / config snippets
Logical sketch of a typical rule:
```
Rule: "First Name fallback background"
  if  First Name Contains "?"
      → Hide Background_A_field
      → Show Background_B_field
  else
      → Show Background_A_field
      → Hide Background_B_field
```

## Related
[[invent-setup-tab]]
[[invent-overview]]
[[megaedit-batch-csv-upload]]
`experiments/invent-scripts-slot-test/RESULTS.md` (probe results for the Variable Logic + CSV batch gap)
