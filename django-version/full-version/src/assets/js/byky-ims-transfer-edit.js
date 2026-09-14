/**
 * Edit Transfer / Edit Return -- row 48's UAT remarks (client's feedback
 * doc), and row 50's Return equivalent. Shared by both
 * ims_vehicle_transfer_edit.html and ims_vehicle_return_edit.html -- the
 * two pages use identical element ids (cart-rows, add-items-*,
 * decision-actions, ...), so one generic file drives both; only the
 * Approve toast's wording branches on the doc no.'s prefix.
 *
 * Three independent pieces, all frontend-only (CLAUDE.md 1 -- nothing here
 * persists past the page session):
 *
 * 1. Cart -- the record's currently selected items, server-rendered as
 *    real rows (there's only ever one demo record per page, so this list
 *    is small); each carries a Remove button.
 * 2. Add Items -- a toggled panel offering the source's pool (parsed once
 *    from add-items-pool-data, the same lazy json_script approach
 *    ims_vehicle_transfer_new.html's byky-ims-transfer.js uses), filtered
 *    by the chosen Inventory Type and with anything already in the cart
 *    excluded. Checking rows there and confirming moves them into the
 *    cart above. On a return this pool is honestly empty (nothing is
 *    currently out at a warehouse or event in the source data), so it
 *    only ever shows the empty state -- a true reflection of the data.
 * 3. Approve / Reject (rows 49/50) -- also available on this page, not
 *    only the list view's kebab (byky-ims-transfer-list.js has the
 *    list-row version). Instant, no confirm dialog; locks the page
 *    afterwards -- Save Changes, cart Remove and Add Items all disable,
 *    matching "once its done, then dont allow to edit/delete."
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

  // ── Approve / Reject (row 49) -- also available here, not only the list
  // view's kebab. Instant, no confirm dialog; locks the page against
  // further edits once decided, same as the list row does.
  var decisionActions = document.getElementById('decision-actions');
  var saveBtn = document.getElementById('save-changes-btn');

  function toast(text) {
    if (typeof Swal === 'undefined') return;
    Swal.fire({
      text: text,
      icon: 'success',
      toast: true,
      position: 'top-end',
      showConfirmButton: false,
      timer: 2500,
      timerProgressBar: true
    });
  }

  function lockPage(status, badgeClass, message) {
    var statusCell = document.querySelector('[data-status-cell]');
    var badge = statusCell && statusCell.querySelector('.scr-badge');
    if (badge) {
      badge.className = 'scr-badge ' + badgeClass;
      badge.innerHTML = '<i></i>' + status;
    }
    if (saveBtn) saveBtn.disabled = true;
    if (addToggle) addToggle.hidden = true;
    cartRows.querySelectorAll('[data-cart-remove]').forEach(function (btn) { btn.hidden = true; });
    if (decisionActions) {
      var span = decisionActions.querySelector('.scr-help');
      if (span) span.textContent = message;
      var approveBtn = decisionActions.querySelector('[data-transfer-approve]');
      var rejectBtn = decisionActions.querySelector('[data-transfer-reject]');
      if (approveBtn) approveBtn.remove();
      if (rejectBtn) rejectBtn.remove();
    }
  }

  if (decisionActions) {
    var crumbEl = document.querySelector('.scr-crumb b');
    var docNo = crumbEl ? crumbEl.textContent.trim() : '';
    var isReturn = docNo.indexOf('RTN') === 0;
    var lockedMsg = 'This ' + (isReturn ? 'return' : 'transfer') + ' has been decided and is locked against further edits.';

    decisionActions.addEventListener('click', function (e) {
      if (e.target.closest('[data-transfer-approve]')) {
        lockPage('Completed', 'scr-badge-active', lockedMsg);
        toast(docNo + (isReturn
          ? ' approved -- items added back to their branch.'
          : ' approved and synced with ERP.'));
      } else if (e.target.closest('[data-transfer-reject]')) {
        lockPage('Rejected', 'scr-badge-inactive', lockedMsg);
        toast(docNo + ' rejected.');
      }
    });
  }

  updateCartCount();
})();
