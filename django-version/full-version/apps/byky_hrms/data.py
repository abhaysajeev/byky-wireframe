"""Display data for Module 2 (HRMS).

Derived from apps/byky_core/seed.py. The client's staff sheet populates only
Employee No, Name and Profession; the other 22 columns are empty headers, so every
identity, document and bank field renders seed.NOT_CAPTURED. No passport numbers,
Emirates IDs, dates of birth or bank details are invented (CLAUDE.md section 12).
"""

import datetime

from apps.byky_core import seed

NOT_CAPTURED = seed.NOT_CAPTURED
SHORT = seed.NOT_CAPTURED_SHORT

# The four documents FSD 2.1's Identity Documents tab tracks expiry for.
# (field key on an employees() row, display label)
DOCUMENTS = [
    ("visa_expiry", "Visa"),
    ("eid_expiry", "Emirates ID"),
    ("labor_expiry", "Labour Card"),
    ("passport_expiry", "Passport"),
]

NEARING_EXPIRY_DAYS = 30

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


def _expiry_status(value):
    """expired / nearing / valid / unknown, from one employee's raw expiry
    value. The staff sheet carries none of these dates today, so every
    employee currently resolves to "unknown" for all four documents -- this
    is the real logic that will light up red/amber/green the moment the
    client supplies actual dates, not a placeholder invented in the meantime
    (CLAUDE.md 12)."""
    if not value or value in (SHORT, NOT_CAPTURED):
        return "unknown"
    try:
        expiry = datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return "unknown"
    days_left = (expiry - datetime.date.today()).days
    if days_left < 0:
        return "expired"
    if days_left <= NEARING_EXPIRY_DAYS:
        return "nearing"
    return "valid"


def document_expiry_summary(employee_rows):
    """Per-document expired/nearing/valid/unknown counts across every
    employee row passed in, for the four-document expiry tile row."""
    out = []
    for key, label in DOCUMENTS:
        tally = {"expired": 0, "nearing": 0, "valid": 0, "unknown": 0}
        for e in employee_rows:
            tally[_expiry_status(e.get(key))] += 1
        total = len(employee_rows) or 1
        out.append(
            {
                "key": key,
                "label": label,
                "total": len(employee_rows),
                "expired": tally["expired"],
                "nearing": tally["nearing"],
                "valid": tally["valid"],
                "unknown": tally["unknown"],
                "pct_expired": round(tally["expired"] / total * 100, 2),
                "pct_nearing": round(tally["nearing"] / total * 100, 2),
                "pct_valid": round(tally["valid"] / total * 100, 2),
                "pct_unknown": round(tally["unknown"] / total * 100, 2),
            }
        )
    return out
