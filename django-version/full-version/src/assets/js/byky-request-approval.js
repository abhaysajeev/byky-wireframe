/**
 * Request Management -- Approve / Reject row actions, shared by Request
 * Approval and Card Discount Approval (both use the same [data-status-cell]
 * status badge + [data-request-approve]/[data-request-reject] row buttons).
 *
 * Confirms via SweetAlert2, per CLAUDE.md's own convention for write-actions
 * (see hrms/ims Mark Inactive for the same pattern). Nothing persists --
 * updates the row's own status badge for the rest of the session only.
 */

'use strict';

(function () {
  function setStatus(row, status) {
    var cell = row.querySelector('[data-status-cell]');
    var badge = cell && cell.querySelector('.scr-badge');
    if (!badge) return;
    var cls = status === 'Approved' ? 'scr-badge-approved' : status === 'Rejected' ? 'scr-badge-rejected' : 'scr-badge-pending';
    badge.className = 'scr-badge ' + cls;
    badge.innerHTML = '<i></i>' + status;
    row.dataset.status = status;
  }

  function rowLabel(row) {
    var code = row.querySelector('.scr-code');
    if (code) return code.textContent.trim();
    var title = row.querySelector('.scr-form-title');
    return title ? title.textContent.trim() : 'this request';
  }

  document.addEventListener('click', function (e) {
    var approveBtn = e.target.closest('[data-request-approve]');
    var rejectBtn = e.target.closest('[data-request-reject]');
    var btn = approveBtn || rejectBtn;
    if (!btn) return;

    // A list row (.scr-row/tr) if there is one -- nearer than .scr-card, so
    // it wins there. The detail page has no row, so this falls back to the
    // whole .scr-card, which holds exactly one [data-status-cell] to update.
    var row = btn.closest('.scr-row, tr, .scr-card');
    if (!row) return;
    var decision = approveBtn ? 'Approved' : 'Rejected';
    var verb = approveBtn ? 'approve' : 'reject';
    var name = rowLabel(row);

    function apply() { setStatus(row, decision); }

    if (typeof Swal === 'undefined') {
      apply();
      return;
    }
    Swal.fire({
      title: (approveBtn ? 'Approve' : 'Reject') + ' ' + name + '?',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: 'Yes, ' + verb,
      customClass: { confirmButton: 'btn btn-primary me-3', cancelButton: 'btn btn-label-secondary' },
      buttonsStyling: false
    }).then(function (result) {
      if (!result.isConfirmed) return;
      apply();
      Swal.fire({
        text: name + ' has been ' + decision.toLowerCase() + '.',
        icon: 'success',
        customClass: { confirmButton: 'btn btn-primary' },
        buttonsStyling: false
      });
    });
  });
})();
