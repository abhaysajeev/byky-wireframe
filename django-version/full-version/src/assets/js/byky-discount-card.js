/**
 * Card Discount (Discount Card Management) -- page-specific behaviour that
 * doesn't belong in the shared byky-screen.js because it's only needed here:
 * day-wise discount checkboxes each unlocking their own % input, "All Days"
 * covering the other seven, and the Usage Type radios unlocking only the
 * one count input that belongs to the selected option.
 *
 * Card Type -> Card Grade is the shared cascading-dropdown mechanism
 * (data-scr-cascades) already in byky-screen.js -- nothing to wire here.
 */

'use strict';

(function () {
  var table = document.getElementById('cd-day-table');
  if (!table) return;

  var allCheck = document.getElementById('cd-day-all');
  var allInput = document.getElementById('cd-discount-all');
  var dayChecks = table.querySelectorAll('.cd-day-check');

  function dayInputFor(check) {
    return check.closest('.scr-day-row').querySelector('.cd-day-discount');
  }

  dayChecks.forEach(function (check) {
    check.addEventListener('change', function () {
      var input = dayInputFor(check);
      input.disabled = !check.checked;
      if (!check.checked) input.value = '';
    });
  });

  if (allCheck && allInput) {
    allCheck.addEventListener('change', function () {
      allInput.disabled = !allCheck.checked;
      if (!allCheck.checked) allInput.value = '';

      // "All Days" supersedes picking individual days -- lock them together
      // rather than leaving two contradictory ways to express the same rule.
      dayChecks.forEach(function (check) {
        check.checked = allCheck.checked;
        check.disabled = allCheck.checked;
        var input = dayInputFor(check);
        input.disabled = true;
        if (allCheck.checked) input.value = '';
      });
    });
  }

  var usageRadios = document.querySelectorAll('.cd-usage-radio');
  function syncUsage() {
    usageRadios.forEach(function (radio) {
      var countInput = radio.closest('.scr-radio-row').querySelector('.cd-usage-count');
      if (!countInput) return;
      var active = radio.checked && radio.dataset.needsCount === '1';
      countInput.disabled = !active;
      if (!active) countInput.value = '';
    });
  }
  usageRadios.forEach(function (radio) { radio.addEventListener('change', syncUsage); });
  syncUsage();
})();
