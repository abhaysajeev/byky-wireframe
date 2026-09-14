"""Display data for Module 2 (HRMS).

Derived from apps/byky_core/seed.py. The client's staff sheet populates only
Employee No, Name and Profession; the other 22 columns are empty headers, so every
identity, document and bank field renders seed.NOT_CAPTURED. No passport numbers,
Emirates IDs, dates of birth or bank details are invented (CLAUDE.md section 12).
"""

import datetime
import hashlib

from apps.byky_core import seed

NOT_CAPTURED = seed.NOT_CAPTURED
SHORT = seed.NOT_CAPTURED_SHORT

# The four documents FSD 2.1's Identity Documents tab tracks expiry for.
# (field key, display label)
DOCUMENTS = [
    ("visa", "Visa"),
    ("eid", "Emirates ID"),
    ("labor", "Labour Card"),
    ("passport", "Passport"),
]


def _demo_expiry_bucket(emp_no, doc_key):
    """Explicit, user-requested exception to CLAUDE.md 12: the client's staff
    sheet carries no real Visa/Emirates ID/Labour Card/Passport expiry dates,
    so there is nothing genuine to bucket. The Document Expiry Status KPI
    tiles need *some* real, clickable, filterable difference between
    employees to demonstrate the click-to-filter interaction in this
    wireframe -- so this assigns each employee a deterministic (stable
    across requests, not random) demo bucket per document, for that purpose
    only. It is never shown as a real date, document number or anything an
    operator could mistake for actual client data -- only as a coloured
    segment and a filter value. Do not extend this pattern to any other
    field; every other document/date field on this screen still renders
    seed.NOT_CAPTURED, honestly, per CLAUDE.md 12."""
    digest = hashlib.md5(f"{emp_no}:{doc_key}".encode()).hexdigest()
    return ["expired", "nearing", "valid"][int(digest, 16) % 3]

# FSD 2.6: six permissions for HRMS, not the seven CMS uses.
PERMISSIONS = ["Access", "Create", "Read", "Update", "Approve", "Block Staff"]

# FSD 2.5 section 18: reason categories for a block action.
BLOCK_REASONS = [
    "Disciplinary",
    "Absconding",
    "Document Expiry",
    "Resignation Pending",
    "Investigation",
    "Other",
]

AWAITING = {
    "addresses": "temporary addresses",
    "grades": "salary grades",
    "block_log": "block and unblock history",
}


def employees():
    """The 99 staff records. Only three columns carry data."""
    out = []
    for e in seed.EMPLOYEES:
        buckets = {key: _demo_expiry_bucket(e["emp_no"], key) for key, _ in DOCUMENTS}
        out.append(
            {
                "emp_no": e["emp_no"],
                "name": e["name"],
                "designation": e["profession"],
                "branch": SHORT,
                "department": SHORT,
                "joining_date": SHORT,
                "nationality": SHORT,
                "visa_no": SHORT,
                "visa_expiry": SHORT,
                "eid_expiry": SHORT,
                "labor_expiry": SHORT,
                "passport_expiry": SHORT,
                "salary_bank": SHORT,
                "salary_bank_account": SHORT,
                "mobile": SHORT,
                "active": True,
                "status": "Active",
                # Demo-only buckets -- see _demo_expiry_bucket()'s docstring.
                # "attention" collapses expired+nearing into one filterable
                # value, since that's the useful click target on the KPI tile
                # (an HR user cares "does this employee need action", not
                # which of the two sub-states).
                "visa_bucket": buckets["visa"],
                "visa_attention": "yes" if buckets["visa"] in ("expired", "nearing") else "no",
                "eid_bucket": buckets["eid"],
                "eid_attention": "yes" if buckets["eid"] in ("expired", "nearing") else "no",
                "labor_bucket": buckets["labor"],
                "labor_attention": "yes" if buckets["labor"] in ("expired", "nearing") else "no",
                "passport_bucket": buckets["passport"],
                "passport_attention": "yes" if buckets["passport"] in ("expired", "nearing") else "no",
            }
        )
    return out


def _desig_code(title):
    """3-4 character code from the job title."""
    words = [w for w in title.replace("/", " ").split() if w]
    if len(words) == 1:
        return words[0][:4].upper()
    return "".join(w[0] for w in words)[:4].upper()


