# BYKY ERP — Frontend Design & Implementation Reference

Authoritative guide for building the BYKY frontend. Read this **before writing any
template, component, or style**. Its purpose is to keep 109 screens visually and
structurally identical, and to prevent the alignment / padding / spacing / overlap /
responsive drift that comes from hand-rolling components.

---

## 1. Project Context

**BYKY Enterprise Vehicle Rental Management System** — a re-development of a legacy
ASP.NET WebForms ERP onto Django + the Vuexy admin template.

- **16 modules, 109 screens.** Specs in `byky Docs/BYKY_ERP_FSD_Module*.pdf`.
- Each FSD screen is specified to a 26-point standard. The sections that are
  **binding contract**: §11 field-level spec, §12 grid spec, §15 validation matrix,
  §16 business rules, §21 buttons, §22 search filters, §23 defaults, §24 permissions.
- §5 "Visual Screen Layout (Wireframe)" is a **transcription of the legacy .aspx**,
  not a design mandate. See §8 of this document.

### Current phase: CLICKABLE WIREFRAME / PROTOTYPE ONLY

The prototype must *behave* like a real application from the user's point of view.
The data underneath is static.

**DO NOT IMPLEMENT — this phase:**

| Not in scope | Notes |
|---|---|
| Database integration | SQLite may hold seed rows for display only |
| Backend APIs / REST endpoints | No DRF, no JSON APIs |
| CRUD write operations | Forms submit to nothing, or redirect to the list |
| Authentication logic | **No login at all** — `/` opens straight on the dashboard |
| Business logic / validation rules | Client-side visual validation only, for demo feel |
| Real data synchronisation | No ETL, no sync jobs |
| Production data management | No migrations beyond display models, if any |

**DO IMPLEMENT:** every screen, every navigation path, every tab, every drawer,
every filter control, every button — all clickable, all leading somewhere sensible.

---

## 2. Repository Map

```
byky-main/
├── CLAUDE.md                      ← this file
├── byky Docs/                     ← 16 FSD PDFs (the requirements)
├── byky assets/Byky_logo.png      ← client logo (replaces Vuexy brand)
├── design-files/figma/*.zip       ← Vuexy Figma UI kit (167MB .fig, open in Figma)
└── django-version/
    ├── full-version/              ← ★ BUILD HERE
    │   ├── apps/                  ← 29 demo apps = the component library
    │   ├── templates/layout/      ← master + 6 layouts + partials
    │   ├── config/
    │   │   ├── settings.py
    │   │   ├── template.py        ← TEMPLATE_CONFIG (theme, layout, skin)
    │   │   └── urls.py            ← route registry
    │   ├── src/                   ← SCSS + JS sources (Gulp/Webpack)
    │   │   ├── scss/_bootstrap-extended/_variables.scss  ← spacing scale
    │   │   └── assets/js/         ← per-page JS (app-user-list.js etc.)
    │   └── web_project/           ← TemplateLayout / TemplateHelper
    ├── starter-kit/               ← stripped shell, 30 templates
    └── template-config/demo-1..6.py
```

### Build on `full-version`, not `starter-kit`

`starter-kit` has only 30 templates. `full-version` has 205 — every one of which is a
working reference implementation we copy from. Keep the demo apps installed during the
wireframe phase as a **living component library**; strip them before production.

### 2.1 Local setup

No virtualenv exists yet. Python 3.10.12 is present; Django 5.2.5 supports 3.10–3.13.

```bash
cd django-version/full-version
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver          # http://127.0.0.1:8000
```

> **Restart the server after ANY change — templates included.** This project does not
> pick up edits reliably without it, despite `DEBUG=True`.
>
> **Restart the server after ANY `.py` change** — views, `urls.py`, `data.py`,
> `seed.py`. Templates reload per request; Python does not. `pkill -f "manage.py
> runserver"` is unreliable here: kill by PID (`ps aux | grep "[m]anage.py runserver"`)
> and confirm the port is actually free before restarting, or you will silently test
> the previous URLconf. This produced false "screen renders fine" results twice —
> once the check only passed because the string being grepped was a static
> `placeholder=` attribute, not rendered data.

`.env` is already present. `db.sqlite3` ships with demo rows.
Front-end asset build (`src/`, Gulp/Webpack) is **not** needed — compiled assets are
already in `src/assets/`. Only run the build if SCSS variables change.

---

## 3. BYKY Brand

### 3.1 Logo

Source artwork: `byky assets/Byky_logo.png` — a red + black chopper-style bike with
a red italic "Byky" wordmark, on a **transparent** background (80% of pixels are
alpha 0; it is not a black-background image).

Derived assets live in `src/assets/img/branding/`:

| File | What it is | Used for |
|---|---|---|
| `byky-logo.png` | Full lockup, trimmed to its alpha bounds. Artwork untouched. | Auth screens, print, anywhere with room |
| `byky-mark.png` | Bike only — wordmark and baseline rule erased, re-trimmed. | Sidebar brand slot (`templates/partials/logo.html`) |

The mark is paired with the word "BYKY" rendered as text in `.app-brand-text`, so
the brand stays legible when the sidebar collapses. **Never** recolour, redraw,
stretch or re-proportion the artwork; the only permitted edits are the crops above.

### 3.2 Primary colour — `#CC0000`

Chosen by research, not taken raw from the logo.

- Logo red is `#EC0000` (H 0°, S 100%, **V 92.5%**) — correct for a logo, too hot as
  a UI primary across dense tables for a full shift.
- `#CC0000` keeps the logo's **hue (0°) and saturation (100%)** and drops brightness
  to **80%**. It is the red the motorcycle industry uses (Honda, Ducati, Target).
- **Contrast 5.89:1 on white** — clears WCAG AA both as white text on a red fill and
  as red text/links on white.
- **ΔE 25.6 from Vuexy's `danger` `#FF4C51`**, which is itself red. This constraint
  is why the obvious "enterprise reds" were rejected: `#DC2626` (ΔE 14.7),
  `#D32F2F` (13.4), `#DA1E28` (14.2) and `#C62828` (17.1) all collide with `danger`
  and would make status badges ambiguous. Desaturating moves *toward* the coral
  danger, so the fix is lower brightness, not lower saturation.

Applied by `src/assets/css/byky-brand.css`, loaded after `core.css` in
`templates/layout/partials/styles.html`.

| Token | Value | Derivation |
|---|---|---|
| `--bs-primary` | `#CC0000` | brand |
| `--bs-primary-rgb` | `204, 0, 0` | |
| hover / active bg | `#B80000` | ×0.902, Vuexy's own hover ratio |
| hover border | `#A30000` | ×0.800 |
| active border | `#990000` | ×0.748 |
| focus shadow rgb | `212, 38, 38` | 15% toward white |
| `--bs-primary-bg-subtle` | `#F7D6D6` | 16% on white |
| `--bs-primary-border-subtle` | `#EB9B9B` | 39.3% on white |
| `--bs-primary-text-emphasis` | `#520000` | ×0.40 |

