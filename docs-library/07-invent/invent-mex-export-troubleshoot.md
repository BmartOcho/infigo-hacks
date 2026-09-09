---
title: "Why Is My MEX File Not Exporting in Infigo Invent Plugin?"
source: "infigo-academy"
url: "https://academy.infigo.net/academy/p/2017/why-is-my-mex-file-not-exporting-in-infigo-invent-plugin"
type: "article"
date: "unknown"
tags: [invent, export, mex, troubleshooting, onedrive, dropbox, cloud-sync, known-limitation]
relevance: "medium"
---

## Summary
Most common cause of "export succeeded but no file appears": the target folder is cloud-synced (OneDrive, Dropbox, Google Drive). Cloud-sync agents interfere with the file-writing process and silently swallow the output. Fix = export to a purely local directory (e.g. `C:\Users\[user]\Downloads`), then move/sync the file manually afterward.

## Key takeaways
- Symptom: Invent reports "saved" but the MEX file doesn't appear in the chosen folder.
- Root cause: cloud-synced folders disrupt Invent's file-writing.
- Fix: pick a non-synced local folder (e.g., Downloads).
- Acknowledged by Infigo as a known limitation; future-update fix flagged but not delivered as of the article.
- If still failing after switching to a local folder: check Invent + InDesign are on latest versions.

## Related
[[invent-export-package]]
[[invent-faqs]]
