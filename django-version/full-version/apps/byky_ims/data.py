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