`.btn-primary` and `.btn-outline-primary` hardcode their own scoped `--bs-btn-*`
variables in `core.css`, so overriding `:root` alone is **not** enough — the
override file redefines them too. `.bg-label-primary`, `.text-primary` and
`.bg-primary` all derive from `--bs-primary` via `color-mix()`/`rgba()` and follow
automatically.

**Use red as an accent, never as large fills** — buttons, active nav, links, badges.
YouTube, Netflix and Target all have red brands and deliberately avoid red as their
dominant UI surface colour.

### 3.3 Light theme only

Dark mode is **out of scope**. In `config/template.py`: `theme: 'light'`,
`has_customizer: False`, `display_customizer: False`, `has_semi_dark: False`.

Turning the customizer off also removes the navbar's light/dark/system switcher
(it is wrapped in `{% if has_customizer %}` in
`templates/layout/partials/navbar/navbar.html`) and the customizer JS entirely.
That is why the brand red is applied through CSS rather than the `primary_color`
setting — `primary_color` only takes effect while the customizer JS is loaded.

**Do not** add `[data-bs-theme="dark"]` rules, dark-mode media queries, or a theme
toggle.

---

## 4. The Vuexy Design System — Non-Negotiables

### 4.1 Spacing scale — READ THIS FIRST

Vuexy **overrides Bootstrap's default spacer map**
(`src/scss/_bootstrap-extended/_variables.scss:142`). The numbers do not mean what
they mean in stock Bootstrap:

| Class suffix | Value | | Class suffix | Value |
|---|---|---|---|---|
| `0` | 0 | | `5` | 1.25rem |
| `50` | 0.125rem | | `6` | **1.5rem** |
| `1` | 0.25rem | | `7` | 1.75rem |
| `1_5` | 0.375rem | | `8` | 2rem |
| `2` | 0.5rem | | `9` | 2.25rem |
| `3` | 0.75rem | | `10` | 2.5rem |
| `4` | **1rem** | | `11` | 2.75rem |
| | | | `12` | 3rem |

> **`mb-3` is 0.75rem here, not 1rem.** Bootstrap habits produce cramped, subtly
> inconsistent layouts. Use the Vuexy conventions below instead of guessing.

**House spacing conventions — use these exact values:**

| Context | Class |
|---|---|
| Gap between cards in a row | `g-6` (or `gy-6`) |
| Bottom margin of a card / section | `mb-6` |
| Form field group spacing | `mb-6` (`mb-4` inside offcanvas/modal) |
| Card body padding | default (`.card-body`) — never override |
| Icon-to-text gap inline | `me-1_5` or `me-2` |
| Page-header bottom margin | `mb-6` |
| Button group gap | `gap-4` |

### 4.2 Colour usage

Semantic only — never a hex value in a template.

