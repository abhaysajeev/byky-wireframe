"""Display data for Module 3 (IMS -- Inventory).

The client's VehicleDetails sheet is a genuine inventory extract, so several IMS
screens run on real records:

  Stock Item (3.1)       1,060 vehicles -- Vehicle Number is the item code and
                         serial, Barcode is the RFID tag EPC
  Category (3.2)         8 real categories
  Sub-Category (3.3)     18 real vehicle types, parented to their category
  Station Mapping (3.6)  1,060 real vehicle-to-station assignments

The rest of the module (brands, units, transfers, e-commerce, promotions, loyalty,
refunds, campaigns, telemetry, alerts) has no source in the client files and shows
the awaiting-data state rather than invented rows.
"""

from apps.byky_core import seed

NOT_CAPTURED = seed.NOT_CAPTURED
SHORT = seed.NOT_CAPTURED_SHORT

# FSD 3.20: six permission flags per row.
PERMISSIONS = ["Access", "Create", "Read", "Update", "Approve", "Delete"]

AWAITING = {
    "brands": "brands",
    "units": "units of measure",
    "transfers": "vehicle transfers",
    "ecom_categories": "e-commerce categories",
    "ecom_items": "catalog entries",
    "features": "features",
    "order_status": "order statuses",
    "promos": "promo codes",
    "loyalty_tiers": "loyalty tiers",
    "loyalty_redeem": "redemption profiles",
    "refunds": "refund claims",
    "newsletter": "newsletter dispatches",
    "push": "push dispatches",
    "rfid_reads": "gate read events",
    "alerts": "alerts",
}


def _code(text, n=4):
    words = [w for w in str(text).replace("/", " ").split() if w]
    if len(words) == 1:
        return words[0][:n].upper()
    return "".join(w[0] for w in words)[:n].upper()


def categories():
    agg = {}
    for v in seed.VEHICLES:
        agg.setdefault(v["category"], {"count": 0, "types": set()})
        agg[v["category"]]["count"] += 1
        agg[v["category"]]["types"].add(v["vtype"])
    out = []
    for name, d in sorted(agg.items(), key=lambda kv: -kv[1]["count"]):
        out.append(
            {
                "code": _code(name),
                "name": name,
                "description": SHORT,
                "items": d["count"],
                "subcategories": len(d["types"]),
                "status": "Active",
            }
        )
    return out


def subcategories():
    """Vehicle types, parented to the category they appear under."""
    agg = {}
    for v in seed.VEHICLES:
        key = (v["category"], v["vtype"])
        agg[key] = agg.get(key, 0) + 1
    out = []
    for (cat, vtype), n in sorted(agg.items(), key=lambda kv: -kv[1]):
        out.append(
            {
                "code": _code(vtype),
                "name": vtype,
                "parent": cat,
                "description": SHORT,
                "items": n,
                "status": "Active",
            }
        )
    return out


def stock_items():
    """One row per vehicle. Rates, cost and reorder levels are not in the source."""
    out = []
    for v in seed.VEHICLES:
        out.append(
            {
                "code": v["number"],
                "name": f'{v["vtype"]} {v["number"]}',
                "category": v["category"],
                "subcategory": v["vtype"],
                "serial": v["number"],
                "rfid": v["barcode"],
                "station": v["station"],
                "brand": SHORT,
                "unit": SHORT,
                "rate": SHORT,
                "qty": 1,
                "status": "Approved",
            }
        )
    return out


def station_mappings():
    out = []
    for v in seed.VEHICLES:
        out.append(
            {
                "branch": v["station"],
                "code": v["number"],
                "name": f'{v["vtype"]} {v["number"]}',
                "serial": v["number"],
                "rfid": v["barcode"],
                "mapped_date": SHORT,
            }
        )
    return out


def unmapped_vehicles():
    """Vehicles with no branch/station assignment yet -- the pool FSD 3.6's
    "Map Vehicle" action assigns to a branch. Every vehicle in the source
    data already carries a real station (see station_mappings() above), so
    this is honestly empty today; the logic is real and will surface genuine
    rows the moment an unassigned vehicle enters the fleet, rather than this
    screen ever inventing one to demo against (CLAUDE.md 12)."""
    out = []
    for v in seed.VEHICLES:
        if v.get("station"):
            continue
        out.append(
            {
                "code": v["number"],
                "name": f'{v["vtype"]} {v["number"]}',
                "rfid": v["barcode"],
                "category": v["category"],
            }
        )
    return out


def counts():
    return {
        "items": len(seed.VEHICLES),
        "categories": len(seed.CATEGORIES),
        "subcategories": len(seed.VEHICLE_TYPES),
        "tagged": sum(1 for v in seed.VEHICLES if v["barcode"]),
        "stations": len(seed.STATIONS),
    }


# --- Asset Management ------------------------------------------------------
#
# The FSD has no standalone asset screen: physical assets live in
# tbl_ItemMaster alongside rental stock (FSD 3.1), and FSD 3.2 is what
# classifies them -- "top-level asset classifications (e.g., Bicycles,
# E-Scooters, Quad Bikes, Spare Parts, Helmets, Maintenance Tools)". This
# screen is the custody and lifecycle view of that same register -- where an
# asset physically sits, who holds it, what it cost, when its warranty lapses
# -- where Vehicle Management (3.1) is the catalogue view of it.
#
# ASSET_CLASSES is dropdown vocabulary lifted from FSD 3.2's own examples and
# the module overview's asset list, not client records. Fleet Vehicle is the
# only class the client has supplied rows for (the 1,060-row VehicleDetails
# extract); the rest stay visible in the filter so the gap is legible.
ASSET_CLASSES = [
    "Fleet Vehicle",
    "Spare Part",
    "Safety Equipment",
    "Maintenance Tool",
    "RFID Hardware",
    "Station Equipment",
]

ASSET_CONDITIONS = ["New", "Good", "Fair", "Needs Repair", "Retired"]


def assets():
    """One row per physical asset the business holds.

    Every value shown is derived from the client's own vehicle extract.
    Custodian, acquisition date, purchase cost, warranty and condition are in
    no supplied file, so they render short-form blank rather than invented
    values (CLAUDE.md 12). Assignment is genuinely derivable -- an asset
    either carries a station in the source data or it does not.
    """
    out = []
    for v in seed.VEHICLES:
        station = v.get("station") or ""
        out.append(
            {
                "code": v["number"],
                "name": f'{v["vtype"]} {v["number"]}',
                "asset_class": "Fleet Vehicle",
                "category": v["category"],
                "subcategory": v["vtype"],
                "serial": v["number"],
                "rfid": v["barcode"],
                "station": station or SHORT,
                "station_key": station,
                "custodian": SHORT,
                "acquired": SHORT,
                "cost": SHORT,
                "warranty": SHORT,
                "condition": SHORT,
                "assignment": "Assigned" if station else "Unassigned",
            }
        )
    return out


def asset_counts():
    rows = assets()
    return {
        "total": len(rows),
        "classes_in_use": len({r["asset_class"] for r in rows}),
        "classes_defined": len(ASSET_CLASSES),
        "tagged": sum(1 for r in rows if r["rfid"]),
        "unassigned": sum(1 for r in rows if r["assignment"] == "Unassigned"),
        "custody_stations": len({r["station_key"] for r in rows if r["station_key"]}),
    }
