/**
 * Live Monitor -- RMS WEB APK UI.xlsx feedback on live/live-monitor/. Only
 * new behaviour this page needs beyond byky-screen.js's generic tab/filter
 * wiring: flatpickr on the From/To Date filter pair, matching the
 * dateFormat every other .byky-date field in the app already uses
 * (byky-hrms.js, byky-ims-transfer.js). Both fields are pre-filled
 * server-side with today's date (views.py's today_display) -- this only
 * turns them into real pickers.
 */

'use strict';

(function () {
  document.querySelectorAll('.byky-date').forEach(function (el) {
    flatpickr(el, { dateFormat: 'd M Y', allowInput: true });
  });
})();
