---
title: "Infigo REST API — where customer-entered attribute values live on orders"
source: "infigo-academy"
url: "https://api-lambda.public.infigosoftware.rocks/openapi"
type: "api-ref"
date: "2026-10-01"
tags: [api, orderlineitem, product-attributes, checkout-attributes, variables, openapi, order-line-detail-report]
relevance: "high"
---

# Attribute values missing from `orderlineitem/get`

## Problem
`GET /services/api/orderlineitem/get?id=<id>` returns a `ProductAttributes` key, but it's
empty, even though the customer-entered values show up in the admin
**Sales → Order Line Detail** report.

## Root cause
Infigo stores what a customer types in three different places, and only one of them is
`ProductAttributes`. The OpenAPI spec (build 16511) says:

| What the customer filled in | Admin location | API field | Endpoint |
|---|---|---|---|
| Product attribute (dropdown/textbox on the product page) | Catalog → Products → *product* → Product Attributes | `ProductAttributes[].Values[].Content` | `orderlineitem/get?id=<jobId>` |
| Checkout attribute (asked once at checkout, order-level) | Catalog → Attributes → Checkout attributes (nopCommerce-standard path; not yet confirmed on our admin) | `CheckoutAttributes[].Values[].Content` | `order/detail/{orderId}` |
| MegaEdit / dynamic-template field (personalization) | the editor template | `Variables[].Items[].{Name,Value}` | `orderlineitem/get?id=<jobId>` |

The Order Line Detail report CSV has a per-line `Attributes` column that holds a
`Name: Value` description string (e.g. `Billing-GL Codes: <option text>`). A value in that
column points to a **product attribute** on the line. The API has no field carrying that
description string, and there is no report/export endpoint in the spec.

**Seen on our storefront (2026-10-01):** a Static PDF product (`Type: 30`, job `Id` prefixed
`s`, e.g. `s1234`) using PrintIQ custom quoting (`Quote.Id` set, `Price: 0`). It had one
dropdown product attribute, which showed in the report's `Attributes` column.
`orderlineitem/get` returned the correct line (`OpvId` matched the report's `OrderLineId`),
but with `ProductAttributes: []`, `Variables: null`, `MisConfigurations: []`. That doesn't
match the spec. The cause is still unknown and sits on Infigo's side. Support ticket sent 2026-10-01;
awaiting reply. Update this note with their answer.

The second cause is the `id` parameter. `orderlineitem/get` takes an **order line item (job)
id or a basket item id**, not the order number. The spec says it returns `null` when nothing
matches. If you pass an order number, it can match an unrelated job or basket item that has
the same number.

## Fix
1. Get the line ids from the order first: `GET /services/api/order/detail/{orderId}`. That
   response's `OrderLineItems` is the array of job ids, and it also holds `CheckoutAttributes`.
2. Call `orderlineitem/get?id=<jobId>` for each line.
3. Read all three carriers (`ProductAttributes`, `Variables`, and the order's
   `CheckoutAttributes`), then check the response's `OrderId` against the order you asked for.
4. If the field really is a product attribute (it's on the product's Product Attributes
   tab), the id is a confirmed job id, and `ProductAttributes` is still empty, the API isn't
   doing what the spec says. Open a ticket with Infigo support.

## Sample
```text
GET /services/api/order/detail/12345
  → { "OrderLineItems": [67890, ...],
      "CheckoutAttributes": [ { "Name": "Cost Center", "Values": [ { "Content": "4410" } ] } ] }

GET /services/api/orderlineitem/get?id=67890
  → { "OrderId": 12345,
      "ProductAttributes": [ { "Id": 7, "Name": "Ship-to Store #",
                               "Values": [ { "Id": "...", "Content": "112" } ] } ],
      "Variables": [ { "Set": {...}, "Items": [ { "Name": "FirstName", "Value": "..." } ] } ] }
```

Support ticket text, for step 4:
> `GET /services/api/orderlineitem/get?id=<jobId>` returns `"ProductAttributes": []` for a
> job whose product attributes are filled in. The values show on the Sales → Order Line
> Detail report, and the API spec (InfigoOrderlineItem.ProductAttributes, "Product
> attributes and selected values for this item") says they should be returned. Is something
> on our platform or the product suppressing them, or is this a known issue?

## Caveats
- The spec is a live, auto-generated file. The docs site at
  `api.public.infigosoftware.rocks` is a JS app that loads
  `https://api-lambda.public.infigosoftware.rocks/openapi` (about 790 KB of YAML). Fetch that
  URL directly to grep it. The `/swagger.json`-style paths return 403.
- `orderlineitem/jobticket?id=<jobId>` returns the job ticket **PDF**. It's a fallback if you
  only need the values for humans to read, not to parse.
- For a value you need to read reliably by API, a checkout attribute (order-level) or an
  editor variable may fit better than a product attribute. Choose based on whether the
  value is per-order or per-line.
- **Checkout attributes don't work for per-product codes.** Every user on the store sees
  them at checkout on every order, whatever products are in the cart or which department
  the user is in. When a code applies only to some products, keep it as a product attribute.
- **Per-line fallbacks while the API is broken.** Infigo has an orderline-level
  `Attributes` placeholder (Admin → Configuration → Placeholder Overview), which job tickets
  use to print attribute details. Two ways to use it:
  - Read `orderlineitem/jobticket?id=<jobId>`. It returns a PDF, so you'd have to parse it.
  - If the value is meant for PrintIQ (GL / cost codes), add a Connect: PrintIQ → Additional
    Reference Fields row: Key = the PrintIQ Job Reference Field name, Value = the
    `Attributes` placeholder (copy the exact token from Placeholder Overview). This is POD
    products only. The value is the whole `Name: Value` string for all of the line's
    attributes. Using orderline placeholders in reference mapping is "cross-use", which
    Infigo says works but isn't officially supported. See [[connect-printiq-job-reference-data]].

Related: [[product-attributes]], [[connect-printiq-overview]], [[connect-printiq-job-reference-data]], [[connectid-checkout-attribute-mapping]]
