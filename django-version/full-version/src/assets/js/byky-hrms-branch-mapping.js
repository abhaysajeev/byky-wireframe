/**
 * Incentive Branch Mapping / Target Branch Mapping -- RMS WEB APK UI.xlsx
 * feedback (byky Docs/new html/incentive-branch-mapping.html and
 * target-branch-mapping.html, structurally identical). Shared by both
 * drawers (#drawerIncentiveBranchMapping, #drawerTargetBranchMapping).
 *
 * Only behaviour these drawers need beyond what byky-drawer.js/byky-screen.js
 * already handle generically (the multiselect itself, the "All Branches"
 * checkbox hiding it via data-show-if, the combo plan/profile search): the
 * Emirate select narrows the Branches multiselect to that emirate's real
 * branches, reading a {name: emirate} map from a page-level json_script
 * (data-branch-emirate-map, set once per page).
 */

'use strict';

(function () {
  var mapEl = document.getElementById('branch-emirate-map');
  if (!mapEl) return;
  var branchEmirate = {};
  try { branchEmirate = JSON.parse(mapEl.textContent); } catch (err) { branchEmirate = {}; }

  ['drawerIncentiveBranchMapping', 'drawerTargetBranchMapping'].forEach(function (id) {
    var drawer = document.getElementById(id);
    if (!drawer) return;

    var emirateSelect = drawer.querySelector('[data-field="emirate"]');
    var multi = drawer.querySelector('.byky-multi[data-field="branches"]');
    if (!emirateSelect || !multi) return;

    function applyFilter() {
      var emirate = emirateSelect.value;
      multi.querySelectorAll('.byky-multi-opt').forEach(function (opt) {
        var checkbox = opt.querySelector('input[type="checkbox"]');
        var name = checkbox ? checkbox.value : '';
        var show = !emirate || branchEmirate[name] === emirate;
        opt.hidden = !show;
        if (!show) checkbox.checked = false;
      });
      if (multi.__bykyRenderPills) multi.__bykyRenderPills();
    }

    emirateSelect.addEventListener('change', applyFilter);
    // Re-apply on every drawer open (add starts blank, edit needs the
    // record's own emirate honoured before its branch checkboxes are read).
    document.addEventListener('shown.bs.offcanvas', function (e) {
      if (e.target === drawer) applyFilter();
    });
    applyFilter();
  });
})();
