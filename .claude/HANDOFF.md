# HANDOFF — infigo-hacks

**Updated:** 2026-11-25 13:40 CST · **Branch:** `docs/closeout-2026-11-25` (off `main` 54c8717) · repo is PUBLIC
**State:** committed & pushed; closeout PR open for the owner · PRs #11 / mexgen-agent #5 merged · memory updated

## Next steps
1. **Review and merge the closeout PR** for `docs/closeout-2026-11-25` (ROADMAP entry, docs-library note, this handoff). Only the owner merges; never merge from Claude.
2. If the event-flyer customer sends feedback, rebuild it as v-05 from the job folder's `Working/mexbuild/build_mex.py`. Geometry lives in `layout.py`. See the event-flyer project memory.

## Open loops
- [ ] Multi-location business card redesign v3: import-verified 2026-11-18 and sent to the customer. Waiting on the customer to (a) add the missing license line to one location's front, and optionally (b) re-export the art with bleed. Either way it's just a clipart swap: rerun the job folder's `Working/assets-v2/tools/` scripts. Memory `location-bc-redesign-mex.md` (carried 3x)

## Gotchas
- Public repo. Before every commit, grep the staged diff for personal names, shop name, client names, storefront URLs, order/job ids, `G:\` / `C:\Users` paths, and `hack_*` memory references. Memory `infigo-hacks-repo-is-public.md` has the full list.
- A dropdown's **parent link is set per variable, not per form slot**. If an input changes page between layouts, use one form, not `formPages`. Nothing can hide a GROUP; it hides its items.
- MegaEdit line model, now confirmed on a 3rd product: first baseline = frame top + (leading% − 0.25) × size. Site-PDF coordinates are the bleed page, so customer-page coordinates (trim at 17 pt) = site + 8.008 for a 9 pt bleed. `MexGen Agent/SPEC.md` §5.
- `python -I` hides the user site-packages where PyMuPDF lives; use `-P`. Under `-P`, add the script dir to `sys.path` yourself to import a sibling module.
- `*.pdf` and `*.mex` are blanket-ignored. Commit author must be the GitHub noreply address.

## Pointers
- Memory: the event-flyer project memory, `location-bc-redesign-mex.md`, `infigo-hacks-repo-is-public.md`
- `ROADMAP.md` (public): Now / Next / Later
- `docs-library/04-megaedit/two-version-dropdown-show-hide-generated.md` — the dropdown + Show/Hide build pattern, now import-verified

## Log
- 2026-11-25 13:40 — Event flyer v-04: one product with a 4/8-slot layout dropdown, shared slot-1–4 inputs, and taglines that wrap to 2 lines (customer complaint). Import-verified from the site PDF: the art swaps on both pages and every baseline sits within 0.1 pt. First live confirmation of a generated Show/Hide rule. Sent to the customer; closed unless they reply.
- 2026-11-18 night — Owner dropped four long-carried loops (API ticket, coupon v-02 import, camp flyer font OK, postcard review). Coupon card v-01's first order printed the amount 36 pt low. Root cause: MegaEdit's line model is `top + (leading% − 0.25) × size`, font-agnostic, and v-01 used hhea leading (183 %). Order PDF patched and reprinted OK; v-02 built (validates 0/0); SPEC §5 generalised.
- 2026-11-18 late — Open loops triaged with the owner: storefront imports run (closed), old history accepted (closed), R13 check and QR edges dropped, location-data question deferred to ROADMAP Next, docs written. PRs infigo-hacks #10, mexgen-agent #4.
