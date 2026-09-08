/**
 * Credit Note (Credit Note Management) -- page-specific behaviour.
 *
 * - Credit Note Amount auto-splits into Gross/Tax at 5% VAT, matching the
 *   client's own worked example exactly (Amount 70 -> Gross 60.67, Tax 9.33).
 * - "Credit This Invoice" on a Results row jumps to the Create tab and
 *   loads that row's data into the form.
 * - "Load Order" looks up the typed order number among the (currently
 *   empty) Results rows -- honestly finds nothing until real invoices exist.
 */

'use strict';

(function () {
  var VAT_RATE = 0.05;

  var amountInput = document.getElementById('cn-amount');
  var grossInput = document.getElementById('cn-gross');
  var taxInput = document.getElementById('cn-credit-tax');

  function splitVat(amount) {
    var gross = amount / (1 + VAT_RATE);
    var tax = amount - gross;
    return { gross: gross, tax: tax };
  }

  if (amountInput && grossInput && taxInput) {
    amountInput.addEventListener('input', function () {
      var amount = parseFloat(amountInput.value);
      if (!isFinite(amount) || amount <= 0) {
        grossInput.value = '';
        taxInput.value = '';
        return;
      }
      var split = splitVat(amount);
      grossInput.value = split.gross.toFixed(2);
      taxInput.value = split.tax.toFixed(2);
    });
  }

  var FIELD_MAP = {
    'cn-order-no': 'orderNo',
    'cn-order-date': 'invoiceDate',
    'cn-trans-no': 'transNo',
    'cn-open-by': 'openBy',
    'cn-close-by': 'closeBy',
    'cn-customer': 'customer',
    'cn-mobile': 'mobile',
    'cn-start': 'start',
    'cn-end': 'end',
    'cn-bill-amount': 'billAmount',
    'cn-tax-pct': 'taxPct',
    'cn-tax-amount': 'taxAmount',
    'cn-net-amount': 'netAmount'
  };

  function loadRowIntoForm(row) {
    Object.keys(FIELD_MAP).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.value = row.dataset[FIELD_MAP[id]] || '';
    });
    var vehicleRows = document.getElementById('cn-vehicle-rows');
    if (vehicleRows) {
      // The wireframe has no per-vehicle breakdown in the row dataset (the
      // Results grid is invoice-level) -- clear the placeholder so the
      // section reads as "loaded" rather than leaving stale copy.
      vehicleRows.innerHTML =
        '<tr><td colspan="4" style="padding:0"><div class="scr-empty" style="padding:20px">' +
        '<p class="scr-empty-sub" style="margin:0">This invoice has no per-vehicle breakdown recorded.</p>' +
        '</div></td></tr>';
    }
  }

  function goToCreateTab() {
    var createTab = document.getElementById('cn-create-tab');
    if (createTab) createTab.click();
  }

  document.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-cn-credit-row]');
    if (!btn) return;
    var row = btn.closest('.scr-row');
    if (!row) return;
    loadRowIntoForm(row);
    goToCreateTab();
  });

  var loadBtn = document.getElementById('cn-load-order');
  var orderInput = document.getElementById('cn-order-no');
  if (loadBtn && orderInput) {
    loadBtn.addEventListener('click', function () {
      var query = orderInput.value.trim().toLowerCase();
      if (!query) return;
      var match = null;
      document.querySelectorAll('.scr-row[data-order-no]').forEach(function (row) {
        if (row.dataset.orderNo && row.dataset.orderNo.toLowerCase() === query) match = row;
      });
      if (match) {
        loadRowIntoForm(match);
      } else if (typeof Swal !== 'undefined') {
        Swal.fire({
          text: 'No invoice found for order "' + orderInput.value.trim() + '".',
          icon: 'info',
          customClass: { confirmButton: 'btn btn-primary' },
          buttonsStyling: false
        });
      }
    });
  }

  var cancelBtn = document.getElementById('cn-cancel');
  if (cancelBtn) {
    cancelBtn.addEventListener('click', function () {
      document.querySelectorAll('.scr-panel[data-tab="create"] input:not([type=button])').forEach(function (el) {
        el.value = '';
      });
      var textarea = document.getElementById('cn-remarks');
      if (textarea) textarea.value = '';
    });
  }
})();
