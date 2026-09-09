---
title: "Configuring MegaEdit scripts on a product or global level | ME_026"
source: "infigo-academy"
url: "https://academy.infigo.net/p/661/configuring-megaedit-scripts-on-a-product-or-global-level-me_026"
type: "tutorial"
date: "2023-07-26"
tags: [megaedit, scripts, custom-scripts, hardcoded-scripts, global-config, product-config]
relevance: "high"
---

## Summary
How to create custom MegaEdit scripts and apply config at two levels: per-product (only affects that MegaEdit product) or global per-script per-storefront (affects every product using that script on the active storefront). Hard-coded Infigo scripts can also be modified, but access must be requested from support.

## Key takeaways
- Create custom scripts at `Admin > MegaEdit Scripts > Create`.
- Per-product config: open the MegaEdit product > Scripts tab > check the script's box and Save > then click `Configure` on the script row.
- Global config: `MegaEdit Scripts` screen > `Global Config` button on the script row. Changes affect ALL products on the **active storefront** using that script.
- Permissions: most admins see only Custom MegaEdit Scripts. Hardcoded/Infigo-provided scripts require additional permissions — contact Customer Support to enable.
- Permissions also apply for editing hardcoded scripts globally.
- Script settings live as JSON in the configuration boxes (visible on the per-product and global config screens).
- **ExecutionType dropdown** on the Create/Edit script screen — load-bearing, controls which runtime API set the script has access to: `Editor` (browser editor; uses `@infigo-official/types-for-megaedit`), `Server Side` (uses `@infigo-official/types-for-megascript` — DynamicProduct, Run object, cron-capable), `Editor and Server Side`, `Price` (pricing scripts; `@infigo-official/types-for-pricing-script`), `Output Creation` (runs during PDF/output generation), `Editor and Server Side and Output Creation`, `Editor and Server Side and optional Output Creation`. Editor and Server Side use entirely different API surfaces — picking the wrong type means the script can't see the objects it needs.
- **Enabled checkbox** must be ticked or the script won't run even if attached to a product.
- **Execution time (seconds)** is a per-execution timeout limit.
- Empirical: Admin screen is titled "Create MegaEdit Product Script" — the menu/path may show as "MegaEdit Product Scripts" rather than the shorter "MegaEdit Scripts" referenced in some Academy docs.

## Related
[[megaedit-batch-csv-upload]]
[[megaedit-barcodes]]
[[megaedit-sync-inputs-to-attributes]]
[[megascripts-types-documentation]]
