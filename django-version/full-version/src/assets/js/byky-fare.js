/**
 * BYKY Fare & Schemes
 *
 * Interactivity for the two create forms adapted from the client mockups:
 * the time-slab table on Fare Entry, and the promotion/free-item tables on
 * Scheme Creation. Wireframe phase -- nothing is submitted anywhere.
 *
 * Migrated onto the .scr-* design system: the time-slab / free-slab editors
 * use the scr-veil/scr-drawer markup, but their show/hide + prefill logic
 * stays bespoke here rather than byky-screen.js's generic wireDrawer, since
 * their rows are built by this script at runtime, not rendered server-side
 * per record (there is no json_script blob to read a record from).
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

  /** Open/close helpers for a scr-veil/scr-drawer pair driven by this script
      rather than byky-screen.js's data-scr-open (see file header). Clicking
      the veil or pressing Escape closes it, matching every other drawer in
      the app even though this pair isn't registered with byky-screen.js. */
  function drawerControls(veilId, drawerId) {
    const veil = document.getElementById(veilId);
    const drawer = document.getElementById(drawerId);
    const api = {
      open() {
        if (veil) veil.hidden = false;
        if (drawer) drawer.hidden = false;
      },
      close() {
        if (veil) veil.hidden = true;
        if (drawer) drawer.hidden = true;
      }
    };
    if (veil) veil.addEventListener('click', api.close);
    document.addEventListener('keydown', e => {
      if (e.key === 'Escape' && drawer && !drawer.hidden) api.close();
    });
    return api;
  }

  // Fare Entry -- time slab rows
  // --------------------------------------------------------------------
  const slabToggle = document.getElementById('timeSlabToggle');
  const slabArea = document.getElementById('timeSlabArea');
  const slabRows = document.getElementById('timeSlabRows');
  const slabDrawer = drawerControls('timeSlabVeil', 'offcanvasTimeSlab');

  // Time slabs -- summary grid + labelled drawer
  // --------------------------------------------------------------------
  // Ten fields per slab cannot stay legible as bare inputs in a table row,
  // so the grid shows formatted values and the drawer owns the labelled
  // form. `editing` holds the row being changed, or null when adding.
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
      <td style="text-align:center">
        <span class="scr-badge scr-badge-pending row-index">1</span>
      </td>
      <td style="font-weight:600">${appliesLabel(slab)}</td>
      <td>${slab.from} &ndash; ${slab.to}</td>
      <td style="text-align:right; font-weight:600">${aed(slab.basic)}</td>
      <td style="text-align:right">${mins(slab.grace)}</td>
      <td style="text-align:right">${mins(slab.interval)}</td>
      <td style="text-align:right">${aed(slab.concPrice)}</td>
      <td style="text-align:right">${mins(slab.concGrace)}</td>
      <td style="text-align:right; white-space:nowrap">
        <button type="button" class="scr-icon-btn scr-icon-btn-edit row-edit" aria-label="Edit slab" style="width:26px; height:26px">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4l10-10a2.1 2.1 0 0 0-3-3L5 17z"></path></svg>
        </button>
        <button type="button" class="scr-icon-btn row-remove" aria-label="Remove slab" style="width:26px; height:26px">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"></path></svg>
        </button>
      </td>`;
    tr.querySelector('.row-edit').addEventListener('click', () => {
      editing = tr;
      writeSlabForm(JSON.parse(tr.dataset.slab));
      document.getElementById('offcanvasTimeSlabLabel').textContent = 'Edit Time Slab';
      slabDrawer.open();
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
      <td colspan="9" style="text-align:center; color:#9490bb; padding:26px 14px">
        No pricing windows yet. Use <span style="font-weight:600">Add Time Slab</span> to create one.
      </td>`;
    slabRows.appendChild(tr);
  }

  const addTimeSlabBtn = document.getElementById('addTimeSlab');
  if (addTimeSlabBtn) {
    addTimeSlabBtn.addEventListener('click', () => {
      editing = null;
      document.getElementById('offcanvasTimeSlabLabel').textContent = 'Add Time Slab';
      writeSlabForm({ applies: 'all', day: '', date: '', from: '10:00', to: '11:00', basic: 90, grace: 5, interval: 10, concPrice: 10, concGrace: 0 });
      slabDrawer.open();
    });
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
      slabDrawer.close();
    });
  }

  ['timeSlabClose', 'timeSlabCancel'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) btn.addEventListener('click', () => { editing = null; slabDrawer.close(); });
  });

  if (slabToggle && slabArea) {
    slabToggle.addEventListener('click', () => {
      // byky-screen.js's delegated .scr-toggle listener flips is-on before
      // this handler runs (this script loads after it) -- read the result.
      const enabled = slabToggle.classList.contains('is-on');
      slabArea.hidden = !enabled;
      if (enabled) syncSlabEmptyState();
    });
  }
  syncSlabEmptyState();

  // Scheme Creation -- promotion items, free items, free-item slabs
  // --------------------------------------------------------------------
  function itemRowHtml(count) {
    return `
      <td style="text-align:center"><span class="scr-badge scr-badge-pending row-index">${count}</span></td>
      <td><select class="scr-input" style="height:34px; font-size:12px">${optionsFrom('tplVehicleTypes')}</select></td>
      <td><select class="scr-input" style="height:34px; font-size:12px">${optionsFrom('tplPackages')}</select></td>
      <td style="text-align:center">
        <button type="button" class="scr-icon-btn row-remove" aria-label="Remove row" style="width:26px; height:26px">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"></path></svg>
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
  const freeSlabDrawer = drawerControls('freeSlabVeil', 'offcanvasFreeSlab');
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
      <td style="text-align:center"><span class="scr-badge scr-badge-pending row-index">1</span></td>
      <td style="font-weight:600">${fsAppliesLabel(r)}</td>
      <td>${r.from} &ndash; ${r.to}</td>
      <td>${r.vehicle}</td>
      <td>${r.pkg}</td>
      <td style="text-align:right; font-weight:600">${r.qty}</td>
      <td style="text-align:right; white-space:nowrap">
        <button type="button" class="scr-icon-btn scr-icon-btn-edit row-edit" aria-label="Edit slab" style="width:26px; height:26px">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4l10-10a2.1 2.1 0 0 0-3-3L5 17z"></path></svg>
        </button>
        <button type="button" class="scr-icon-btn row-remove" aria-label="Remove slab" style="width:26px; height:26px">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13"></path></svg>
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
      freeSlabDrawer.open();
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
      <td colspan="7" style="text-align:center; color:#9490bb; padding:26px 14px">
        No slab restrictions yet. Use <span style="font-weight:600">Add Time Slab</span> to create one.
      </td>`;
    freeSlabRows.appendChild(tr);
  }

  const addFreeSlabBtn = document.getElementById('addFreeSlab');
  if (addFreeSlabBtn) {
    addFreeSlabBtn.addEventListener('click', () => {
      editingFree = null;
      document.getElementById('offcanvasFreeSlabLabel').textContent = 'Add Time Slab';
      fs.applies.value = 'all'; fs.day.value = ''; fs.date.value = '';
      fs.from.value = '10:00'; fs.to.value = '11:00'; fs.qty.value = 1;
      fsSyncApplies();
      freeSlabDrawer.open();
    });
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
      freeSlabDrawer.close();
    });
  }

  ['freeSlabClose', 'freeSlabCancel'].forEach(id => {
    const btn = document.getElementById(id);
    if (btn) btn.addEventListener('click', () => { editingFree = null; freeSlabDrawer.close(); });
  });
  syncFreeSlabEmptyState();

  // Toggles that reveal an optional block -- each is a scr-toggle button;
  // byky-screen.js's delegated listener flips its is-on class before this
  // one runs (this script loads after it), so read the class, don't toggle it.
  [['freeItemsToggle', 'freeItemsArea'], ['freeSlabToggle', 'freeSlabArea']].forEach(([t, a]) => {
    const toggle = document.getElementById(t);
    const area = document.getElementById(a);
    if (toggle && area) toggle.addEventListener('click', () => {
      const enabled = toggle.classList.contains('is-on');
      area.hidden = !enabled;
      if (enabled) syncFreeSlabEmptyState();
    });
  });

  attachPickers(document);
})();