def designations():
    """FSD 2.3 is the master of staff job titles. The client's Profession column
    is exactly that, so the list is derived from it rather than invented."""
    counts = {}
    for e in seed.EMPLOYEES:
        counts[e["profession"]] = counts.get(e["profession"], 0) + 1
    out = []
    for title, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        out.append(
            {
                "code": _desig_code(title),
                "title": title,
                "description": SHORT,
                # FSD 2.3 section 23 defaults RankOrder to 1. The client supplied no
                # seniority ranking, so inferring one from headcount would misstate it.
                "rank": 1,
                "headcount": n,
                "active": True,
                "status": "Active",
            }
        )
    return out


def counts():
    emps = seed.EMPLOYEES
    return {
        "total": len(emps),
        "designations": len({e["profession"] for e in emps}),
        "branches": len(seed.STATIONS),
        "blocked": 0,
    }


def _desig_titles():
    return [d["title"] for d in designations()]


# ---------------------------------------------------------------------------
# Incentive (RMS WEB APK UI feedback -- "new html" mockups, not FSD screens).
# Built from the client's incentive.html mockup. The mockup pins "Cashier
# with RMS Login" / "Cashier without RMS Login" / "Labour" as separate user
# types with 6 further invented job titles (Supervisor, Warehouse Staff,
# Accountant, Manager...) that don't exist in the real 9-designation master.
# Kept 100% of the mockup's behaviour (the RMS-login split, its own dividend
# rules, the pinned-first ordering) but grounded the type list in real
# designations() instead: the RMS-login split is modelled as two sub-rows of
# the one real "Cashier" designation (pinned first, alongside "Labour", also
# real), and every "other" type is a real designation in its real headcount
# order -- never an invented job title.
# ---------------------------------------------------------------------------

CASHIER_RMS = "Cashier with RMS Login"
CASHIER_NO_RMS = "Cashier without RMS Login"

DIVIDEND_LABELS = {
    "single": "Full amount — single person",
    "split": "Split equally — on-duty headcount",
}
CASHIER_NO_LOGIN_LABELS = {
    "as_labour": "Counted as Labour — joins the equal-split headcount",
    "as_cashier": "Counted as Cashier — own % split equally among them",
}


def incentive_user_types():
    """Ordered [{"title", "pinned"}] -- Cashier (RMS)/Cashier (No RMS)/Labour
    pinned first (see module note above), then every other real designation
    in headcount order."""
    titles = _desig_titles()
    others = [t for t in titles if t not in ("Cashier", "Labour")]
    pinned = [CASHIER_RMS, CASHIER_NO_RMS, "Labour"]
    return [{"title": t, "pinned": True} for t in pinned] + [{"title": t, "pinned": False} for t in others]


def default_dividend_for(user_type):
    if user_type == CASHIER_RMS:
        return "single"
    if user_type == CASHIER_NO_RMS:
        return "as_labour"
    return "split"


def dividend_label(row):
    if row["type"] == CASHIER_RMS:
        return "Full amount — single person (the one logged into RMS)"
    if row["type"] == CASHIER_NO_RMS:
        return CASHIER_NO_LOGIN_LABELS.get(row["dividend"], row["dividend"])
    return DIVIDEND_LABELS.get(row["dividend"], row["dividend"])


def _incentive_plan(code, name, rows):
    total_pct = sum(r["target_pct"] for r in rows)
    return {
        "code": code,
        "name": name,
        "rows": rows,
        "types": [r["type"] for r in rows],
        "total_pct": total_pct,
    }


def incentive_plans():
    """2 deterministic sample plans, the same worked example the mockup
    ships (its two dividend modes for the no-RMS-login cashier), over real
    designations. Openly-fabricated demo percentages, not client-supplied
    figures -- same footing as this module's other demo constants."""
    return [
        _incentive_plan(
            "INC-2026-001",
            "Standard Branch Collection Incentive",
            [
                {"type": CASHIER_RMS, "target_pct": 1, "dividend": "single"},
                {"type": CASHIER_NO_RMS, "target_pct": 0, "dividend": "as_labour"},
                {"type": "Labour", "target_pct": 1, "dividend": "split"},
            ],
        ),
        _incentive_plan(
            "INC-2026-002",
            "Premium Station Incentive",
            [
                {"type": CASHIER_RMS, "target_pct": 1, "dividend": "single"},
                {"type": CASHIER_NO_RMS, "target_pct": 1, "dividend": "as_cashier"},
                {"type": "Labour", "target_pct": 1, "dividend": "split"},
                {"type": "Administrative Supervisor", "target_pct": 0.5, "dividend": "split"},
            ],
        ),
    ]


def incentive_plan_by_code(code):
    for p in incentive_plans():
        if p["code"] == code:
            return p
    return None


