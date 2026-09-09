/**
 * Map <thing> to Branch -- the full-page assignment flow, shared by Map
 * Vehicle (FSD 3.6) and Map Asset.
 *
 * Choose a branch, tick unmapped rows (byky-screen.js already handles the
 * search box and pagination via the standard .scr-row/data-search markup),
 * then Map. Nothing persists -- this removes the mapped rows from the current
 * page's list and shows a success banner, exactly as far as a backend-free
 * wireframe can go.
 *
 * The wording comes from the card's own data-scr-noun-singular/plural, the
 * same pair byky-screen.js reads for the toolbar count, so this file says
 * "3 assets" or "3 vehicles" without knowing which page it is on.
 */

'use strict';

(function () {
  var card = document.getElementById('map-items-card');
  var noun = (card && card.dataset.scrNounSingular) || 'item';
  var nounPlural = (card && card.dataset.scrNounPlural) || noun + 's';
  function things(n) { return n + ' ' + (n === 1 ? noun : nounPlural); }
  var branchSelect = document.getElementById('map-branch-select');
  var selectAll = document.getElementById('map-select-all');
  var mapBtn = document.getElementById('map-items-btn');
  var banner = document.getElementById('map-success-banner');
  var bannerText = document.getElementById('map-success-text');
  if (!card || !branchSelect || !mapBtn) return;

  function visibleCheckboxes() {
    return card.querySelectorAll('.scr-row:not([hidden]) input[data-map-check]');
  }

  function updateButton() {
    var checkedCount = card.querySelectorAll('input[data-map-check]:checked').length;
    var branch = branchSelect.value;
    mapBtn.disabled = !(branch && checkedCount > 0);
    mapBtn.textContent = ''; // rebuilt below with the icon kept
    var icon = 'M5 13l4 4L19 7';
    mapBtn.innerHTML =
      '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="' + icon + '"></path></svg>' +
      (checkedCount > 0
        ? 'Map ' + things(checkedCount) + (branch ? ' to ' + branch : '')
        : 'Map Selected');
  }

  branchSelect.addEventListener('change', updateButton);

  if (selectAll) {
    selectAll.addEventListener('change', function () {
      visibleCheckboxes().forEach(function (cb) { cb.checked = selectAll.checked; });
      updateButton();
    });
  }

  card.addEventListener('change', function (e) {
    if (e.target.matches('input[data-map-check]')) updateButton();
  });

  mapBtn.addEventListener('click', function () {
    var branch = branchSelect.value;
    var checked = card.querySelectorAll('.scr-row input[data-map-check]:checked');
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
          '</span><div><div class="scr-empty-title">No unmapped ' + nounPlural + '</div>' +
          '<p class="scr-empty-sub">Every ' + noun + ' now carries a branch.</p></div></div>' +
          '</td></tr>';
      }
    }
    var countEl = card.querySelector('.scr-toolbar-count');
    if (countEl) countEl.textContent = things(remaining);
    var pagerInfo = card.querySelector('.scr-pager-info');
    if (pagerInfo) pagerInfo.textContent = 'Showing ' + remaining + ' of ' + remaining;

    updateButton();

    if (banner && bannerText) {
      bannerText.textContent = things(count) + ' mapped to ' + branch + ' successfully.';
      banner.hidden = false;
      window.scrollTo({ top: 0, behavior: 'smooth' });
    }
  });

  var bannerClose = banner && banner.querySelector('.scr-banner-close');
  if (bannerClose) bannerClose.addEventListener('click', function () { banner.hidden = true; });

  updateButton();
})();
