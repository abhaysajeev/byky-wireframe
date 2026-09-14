/**
 * Inventory Transfer & Return -- Transfer Approve/Reject (row 49 of the
 * client's feedback doc: "Transfer: Approve/Reject, Note: RMS > ERP").
 *
 * A one-time, instant decision (no confirm dialog -- frontend-only actions
 * stay a direct click) that locks the row: Edit/Approve/Reject/Delete all
 * disappear from the kebab afterwards, replaced by a plain "Locked" note,
 * since the client's ask is explicit that a decided transfer can't be
 * edited or deleted again. Approving simulates the sync to ERP with a
 * brief toast; nothing here actually integrates with anything.
 */

'use strict';

(function () {
  function lockedHtml() {
    return '<span class="scr-help" style="margin:0" title="Approve/Reject is one-time -- Edit and Delete lock once a decision is made">Locked</span>';
  }

  function setStatus(row, status, badgeClass) {
    var cell = row.querySelector('[data-status-cell]');
    var badge = cell && cell.querySelector('.scr-badge');
    if (badge) {
      badge.className = 'scr-badge ' + badgeClass;
      badge.innerHTML = '<i></i>' + status;
    }
    row.dataset.status = status;
    var actions = row.querySelector('[data-transfer-actions]');
    if (actions) actions.innerHTML = lockedHtml();
  }

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

  document.addEventListener('click', function (e) {
    var approveBtn = e.target.closest('[data-transfer-approve]');
    var rejectBtn = e.target.closest('[data-transfer-reject]');
    if (!approveBtn && !rejectBtn) return;

    var row = (approveBtn || rejectBtn).closest('.scr-row');
    if (!row) return;
    var docNo = row.querySelector('.scr-code');
    var name = docNo ? docNo.textContent.trim() : 'This transfer';

    if (approveBtn) {
      setStatus(row, 'Completed', 'scr-badge-active');
      toast(name + ' approved and synced with ERP.');
    } else {
      setStatus(row, 'Rejected', 'scr-badge-inactive');
      toast(name + ' rejected.');
    }
  });
})();
