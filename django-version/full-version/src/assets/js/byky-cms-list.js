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
    layout: {
      topStart: {
        rowClass: 'row m-3 my-0 justify-content-between',
        features: [{ pageLength: { menu: [10, 25, 50, 100], text: '_MENU_' } }]
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
    new DataTable(el, opts);
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
