# mexgen → MEX Generator Agent — Build Plan

**Goal:** plain-text brief + background PDF(s) + font files → import-ready `.mex`, no InDesign/Invent in the loop.
**Starting point:** `mexgen/mexgen.py` (969 lines, stdlib Python) — donor-based inspect/build/edit, proven live in MegaEdit 2026-07-01/02.
**Canonical seed template:** the name-tag template (v-06) — 2 pages, 5 text fields, 3 static fonts, no logic, no hidden resource sets. Cleanest MEX we have.

---

## Ground truth (do not re-derive — these are verified)

| Fact | Source |
|---|---|
| MEX = plain zip: `template.xml` + `backgrounds/` `cliparts/` `fonts/` | `docs-library/07-invent/mex-file-format-anatomy.md` |
| Layout stored twice: XML `<Pages>` and JSON `InDesignData` (CDATA in `<Resources><DataItems>`) — both must agree | `mex-file-format-anatomy.md` |
| **XML `<Font name>` is authoritative for font; JSON font GUID is ignored** | name-tag build 2026-09-16 (v-03 test) |
| **XML `<FontSize>` is authoritative; JSON fontSize stays INHERIT** | mexgen v-01 |
| Field `<Font name>` must match a `<Resources><Fonts><Category><Font name>` exactly | name-tag build |
| **Variable fonts (fvar table) render as system fallback** — statics only | name-tag v-01 |
| Invent flattens weights with no Standard-category entry to SemiBold | name-tag v-02 |
| MEX import registers fonts on the storefront; storefront dedupes by name and keeps the first binary | name-tag build (Black weight stale) |
| Field id = zero-padded adobeId; variables/rules = random GUID | mexgen |
| JSON `fields[].page` is 0-based; XML page order = index | mexgen |
| `Information/CustomData` = JSON text blob `{"originalFieldId": id}` | mexgen |
| fieldGrowType FREE = auto-grow, not user-resize; use FIXED + `allowSizeChange` | text-field resize snapback note |
| Static clipart binding is XML `<ClipartImage name>`; JSON imageValue stays NONE | mexgen |
| Backgrounds are a proven render path — byte-swap PDFs to pin art | mexgen |

---

## Phases

### Phase 0 — Consolidate the spec (½ day)
- [ ] `mexgen/SPEC.md`: every fact above + the JSON field/variable/form shapes from `mex-file-format-anatomy.md`, in one file. This is what the agent reads.
- [ ] `mexgen/fixtures/`: copy in name-tag v-01 (variable font, broken), v-02 (XML/JSON mismatch), v-06 (clean), the Field card rev, Event Flyer. Dump each with `mexgen inspect`.
- **Done when:** a fresh Claude session can build a field by reading SPEC.md alone.

### Phase 1 — `mexgen validate` hardening (1–2 days)
Turn every bug we've hit into a rule. Exit non-zero on any ERROR.
- [ ] `FONT_VARIABLE` — any `fonts/*.ttf|otf` with an `fvar` table → ERROR
- [ ] `FONT_UNDECLARED` — field `<Font name>` not in `<Resources><Fonts>` → ERROR
- [ ] `FONT_BINARY_MISSING` — `BinaryReference` path not in zip → ERROR
- [ ] `FONT_XML_JSON_MISMATCH` — XML font name vs JSON GUID → different file → WARN (XML wins, but flag it)
- [ ] `FONT_DUPLICATE_CATEGORY` — same binary declared in two categories → WARN
- [ ] `FONT_NAME_TABLE` — report nameID 1/2/4/6 + fsSelection for each TTF (info)
- [ ] `FIELD_XML_JSON_COUNT` — text/image field counts and ids match both sides → ERROR
- [ ] `FIELD_PAGE_RANGE` — JSON page index < XML page count → ERROR
- [ ] `RESOURCE_DANGLING` — declared asset with no zip entry, or zip entry with no declaration → ERROR/WARN
- [ ] `XML_WELLFORMED`, `JSON_PARSES` → ERROR
- [ ] `GROWTYPE_FREE` — WARN with pointer to snapback hack
- **Done when:** v-01 fixture fails on FONT_VARIABLE, v-02 warns on MISMATCH, v-06 passes clean.

