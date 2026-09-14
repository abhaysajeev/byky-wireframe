"""Reference data for Fare & Schemes.

Both screens come from client-supplied HTML mockups (byky Docs/
Fare_Entry_Advanced_UI_v3.html and Scheme_Creation.html) rather than from the
FSD, so the field lists here mirror those mockups exactly.

Dropdown options that describe real BYKY inventory are pulled from the seed data;
the rest are the fixed enumerations the mockups define.
"""

from apps.byky_core import seed
from apps.byky_cms import data as cms_data

PRICE_LEVELS = ["Company", "Branch", "Location"]
FARE_STATUS = ["Active", "Inactive"]

DAYS = ["All Days", "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"]

PROMOTION_FOR = ["Value", "Quantity"]
INVENTORY_TYPES = ["Vehicle", "Accessory", "Both"]
PROMOTION_TYPES = ["Free Item", "Discount", "Buy X Get Y"]

# Package durations the client's mockup uses as examples.
PACKAGE_TIMES = [15, 30, 45, 60, 90, 120]


def categories():
    return seed.CATEGORIES


def vehicle_types():
    return seed.VEHICLE_TYPES


def companies():
    return ["BYKY"]


# ---------------------------------------------------------------------------
# Fare list (client feedback: Fare Entry needed a list view like every other
# module instead of opening straight on the create form). Deterministic demo
# rows -- same spirit as this app's other wireframe demo data (e.g.
# apps/byky_device's demo MAC addresses): real categories/vehicle types/
# branches, openly-fabricated fare amounts and codes, never claimed as real
# client pricing.
# ---------------------------------------------------------------------------

def fares():
    cats = categories()
    types = vehicle_types()
    branches = [b["name"] for b in cms_data.branches()]
    rows = [
        {
            "code": "FAR-2026-001",
            "price_level": "Company",
            "scope": "BYKY",
            "branches": [],
            "category": cats[0] if cats else "",
            "vehicle_type": types[0] if types else "",
            "from_date": "01 Jan 2026",
            "to_date": "31 Dec 2026",
            "tax_pct": 5,
            "status": "Active",
            "package_time": 30,
            "basic_fare": 100,
        },
        {
            "code": "FAR-2026-002",
            "price_level": "Branch",
            "scope": "BYKY",
            "branches": branches[:2],
            "category": cats[1] if len(cats) > 1 else (cats[0] if cats else ""),
            "vehicle_type": types[1] if len(types) > 1 else (types[0] if types else ""),
            "from_date": "01 Mar 2026",
            "to_date": "30 Sep 2026",
            "tax_pct": 5,
            "status": "Active",
            "package_time": 45,
            "basic_fare": 130,
        },
        {
            "code": "FAR-2026-003",
            "price_level": "Branch",
            "scope": "BYKY",
            "branches": branches[2:5],
            "category": cats[2] if len(cats) > 2 else (cats[0] if cats else ""),
            "vehicle_type": types[2] if len(types) > 2 else (types[0] if types else ""),
            "from_date": "01 Jun 2025",
            "to_date": "31 May 2026",
            "tax_pct": 5,
            "status": "Inactive",
            "package_time": 60,
            "basic_fare": 150,
        },
    ]
    return rows


def fare_by_code(code):
    for f in fares():
        if f["code"] == code:
            return f
    return None


def fare_counts(rows):
    return {
        "total": len(rows),
        "active": sum(1 for r in rows if r["status"] == "Active"),
        "inactive": sum(1 for r in rows if r["status"] == "Inactive"),
    }
