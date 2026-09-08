/**
 * Map Vehicle to Branch (FSD 3.6) -- full-page flow.
 *
 * Choose a branch, tick unmapped vehicles (byky-screen.js already handles the
 * search box and pagination via the standard .scr-row/data-search markup),
 * then Map. Nothing persists -- this removes the mapped rows from the current
 * page's list and shows a success banner, exactly as far as a backend-free
 * wireframe can go.
 */

'use strict';

(function () {
  var card = document.getElementById('map-vehicles-card');
  var branchSelect = document.getElementById('map-branch-select');
  var selectAll = document.getElementById('map-select-all');
  var mapBtn = document.getElementById('map-vehicles-btn');
  var banner = document.getElementById('map-success-banner');
  var bannerText = document.getElementById('map-success-text');
  if (!card || !branchSelect || !mapBtn) return;

  function visibleCheckboxes() {
    return card.querySelectorAll('.scr-row:not([hidden]) input[data-veh-check]');
  }

  function updateButton() {
    var checkedCount = card.querySelectorAll('input[data-veh-check]:checked').length;
    var branch = branchSelect.value;
    mapBtn.disabled = !(branch && checkedCount > 0);
    mapBtn.textContent = ''; // rebuilt below with the icon kept
    var icon = 'M5 13l4 4L19 7';
    mapBtn.innerHTML =
      '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="' + icon + '"></path></svg>' +
      (checkedCount > 0
        ? 'Map ' + checkedCount + ' Vehicle' + (checkedCount === 1 ? '' : 's') + (branch ? ' to ' + branch : '')
        : 'Map Selected Vehicles');
  }

  branchSelect.addEventListener('change', updateButton);

  if (selectAll) {
    selectAll.addEventListener('change', function () {
      visibleCheckboxes().forEach(function (cb) { cb.checked = selectAll.checked; });
      updateButton();
    });
  }

  card.addEventListener('change', function (e) {
    if (e.target.matches('input[data-veh-check]')) updateButton();
  });

  mapBtn.addEventListener('click', function () {
    var branch = branchSelect.value;
    var checked = card.querySelectorAll('.scr-row input[data-veh-check]:checked');
    var count = checked.length;
    if (!branch || !count) return;

    checked.forEach(function (cb) {
      var row = cb.closest('.scr-row');
      if (row) row.remove();
    });
    if (selectAll) selectAll.checked = false;

    var remaining = card.querySelectorAll('.scr-row').length;
    if (!remaining) {
      var tbody = card.querySelector('tbody');
      var colspan = card.querySelectorAll('thead th').length;
      if (tbody) {
        tbody.innerHTML =
          '<tr><td colspan="' + colspan + '" style="padding:0">' +
          '<div class="scr-empty"><span class="scr-empty-ico">' +
          '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#a9a6c4" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="m9 15 5-5"></path><circle cx="12" cy="12" r="9"></circle></svg>' +
          '</span><div><div class="scr-empty-title">No unmapped vehicles</div>' +
          '<p class="scr-empty-sub">Every vehicle now carries a branch.</p></div></div>' +
          '</td></tr>';
      }
    }
    var countEl = card.querySelector('.scr-toolbar-count');
    if (countEl) countEl.textContent = remaining + (remaining === 1 ? ' vehicle' : ' vehicles');
    var pagerInfo = card.querySelector('.scr-pager-info');
    if (pagerInfo) pagerInfo.textContent = 'Showing ' + remaining + ' of ' + remaining;

    updateButton();

    if (banner && bannerText) {
      bannerText.textContent = count + ' vehicle' + (count === 1 ? '' : 's') + ' mapped to ' + branch + ' successfully.';
      banner.hidden = false;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });

  var bannerClose = banner && banner.querySelector('.scr-banner-close');
  if (bannerClose) bannerClose.addEventListener('click', function () { banner.hidden = true; });

  updateButton();
})();