def incentive_counts(plans):
    types_covered = {t for p in plans for t in p["types"]}
    split_rows = sum(1 for p in plans for r in p["rows"] if r["dividend"] == "split")
    avg_pct = (sum(p["total_pct"] for p in plans) / len(plans)) if plans else 0
    return {
        "total": len(plans),
        "types_covered": len(types_covered),
        "avg_pct": round(avg_pct, 1),
        "split_rows": split_rows,
    }


# ---------------------------------------------------------------------------
# Incentive Branch Mapping (RMS WEB APK UI feedback -- incentive-branch-
# mapping.html). Maps an incentive plan to a set of branches, with a
# validity window and a priority so each branch resolves to one active
# mapping at a time.
# ---------------------------------------------------------------------------

# Fixed reference "today" for validity/expiry math across the 5 new HRMS
# screens -- never datetime.now(), so the demo state (and its "expiring
# soon" tags) stays identical between requests instead of drifting with the
# real clock.
TODAY = datetime.date(2026, 9, 14)


def is_expiring_soon(valid_to, today=TODAY):
    return 0 <= (valid_to - today).days <= 30


def mapping_branch_keys(mapping, all_branch_names):
    return all_branch_names if mapping["all_branches"] else mapping["branch_keys"]


def incentive_branch_mappings():
    """3 deterministic sample mappings over real branches/incentive plans --
    mirrors the mockup's own worked example. Openly-fabricated mapping
    names/dates, real branch and plan references."""
    plans = incentive_plans()
    return [
        {
            "code": "IBM-2026-001",
            "name": "Dubai Core Branches — Incentive",
            "all_branches": False,
            "branch_keys": ["Creek Park Gate 1", "Creek Park Gate 4", "Al Mamzar Park"],
            "emirate": "Dubai",
            "plan_code": plans[0]["code"],
            "valid_from": datetime.date(2026, 1, 1),
            "valid_to": datetime.date(2026, 12, 31),
            "priority": 2,
        },
        {
            "code": "IBM-2026-002",
            "name": "Abu Dhabi — Premium Incentive",
            "all_branches": False,
            "branch_keys": ["Al Zabeel Park Gate 1"],
            "emirate": "Abu Dhabi",
            "plan_code": plans[1]["code"],
            "valid_from": datetime.date(2026, 6, 1),
            "valid_to": TODAY + datetime.timedelta(days=18),
            "priority": 1,
        },
        {
            "code": "IBM-2026-003",
            "name": "Network-Wide Standard Incentive",
            "all_branches": True,
            "branch_keys": [],
            "emirate": "",
            "plan_code": plans[0]["code"],
            "valid_from": datetime.date(2026, 1, 1),
            "valid_to": datetime.date(2027, 3, 31),
            "priority": 8,
        },
    ]


def incentive_mapping_counts(mappings, all_branch_names):
    unique = set()
    plans_used = set()
    expiring = 0
    for m in mappings:
        unique.update(mapping_branch_keys(m, all_branch_names))
        plans_used.add(m["plan_code"])
        if is_expiring_soon(m["valid_to"]):
            expiring += 1
    return {
        "total": len(mappings),
        "unique_branches": len(unique),
        "plans_in_use": len(plans_used),
        "expiring_soon": expiring,
    }


# ---------------------------------------------------------------------------
# Target (RMS WEB APK UI feedback -- target.html). A named target profile
# over a Yearly/Monthly/Daily/Custom period, carrying a collection target
# (AED) and a new-customer target. Branch mapping is a separate screen
# (Target Branch Mapping) -- this one only previews it read-only, exactly
# as the mockup's own "coming in the next update" language states.
# ---------------------------------------------------------------------------

_MONTHS = ["January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December"]


def period_label(period):
    """Formats a period dict the same way the mockup's periodLabel() does."""
    t = period["type"]
    if t == "Yearly":
        return f"FY{period['year']}"
    if t == "Monthly":
        months = period["months"]
        if len(months) == 1:
            return f"{months[0][:3]} {period['year']}"
        if len(months) <= 3:
            return ", ".join(m[:3] for m in months) + f" {period['year']}"
        return f"{len(months)} months, {period['year']}"
    if t == "Daily":
        d = datetime.date(int(period["year"]), _MONTHS.index(period["month"]) + 1, int(period["day"]))
        return d.strftime("%b %-d, %Y") if hasattr(d, "strftime") else str(d)
    if t == "Custom Date Range":
        return f"{period['from_date'].strftime('%b %-d')} – {period['to_date'].strftime('%b %-d, %Y')}"
    return ""


