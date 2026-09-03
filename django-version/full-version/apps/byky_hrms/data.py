"""Display data for Module 2 (HRMS).

Derived from apps/byky_core/seed.py. The client's staff sheet populates only
Employee No, Name and Profession; the other 22 columns are empty headers, so every
identity, document and bank field renders seed.NOT_CAPTURED. No passport numbers,
Emirates IDs, dates of birth or bank details are invented (CLAUDE.md section 12).
"""

from apps.byky_core import seed

NOT_CAPTURED = seed.NOT_CAPTURED
SHORT = seed.NOT_CAPTURED_SHORT

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
                "emirates_id_expiry": SHORT,
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
