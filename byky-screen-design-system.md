# The `.scr-*` Screen Design System

A guide for extending BYKY's shared, hand-built screen styling to a new
module or screen. Read this before styling any screen from scratch — almost
everything you need already exists in the two shared files below.

If you haven't read `CLAUDE.md` yet, read it first. This document assumes
its rules (data honesty, spacing scale, no vendor libraries, list+drawer for
multi-field rows, etc.) and only adds the specifics of this particular
system.

---

## 1. Two systems exist — know which one you're extending

| | `.scr-*` system (this doc) | Declarative generic system |
|---|---|---|
| Files | `src/assets/css/byky-screen.css`, `src/assets/js/byky-screen.js` | `apps/byky_core/templates/byky/generic_screen.html` + `apps/byky_core/screens.py` |
| Look | Custom, "premium" — the one described here | Vuexy/Bootstrap/DataTables |
| Powers | Company Details, Country & State Management, Location Management, Branch Management, Department Management, Branch Department Mapping, Station Address Mapping, Global Application Configuration & Settings | ~70 other Tier A screens across HRMS, IMS, RMS, Tracking, RFID, Reports, SFA, Mobile, Notifications, Wallet, Integration, Scheduler |
| Status | The current direction — new module work should default to this | Not being actively extended, but not being ripped out either |

**Do not mix them on one screen.** If you're redesigning a screen that
currently uses the generic system, migrate it fully to `.scr-*` — don't add
`.scr-*` classes on top of Vuexy markup or vice versa.

The canonical **styling reference** — the file to open and copy markup
from — is:

```
apps/byky_cms/templates/cms_company_details.html
```

It was the first screen built and is kept deliberately unchanged so every
later screen has a stable, pixel-accurate example to match. When in doubt
about spacing, hierarchy, or tone, look at how Company Details does it.

---

## 2. Core files

| File | Owns |
|---|---|
| `src/assets/css/byky-screen.css` | Every `.scr-*` class: layout, cards, forms, drawers, tables, badges, pagers, maps, integrations. |
| `src/assets/js/byky-screen.js` | All `data-scr-*` behaviour: filter dropdowns, search, client-side pagination, drawers (open/close/prefill), tabs, toggle switches. One IIFE, no dependencies. |
| `src/assets/js/byky-leaflet-map.js` | The shared real-tile station map (see §7). |
| `apps/byky_cms/templates/cms_company_details.html` | The styling reference (Tier B, full-page form + drawer). |
| `apps/byky_cms/templates/cms_location_management.html` | Reference for a zero-data Tier A screen (empty state, no KPI tiles). |
| `apps/byky_cms/templates/cms_country_state_management.html` | Reference for a tabbed dual-grid screen. |
| `apps/byky_cms/templates/cms_branch_management.html` | Reference for a drawer with `<select>` fields and multiple checkboxes ("Flags"). |
| `apps/byky_sysadmin/templates/sysadmin_global_application_configuration_settings.html` | Reference for a settings/config screen (section-card form + "integration" list+drawer rows). |

**Before writing any new markup, grep both shared files** to confirm the
class or `data-scr-*` attribute you're about to use doesn't already exist —
and to see exactly how the JS reads it:

```bash
grep -n "scr-" src/assets/css/byky-screen.css
grep -n "data-scr\|dataset\." src/assets/js/byky-screen.js
```

---

## 3. Screen skeleton

Every `.scr-*` screen follows the same block wiring:

```django
{% block page_css %}
{{ block.super }}
<link rel="stylesheet" href="{% static 'css/byky-screen.css' %}" />
{% endblock page_css %}

{% block page_js %}
{{ block.super }}
<script src="{% static 'js/byky-screen.js' %}"></script>
{% endblock page_js %}

{% block content %}
<div class="scr">
  <div class="scr-head"> ... breadcrumb, title, subtitle, header buttons ... </div>
  <div class="scr-card" data-scr-noun-singular="thing" data-scr-noun-plural="things">
    <div class="scr-toolbar"> ... search + filter dropdowns ... </div>
    <div class="scr-table-scroll scr-sb">
      <table>
        <thead>...</thead>
        <tbody>
          {% for row in rows %}
          <tr class="scr-row" data-search="..." data-record-id="{{ row.json_id }}">...</tr>
          {{ row.fields_json|json_script:row.json_id }}
          {% empty %}
          <tr><td colspan="N" style="padding:0">
            <div class="scr-empty">...</div>
          </td></tr>
          {% endfor %}
        </tbody>
      </table>
    </div>
    <div class="scr-pager"> ... prev/next buttons + a numbered-page host ... </div>
  </div>
</div>

<div class="scr-veil" data-scr-drawer="thing" hidden data-scr-close></div>
<aside class="scr-drawer" data-scr-drawer="thing" data-add-title="Add Thing" data-title-field="name" hidden>
  ... drawer head / body / foot ...
</aside>
{% endblock %}
```

