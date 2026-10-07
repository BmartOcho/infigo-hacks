---
title: "'Cannot use the form value for attributes' Setup-level log on product pages"
source: "storefront-log"
url: ""
type: "hack-note"
date: "2026-10-05"
tags: [logs, product-attributes, attribute-combinations, textbox-attribute, crawler, meta-externalagent, noise]
relevance: "medium"
---

# "Issue setting up the product details page … Cannot use the form value for attributes:" log entries

## Problem
After adding a per-product purchasing-code attribute (textbox) to product pages, the admin
log (Log level: **Setup**, Origin: Website) filled with entries like:

`Issue setting up the product details page for Door Hangers (28). Cannot use the form value for attributes:`

Page URL is `POST /catalog/getproductattributecombinationdetails`, referrer is the product
page, Content-Length ~33 bytes, and the attribute list after the colon is **empty**.

## Root cause
`getproductattributecombinationdetails` is the AJAX call the product page fires on load and
on every attribute change to find the matching **attribute combination** (price / stock /
SKU). It parses the posted attribute form values. When the posted body carries no usable
values for the product's attributes, the platform writes this Setup-level diagnostic. It is
not an order failure and the page still renders.

The first observed entry came from a **Meta (Facebook) crawler**, not a customer: the
User-Agent ends in `meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler)`
and the IP is in Meta's `57.141.x.x` range. The crawler executes the page JS, which fires
the combination lookup with an essentially empty body, hence the empty attribute list.
Text-type attributes are also excluded from attribute combinations (July 2026 release notes),
so a textbox-only attribute set can never resolve to a combination anyway.

## Fix
1. In the log view, filter on the full message and check User-Agent / IP of each entry.
   Entries from `meta-externalagent`, `facebookexternalhit`, Googlebot, Bingbot etc. are
   crawler noise and can be ignored.
2. If entries also come from real customer sessions (normal browser UA, logged-in customer
   id), then check the product variant's Attributes tab: a Required textbox attribute with
   no default fires this on page load before the customer types anything. Either untick
   Required (enforce via a pricing/validation rule instead) or give it a default value.
3. Nothing to send to support unless customers report the product page not loading or
   add-to-cart failing.

## Sample
Log headers that identify crawler noise:
```
"User-Agent": "Mozilla/5.0 ... Chrome/145.0.0.0 ... (compatible; meta-externalagent/1.1 (+https://developers.facebook.com/docs/sharing/webmasters/crawler))"
"X-Forwarded-For": "57.141.16.12"
"Content-Length": "33"
```

## Caveats
- Log level **Setup** is diagnostic, not Error. Don't treat volume alone as breakage.
- Expect a burst of these right after adding attributes to many products: crawlers re-fetch
  pages whose content changed, and every product page view now triggers the lookup.
- Confirm against a real-customer entry before concluding it is all noise.

Related: [[product-attributes]], [[api-order-line-attributes]], [[infigo-release-notes-2026-07]]
