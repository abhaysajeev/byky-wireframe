/**
 * Transfer / Return -- the full-page movement flow.
 *
 * byky-ims-map-to-branch.js already owns select-all, the button and the
 * success banner; this adds the three things a movement needs on top:
 *
 *   1. the pool is scoped to wherever the items currently are. Whichever
 *      field carries data-scr-pool-source drives the grid's branch filter --
 *      From Branch on a transfer, From Warehouse or From Event Location on a
 *      return -- so one file serves both without knowing which page it is on.
 *   2. the button waits for every *visible* required field, not just a
 *      selection. Visible matters: the destination fields swap with the type,
 *      and a hidden one must not block the form.
 *   3. the three condition photos show the chosen filename.
 *
 * Nothing persists. Same wireframe rules as every other screen here.
 */

'use strict';

(function () {
  var card = document.getElementById('map-items-card');
  var hint = document.getElementById('transfer-pool-hint');
  if (!card) return;

  var branchWrap = card.querySelector('.scr-filter-wrap[data-filter-key="branch"]');
  var sources = document.querySelectorAll('[data-scr-pool-source]');

  function applyPoolSource() {
    /* the visible source field wins; the others are hidden by the type swap */
    var value = '';
    sources.forEach(function (sel) {
      var field = sel.closest('.scr-field');
      if ((!field || !field.hidden) && sel.value) value = sel.value;
    });
    if (branchWrap) {
      var opt = branchWrap.querySelector('.scr-filter-opt[data-value="' + value + '"]');
      if (opt) opt.click();
    }
    if (hint) {
      hint.textContent = value
        ? 'Everything currently at ' + value + '.'
        : hint.dataset.emptyHint || hint.textContent;
    }
  }

  /* Every required field that is on screen must be filled. Reading it off the
     rendered asterisk keeps this in step with the form itself -- add a field
     and mark it required and the gate picks it up, with nothing to update. */
  function headerComplete() {
    var ok = true;
    document.querySelectorAll('.scr-field').forEach(function (f) {
      if (f.hidden || !f.querySelector('.scr-required')) return;
      var input = f.querySelector('[data-field]');
      if (input && !input.value) ok = false;
    });
    return ok;
  }

  window.bykyMapGate = headerComplete;

  document.addEventListener('change', function (e) {
    if (e.target.matches('[data-scr-pool-source]')) applyPoolSource();
    if (e.target.matches('[data-field]')) {
      /* the type swap can hide the field that was holding the pool source */
      applyPoolSource();
      if (window.bykyMapRefresh) window.bykyMapRefresh();
    }
  });

  document.querySelectorAll('.scr-upload input[type="file"]').forEach(function (input) {
    input.addEventListener('change', function () {
      var label = input.parentNode.querySelector('span');
      if (label && input.files && input.files[0]) label.textContent = input.files[0].name;
    });
  });

  if (typeof flatpickr !== 'undefined') {
    document.querySelectorAll('.byky-date').forEach(function (el) {
      flatpickr(el, { dateFormat: 'd M Y', allowInput: true });
    });
  }

  if (hint) hint.dataset.emptyHint = hint.textContent;
  applyPoolSource();
  if (window.bykyMapRefresh) window.bykyMapRefresh();
})();
