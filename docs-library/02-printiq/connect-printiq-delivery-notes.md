---
title: "Sending Delivery Notes and Special Instructions to printIQ | CI_PrintIQ_009"
source: "printiq-kb"
url: "https://academy.infigo.net/p/347/sending-delivery-notes-and-special-instructions-to-printiq-ci_printiq_009"
type: "tutorial"
date: "2022-12-05"
tags: [connectid, checkout-attributes, delivery-notes, special-instructions, notes]
relevance: "medium"
---

## Summary
Maps Infigo Checkout Attributes (typically multi-line textboxes shown during checkout) into PrintIQ's Delivery Notes and Special Instructions fields. The mapping is by Checkout Attribute name. Tutorial video: https://www.youtube.com/embed/cWqYHgpKzAo

## Key takeaways
- Create the Infigo Checkout Attribute first: admin search "checkout" → **Checkout Attributes** → add/edit. Use a multi-line textbox for free-text instructions.
- In the Connect:PrintIQ plugin config, locate the **Delivery Notes** and **Special Instructions** fields and paste the **name** of the corresponding Checkout Attribute into each.
- Whatever the customer types in checkout flows through to those PrintIQ fields on the resulting quote/job.
- Pairs with the FAQ note that PrintIQ Notes field is the safe place to stuff data for Stock products that can't accept Additional Reference Fields.

## Related
[[connect-printiq-job-reference-data]]
[[connect-printiq-faq]]