### Phase 2 — `mexgen new` (from-scratch skeleton) (1–2 days)
Today mexgen needs a donor. Make the donor implicit.
- [ ] `mexgen new --spec product.yaml` → blank MEX: pages (w/h/bleed pts), backgrounds, fonts declared, zero fields, empty forms/variables. Built by stripping v-06 to the skeleton and re-emitting.
- [ ] Fonts pipeline: `fonts_dir` → validate static → declare each in `Standard` category as `"<Family> - <Style>"` from the name table → emit BinaryReference.
- [ ] Backgrounds: PDF per page → `backgrounds/background_N.pdf` + XML `<Background>` + JSON `pages[]`.
- **Done when:** `mexgen new` output passes `validate` and imports into MegaEdit as an empty 2-page product.

### Phase 3 — Layout DSL (2–4 days — the real work)
Extend the existing config (`stacks`, `protoFrom`, `resolve_position`) into a small declarative layout language.
```yaml
pages:
  - size: [252, 144]   # pts
    bleed: 9
    background: front.pdf
fields:
  - name: firstName
    type: text
    variable: {name: "First Name", required: true, max_chars: 20}
    font: {file: Saira-Black.ttf, size: 32, color: [100, 60, 0, 0]}
    box: {anchor: center, y: 62%, w: 90%, h: 40}
    align: center
    fit_to_box: false
    grow: fixed
  - name: lastName
    below: firstName        # relative placement
    gap: 4
    font: {file: Saira-ExtraBold.ttf, size: 18}
```
- [ ] Anchors: `top-left | center | ...`, %-of-page or pts, `below:/right-of:` relative placement, `stack:` groups.
- [ ] Auto-create variable + form ITEM per text field unless `static: true`.
- [ ] Rich-text inline spans (`<span style="font-family:..;font-size:..">`) for multi-size blocks.
- [ ] Image fields + IMAGE variables (customer-swappable logo).
- [ ] Barcode/QR field bound to URL variable.
- **Done when:** name-tag v-06 can be regenerated from a YAML spec and diffs clean against the real export (positions ±0.5pt, fonts/sizes exact).

### Phase 4 — Agent layer: Claude Code skill first, MCP second (1–2 days)
- [ ] Skill `mex-build` (SKILL.md): brief + assets → write `product.yaml` → `mexgen new` → `mexgen build` → `mexgen validate` → report + file path. Reads SPEC.md. Refuses to emit if validate fails.
- [ ] Skill `mex-inspect`: drop a MEX → font/field/resource report (what I did by hand today).
- [ ] Skill `mex-fix`: known-issue playbook — variable font swap, weight remap, storefront-name collision rename.
- [ ] MCP server (`mexgen-mcp`, Python FastMCP): tools `mex_inspect`, `mex_new`, `mex_build`, `mex_validate`, `mex_edit`. Same code, tool wrapper. Only after skill loop is stable — MCP is for when Infigo (or another agent) calls it.
- **Done when:** "Build a 2-sided 3.5×2 name badge, fonts in ./fonts, art in ./art, fields: first name 32pt Black, last name 18pt ExtraBold, company 14pt SemiBold" produces a validated MEX in one turn.

### Phase 5 — Import-test harness (ongoing)
- [ ] `TESTLOG.md`: one row per import — MEX, storefront, result, screenshot path. Every "awaiting import test" note gets closed here.
- [ ] Later: Claude in Chrome script — upload MEX to Infigo admin, open MegaEdit, screenshot, attach to log.

### Phase 6 — Logic rules (deferred)
Show/Hide/SetText/SetImage generation + parent-linked variables. Only after Phases 1–4 are boring.

---

## Order of attack for the CC session
1. Phase 1 first — cheapest, highest value, and it makes every later phase self-checking.
2. Phase 0 in parallel (documentation while tests run).
3. Phase 2 → 3 → 4.

## Starter prompt for the local CC session
```
Read mexgen/MEXGEN-AGENT-PLAN.md and mexgen/SPEC.md (if present; else
docs-library/07-invent/mex-file-format-anatomy.md). Start with Phase 1: extend `mexgen validate`
with the listed rules. Fixtures are in mexgen/fixtures/. v-01 must FAIL on
FONT_VARIABLE, v-02 must WARN on FONT_XML_JSON_MISMATCH, v-06 must pass clean.
Stdlib only, except fontTools is allowed for name-table reads. Do not touch build
logic in this phase. Commit per rule.
```

## Open questions to settle before Phase 3
- Font naming convention for `Standard` category: keep Invent's `"Saira - Black"` (space-dash-space) for storefront compatibility? **Recommend yes.**
- Units in YAML: pts everywhere (matches XML) vs inches for humans. **Recommend pts internally, accept `in`/`mm` suffixes.**
- Where does the storefront font manager state live? The agent can't see it. Add a `--storefront-fonts fonts.txt` input so validate can warn on name collisions.
