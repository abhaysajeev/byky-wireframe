/**
 * Edit Transfer -- row 48's UAT remarks (client's feedback doc).
 *
 * Two independent pieces, both frontend-only (CLAUDE.md 1 -- nothing here
 * persists past the page session):
 *
 * 1. Cart -- the transfer's currently selected items, server-rendered as
 *    real rows (there's only ever one demo transfer, so this list is
 *    small); each carries a Remove button.
 * 2. Add Items -- a toggled panel offering the same From Branch's pool
 *    (parsed once from add-items-pool-data, the same lazy json_script
 *    approach ims_vehicle_transfer_new.html's byky-ims-transfer.js uses),
 *    filtered by the chosen Inventory Type and with anything already in
 *    the cart excluded. Checking rows there and confirming moves them
 *    into the cart above.
 */

'use strict';

(function () {
  var cartRows = document.getElementById('cart-rows');
  var cartCount = document.getElementById('cart-count');
  var cartCard = document.getElementById('cart-card');
  if (!cartRows) return; // transfer not found -- nothing on this page to wire

  var addCard = document.getElementById('add-items-card');
  var addToggle = document.getElementById('cart-add-toggle');
  var addCancel = document.getElementById('add-items-cancel');
  var addConfirm = document.getElementById('add-items-confirm');
  var addTypeSelect = document.getElementById('add-items-type');
  var addRows = document.getElementById('add-items-rows');
  var addCount = document.getElementById('add-items-count');
  var addHint = document.getElementById('add-items-hint');
  var poolDataEl = document.getElementById('add-items-pool-data');
  var allPoolItems = poolDataEl ? JSON.parse(poolDataEl.textContent) : [];
  var fromBranch = addCard ? addCard.dataset.fromBranch : '';

  function cartCodes() {
    return Array.prototype.map.call(cartRows.querySelectorAll('.scr-row[data-code]'), function (tr) {
      return tr.dataset.code;
    });
  }

  function updateCartCount() {
    var n = cartRows.querySelectorAll('.scr-row[data-code]').length;
    if (cartCount) cartCount.textContent = n + ' item' + (n === 1 ? '' : 's');
    var emptyRow = document.getElementById('cart-empty-row');
    if (n === 0 && !emptyRow) {
      var colspan = 7;
      var tr = document.createElement('tr');
      tr.id = 'cart-empty-row';
      tr.innerHTML = '<td colspan="' + colspan + '" style="padding:0"><div class="scr-empty">' +
        '<span class="scr-empty-ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#a9a6c4" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16v12H4zM4 7l2-3h12l2 3"></path></svg></span>' +
        '<div><div class="scr-empty-title">Cart is empty</div><p class="scr-empty-sub">Use Add Items above to pick from ' + fromBranch + '.</p></div></div></td>';
      cartRows.appendChild(tr);
    } else if (n > 0 && emptyRow) {
      emptyRow.remove();
    }
  }

  cartRows.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-cart-remove]');
    if (!btn) return;
    var row = btn.closest('.scr-row');
    if (row) row.remove();
    updateCartCount();
    /* whatever just left the cart becomes available in Add Items again */
    renderAddPool();
  });

  function escapeHtml(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }

  function cartRowHtml(item) {
    return '<tr class="scr-row" data-code="' + escapeHtml(item.code) + '">' +
      '<td><span class="scr-code">' + escapeHtml(item.code) + '</span></td>' +
      '<td style="font-weight:600">' + escapeHtml(item.name) + '</td>' +
      '<td><span class="scr-badge scr-badge-pending"><i></i>' + escapeHtml(item.item_type) + '</span></td>' +
      '<td class="scr-contact">' + escapeHtml(item.category) + '</td>' +
      '<td class="scr-contact">' + escapeHtml(item.vtype) + '</td>' +
      '<td><span class="scr-code">' + escapeHtml(item.rfid) + '</span></td>' +
      '<td style="text-align:right"><button type="button" class="scr-icon-btn" title="Remove from cart" data-cart-remove>' +
      '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M9 7V5a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2m3 0-1 13a1 1 0 0 1-1 1H8a1 1 0 0 1-1-1L6 7h12ZM10 11v6M14 11v6"></path></svg>' +
      '</button></td></tr>';
  }

  function addRowHtml(item) {
    return '<tr class="scr-row" data-search="' + escapeHtml((item.code + ' ' + item.name + ' ' + item.rfid).toLowerCase()) + '">' +
      '<td><input type="checkbox" data-add-check value="' + escapeHtml(item.code) + '"></td>' +
      '<td><span class="scr-code">' + escapeHtml(item.code) + '</span></td>' +
      '<td style="font-weight:600">' + escapeHtml(item.name) + '</td>' +
      '<td><span class="scr-badge scr-badge-pending"><i></i>' + escapeHtml(item.item_type) + '</span></td>' +
      '<td class="scr-contact">' + escapeHtml(item.category) + '</td>' +
      '<td class="scr-contact">' + escapeHtml(item.vtype) + '</td>' +
      '<td><span class="scr-code">' + escapeHtml(item.rfid) + '</span></td></tr>';
  }

  function addEmptyHtml(title, sub) {
    return '<tr><td colspan="7" style="padding:0"><div class="scr-empty">' +
      '<span class="scr-empty-ico"><svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#a9a6c4" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"></circle><path d="M12 7v5l3.5 2"></path></svg></span>' +
      '<div><div class="scr-empty-title">' + title + '</div><p class="scr-empty-sub">' + sub + '</p></div></div></td></tr>';
  }

  function updateAddConfirm() {
    var checked = addRows.querySelectorAll('input[data-add-check]:checked').length;
    if (addConfirm) addConfirm.disabled = checked === 0;
  }

  function renderAddPool() {
    if (!addRows) return;
    var type = addTypeSelect ? addTypeSelect.value : '';
    if (!type) {
      addRows.innerHTML = addEmptyHtml('Pick an Inventory Type', "Vehicles or assets still at " + fromBranch + " will appear here.");
      if (addCount) addCount.textContent = '0 items';
      updateAddConfirm();
      return;
    }
    var already = cartCodes();
    var matches = allPoolItems.filter(function (i) {
      return i.branch === fromBranch && i.item_type === type && already.indexOf(i.code) === -1;
    });
    addRows.innerHTML = matches.length
      ? matches.map(addRowHtml).join('')
      : addEmptyHtml('Nothing left to add', 'Every ' + type.toLowerCase() + ' at ' + fromBranch + ' is already in the cart.');
    updateAddConfirm();

    /* let byky-screen.js's own search/pagination re-scan the freshly built
       rows -- same trick byky-ims-transfer.js uses for New Transfer's pool,
       since applyFilters() re-reads .scr-row fresh every call rather than
       caching them, and also fixes the toolbar count text for us. */
    var searchInput = addCard.querySelector('.scr-search input');
    if (searchInput) {
      searchInput.dispatchEvent(new Event('input', { bubbles: true }));
    } else if (addCount) {
      addCount.textContent = matches.length + ' item' + (matches.length === 1 ? '' : 's');
    }
  }

  if (addTypeSelect) addTypeSelect.addEventListener('change', renderAddPool);
  if (addRows) {
    addRows.addEventListener('change', function (e) {
      if (e.target.matches('input[data-add-check]')) updateAddConfirm();
    });
  }

  if (addToggle && addCard) {
    addToggle.addEventListener('click', function () {
      addCard.hidden = !addCard.hidden;
      if (!addCard.hidden) {
        renderAddPool();
        addCard.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  }
  if (addCancel && addCard) {
    addCancel.addEventListener('click', function () {
      addCard.hidden = true;
      if (addTypeSelect) addTypeSelect.value = '';
      renderAddPool();
    });
  }

  if (addConfirm) {
    addConfirm.addEventListener('click', function () {
      var checked = addRows.querySelectorAll('input[data-add-check]:checked');
      var type = addTypeSelect ? addTypeSelect.value : '';
      checked.forEach(function (box) {
        var code = box.value;
        var item = allPoolItems.filter(function (i) { return i.code === code; })[0];
        if (item) cartRows.insertAdjacentHTML('beforeend', cartRowHtml(item));
      });
      updateCartCount();
      renderAddPool();
      if (addHint) addHint.textContent = 'Added ' + checked.length + ' item' + (checked.length === 1 ? '' : 's') + ' to the cart.';
    });
  }

  updateCartCount();
})();
