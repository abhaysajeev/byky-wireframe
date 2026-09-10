# BYKY drawer — shared component spec

Everything needed to give **one** create/edit drawer to every screen in the app,
and to convert any remaining screen to it later without redesigning anything.

Hand this file to an LLM together with the module names you want converted. It
contains the full contract, so no other context is required.

---

## 1. Tech stack this targets

| Layer | What is in use |
|---|---|
| Backend | Django, `django-version/full-version/`, apps under `apps/byky_*` |
| Templates | Django templates; layout via `layout_path` → `layout/layout_vertical.html` |
| Screens | Declarative specs in `apps/byky_core/screens.py`, rendered by `apps/byky_core/templates/byky/generic_screen.html` |
| CSS/JS | Plain CSS + vanilla JS in `src/assets/`, collected to `staticfiles/`. No SCSS build, no bundler, no npm |
| UI kit | Vuexy/Bootstrap 5 is present; the drawer deliberately overrides its `.offcanvas` chrome and does **not** use `.form-control` / `.row.g-4` |
| Fonts | Sora (imported by `src/assets/css/sidebar.css`), IBM Plex Mono for codes |
| Open/close | **Bootstrap's offcanvas JS is retained** — triggers stay `data-bs-toggle="offcanvas" data-bs-target="#<drawer_id>"` |

## 2. Files in this patch

| File | Destination (relative to `django-version/full-version/`) | Action |
|---|---|---|
| `apps/byky_core/templates/byky/partials/drawer.html` | same path | **new** — the single shared drawer |
| `src/assets/css/byky-drawer.css` | same path | new |
| `src/assets/js/byky-drawer.js` | same path | new |

Then:

1. In `templates/layout/partials/styles.html`, after `sidebar.css`:
   ```html
   <link rel="stylesheet" href="{% static 'css/byky-drawer.css' %}" />
   ```
2. In `templates/layout/partials/scripts.html` (or `master.html`, before `</body>`, after Bootstrap):
   ```html
   <script src="{% static 'js/byky-drawer.js' %}"></script>
   ```
3. `collectstatic`.

Loading it globally is intentional: a converted drawer needs no per-page includes.

## 3. Replace the inline drawer in `generic_screen.html`

In `apps/byky_core/templates/byky/generic_screen.html`, delete the whole block
that currently starts at

```django
{% if spec.add_label %}
<div class="offcanvas offcanvas-end{% if spec.wide %} offcanvas-wide{% endif %}" ...
```

and ends with its closing `{% endif %}` (~line 137 to ~line 189), and put in its place:

```django
{% include "byky/partials/drawer.html" with spec=spec module_label=module_label %}
```

`module_label` is already in the context of `generic_screen.html`. Nothing else in
that template changes; `screens.py` does not change at all.

That one edit converts every module that renders through `generic_screen.html`:
`byky_wallet`, `byky_api`, `byky_notification`, `byky_sysadmin`, `byky_mobile`,
`byky_rfid`, `byky_security`, `byky_integration`, `byky_rms`, `byky_tracking`.

## 4. Include contract

```django
{% include "byky/partials/drawer.html" with spec=spec module_label="Inventory · Vehicles" %}
```

| Key | Required | Meaning |
|---|---|---|
| `spec.add_label` | yes | Drawer title, e.g. `"Add Vehicle"`. If falsy, the drawer renders nothing |
| `spec.drawer_id` | yes | DOM id the trigger targets |
| `spec.sections` | yes | `[{title, fields: [...]}, …]`; `title` may be `""` for a single unnamed section |
| `spec.size` | no | `"compact"` / `"standard"` / `"wide"` — **override only** |
| `module_label` | no | Overline above the title; omit and the line disappears |

Field keys (as produced by `screens.field()` in `screens.py`):
`id`, `label`, `kind`, `required`, `placeholder`, `options` / `resolved`, `width`, `help`.

Supported `kind`: `text`, `select`, `date`, `textarea`, `number`, `file`, `checkbox`.
Anything else falls through to a text input.

`width` is the old Bootstrap column number. `12`, `9` and `8` become full-width
(span 2); everything else is a single cell. In the compact size every field is
full-width regardless.

## 5. Size is automatic — this is the important part

Drawers across the app hold anywhere from 3 to 25+ fields. `byky-drawer.js`
measures the **rendered** field count and named-section count on load and applies
the size class. Do not set `spec.size` unless a specific screen needs to disagree.

| Size | Width | Columns | Chosen when |
|---|---|---|---|
| `is-compact` | 440px | 1 | ≤ 4 fields **and** ≤ 1 named section |
| `is-standard` | 560px | 2 | anything in between |
| `is-wide` | 720px | 2 | > 12 fields **or** ≥ 4 named sections |

Under 768px every size becomes full-width, single-column.

These thresholds live in exactly one place — `pickSize()` at the top of
`byky-drawer.js`. Change them there and every drawer follows.

## 6. Behaviour the shared file provides

