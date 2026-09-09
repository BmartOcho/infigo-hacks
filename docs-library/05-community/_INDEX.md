# 05-community — Index

Community-sourced material on Infigo, MegaEdit, MegaScript, PrintIQ, ConnectID, and adjacent web-to-print platforms. Vendor docs live in `01-official-infigo/`, `02-printiq/`, `03-connectid/`, `04-megaedit/`. This folder is for user-generated content: forum threads, public GitHub repos, third-party reviews, podcast/video walkthroughs, blog posts.

Harvested 2026-05-22.

## Files in this folder

### Highest-signal (code + dense operator voice)

| File | Source | Why it matters |
|---|---|---|
| `github-infigo-pricing-script-types.md` | GitHub (Infigo-Official) | Full TypeScript API surface + 4 paste-ready pricing-script examples (tier, role, CSV, file-info). Best single reference for `Item.*`, `HelperMethods.*` outside Academy. |
| `github-infigo-megaedit-types.md` | GitHub | npm-installable type defs for MegaEdit scripting. Auto-gen TypeDoc is the offline-readable API. |
| `github-infigo-megascript-types.md` | GitHub | Type defs for the server-side workflow/imposition engine. |
| `github-infigo-iframe-demo-app.md` | GitHub | Vue + Node reference impl for embedding the editor via iframe + JS Communicator Library. |
| `capterra-infigo-reviews-aggregated.md` | Capterra (17 verified reviews) | Most dense pool of admin pain points — JS requirement, two template systems, doc gaps, missing features, MFA email pain, Infigo Designer 32-bit Acrobat wall. |
| `printiq-aggregate-reviews.md` | Slashdot + SourceForge + Capterra + GetApp | Consistent cross-source signal: PrintIQ front-end strong, back-end support weak, ~85% coverage. Critical for setting integration expectations. |

### Medium-signal (context + benchmarks)

| File | Source |
|---|---|
| `dpsmagazine-w2p-roundup-2016.md` | DPS Magazine trade press |
| `printpod-podcast-series.md` | Infigo PrintPod (guest interviews) |
| `softwareadvice-getapp-aggregate.md` | Software Advice / GetApp |
| `youtube-megaedit-3d-blender-dieline-tutorials.md` | YouTube (Infigo channel) |
| `printplanet-best-all-around-w2p.md` | PrintPlanet (gated) |
| `printplanet-catfish-w2p-thread.md` | PrintPlanet (gated) |
| `printplanet-experience-with-printiq.md` | PrintPlanet (gated) |

### Low-signal (anchors for future research)

| File | Source |
|---|---|
| `linkedin-infigo-presence.md` | LinkedIn — handles + naming-collision warnings |
| `nopcommerce-infigo-solution-partner.md` | nopCommerce (stack confirmation) |
| `printplanet-software-comparison.md` | PrintPlanet (gated) |
| `printplanet-actual-experience-thread.md` | PrintPlanet (gated) |

## Top 5 most useful for daily work at our shop

1. **`github-infigo-pricing-script-types.md`** — paste-ready scripts and the canonical `Item.*` surface. Directly relevant to the shop's batch / VDP pricing scripts.
2. **`capterra-infigo-reviews-aggregated.md`** — every admin pain point storefront admins hit, validated by other shops. Useful when escalating to Infigo support or explaining choices internally.
3. **`printiq-aggregate-reviews.md`** — confirms the "file Infigo + PrintIQ tickets in parallel" pattern; sets the 85%-coverage expectation.
4. **`github-infigo-iframe-demo-app.md`** — only public, working reference for the iframe + Communicator Library hand-off. Relevant if our shop ever embeds the editor in a partner site.
5. **`github-infigo-megaedit-types.md`** — fastest path to a typed MegaEdit script (no Academy login needed).

## Known gaps

- **Reddit:** essentially zero hits. r/printing, r/Printers, r/printshop, r/PrintTech do not discuss Infigo, MegaEdit, or PrintIQ. r/web2print does not exist or has no Infigo content. The W2P-admin demographic is on PrintPlanet, LinkedIn, and Capterra, not Reddit.
- **PrintPlanet content gating:** the modern PrintPlanet UI returns near-empty HTML to anonymous fetches. All listed PrintPlanet docs rely on Google's indexed snippets. To get full thread text, log in to PrintPlanet and re-scrape.
- **Stack Overflow / Stack Exchange:** no Infigo-tagged questions. The integration is too niche.
- **Independent operator blogs:** no individual print-shop admin appears to publish day-to-day Infigo content. The closest analogues are vendor-published "case studies" (FE Burman, Peczuh, Cober, ASU Print Lab) — those belong in `06-third-party/` if you want them, not here.
- **Third-party YouTube tutorials:** none found. All hits are Infigo's own channel.
- **ConnectID community content:** none found. ConnectID is an Infigo-private bridge product with no community footprint outside vendor docs.
