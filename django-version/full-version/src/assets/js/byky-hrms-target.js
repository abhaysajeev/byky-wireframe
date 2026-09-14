/**
 * Target -- RMS WEB APK UI.xlsx feedback (byky Docs/new html/target.html).
 *
 * The drawer's period-type field (kind "custom", data-days-host="type")
 * gets a 4-way segmented toggle (Yearly/Monthly/Daily/Custom Date Range)
 * rendered here, matching the mockup's own tab-btn pills rather than a
 * plain <select> -- a hidden input carries the chosen value as data-field
 * "type" so byky-drawer.js's generic show_if wiring drives which of the
 * 4 period blocks (already declared in drawers.py's TARGET_PROFILE spec)
 * is visible, exactly like any other field.
 *
 * Also owns Daily's Day options, recomputed from year/month so it never
 * offers a 31st for a 30-day month (leap-year aware via
 * `new Date(year, month, 0).getDate()`, same trick as the mockup).
 */

'use strict';

(function () {
  var drawer = document.getElementById('drawerTargetProfile');
  if (!drawer) return;

  var host = drawer.querySelector('[data-days-host="type"]');
  if (!host) return;

  var TYPES = ['Yearly', 'Monthly', 'Daily', 'Custom Date Range'];

  host.innerHTML =
    '<input type="hidden" data-field="type" value="Yearly">' +
    '<div class="scr-content-tabs" data-target-type-tabs style="margin:0 0 4px">' +
    TYPES.map(function (t, i) {
      return '<button type="button" class="scr-content-tab' + (i === 0 ? ' is-on' : '') + '" data-type-value="' + t + '">' + t + '</button>';
    }).join('') +
    '</div>';

  var hidden = host.querySelector('[data-field="type"]');
  var tabs = host.querySelectorAll('[data-type-value]');

  tabs.forEach(function (tab) {
    tab.addEventListener('click', function () {
      tabs.forEach(function (t) { t.classList.toggle('is-on', t === tab); });
      hidden.value = tab.dataset.typeValue;
      hidden.dispatchEvent(new Event('change', { bubbles: true }));
    });
  });

  function setActiveType(type) {
    hidden.value = type;
    tabs.forEach(function (t) { t.classList.toggle('is-on', t.dataset.typeValue === type); });
    hidden.dispatchEvent(new Event('change', { bubbles: true }));
  }

  // Daily's Day select: repopulate from the days in the chosen year/month.
  var monthSelect = drawer.querySelector('[data-field="month"]');
  var yearSelect = drawer.querySelector('[data-field="year"]');
  var daySelect = drawer.querySelector('[data-field="day"]');
  var MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];

  function populateDays() {
    if (!daySelect || !monthSelect) return;
    var monthIdx = MONTHS.indexOf(monthSelect.value) + 1;
    var year = parseInt((yearSelect && yearSelect.value) || '2026', 10);
    if (!monthIdx) return;
    var daysInMonth = new Date(year, monthIdx, 0).getDate();
    var current = daySelect.value;
    daySelect.innerHTML = '<option value="">Select</option>';
    for (var d = 1; d <= daysInMonth; d++) {
      var opt = document.createElement('option');
      opt.textContent = String(d);
      if (String(d) === current) opt.selected = true;
      daySelect.appendChild(opt);
    }
  }
  if (monthSelect) monthSelect.addEventListener('change', populateDays);
  if (yearSelect) yearSelect.addEventListener('change', populateDays);

  // Re-sync the segmented toggle (and Daily's day options) whenever this
  // drawer opens -- edit mode needs the record's own type/month honoured.
  document.addEventListener('shown.bs.offcanvas', function (e) {
    if (e.target !== drawer) return;
    var type = hidden.value || 'Yearly';
    setActiveType(type);
    populateDays();
  });

  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('[data-scr-open^="target-profile:"]');
    if (!btn) return;
    var type = 'Yearly';
    if (btn.dataset.scrOpen === 'target-profile:edit') {
      var row = btn.closest('.scr-row');
      var node = row && document.getElementById(row.dataset.recordId);
      var record = node ? JSON.parse(node.textContent) : null;
      if (record && record.type) type = record.type;
    }
    setTimeout(function () { setActiveType(type); populateDays(); }, 0);
  });
})();
