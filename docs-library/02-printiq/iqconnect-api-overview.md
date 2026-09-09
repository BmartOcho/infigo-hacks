---
title: "IQconnect - API"
source: "printiq-docs"
url: "https://printiq.com/iqconnect-api/"
type: "article"
date: "2025-01-31"
tags: [api, iqconnect, integration, smartsite, punch-out, link, integrate]
relevance: "high"
---

## Summary
PrintIQ's IQconnect-API page is the umbrella description of their four API-based integration modes: Integrate (CRM/ERP touchpoints), Link (cross-PrintIQ outsourcing), Punch-Out (deliver completed orders from a 3rd-party cart to PrintIQ), and SmartSite (drop-in widgets for an SEO website). All four wrap the same underlying IQconnect REST API surface.

## Key takeaways
- IQconnect-API is a paid module that exposes "many of the workflows in printIQ" via documented REST APIs. Credentials (Application Name + Application Key + user) are issued by PrintIQ Support.
- Four product flavors layered on the same API:
  - **Integrate** — generic API touchpoints; pre-built integrations exist for HubSpot and Zoho, plus published Zaps in Zapier.
  - **Link** — instance-to-instance outsource: query supplier PrintIQ for price, push the quote, transfer artwork; powered by the Outsource Manager.
  - **Punch-Out** — third-party e-commerce cart finalizes checkout then pushes the order (with artwork) into PrintIQ's Production Board. PrintIQ can send back basic unformatted status updates; anything custom is a dev project.
  - **SmartSite** — copy/paste widget on an SEO site that calls the API to drive the Simplified Order workflow.
- The doc is marketing-level. No endpoint paths, request shapes, or schemas are public; the full API doc is behind the licensed module.
- Integrate API supports both **customer** and **pipeline** updates to CRMs, suggesting separate Customer and Quote/Job endpoints.

## Related
[[connect-printiq-overview]] — how Infigo consumes these APIs as a Punch-Out client.
[[printiq-getprice-live-pricing]] — the specific GetPrice call used by the Infigo plugin.
