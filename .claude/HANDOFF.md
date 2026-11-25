# HANDOFF — infigo-hacks

**Updated:** 2026-11-25 15:30 CST · **Branch:** `docs/closeout-2026-11-25-badge` (off `main` b59e422, after PR #12 merged) · repo is PUBLIC
**State:** committed; push + PR waiting on owner OK · memory updated

## Next steps
1. **Send the name-badge customer the Flex product note.** The CSV column is now **Matchup** (type the whole line, e.g. "Big 12 Championship"). Point them to the product's sample CSV download, which was verified. Memory `big-ticket-name-badge-flex.md`.
2. Review and merge the closeout PR for `docs/closeout-2026-11-25-badge` (ROADMAP entry, new docs-library note, this handoff). Only the owner merges.

## Gotchas
- Public repo. Before every commit, grep the staged diff for personal names, shop name, client names, storefront URLs, order/job ids, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory `infigo-hacks-repo-is-public.md` has the full list.
- A CSV field that mixes `[#Column#]` with literal words prints those words on every record. The customer can't remove them. Fix with a new product that uses one free-text placeholder. Write-up: `docs-library/04-megaedit/static-text-beside-csv-placeholder.md`.
- The badge venue is still baked into background_1/2.pdf. Strip it and add Venue/City columns only if an event at another venue comes up.
- `python -I` hides the user site-packages where PyMuPDF lives; use `-P`, or run plain `py`, for trusted local files.
- `*.pdf` and `*.mex` are blanket-ignored. Commit author must be the GitHub noreply address.

## Pointers
- Memory: `big-ticket-name-badge-flex.md`, `infigo-hacks-repo-is-public.md`
- `ROADMAP.md` (public): Now / Next / Later
- `docs-library/04-megaedit/static-text-beside-csv-placeholder.md`

## Log
- 2026-11-25 15:40 — Owner closed the multi-location business card loop (carried 4x). v3 stands as the release candidate; reopen only if the customer sends corrected art.
- 2026-11-25 15:30 — Name badge made event-agnostic: a new Flex product with a free-text `[#Matchup#]` column replaces the hard-coded "vs. <home team>". The old product is untouched, so reorders still work. Import-verified from the site PDF; the product's sample-CSV download shows the new header.
- 2026-11-25 13:40 — Event flyer v-04: one product with a 4/8-slot layout dropdown, shared slot-1–4 inputs, and taglines that wrap to 2 lines (customer complaint). Import-verified from the site PDF: the art swaps on both pages and every baseline sits within 0.1 pt. First live confirmation of a generated Show/Hide rule. Sent to the customer; closed unless they reply.
