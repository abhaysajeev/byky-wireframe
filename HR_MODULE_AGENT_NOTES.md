# Notes for the agent working on HR module changes

Written by another Claude Code session working in this same repo, right
after resolving two large merge conflicts caused by two agents/worktrees
editing the same shared files (`vertical_menu.json`, `byky-screen.css`,
`byky-screen.js`, `config/settings.py`, `config/urls.py`) for days without
syncing against `main`. Nothing was lost, but it took a full session to
untangle. This doc exists so it doesn't happen again while you work on HRMS
and I (or someone else) keep working on other modules in parallel.

Read this before you start, and re-read the "Sync often" section every time
you're about to commit.

---

## 0. Update — Employee Personal Data changed after this doc was first written

`apps/byky_hrms/data.py`, `apps/byky_hrms/views.py`, and
`apps/byky_hrms/templates/hrms_employee_personal_data.html` were all touched
again in a follow-up round of commits (after this doc's original §4 was
written) — the "no one else is working there right now" note in §3 is only
true as of *this* update; **pull latest `main` before editing any of these
three files** so you're not diffing against a stale copy.

What changed, and why, so you don't "fix" it back:

- The **Document Expiry Status** card (Visa / Emirates ID / Labour Card /
  Passport) is now interactive: clicking a document filters the employee
  table to everyone needing attention (expired or nearing) on it. This
  reuses the existing filter+search+pagination mechanism via a new
  **`data-scr-kpi-filter="<filter key>:<value>"`** attribute on a
  `.scr-tile`/`.scr-doc-item` button (added to `byky-screen.js`) — clicking
  it just clicks the matching `.scr-filter-opt` under a `.scr-filter-wrap`
  with that `data-filter-key`, so it works with zero new filtering logic.
  A second new attribute, **`data-scr-kpi-group="<name>"`**, makes a set of
  tiles mutually exclusive (picking one resets the others, clicking the
  active one again clears it) — used so the 4 documents don't silently AND
  together. Both are documented inline in `byky-screen.js` right above
  where they're implemented; read that if you need to reuse either.
- The 4 document buckets (expired/nearing/valid) shown on that card are
  **synthetic demo data**, generated deterministically per employee by
  `_demo_expiry_bucket()` in `apps/byky_hrms/data.py`. This is a **narrow,
  explicit, user-requested exception** to the no-invented-data rule in §6
  below — the client's staff sheet genuinely has no expiry dates, and the
  user explicitly asked for a working click-to-filter demo anyway. **Read
  that function's docstring before touching this screen** — it explains
  the exception is scoped to this one interaction only. Every other
  document field on the screen (drawer inputs, expiry dates, numbers) still
  renders `seed.NOT_CAPTURED` honestly; do not extend the demo-bucket
  pattern to any other field or screen without the same explicit user
  sign-off.
- The card's visual style went through two iterations and settled on:
  no tricolor proportion bar, no colour legend, just each document's name
  + "`N` expired · `M` nearing" as plain text, with a minimal (text-colour
  only, no border/background box) active state when clicked. If you're
  restyling this card, match that — the tricolour bar was deliberately
  removed, not missed.
- New shared CSS added: `.scr-doc-expiry*`, `.scr-doc-item*` in
  `byky-screen.css` (this card had no CSS at all before this round, in any
  earlier session either — it was rendering unstyled).

---

## 1. Why the last clash happened (so you know what to avoid)

Two worktrees branched off `main` at the same old commit and then each ran
for **18+ commits** without ever pulling `main` back in. Meanwhile `main`
itself got a full sidebar rebuild, a dozen new modules, and a menu-JSON
reorganization. By the time both branches were merged back, `vertical_menu.json`
alone had 11 separate conflict hunks, plus real feature conflicts in shared
CSS/JS files. Every one was resolvable, but only because the person doing the
merge could read `git log`, diff both sides, and understand *why* each hunk
differed (a bug fix vs. stale pre-fix code, a rename vs. an old name, etc.).
That's expensive. Syncing every day would have made each of those a
one-line, obvious resolution instead.

**The fix going forward is frequency, not process weight**: small, frequent
syncs beat a big, correct-but-costly merge at the end.

---

## 2. Sync often — the actual rule

Before you start a work session, and again before any commit that touches a
shared file (see §3), run:

```bash
git fetch origin
git merge origin/main
```

(or rebase if you prefer — either is fine, this repo doesn't require one over
the other). Do this **at least once a day** if you're running long, and
ideally before every commit. If a conflict shows up here, it'll be small and
recent, not a week's worth of drift — resolve it immediately, don't defer it.

Push your own commits to a feature branch (not `main` directly) reasonably
often too, so your work isn't sitting unintegrated for days. Small commits
with clear messages, same convention as the rest of this repo's history —
one logical change per commit, description of *why*, not just what.

---

## 3. Files you'll likely touch that are shared, not HR-only

These are edited by every module's work, so conflicts concentrate here.
Sync before touching them, and keep your edits to them as small/localized as
possible (e.g. one menu entry, not a whole reorder):

