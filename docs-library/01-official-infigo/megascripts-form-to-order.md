---
title: "MegaScripts: Form-to-Order Automation"
source: "infigo-academy"
url: "https://academy.infigo.net/p/2706"
type: "article"
date: "unknown"
tags: [megascripts, automation, api, order-creation, form, customer-creation, integration]
relevance: "high"
---

## Summary
MegaScript pattern that turns an HTML form submission directly into an Infigo order — no login, no checkout. Auto-creates the customer if needed. Useful for sample requests, internal job tickets, branded portals, B2B recurring orders, and marketing landing pages. Configured via JSON mapping in the MegaScript engine.

## Key takeaways
- Trigger Event = **Place Order** or **Form Submit**.
- Configuration is JSON, with variable substitution syntax: `${email}`, `${first_name}`, `${quantity}`, etc.
- Three core blocks in the JSON config:
  - `customerMapping` — form fields → customer attributes (username, email, firstName, lastName, fullName)
  - `defaultVariables` — fallback values (e.g. country: "GB")
  - `hubSpotProperties` — for CRM integration
- Set up at **Admin > MegaScripts > Add New > Trigger Type: On Event > Event: Place Order**.
- Attach to storefront via **Connect > Scripting**.
- Optional `successPage` and `errorPage` URLs for post-submit redirect.
- `logLevel: 4` for verbose troubleshooting logs.
- Works with HubSpot / CERM / other integrations to chain automation.

## Code / config snippets

### Example MegaScript JSON config
```json
{
  "pluginSystemName": "mis.scripting",
  "hubSpotProperties": {},
  "customerMapping": {
    "username": "${email}",
    "email": "${email}",
    "firstName": "${first_name}",
    "lastName": "${last_name}",
    "fullName": "${first_name} ${last_name}"
  },
  "defaultVariables": {
    "country": "GB"
  }
}
```

### Setup steps
1. Admin > MegaScripts > Add New, Trigger Type "On Event", Event "Place Order".
2. Paste JSON config; save.
3. Connect > Scripting > select storefront > attach the MegaScript, set Trigger Event = "Place Order" or "Form Submit".
4. Build HTML form whose `name` attributes match the `${...}` placeholders in `customerMapping`.
5. Submit → order is created with no checkout flow.

## Related
[[prepopulate-data-script-megaedit]]
