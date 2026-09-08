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
  // Border colour is set inline (no scr-* border-tint class exists for this one
  // screen-specific switch) using the same tint tokens byky-screen.css defines
  // for scr-btn-danger / scr-badge-approved, so it reads consistent even though
  // it isn't itself a shared class.
  const actionType = document.getElementById('block-action-type');
  const panel = document.getElementById('block-action-panel');
  if (actionType && panel) {
    const apply = () => {
      const blocking = actionType.value === 'BLOCK';
      panel.style.borderColor = blocking ? '#f3c3c5' : '#c4e9d5';
      const btn = document.getElementById('block-confirm');
      if (btn) {
        btn.classList.toggle('scr-btn-danger', blocking);
        btn.classList.toggle('scr-btn-success', !blocking);
        btn.textContent = blocking ? 'Confirm Block' : 'Confirm Unblock';
      }
    };
    actionType.addEventListener('change', apply);
    apply();
  }
})();