def _target_profile(code, name, period, collection_target, customer_target):
    return {
        "code": code,
        "name": name,
        "type": period["type"],
        "period": period,
        "period_display": period_label(period),
        "collection_target": collection_target,
        "customer_target": customer_target,
    }


def target_profiles():
    """4 deterministic sample profiles, one per period type -- mirrors the
    mockup's own worked example. Openly-fabricated round AED/count figures,
    deterministic, never claimed as real client targets -- this is a
    forward target the client sets, not derived revenue, so it isn't
    tagged Indicative the way sales.py's dashboard figures are, but it's
    the same spirit of clearly-demo wireframe content."""
    return [
        _target_profile("TP-2026-001", "FY26 Network Collection Target", {"type": "Yearly", "year": "2026"}, 8500000, 4200),
        _target_profile("TP-2026-002", "September 2026 Growth Target", {"type": "Monthly", "year": "2026", "months": ["September"]}, 720000, 360),
        _target_profile("TP-2026-003", "National Day Weekend Target", {"type": "Daily", "year": "2026", "month": "December", "day": "2"}, 45000, 25),
        _target_profile("TP-2026-004", "Q4 Expansion Target", {"type": "Custom Date Range", "from_date": datetime.date(2026, 10, 1), "to_date": datetime.date(2026, 12, 31)}, 1900000, 950),
    ]


def target_profile_by_code(code):
    for p in target_profiles():
        if p["code"] == code:
            return p
    return None


def target_counts(profiles, mapped_codes):
    return {
        "total": len(profiles),
        "combined_collection": sum(p["collection_target"] for p in profiles),
        "combined_customers": sum(p["customer_target"] for p in profiles),
        "unmapped": sum(1 for p in profiles if p["code"] not in mapped_codes),
    }


# ---------------------------------------------------------------------------
# Target Branch Mapping (RMS WEB APK UI feedback -- target-branch-mapping.html).
# Structurally identical to Incentive Branch Mapping above.
# ---------------------------------------------------------------------------

def target_branch_mappings():
    """3 deterministic sample mappings over real branches/target profiles."""
    profiles = target_profiles()
    return [
        {
            "code": "BM-2026-001",
            "name": "Dubai — FY26 Network Target",
            "all_branches": False,
            "branch_keys": ["Creek Park Gate 1", "Al Barsha Pond Park"],
            "emirate": "Dubai",
            "profile_code": profiles[0]["code"],
            "valid_from": datetime.date(2026, 1, 1),
            "valid_to": datetime.date(2026, 12, 31),
            "priority": 3,
        },
        {
            "code": "BM-2026-002",
            "name": "Sharjah — September Growth Target",
            "all_branches": False,
            "branch_keys": ["Majaz 1", "Sharjah Corniche 1"],
            "emirate": "Sharjah",
            "profile_code": profiles[1]["code"],
            "valid_from": datetime.date(2026, 9, 1),
            "valid_to": TODAY + datetime.timedelta(days=10),
            "priority": 1,
        },
        {
            "code": "BM-2026-003",
            "name": "Network-Wide Q4 Expansion",
            "all_branches": True,
            "branch_keys": [],
            "emirate": "",
            "profile_code": profiles[3]["code"],
            "valid_from": datetime.date(2026, 10, 1),
            "valid_to": datetime.date(2026, 12, 31),
            "priority": 5,
        },
    ]


def target_mapping_counts(mappings, all_branch_names):
    unique = set()
    profiles_used = set()
    expiring = 0
    for m in mappings:
        unique.update(mapping_branch_keys(m, all_branch_names))
        profiles_used.add(m["profile_code"])
        if is_expiring_soon(m["valid_to"]):
            expiring += 1
    return {
        "total": len(mappings),
        "unique_branches": len(unique),
        "profiles_in_use": len(profiles_used),
        "expiring_soon": expiring,
    }


def document_expiry_summary(employee_rows):
    """Per-document expired/nearing/valid counts across every employee row
    passed in, for the Document Expiry Status KPI tiles. Reads the demo
    buckets from employees() -- see _demo_expiry_bucket()'s docstring for
    why those exist and what they are not."""
    out = []
    for key, label in DOCUMENTS:
        tally = {"expired": 0, "nearing": 0, "valid": 0}
        for e in employee_rows:
            tally[e[key + "_bucket"]] += 1
        out.append(
            {
                "key": key,
                "label": label,
                "expired": tally["expired"],
                "nearing": tally["nearing"],
                "valid": tally["valid"],
                "attention": tally["expired"] + tally["nearing"],
            }
        )
    return out
