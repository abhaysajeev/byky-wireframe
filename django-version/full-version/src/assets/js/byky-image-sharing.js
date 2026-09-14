/**
 * Image Sharing -- RMS WEB APK UI.xlsx feedback on live/image-sharing/.
 * byky-screen.js already handles the search box, the new Branch filter
 * dropdown and pagination via the standard .scr-row/data-search/
 * data-branch markup; this file owns everything the feedback doc added
 * that's specific to this screen:
 *
 * 1. flatpickr on the new From/To Date fields (decorative, like Live
 *    Monitor's own date pair -- neither screen wires a working date-range
 *    filter in this wireframe phase).
 * 2. Select-All + per-row checkboxes drive a bulk action bar (0 selected
 *    is hidden) with one "Delete from Database" button, alongside each
 *    row's own kebab item doing the same for just that row. Both remove
 *    rows from the DOM and nudge byky-screen.js to re-filter, the same
 *    pattern byky-ims-map-to-branch.js already uses for its own
 *    select-and-act flow.
 * 3. The Station Count KPI -- distinct branches among the *checked* rows,
 *    not the whole list -- recomputes on every checkbox change.
 */

'use strict';

(function () {
  var card = document.querySelector('[data-scr-noun-singular="image"]');
  if (!card) return;

  var selectAll = document.getElementById('image-select-all');
  var bulkBar = document.getElementById('image-bulk-bar');
  var bulkCount = document.getElementById('image-bulk-count');
  var bulkDeleteBtn = document.getElementById('image-bulk-delete');
  var stationCountEl = document.querySelector('[data-image-station-count]');
  var totalCountEl = document.querySelector('[data-image-total-count]');

  document.querySelectorAll('.byky-date').forEach(function (el) {
    flatpickr(el, { dateFormat: 'd M Y', allowInput: true });
  });

  function checkboxes() {
    return card.querySelectorAll('input[data-image-check]');
  }

  function checkedBoxes() {
    return card.querySelectorAll('input[data-image-check]:checked');
  }

  function refreshSelectionState() {
    var checked = checkedBoxes();
    var count = checked.length;

    if (bulkBar) bulkBar.hidden = count === 0;
    if (bulkCount) bulkCount.textContent = count + ' selected';

    var branches = {};
    checked.forEach(function (cb) { branches[cb.dataset.branch] = true; });
    if (stationCountEl) stationCountEl.textContent = Object.keys(branches).length;

    if (selectAll) {
      var all = checkboxes();
      selectAll.checked = all.length > 0 && count === all.length;
      selectAll.indeterminate = count > 0 && count < all.length;
    }
  }

  function removeRows(rows) {
    rows.forEach(function (row) { row.remove(); });

    var remaining = card.querySelectorAll('.scr-row').length;
    if (totalCountEl) totalCountEl.textContent = remaining;

    /* Re-run byky-screen.js's own filter/pager/count logic instead of
       hand-updating it here -- it already knows how to recompute the
       toolbar count and pager against whatever search/branch filter is
       active, the same trick byky-ims-map-to-branch.js relies on. */
    var searchInput = card.querySelector('.scr-search input');
    if (searchInput) searchInput.dispatchEvent(new Event('input', { bubbles: true }));

    refreshSelectionState();
  }

  if (selectAll) {
    selectAll.addEventListener('change', function () {
      checkboxes().forEach(function (cb) { cb.checked = selectAll.checked; });
      refreshSelectionState();
    });
  }

  card.addEventListener('change', function (e) {
    if (e.target.matches('input[data-image-check]')) refreshSelectionState();
  });

  if (bulkDeleteBtn) {
    bulkDeleteBtn.addEventListener('click', function () {
      var rows = Array.prototype.map.call(checkedBoxes(), function (cb) {
        return cb.closest('.scr-row');
      }).filter(Boolean);
      if (rows.length) removeRows(rows);
    });
  }

  card.addEventListener('click', function (e) {
    var btn = e.target.closest('[data-image-row-delete]');
    if (!btn) return;
    var row = btn.closest('.scr-row');
    if (row) removeRows([row]);
  });

  refreshSelectionState();
})();
