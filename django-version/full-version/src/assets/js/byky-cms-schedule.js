/**
 * BYKY CMS -- Station Working Time (FSD 1.8)
 *
 * Attaches an HH:mm time picker to every shift input in the 7 x 4 weekly matrix.
 * Wireframe phase: nothing is saved.
 */

'use strict';

(function () {
  const inputs = document.querySelectorAll('.shift-time');
  if (!inputs.length || typeof flatpickr === 'undefined') return;

  inputs.forEach(el =>
    flatpickr(el, {
      enableTime: true,
      noCalendar: true,
      dateFormat: 'H:i',
      time_24hr: true
    })
  );
})();
