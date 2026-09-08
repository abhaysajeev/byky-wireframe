'use strict';

(() => {
  // .byky-datetime is scoped to this page only -- no other .scr-* screen has
  // needed a date+time picker yet, so it isn't in the shared byky-screen.js
  // flatpickr init (which only handles .byky-date, date-only, via byky-hrms.js).
  if (typeof flatpickr !== 'undefined') {
    document.querySelectorAll('.byky-datetime').forEach(el =>
      flatpickr(el, { dateFormat: 'd M Y, H:i', enableTime: true, time_24hr: true, allowInput: true })
    );
  }
})();
