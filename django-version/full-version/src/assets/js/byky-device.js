/**
 * Device Mapping -- row 50 of the client's feedback doc (RMS WEB
 * 07.09.2026-1.pdf, "Device Management" page).
 *
 * Three independent pieces, all frontend-only (CLAUDE.md 1 -- nothing here
 * persists past the page session):
 *
 * 1. Add Device Mapping's Device field (a convenience picker, not itself a
 *    stored field -- apps/byky_device/views.py's DeviceMappingView) reads
 *    the approved-devices-data json_script blob and auto-fills the
 *    read-only Device ID / Name / MAC / APK Version fields below it.
 * 2. Station selection warns if that branch's own "Allow Multiple Devices"
 *    flag (Branch Management's multi_user, reused rather than inventing a
 *    new one) is off and it already has a mapped device, via the
 *    branch-flags-data blob. Every branch in today's demo data has
 *    multi_user=true (apps/byky_cms/data.py), so this warning is dormant
 *    against current data -- it fires correctly the day a branch's flag is
 *    turned off.
 * 3. Each mapped device's Logout/Block/Unblock kebab actions are plain
 *    instant buttons -- no confirm dialog, no remark prompt (frontend-only
 *    actions like these stay a direct click, not a modal popup). Block and
 *    Unblock are dynamic: a row starts showing only the action matching
 *    its current state, and clicking one swaps to the other live. These
 *    act on the already-mapped fleet, a distinct concept from Device
 *    Approval's own Block/Unblock on its onboarding queue.
 */

'use strict';

(function () {
  var devicePick = document.querySelector('#offcanvasAddDevice [data-field="device_pick"]');
  var approvedDataEl = document.getElementById('approved-devices-data');
  if (devicePick && approvedDataEl) {
    var byLabel = {};
    JSON.parse(approvedDataEl.textContent).forEach(function (d) {
      byLabel[d.name + ' — ' + d.mac] = d;
    });
    var drawer = devicePick.closest('.byky-drawer');
    devicePick.addEventListener('change', function () {
      var picked = byLabel[devicePick.value];
      if (!picked || !drawer) return;
      function fill(field, val) {
        var el = drawer.querySelector('[data-field="' + field + '"]');
        if (el) el.value = val || '';
      }
      fill('device_id', picked.device_id);
      fill('name', picked.name);
      fill('mac', picked.mac);
      fill('apk_version', picked.apk_version);
    });
  }

  var branchSelect = document.querySelector('#offcanvasAddDevice [data-field="station"]');
  var branchDataEl = document.getElementById('branch-flags-data');
  if (branchSelect && branchDataEl) {
    var branchFlags = {};
    JSON.parse(branchDataEl.textContent).forEach(function (b) {
      branchFlags[b.name] = b;
    });
    var field = branchSelect.closest('.byky-field');
    var warning = document.createElement('div');
    warning.className = 'byky-help byky-help-danger';
    warning.hidden = true;
    warning.textContent = 'This branch does not allow more than one device. Enable "Allow Multiple Devices" on Branch Management first.';
    if (field) field.appendChild(warning);
    branchSelect.addEventListener('change', function () {
      var b = branchFlags[branchSelect.value];
      warning.hidden = !(b && b.mapped && !b.multi_user);
    });
  }

  function setStatus(row, label, cls) {
    var badge = row.querySelector('[data-status-badge]');
    if (badge) {
      badge.className = 'scr-badge ' + cls;
      badge.innerHTML = '<i></i>' + label;
    }
  }

  function wireInstantAction(attr, apply) {
    document.querySelectorAll('[' + attr + ']').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var row = btn.closest('.scr-row');
        if (!row) return;
        apply(row);
      });
    });
  }

  wireInstantAction('[data-device-logout]', function (row) {
    setStatus(row, 'Offline', 'scr-badge-rejected');
  });
  wireInstantAction('[data-device-block]', function (row) {
    setStatus(row, 'Blocked', 'scr-badge-pending');
    var blockBtn = row.querySelector('[data-device-block]');
    var unblockBtn = row.querySelector('[data-device-unblock]');
    if (blockBtn) blockBtn.hidden = true;
    if (unblockBtn) unblockBtn.hidden = false;
  });
  wireInstantAction('[data-device-unblock]', function (row) {
    setStatus(row, 'Online', 'scr-badge-approved');
    var blockBtn = row.querySelector('[data-device-block]');
    var unblockBtn = row.querySelector('[data-device-unblock]');
    if (blockBtn) blockBtn.hidden = false;
    if (unblockBtn) unblockBtn.hidden = true;
  });
})();