**Drawers live as siblings of `.scr`, not descendants.** This is
deliberate — `byky-screen.js` delegates several listeners (toggles,
`data-scr-close`, Escape) at `document` level specifically because of this,
so don't nest the drawer/veil inside `.scr` "to keep it tidy."

**Copy the pager markup verbatim** from any migrated screen
(`cms_location_management.html` is the simplest). The JS finds the prev/next
buttons and replaces a `.scr-pager-current` placeholder with a
`.scr-pager-pages` host it manages — pagination is real, not decorative (see
§6).

**KPI tiles are optional.** Skip them entirely on a zero-data screen (see
`cms_location_management.html`) — tiles built from nothing are noise, not
signal.

---

## 4. List + drawer pattern

One drawer per entity, wired purely through `data-*` attributes:

```html
<button data-scr-open="branch:add">Add Branch</button>
...
<button data-scr-open="branch:edit">Edit</button>   <!-- inside a .scr-row -->

<div class="scr-veil" data-scr-drawer="branch" hidden data-scr-close></div>
<aside class="scr-drawer" data-scr-drawer="branch" data-add-title="Add Branch" data-title-field="name" hidden>
  ...
</aside>
```

- `data-scr-open="<name>:add"` / `"<name>:edit"` — opens the named drawer.
  On edit, the JS reads `data-record-id` off the closest `.scr-row`, finds
  the matching `{{ ...|json_script:id }}` blob, and prefills every
  `.scr-drawer-input[data-field]` from it.
- `data-title-field` — which field's value becomes the drawer title in edit
  mode (defaults to `name`).
- `data-lock-on-edit="true"` on an input — becomes read-only in edit mode
  (e.g. a code/ID field that shouldn't change after creation).
- `data-scr-enables="<field-key>"` on a `.scr-check` checkbox — disables/
  enables another field by its `data-field` key, based on the checkbox's own
  checked state (e.g. "Is Hotel" enabling "Hotel Commission %").
- `data-default-checked="true"` on a `.scr-check` — its default state in
  **Add** mode.

**Gotcha already fixed once — don't reintroduce it.** If a drawer group
holds *multiple* checkboxes under one `.scr-drawer-field` wrapper (a
"Flags" section), do **not** rely on per-field-group `querySelector`
(singular) to find them — it only ever reaches the first one. `open()` in
`byky-screen.js` handles all `.scr-check` elements in one separate pass for
exactly this reason. If you add new checkbox-driven behaviour, extend that
pass, don't add a second per-field one.

**Multi-field editable rows are never inline.** A row with more than ~2
editable fields renders as a formatted read-only line with Edit/Delete, and
the drawer owns the real form — this is a CLAUDE.md rule, not specific to
`.scr-*`, but the drawer is how you implement it here.

---

## 5. Form / section-card pattern (Tier B, settings screens)

For a full-page form (Tier B) or a settings screen, use `.scr-form-*` +
`.scr-section` + `.scr-grid` instead of a table:

```html
<div class="scr-card">
  <div class="scr-form-head">
    <div class="scr-form-title-row">
      <h2 class="scr-form-title">Company Record</h2>
      <span class="scr-form-badge">Full page · Tier B</span>
    </div>
    <p class="scr-form-sub">...</p>
  </div>
  <div class="scr-form-body">
    <div class="scr-section">
      <div class="scr-section-head">
        <h3 class="scr-section-title">Basic Information</h3>
        <div class="scr-section-rule"></div>
      </div>
      <div class="scr-grid">
        <div class="scr-field" style="grid-column:span 2">
          <label class="scr-label">Company Name<span class="scr-required">*</span></label>
          <input type="text" class="scr-input" value="..." />
          <div class="scr-help">...</div>
        </div>
      </div>
    </div>
    <!-- repeat .scr-section per group -->
    <div class="scr-form-foot">
      <div class="scr-toggle-row">
        <button type="button" class="scr-toggle is-on"><i></i></button>
        <span class="scr-toggle-label">Active</span>
      </div>
      <div class="scr-form-actions">
        <button class="scr-btn-secondary">Cancel</button>
        <button class="scr-btn-save-new">Save &amp; New</button>
        <button class="scr-btn-primary">Save</button>
      </div>
    </div>
  </div>
</div>
```

`.scr-field`'s `grid-column:span N` controls width within the auto-fit
grid — use it the same way `col-md-*` would be used elsewhere.

**Integrations / credential sets are list+drawer, not inline.** The Global
Application Configuration screen needed four external integrations
(WhatsApp, SMS, Mail, Payment Gateway), each with 5-7 credential fields.
Flattening ~25 inputs into the form would have buried the actual settings —
so each integration is a `.scr-integration` row (name, description, status
badge, "Configure" button) that opens its own named drawer. Follow this
precedent for anything similarly multi-field and semi-optional: don't
inline it, give it a row + drawer.

---

## 6. Filtering, search, pagination, tabs

- **Search:** `<div class="scr-search"><input placeholder="..."></div>` —
  matches against each row's `data-search="..."` attribute (lowercase,
  space-joined searchable text).
