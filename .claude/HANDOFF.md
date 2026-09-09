# HANDOFF — infigo-hacks

**Updated:** 2026-09-09 11:30 CDT · **Branch:** `main` · **HEAD:** see `git log -1`
**State:** tree clean & pushed · memory updated · repo is PUBLIC

## Next steps
1. Write `docs-library/07-invent/csv-image-swap-album-syntax.md` from the "CSV-driven image swap research" entry in `ROADMAP.md` (Closed section): `AlbumName/ImageName.ext` in a CSV cell swaps the image per record; Infigo docs say no extension, empirically wrong. Follow `docs-library/_FORMAT.md`, add it to `07-invent/_INDEX.md`, and update the doc count in `docs-library/INDEX.md`.
2. Same treatment for the "Variable Logic in batch is an architectural ceiling" limitation (source material: `experiments/invent-scripts-slot-test/RESULTS.md`).
3. Decide whether `pricing-generator.html` gets hosted (ROADMAP "Later") now that the repo is public — GitHub Pages is the zero-cost option.

## Open loops
- [ ] ROADMAP "Now" still carries the name-badge batch product ConnectID question from May 2026 (parent-pricing cart setting test vs routing-only). Confirm whether it was resolved on the storefront and close or update it.

## Gotchas
- Public repo. Before every commit: grep the staged diff for personal names, shop name, client names, storefront URLs, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory file `infigo-hacks-repo-is-public.md` has the full list and the established generic aliases (Field / Regional, "locations").
- `*.pdf` and `*.mex` are blanket-ignored. A reference PDF needs a `.gitignore` negation or, better, conversion to markdown.
- Commit author must be the GitHub noreply address, not Gmail. Set once: `git config user.email 109639555+BmartOcho@users.noreply.github.com` in this repo.
- Session prompts (`NEXT.md`, `STARTER-PROMPT.md`, `MEX-GENERATOR-STARTER-PROMPT.md`), `Claude outputs/`, `Customer-CSV-Additions/`, and `mexgen/dump-*/` exist locally but are ignored. Don't un-ignore them.

## Pointers
- Memory: `infigo-hacks-repo-is-public.md`, `infigo-hacks-repo-gitignore.md`
- `ROADMAP.md` (public) — Now / Next / Later
- `docs-library/INDEX.md` — library entry point; `_FORMAT.md` — per-doc format

## Log
- 2026-09-09 11:30 — Repo created private, cleansed of all personal/shop/client identifiers, history squashed to one commit, flipped PUBLIC, business-card example genericized to Field/Regional.
