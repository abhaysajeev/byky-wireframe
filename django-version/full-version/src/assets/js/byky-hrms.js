/**
 * BYKY HRMS
 *
 * Date pickers for the employee document and personal date fields, and the
 * FSD 2.5 accent switch between Block and Unblock.
 */

'use strict';

(function () {
  if (typeof flatpickr !== 'undefined') {
    document.querySelectorAll('.byky-date').forEach(el =>
      flatpickr(el, { dateFormat: 'd M Y', allowInput: true })
    );
  }

  // FSD 2.5 section 17: Block shows a danger accent, Unblock a success accent.
  const actionType = document.getElementById('block-action-type');
  const panel = document.getElementById('block-action-panel');
  if (actionType && panel) {
    const apply = () => {
      const blocking = actionType.value === 'BLOCK';
      panel.classList.toggle('border-danger', blocking);
      panel.classList.toggle('border-success', !blocking);
      const btn = document.getElementById('block-confirm');
      if (btn) {
        btn.classList.toggle('btn-danger', blocking);
        btn.classList.toggle('btn-success', !blocking);
        btn.textContent = blocking ? 'Confirm Block' : 'Confirm Unblock';
      }
    };
    actionType.addEventListener('change', apply);
    apply();
  }
})();
