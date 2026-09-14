/**
 * Duty Roster -- RMS WEB APK UI.xlsx feedback (byky Docs/new html/duty-roster.html).
 *
 * Everything here reads one consolidated payload (#roster-json-data,
 * computed once by DutyRosterView) instead of re-deriving the deterministic
 * per-day status/shift hash client-side: R.employees, R.matrix (emp_no ->
 * {dateISO: {status, shift1_start, shift1_end}}), R.weeks, R.branches,
 * R.states, R.today.
 *
 * State Wise / Branch Roster / Employee View are plain tab panels
 * (byky-screen.js's [data-scr-tabgroup] already handles switching); this
 * file owns what's drawn inside each one. Branch-Day and Day Details are
 * the mockup's two read-only modals -- populated here directly via the
 * Bootstrap Modal API rather than the generic data-scr-view/data-scr-detail
 * trigger contract, since their content is computed per click, not a
 * static per-row json_script blob. Edit Day similarly opens via
 * drawer.__bykyFill() directly (its trigger is a calendar cell, not a
 * .scr-row, which the generic data-scr-open:edit delegation requires).
 */

'use strict';

(function () {
  var dataEl = document.getElementById('roster-json-data');
  if (!dataEl) return;
  var R = JSON.parse(dataEl.textContent);

  document.querySelectorAll('.byky-date:not(.byky-datetime)').forEach(function (el) {
    if (typeof flatpickr !== 'undefined') flatpickr(el, { dateFormat: 'd M Y', allowInput: true });
  });

  var empByNo = {};
  R.employees.forEach(function (e) { empByNo[e.emp_no] = e; });

  var branchEmployees = {};
  R.employees.forEach(function (e) {
    (branchEmployees[e.branch] = branchEmployees[e.branch] || []).push(e);
  });

  var currentWeek = R.weeks[R.currentWeekIndex];

  function dayLabel(iso) {
    var d = new Date(iso + 'T00:00:00');
    return d.toLocaleDateString('en-US', { weekday: 'short' }) + ' ' + d.getDate();
  }

  function statusBadgeClass(status) {
    if (status === 'Working') return 'scr-badge-approved';
    if (status === 'Sick Leave' || status === 'Casual Leave') return 'scr-badge-rejected';
    return 'scr-badge-pending';
  }

  function shiftLabel(rec) {
    if (!rec || rec.status !== 'Working' || !rec.shift1_start) return '';
    return rec.shift1_start + ' – ' + rec.shift1_end;
  }

  // ---- shared read-only modals (populated directly, not via the generic
  // data-scr-view/data-scr-detail trigger contract -- see file docstring) ----
  function openRecordsModal(title, columns, labels, rows) {
    var modalEl = document.getElementById('scr-records-modal');
    if (!modalEl || typeof bootstrap === 'undefined') return;
    document.getElementById('scr-records-modal-title').textContent = title;
    var thead = document.getElementById('scr-records-thead');
    var tbody = document.getElementById('scr-records-tbody');
    thead.innerHTML = labels.map(function (l) { return '<th>' + l + '</th>'; }).join('');
    tbody.innerHTML = rows.map(function (row) {
      return '<tr>' + columns.map(function (c) { return '<td>' + (row[c] == null ? '' : row[c]) + '</td>'; }).join('') + '</tr>';
    }).join('');
    document.getElementById('scr-records-empty').hidden = rows.length > 0;
    bootstrap.Modal.getOrCreateInstance(modalEl).show();
  }

  function openDetailModal(title, fields) {
    var modalEl = document.getElementById('scr-detail-modal');
    if (!modalEl || typeof bootstrap === 'undefined') return;
    document.getElementById('scr-detail-modal-title').textContent = title;
    var rows = document.getElementById('scr-detail-rows');
    rows.innerHTML = '';
    var shown = 0;
    fields.forEach(function (pair) {
      if (pair[1] === '' || pair[1] == null) return;
      shown++;
      var row = document.createElement('div');
      row.className = 'scr-detail-row';
      row.innerHTML = '<span class="scr-detail-label">' + pair[0] + '</span><span class="scr-detail-value">' + pair[1] + '</span>';
      rows.appendChild(row);
    });
    document.getElementById('scr-detail-empty').hidden = shown > 0;
    bootstrap.Modal.getOrCreateInstance(modalEl).show();
  }

  function openEditDay(emp, dateIso) {
    var drawer = document.getElementById('drawerDutyRosterDay');
    if (!drawer || !drawer.__bykyFill) return;
    var rec = (R.matrix[emp.emp_no] || {})[dateIso] || {};
    var record = {
      employee_label: emp.name + ' — ' + dateIso,
      day_type: rec.status || 'Working',
      branch: emp.branch,
      shift1_start: rec.shift1_start ? dateIso + ' ' + rec.shift1_start : '',
      shift1_end: rec.shift1_end ? dateIso + ' ' + rec.shift1_end : '',
    };
    drawer.__bykyFill('edit', record);
    if (window.bootstrap && bootstrap.Offcanvas) bootstrap.Offcanvas.getOrCreateInstance(drawer).show();
  }

  // ============================================================
  // State Wise tab
  // ============================================================
  function renderStateTable() {
    var theadRow = document.querySelector('#roster-state-table thead tr');
    theadRow.innerHTML = '<th>Branch</th>' + currentWeek.days.map(function (d) { return '<th>' + dayLabel(d) + '</th>'; }).join('') + '<th>Action</th>';

    var tbody = document.querySelector('#roster-state-table tbody');
    tbody.innerHTML = '';
    R.branches.forEach(function (b) {
      var emps = branchEmployees[b.name] || [];
      var tr = document.createElement('tr');
      tr.className = 'scr-row';
      tr.dataset.rosterstate = b.emirate;
      tr.dataset.search = b.name.toLowerCase();
      var cells = '<td style="font-weight:600">' + b.name + '</td>';
      currentWeek.days.forEach(function (day) {
        var c = 0, l = 0;
        emps.forEach(function (e) {
          var rec = (R.matrix[e.emp_no] || {})[day];
          if (rec && rec.status === 'Working') { if (e.role === 'Cashier') c++; else l++; }
        });
        if (c || l) {
          cells += '<td><div class="scr-duty-badges">' +
            (c ? '<button type="button" class="scr-duty-badge scr-duty-badge-c" data-branch-day="' + b.name + '|' + day + '">' + c + 'C</button>' : '') +
            (l ? '<button type="button" class="scr-duty-badge scr-duty-badge-l" data-branch-day="' + b.name + '|' + day + '">' + l + 'L</button>' : '') +
            '</div></td>';
        } else {
          cells += '<td><span class="scr-duty-badge-empty">—</span></td>';
        }
      });
      cells += '<td><button type="button" class="scr-icon-btn" title="View branch roster" data-goto-branch="' + b.name + '">' +
        '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7"></path><circle cx="12" cy="12" r="3"></circle></svg></button></td>';
      tr.innerHTML = cells;
      tbody.appendChild(tr);
    });
  }

  document.getElementById('roster-state-table').addEventListener('click', function (e) {
    var badge = e.target.closest('[data-branch-day]');
    if (badge) {
      var parts = badge.dataset.branchDay.split('|');
      var branch = parts[0], day = parts[1];
      var rows = (branchEmployees[branch] || [])
        .filter(function (e) { return ((R.matrix[e.emp_no] || {})[day] || {}).status === 'Working'; })
        .map(function (e) {
          var rec = (R.matrix[e.emp_no] || {})[day];
          return { name: e.name, role: e.role, status: rec.status, time: shiftLabel(rec) };
        });
      openRecordsModal(branch + ' — ' + dayLabel(day), ['name', 'role', 'status', 'time'], ['Employee', 'Role', 'Status', 'Time'], rows);
      return;
    }
    var gotoBtn = e.target.closest('[data-goto-branch]');
    if (gotoBtn) {
      var branchName = gotoBtn.dataset.gotoBranch;
      var branchTab = document.querySelector('.scr-content-tab[data-tab="branch"]');
      if (branchTab) branchTab.click();
      var select = document.getElementById('roster-branch-select');
      if (select) { select.value = branchName; select.dispatchEvent(new Event('change')); }
    }
  });

  // ============================================================
  // Branch Roster tab (+ Add Weekly Branch Roster drawer, same renderer)
  // ============================================================
  function renderWeekGrid(host, branchName, week) {
    if (!host) return;
    var emps = branchEmployees[branchName] || [];
    host.innerHTML = '';
    week.days.forEach(function (day) {
      var working = emps.filter(function (e) { return ((R.matrix[e.emp_no] || {})[day] || {}).status === 'Working'; });
      var cashiers = working.filter(function (e) { return e.role === 'Cashier'; });
      var labour = working.filter(function (e) { return e.role !== 'Cashier'; });

      var card = document.createElement('div');
      card.className = 'scr-wk-day-card';
      card.dataset.day = day;
      var d = new Date(day + 'T00:00:00');
      var html = '<div class="scr-wk-day-head">' + d.toLocaleDateString('en-US', { weekday: 'long' }) + '</div>' +
        '<div class="scr-wk-day-date">' + d.toLocaleDateString('en-US', { day: 'numeric', month: 'short' }) + '</div>';

      function chip(e) {
        var rec = (R.matrix[e.emp_no] || {})[day];
        return '<div class="scr-wk-chip" data-emp="' + e.emp_no + '">' +
          '<span class="scr-wk-chip-name">' + e.name + '</span>' +
          '<span class="scr-wk-chip-time">' + shiftLabel(rec) + '</span>' +
          '<button type="button" class="scr-wk-chip-x" title="Remove" data-wk-remove>' +
          '<svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M6 6l12 12M18 6 6 18"></path></svg></button></div>';
      }

      html += cashiers.map(chip).join('') || '<div class="scr-help" style="font-size:10.5px">No cashier assigned</div>';
      html += '<button type="button" class="scr-wk-add" data-scr-open="duty-roster-add-to-day:add">+ Cashier</button>';
      html += labour.map(chip).join('');
      html += '<button type="button" class="scr-wk-add" data-scr-open="duty-roster-add-to-day:add">+ Labour</button>';

      card.innerHTML = html;
      host.appendChild(card);
    });
  }

  var branchGrid = document.getElementById('roster-branch-grid');
  var branchSelect = document.getElementById('roster-branch-select');
  if (branchGrid && branchSelect) {
    branchSelect.addEventListener('change', function () {
      renderWeekGrid(branchGrid, branchSelect.value, currentWeek);
    });
    renderWeekGrid(branchGrid, branchSelect.value, currentWeek);

    branchGrid.addEventListener('click', function (e) {
      if (e.target.closest('[data-wk-remove]')) {
        var chip = e.target.closest('.scr-wk-chip');
        if (chip) chip.remove();
      }
    });
  }

  // ============================================================
  // Employee View tab
  // ============================================================
  var empSelectHidden = document.getElementById('roster-employee-selected');
  var empProfile = document.getElementById('roster-employee-profile');
  var empCalendar = document.getElementById('roster-employee-calendar');

  function renderEmployeeCalendar(empNo) {
    var emp = empByNo[empNo];
    if (!emp || !empCalendar) return;
    var monthMatrix = R.matrix[empNo] || {};
    var allDays = [];
    R.weeks.forEach(function (w) { allDays = allDays.concat(w.days); });

    var counts = { Working: 0, 'Week Off': 0, 'Sick Leave': 0, 'Casual Leave': 0 };
    allDays.forEach(function (d) { var st = (monthMatrix[d] || {}).status; if (st) counts[st] = (counts[st] || 0) + 1; });

    if (empProfile) {
      empProfile.innerHTML = '<b style="color:#1a1640">' + emp.name + '</b> (' + emp.emp_no + ') · ' + emp.designation + ' · ' + emp.branch + ', ' + emp.emirate +
        ' &nbsp;·&nbsp; Working days: ' + counts.Working + ' · Week-offs: ' + counts['Week Off'] + ' · Sick leave: ' + counts['Sick Leave'] + ' · Casual leave: ' + counts['Casual Leave'];
    }

    empCalendar.innerHTML = '';
    var dowLabels = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    dowLabels.forEach(function (l) {
      var el = document.createElement('div');
      el.className = 'scr-cal-dow';
      el.textContent = l;
      empCalendar.appendChild(el);
    });
    var firstDow = new Date(allDays[0] + 'T00:00:00').getDay();
    for (var i = 0; i < firstDow; i++) empCalendar.appendChild(document.createElement('div'));

    allDays.forEach(function (day) {
      var rec = monthMatrix[day] || {};
      var d = new Date(day + 'T00:00:00');
      var cell = document.createElement('div');
      cell.className = 'scr-cal-cell' + (day === R.today ? ' is-today' : '');
      cell.innerHTML = '<span class="scr-cal-date">' + d.getDate() + '</span>' +
        '<span class="scr-badge ' + statusBadgeClass(rec.status) + '"><i></i>' + (rec.status || '') + '</span>' +
        (rec.status === 'Working' ? '<span class="scr-cal-shift">' + shiftLabel(rec) + '</span><span class="scr-cal-branch">' + emp.branch + '</span>' : '') +
        '<button type="button" class="scr-cal-edit" title="Edit day" data-cal-edit="' + day + '">' +
        '<svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 20h4l10-10a2.1 2.1 0 0 0-3-3L5 17z"></path></svg></button>';
      cell.addEventListener('click', function (e) {
        if (e.target.closest('[data-cal-edit]')) return;
        openDetailModal(emp.name + ' — ' + day, [
          ['Employee', emp.name + ' (' + emp.emp_no + ')'],
          ['Date & Day', d.toLocaleDateString('en-US', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })],
          ['Status', rec.status || ''],
          ['Branch', rec.status === 'Working' ? emp.branch : ''],
          ['Shift 1', shiftLabel(rec)],
        ]);
      });
      cell.querySelector('[data-cal-edit]').addEventListener('click', function (ev) {
        ev.stopPropagation();
        openEditDay(emp, day);
      });
      empCalendar.appendChild(cell);
    });
  }

  document.addEventListener('change', function (e) {
    if (e.target === empSelectHidden && empSelectHidden.value) renderEmployeeCalendar(empSelectHidden.value);
  });
  // employee_key resolves to the employee's *name* (combo's combo_key), so
  // resolve the emp_no back out for the calendar/matrix lookups.
  document.addEventListener('change', function (e) {
    if (e.target === empSelectHidden) {
      var byName = R.employees.filter(function (x) { return x.name === empSelectHidden.value; })[0];
      if (byName) renderEmployeeCalendar(byName.emp_no);
    }
  });
  if (R.employees.length) renderEmployeeCalendar(R.employees[0].emp_no);

  // ============================================================
  // State Wise / renders once on load; header menu jump to Bulk Import
  // ============================================================
  renderStateTable();
  var gotoImport = document.querySelector('[data-roster-goto-import]');
  if (gotoImport) {
    gotoImport.addEventListener('click', function () {
      var el = document.getElementById('roster-bulk-import');
      if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
  }

  // ============================================================
  // Add Employee Roster drawer -- day-by-day builder in its "custom" slot
  // ============================================================
  (function () {
    var drawer = document.getElementById('drawerDutyRosterEmployee');
    if (!drawer) return;
    var host = drawer.querySelector('[data-days-host="days"]');
    var employeeHidden = drawer.querySelector('[data-field="employee_key"]');
    var weekSelect = drawer.querySelector('[data-field="week"]');
    if (!host || !employeeHidden || !weekSelect) return;

    function renderDays() {
      var empName = employeeHidden.value;
      var emp = R.employees.filter(function (x) { return x.name === empName; })[0];
      var week = R.weeks[weekSelect.selectedIndex - 1]; // option 0 is the blank "Select"
      if (!emp || !week) {
        host.innerHTML = '<div class="scr-help">Choose a state, category, employee and week above, then set each day below.</div>';
        return;
      }
      var monthMatrix = R.matrix[emp.emp_no] || {};
      host.innerHTML = week.days.map(function (day) {
        var rec = monthMatrix[day] || {};
        var d = new Date(day + 'T00:00:00');
        return '<div class="scr-wk-day-card" style="min-width:0; margin-bottom:8px">' +
          '<div class="scr-wk-day-head">' + d.toLocaleDateString('en-US', { weekday: 'long', day: 'numeric', month: 'short' }) + '</div>' +
          '<select class="byky-input byky-select" data-day-type="' + day + '" style="margin-bottom:6px">' +
          ['Working', 'Week Off', 'Sick Leave', 'Casual Leave'].map(function (t) { return '<option' + (t === rec.status ? ' selected' : '') + '>' + t + '</option>'; }).join('') +
          '</select>' +
          (rec.status === 'Working' ? '<div class="scr-wk-chip-time">' + shiftLabel(rec) + ' at ' + emp.branch + '</div>' : '') +
          '</div>';
      }).join('');
    }

    employeeHidden.addEventListener('change', renderDays);
    weekSelect.addEventListener('change', renderDays);
    renderDays();
  })();

  // ============================================================
  // Add Weekly Branch Roster drawer -- reuses renderWeekGrid
  // ============================================================
  (function () {
    var drawer = document.getElementById('drawerDutyRosterWeekly');
    if (!drawer) return;
    var host = drawer.querySelector('[data-days-host="columns"]');
    var branchField = drawer.querySelector('[data-field="branch"]');
    var weekField = drawer.querySelector('[data-field="week"]');
    if (!host || !branchField || !weekField) return;

    function render() {
      var week = R.weeks[weekField.selectedIndex - 1];
      if (!branchField.value || !week) {
        host.innerHTML = '<div class="scr-help">Choose a state, branch and week above.</div>';
        return;
      }
      renderWeekGrid(host, branchField.value, week);
    }
    branchField.addEventListener('change', render);
    weekField.addEventListener('change', render);
    render();
  })();

  // ============================================================
  // Bulk Import (Excel) -- real read/write via the vendored SheetJS
  // ============================================================
  (function () {
    if (typeof XLSX === 'undefined') return;
    var columnsEl = document.getElementById('roster-import-columns-data');
    var COLUMNS = columnsEl ? JSON.parse(columnsEl.textContent) : [];

    function sampleRows() {
      var sample = R.employees.slice(0, 3);
      var today = R.today;
      return sample.map(function (e) {
        var rec = (R.matrix[e.emp_no] || {})[today] || {};
        return [e.emp_no, e.name, today, rec.status || 'Working', e.branch, rec.shift1_start || '09:00', rec.shift1_end || '18:00', '', '', ''];
      });
    }

    function downloadSheet(rows, filename) {
      var ws = XLSX.utils.aoa_to_sheet([COLUMNS].concat(rows));
      var wb = XLSX.utils.book_new();
      XLSX.utils.book_append_sheet(wb, ws, 'Roster');
      XLSX.writeFile(wb, filename);
    }

    var templateBtn = document.getElementById('roster-download-template');
    if (templateBtn) templateBtn.addEventListener('click', function () { downloadSheet(sampleRows(), 'duty-roster-template.xlsx'); });

    var currentBtn = document.getElementById('roster-download-current');
    if (currentBtn) {
      currentBtn.addEventListener('click', function () {
        var rows = [];
        R.employees.forEach(function (e) {
          var monthMatrix = R.matrix[e.emp_no] || {};
          Object.keys(monthMatrix).forEach(function (day) {
            var rec = monthMatrix[day];
            rows.push([e.emp_no, e.name, day, rec.status, e.branch, rec.shift1_start || '', rec.shift1_end || '', '', '', '']);
          });
        });
        downloadSheet(rows, 'duty-roster-current-month.xlsx');
      });
    }

    var input = document.getElementById('roster-import-input');
    var filenameLabel = document.getElementById('roster-import-filename');
    var previewWrap = document.getElementById('roster-import-preview');
    var previewBody = document.getElementById('roster-import-preview-body');
    var parsedRows = [];

    if (input) {
      input.addEventListener('change', function () {
        var file = input.files && input.files[0];
        if (!file) return;
        if (filenameLabel) filenameLabel.textContent = file.name;
        var reader = new FileReader();
        reader.onload = function (e) {
          var wb = XLSX.read(e.target.result, { type: 'array' });
          var sheet = wb.Sheets[wb.SheetNames[0]];
          var json = XLSX.utils.sheet_to_json(sheet, { header: 1 });
          parsedRows = json.slice(1).filter(function (r) { return r && r.length && r[0]; });
          renderPreview();
        };
        reader.readAsArrayBuffer(file);
      });
    }

    function renderPreview() {
      if (!previewBody) return;
      previewBody.innerHTML = parsedRows.map(function (r, i) {
        var code = r[0], name = r[1], date = r[2], dayType = r[3], branch = r[4];
        var matches = !!empByNo[code];
        return '<tr><td>' + (i + 1) + '</td><td>' + (name || code || '') + '</td><td>' + date + '</td><td>' + dayType + '</td><td>' + branch + '</td>' +
          '<td><span class="scr-badge ' + (matches ? 'scr-badge-approved' : 'scr-badge-rejected') + '"><i></i>' + (matches ? 'Matched' : 'No match') + '</span></td></tr>';
      }).join('');
      if (previewWrap) previewWrap.hidden = parsedRows.length === 0;
    }

    var cancelBtn = document.getElementById('roster-import-cancel');
    if (cancelBtn) cancelBtn.addEventListener('click', function () {
      parsedRows = [];
      if (previewWrap) previewWrap.hidden = true;
      if (input) input.value = '';
      if (filenameLabel) filenameLabel.textContent = 'Import from Excel';
    });

    var applyBtn = document.getElementById('roster-import-apply');
    if (applyBtn) applyBtn.addEventListener('click', function () {
      // Frontend-only, per CLAUDE.md 1: nothing persists. Applies matched
      // rows into the in-memory matrix so the State Wise/Branch Roster/
      // Employee View tabs reflect the import immediately, then re-renders.
      var applied = 0;
      parsedRows.forEach(function (r) {
        var emp = empByNo[r[0]];
        if (!emp) return;
        var day = String(r[2]);
        R.matrix[emp.emp_no] = R.matrix[emp.emp_no] || {};
        R.matrix[emp.emp_no][day] = { status: r[3], shift1_start: r[5] || null, shift1_end: r[6] || null };
        applied++;
      });
      renderStateTable();
      if (branchSelect) renderWeekGrid(branchGrid, branchSelect.value, currentWeek);
      var selectedName = empSelectHidden && empSelectHidden.value;
      var selectedEmp = selectedName && R.employees.filter(function (x) { return x.name === selectedName; })[0];
      if (selectedEmp) renderEmployeeCalendar(selectedEmp.emp_no);
      parsedRows = [];
      if (previewWrap) previewWrap.hidden = true;
      if (input) input.value = '';
      if (filenameLabel) filenameLabel.textContent = applied + ' row' + (applied === 1 ? '' : 's') + ' applied';
    });
  })();
})();
