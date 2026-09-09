"""Display data for Module 1 (Company Management).

Derived from apps/byky_core/seed.py, i.e. from the client's Excel files.

Where the client data contains no source for an FSD entity, the list is empty and
the screen shows an "awaiting data" state naming what is still needed. Nothing is
fabricated -- see CLAUDE.md section 12.
"""

from apps.byky_core import seed

NOT_CAPTURED = seed.NOT_CAPTURED
SHORT = seed.NOT_CAPTURED_SHORT

# Emirate -> country. The client's vehicle sheet contains a Kuwait station and a
# "Kuwait Bike" category, so two countries are represented in the data.
_COUNTRY_OF = {"Kuwait": "Kuwait"}
_DEFAULT_COUNTRY = "United Arab Emirates"

# Standard emirate/city abbreviations -- conventional codes, not invented ones.
_STATE_CODE = {
    "Abu Dhabi": "AUH", "Dubai": "DXB", "Sharjah": "SHJ", "Ajman": "AJM",
    "Ras Al Khaimah": "RAK", "Fujairah": "FUJ", "Al Ain": "AAN", "Kuwait": "KWI",
}


def country_of_state(state_name):
    """Which country a state/emirate belongs to -- same mapping states() and
    countries() already use, exposed standalone so a screen that only stores
    the state (e.g. Branch, seeded from station data) can still prefill a
    Country field without duplicating the lookup."""
    return _COUNTRY_OF.get(state_name, _DEFAULT_COUNTRY)


def countries():
    seen = {}
    for s in seed.STATIONS:
        c = _COUNTRY_OF.get(s["emirate"], _DEFAULT_COUNTRY)
        seen.setdefault(c, 0)
        seen[c] += 1
    out = []
    for name, n in sorted(seen.items()):
        out.append(
            {
                "code": "UAE" if name.startswith("United") else "KWT",
                "name": name,
                "states": n,
                "active": True,
            }
        )
    return out


def states():
    """Emirates, as the state tier under country."""
    agg = {}
    for s in seed.STATIONS:
        e = s["emirate"]
        agg.setdefault(e, {"branches": 0, "fleet": 0})
        agg[e]["branches"] += 1
        agg[e]["fleet"] += s["vehicle_count"]
    out = []
    for name, v in sorted(agg.items()):
        out.append(
            {
                "code": _STATE_CODE.get(name, name[:3].upper()),
                "name": name,
                "country": _COUNTRY_OF.get(name, _DEFAULT_COUNTRY),
                "branches": v["branches"],
                "fleet": v["fleet"],
                "active": True,
            }
        )
    return out


BRANCH_TYPES = ["Head Office", "Regional Office", "Regional Warehouse", "Branch Office", "Branch Warehouse"]


def branches():
    """Each rental station is a branch hub (FSD 1.4: 'rental station branch hubs').
    All 36 are real, operating rental stations, so Branch Type defaults to
    "Branch Office" -- the client's files carry no head-office/warehouse
    designation, so nothing is invented, just the type these rows actually
    are. Is Hotel, Is App Payment and Is Test Vehicle have no source in the
    client files either, so they default to False -- not invented, just not
    yet flagged true for any real branch. Is HO is derived from Branch Type,
    not a separate flag, so the two can't disagree."""
    out = []
    for s in seed.STATIONS:
        branch_type = "Branch Office"
        out.append(
            {
                "code": s["code"].replace("ST", "BR"),
                "station_code": s["code"],
                "name": s["name"],
                "company": "BYKY",
                "location": s["emirate"],
                "fleet": s["vehicle_count"],
                # Same real number as "fleet" -- the vehicles stationed here
                # are exactly what's deployed to this branch. Not tracked
                # separately from fleet for Head Office (no vehicles sit at
                # an admin office), which the drawer field also reflects by
                # hiding for that one branch type.
                "assets_deployed": s["vehicle_count"],
                "branch_type": branch_type,
                "is_ho": branch_type == "Head Office",
                "is_hotel": False,
                "app_payment": False,
                "multi_user": True,
                "test_vehicle": False,
                "hotel_commission": "0.00",
                "active": True,
            }
        )
    return out


def company():
    """The single operating company. Registration details are not in the client
    files, so they render as 'not captured' rather than being invented."""
    st = seed.STATIONS
    return {
        "code": "BYKY",
        "name": "BYKY",
        "address": NOT_CAPTURED,
        "state": "Dubai",
        "city": NOT_CAPTURED,
        "zip": NOT_CAPTURED,
        "inc_cert_no": NOT_CAPTURED,
        "business_cert_no": NOT_CAPTURED,
        "income_tax_no": NOT_CAPTURED,
        "tax_pct": "0.00",
        "tin": NOT_CAPTURED,
        "cst": NOT_CAPTURED,
        "service_tax_no": NOT_CAPTURED,
        "contact_person": NOT_CAPTURED,
        "phone": NOT_CAPTURED,
        "fax": NOT_CAPTURED,
        "email": NOT_CAPTURED,
        "web_address": NOT_CAPTURED,
        "ceo_name": NOT_CAPTURED,
        "dto_name": NOT_CAPTURED,
        "logo": "",  # not a client-data gap (NOT_CAPTURED) -- genuinely no logo uploaded yet
        "branches": len(st),
        "status": "Approved",
        "active": True,
    }