- **Brand accent** — 3px gradient hairline (`#a80f14 → #d81f26 → #f04a50`) across the top edge.
- **Header** — module overline (uppercase, letter-spaced) above the title; 32px close button that rotates 90° on hover. No logo tile, no field counter.
- **Section jump tabs** — rendered only when there are 2+ *named* sections. Clicking one smooth-scrolls the body; they are jump links, **not** tabs that hide fields, so Save always submits the whole form.
- **Sticky section headers** — each section title pins to the top of the scroll area while its own fields pass under it.
- **Travelling highlight** — the current section shows a red 13px accent bar, ink title, tinted rule and red count, synced to both scroll position and tab clicks. A 700ms lock after a click stops the scroll handler from stealing the highlight mid-animation.
- **Field treatments** — chevron on selects, calendar glyph on dates, dashed upload well that shows the chosen filename, inline pill switches for booleans, generic placeholders only (`Enter vehicle code`, `Select`, `Select date`, `Choose file` — never sample values).
- **Footer rail** — tinted, never scrolls away: Active switch left, then Cancel (text), Save & New (outline), Save (solid `#d81f26`).

### Scroll tracking — do not "simplify" this

Both the jump-scroll and the highlight use `getBoundingClientRect()` deltas:

```js
body.scrollTo({ top: body.scrollTop + (sec.getBoundingClientRect().top - body.getBoundingClientRect().top) - 6, behavior: 'smooth' });
```

`offsetTop` **does not work here** — the drawer is a positioned ancestor, so
`offsetTop` resolves against it and is unrelated to scroll position. Using it
produces dead scrolls and a highlight that never activates.

## 7. Converting a bespoke drawer (for later batches)

Six BYKY drawers do not go through `generic_screen.html`:

| Screen | File |
|---|---|
| E-commerce stock item catalog | `apps/byky_ims/templates/ims_e_commerce_stock_item_catalog.html` |
| Newsletter marketing dispatch | `apps/byky_ims/templates/ims_newsletter_marketing_dispatch.html` |
| Vehicle item features master | `apps/byky_ims/templates/ims_vehicle_item_features_master.html` |
| E-commerce category master | `apps/byky_ims/templates/ims_e_commerce_category_master.html` |
| Customer details registration (FSD 4.1) | `apps/byky_rms/templates/rms_customer_details_registration.html` |
| GPS/IoT hardware device registration (FSD 5.1) | `apps/byky_tracking/templates/tracking_gps_iot_hardware_device_registration.html` |

To convert one, do **not** restyle it in place. Instead:

1. Read its `<div class="offcanvas offcanvas-end" id="…">` block and write its fields down as a spec dict — `sections` of `{title, fields}` using the `screens.py` field shape.
2. Put that dict in the screen's view context as `spec` (keep the existing `drawer_id` so the page's trigger still works), or declare it in `screens.py` if the screen is otherwise spec-shaped.
3. Delete the whole offcanvas block and replace it with the one-line `{% include %}` from §4.
4. Leave the trigger button, the page's list/table, and all other markup untouched.

Also present, and **out of scope** — stock Vuexy demo screens, not BYKY: `apps/users`, `apps/ecommerce`, `apps/kanban`, `apps/my_calendar`, `apps/tables`, `apps/ui`, and `templates/partials/_offcanvas/` (add payment, send invoice).

## 8. Rules for whoever edits this next

- **One file only.** Every drawer extends `byky/partials/drawer.html`. Never fork it per screen; never add a second drawer template. If a screen needs something new, add an optional `spec` key with a safe default.
- **Do not edit the design values** in `byky-drawer.css` — colours, radii, sizes and weights are the approved design. If something looks wrong, a Bootstrap/Vuexy rule is leaking; counter it with a narrowly scoped `.byky-drawer …` rule at the end of the file plus a one-line comment saying which rule it counters.
- **Do not re-introduce** `.form-control`, `.form-select`, `.row.g-4`, `.col-md-*`, `.btn`, `.btn-label-*` inside the drawer.
- **Keep Bootstrap's offcanvas JS** for open/close and `data-bs-dismiss`. `byky-drawer.js` only adds sizing, jump tabs and scroll tracking.
- **No new dependencies**, no build step, no SCSS, no npm.
- Sidebar files (`templates/sidebar/*`, `css/sidebar.css`, `css/sidebar-integration.css`, `js/sidebar.js`, `vertical_menu.json`) are out of scope.

## 9. Design reference

Ink `#1a1640` · muted `#4b4770` / `#6b6790` / `#8b87b0` / `#9490bb` / `#a9a6c4` /
`#c9c6dd` · hairlines `#f0eff7` / `#eeedf5` / `#e8e7f2` · tinted surfaces `#fbfaff` /
`#f6f5fc` / `#f4f3f9` · brand `#d81f26`, deep `#c2141a`, dark `#a80f14`, light `#f04a50`,
wash `#fdeced`, border `#f3c3c5` · green `#1f9d63` · Sora 500/600/700 ·
inputs 42px tall, 11px radius · buttons 9px radius · drawer body padding 24px.

## 10. Acceptance checks after any conversion

1. Trigger opens the drawer; veil click, Esc and Cancel all close it.
2. A 3-field screen opens at 440px single-column with **no** section header and **no** jump tabs.
3. A 20+ field screen opens at 720px two-column with jump tabs; clicking the last tab scrolls the body and moves the underline.
4. Scrolling moves the highlight through the sections; the first section is highlighted at rest.
5. Section titles stay pinned while their fields scroll under them.
6. Footer stays visible at every field count; Save is solid `#d81f26`.
7. Below 768px the drawer is full-width and single-column.
8. Zero console errors; no `.form-control` or `.btn` inside `.byky-drawer`.
