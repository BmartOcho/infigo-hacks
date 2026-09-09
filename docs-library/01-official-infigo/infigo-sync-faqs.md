---
title: "Infigo Sync FAQs"
source: "infigo-academy"
url: "https://academy.infigo.net/p/1818/infigo-sync-faqs"
type: "article"
date: "unknown"
tags: [infigo-sync, hotfolder, output, filename, status-update, windows, admin]
relevance: "high"
---

## Summary
Infigo Sync (formerly Catfish Sync) is the Windows-based downloader that polls Infigo every 30s for print-ready PDFs, job tickets, invoices, packing slips and XML outputs and drops them in a local folder. Covers the critical filename prefix pattern required for SPO status updates, polling cadence, install/network requirements, error log locations, and the "must start with %TypeLetter%_%OrderID%_%JobID%_" rule (NOT the order shown in older docs).

## Key takeaways
- Default poll interval is **30 seconds** — this is the MINIMUM (configurable upward only) to avoid platform load.
- Sync downloads ALL files in the storefront hotfolder regardless of filename. Filename only determines whether Shared Print Operations (SPO) status updates happen.
- **CRITICAL filename rule for SPO status updates** — filename MUST start with:
  ```
  %TypeLetter%_%OrderID%_%JobID%_
  ```
  (This corrects an older doc that said `JobType_OrderID_JobID_` is sufficient — in practice it must START with these tokens in this exact order.)
- Examples that update status: `P_12345_98765_output.pdf`, `P_12345_98765_Final.pdf`
- Examples that do NOT update status: `Output_12345_98765_P.pdf`, `%TypeLetter%_%JobID%_%OrderID%_…` (wrong order)
- Additional tokens (ProductName, CheckoutAt, timestamps) can be appended AFTER the required prefix.
- Hotfolders support sub-folder routing based on product, customer location, or other criteria. **Only ONE level of sub-folders is supported**.
- Multiple Sync instances pointing at the same machine require SEPARATE Storefront API keys.
- macOS supported only via Windows VM (e.g. Parallels). Sync runs only while the VM is active.
- Install premature-end errors usually = antivirus / Windows Security / firewall interference. Try running MSI as administrator.
- Default error folder: `C:\InfigoSyncUpload` — contains PDFs Sync failed to upload.
- Error log: `infigosync.log` in `C:\Program Files (x86)\[companyreference]\InfigoSync`
- Config file: `InfigoSync.exe.config` (same directory as log).
- Local-file security errors usually = Sync service running as `System` rather than a specific user account; switch to user account for proper file permissions.
- Check job hotfolder routing in Shared Print Operations > job entry > Print Location / Hotfolders.

## Code / config snippets

### Filename template for status-update compatibility
```
%TypeLetter%_%OrderID%_%JobID%_<anything>
```

### Common file paths
```
Error folder:       C:\InfigoSyncUpload
Log file:           C:\Program Files (x86)\[companyref]\InfigoSync\infigosync.log
Config file:        C:\Program Files (x86)\[companyref]\InfigoSync\InfigoSync.exe.config
```

## Related
[[infigo-sync-install]]
