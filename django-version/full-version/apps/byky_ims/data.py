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
# Company-owned operating equipment ONLY -- antennas, readers, trackers, SIMs,
# counter hardware, cameras, tools. Rental stock (the 1,060 vehicles) belongs
# to Vehicle Management (FSD 3.1) and must never be duplicated here: the two
# screens answer different questions, and a vehicle appearing in both is the
# defect this split exists to prevent.
#
# The FSD has no asset-management screen, but it does specify the hardware
# itself in detail, so the type catalogue below is derived, not invented. Each
# entry records where it comes from, and "source" says how firmly:
#
#   specified  the FSD masters this device in its own table/screen
#   implied    an FSD screen depends on the device but never masters it
#   client     named by the client, outside the FSD
#
# That column is the honest part. Everything the FSD does not pin down --
# how many units exist, their serials, custodians, costs -- stays empty until
# the client supplies it (CLAUDE.md 12).

ASSET_CLASSES = [
    "RFID Hardware",
    "Telematics Device",
    "Counter Equipment",
    "IT & Network",
    "Site Security",
    "Workshop & Safety",
]

ASSET_SOURCES = {
    "specified": "FSD-specified",
    "implied": "FSD-implied",
    "client": "Client-named",
}

ASSET_CONDITIONS = ["New", "Good", "Fair", "Needs Repair", "Retired"]

# code, type, class, the identifier the FSD tracks it by, where it lives,
# source, spec reference. Codes are written out rather than derived from the
# name -- initialism collided ("Cellular SIM Card" and "CCTV Surveillance
# Camera" both reduce to CSC) and an ampersand leaked into one, which is not
# something a master-table code should ever carry.
_ASSET_TYPES = [
    ("ANT", "UHF RFID Gate Antenna", "RFID Hardware", "Antenna Code · IP · MAC",
     "Station gate", "specified", "FSD 8.1 · tbl_AntennaMaster"),
    ("RDR", "UHF RFID Reader Unit", "RFID Hardware", "Reader IP · TCP port",
     "Station gate", "specified", "FSD 8.1 · Reader IP / Port"),
    ("RSC", "RFID Desktop Card Scanner", "RFID Hardware", "Asset tag",
     "Station counter", "implied", "FSD 4.2 · Tap card on RFID scanner"),
    ("GPS", "GPS / IoT Tracker Unit", "Telematics Device", "IMEI · Serial No",
     "Fitted to vehicle", "specified", "FSD 5.1 · tbl_GPSDeviceMaster"),
    ("SIM", "Cellular SIM Card", "Telematics Device", "MSISDN · Carrier",
     "Fitted in tracker", "specified", "FSD 5.1 · SIM MSISDN / Carrier"),
    ("RLY", "Relay Immobilizer Kit", "Telematics Device", "Asset tag",
     "Fitted to vehicle", "specified", "FSD 5.1 · Relay kill switch"),
    ("HHD", "Staff Handheld Device", "Counter Equipment", "IMEI · Asset tag",
     "Station staff", "implied", "FSD 9.6 · Camera document capture"),
    ("BCS", "Barcode Scanner", "Counter Equipment", "Asset tag",
     "Station counter", "implied", "FSD 4.6 · Barcode scanner input"),
    ("POS", "POS Checkout Terminal", "Counter Equipment", "Asset tag",
     "Station counter", "implied", "FSD 4.6 · Station POS checkout"),
    ("PRN", "Receipt & Invoice Printer", "Counter Equipment", "Asset tag",
     "Station counter", "implied", "FSD 4.6 · Printed invoice"),
    ("NET", "Network Router / Switch", "IT & Network", "IP · MAC",
     "Station back office", "implied", "FSD 8.1 · Reader LAN addressing"),
    ("CCTV", "CCTV Surveillance Camera", "Site Security", "Asset tag · IP",
     "Station forecourt", "client", "Client-named — no FSD screen"),
    ("TKIT", "Maintenance Tool Kit", "Workshop & Safety", "Asset tag",
     "Workshop", "specified", "FSD 3.2 · Maintenance Tools"),
    ("HLMT", "Safety Helmet Stock", "Workshop & Safety", "Asset tag",
     "Station counter", "specified", "FSD 3.2 · Helmets"),
]


def asset_types():
    """The catalogue of equipment kinds the business operates.

    Real content, derived from the FSD hardware specs (see _ASSET_TYPES). Unit
    counts are zero across the board because no equipment inventory has been
    supplied -- the catalogue is what the system knows, not what it owns.
    """
    out = []
    for code, name, cls, identifier, location, source, ref in _ASSET_TYPES:
        out.append(
            {
                "code": code,
                "name": name,
                "asset_class": cls,
                "identifier": identifier,
                "location": location,
                "source": source,
                "source_label": ASSET_SOURCES[source],
                "reference": ref,
                "units": 0,
                "status": "Active",
            }
        )
    return out


def assets():
    """Individual equipment units on the register.

    Honestly empty: the client's files cover vehicles and staff only, and no
    antenna, tracker, terminal or camera inventory has been supplied. The
    grid still renders its real columns so the client can see the shape of
    what is being asked for, and the drawer is live so a unit can be walked
    through end to end in a demo. Never seed this with invented serials.
    """
    return []


def asset_counts():
    types = asset_types()
    rows = assets()
    return {
        "types": len(types),
        "classes": len({t["asset_class"] for t in types}),
        "specified": sum(1 for t in types if t["source"] == "specified"),
        "registered": len(rows),
        "stations": len(seed.STATIONS),
    }
