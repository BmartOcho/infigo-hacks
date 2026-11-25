# Static Text Next to a CSV Placeholder Can't Be Removed by the Customer

**Tags:** megaedit, csv, batch, placeholder, template, static-text, vdp, flexibility

## Problem
A CSV name-badge product printed a game line as "<opponent> vs. <home team>". The customer needed badges for events with a different home team, or no matchup at all. Deleting the home team (from the CSV and from the proof) still printed "vs. <HOME TEAM>" on every badge.

## Root cause
The text field held a placeholder plus fixed text in one string:

```xml
<Text isRichText="true"><![CDATA[[#Visiting Team#] vs. HOMETEAM]]></Text>
```

A CSV batch fills in only the `[#Column#]` tokens on each row. Everything else in the field is part of the template and prints on every record. Neither the CSV nor an edit in the editor can change it. Only a new template can.

## Fix
Build a **new product**, because replacing the template breaks reorders of the old one. In it, the field is a single free-text placeholder, and the customer types the whole line:

| Where (template.xml) | Old | New |
|---|---|---|
| Variable `name` / `dynamicName` | `Visiting Team` / `Visiting_Team` | `Matchup` / `Matchup` |
| Form item `label` | `Visiting Team` | `Matchup` |
| Field `fieldValue` (JSON, one per page) | `[#Visiting Team#] vs. HOMETEAM` | `[#Matchup#]` |
| Field `<Text>` CDATA (XML, one per page) | `[#Visiting Team#] vs. HOMETEAM` | `[#Matchup#]` |

Rename every occurrence together. The build script should assert the expected count of each before it writes the file. Leave all other parts of the MEX byte-identical. The field already had `FitTextToBox` (no wrap), so a longer line just shrinks to fit.

## Sample
CSV header: `First Name,Last Name,Dealership Name,Event Date,Matchup`. Rows can say `Big 12 Championship` or `Texas Tech vs. BYU`. Import-verified 2026-11-25: the site PDF put the line at the original position and font, and the product's own "sample CSV" download showed the new header.

## Caveats
- The line prints in the case the customer types. Forcing `TextCase uppercase` would also uppercase "vs.".
- Check the **background PDF** for other per-event text, such as a venue baked into the art. It isn't a field, so the CSV can't change it either. Making it variable means stripping the text from the background and adding a column.
- Audit for this pattern when building any CSV product: a field mixing `[#...#]` with literal words is a future change request waiting to happen.