# (label, key, required, help, span) per field, grouped exactly as the approved
# "Byky Company Details" design groups them -- 20 fields across 4 sections,
# matching FSD 1.1 section 11.
_COMPANY_SECTIONS = [
    ("basic", "Basic Information", "Basics", [
        ("Company Code", "code", True, "Immutable once approved.", 1),
        ("Company Name", "name", True, "", 2),
        ("CEO Name", "ceo_name", False, "", 1),
        ("DTO Name", "dto_name", False, "", 1),
    ]),
    ("address", "Address", "Address", [
        ("Address", "address", False, "", 2),
        ("Emirate / State", "state", True, "", 1),
        ("City", "city", False, "", 1),
        ("ZIP Code", "zip", False, "", 1),
    ]),
    ("tax", "Registration & Tax", "Registration", [
        ("Incorporation Certificate No", "inc_cert_no", False, "", 1),
        ("Business Certificate No", "business_cert_no", False, "", 1),
        ("Income Tax No", "income_tax_no", False, "", 1),
        ("Tax %", "tax_pct", False, "UAE standard VAT is 5%.", 1),
        ("TIN", "tin", False, "", 1),
        ("CST", "cst", False, "", 1),
        ("Service Tax No", "service_tax_no", False, "", 1),
    ]),
    ("contact", "Contact", "Contact", [
        ("Contact Person", "contact_person", False, "", 1),
        ("Phone Number", "phone", True, "", 1),
        ("Fax", "fax", False, "", 1),
        ("Email Address", "email", True, "", 1),
        ("Web Address", "web_address", False, "", 1),
    ]),
]


_COMPANY_SECTION_HINTS = {
    "basic": "The company code is written into every station, vehicle and agreement "
    "reference — it cannot be changed after approval.",
    "address": "The emirate drives which fare plans and RFID gate rules a company inherits.",
    "tax": "Seven registration fields stay empty until the client sends the trade "
    "licence pack; nothing here is invented.",
    "contact": "This contact receives approval, settlement and device-health "
    "notifications for every station the company owns.",
}


def company_sections(company_record):
    """Groups company_record's 20 fields into the 4 sections the design and
    FSD 1.1 both use. A field whose value is the NOT_CAPTURED sentinel renders
    blank with an "awaiting" flag, rather than showing the sentinel text in an
    input -- that phrasing is for read-only detail views, not form fields."""
    sections = []
    for key, title, label, fields in _COMPANY_SECTIONS:
        out_fields = []
        for flabel, fkey, required, help_text, span in fields:
            raw = company_record.get(fkey, "")
            awaiting = raw == NOT_CAPTURED
            out_fields.append(
                {
                    "key": fkey,
                    "label": flabel,
                    "value": "" if awaiting else raw,
                    "required": required,
                    "help": help_text,
                    "span": span,
                    "awaiting": awaiting,
                }
            )
        sections.append(
            {
                "key": key,
                "title": title,
                "label": label,
                "fields": out_fields,
                "hint": _COMPANY_SECTION_HINTS.get(key, ""),
            }
        )
    return sections


def company_completeness(sections):
    fields = [f for s in sections for f in s["fields"]]
    total = len(fields)
    filled = sum(1 for f in fields if not f["awaiting"])
    return {
        "total": total,
        "filled": filled,
        "pct": round(filled / total * 100) if total else 0,
    }


def company_fill_level(pct):
    if pct >= 80:
        return "good"
    if pct >= 55:
        return "mid"
    return "low"


def station_addresses():
    """Stations exist, but the client files carry no GPS or contact columns."""
    out = []
    for s in seed.STATIONS:
        out.append(
            {
                "station_no": s["code"],
                "branch": s["name"],
                "state": s["emirate"],
                "latitude": SHORT,
                "longitude": SHORT,
                "contact_no": SHORT,
                "status": "Pending",
            }
        )
    return out


DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
SHIFTS = [1, 2, 3, 4]

# Entities the FSD specifies but the client's two files contain no source for.
# These render an "awaiting data" state naming exactly what is needed.
def departments():
    """The department master (FSD 1.5).

    Empty, and deliberately so: the client has supplied no departments, and
    CLAUDE.md records that inventing them is not on the table. Everything that
    offers departments -- the Branch drawer's multi-select, Branch Department
    Mapping -- reads this, so all of them fill themselves the moment real
    departments arrive, and until then all of them say the same honest thing.
    """
    return []


AWAITING = {
    "locations": "locations",
    "departments": "departments",
    "branch_departments": "branch department mappings",
    "working_times": "working time schedules",
}

# FSD 1.9: seven permissions per screen, plus a Select All toggle.
PERMISSIONS = ["Access", "Create", "Read", "Update", "Print", "Approve", "Delete"]
