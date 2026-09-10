/* BYKY drawer behaviour — one file for every drawer on the site.
   1. picks compact / standard / wide from the rendered field count
   2. builds the section jump tabs (only when 2+ named sections exist)
   3. keeps the current section highlighted while you scroll
   Bootstrap's offcanvas still owns open/close. No dependencies. */
(function () {
  'use strict';

  /* Size thresholds — the only place these numbers live.
     compact:  <= 4 fields and at most one named section
     wide:     > 12 fields, or 4+ named sections
     standard: everything else */
  function pickSize(fieldCount, namedSections) {
    if (fieldCount <= 4 && namedSections <= 1) return 'is-compact';
    if (fieldCount > 12 || namedSections >= 4) return 'is-wide';
    return 'is-standard';
  }

  function setup(drawer) {
    if (drawer.__bykyReady) return;
    drawer.__bykyReady = true;

    var body = drawer.querySelector('[data-byky-body]');
    var jumpBar = drawer.querySelector('[data-byky-jumps]');
    var sections = [].slice.call(drawer.querySelectorAll('[data-byky-section]'));
    var fields = drawer.querySelectorAll('.byky-field');
    var named = sections.filter(function (s) { return (s.dataset.sectionLabel || '').trim(); });

    /* 1 ── size (an explicit is-* class from spec.size wins) */
    if (!/\bis-(compact|standard|wide)\b/.test(drawer.className)) {
      drawer.classList.add(pickSize(fields.length, named.length));
    }

    /* selects: colour the text once a real option is chosen */
    [].forEach.call(drawer.querySelectorAll('.byky-select'), function (sel) {
      var sync = function () { sel.classList.toggle('has-value', !!sel.value); };
      sel.addEventListener('change', sync);
      sync();
    });

    /* file inputs: show the chosen filename */
    [].forEach.call(drawer.querySelectorAll('.byky-file-input'), function (inp) {
      inp.addEventListener('change', function () {
        var label = inp.parentNode.querySelector('span');
        if (label) label.textContent = inp.files && inp.files[0] ? inp.files[0].name : 'Choose file';
      });
    });

    if (!body || named.length < 2) return;

    /* 2 ── jump tabs */
    var tabs = named.map(function (sec, i) {
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'byky-jump' + (i === 0 ? ' is-on' : '');
      b.textContent = sec.dataset.sectionLabel;
      b.addEventListener('click', function () {
        lockUntil = Date.now() + 700;
        body.scrollTo({
          top: body.scrollTop + (sec.getBoundingClientRect().top - body.getBoundingClientRect().top) - 6,
          behavior: 'smooth'
        });
        mark(i);
      });
      jumpBar.appendChild(b);
      return b;
    });
    jumpBar.hidden = false;

    /* 3 ── scroll tracking. Rect deltas, not offsetTop: the drawer is a
       positioned ancestor, so offsetTop is unrelated to scroll position. */
    var lockUntil = 0;
    var current = -1;

    function mark(i) {
      if (i === current) return;
      current = i;
      tabs.forEach(function (t, k) { t.classList.toggle('is-on', k === i); });
      named.forEach(function (s, k) { s.classList.toggle('is-current', k === i); });
    }

    body.addEventListener('scroll', function () {
      if (Date.now() < lockUntil) return;
      var top = body.getBoundingClientRect().top;
      var idx = 0;
      named.forEach(function (sec, i) {
        if (sec.getBoundingClientRect().top - top <= 12) idx = i;
      });
      mark(idx);
    }, { passive: true });

    mark(0);
  }

  function setupAll() {
    [].forEach.call(document.querySelectorAll('[data-byky-drawer]'), setup);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupAll);
  } else {
    setupAll();
  }

  /* re-measure when a drawer opens (fonts/plugins may have shifted layout) */
  document.addEventListener('shown.bs.offcanvas', function (e) {
    if (e.target && e.target.matches('[data-byky-drawer]')) {
      var body = e.target.querySelector('[data-byky-body]');
      if (body) body.dispatchEvent(new Event('scroll'));
    }
  });
})();
