/**
 * Device Mapping -- row 50 of the client's feedback doc (RMS WEB
 * 07.09.2026-1.pdf, "Device Management" page).
 *
 * Three independent pieces, all frontend-only (CLAUDE.md 1 -- nothing here
 * persists past the page session):
 *
 * 1. Add Device Mapping's Device dropdown (approved-but-unmapped devices
 *    only) auto-fills the read-only Device ID / Name / MAC / APK Version
 *    fields below it from the option's own data attributes.
 * 2. Station selection warns if that branch's own "Allow Multiple Devices"
 *    flag (Branch Management's multi_user, reused rather than inventing a
 *    new one) is off and it already has a mapped device. Every branch in
 *    today's demo data has multi_user=true (apps/byky_cms/data.py), so
 *    this warning is dormant against current data -- it fires correctly
 *    the day a branch's flag is turned off.
 * 3. Each mapped device's Logout/Block/Unblock kebab actions require a
 *    remark before they apply (SweetAlert2 with a textarea input), unlike
 *    byky-screen.js's generic data-scr-block/unblock which confirms with a
 *    plain yes/no -- these act on the already-mapped fleet, a distinct
 *    concept from Device Approval's own Block/Unblock on its onboarding
 *    queue.
 */

'use strict';

(function () {
  var devicePick = document.getElementById('device-mapping-pick');
  if (devicePick) {
    var drawer = devicePick.closest('.scr-drawer');
    devicePick.addEventListener('change', function () {
      var opt = devicePick.options[devicePick.selectedIndex];
      function fill(field, val) {
        var el = drawer.querySelector('[data-field="' + field + '"]');
        if (el) el.value = val || '';
      }
      fill('device_id', opt.dataset.deviceId);
      fill('name', opt.dataset.name);
      fill('mac', opt.dataset.mac);
      fill('apk_version', opt.dataset.apk);
    });
  }

  var branchSelect = document.querySelector('[data-scr-drawer="device"] [data-field="station"]');
  if (branchSelect) {
    var warning = branchSelect.closest('.scr-drawer-field').querySelector('[data-branch-multi-warning]');
    branchSelect.addEventListener('change', function () {
      var opt = branchSelect.options[branchSelect.selectedIndex];
      var allowsMultiple = opt.dataset.multiUser !== 'false';
      var alreadyMapped = opt.dataset.mapped === 'true';
      if (warning) warning.hidden = !(alreadyMapped && !allowsMultiple);
    });
  }

  function rowLabel(row) {
    var code = row.querySelector('.scr-code');
    return code ? code.textContent.trim() : 'this device';
  }

  function setStatus(row, label, cls) {
    var badge = row.querySelector('[data-status-badge]');
    if (badge) {
      badge.className = 'scr-badge ' + cls;
      badge.innerHTML = '<i></i>' + label;
    }
  }

  function wireRemarkAction(attr, verb, doneVerb, apply) {
    document.querySelectorAll('[' + attr + ']').forEach(function (btn) {
      btn.addEventListener('click', function (e) {
        e.preventDefault();
        var row = btn.closest('.scr-row');
        if (!row) return;
        var name = rowLabel(row);

        if (typeof Swal === 'undefined') {
          var remark = window.prompt(verb + ' ' + name + ' -- remark (required):');
          if (remark && remark.trim()) apply(row);
          return;
        }
        Swal.fire({
          title: verb + ' ' + name + '?',
          input: 'textarea',
          inputLabel: 'Remark',
          inputPlaceholder: 'Reason for this action',
          inputValidator: function (value) {
            if (!value || !value.trim()) return 'A remark is required.';
          },
          showCancelButton: true,
          confirmButtonText: 'Confirm ' + verb,
          customClass: { confirmButton: 'btn btn-primary me-3', cancelButton: 'btn btn-label-secondary' },
          buttonsStyling: false
        }).then(function (result) {
          if (!result.isConfirmed) return;
          apply(row);
          Swal.fire({
            text: name + ' has been ' + doneVerb + '.',
            icon: 'success',
            customClass: { confirmButton: 'btn btn-primary' },
            buttonsStyling: false
          });
        });
      });
    });
  }

  wireRemarkAction('[data-device-logout]', 'Logout', 'logged out', function (row) {
    setStatus(row, 'Offline', 'scr-badge-rejected');
  });
  wireRemarkAction('[data-device-block]', 'Block', 'blocked', function (row) {
    setStatus(row, 'Blocked', 'scr-badge-pending');
  });
  wireRemarkAction('[data-device-unblock]', 'Unblock', 'unblocked', function (row) {
    setStatus(row, 'Online', 'scr-badge-approved');
  });
})();