- Solid: `bg-primary` `bg-success` `bg-danger` `bg-warning` `bg-info` `bg-secondary`
- Soft/label (Vuexy's signature): **`bg-label-*`** — used in 56 demo templates.
  This is the default for badges, avatar tiles, and status chips.
- Text: `text-primary` `text-success` `text-danger` `text-heading` `text-body-secondary`
- Buttons: `btn-primary` (one per screen), `btn-label-secondary`, `btn-label-danger`,
  `btn-outline-*`, `btn-icon` (icon-only)

Primary is `#CC0000` via `src/assets/css/byky-brand.css` (see §3.2) — never set it
per-component, and never write a hex in a template.

**`primary` and `danger` are both red.** Keep their jobs strictly separate: `primary`
means "the main action / brand", `danger` means "destructive or failed". A Delete
button is `btn-label-danger`, never `btn-primary`. A Rejected badge is
`bg-label-danger`, never `bg-label-primary`.

### 4.3 Typography

- Page/section headings: `<h5 class="mb-0">` inside `.card-header`
- Entity name in a detail header: `<span class="h5">`
- KPI numbers: `<h4 class="mb-0">`
- Supporting text: `<p class="mb-0">` or `<small>`
- Never set `font-size`, `font-weight`, or `font-family` inline.

**One deliberate exception:** the sidebar (`src/assets/css/sidebar.css`) loads
"Sora" (300–800) for its own rail — a scoped, approved carve-out from the "Byky
Sidebar v2" redesign, not drift. The dashboard (`src/assets/css/byky-dashboard.css`)
also uses Sora, matching its own approved design, plus "IBM Plex Mono" for the
vehicle-code chips in Recent Rental Agreements. Every other screen stays on
Public Sans.

### 4.4 Icons

Tabler, via the `icon-base` convention:

```html
<i class="icon-base ti tabler-users icon-26px"></i>   <!-- KPI tile -->
<i class="icon-base ti tabler-lock icon-sm me-1_5"></i> <!-- inline w/ label -->
```

Sizes: `icon-xs` `icon-sm` `icon-md` `icon-lg` `icon-22px` `icon-26px`.
Full catalogue: `/icons/tabler/` (`apps/icons/templates/icons_tabler.html`).

### 4.5 Radius / shadow / borders

Inherited from `.card`, `.btn`, `.form-control`. **Never** write a custom
`border-radius` or `box-shadow`. Section dividers use `<hr>` or
`.border-bottom` / `.border-end`, matching `card-widget-separator`.

### 4.6 Responsive

Light theme only — no dark-mode rules (§3.3). Always pair the mobile and desktop class:
`flex-column flex-md-row`, `col-sm-6 col-xl-3`, `d-none d-sm-block`,
`gap-4 gap-md-0`. Tables go inside `.card-datatable` or `.table-responsive` —
**never** let a table set the page's horizontal scroll.

---

## 5. Template Discovery Algorithm

**If the screen you're building belongs to a module already migrated to the
shared `.scr-*` design system** (currently: CMS, and Global Application
Configuration & Settings) **read `byky-screen-design-system.md` (repo root)
first** — it documents that system's shared CSS/JS, its list+drawer and
form patterns, and how to extend it safely, and supersedes the Vuexy lookup
below for that screen. Everything else in this repo still goes through the
algorithm below.

Before building **any** UI block, run this in order. Do not skip to step 4.

```
1. Does Vuexy already ship this component?        → reuse it
2. Does another project page implement the pattern? → adapt it
3. Can existing Vuexy components be combined?     → compose it
4. Only then: minimal custom component, matching §4
```

**Search commands that work:**

```bash
cd django-version/full-version
grep -rl "offcanvas"       apps/*/templates/*.html
grep -rl "nav-pills"       apps/*/templates/*.html
grep -rl "bs-stepper"      apps/*/templates/*.html
ls apps/*/templates/                       # 205 reference screens
```

### 5.1 Component Lookup Table — copy from these files

| UI block needed | Source file (under `django-version/full-version/`) |
|---|---|
| **Page layout (vertical menu)** | `templates/layout/layout_vertical.html` |
| **Blank/auth layout** | `templates/layout/layout_blank.html` |
| **KPI / stat tile row** | `apps/users/templates/app_user_list.html` (lines 35–120) |
| **KPI row w/ separators** | `apps/ecommerce/templates/app_ecommerce_order_list.html` |
| **List + filters + DataTable + pagination + export** | `apps/users/templates/app_user_list.html` + `src/assets/js/app-user-list.js` |
| **Advanced DataTable** | `apps/tables/templates/tables_datatables_advanced.html` |
| **Plain table** | `apps/tables/templates/tables_basic.html` |
| **Offcanvas (drawer) create form** | `apps/users/templates/app_user_list.html` → `#offcanvasAddUser` |
| **Full-page form (project CRUD pattern)** | `apps/transactions/templates/transactions_add.html` |
| **Form layouts (vertical/horizontal/sticky)** | `apps/form_layouts/templates/form_layouts_*.html` |
| **Form validation feedback** | `apps/form_validation/templates/form_validation.html` |
| **Multi-step wizard** | `apps/form_wizard/templates/form_wizard_numbered.html`, `wizard_ex_*.html` |
| **Detail view with tab pills** | `apps/users/templates/app_user_view_account.html` (lines 163–183) |
| **Detail header + status badges + side panel** | `apps/ecommerce/templates/app_ecommerce_order_details.html` |
| **Profile header with banner** | `apps/pages/templates/pages_profile_user.html` |
| **Settings / configuration screen** | `apps/pages/templates/pages_account_settings_account.html` |
| **Role & permission matrix** | `apps/access/templates/app_access_roles.html`, `app_access_permission.html` |
| **Timeline / activity feed** | `apps/extended_ui/templates/extended_ui_timeline_basic.html` |
| **Charts (ApexCharts)** | `apps/charts/templates/charts_apex.html` |
| **Dashboard composition** | `apps/dashboards/templates/dashboard_analytics.html`, `dashboard_crm.html` |
| **Fleet dashboard + map** | `apps/logistics/templates/app_logistics_dashboard.html`, `app_logistics_fleet.html` |
| **Leaflet map** | `apps/maps/templates/maps_leaflet.html` |
| **Kanban board** | `apps/kanban/templates/app_kanban.html` |
| **Calendar / scheduler** | `apps/my_calendar/templates/app_calendar.html` |
| **Invoice list / preview / add** | `apps/invoice/templates/app_invoice_*.html` |
| **Modals / dialogs** | `apps/modal_examples/templates/modal_examples.html`, `apps/ui/templates/ui_modals.html` |
| **Confirm dialog (delete)** | `apps/extended_ui/templates/extended_ui_sweetalert2.html` |
| **Toasts / notifications** | `apps/ui/templates/ui_toasts.html` |
| **Breadcrumbs & pagination** | `apps/ui/templates/ui_pagination_breadcrumbs.html` |
| **Badges (status chips)** | `apps/ui/templates/ui_badges.html` |
| **Avatars** | `apps/extended_ui/templates/extended_ui_avatar.html` |
| **Cards (all variants)** | `apps/cards/templates/cards_*.html` |
| **Accordion / FAQ / collapsible sections** | `apps/pages/templates/pages_faq.html` |
| **File upload (Dropzone)** | `apps/forms/templates/forms_file_upload.html` |
| **Date / time pickers (flatpickr)** | `apps/forms/templates/forms_pickers.html` |
| **Select2 dropdowns** | `apps/forms/templates/forms_selects.html` |
| **Switches / toggles** | `apps/forms/templates/forms_switches.html` |
| **Rich text editor (Quill)** | `apps/forms/templates/forms_editors.html` |
| **Input masks / groups** | `apps/forms/templates/forms_input_groups.html` |
| **Tree view** | `apps/extended_ui/templates/extended_ui_treeview.html` |
| **Empty / error / 404 / maintenance states** | `apps/pages/templates/pages_misc_*.html` |

### 5.2 Vendor libraries already bundled — do not add new ones

`src/assets/vendor/libs/`: datatables-bs5 (+buttons, responsive, select, rowgroup,
fixedheader, fixedcolumns), select2, flatpickr, bootstrap-daterangepicker, dropzone,
quill, @form-validation, bs-stepper, apex-charts, chartjs, leaflet, mapbox-gl,
fullcalendar, jkanban, sweetalert2, notyf, tagify, cleave-zen, nouislider,
perfect-scrollbar, shepherd, jstree, sortablejs, swiper, jquery-repeater, raty-js.

**If a need is covered by this list, adding another library is a defect.**

---

## 6. BYKY App Structure

Generated in Phase 0. One Django app per FSD module, plus a shared core.

```
apps/
  byky_core/                 shared view base, seed data, shared partials
    views.py                 BykyScreenView -- every BYKY screen extends this
    seed.py / seed_data.json see §12
    templates/byky/partials/ page_header, kpi_row, status_badge, empty_state,
                             screen_placeholder
  byky_cms/          9   byky_reports/       8   byky_scheduler/     5
  byky_hrms/         6   byky_sfa/           6   byky_sysadmin/      5
  byky_ims/         20   byky_rfid/          5   byky_api/           5
  byky_rms/          8   byky_mobile/        7   byky_security/      5
  byky_tracking/     4   byky_notification/  5   byky_integration/   5
                         byky_wallet/        5
  byky_fare/         2   (Fare & Schemes -- not an FSD module; built from the
                         client's two HTML mockups in `byky Docs/`)
```

Each module app holds `urls.py` (one route per FSD screen) and
`templates/<slug>_<screen>.html`. Every route is registered in `config/urls.py`
and appears in the sidebar; all return HTTP 200.

> **`byky_sysadmin`, not `byky_admin`** — the slug `admin` collides with Django's
> own `/admin/`, which is registered first in `config/urls.py` and swallows the
> routes. Do not rename it back.

### Shared view

```python
from apps.byky_core.views import BykyScreenView
```

`BykyScreenView` calls `TemplateLayout.init`, then puts the screen's FSD identity
into the context: `screen_no`, `screen_title`, `module_label`, `legacy_page`,
`tier`, `tier_label`, `phase`, `purpose`, `layout`. Pass these as `as_view()`
kwargs in `urls.py` — never hardcode them in a template.

### Screen placeholder

Any screen not yet built renders `byky/partials/screen_placeholder.html`, showing
its real FSD purpose, specified layout, legacy `.aspx` page, tier and phase. A
walkthrough therefore stays honest about what is built and what is scheduled. As a
module gets built, replace the template body — the route and menu entry already exist.

### No authentication

There is no login. `config/urls.py` and every module's `urls.py` route straight to the
view — no `login_required` anywhere — so `/` opens on the dashboard and all 109 screens
are reachable cold. This is deliberate for the walkthrough; the navbar shows a static
"Administrator / SuperAdmin" identity and no Log out, because there is nothing to log
out of.

The `auth` app and its templates remain on disk for the production phase. Do not
reintroduce `login_required` while the prototype is being demoed.

### The demo strip (Phase 0b)

The 29 Vuexy demo apps are **unregistered** from `INSTALLED_APPS` and `config/urls.py`.
Installed now: `auth` (the real login app), `apps.byky_core`, and the 16 `apps.byky_*`.

Their **155 templates remain on disk** under `apps/<demo_app>/templates/` and are still
the component library (§5.1). Read them with `cat`; they do not need to be installed.

Two consequences to respect:

- `apps/pages/templates/pages_misc_error.html` and `pages_misc_not_authorized.html` were
  **copied into `apps/byky_core/templates/`** because the 404/403/400/500 handlers in
  `config/urls.py` load them by bare filename.
- `src/assets/css/demo.css` **stays linked**. Despite its name it carries the
  `layout-navbar-fixed` padding rules the fixed navbar depends on; only its `.demo-*`
  helper classes are demo-specific.

The navbar (`templates/layout/partials/navbar/navbar.html`) is reduced to the sidebar
toggle plus the user dropdown (username, group, Log out). Search, language switcher,
quick links, the notifications dropdown and the Billing/Pricing/FAQ items are gone --
they were placeholder content pointing at demo routes.

### The dashboard

`/` is `index`, owned by `apps/byky_core/urls.py` -> `BykyDashboardView` ->
`apps/byky_core/templates/byky_dashboard.html` + `src/assets/js/byky-dashboard.js`.

Adapted from Vuexy's `dashboard_analytics` -- same grid, card shapes, ApexCharts, Swiper
and DataTable. Every figure comes from `seed.dashboard()`. Series reach the JS through a
`{{ chart_data|json_script:"byky-chart-data" }}` tag; nothing is hardcoded in the JS.

### Revenue figures are indicative, and confined to one module

The client's files carry no dates, prices or transactions, so **no revenue figure can
be derived from them**. `apps/byky_core/sales.py` generates indicative AED figures
that are:

- **derived from the real fleet** — a station's revenue tracks the vehicles it
  actually holds, so the shape matches the real network;
- **deterministic** — seeded, so numbers never jump between page loads;
- **stated once** — the utilisation assumptions (1.6 rentals/vehicle/day, 1.5 h each,
  AED 25/h) are constants at the top of the module.

Cards showing them carry an **Indicative** badge, and the dashboard footer says which
figures are BYKY's own and which are not. When the client supplies rental data,
replace the functions in `sales.py` and every dashboard figure follows.

**Never reuse these figures on operational screens.** The dashboard is the only place
they belong.

### Maps

`apps/byky_core/geo.py` holds approximate coordinates for all 36 stations (the
published locations of the real parks and corniches). Leaflet, with a keyless tile
provider — never Mapbox, which needs an access token.

- `byky/partials/station_map.html` + `src/assets/js/byky-map.js` — the shared map,
  used on Fleet Telematics Registry (5.2) and Station Address Mapping (1.7)
- **Basemap is Esri's light-grey canvas + its reference (label) layer**, not OSM's
  standard tiles. OSM renders place names in the local script — Arabic across the
  UAE — and this dashboard is read in English. Esri's canvas labels are latin, and
  the neutral grey base keeps the red station markers dominant.
- **Tiles need a Referer.** Django defaults `SECURE_REFERRER_POLICY` to `same-origin`,
  which strips it and makes tile servers return 403 — the map renders as a wall of
  "Access blocked" tiles. `config/settings.py` sets
  `strict-origin-when-cross-origin`; do not remove it.
- Two alternatives were tried and rejected: CARTO now watermarks keyless browser
  requests with "KEY REQUIRED", and Wikimedia's `osm-intl` (latin labels) returns 403
  to external referers.
- Leaflet is ~500 KB, so `generic_screen.html` loads it only when the view sets
  `show_map`
- The dashboard has its own richer map with revenue in the popups
- The Kuwait station is plotted but excluded from auto-fit, or the whole Gulf gets
  framed and the UAE network shrinks to nothing
- These coordinates are **not** survey data — FSD 1.7 still needs exact per-station
  GPS from the client

### Shared partials

| Partial | Use |
|---|---|
| `byky/partials/privilege_matrix.html` | **Tier D**, reused by all 16 modules. Role selector + role x screen x 7-permission grid (Access, Create, Read, Update, Print, Approve, Delete) + Select All per row |
| `byky/partials/awaiting_data.html` | Screen built, records not supplied yet. Pass `needs` a **short noun phrase** ("antennas", "tariff plans") — it completes the sentence "This screen is ready — X will appear once added." Keep it human; never phrase it as a system reporting a missing input |
| `byky/partials/station_map.html` | Leaflet/OpenStreetMap station map; view supplies `map_data` from `geo.station_points()` |

`page_header.html` keeps the breadcrumb, title and primary action on **one line**, with
the description beneath at `small`. Do not restack it into three blocks.

Missing values have two forms: `seed.NOT_CAPTURED` (`— not captured —`) for forms and
detail views, and `seed.NOT_CAPTURED_SHORT` (`—`) for **grid cells**, where the long
string wraps and triples row height. Use the short form in any table column.

Legacy `.aspx` filenames are build metadata. They appear on the unbuilt-screen
placeholder but must **never** be shown on a finished client-facing screen.
| `byky/partials/page_header.html` | Title, breadcrumb parent, subtitle, optional primary action |
| `byky/partials/kpi_row.html` | KPI tile row; pass `kpis` list of dicts |
| `byky/partials/status_badge.html` | Approval / active chip — never uses `primary` |
| `byky/partials/empty_state.html` | Legitimately empty list or panel |
| `byky/partials/screen_placeholder.html` | Unbuilt screen |

---

## 7. Django Page Skeleton

Every screen extends `layout_path` and fills these blocks. Copy this verbatim.

```django
{% extends layout_path %}
{% load static %}
{% load i18n %}

{% block title %}Branch Management - Company Management{% endblock title %}

{% block vendor_css %}
{{ block.super }}
<link rel="stylesheet" href="{% static 'vendor/libs/datatables-bs5/datatables.bootstrap5.css' %}" />
{% endblock vendor_css %}

{% block vendor_js %}
{{ block.super }}
<script src="{% static 'vendor/libs/datatables-bs5/datatables-bootstrap5.js' %}"></script>
{% endblock vendor_js %}

{% block page_js %}
{{ block.super }}
<script src="{% static 'js/byky-cms-branch-list.js' %}"></script>
{% endblock page_js %}

{% block content %}
  <!-- screen content -->
{% endblock %}
```

**Rules**
- `{{ block.super }}` is mandatory in every block — omitting it drops the base assets.
- Vendor CSS/JS go in `vendor_css` / `vendor_js`; page logic in `page_js`.
- Never add a `<script>` or `<style>` inside `{% block content %}`.

### 7.1 View skeleton

Every view must go through `TemplateLayout.init` or the layout context is missing:

```python
from django.views.generic import TemplateView
from web_project import TemplateLayout

class BranchListView(TemplateView):
    def get_context_data(self, **kwargs):
        context = TemplateLayout.init(self, super().get_context_data(**kwargs))
        context.update({"branches": BRANCHES})   # static seed data
        return context
```

Reference implementation: `apps/transactions/` — the one app wired end-to-end
(list / add / update / delete views + templates + fixtures). **Clone its shape.**

### 7.2 Layout switching

Set per view via `context["layout"]` before `TemplateLayout.init`, or globally in
`config/template.py`. Options: `vertical` (default), `horizontal`, `blank`, `front`.
Never duplicate a layout file to change one thing.

---

## 8. Screen Design Approach — Four Tiers

**Do not force all 109 screens into one layout.** Screen counts are confirmed three ways per module (navigation map, §4 header, and
actual §4 screen blocks) and all agree: 9+6+20+9+4+8+6+5+7+5×7 = **109**.

FSD 4.5 *Rental Tariff & Fare Setup* is the one deliberate departure: it was removed
from the build because the client's own Fare Entry and Scheme Creation mockups supersede
it, and keeping both would have given the same tariff two places to live. RMS therefore
ships 8 screens, and the built total is 108 FSD screens + 2 Fare & Schemes = 110 routes.

The legacy split-panel
(form left, grid right) is an ASP.NET WebForms artifact and is rejected: Module 1.1's
own grid spec is 7 columns / 1020px, which cannot fit a half-width panel without a
nested horizontal scrollbar.

**Rule: honour the FSD's data and behaviour exactly; modernise the presentation.**

### Tier A — Thin masters (3–5 fields) → list page + offcanvas drawer

70 screens: Category, Sub-Category, Brand, Unit, Department, Designation, Grade,
Order Status, Features, Location, Delivery Location, Vehicle Type…

Full-width list; **Add** opens an offcanvas over it. The grid stays visible behind, so
rapid consecutive data entry (the one thing split-panel was good at) is preserved.

> Source: `app_user_list.html` (list + `#offcanvasAddUser`)

### Tier B — Rich entities (12+ fields) → dedicated `/add` and `/<pk>/edit` pages

8 screens: Company Details (1.1), Branch Management (1.4), Employee Personal Data
(2.1), Stock Item (3.1), Ecom Stock Item (3.9), Promo Code (3.12), Customer Details
(4.1), Antenna Calibration (8.3).

Full-width form card, split into labelled sections (Basic Information / Contact /
Configuration / Additional). Use tabs or a stepper when it exceeds ~15 fields.

> Source: `transactions_add.html` + `form_layouts_vertical.html`; wizard from
> `form_wizard_numbered.html`

### Tier C — Read-only monitors & reports → filter bar + full-width grid, no form

15 screens. All of Module 6 (7 reports), plus 3.18 Live RFID Monitoring, 3.19 Alerts,
8.4 RFID Gate Monitor, 13.4 Audit Log, 16.4 System Health.

Filter card on top (date range, branch, status), KPI row where the FSD implies
totals, then the grid with export buttons.

> Source: `tables_datatables_advanced.html` + `charts_apex.html` for report visuals

### Tier D — The 16 `*Privilege` screens → permission matrix

16 screens.

Role × Screen × CRUD checkbox grid. **One shared component, reused 16 times.**

> Source: `app_access_roles.html` / `app_access_permission.html`

### Universal rules

- **`Save & New`** button beside `Save` on every Tier A/B form.
- Approval-flow screens get a status badge
  (`bg-label-warning` Pending / `bg-label-success` Approved / `bg-label-danger` Rejected)
  plus an `[Approve] [Reject]` button group, shown only for SuperAdmin.
- Cascading dropdowns (Country → State → Location → Branch) use **one** shared JS
  helper, not a per-screen copy.

---

## 9. Screen Anatomy Templates

### 9.1 List view

```
Page header ── title · description · [Primary Action]
KPI row (optional)         .row.g-6.mb-6 → .col-sm-6.col-xl-3 > .card
Filter card                .card-header + 3 × .col-md-4 selects
Data table                 .card-datatable > table.datatables-*
Pagination                 (DataTables layout.bottomStart/bottomEnd)
```

### 9.2 Detail view

```
Breadcrumb
Header ── entity name · status badges · [Edit] [Delete] [Approve]
Summary card / KPI strip
Tab pills (.nav-align-top > ul.nav.nav-pills.mb-6)
Section cards per tab
Related data table
Activity / audit timeline
```

Never dump every field into one large card. Build hierarchy.

### 9.3 Form view

```
Page header + [Back]
Form card
  ├── Basic Information
  ├── Contact / Related Information
  ├── Configuration
  └── Additional Information
[Save] [Save & New] [Cancel]
```

---

## 10. Visual Quality Bar

This is a wireframe, but it must **not look like a wireframe**. It should read as a
polished product — achieved by *composing Vuexy components*, not by inventing designs.

**Required:** modern · clean · scannable · professional · interactive · consistent.

**Avoid:**
- Walls of text
- Large empty regions
- Rows of identical cards with no hierarchy
- Every screen being "just a table"
- Generic dashboards with no visual focus
- The same layout repeated across all 16 modules

**Split-screen layouts are prohibited** unless showing two things at once is a clear
usability win (e.g. a live map beside a vehicle list in Module 5/8). Prefer full-page
detail views, tabs, cards, drawers, dialogs, expandable rows, progressive disclosure.

---

## 11. Clickable Prototype Requirements

Every meaningful affordance navigates somewhere. Nothing is a dead `href="#"` unless
it is a genuinely inert demo control.

Must be clickable: sidebar items · menu groups · table rows · View/Edit buttons ·
tabs · cards · primary actions · Back buttons · breadcrumbs · dialog actions ·
wizard steps · pagination.

Reference journey:

```
Branch List → click row → Branch Detail → Departments tab
     → click department → Department Detail → Back → Branch Detail → breadcrumb → Branch List
```

Write-actions (Save / Delete / Approve) show a SweetAlert2 or toast confirmation and
return to the list. **No data is persisted.**

---

## 12. Data Strategy

Two client Excel files in `byky Docs/` are the source of realistic sample data:
`Location and Employee Data.xlsx` and `VehicleDetails.xlsx`.

They are reconciled once by
`scratchpad/build_seed.py` into **`apps/byky_core/seed_data.json`**, read through
**`apps/byky_core/seed.py`**:

```python
from apps.byky_core import seed
seed.STATIONS      # 36 stations
seed.EMPLOYEES     # 99 employees
seed.VEHICLES      # 1,060 vehicles
seed.counts()      # headline figures for KPI tiles
seed.vehicles_at(station_code)
seed.station_by_code(code)
seed.employee_by_no(emp_no)
seed.NOT_CAPTURED  # "— not captured —"

# Dashboard aggregations -- all derived, none invented
seed.dashboard()          # every figure the landing page shows
seed.by_emirate()         # [(emirate, station_count, fleet_size)]
seed.by_category()        # [(category, count)]
seed.by_vehicle_type()    # [(type, count)]
seed.by_profession()      # [(profession, count)]
seed.top_stations(n)      # stations ranked by fleet
seed.station_rows()       # directory rows with share / share_scaled
seed.fleet_curve()        # per-station fleet sizes, ranked
```

`seed_data.json` is regenerated by `apps/byky_core/build_seed.py` when the client sends
corrected data. It uses an explicit alias map, not fuzzy matching, so every
reconciliation decision stays auditable.

### What the data actually contains

| Entity | Rows | Fields with data |
|---|---|---|
| Stations | 36, across 8 emirates | code, name, emirate, vehicle_count |
| Employees | 99, `BYKY001`-style ids | emp_no, name, profession (9 kinds) |
| Vehicles | 1,060, every number and barcode unique | number, barcode, category (8), type (18), station |

Emirates: Al Ain 9 · Dubai 6 · Abu Dhabi 5 · Sharjah 5 · Ajman 4 · Fujairah 3 ·
Ras Al Khaimah 3 · Kuwait 1. Vehicle barcodes map directly onto Module 8's RFID
tag EPC.

### Reconciliation decisions already made

- The two sheets disagreed on station names. **Merged**, using an explicit alias map
  in `build_seed.py` (no fuzzy matching) so every decision is auditable.
- Kept the 3 stations that appear only in the vehicle sheet: `Ajman Corniche`,
  `Dubai` (looks like an unassigned/holding bucket), `Hilton Kuwait Resort`.
- `Qidfa Beach` exists in the location sheet with **0 vehicles** — kept, and a useful
  empty-state to demo.
- Display names are spell-corrected for screen use (`Abudhbi` → `Abu Dhabi`,
  `Sooter` → `Scooter`, `RAK Cor 1` → `RAK Corniche 1`), and duplicate vehicle types
  merged (23 raw → 18 canonical).

### Employee fields that do not exist

The staff sheet has 26 columns but **only 4 are populated** — Employee No, Name and
Profession. Date of Join, Nationality, Passport, Visa, Labour Card, Emirates ID,
Mobile, Mother's Name, Address, UID, GDRFA File No and all bank columns are **empty
headers**.

HRMS detail screens must still render every field the FSD specifies, showing
`seed.NOT_CAPTURED` for the missing ones. **Do not invent passport numbers, Emirates
IDs, bank details or dates of birth.** The empty state doubles as a visible prompt
for the client to supply the data.

### Rules

1. Use the data only where it is relevant to that screen's user context.
2. List views carry only the fields that help a user scan and compare. Everything
   else belongs in the detail view, a tab, or an expandable row.
3. Detail views group fields by meaning (Basic / Operational / Assignment /
   Location / Related) — never one long card of every column.
4. Never render lorem ipsum, `John Doe`, or `ACME Inc.`
5. No CRUD, no APIs, no sync. Static display only.

## 13. Naming & File Conventions

| Thing | Convention | Example |
|---|---|---|
| Django app | `apps/byky_<module>/` | `apps/byky_cms/` |
| URL path | `/<module>/<entity>/<action>/` | `/cms/branch/list/` |
| URL name | `<module>-<entity>-<action>` | `cms-branch-list` |
| Template | `<module>_<entity>_<action>.html` | `cms_branch_list.html` |
| Page JS | `src/assets/js/byky-<module>-<entity>-<action>.js` | `byky-cms-branch-list.js` |
| DataTable class | `datatables-<entity>` | `datatables-branch` |
| Offcanvas id | `offcanvasAdd<Entity>` | `offcanvasAddBranch` |

Register every app's urls in `config/urls.py` and every screen in
`templates/layout/partials/menu/vertical/json/vertical_menu.json`.

### Menu — `templates/layout/partials/menu/vertical/json/vertical_menu.json`

Drives the sidebar. Verified entry shape:

```json
{ "name": "Company Management",
  "icon": "menu-icon icon-base ti tabler-building",
  "slug": "cms",
  "submenu": [
    { "url": "cms-branch-list", "name": "Branch Management", "slug": "cms-branch-list" },
    { "url": "/cms/branch/list/", "external": true, "name": "Raw path variant" }
  ] }
```

Mechanics, as implemented in `partials/menu_link_template.html`:

- `url` is a **Django URL name**, resolved with `{% url item.url %}`.
  To use a literal path instead, add `"external": true`.
- **Active state comes from `url`, not `slug`:**
  `item.url == request.resolver_match.url_name or item.url == request.path`.
  So the `url` value must equal the registered URL name exactly. `slug` is carried in
  the JSON but is not what highlights the item — do not rely on it.
- `icon` must include the `menu-icon` prefix: `"menu-icon icon-base ti tabler-*"`.
- Section divider: `{ "menu_header": "Modules" }` — **snake_case**, not `menuHeader`.
- Optional `badge`: `["danger", "5"]` → `.badge.bg-danger.rounded-pill`.
- Optional `permission`: the item renders only if
  `request.user|has_permission:<perm>` passes (`web_project/template_tags/theme.py:46`).
  **Permission-driven menu filtering already exists** — use this key for the Module
  `*Privilege` screens rather than building a new mechanism. Leave it unset during the
  wireframe phase so every screen is reachable for the demo.

The horizontal menu has its own file: `partials/menu/horizontal/json/horizontal_menu.json`.

---

## 14. Pre-Flight Checklist — run before writing any screen

1. Which FSD screen is this? Read its §11 field table and §12 grid spec.
2. Which tier (A/B/C/D) is it?
3. Break it into UI blocks (header / KPIs / filters / table / form / tabs).
4. For each block, find the source file in §5.1. **Open it. Copy its markup.**
5. Are all field names, dropdowns, buttons and filters from the FSD present?
6. Spacing uses `g-6` / `mb-6` / `mb-4` — no stray `mb-3`?
7. Colours are semantic classes — no hex anywhere?
8. Responsive pairs present (`col-sm-* col-xl-*`, `flex-column flex-md-row`)?
9. Every button/row/tab navigates somewhere?
10. Route registered in `config/urls.py` **and** `vertical_menu.json`?

---

## 15. Anti-Patterns — these are defects

**Exception to this whole section: `templates/sidebar/`, `src/assets/css/sidebar.css`,
`src/assets/js/sidebar.js`, and the dashboard's `apps/byky_core/templates/byky_dashboard.html`
+ `src/assets/css/byky-dashboard.css` + `src/assets/js/byky-dashboard.js`.** These
are separately commissioned, approved, self-contained designs ported verbatim —
"Byky Sidebar v2" and the redesigned dashboard — not screens composed from Vuexy
components. Their hex colours, custom `border-radius`, `box-shadow`, and the
"Sora"/"IBM Plex Mono" typefaces are the approved design, not drift. Do not "fix"
them toward Vuexy/Public Sans conventions, and do not reintroduce ApexCharts,
Swiper or DataTables on the dashboard — its charts are hand-drawn SVG in
`byky-dashboard.js`, reading the same `chart_data` context the old build used.

**Leaflet is the one exception, and it is required.** The Station Network card
is a real tile map, not a drawn chart. A hand-drawn bubble plot on a blank grid
was tried here and rejected on sight by the client: without coastline, streets
or satellite imagery it reads as "square pixels", and an operator placing a
station cannot use it. Every station map on the site now goes through
`src/assets/js/byky-leaflet-map.js` — opt in with
`<div class="byky-map" data-map-points="<json_script id>"></div>` plus leaflet's
vendor css/js in the page's `vendor_css`/`vendor_js` blocks. It offers three
keyless Esri basemaps (Light / Streets / Satellite) via a layer switcher; never
Mapbox, which needs an access token. Leaflet's container needs an explicit CSS
height — it cannot size itself from content the way an `<svg>` does.
`src/assets/css/sidebar-integration.css` and `src/assets/js/sidebar-layout-sync.js`
are the only files that may touch how the sidebar sits inside the rest of the
layout (positioning, width sync) — never restyle the ported components themselves
there.

- ❌ Writing custom CSS before searching `apps/*/templates/` for the pattern
- ❌ Any inline `style="..."`, hex colour, `border-radius`, `box-shadow`, or `font-size`
- ❌ Bootstrap-default spacing assumptions (`mb-3` ≠ 1rem here)
- ❌ Adding a JS/CSS library already present in `src/assets/vendor/libs/`
- ❌ A `<table>` not wrapped in `.card-datatable` / `.table-responsive`
- ❌ Split-panel form+grid layouts
- ❌ A multi-line `{# ... #}` comment — Django's `{# #}` is **single-line only**, so a
     multi-line one renders as visible text on the page. Use `{% comment %}` instead.
     This shipped visibly twice before being caught.
- ❌ Omitting `{{ block.super }}` in a template block
- ❌ A view that skips `TemplateLayout.init`
- ❌ Duplicating a layout file to change one setting
- ❌ Any dark-mode rule, `[data-bs-theme="dark"]` block, or theme toggle (§3.3)
- ❌ Using `btn-primary` for a destructive action, or `bg-label-primary` for a failed
     status — `primary` and `danger` are both red and must stay semantically separate
- ❌ Inventing passport numbers, Emirates IDs, bank details or dates of birth (§12)
- ❌ Building real CRUD, APIs, or auth in this phase
- ❌ Placeholder data that is obviously fake (`John Doe`, `Lorem ipsum`)
- ❌ A screen whose fields don't match the FSD §11 table

---

## 16. Performance

Asset weight was ~11.7 MB per page before this pass; it is now ~2.2-2.5 MB on first
load and effectively HTML-only afterwards. What did it, in order of impact:

| Change | Where | Effect |
|---|---|---|
| `GZipMiddleware` **above** WhiteNoise | `config/settings.py` | HTML 1.53 MB → 41 KB on the largest grid; static 10.4 MB → 2.5 MB |
| `whitenoise.runserver_nostatic` | `INSTALLED_APPS` | `runserver` otherwise serves `/static/` *before* the middleware chain, so nothing gets compressed in dev |
| `WHITENOISE_MAX_AGE` = 1 year | `config/settings.py` | Vendor assets cached; repeat views cost only HTML |
| Branding images resized | `src/assets/img/branding/` | `byky-mark.png` 783 KB → 10 KB (it was 1401px wide, displayed at 26px) |
| Dropped `@algolia/autocomplete-js`, `hammer.js` | `partials/scripts.html` | 365 KB; the navbar search they served no longer exists |
| Leaflet loaded only when `show_map` | `generic_screen.html` | 500 KB off every non-map screen |
| DataTables `deferRender` | `byky-cms-list.js` | 1,060-row grids stop building ~12,000 cells up front |

Rules to keep it there:

- Per-page libraries belong in each template's `vendor_css` / `vendor_js` blocks,
  **never** in `partials/scripts.html` or `styles.html`.
- Check any image you add renders near its natural size. A 1400px PNG in a 26px slot
  is the single easiest regression to introduce.
- `datatables-bootstrap5.js` (4.7 MB) and `iconify-icons.css` (2.7 MB) are minified
  vendor bundles — do not edit them; gzip and caching are the answer.

---

## 17. Open Items

### Settled

- [x] Primary red → `#CC0000` (§3.2)
- [x] Logo variants derived → `src/assets/img/branding/` (§3.1)
- [x] Light theme only, customizer and dark toggle removed (§3.3)
- [x] Station master → both Excel files merged, 36 stations (§12)
- [x] Employee gaps → render every FSD field, `seed.NOT_CAPTURED` for missing (§12)
- [x] Local venv created at `django-version/full-version/.venv`
- [x] Landing page → BYKY analytics dashboard from real data (§6)
- [x] 29 Vuexy demo apps unregistered; navbar stripped to user menu (§6)
- [x] Screen count corrected to **109** (was miscounted as 99)

### Still open

- [ ] Client sign-off on the split-panel → tiered-layout change (§8). Bring a
      traceability table (FSD field → screen → control) to that conversation.
- [ ] `Dubai` appears as a station in the vehicle sheet with no counterpart in the
      location sheet — confirm whether it is a warehouse, a holding bucket for
      unassigned stock, or a data-entry artifact.
- [ ] `Hilton Kuwait Resort` and the `Kuwait Bike` category imply a Kuwait operation
      alongside the UAE. Confirm, because Module 1 (Country & State Management)
      needs to be multi-country if so.
- [ ] Vehicle categories `Special Offer` (7), `Rent Bike` (2) and `Barsha Baby` (3)
      look like operational tags rather than real categories — confirm before
      modelling them as master data.

### Note on Modules 10–16

Their §11 field tables are thin (2–3 representative rows against 12–14 for Modules
1–3), **but §4 "Complete UI Layout" names every field explicitly for all 35 screens**.
They are buildable from spec without inventing anything — read §4, not §11, for those
modules. Example, 11.1 Wallet Refund Request: Claim ID, Customer Name, Mobile No,
Wallet Balance AED, Claimed Refund Amount AED, Refund Reason, IBAN Number, Bank Name,
plus Approve & Dispatch Payout / Reject Claim actions and a requests grid.

Do not extrapolate beyond what §4 lists for these modules.

### Build order

**Phase 0 — done.** Skeleton, brand, seed data, shared components, dashboard, demo strip.

**Phases 4-12 — done.** Modules 4-16, 74 screens, all rendering.

Modules 4-16 are rendered from **declarative specs** rather than bespoke templates:
each screen's FSD fields, grid columns and filters are declared in the module's
`views.py` and drawn by `byky/generic_screen.html`. One template for ~70 list screens
is what keeps spacing and markup identical; bespoke templates remain only where a
screen genuinely differs (CMS shift matrix, block/unblock console, privilege matrix,
dashboard, and the data-rich CMS/HRMS/IMS screens).

Real client data reaches three more screens: **Vehicle Fleet Telematics Registry**
(5.2, 1,060 vehicles), **Vehicle Type & Specification Master** (5.3, 18 models) and
**RFID Tag EPC Encoding** (8.2, 1,060 tags — the client's Barcode column *is* the EPC).

Grids render their **column headers even when empty**, with the awaiting-data state
inside the table body, so a client can see the structure each FSD screen specifies.

**Fare & Schemes — done.** Two screens (`/fare/fare-entry/`, `/fare/scheme-creation/`)
built from the client's `Fare_Entry_Advanced_UI_v3.html` and `Scheme_Creation.html`
mockups rather than an FSD module. Both are Tier B: numbered section cards, one card
per stage of the configuration.

**Repeatable multi-field rows use list + drawer, never inline inputs.** A time slab
carries ten fields and a free-item rule eight. Rendered as bare controls in a table
row they lose their labels, and the cells clip. So the grid shows formatted read-only
values (`Every day · 10:00–11:00 · AED 90.00 · 5 min`) with Edit and Delete, and
`#offcanvasTimeSlab` / `#offcanvasFreeSlab` own the labelled form — the same list +
drawer pattern as Tier A. Two-field rows (vehicle type + package) stay inline; they
are readable as they are. Apply this rule to any future grid of editable rows.

**Sidebar — replaced.** "Byky Sidebar v2" (`templates/sidebar/`,
`src/assets/css/sidebar.css`, `src/assets/js/sidebar.js`) replaces the old
`#layout-menu` Vuexy rail — full labels, no clipping, collapse-to-76px icon rail,
hover-to-peek, drag-to-resize, independently-expanding accordions with persisted
open state. All menu **data** (group names, leaf labels, URL names, badge counts,
section headers) is unchanged, still `vertical_menu.json`; the new templates only
supply markup/CSS/JS and one `svg` icon path per group (added to that same JSON).

The component's native model assumes an app-shell with internal content
scrolling, which this app doesn't use anywhere (110+ screens rely on window-level
scroll with a fixed navbar). So the sidebar is pinned `position:fixed` instead
(`src/assets/css/sidebar-integration.css`), with `.layout-page`'s
`padding-inline-start` kept in sync via a CSS custom property
(`--byky-sb-w`) that `src/assets/js/sidebar-layout-sync.js` updates on
collapse/expand/drag — keyed off `.is-collapsed`, not raw width, so hover-peek
(which visually overlays without pushing content) never touches it.
`TEMPLATE_CONFIG["menu_fixed"]` is `False` for the same reason: left `True`, Vuexy's
own `.layout-menu-fixed` padding rule would fight this one.

Leaf rows carry no icon — only the top-level Dashboard link and the 17 group rows
do, via a `top_level` flag threaded through the templates. Watch this if adding a
menu template include: Django's `{% include %}` inherits the outer context by
default, so `top_level` must be **explicitly** reset to `False` at the point the
submenu loop includes a leaf (`menu_collapsible_template.html`) — omitting it lets
`True` leak down from the enclosing group and puts an icon on every leaf.

**All of the sidebar's own internal class names were renamed to `byky-menu-*`**
(`menu-item`, `menu-link`, `menu-toggle`, `menu-icon`, `menu-sub`, `menu-header` →
`byky-menu-item`, etc. — `menu-badge`, `menu-caret`, `menu-label` and `menu-slot`
were already collision-free and kept as-is). The ported design's own generic names
matched Vuexy's own vertical-menu vocabulary in `core.css` (100+ rules combined),
which is still loaded globally — most visibly, Vuexy's `.menu-toggle::after`
chevron pseudo-element was rendering on top of every group icon. If you ever touch
these files, keep the `byky-` prefix; reverting to the bare names reopens that
whole class of bugs.

**Dashboard — replaced.** The landing dashboard (`apps/byky_core/templates/byky_dashboard.html`,
`src/assets/css/byky-dashboard.css`, `src/assets/js/byky-dashboard.js`) is a
second ported, approved design (".bd" prefix throughout), replacing the old
ApexCharts/Swiper/Leaflet/DataTables build. `views.py`, `seed.py`, `sales.py` and
`geo.py` are unchanged — the new JS reads the same `chart_data` context via
`{{ chart_data|json_script:"byky-chart-data" }}` and draws the sparkline, month
bars, ranked bars, deployment gauge and station map itself, in plain SVG. The page
restyles `#layout-navbar` to a 64px white header, but only on this page — it
arrives through `{% block page_css %}`, which Django scopes per-template, so no
other screen's navbar is affected by loading it.

**Phase 3 (IMS) — done.** All 20 screens. Four run on real client records:
Stock Item Management (1,060 vehicles — Vehicle Number is the item code and serial,
**Barcode is the RFID tag EPC**), Category Master (8), Sub-Category Master (23
category/model pairs), and Vehicle Station Mapping (1,060 real assignments). The
other 15 — brands, units, transfers, e-commerce, features, order status, promotions,
loyalty, refunds, campaigns, RFID telemetry, alerts — have no source data and show
the awaiting-data state. IMS privileges use six flags across all 20 screens.

**Phase 2 (HRMS) — done.** All 6 screens. Employee Personal Data (Tier B) carries all
22 FSD inputs over the 99 real staff records; Designation Master is **derived from the
client's own Profession column** (9 job titles with headcount), since that column is
exactly what FSD 2.3 masters. Temporary Address, Grade Master and the block log show
the awaiting-data state. Block/Unblock implements the FSD 2.5 danger/success accent
switch. HRMS privileges use **six** permissions (Access, Create, Read, Update, Approve,
Block Staff) against CMS's seven — the shared matrix is parameterised, so each module
passes its own list.

**Phase 1 (CMS) — done.** All 9 screens built against FSD sections 11/12/21/22/23:
Company Details and Branch Management as Tier B, Country & State (tabbed dual grid),
Location, Department and Branch Department Mapping as Tier A, Station Address
Mapping as Tier A over real station data, Station Working Time as the 7x4 shift matrix,
and CMS Privilege Management as the first Tier D build.

Module 1 data lives in `apps/byky_cms/data.py`, derived from `byky_core.seed`:
2 countries (UAE + Kuwait, both present in the client data), 8 states (emirates),
36 branches (one per station), 1 company. Shared JS: `byky-cms-list.js`
(DataTables + Is-Hotel toggle + privilege Select All) and `byky-cms-schedule.js`
(flatpickr HH:mm on the shift matrix).

**Four CMS entities have no source data** and render the awaiting-data state rather
than invented rows: locations, departments, branch-department mappings, and
weekly working times. Station GPS, addresses and contact numbers are likewise
"not captured". This is a live data request to the client, not a gap in the build.

Remaining phases:
Then module by module in dependency order:
**1 CMS → 2 HRMS → 3 IMS → 4 RMS → 5 TRACKING → 8 RFID → 6 REPORTS → 7 SFA →
9 Mobile → 10 → 11 → 12 → 13 → 14 → 15 → 16.**

Module 1 first because every other module references its company / branch / station
masters. Never start a module before the previous one is checked against its §11
field table and §12 grid spec.
