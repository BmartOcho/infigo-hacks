# Business Card Template — Two-Product Build Spec

_Infigo storefront · Infigo + MegaEdit · drafted 2026-07-01_

Customer: property-management client with two employee classes — **Living** (on-site staff, one community) and **Communities** (managers, multiple communities). Build is **self-service**: staff log in and fill their own card fields; no CSV/batch. This spec delivers two MegaEdit products, each gated to its own customer group.

---

## 1. Why two products (not one branching product)

- **Auto-routing, no mis-pick.** Group membership decides which card a person sees. No "which division are you?" dropdown to get wrong. Each product shows only the fields that role needs.
- **No Variable Logic needed in the core build.** Because each product has a fixed logo and a fixed field set, there's nothing to conditionally show/hide. Fewer moving parts = fewer failure modes. (A single product would force a Division dropdown + Variable Logic, which fires on user *change* and not reliably on *load*.)
- **Cleaner "all required" UX.** A flat required form per role beats a branching form where half the fields are hidden.

---

## 2. Confirm before publishing

Two open items that change the build if the answer flips:

1. **Multi-community output.** This spec assumes a manager who runs 4 communities **logs in and orders once per community** (each order = that community's card). If instead they must get all cards in **one sitting**, interactive MegaEdit can't personalize N cards in one pass — the Communities side would need a small per-community CSV feed instead. You flagged you'd double-check this.
2. **Community card content.** This spec assumes the Communities card **prints the community name** (name + phone + community email) and only *omits the street address*. If the Communities card should carry no community identifier at all, drop the Community Name field from Product B.

---

## 3. Architecture at a glance

| | Product A — Living Card | Product B — Communities Card |
|---|---|---|
| Audience | "living" staff (Living customer group) | "communities" staff (Communities group) |
| Logo | Living tree (B&W), static | Community tree (B&W), static |
| Community name | Yes | Yes _(confirm — see §2)_ |
| Street address | **Yes**, required | **No** |
| Phone | Direct phone | Community phone (differs per community) |
| Email(s) | 1 — personal/work | 2 — personal + community |
| Cards per person | One | One per community (order per community) |
| In-editor logic | None | None (core build) |

---

## 4. Prerequisites (one-time platform setup)

1. **Customer groups / roles.** Create (or reuse) two roles: `Living` and `Communities`. Assign every employee to the correct one. Because the split maps to "living"/"communities" in the email, you can bulk-assign at customer import based on the address pattern, or set it manually per user.
2. **Logo assets.** Upload both B&W tree logos as fixed placed images — one for each product. These are artwork, not editable fields.
3. **Enable Prepopulate Data Script** on each product (fills first/last/title/email from the account — see §7). Path: `Admin > Catalog > Product Types > MegaEdit > MegaEdit Products > Edit product > Scripts tab > enable "Prepopulate Data Script" > Save`.
4. **Confirm any custom profile fields** you want to prefill (e.g. Job Title) exist on the customer record. Standard fields (first/last/email) are available by default; anything else must be a defined profile field.

---

## 5. Product A — Living Card

### Fields

| Field | Control | Required | Source | Notes |
|---|---|---|---|---|
| First Name | Text | Yes | Prefill (account) | editable |
| Last Name | Text | Yes | Prefill | editable |
| Job Title | Text | Yes | Prefill if stored, else CM | |
| Direct Phone | Text | Yes | CM | |
| Email | Text | Yes | Prefill (account email) | single email on this card |
| Community Name | Text | Yes | CM | |
| Address — Street | Text | Yes | CM | |
| Address — Suite/Unit | Text | No | CM | optional line |
| City | Text | Yes | CM | |
| State | Text | Yes | CM | |
| ZIP | Text | Yes | CM | |

_(City/State/ZIP can be merged into one required line if the layout prefers it — keeps the form shorter.)_

### Logo
Living tree logo, placed as static artwork. Not a field.

### Logic
None. Flat required form.

---

## 6. Product B — Communities Card

### Fields

| Field | Control | Required | Source | Notes |
|---|---|---|---|---|
| First Name | Text | Yes | Prefill (account) | editable |
| Last Name | Text | Yes | Prefill | editable |
| Job Title | Text | Yes | Prefill if stored, else CM | |
| Community Name | Text | Yes _(confirm §2)_ | CM | identifies which community this card is for |
| Community Phone | Text | Yes | CM | the per-community number that differs |
| Personal Email | Text | Yes | Prefill (account email) | email #1 |
| Community Email | Text | Yes | CM | email #2 |
| Direct/Cell Phone | Text | No | CM | optional personal line |

**No address block** on this product.

### Multi-community & the maintenance exception
Handled by ordering behavior, not the template:

- A manager over multiple communities **places one order per community**, entering that community's name / phone / community email each time. Each order produces one distinct card.
- **Maintenance** staff order a **single** card. This is an ordering instruction to communicate to that group — nothing in the template blocks it. (If you want it enforced, the cleanest option is a separate note/role guidance rather than template logic.)

### Logo
Community tree logo, placed as static artwork. Not a field.

### Logic
None in the core build.

---

## 7. Prefill (Prepopulate Data Script)

- Enabled per product on the Scripts tab (§4.3).
- Fills text fields from the customer's account when the editor loads: First Name, Last Name, Job Title (if stored as a profile field), and Email.
- Prefilled fields stay **editable** and still count as required — the prefill just satisfies the requirement by default.
- Community Name, Community Phone, Community Email, and the address block are **not** account data → these remain required CM entries.

---

## 8. Required-field enforcement

- Set every field marked "Required: Yes" as required in the MegaEdit field properties. The editor then **blocks Add to Basket** until all are filled.
- If any option is delivered as a **Product Attribute** (dropdown/radio/file upload) instead of an editor field, use the attribute's **Required** flag on the product variant's Attributes tab (`Catalogue > Products > Product Management > Edit > Product Variant > Edit > Attributes tab`).
- Result: no card can be ordered with a blank field.

---

## 9. Customer-group gating (product visibility)

- On each product, restrict visibility to its role via the product's **ACL / "Limited to customer roles"** setting (Infigo is NopCommerce-based — look for "Subject to ACL" + role selection on the product edit page; confirm the exact label on your build).
- Living product → visible to `Living` role only. Communities product → `Communities` role only.
- Net effect: each person logs in and sees exactly one card. The "logo by email" requirement is satisfied structurally — no rule, no selector.

---

## 10. Optional — push field values onto the order line

Only if you want the entered values as separate order-line attributes (for the production ticket / PrintIQ / reporting) rather than just baked into the card PDF:

- Enable the hardcoded **Sync Inputs to Attributes** script on the product, add a matching Product Attribute, and tag the field's Details > Tags with `save to attribute_<Exact Attribute Name>`.
- Not required for the card artwork itself — the values already render in the MegaEdit output.

---

## 11. Build checklist (in order)

1. Create/confirm `Living` and `Communities` customer roles; assign employees.
2. Upload both B&W tree logos.
3. Build **Product A (Living)**: layout + fields per §5, set required flags, place Living logo, enable Prepopulate Data Script.
4. Build **Product B (Communities)**: layout + fields per §6, set required flags, place Community logo, enable Prepopulate Data Script.
5. Restrict each product to its role via ACL (§9).
6. Save each as Product Default.
7. Run the test plan (§12).
8. Publish.

---

## 12. Test plan

- **Living user:** log in as a test account in the `Living` role → only the Living card is visible → open editor → First/Last/Title/Email prefilled → all required fields flagged → attempt Add to Basket with a blank field → **blocked** → fill all → proof shows Living logo + address block + single email.
- **Communities user:** test account in `Communities` role → only the Communities card visible → **two** email fields, **no** address, Community logo, per-community phone → required enforcement works.
- **Cross-check:** a `Living` user cannot see the Communities product and vice versa.
- **Prefill accuracy:** confirm the prefilled name/title/email match the account.
- **Multi-community:** place two Communities orders with different community details → two distinct correct cards.

---

## 13. Requirements coverage (verification)

| # | Customer ask | How this build covers it |
|---|---|---|
| 1 | B&W tree logo, Living + Communities variants | Static logo placed per product |
| 2 | "living" email → Living logo; "communities" → Community logo | Customer-role gating; role derived from email pattern |
| 3 | Living: community name + address on card | Living fields (§5), required |
| 4 | Communities: no location address | Address block omitted from Product B |
| 5 | Multi-community → card each, except Maintenance | One order per community (self-service); Maintenance orders once (policy) |
| 6 | Communities: 2 emails (personal + community) | Two required email fields (§6) |
| 7 | Template, CMs fill fields, all required | Two products, required flags on every field, prefill for account data |

---

## 14. If you ever want the single-product version instead

Collapse to one product with a **required "Division" dropdown** (Living / Communities) and add Invent Variable Logic:

```
Rule: "Division layout"
  if  Division Equals "Living"
      → Show LivingLogo, Show AddressBlock, Hide CommunityLogo, Hide SecondEmail
  else if Division Equals "Communities"
      → Show CommunityLogo, Show SecondEmail, Hide LivingLogo, Hide AddressBlock
```

Trade-offs vs two products: relies on the CM picking Division correctly, shows a branching form, and depends on Variable Logic firing on the dropdown change. Fine for one catalog tile; weaker for guaranteed-correct routing.

---

## Sources

- MegaScripts / Variable behavior — Infigo Academy (local: docs-library/01-official-infigo/megaedit-variables-applying.md, prepopulate-data-script-megaedit.md, multipart-versioning-bg050.md)
- Invent Variable Logic + the form-vs-CSV firing rule (local: docs-library/07-invent/invent-variable-logic.md)
- Product Attributes required flag + control types (local: docs-library/01-official-infigo/product-attributes.md)
- Sync inputs to attributes (local: docs-library/04-megaedit/megaedit-sync-inputs-to-attributes.md)
- Pattern note (local: docs-library/04-megaedit/conditional-businesscard-template-pattern.md)
