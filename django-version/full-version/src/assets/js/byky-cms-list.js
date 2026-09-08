/**
 * BYKY CMS list screens
 *
 * One initialiser for every Module 1 DataTable. Wireframe phase: the data is
 * already in the DOM, so DataTables runs client-side. Production will need a
 * server-side endpoint per list (see CLAUDE.md).
 */

'use strict';

(function () {
  // FSD section 12 gives per-screen grid specs; the shared parts are the page
  // length menu, the search box and the export collection.
  const common = table => ({
    // 15 rows per page across every list on the site -- long enough to compare
    // a working set, short enough that a 1,060-row grid never renders in full.
    pageLength: 15,
    layout: {
      topStart: {
        rowClass: 'row m-3 my-0 justify-content-between',
        features: [{ pageLength: { menu: [15, 25, 50, 100], text: '_MENU_' } }]
      },
      topEnd: {
        features: [
          { search: { placeholder: table.dataset.searchLabel || 'Search', text: '_INPUT_' } }
        ]
      },
      bottomStart: { features: ['info'] },
      bottomEnd: { features: ['paging'] }
    },
    responsive: true,
    deferRender: true,
    processing: true
  });

  document.querySelectorAll('table[class*="datatables-"]').forEach(el => {
    const opts = common(el);
    // Actions column is never sortable or searchable.
    const head = el.querySelectorAll('thead th');
    const last = head.length - 1;
    if (head[last] && /action/i.test(head[last].textContent)) {
      opts.columnDefs = [{ targets: last, orderable: false, searchable: false }];
    }
    // Kept on the element so a page-level Export button (see below) can read
    // back exactly the filtered/sorted rows the user is currently looking at.
    el._dt = new DataTable(el, opts);
  });

  // Generic CSV export -- any button with data-export-table="<table selector>"
  // downloads that table's current filtered rows (DataTables' own "search:
  // applied" scope), skipping the Actions column. DataTables' own Buttons
  // extension isn't vendored (only its CSS is -- no JS, no jszip/pdfmake), so
  // rather than pull in a new library for one export button, this is a small
  // dependency-free Blob download, reusable by any other legacy list screen.
  function csvCell(v) {
    v = v === null || v === undefined ? '' : String(v).trim();
    return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
  }
  document.querySelectorAll('[data-export-table]').forEach(btn => {
    btn.addEventListener('click', () => {
      const table = document.querySelector(btn.dataset.exportTable);
      const dt = table && table._dt;
      if (!dt) return;
      const columns = [];
      table.querySelectorAll('thead th').forEach((th, i) => {
        if (/action/i.test(th.textContent)) return;
        columns.push({ i, label: th.textContent.trim() });
      });
      const rows = dt.rows({ search: 'applied' }).nodes().toArray();
      const lines = [columns.map(c => csvCell(c.label)).join(',')];
      rows.forEach(tr => {
        const cells = tr.querySelectorAll('td');
        lines.push(columns.map(c => csvCell(cells[c.i] ? cells[c.i].textContent : '')).join(','));
      });
      const blob = new Blob([lines.join('\r\n')], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = (btn.dataset.exportName || 'export') + '.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    });
  });

  // Mark Inactive / Mark Active -- a row-level status toggle for grids that
  // don't have a dedicated block/unblock console screen of their own (see
  // hrms_employee_block_unblock.html for the pattern where one exists).
  // Confirms via SweetAlert2 (vendored, unused elsewhere so far) per
  // CLAUDE.md's own documented convention for write-actions; nothing is
  // persisted, so this only updates the row's own badge for the rest of the
  // session.
  document.addEventListener('click', e => {
    const btn = e.target.closest('[data-mark-inactive]');
    if (!btn) return;
    e.preventDefault();
    const row = btn.closest('tr');
    // The row can carry other .badge elements (e.g. a Category chip) before
    // the status one in DOM order -- a bare row.querySelector('.badge') once
    // grabbed that instead and silently corrupted it. data-status-cell marks
    // the actual status cell explicitly, the same fix already applied to the
    // checkbox and cascading-dropdown prefill bugs elsewhere in this app.
    const statusCell = row && row.querySelector('[data-status-cell]');
    const badge = statusCell && statusCell.querySelector('.badge');
    if (!badge) return;
    const nameEl = row.querySelector('[data-row-name]');
    const name = nameEl ? nameEl.textContent.trim() : 'this item';
    const goingInactive = badge.textContent.trim() !== 'Inactive';
    const verb = goingInactive ? 'inactive' : 'active';

    function apply() {
      badge.textContent = goingInactive ? 'Inactive' : 'Approved';
      badge.className = 'badge rounded-pill ' + (goingInactive ? 'bg-label-danger' : 'bg-label-success');
      btn.textContent = goingInactive ? 'Mark Active' : 'Mark Inactive';
    }

    if (typeof Swal === 'undefined') {
      apply();
      return;
    }
    Swal.fire({
      title: `Mark ${name} ${verb}?`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonText: `Yes, mark ${verb}`,
      customClass: { confirmButton: 'btn btn-primary me-3', cancelButton: 'btn btn-label-secondary' },
      buttonsStyling: false
    }).then(result => {
      if (!result.isConfirmed) return;
      apply();
      Swal.fire({
        text: `${name} is now ${verb}.`,
        icon: 'success',
        customClass: { confirmButton: 'btn btn-primary' },
        buttonsStyling: false
      });
    });
  });

  // Select2 on any drawer dropdown that asks for it.
  if (window.jQuery && jQuery.fn.select2) {
    jQuery('.select2').each(function () {
      const $this = jQuery(this);
      $this.select2({ dropdownParent: $this.parent(), placeholder: $this.data('placeholder') || 'Select' });
    });
  }

  // FSD 1.4 section 17: Hotel Commission is enabled only when Is Hotel is checked.
  const isHotel = document.getElementById('flag-ishotel');
  const commission = document.getElementById('hotel-commission');
  if (isHotel && commission) {
    isHotel.addEventListener('change', () => {
      commission.disabled = !isHotel.checked;
      if (!isHotel.checked) commission.value = '0.00';
    });
  }

  // Dual-entity tab screens (FSD 1.2) keep ONE page-header action button; it
  // retargets to whichever tab is active so button placement never moves.
  const headerAction = document.querySelector('.byky-page-action');
  if (headerAction) {
    document.querySelectorAll('[data-bs-toggle="tab"]').forEach(tab => {
      tab.addEventListener('shown.bs.tab', () => {
        const target = tab.dataset.addTarget;
        const label = tab.dataset.addLabel;
        if (!target || !label) return;
        headerAction.setAttribute('data-bs-target', target);
        headerAction.setAttribute('href', target);
        headerAction.querySelector('.byky-action-label').textContent = label;
      });
    });
  }

  // FSD 1.9: Select All toggles every permission checkbox on that row.
  document.querySelectorAll('.privilege-select-all').forEach(box => {
    box.addEventListener('change', () => {
      box
        .closest('tr')
        .querySelectorAll('input[type="checkbox"]:not(.privilege-select-all)')
        .forEach(cb => (cb.checked = box.checked));
    });
  });
})();
