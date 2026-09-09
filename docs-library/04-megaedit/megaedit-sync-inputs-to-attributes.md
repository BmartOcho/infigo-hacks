---
title: "Sync MegaEdit Inputs to Product Attributes"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2376/sync-megaedit-inputs-to-product-attributes"
type: "tutorial"
date: "unknown"
tags: [megaedit, invent, product-attributes, sync, tags, save-to-attribute, hardcoded-script]
relevance: "high"
---

## Summary
A hardcoded script (`Product Attribute Sync Script`) that maps any MegaEdit form field (text, image, custom) directly into a corresponding product attribute on the order line. Activated at the MegaEdit Scripts screen, enabled per-product on Scripts tab, and triggered by tagging the field in MegaEdit with `save to attribute_<attribute name>` exactly matching the attribute name on the product. Same `save to attribute_` tag pattern works in Invent.

## Key takeaways
- Script is hardcoded — find it at the bottom of `Admin > MegaEdit Scripts`. If you can't see it, log in as platform admin or ask support to activate it.
- Enable per-product on the MegaEdit product's Scripts tab and save.
- Add a matching Product Attribute to the product on the Product Variant settings.
- In the MegaEdit editor, open the field's properties > Details tab > **Tags** field. Enter: `save to attribute_<Exact Attribute Name>`.
- When customer clicks Add to Basket, the field's value is transferred to the matching attribute on the order line.
- Works for:
  - Text fields (string value, respects formatting constraints)
  - Image fields (uploaded asset reference or URL)
  - Custom fields (with specialized extraction logic)
- For dropdown / radio attributes, the script looks up the matching option ID. For free-text attributes, raw value is assigned.
- Invent: set up a variable linked to the text field. On the text field's General tab, use the same `save to attribute_<name>` tag. Export as MEX into MegaEdit — same behavior.
- Does not modify existing functionality — must be explicitly enabled.

## Code / config snippets
Tag syntax on a field's Details tab:
```
save to attribute_<Exact Attribute Name>
```

Example:
```
save to attribute_Example Attribute
```

## Related
[[megaedit-batch-csv-upload]]
[[megaedit-scripts-config]]
