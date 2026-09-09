# Invent Docs Library — Index

Documentation harvested from Infigo Academy on **Invent** — the Adobe InDesign plugin that exports `.MEX` packages for MegaEdit. Covers install, the Setup tab, Variable Logic (the conditional rules engine that lives inside Invent and ships baked into the MEX), exporting, and troubleshooting.

## Files

| File | What it covers |
|------|----------------|
| [invent-overview.md](invent-overview.md) | Category index — Invent pathway (Getting Started → MegaEdit↔Invent → Resources → Variables → Forms → Exporting → FAQ), what Invent is, handoff model (Invent → MEX → MegaEdit) |
| [invent-install.md](invent-install.md) | **Getting Started** — Download Invent plugin + Anastasiy/AEScripts Extension Manager, install via Extension Manager, enable in InDesign via Window → Extensions → Infigo Invent |
| [invent-setup-tab.md](invent-setup-tab.md) | **Setup tab** (5 sub-tabs: Editor / Field / Image / Visual / Other) — MegaEdit product settings baked into the MEX. **Doc is stale**: real plugin also exposes Scripts, Hardcoded Scripts, Export Type, Page Type fields the Academy doc never mentions. |
| [invent-variable-logic.md](invent-variable-logic.md) | **Variable Logic** — Rules = Conditions + Actions (Set Value / Show / Hide), if / else if / else; works on Invent Variables and Fields. **Form-driven only — does not fire on CSV batch upload** (load-bearing limitation, see hack file). |
| [invent-export-package.md](invent-export-package.md) | **Exporting** — Save InDesign file → Export tab → Set Export File → Export. Validation errors block export. |
| [invent-mex-export-troubleshoot.md](invent-mex-export-troubleshoot.md) | **FAQ** — Common export failure: exporting to OneDrive / Dropbox / cloud-synced folder silently fails. Fix = export to a purely local path. |
| [invent-faqs.md](invent-faqs.md) | **FAQ** — Master Pages (static only), rectangle frames only, no Adobe Cloud Fonts, log file locations, version check, batch coming-later note. Comment thread confirms batch + Invent integration is a known gap. |

## Notes / gaps

- **Scripts / Hardcoded Scripts fields** in Setup → Other tab are undocumented on Academy as of May 2026. The 2023 Setup Tab article predates them.
- **Invent + Batch CSV** is a known product gap — Infigo themselves acknowledge in FAQ that batch support "is coming." User-reported in Aug 2023 comment (Rob Whitney) and still unresolved.
- Categories `c/250 Invent Logic` and `c/405 Advanced Grouping` not harvested individually — Variable Logic article is the load-bearing entry from those.
- Webinars (July 2023 Intro, March 2024 Business Card Workshop) are video-only, not text-harvestable.
- The official Invent docs live on Zendesk and are surfaced through Academy — content is identical.
