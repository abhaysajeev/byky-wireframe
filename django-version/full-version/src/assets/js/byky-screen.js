/* BYKY screen design system -- the shared behaviour every redesigned screen
   extends: filter dropdowns, live search (scoped per panel/card so a tabbed
   screen's two grids filter independently), one or more Add/Edit drawers with
   their own tabs, top-level content tabs (for screens with more than one grid,
   e.g. Country & State), and "active" toggle switches. Vanilla JS, no vendor
   libraries; static data, nothing here submits or persists. Generalised from
   byky-company-details.js -- see that file's screen for the reference look. */
(function () {
  'use strict';

  var root = document.querySelector('.scr');
  if (!root) return;

  function scopeOf(el) {
    return el.closest('.scr-panel') || el.closest('.scr-card') || root;
  }

  /* ── filter dropdowns + search (scoped to the nearest panel/card) ─ */
  var filterWraps = root.querySelectorAll('.scr-filter-wrap');
  filterWraps.forEach(function (wrap) {
    var btn = wrap.querySelector('.scr-filter-btn');
    var menu = wrap.querySelector('.scr-filter-menu');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var willOpen = menu.hidden;
      filterWraps.forEach(function (w) { w.querySelector('.scr-filter-menu').hidden = true; });
      menu.hidden = !willOpen;
    });
    menu.querySelectorAll('.scr-filter-opt').forEach(function (opt) {
      opt.addEventListener('click', function () {
        menu.querySelectorAll('.scr-filter-opt').forEach(function (o) { o.classList.remove('is-active'); });
        opt.classList.add('is-active');
        var label = btn.querySelector('.scr-filter-label');
        var value = opt.dataset.value || '';
        if (label) label.textContent = opt.textContent;
        btn.classList.toggle('is-active', !!value);
        menu.hidden = true;
        applyFilters(scopeOf(wrap));
      });
    });
  });
  document.addEventListener('click', function () {
    filterWraps.forEach(function (w) { w.querySelector('.scr-filter-menu').hidden = true; });
  });

  root.querySelectorAll('.scr-search input').forEach(function (input) {
    input.addEventListener('input', function () { applyFilters(scopeOf(input)); });
  });

  /* ── pagination ───────────────────────────────────────────────────
     15 rows a page, matching the DataTables screens (byky-cms-list.js).
     Paging runs over the *filtered* set, not the raw rows, so searching
     re-pages rather than leaving gaps; any filter/search change resets to
     page 1, while clicking a page number keeps it. State is per scope, so a
     tabbed screen's two grids page independently. */
  var PAGE_SIZE = 15;
  var pageOf = new WeakMap();

  /* Page numbers to render: all of them while they fit, otherwise first and
     last with a window around the current page and ellipses for the gaps. */
  function pageList(current, total) {
    if (total <= 7) {
      return Array.apply(null, { length: total }).map(function (_, i) { return i + 1; });
    }
    var out = [1];
    var lo = Math.max(2, current - 1);
    var hi = Math.min(total - 1, current + 1);
    if (lo > 2) out.push('…');
    for (var i = lo; i <= hi; i++) out.push(i);
    if (hi < total - 1) out.push('…');
    out.push(total);
    return out;
  }

  /* The template ships prev/next buttons around a static "1". Keep the
     buttons (their icons are template-owned) and swap the static number for a
     container this owns. */
  function pagesHost(nav) {
    var host = nav.querySelector('.scr-pager-pages');
    if (!host) {
      host = document.createElement('span');
      host.className = 'scr-pager-pages';
      var stale = nav.querySelector('.scr-pager-current');
      if (stale) nav.replaceChild(host, stale);
      else nav.appendChild(host);
    }
    return host;
  }

  function renderPager(scope, page, pages) {
    scope.querySelectorAll('.scr-pager-nav').forEach(function (nav) {
      var btns = nav.querySelectorAll('.scr-pager-btn');
      var prev = btns[0];
      var next = btns[btns.length - 1];
      if (prev) {
        prev.disabled = page <= 1;
        prev.onclick = function () { goTo(scope, page - 1); };
      }
      if (next) {
        next.disabled = page >= pages;
        next.onclick = function () { goTo(scope, page + 1); };
      }

      var host = pagesHost(nav);
      host.textContent = '';
      pageList(page, pages).forEach(function (n) {
        if (n === '…') {
          var gap = document.createElement('span');
          gap.className = 'scr-pager-gap';
          gap.textContent = '…';
          host.appendChild(gap);
          return;
        }
        var b = document.createElement('button');
        b.type = 'button';
        b.className = n === page ? 'scr-pager-current' : 'scr-pager-page';
        b.textContent = n;
        if (n !== page) b.onclick = function () { goTo(scope, n); };
        host.appendChild(b);
      });
    });
  }

  function goTo(scope, page) {
    pageOf.set(scope, page);
    applyFilters(scope, true);
  }

  function applyFilters(scope, keepPage) {
    var searchInput = scope.querySelector('.scr-search input');
    var q = (searchInput && searchInput.value || '').trim().toLowerCase();
    var rows = scope.querySelectorAll('.scr-row');
    var active = {};
    scope.querySelectorAll('.scr-filter-wrap').forEach(function (w) {
      var key = w.dataset.filterKey;
      var picked = w.querySelector('.scr-filter-opt.is-active');
      active[key] = picked ? (picked.dataset.value || '') : '';
    });

    var matches = [];
    rows.forEach(function (tr) {
      var matchesQ = !q || (tr.dataset.search || '').indexOf(q) > -1;
      var matchesAll = Object.keys(active).every(function (key) {
        return !active[key] || tr.dataset[key] === active[key];
      });
      if (matchesQ && matchesAll) matches.push(tr);
    });

    var pages = Math.max(1, Math.ceil(matches.length / PAGE_SIZE));
    var page = keepPage ? (pageOf.get(scope) || 1) : 1;
    if (page > pages) page = pages;
    if (page < 1) page = 1;
    pageOf.set(scope, page);

    var start = (page - 1) * PAGE_SIZE;
    var end = start + PAGE_SIZE;
    rows.forEach(function (tr) { tr.hidden = true; });
    matches.forEach(function (tr, i) { tr.hidden = i < start || i >= end; });

    // The toolbar count is the size of the whole filtered set, not the page.
    var singular = scope.dataset.scrNounSingular || 'row';
    var plural = scope.dataset.scrNounPlural || singular + 's';
    scope.querySelectorAll('.scr-toolbar-count').forEach(function (el) {
      el.textContent = matches.length + ' ' + (matches.length === 1 ? singular : plural);
    });
    scope.querySelectorAll('.scr-pager-info').forEach(function (el) {
      el.textContent = matches.length
        ? 'Showing ' + (start + 1) + '–' + Math.min(end, matches.length) + ' of ' + matches.length
        : 'Showing 0 of 0';
    });

    renderPager(scope, page, pages);
  }

  /* Paginate on load: the server renders every row, so without this a 36-row
     grid would show all 36 until the first filter interaction.

     Only leaf scopes get initialised. On a tabbed screen the .scr-card wraps
     both .scr-panels, and paging the card would treat the two grids as one
     list -- scopeOf() already resolves to the nearest panel, so the card must
     be skipped when it contains any. */
  var scopes = Array.prototype.slice.call(root.querySelectorAll('.scr-panel'));
  Array.prototype.forEach.call(root.querySelectorAll('.scr-card'), function (card) {
    if (!card.querySelector('.scr-panel')) scopes.push(card);
  });
  scopes.forEach(function (scope) {
    if (scope.querySelector('.scr-row')) applyFilters(scope);
  });

  /* ── cascading dropdowns (Country → State → Location → Branch) ────
     One shared helper, per CLAUDE.md, rather than a per-screen copy. A
     parent select declares data-scr-cascades="<child field key>"; the child
     select carries its full option list as JSON in data-scr-options (each
     entry {value, parent}) plus a plain "Select" placeholder in the markup.
     Selecting a parent value rebuilds the child's options to only those
     entries whose `parent` matches -- an unfiltered rebuild (all options)
     when the parent is cleared. Delegated at document level so it works
     inside drawers, which sit outside .scr. */
  document.addEventListener('change', function (e) {
    var parent = e.target;
    if (!(parent.matches && parent.matches('select[data-scr-cascades]'))) return;
    var childKey = parent.dataset.scrCascades;
    var scope = parent.closest('.scr-drawer, .scr-form-body, .scr') || document;
    var child = scope.querySelector('select[data-field="' + childKey + '"]');
    if (!child || !child.dataset.scrOptions) return;

    var options;
    try {
      options = JSON.parse(child.dataset.scrOptions);
    } catch (err) {
      return;
    }
    var value = parent.value;

    while (child.options.length > 1) child.remove(1);
    options.forEach(function (opt) {
      if (value && opt.parent !== value) return;
      var el = document.createElement('option');
      el.textContent = opt.value;
      child.appendChild(el);
    });
    child.value = '';
  });

  /* ── logo / image upload preview ─────────────────────────────────
     Any input[type=file][data-scr-logo-preview="<target id>"] renders the
     chosen image into that element (an <img>, created if not already
     present). Nothing uploads anywhere -- wireframe phase, local preview
     only. Delegated at document level for the same reason as drawers: a
     preview tile can sit outside .scr (e.g. in a drawer). */
  document.addEventListener('change', function (e) {
    var input = e.target;
    if (!(input.matches && input.matches('input[type="file"][data-scr-logo-preview]'))) return;
    var file = input.files && input.files[0];
    if (!file || file.type.indexOf('image/') !== 0) return;
    var target = document.getElementById(input.dataset.scrLogoPreview);
    if (!target) return;
    var reader = new FileReader();
    reader.onload = function () {
      var img = target.querySelector('img');
      if (!img) {
        img = document.createElement('img');
        img.alt = 'Logo preview';
        target.innerHTML = '';
        target.appendChild(img);
      }
      img.src = reader.result;
    };
    reader.readAsDataURL(file);
  });

  /* ── toggle switches -- delegated at document level since drawers live
     outside .scr as siblings, not descendants ─────────────────────── */
  document.addEventListener('click', function (e) {
    var toggle = e.target.closest('.scr-toggle');
    if (!toggle) return;
    toggle.classList.toggle('is-on');
  });

  /* ── Tier D privilege matrix: per-row Select All + Remove All Privileges ─
     Shared by all 16 modules' privilege screens (byky/partials/privilege_matrix.html).
     Select All toggles every permission checkbox on its own row; Remove All
     Privileges (data-scr-clear-privileges) clears every checkbox in the
     nearest matrix table in one action, including every row's Select All. */
  document.querySelectorAll('.privilege-select-all').forEach(function (box) {
    box.addEventListener('change', function () {
      box.closest('tr').querySelectorAll('input[type="checkbox"]:not(.privilege-select-all)').forEach(function (cb) {
        cb.checked = box.checked;
      });
    });
  });

  document.querySelectorAll('[data-scr-clear-privileges]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var table = btn.closest('.scr-card').querySelector('table');
      if (!table) return;
      table.querySelectorAll('input[type="checkbox"]').forEach(function (cb) { cb.checked = false; });
    });
  });

  /* ── top-level content tabs (screens with more than one grid) ───── */
  document.querySelectorAll('[data-scr-tabgroup]').forEach(function (group) {
    var name = group.dataset.scrTabgroup;
    var tabs = group.querySelectorAll('.scr-content-tab');
    var panels = document.querySelectorAll('.scr-panel[data-tabgroup="' + name + '"]');
    tabs.forEach(function (t) {
      t.addEventListener('click', function () {
        tabs.forEach(function (o) { o.classList.toggle('is-on', o === t); });
        panels.forEach(function (p) { p.hidden = p.dataset.tab !== t.dataset.tab; });
      });
    });
  });

  /* ── drawers: one or more, each named via data-scr-drawer ────────── */
  var drawers = {};
  document.querySelectorAll('[data-scr-drawer]').forEach(function (el) {
    var name = el.dataset.scrDrawer;
    drawers[name] = drawers[name] || {};
    if (el.classList.contains('scr-veil')) drawers[name].veil = el;
    if (el.classList.contains('scr-drawer')) drawers[name].drawer = el;
  });

  function wireDrawer(cfg) {
    var veil = cfg.veil, drawer = cfg.drawer;
    if (!veil || !drawer) return;
    var titleEl = drawer.querySelector('.scr-drawer-title');
    var tabs = drawer.querySelectorAll('.scr-drawer-tab');
    var fieldGroups = drawer.querySelectorAll('.scr-drawer-field, .scr-drawer-hint-group');
    var toggle = drawer.querySelector('.scr-toggle');
    var addTitle = drawer.dataset.addTitle || 'Add';
    var titleField = drawer.dataset.titleField || 'name';

    function selectTab(key) {
      tabs.forEach(function (t) { t.classList.toggle('is-on', t.dataset.tab === key); });
      fieldGroups.forEach(function (g) { g.hidden = g.dataset.tab !== key; });
    }
    tabs.forEach(function (t) { t.addEventListener('click', function () { selectTab(t.dataset.tab); }); });

    /* a checkbox with data-scr-enables="<field key>" toggles that field's
       disabled state to match its own checked state (e.g. "Is Hotel" enabling
       the Hotel Commission % input) -- wired once, re-synced on every open() */
    var enablers = drawer.querySelectorAll('.scr-check[data-scr-enables]');
    enablers.forEach(function (check) {
      var target = drawer.querySelector('[data-field="' + check.dataset.scrEnables + '"]');
      function sync() { if (target) target.disabled = !check.checked; }
      check.addEventListener('change', sync);
    });

    function open(mode, record) {
      drawer.dataset.mode = mode;
      if (titleEl) titleEl.textContent = mode === 'edit' && record ? (record[titleField] || addTitle) : addTitle;
      fieldGroups.forEach(function (g) {
        var input = g.querySelector('.scr-drawer-input');
        if (!input) return;
        var key = input.dataset.field;
        input.value = mode === 'edit' && record ? (record[key] || '') : '';
        input.readOnly = mode === 'edit' && input.dataset.lockOnEdit === 'true';
      });
      /* Cascading child selects (data-scr-options) only hold a placeholder
         option until their parent's "change" fires and rebuilds the real
         list -- setting .value programmatically above does not dispatch
         that event, so the child would otherwise always land on "Select"
         in edit mode. Fire the parents now that their own values are set,
         then re-apply the record's value to each child now that it has
         real options to match against. */
      /* bubbles: true is required here -- the cascade listener is delegated
         at document level (drawers sit outside .scr), so a non-bubbling
         event never reaches it. The .scr-check listeners a few lines below
         don't need this because they're attached directly to each checkbox,
         not delegated. */
      drawer.querySelectorAll('select[data-scr-cascades]').forEach(function (p) {
        p.dispatchEvent(new Event('change', { bubbles: true }));
      });
      fieldGroups.forEach(function (g) {
        var input = g.querySelector('select[data-scr-options]');
        if (!input) return;
        input.value = mode === 'edit' && record ? (record[input.dataset.field] || '') : '';
      });
      /* checkboxes are handled as their own pass, not scoped to fieldGroups --
         a "Flags" group can hold several .scr-check elements under one label,
         and fieldGroups' querySelector (singular) would only ever reach the
         first of them. */
      drawer.querySelectorAll('.scr-check').forEach(function (check) {
        var ckey = check.dataset.field;
        check.checked = mode === 'edit' && record ? !!record[ckey] : check.dataset.defaultChecked === 'true';
        check.dispatchEvent(new Event('change'));
      });
      if (toggle) {
        var isActive = mode === 'edit' && record ? !!record.active : true;
        toggle.classList.toggle('is-on', isActive);
      }
      if (tabs.length) selectTab(tabs[0].dataset.tab);
      veil.hidden = false;
      drawer.hidden = false;
    }
    function close() {
      veil.hidden = true;
      drawer.hidden = true;
    }
    veil.addEventListener('click', close);
    drawer._scrOpen = open;
    drawer._scrClose = close;
  }
  Object.keys(drawers).forEach(function (name) { wireDrawer(drawers[name]); });

  document.querySelectorAll('[data-scr-open]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var parts = btn.dataset.scrOpen.split(':');
      var name = parts[0], mode = parts[1] || 'add';
      var cfg = drawers[name];
      if (!cfg || !cfg.drawer || !cfg.drawer._scrOpen) return;
      var record = null;
      if (mode === 'edit') {
        var row = btn.closest('.scr-row');
        var node = row && document.getElementById(row.dataset.recordId);
        record = node ? JSON.parse(node.textContent) : null;
      }
      cfg.drawer._scrOpen(mode, record);
    });
  });
  document.querySelectorAll('[data-scr-close]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var drawer = btn.closest('.scr-drawer');
      if (drawer && drawer._scrClose) drawer._scrClose();
    });
  });
  document.addEventListener('keydown', function (e) {
    if (e.key !== 'Escape') return;
    Object.keys(drawers).forEach(function (name) {
      var d = drawers[name].drawer;
      if (d && !d.hidden && d._scrClose) d._scrClose();
    });
  });

  /* ── shared "view records" modal ──────────────────────────────────
     Any trigger with data-scr-view="<json-script id>" opens the shared
     #scr-records-modal (byky/partials/records_modal.html) populated from
     that JSON array, using data-scr-view-columns / -labels (JSON arrays of
     matching length) to build the table and data-scr-view-title for the
     heading. A branch's vehicle count is the first use; any future
     count-that-opens-a-list reuses this with no new markup or JS, just a
     trigger button and a json_script blob. Bootstrap's own modal JS (already
     loaded site-wide) handles show/hide; this only populates content on
     show.bs.modal, reading the triggering button via event.relatedTarget. */
  var recordsModal = document.getElementById('scr-records-modal');
  if (recordsModal) {
    var rmTitle = document.getElementById('scr-records-modal-title');
    var rmHead = document.getElementById('scr-records-thead');
    var rmBody = document.getElementById('scr-records-tbody');
    var rmEmpty = document.getElementById('scr-records-empty');
    var rmExport = document.getElementById('scr-records-export');
    var rmState = { rows: [], columns: [], labels: [], title: 'Records' };

    function csvCell(v) {
      v = v === null || v === undefined ? '' : String(v);
      return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
    }

    recordsModal.addEventListener('show.bs.modal', function (e) {
      var btn = e.relatedTarget;
      if (!btn) return;
      var node = document.getElementById(btn.dataset.scrView);
      var rows = [];
      try {
        rows = node ? JSON.parse(node.textContent) : [];
      } catch (err) {
        rows = [];
      }
      var columns = [];
      var labels = [];
      try {
        columns = JSON.parse(btn.dataset.scrViewColumns || '[]');
        labels = JSON.parse(btn.dataset.scrViewLabels || '[]');
      } catch (err2) {
        columns = [];
        labels = [];
      }
      rmState = { rows: rows, columns: columns, labels: labels, title: btn.dataset.scrViewTitle || 'Records' };

      if (rmTitle) rmTitle.textContent = rmState.title;

      rmHead.innerHTML = '';
      labels.forEach(function (label) {
        var th = document.createElement('th');
        th.textContent = label;
        rmHead.appendChild(th);
      });

      rmBody.innerHTML = '';
      rows.forEach(function (row) {
        var tr = document.createElement('tr');
        columns.forEach(function (key) {
          var td = document.createElement('td');
          td.textContent = row[key] === null || row[key] === undefined ? '' : row[key];
          tr.appendChild(td);
        });
        rmBody.appendChild(tr);
      });
      if (rmEmpty) rmEmpty.hidden = rows.length > 0;
    });

    if (rmExport) {
      rmExport.addEventListener('click', function () {
        if (!rmState.rows.length) return;
        var lines = [rmState.labels.map(csvCell).join(',')];
        rmState.rows.forEach(function (row) {
          lines.push(rmState.columns.map(function (key) { return csvCell(row[key]); }).join(','));
        });
        var blob = new Blob([lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
        var url = URL.createObjectURL(blob);
        var a = document.createElement('a');
        a.href = url;
        a.download = (rmState.title || 'export').replace(/[^\w\- ]+/g, '').trim().replace(/\s+/g, '-') + '.csv';
        document.body.appendChild(a);
        a.click();
        a.remove();
        URL.revokeObjectURL(url);
      });
    }
  }
})();
