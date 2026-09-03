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
                "status": "Approved",
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
                "status": "Approved",
                "active": True,
            }
        )
    return out


def branches():
    """Each rental station is a branch hub (FSD 1.4: 'rental station branch hubs')."""
    out = []
    for s in seed.STATIONS:
        out.append(
            {
                "code": s["code"].replace("ST", "BR"),
                "name": s["name"],
                "company": "BYKY",
                "location": s["emirate"],
                "fleet": s["vehicle_count"],
                "is_ho": False,
                "multi_user": True,
                "hotel_commission": "0.00",
                "status": "Approved" if s["vehicle_count"] else "Pending",
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
        "state": "Dubai",
        "city": NOT_CAPTURED,
        "zip": NOT_CAPTURED,
        "inc_cert_no": NOT_CAPTURED,
        "income_tax_no": NOT_CAPTURED,
        "tax_pct": "0.00",
        "contact_person": NOT_CAPTURED,
        "phone": NOT_CAPTURED,
        "email": NOT_CAPTURED,
        "ceo_name": NOT_CAPTURED,
        "branches": len(st),
        "status": "Approved",
        "active": True,
    }


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
AWAITING = {
    "core_locations": "core locations",
    "departments": "departments",
    "branch_departments": "branch department mappings",
    "working_times": "working time schedules",
}

# FSD 1.9: seven permissions per screen, plus a Select All toggle.
PERMISSIONS = ["Access", "Create", "Read", "Update", "Print", "Approve", "Delete"]