- **Filter dropdown:** `data-filter-key="branch"` on a `.scr-filter-wrap`;
  each `.scr-filter-opt[data-value="X"]` matches rows where
  `tr.dataset.branch === "X"`.
- **Noun labels:** `data-scr-noun-singular` / `data-scr-noun-plural` on the
  `.scr-card` (or `.scr-panel`) drive the pluralized `"N things"` toolbar
  count text.
- **Pagination is real, not decorative.** 15 rows a page (matching the
  DataTables screens — see `byky-cms-list.js`), computed over the
  **filtered** set. Any filter/search change resets to page 1; clicking a
  page number preserves it. This is entirely handled by `applyFilters()` /
  `renderPager()` in `byky-screen.js` — you only need to ship the pager
  markup, not wire anything yourself.
- **Scoping:** `scopeOf(el)` resolves to the nearest `.scr-panel`, else the
  nearest `.scr-card`, else the whole screen. This is why a tabbed screen's
  two grids (e.g. Countries / States) filter, search, and paginate
  **independently** — each lives in its own `.scr-panel`. The pagination
  init loop explicitly skips a `.scr-card` that contains `.scr-panel`s, to
  avoid treating two grids as one list. If you add a new scoping context,
  preserve this leaf-scope-only behaviour.
- **Top-level content tabs** (a screen with more than one grid, not to be
  confused with drawer tabs): wrap tab buttons in
  `[data-scr-tabgroup="name"]` with `.scr-content-tab` children, and give
  each grid's wrapper `.scr-panel[data-tabgroup="name"][data-tab="key"]`.

---

## 7. Maps

