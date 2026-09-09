---
title: "Conditional/Multi-variant Business Card Template — single vs two products"
source: "author-session"
type: "hack-note"
date: "2026-07-01"
tags: [megaedit, invent, variable-logic, business-card, conditional, required-fields, customer-group, batch-gap, single-vs-two-products]
relevance: "high"
---

## Problem
Property-mgmt customer wants one business-card setup covering two employee classes:
- "Field" = on-site staff, one location. Field logo (B&W), location name + address on card, personal email.
- "Regional" = managers, multiple locations. Regional logo (B&W), NO address, TWO emails (personal + location). Managers of >1 community get one card per locationy (phones differ) — EXCEPT Maintenance (single card).
All fields required; CMs self-serve the fields going forward. Single product with editor logic, or two products?

## Root cause / constraints
- Invent Variable Logic (Show/Hide/SetValue, if/elseif/else) handles logo swap + optional address + optional 2nd email — but it is FORM-DRIVEN and does NOT fire on MegaEdit CSV batch upload (confirmed gap, see `experiments/invent-scripts-slot-test/RESULTS.md`). Bulk seeding => must pre-bake one template per division.
- "Card per location" is a multiplicity, not visibility — Variable Logic cannot spin N personalized cards. Multipart versioning gives N versions but shares attributes (no per-version personalization).

## Fix / verdict
Build TWO products (Field, Regional), each locked to the matching customer group so the email-based split is enforced by membership. Single product only viable if the customer will NEVER bulk-CSV and accepts one-order-per-location. Each requirement maps to:
- logo/address/2nd-email conditionals = Invent Variable Logic (form only)
- all-required + control types = Product Attributes "Required" flag
- prefill CM name/email = Prepopulate Data Script
- entered fields onto job = Sync Inputs to Attributes (`save to attribute_<Name>`)

## Sample (logic sketch)
Field: logo=Field; show LocationName+Address (required); email=personal; 1 card.
Regional: logo=Regional; hide Address; email=personal+location (both required); if Role != Support AND #locations>1 → one card per locationy (name+phone+communityEmail each).

## Caveats / interactions
- Card-per-location output: one order per location (interactive) OR one CSV row per card (batch, split-CSV). Image swap on CSV works via album syntax.
- Support-staff exception = Role field gating the repeat.
- Confirm whether Regional card shows location NAME (address omitted only).
