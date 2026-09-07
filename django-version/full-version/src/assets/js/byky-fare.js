/**
 * BYKY Fare & Schemes
 *
 * Interactivity for the two create forms adapted from the client mockups:
 * the time-slab table on Fare Entry, and the promotion/free-item tables on
 * Scheme Creation. Wireframe phase -- nothing is submitted anywhere.
 */

'use strict';

(function () {
  const optionsFrom = selectId => {
    const src = document.getElementById(selectId);
    return src ? src.innerHTML : '<option value="">Select</option>';
  };

  /** Renumber the leading counter cell after any add or remove. */
  function renumber(tbody) {
    [...tbody.rows]
      .filter(row => !row.classList.contains('slab-empty'))
      .forEach((row, i) => {
        const badge = row.querySelector('.row-index');
        if (badge) badge.textContent = i + 1;
      });
  }

  function wireRemove(tr, tbody) {
    tr.querySelector('.row-remove').addEventListener('click', () => {
      tr.remove();
      renumber(tbody);
    });
  }

  /** Flatpickr on any date input added after page load. */
  function attachPickers(scope) {
    if (typeof flatpickr === 'undefined') return;
    scope.querySelectorAll('.byky-date').forEach(el => {
      if (!el._flatpickr) flatpickr(el, { dateFormat: 'd M Y', allowInput: true });
    });
  }

  // Fare Entry -- time slab rows
  // --------------------------------------------------------------------
  const slabToggle = document.getElementById('timeSlabToggle');
  const slabArea = document.getElementById('timeSlabArea');
  const slabRows = document.getElementById('timeSlabRows');

  // Time slabs -- summary grid + labelled drawer
  // --------------------------------------------------------------------
  // Ten fields per slab cannot stay legible as bare inputs in a table row,
  // so the grid shows formatted values and the drawer owns the labelled
  // form. `editing` holds the row being changed, or null when adding.
  const slabDrawerEl = document.getElementById('offcanvasTimeSlab');
  const slabForm = {
    applies: document.getElementById('slab-applies'),
    dayWrap: document.getElementById('slab-day-wrap'),
    dateWrap: document.getElementById('slab-date-wrap'),
    day: document.getElementById('slab-day'),
    date: document.getElementById('slab-date'),
    from: document.getElementById('slab-from'),
    to: document.getElementById('slab-to'),
    basic: document.getElementById('slab-basic'),
    grace: document.getElementById('slab-grace'),
    interval: document.getElementById('slab-interval'),
    concPrice: document.getElementById('slab-conc-price'),
    concGrace: document.getElementById('slab-conc-grace')
  };
  let editing = null;

  const aed = v => 'AED ' + Number(v || 0).toFixed(2);
  const mins = v => (Number(v || 0)) + ' min';

  function appliesLabel(slab) {
    if (slab.applies === 'day') return slab.day;
    if (slab.applies === 'date') return slab.date || 'Date not set';
    return 'Every day';
  }

  function syncAppliesFields() {
    if (!slabForm.applies) return;
    slabForm.dayWrap.hidden = slabForm.applies.value !== 'day';
    slabForm.dateWrap.hidden = slabForm.applies.value !== 'date';
  }
  if (slabForm.applies) slabForm.applies.addEventListener('change', syncAppliesFields);

  function readSlabForm() {
    return {
      applies: slabForm.applies.value,
      day: slabForm.day.value,
      date: slabForm.date.value,
      from: slabForm.from.value,
      to: slabForm.to.value,
      basic: slabForm.basic.value,
      grace: slabForm.grace.value,
      interval: slabForm.interval.value,
      concPrice: slabForm.concPrice.value,
      concGrace: slabForm.concGrace.value
    };
  }

  function writeSlabForm(slab) {
    slabForm.applies.value = slab.applies;
    slabForm.day.value = slab.day;
    slabForm.date.value = slab.date;
    slabForm.from.value = slab.from;
    slabForm.to.value = slab.to;
    slabForm.basic.value = slab.basic;
    slabForm.grace.value = slab.grace;
    slabForm.interval.value = slab.interval;
    slabForm.concPrice.value = slab.concPrice;
    slabForm.concGrace.value = slab.concGrace;
    syncAppliesFields();
  }

  function renderSlabRow(tr, slab) {
    tr.dataset.slab = JSON.stringify(slab);
    tr.innerHTML = `
      <td class="text-center">
        <span class="badge bg-label-primary rounded-pill row-index">1</span>
      </td>
      <td><span class="fw-medium">${appliesLabel(slab)}</span></td>
      <td>${slab.from} &ndash; ${slab.to}</td>
      <td class="text-end fw-medium">${aed(slab.basic)}</td>
      <td class="text-end">${mins(slab.grace)}</td>
      <td class="text-end">${mins(slab.interval)}</td>
      <td class="text-end">${aed(slab.concPrice)}</td>
      <td class="text-end">${mins(slab.concGrace)}</td>
      <td class="text-end text-nowrap">
        <button type="button" class="btn btn-icon btn-sm btn-text-secondary rounded-pill row-edit" aria-label="Edit slab">
          <i class="icon-base ti tabler-edit icon-16px"></i>
        </button>
        <button type="button" class="btn btn-icon btn-sm btn-text-danger rounded-pill row-remove" aria-label="Remove slab">
          <i class="icon-base ti tabler-trash icon-16px"></i>
        </button>
      </td>`;
    tr.querySelector('.row-edit').addEventListener('click', () => {
      editing = tr;
      writeSlabForm(JSON.parse(tr.dataset.slab));
      document.getElementById('offcanvasTimeSlabLabel').textContent = 'Edit Time Slab';
      bootstrap.Offcanvas.getOrCreateInstance(slabDrawerEl).show();
    });
    tr.querySelector('.row-remove').addEventListener('click', () => {
      tr.remove();
      renumber(slabRows);
      syncSlabEmptyState();
    });
    renumber(slabRows);
  }

  /** Placeholder row so the grid never reads as a broken table. */
  function syncSlabEmptyState() {
    if (!slabRows) return;
    const existing = slabRows.querySelector('.slab-empty');
    const hasRows = [...slabRows.rows].some(r => !r.classList.contains('slab-empty'));
    if (hasRows) {
      if (existing) existing.remove();
      return;
    }
    if (existing) return;
    const tr = document.createElement('tr');
    tr.className = 'slab-empty';
    tr.innerHTML = `
      <td colspan="9" class="text-center text-body-secondary py-6">
        No pricing windows yet. Use <span class="fw-medium">Add Time Slab</span> to create one.
      </td>`;
    slabRows.appendChild(tr);
  }

  const slabSaveBtn = document.getElementById('slabSave');
  if (slabSaveBtn) {
    slabSaveBtn.addEventListener('click', () => {
      const slab = readSlabForm();
      const tr = editing || document.createElement('tr');
      renderSlabRow(tr, slab);
      if (!editing) slabRows.appendChild(tr);
      editing = null;
      renumber(slabRows);
      syncSlabEmptyState();
      bootstrap.Offcanvas.getOrCreateInstance(slabDrawerEl).hide();
    });
  }

  if (slabDrawerEl) {
    slabDrawerEl.addEventListener('hidden.bs.offcanvas', () => {
      editing = null;
      document.getElementById('offcanvasTimeSlabLabel').textContent = 'Add Time Slab';
    });
  }

  if (slabToggle && slabArea) {
    slabToggle.addEventListener('change', () => {
      slabArea.hidden = !slabToggle.checked;
      if (slabToggle.checked) syncSlabEmptyState();
    });
  }
  syncSlabEmptyState();

  // Scheme Creation -- promotion items, free items, free-item slabs
  // --------------------------------------------------------------------
  function itemRowHtml(count) {
    return `
      <td class="text-center"><span class="badge bg-label-primary rounded-pill row-index">${count}</span></td>
      <td><select class="form-select form-select-sm">${optionsFrom('tplVehicleTypes')}</select></td>
      <td><select class="form-select form-select-sm">${optionsFrom('tplPackages')}</select></td>
      <td class="text-center">
        <button type="button" class="btn btn-icon btn-sm btn-text-danger rounded-pill row-remove" aria-label="Remove row">
          <i class="icon-base ti tabler-trash icon-16px"></i>
        </button>
      </td>`;
  }

  function bindSimpleTable(addBtnId, tbodyId, builder) {
    const btn = document.getElementById(addBtnId);
    const tbody = document.getElementById(tbodyId);
    if (!btn || !tbody) return;
    const add = () => {
      const tr = document.createElement('tr');
      tr.innerHTML = builder(tbody.rows.length + 1);
      tbody.appendChild(tr);
      wireRemove(tr, tbody);
      attachPickers(tr);
    };
    btn.addEventListener('click', add);
    if (!tbody.rows.length) add();
  }

  bindSimpleTable('addPromoItem', 'promoItemRows', itemRowHtml);
  bindSimpleTable('addFreeItem', 'freeItemRows', itemRowHtml);

  // Free-item slabs -- same summary grid + labelled drawer as Fare Entry
  // --------------------------------------------------------------------
  const freeSlabRows = document.getElementById('freeSlabRows');
  const freeDrawerEl = document.getElementById('offcanvasFreeSlab');
  const fs = {
    applies: document.getElementById('fs-applies'),
    dayWrap: document.getElementById('fs-day-wrap'),
    dateWrap: document.getElementById('fs-date-wrap'),
    day: document.getElementById('fs-day'),
    date: document.getElementById('fs-date'),
    from: document.getElementById('fs-from'),
    to: document.getElementById('fs-to'),
    vehicle: document.getElementById('fs-vehicle'),
    pkg: document.getElementById('fs-package'),
    qty: document.getElementById('fs-qty')
  };
  let editingFree = null;

  function fsSyncApplies() {
    if (!fs.applies) return;
    fs.dayWrap.hidden = fs.applies.value !== 'day';
    fs.dateWrap.hidden = fs.applies.value !== 'date';
  }
  if (fs.applies) fs.applies.addEventListener('change', fsSyncApplies);

  function fsAppliesLabel(r) {
    if (r.applies === 'day') return r.day;
    if (r.applies === 'date') return r.date || 'Date not set';
    return 'Every day';
  }

  function renderFreeSlabRow(tr, r) {
    tr.dataset.slab = JSON.stringify(r);
    tr.innerHTML = `
      <td class="text-center"><span class="badge bg-label-primary rounded-pill row-index">1</span></td>
      <td><span class="fw-medium">${fsAppliesLabel(r)}</span></td>
      <td>${r.from} &ndash; ${r.to}</td>
      <td>${r.vehicle}</td>
      <td>${r.pkg}</td>
      <td class="text-end fw-medium">${r.qty}</td>
      <td class="text-end text-nowrap">
        <button type="button" class="btn btn-icon btn-sm btn-text-secondary rounded-pill row-edit" aria-label="Edit slab">
          <i class="icon-base ti tabler-edit icon-16px"></i>
        </button>
        <button type="button" class="btn btn-icon btn-sm btn-text-danger rounded-pill row-remove" aria-label="Remove slab">
          <i class="icon-base ti tabler-trash icon-16px"></i>
        </button>
      </td>`;
    tr.querySelector('.row-edit').addEventListener('click', () => {
      editingFree = tr;
      const v = JSON.parse(tr.dataset.slab);
      fs.applies.value = v.applies; fs.day.value = v.day; fs.date.value = v.date;
      fs.from.value = v.from; fs.to.value = v.to;
      fs.vehicle.value = v.vehicle; fs.pkg.value = v.pkg; fs.qty.value = v.qty;
      fsSyncApplies();
      document.getElementById('offcanvasFreeSlabLabel').textContent = 'Edit Time Slab';
      bootstrap.Offcanvas.getOrCreateInstance(freeDrawerEl).show();
    });
    tr.querySelector('.row-remove').addEventListener('click', () => {
      tr.remove();
      renumber(freeSlabRows);
      syncFreeSlabEmptyState();
    });
    renumber(freeSlabRows);
  }

  function syncFreeSlabEmptyState() {
    if (!freeSlabRows) return;
    const existing = freeSlabRows.querySelector('.slab-empty');
    const hasRows = [...freeSlabRows.rows].some(r => !r.classList.contains('slab-empty'));
    if (hasRows) {
      if (existing) existing.remove();
      return;
    }
    if (existing) return;
    const tr = document.createElement('tr');
    tr.className = 'slab-empty';
    tr.innerHTML = `
      <td colspan="7" class="text-center text-body-secondary py-6">
        No slab restrictions yet. Use <span class="fw-medium">Add Time Slab</span> to create one.
      </td>`;
    freeSlabRows.appendChild(tr);
  }

  const freeSlabSaveBtn = document.getElementById('freeSlabSave');
  if (freeSlabSaveBtn) {
    freeSlabSaveBtn.addEventListener('click', () => {
      const r = {
        applies: fs.applies.value, day: fs.day.value, date: fs.date.value,
        from: fs.from.value, to: fs.to.value,
        vehicle: fs.vehicle.value, pkg: fs.pkg.value, qty: fs.qty.value
      };
      const tr = editingFree || document.createElement('tr');
      renderFreeSlabRow(tr, r);
      if (!editingFree) freeSlabRows.appendChild(tr);
      editingFree = null;
      renumber(freeSlabRows);
      syncFreeSlabEmptyState();
      bootstrap.Offcanvas.getOrCreateInstance(freeDrawerEl).hide();
    });
  }

  if (freeDrawerEl) {
    freeDrawerEl.addEventListener('hidden.bs.offcanvas', () => {
      editingFree = null;
      document.getElementById('offcanvasFreeSlabLabel').textContent = 'Add Time Slab';
    });
  }
  syncFreeSlabEmptyState();

  // Toggles that reveal an optional block
  [['freeItemsToggle', 'freeItemsArea'], ['freeSlabToggle', 'freeSlabArea']].forEach(([t, a]) => {
    const toggle = document.getElementById(t);
    const area = document.getElementById(a);
    if (toggle && area) toggle.addEventListener('change', () => {
      area.hidden = !toggle.checked;
      if (toggle.checked) syncFreeSlabEmptyState();
    });
  });

  attachPickers(document);
})();
