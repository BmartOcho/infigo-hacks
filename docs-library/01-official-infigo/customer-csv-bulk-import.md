---
title: "Customer CSV Bulk Import"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1606/customer-csv-bulk-import"
type: "article"
date: "2023-08-08"
tags: [customers, csv, bulk-import, admin, departments, regions, troubleshooting]
relevance: "high"
---

## Summary
Bulk customer creation/update via CSV upload. Path: Customers > Customer Management > "CSV import" tab. Same column headers as the in-app create-customer form; the import validates row-by-row, creates new customers if no match, otherwise updates the matching customer (matched by email or username depending on settings).

## Key takeaways
- Location: **Customers > Customer Management > CSV import tab**.
- The CSV import page itself includes column descriptions, examples, and a downloadable sample template at the bottom.
- **Column headers are case-sensitive and must match the table exactly.**
- **Configuration dependencies** affecting valid columns / required fields:
  - **Usernames** setting (Configuration > Settings > Customer Settings): if DISABLED, Approver1/2/3 columns must use full email addresses (not usernames).
  - **Registration form** required fields: every field marked required in the Registration tab MUST be present in the CSV.
- **Departments** in the CSV must already exist on the platform and the name (case + format) must match exactly. Otherwise import fails for that row.
- **County / Region** values must exist on the system before import. See related doc on adding counties/regions.
- Match logic: by email or username depending on "Usernames" setting. Match found → update; no match → create.
- Error CSV is generated post-import listing failed rows + reason.
- **Password gotcha:** double-quote characters in passwords break CSV parsing. Escape with double-double-quotes inside outer double-quotes — e.g. `test"*2` → CSV value `"test""*2"`. Easier: use a different special character.

## Related
[[customer-budget-csv-import]]