| File | What you'll add | Conflict risk |
|---|---|---|
| `django-version/full-version/templates/layout/partials/menu/vertical/json/vertical_menu.json` | Your HRMS submenu entries, badge count | **High** — every module touches this |
| `django-version/full-version/src/assets/css/byky-screen.css` | Only if HR needs a genuinely new `.scr-*` class/pattern not already there | Medium |
| `django-version/full-version/src/assets/js/byky-screen.js` | Only if HR needs new generic `data-scr-*` behavior | Medium |
| `django-version/full-version/config/settings.py` | Nothing — `apps.byky_hrms` is already registered | Low (don't need to touch) |
| `django-version/full-version/config/urls.py` | Nothing — HRMS urls are already included | Low (don't need to touch) |

Everything under `apps/byky_hrms/` itself (`views.py`, `data.py`, `urls.py`,
`templates/hrms_*.html`) is otherwise yours alone — but see **§0 above**
first: `data.py`, `views.py`, and `hrms_employee_personal_data.html`
specifically were touched again after this doc was first written, so pull
`main` before editing those three.

**Before adding a genuinely new `.scr-*` class or `data-scr-*` attribute**:
grep both shared files first (`byky-screen-design-system.md` §9 covers this)
to confirm it doesn't already exist. Several conditional-visibility and
badge-state patterns already exist (`data-scr-show-if`, `.scr-badge-active`
/`.scr-badge-inactive`) — check before inventing your own.

---

## 4. Current HRMS state (as of this writing) — so you know the baseline

Screens, already built and registered:

```
hrms-employee-personal-data        → hrms_employee_personal_data.html
hrms-employee-temporary-address    → hrms_employee_temporary_address.html
hrms-employee-designation-master   → hrms_employee_designation_master.html
hrms-employee-grade-master         → hrms_employee_grade_master.html
hrms-employee-block-unblock        → hrms_employee_block_unblock.html
hrms-hrms-privileges               → hrms_hrms_privileges.html
```

Sidebar entry (`vertical_menu.json`), module labeled **"Human Resources"**,
badge count **5**, matching the 5 submenu entries below:

```json
{
  "name": "Human Resources",
  "slug": "hrms",
  "submenu": [
    { "url": "hrms-employee-personal-data", "name": "Employee Personal Data" },
    { "url": "hrms-employee-temporary-address", "name": "Employee Temporary Address" },
    { "url": "hrms-employee-designation-master", "name": "Employee Designation Master" },
    { "url": "hrms-employee-block-unblock", "name": "Employee Block / Unblock" },
    { "url": "hrms-hrms-privileges", "name": "HRMS Privileges" }
  ]
}
```

**`hrms-employee-grade-master`** (`hrms_employee_grade_master.html`) is
built and registered in `urls.py` but **not in the sidebar** — a hidden
screen. If your work involves it, you'll need to add it to the submenu
above (and bump the badge to 6) rather than assuming it's already linked.

`Employee Personal Data` is the richest screen (Tier B, 22 FSD fields, all 99
real staff records, Document Expiry Status card, flatpickr DOB, nationality
dropdown). It's the reference to match for structure/spacing if you add
another Tier B HR screen.

---

## 5. Naming conventions currently enforced sidebar-wide

Recently, every sidebar label had its trailing "Management" suffix stripped
(e.g. "Company Management" → "Company", "Discount Card Management" →
"Discount Card"). If you add a new HR submodule/screen, **don't give it a
"... Management" label** — match the stripped-suffix convention already
applied everywhere else, or your addition will look inconsistent with every
other module the moment it's merged.

Also recently: several CMS screens replaced an invented "Approval" status
(Approved/Pending/Rejected badges with no real approval workflow behind
them) with an honest **Active/Inactive** status driven by the record's real
`active` field. If any HR screen has a similar decorative "Approval" column
with no actual workflow behind it, consider the same fix — but that's a
judgment call for whoever owns that screen, not a hard rule.

---

## 6. General project rules (from `CLAUDE.md`, still binding)

- Wireframe phase: no real CRUD, no APIs, static seed data only.
- Never invent data (no fake passport numbers, fake dates, "John Doe").
  Missing HR fields render `seed.NOT_CAPTURED` / `NOT_CAPTURED_SHORT`.
- `.scr-*` is the current design system for any screen you touch or add —
  see `byky-screen-design-system.md` at repo root before writing markup from
  scratch.
- Restart the dev server after any Python or template change — it does not
  reliably hot-reload in this project.
- Run a full route sweep (`manage.py check` + a `Client()`/`get_resolver()`
  walk over every URL) before considering a change done.

---

## 7. If a conflict does happen anyway

Don't panic-resolve. For `vertical_menu.json` specifically: read both sides,
figure out which one is *later* (check `git log` on the file, or just reason
about which naming/structure matches the current conventions in §5), and
keep that one — don't try to hand-merge two different sidebar reorganizations
into a third new structure. For CSS/JS: if one side is a bug fix and the
other predates the bug, the fix wins — check the commit message/comment for
context before assuming it's a stylistic difference.
