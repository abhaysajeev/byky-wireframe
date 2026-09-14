/**
 * Incentive -- RMS WEB APK UI.xlsx feedback (byky Docs/new html/incentive.html).
 *
 * The drawer's User Type(s) multiselect (kind "multiselect", already generic)
 * drives a breakdown table this file renders into the drawer's "custom"
 * field slot (data-days-host="breakdown") -- one row per selected type, a
 * % of Collection number input plus a Dividend rule select, with a running
 * allocation-total badge. Two designations get bespoke behaviour ported
 * straight from the mockup:
 *
 * - "Cashier with RMS Login" always gets the full amount, alone -- its
 *   dividend cell is fixed text, not a select.
 * - "Cashier without RMS Login" can fold into Labour's equal split (its own
 *   % input then locks at 0) or stand on its own, counted like any other
 *   split-eligible type.
 *
 * See apps/byky_hrms/data.py's module note for why the type list itself is
 * real designations rather than the mockup's invented job titles.
 */

'use strict';

(function () {
  var drawer = document.getElementById('drawerIncentivePlan');
  if (!drawer) return;

  var CASHIER_RMS = 'Cashier with RMS Login';
  var CASHIER_NO_RMS = 'Cashier without RMS Login';

  var host = drawer.querySelector('[data-days-host="breakdown"]');
  var multi = drawer.querySelector('.byky-multi[data-field="user_types"]');
  if (!host || !multi) return;

  var rows = {}; // { type: { pct, dividend } }

  function defaultDividendFor(type) {
    if (type === CASHIER_RMS) return 'single';
    if (type === CASHIER_NO_RMS) return 'as_labour';
    return 'split';
  }

  function selectedTypes() {
    return Array.prototype.map.call(
      multi.querySelectorAll('input[type="checkbox"]:checked'),
      function (b) { return b.value; }
    );
  }

  function updateAllocBadge() {
    var total = Object.keys(rows).reduce(function (sum, t) { return sum + (parseFloat(rows[t].pct) || 0); }, 0);
    var el = host.querySelector('[data-alloc-total]');
    if (!el) return;
    el.textContent = 'Total % of collection: ' + (Math.round(total * 10) / 10) + '%';
    el.className = 'scr-alloc-badge' + (total > 100 ? ' is-warn' : '');
  }

  function render() {
    var types = selectedTypes();
    // Fixed display order: pinned types first (in their own order), then
    // every other selected type in the order the multiselect lists them.
    var pinned = [CASHIER_RMS, CASHIER_NO_RMS, 'Labour'].filter(function (t) { return types.indexOf(t) > -1; });
    var rest = types.filter(function (t) { return pinned.indexOf(t) === -1; });
    var ordered = pinned.concat(rest);

    types.forEach(function (t) { if (!rows[t]) rows[t] = { pct: 0, dividend: defaultDividendFor(t) }; });
    Object.keys(rows).forEach(function (t) { if (types.indexOf(t) === -1) delete rows[t]; });

    if (!ordered.length) {
      host.innerHTML = '<div class="scr-help">Select one or more user types above to configure their target % and dividend rule.</div>';
      return;
    }

    var html = '<table class="scr-records-table" style="width:100%"><thead><tr>' +
      '<th>User Type</th><th>% of Collection</th><th>Dividend</th></tr></thead><tbody>';

    ordered.forEach(function (t) {
      var row = rows[t];
      html += '<tr data-breakdown-row="' + t.replace(/"/g, '&quot;') + '"><td>' + t + '</td>';

      if (t === CASHIER_RMS) {
        html += '<td>' + row.pct + '%</td><td>Full amount — single person (the one logged into RMS)</td>';
      } else if (t === CASHIER_NO_RMS) {
        var folded = row.dividend === 'as_labour';
        html += '<td><input type="number" min="0" max="100" step="any" class="byky-input" data-breakdown-pct' + (folded ? ' disabled' : '') + ' value="' + (folded ? 0 : row.pct) + '" style="width:80px"></td>';
        html += '<td><select class="byky-input byky-select" data-breakdown-dividend>' +
          '<option value="as_labour"' + (row.dividend === 'as_labour' ? ' selected' : '') + '>Counted as Labour — joins the equal-split headcount</option>' +
          '<option value="as_cashier"' + (row.dividend === 'as_cashier' ? ' selected' : '') + '>Counted as Cashier — own % split equally among them</option>' +
          '</select></td>';
      } else {
        html += '<td><input type="number" min="0" max="100" step="any" class="byky-input" data-breakdown-pct value="' + row.pct + '" style="width:80px"></td>';
        html += '<td><select class="byky-input byky-select" data-breakdown-dividend>' +
          '<option value="single"' + (row.dividend === 'single' ? ' selected' : '') + '>Full amount — single person</option>' +
          '<option value="split"' + (row.dividend === 'split' ? ' selected' : '') + '>Split equally — on-duty headcount</option>' +
          '</select></td>';
      }
      html += '</tr>';
    });

    html += '</tbody></table><div style="margin-top:10px; text-align:right"><span class="scr-alloc-badge" data-alloc-total>Total % of collection: 0%</span></div>';
    host.innerHTML = html;
    updateAllocBadge();
  }

  host.addEventListener('input', function (e) {
    var tr = e.target.closest('[data-breakdown-row]');
    if (!tr || !e.target.matches('[data-breakdown-pct]')) return;
    var type = tr.dataset.breakdownRow;
    if (rows[type]) rows[type].pct = parseFloat(e.target.value) || 0;
    updateAllocBadge();
  });

  host.addEventListener('change', function (e) {
    var tr = e.target.closest('[data-breakdown-row]');
    if (!tr || !e.target.matches('[data-breakdown-dividend]')) return;
    var type = tr.dataset.breakdownRow;
    if (!rows[type]) return;
    rows[type].dividend = e.target.value;
    if (type === CASHIER_NO_RMS && e.target.value === 'as_labour') rows[type].pct = 0;
    render();
  });

  multi.addEventListener('change', function (e) {
    if (e.target.matches('input[type="checkbox"]')) render();
  });

  // Edit-mode prefill: byky-drawer.js's fill() already checked the right
  // multiselect boxes from record.user_types by the time this fires (both
  // listen on the same drawer 'change'/open cycle) -- read the record's own
  // breakdown_data to seed `rows` with real pct/dividend instead of the
  // render() defaults, then draw.
  document.addEventListener('click', function (e) {
    var btn = e.target.closest && e.target.closest('[data-scr-open="incentive-plan:edit"], [data-scr-open="incentive-plan:add"]');
    if (!btn) return;
    rows = {};
    if (btn.dataset.scrOpen === 'incentive-plan:edit') {
      var row = btn.closest('.scr-row');
      var node = row && document.getElementById(row.dataset.recordId);
      var record = node ? JSON.parse(node.textContent) : null;
      if (record && record.breakdown_data) {
        Object.keys(record.breakdown_data).forEach(function (t) {
          rows[t] = { pct: record.breakdown_data[t].target_pct, dividend: record.breakdown_data[t].dividend };
        });
      }
    }
    // multiselect's own prefill runs synchronously inside byky-drawer.js's
    // click handler too; render on the next tick so its checkboxes are set.
    setTimeout(render, 0);
  });

  render();
})();
