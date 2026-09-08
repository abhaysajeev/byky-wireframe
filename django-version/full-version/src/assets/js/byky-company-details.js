/* BYKY Company Details (FSD 1.1) — filter dropdowns, live search, the Add/Edit
   drawer and its tabs, and the two "active" toggle switches. Vanilla JS, no
   vendor libraries; static data, nothing here submits or persists. */
(function () {
  'use strict';

  var root = document.querySelector('.cd');
  if (!root) return;

  /* ── filter dropdowns ─────────────────────────────────────────── */
  var filterWraps = root.querySelectorAll('.cd-filter-wrap');
  filterWraps.forEach(function (wrap) {
    var btn = wrap.querySelector('.cd-filter-btn');
    var menu = wrap.querySelector('.cd-filter-menu');
    btn.addEventListener('click', function (e) {
      e.stopPropagation();
      var willOpen = menu.hidden;
      filterWraps.forEach(function (w) { w.querySelector('.cd-filter-menu').hidden = true; });
      menu.hidden = !willOpen;
    });
    menu.querySelectorAll('.cd-filter-opt').forEach(function (opt) {
      opt.addEventListener('click', function () {
        menu.querySelectorAll('.cd-filter-opt').forEach(function (o) { o.classList.remove('is-active'); });
        opt.classList.add('is-active');
        var label = btn.querySelector('.cd-filter-label');
        var value = opt.dataset.value || '';
        if (label) label.textContent = opt.textContent;
        btn.classList.toggle('is-active', !!value);
        menu.hidden = true;
        applyFilters();
      });
    });
  });
  document.addEventListener('click', function () {
    filterWraps.forEach(function (w) { w.querySelector('.cd-filter-menu').hidden = true; });
  });

  var searchInput = root.querySelector('.cd-search input');
  if (searchInput) searchInput.addEventListener('input', applyFilters);

  function applyFilters() {
    var q = (searchInput && searchInput.value || '').trim().toLowerCase();
    var rows = root.querySelectorAll('.cd-row');
    var visible = 0;
    var active = {};
    filterWraps.forEach(function (w) {
      var key = w.dataset.filterKey;
      var picked = w.querySelector('.cd-filter-opt.is-active');
      active[key] = picked ? (picked.dataset.value || '') : '';
    });
    rows.forEach(function (tr) {
      var matchesQ = !q || (tr.dataset.search || '').indexOf(q) > -1;
      var matchesAll = Object.keys(active).every(function (key) {
        return !active[key] || tr.dataset[key] === active[key];
      });
      var show = matchesQ && matchesAll;
      tr.hidden = !show;
      if (show) visible++;
    });
    root.querySelectorAll('.cd-toolbar-count').forEach(function (el) {
      el.textContent = visible + (visible === 1 ? ' company' : ' companies');
    });
    root.querySelectorAll('.cd-pager-info').forEach(function (el) {
      el.textContent = 'Showing ' + visible + ' of ' + rows.length;
    });
  }

  /* ── toggle switches (drawer "Active" + inline form "is active") ─ */
  root.addEventListener('click', function (e) {
    var toggle = e.target.closest('.cd-toggle');
    if (!toggle) return;
    toggle.classList.toggle('is-on');
  });
  var drawerToggle = document.querySelector('#cd-drawer .cd-toggle');
  if (drawerToggle) {
    drawerToggle.addEventListener('click', function () { drawerToggle.classList.toggle('is-on'); });
  }

  /* ── drawer: open/close, tabs, prefill on edit ───────────────────── */
  var veil = document.getElementById('cd-veil');
  var drawer = document.getElementById('cd-drawer');
  if (!veil || !drawer) return;

  var titleEl = document.getElementById('cd-drawer-title');
  var tabs = drawer.querySelectorAll('.cd-drawer-tab');
  var fieldGroups = drawer.querySelectorAll('.cd-drawer-field, .cd-drawer-hint-group');
  var toggle = drawer.querySelector('.cd-toggle');

  function selectTab(key) {
    tabs.forEach(function (t) { t.classList.toggle('is-on', t.dataset.tab === key); });
    fieldGroups.forEach(function (g) { g.hidden = g.dataset.tab !== key; });
  }
  tabs.forEach(function (t) {
    t.addEventListener('click', function () { selectTab(t.dataset.tab); });
  });

  function openDrawer(mode, record) {
    drawer.dataset.mode = mode;
    if (titleEl) titleEl.textContent = mode === 'edit' && record ? (record.name || 'Company') : 'Add Company';
    fieldGroups.forEach(function (g) {
      var input = g.querySelector('.cd-drawer-input');
      if (!input) return;
      var key = input.dataset.field;
      var value = mode === 'edit' && record ? (record[key] || '') : '';
      input.value = value;
      input.readOnly = mode === 'edit' && key === 'code';
    });
    if (toggle) {
      var isActive = mode === 'edit' && record ? !!record.active : true;
      toggle.classList.toggle('is-on', isActive);
    }
    selectTab('basic');
    veil.hidden = false;
    drawer.hidden = false;
  }
  function closeDrawer() {
    veil.hidden = true;
    drawer.hidden = true;
  }

  document.querySelectorAll('[data-cd-open="add"]').forEach(function (btn) {
    btn.addEventListener('click', function () { openDrawer('add', null); });
  });
  document.querySelectorAll('[data-cd-open="edit"]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var row = btn.closest('.cd-row');
      var node = row && document.getElementById(row.dataset.recordId);
      var record = node ? JSON.parse(node.textContent) : null;
      openDrawer('edit', record);
    });
  });
  document.querySelectorAll('[data-cd-close]').forEach(function (btn) {
    btn.addEventListener('click', closeDrawer);
  });
  veil.addEventListener('click', closeDrawer);
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && !drawer.hidden) closeDrawer();
  });
})();
