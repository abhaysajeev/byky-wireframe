"""Display data for Module 2 (HRMS).

Derived from apps/byky_core/seed.py. The client's staff sheet populates only
Employee No, Name and Profession; the other 22 columns are empty headers, so every
identity, document and bank field renders seed.NOT_CAPTURED. No passport numbers,
Emirates IDs, dates of birth or bank details are invented (CLAUDE.md section 12).
"""

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
