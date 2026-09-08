# Byky RMS sidebar — Django integration

Files
-----
    templates/sidebar/sidebar.html                  the rail (include this)
    templates/sidebar/menu_header_template.html     section header  (OPERATIONS / BUSINESS / SYSTEM)
    templates/sidebar/menu_item_template.html       link vs. collapsible switch
    templates/sidebar/menu_link_template.html       plain link row
    templates/sidebar/menu_collapsible_template.html  group row + submenu
    templates/sidebar/menu_icon_template.html       inline-SVG icon (falls back to your icon class)
    static/sidebar/sidebar.css                      all styling + animations
    static/sidebar/sidebar.js                       collapse, hover-peek, resize, tooltips
    static/sidebar/byky-mark.png                    logo mark
    vertical_menu.json                              menu data with the icon paths baked in

Install
-------
1. Copy `templates/sidebar/` into your templates dir and `static/sidebar/` into your static dir.
2. Replace your `vertical_menu.json` with the one here, or copy the `svg` values into yours.
   Point each submenu `url` at your real url names.
3. In your base layout:

       {% load static %}
       <link rel="stylesheet" href="{% static 'sidebar/sidebar.css' %}">
       ...
       <div class="byky-shell">
         {% include 'sidebar/sidebar.html' %}
         <main style="flex:1;min-width:0;display:flex;flex-direction:column;overflow:hidden">
           {% block content %}{% endblock %}
         </main>
       </div>
       <script src="{% static 'sidebar/sidebar.js' %}"></script>

4. Keep your existing template filters: `has_permission` and `filter_by_url` are used unchanged.

Notes
-----
* Your original four templates kept their names, classes and Django logic
  (`permission`, `filter_by_url`, `trans`, `badge`, `external`, `target`), so the
  context processor that feeds `menu_items` needs no changes.
* Badges: `item.badge` still renders `badge.1`. Collapsible groups with no badge
  show the submenu count, as in the design.
* Icons are inline SVG via `item.svg`. If an item has no `svg`, the template falls
  back to `<i class="menu-icon {{ item.icon }}">` so Boxicons/Remix keep working.
* Submenu groups expand independently and animate their height, so opening one
  never collapses another — nothing shifts under the cursor. Each group closes by
  clicking its own row; the open set persists in localStorage.
* Feature parity: collapse toggle, hover-to-peek expand (overlay + wordmark
  animation), drag-to-resize 232–400px, independently expanding submenus (open groups remembered), badge/chevron
  crossfade, truncation-only tooltips anchored outside the rail, localStorage
  persistence of width and collapsed state.
* Extra for production: below 768px the rail becomes an off-canvas overlay —
  add `<button data-byky-open>` anywhere in your topbar to open it.
* Bootstrap is not required. If Bootstrap is present, nothing here depends on it;
  our `.menu-*` rules are scoped under `.byky-sidebar`/`.byky-nav`.