Any screen needing station geography uses the shared Leaflet map — **never**
a hand-drawn SVG bubble plot. (One was tried early in this project's history
and rejected on sight: without coastline, streets, or satellite imagery it
reads as "square pixels," and an operator placing a station can't use it.)

```django
{% block vendor_css %}
{{ block.super }}
<link rel="stylesheet" href="{% static 'vendor/libs/leaflet/leaflet.css' %}" />
{% endblock vendor_css %}

{% block vendor_js %}
{{ block.super }}
<script src="{% static 'vendor/libs/leaflet/leaflet.js' %}"></script>
{% endblock vendor_js %}

{% block page_js %}
{{ block.super }}
<script src="{% static 'js/byky-leaflet-map.js' %}"></script>
{% endblock page_js %}
```

```html
<div class="scr-map-frame">
  {{ map_points|json_script:"my-map-data" }}
  <div class="byky-map" data-map-points="my-map-data"
       data-map-focus="Dubai"      {# optional, default Dubai #}
       data-map-max-zoom="10">     {# optional, default 10 #}
  </div>
</div>
```

- `map_points` in context comes from `apps.byky_core.geo.station_points()` —
  don't invent coordinates.
- Three keyless Esri basemaps ship with a layer switcher: **Streets**
  (default), **Light**, **Satellite**. Override the default per screen with
  `data-map-base="light|streets|satellite"`. Never wire up Mapbox — it
  needs an access token this project doesn't have.
- Leaflet needs an explicit CSS height on its container (`.byky-map` already
  has one) — unlike an `<svg>`, it can't size itself from content.

---

## 8. Data-honesty rules still apply

Everything in `CLAUDE.md` §12 is unchanged inside `.scr-*` screens:

- Never invent a value. A field with no source data renders **blank** with
  a placeholder hinting at the shape (`https://`, `/media/vehicles/`,
  `e.g. 5`) and the class `is-awaiting` on `.scr-input` / `.scr-drawer-input`
  for the subtle tint.
- Use `seed.NOT_CAPTURED` (`"— not captured —"`) in forms/detail views and
  `seed.NOT_CAPTURED_SHORT` (`"—"`) in grid cells — same as everywhere else
  in the app.
- An awaiting-data list screen shows its real column headers with an honest
  empty state in the body (`.scr-empty`), not a fabricated row.

---

## 9. Extending the CSS/JS itself

It's fine — expected, even — to add new `.scr-*` classes or `data-scr-*`
attributes when a real screen needs a capability the system doesn't have
yet. Precedent for this already exists:

- Content tabs (`.scr-content-tab*`) — added for Country & State's dual grid.
- Flag pills / checkbox rows (`.scr-flag*`, `.scr-check*`) — added for
  Branch Management.
- Map frame (`.scr-map-frame`, `.scr-map-legend`) — added for Station
  Address Mapping, generalized so any future screen gets a map card free.
- Drawer textarea / file input styling — added for Station Address Mapping.
- Integration rows (`.scr-integration*`) — added for Global Configuration.

**Rules for doing this safely:**

1. **Grep first.** Confirm the capability genuinely doesn't exist before
   adding it (§2 above).
2. **Generalize from the real need**, using the same naming convention
   (`scr-` prefix, kebab-case) — don't add a one-off class scoped to your
   screen only. If it's reusable, put it in the shared files; if it's
   truly one-of-a-kind, it doesn't belong in `.scr-*` at all.
3. **Never touch the two shared files and expect zero blast radius.** They
   are loaded by every migrated screen. After any change, re-verify the
   *other* already-migrated screens too (see §10) — this project has
   caught real regressions this way (e.g. `.scr-card{overflow:hidden}`
   clipping a dropdown on a screen that didn't even have the dropdown that
   exposed the bug).
4. Add a one-line comment explaining *why* the addition exists, the way the
   rest of both files do — not what the CSS/JS does mechanically.

---

## 10. Verification checklist

Run all of this before considering a migrated screen done:

```bash
cd django-version/full-version
.venv/bin/python manage.py check
.venv/bin/python manage.py collectstatic --noinput

# Restart is required for template changes -- this project does not
# reliably pick them up otherwise (see CLAUDE.md). Kill by PID, don't use
# a bare pkill, and confirm the port is actually free before restarting.
ps aux | grep "[m]anage.py runserver"
kill -9 <pid>
nohup .venv/bin/python manage.py runserver 127.0.0.1:8009 --noreload > /tmp/dev-server.log 2>&1 &
disown
```

Then, with Playwright (Firefox — that's the browser this project has
actually shipped to; Chromium alone has previously hidden a real bug):

- Every drawer opens in **Add** mode with blank fields and the correct
  default-checked state.
- Every "Edit" action opens with the record correctly prefilled — including
  every checkbox, not just the first one in a group.
- Search, filter dropdowns, and pagination all update the toolbar count and
  "Showing X–Y of Z" text correctly, and interact correctly with each other
  (e.g. filtering re-pages to page 1, filtered count feeds page count).
- A tabbed screen's two panels filter/paginate independently.
- No horizontal overflow at 1280 / 1024 / 768px viewport widths.
- Zero console errors.

Finally, a full route sweep — every non-parametrized, non-admin URL should
return 200 (two permanent, expected exceptions: `/logout/` is 405,
`/send_verification/` is a 302 redirect):

```python
from django.test import Client
from django.urls import get_resolver
c = Client()
seen = set()
def walk(res, prefix=''):
    for p in res.url_patterns:
        if hasattr(p, 'url_patterns'):
            walk(p, prefix + str(p.pattern))
        else:
            pat = prefix + str(p.pattern)
            if '<' in pat or pat.startswith('admin') or '__debug__' in pat:
                continue
            seen.add('/' + pat)
walk(get_resolver())
bad = [(u, c.get(u).status_code) for u in sorted(seen) if c.get(u).status_code != 200]
print('routes checked:', len(seen), '| non-200:', bad)
```

---

## 11. Worked example: migrating a new screen

1. **Read the old template and its view** to get the exact field/column
   list (FSD §11/§12 are the binding contract, per CLAUDE.md §14's
   pre-flight checklist).
2. **Pick the closest already-migrated screen as your structural twin**:
   - Zero real data, simple Tier A list → `cms_location_management.html`
   - Rich Tier B form → `cms_company_details.html`
   - List with `<select>` fields and checkboxes in its drawer →
     `cms_branch_management.html`
   - Tabbed dual-grid → `cms_country_state_management.html`
   - Settings/config screen with credential-style sub-forms →
     `sysadmin_global_application_configuration_settings.html`
3. **Read `byky-screen.css` and `byky-screen.js` in full** (or at minimum
   grep every class/attribute you intend to use) so you don't invent
   something that already exists, or misuse something that works
   differently than you assume.
4. **Write the template**, copying structure from your twin and adapting
   field names/labels/routes. Don't invent data — if the source has gaps,
   render them per §8.
5. **Wire the view/urls** only if new context variables are genuinely
   needed. Many screens need nothing beyond what a shared base view
   (e.g. `CmsScreenView`) already provides — check before adding.
6. **Verify** per §10, including a regression pass on 2-3 other already-
   migrated screens if you touched the shared CSS/JS files.
