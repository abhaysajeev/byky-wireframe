/**
 * Transfer / Return -- the full-page movement flow.
 *
 * byky-ims-map-to-branch.js already owns select-all, the button and the
 * success banner; this adds what a movement needs on top:
 *
 *   1. the pool is scoped to wherever the items currently are. Whichever
 *      field carries data-scr-pool-source drives the grid's branch filter --
 *      From Branch on a transfer, From Warehouse or From Event Location on a
 *      return -- so one file serves both without knowing which page it is on.
 *   2. the button waits for every *visible* required field, not just a
 *      selection. Visible matters: the destination fields swap with the type,
 *      and a hidden one must not block the form.
 *   3. the three condition photos show the chosen filename.
 *   4. on Transfer only (#transfer-pool-data), the item pool -- 1,060+
 *      vehicles and assets across every branch -- is never rendered as rows
 *      up front. It's parsed once from a json_script blob and only built
 *      into rows once both Inventory Type and From Branch are chosen,
 *      scoped to just that combination -- the old always-rendered table put
 *      every item from every branch in the DOM regardless of selection,
 *      flagged as a page-hang risk as the fleet grows.
 *
 * Nothing persists. Same wireframe rules as every other screen here.
 */

'use strict';

(function () {
  var card = document.getElementById('map-items-card');
  var hint = document.getElementById('transfer-pool-hint');
  if (!card) return;

  var branchWrap = card.querySelector('.scr-filter-wrap[data-filter-key="branch"]');
  var sources = document.querySelectorAll('[data-scr-pool-source]');

  // ── lazy item pool (Transfer page only) ──────────────────────────
  var poolDataEl = document.getElementById('transfer-pool-data');
  var poolRows = document.getElementById('transfer-pool-rows');
  var poolCount = document.getElementById('transfer-pool-count');
  var invTypeSelect = document.getElementById('transfer-inventory-type');
  var fromBranchSelect = document.getElementById('transfer-from-branch');
  var allPoolItems = poolDataEl ? JSON.parse(poolDataEl.textContent) : null;

  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function poolRowHtml(item) {
    var search = (item.code + ' ' + item.name + ' ' + item.rfid).toLowerCase();
    return '<tr class="scr-row" data-search="' + escapeHtml(search) + '" data-branch="' + escapeHtml(item.branch) +
      '" data-itemtype="' + escapeHtml(item.item_type) + '" data-category="' + escapeHtml(item.category) +
      '" data-vtype="' + escapeHtml(item.vtype) + '">' +
      '<td><input type="checkbox" data-map-check value="' + escapeHtml(item.code) + '"></td>' +
      '<td><span class="scr-code">' + escapeHtml(item.code) + '</span></td>' +
      '<td style="font-weight:600">' + escapeHtml(item.name) + '</td>' +
      '<td><span class="scr-badge scr-badge-pending"><i></i>' + escapeHtml(item.item_type) + '</span></td>' +
      '<td class="scr-contact">' + escapeHtml(item.category) + '</td>' +
      '<td class="scr-contact">' + escapeHtml(item.vtype) + '</td>' +
      '<td><span class="scr-code">' + escapeHtml(item.rfid) + '</span></td></tr>';
  }

  function poolEmptyHtml(title, sub) {
    return '<tr><td colspan="7" style="padding:0"><div class="scr-empty">' +
      '<span class="scr-empty-ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#a9a6c4" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16v12H4zM4 7l2-3h12l2 3"></path></svg></span>' +
      '<div><div class="scr-empty-title">' + title + '</div><p class="scr-empty-sub">' + sub + '</p></div></div></td></tr>';
  }

  function loadPool() {
    if (!poolRows || !allPoolItems) return;
    var invType = invTypeSelect ? invTypeSelect.value : '';
    var branch = fromBranchSelect ? fromBranchSelect.value : '';
    var pagerInfo = document.getElementById('transfer-pool-pager-info');

    if (!invType || !branch) {
      poolRows.innerHTML = poolEmptyHtml('Select filters to load items', 'Pick an Inventory Type and a From Branch above to list what it holds.');
      if (poolCount) poolCount.textContent = '0 items';
      if (pagerInfo) pagerInfo.textContent = 'Showing 0 of 0';
      return;
    }

    var matches = allPoolItems.filter(function (i) { return i.item_type === invType && i.branch === branch; });
    poolRows.innerHTML = matches.length
      ? matches.map(poolRowHtml).join('')
      : poolEmptyHtml('No items at this branch', 'This branch holds no ' + invType.toLowerCase() + 's right now.');

    /* let byky-screen.js's own search/filter/pagination re-scan the new
       rows -- same trick byky-ims-map-to-branch.js uses after a transfer
       removes rows, since applyFilters() re-reads .scr-row fresh every
       call rather than caching them. */
    var searchInput = card.querySelector('.scr-search input');
    if (searchInput) searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    if (window.bykyMapRefresh) window.bykyMapRefresh();
  }

  function applyPoolSource() {
    /* the visible source field wins; the others are hidden by the type swap */
    var value = '';
    sources.forEach(function (sel) {
      var field = sel.closest('.scr-field');
      if ((!field || !field.hidden) && sel.value) value = sel.value;
    });
    if (branchWrap) {
      var opt = branchWrap.querySelector('.scr-filter-opt[data-value="' + value + '"]');
      if (opt) opt.click();
    }
    if (hint) {
      hint.textContent = value
        ? 'Everything currently at ' + value + '.'
        : hint.dataset.emptyHint || hint.textContent;
    }
  }

  /* Every required field that is on screen must be filled. Reading it off the
     rendered asterisk keeps this in step with the form itself -- add a field
     and mark it required and the gate picks it up, with nothing to update. */
  function headerComplete() {
    var ok = true;
    document.querySelectorAll('.scr-field').forEach(function (f) {
      if (f.hidden || !f.querySelector('.scr-required')) return;
      var input = f.querySelector('[data-field]');
      if (input && !input.value) ok = false;
    });
    return ok;
  }

  window.bykyMapGate = headerComplete;

  document.addEventListener('change', function (e) {
    if (e.target.matches('[data-scr-pool-source]')) applyPoolSource();
    if (e.target.matches('[data-field]')) {
      /* the type swap can hide the field that was holding the pool source */
      applyPoolSource();
      if (window.bykyMapRefresh) window.bykyMapRefresh();
    }
    if (e.target === invTypeSelect || e.target === fromBranchSelect) loadPool();
  });

  document.querySelectorAll('.scr-upload input[type="file"]').forEach(function (input) {
    input.addEventListener('change', function () {
      var label = input.parentNode.querySelector('span');
      if (label && input.files && input.files[0]) label.textContent = input.files[0].name;
    });
  });

  if (typeof flatpickr !== 'undefined') {
    document.querySelectorAll('.byky-date').forEach(function (el) {
      flatpickr(el, { dateFormat: 'd M Y', allowInput: true });
    });
  }

  if (hint) hint.dataset.emptyHint = hint.textContent;
  applyPoolSource();
  loadPool();
  if (window.bykyMapRefresh) window.bykyMapRefresh();
})();
