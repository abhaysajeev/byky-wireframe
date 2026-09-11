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


# Demo brands. A narrow, explicit, user-requested exception to the
# no-invented-data rule (CLAUDE.md 12): the client has supplied no brand
# list, and this master otherwise has nothing to show against. Website is
# left NOT_CAPTURED rather than invented -- only the two names and codes
# were actually asked for.
#
# Replace this list with the client's own the moment it arrives; nothing else
# needs to change, because every screen that offers brands reads brands()
# rather than holding its own copy.
_DEMO_BRANDS = [
    ("BERG", "Berg"),
    ("ESCO", "E Scooter"),
]


def brands():
    """The brand master (FSD 3.4)."""
    return [
        {
            "code": code,
            "name": name,
            "website": NOT_CAPTURED,
            "active": True,
            "status": "Active",
        }
        for code, name in _DEMO_BRANDS
    ]


# Demo units of measure. A narrow, explicit, user-requested exception to the
# no-invented-data rule (CLAUDE.md 12): the client has supplied no UOM list,
# and this master otherwise has nothing to show against.
#
# Replace this list with the client's own the moment it arrives; nothing else
# needs to change, because every screen that offers units reads units()
# rather than holding its own copy.
_DEMO_UNITS = [
    ("NOS", "Nos"),
]


def units():
    """The unit of measure master (FSD 3.5). Whole-count items -- no decimal
    quantities -- so Allow Decimal defaults to No."""
    return [
        {
            "code": code,
            "name": name,
            "allow_decimal": False,
            "active": True,
            "status": "Active",
        }
        for code, name in _DEMO_UNITS
    ]


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
                "status": "Active",
            }
        )
    return out


def station_mappings():
    """Everything a branch holds, vehicles and company assets together.

    Each row carries item_type so the screen can show them in one grid and
    filter to either. Only vehicles have rows today -- the asset register is
    empty -- so the Assets view of this list is honestly blank rather than
    padded out.
    """
    out = []
    for v in seed.VEHICLES:
        out.append(
            {
                "item_type": "Vehicle",
                "branch": v["station"],
                "code": v["number"],
                "name": f'{v["vtype"]} {v["number"]}',
                "serial": v["number"],
                "rfid": v["barcode"],
                "mapped_date": SHORT,
            }
        )
    for a in assets():
        if not a.get("station_key"):
            continue
        out.append(
            {
                "item_type": "Asset",
                "branch": a["station_key"],
                "code": a["code"],
                "name": a["name"],
                "serial": a["serial"],
                "rfid": a["identifier"],
                "mapped_date": SHORT,
            }
        )
    return out


ITEM_TYPES = ["Vehicle", "Asset"]

# --- Transfer & Return -----------------------------------------------------

# FSD 3.7's movement reasons, as the client listed them.
TRANSFER_TYPES = [
    "Branch to Branch",
    "To Maintenance",
    "To Storage",
    "Dismissed",
    "To Events",
]

# Which extra destination field each transfer type asks for. Kept here rather
# than in the template so the form and any later validation read the same list.
TRANSFER_DESTINATION = {
    "Branch to Branch": "to_branch",
    "To Maintenance": "to_warehouse",
    "To Storage": "to_warehouse",
    "Dismissed": "to_warehouse",
    "To Events": "event_location",
}


# A return comes back FROM somewhere, so it has its own short list rather than
# reusing the transfer reasons -- there is no "return from branch to branch".
RETURN_TYPES = ["From Maintenance", "From Storage", "From Events"]

RETURN_SOURCE = {
    "From Maintenance": "from_warehouse",
    "From Storage": "from_warehouse",
    "From Events": "from_event_location",
}


def returnable_items():
    """Everything currently sitting in a warehouse or at an event -- the pool
    a return brings back.

    An item is returnable exactly when it is not at a branch. Nothing is today:
    no branch is registered as a warehouse, no event venue exists, and every
    vehicle in the client's data sits at a station. Real logic over real data,
    so it fills itself rather than being seeded (CLAUDE.md 12).
    """
    branch_names = {b["name"] for b in warehouses()}
    return [i for i in transferable_items() if i["branch"] in branch_names]


def warehouses():
    """Branches that are warehouses -- the destinations for maintenance,
    storage and dismissal.

    Derived from the branch master's own type, so it fills itself the moment a
    branch is registered as a warehouse. Empty today: all 36 stations in the
    client's data are Branch Offices.
    """
    from apps.byky_cms import data as cms_data

    return [b for b in cms_data.branches() if "Warehouse" in b.get("branch_type", "")]


def event_locations():
    """Venues a vehicle can be sent to for an event. No source data yet."""
    return []


def transferable_items():
    """Everything currently held at a branch, vehicles and assets alike --
    the pool a transfer picks from. Carries the columns the grid filters on."""
    out = []
    for v in seed.VEHICLES:
        out.append(
            {
                "item_type": "Vehicle",
                "branch": v["station"],
                "code": v["number"],
                "name": f'{v["vtype"]} {v["number"]}',
                "category": v["category"],
                "vtype": v["vtype"],
                "rfid": v["barcode"],
            }
        )
    for a in assets():
        if not a.get("station_key"):
            continue
        out.append(
            {
                "item_type": "Asset",
                "branch": a["station_key"],
                "code": a["code"],
                "name": a["name"],
                "category": a["asset_class"],
                "vtype": a["type"] if a.get("type") else SHORT,
                "rfid": a["identifier"],
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
# The type catalogue below is derived from the hardware the rest of the system
# already specifies, not invented -- the per-entry comments record where each
# one comes from so the list stays auditable. That provenance is deliberately
# NOT rendered: it is build metadata, and a client-facing screen has no reason
# to carry spec references (same rule as the legacy .aspx filenames).
#
# What the spec does not pin down -- how many units exist, their serials,
# custodians, costs -- stays empty until the client supplies it (CLAUDE.md 12).

ASSET_CLASSES = [
    "RFID Hardware",
    "Telematics Device",
    "Counter Equipment",
    "IT & Network",
    "Site Security",
    "Workshop & Safety",
]

ASSET_CONDITIONS = ["New", "Good", "Fair", "Needs Repair", "Retired"]

# code, type, class, the identifier a unit is looked up by, where it is
# deployed. Codes are written out rather than derived from the name -- the
# initialism collided ("Cellular SIM Card" and "CCTV Surveillance Camera" both
# reduce to CSC) and an ampersand leaked into one, which is not something a
# master-table code should ever carry.
#
# Trailing comment on each row is its provenance, kept for maintainers only.
_ASSET_TYPES = [
    ("ANT", "UHF RFID Gate Antenna", "RFID Hardware", "Antenna Code · IP · MAC",
     "Station gate"),                        # 8.1 tbl_AntennaMaster
    ("RDR", "UHF RFID Reader Unit", "RFID Hardware", "Reader IP · TCP port",
     "Station gate"),                        # 8.1 reader IP / port
    ("RSC", "RFID Desktop Card Scanner", "RFID Hardware", "Asset tag",
     "Station counter"),                     # 4.2 tap card on RFID scanner
    ("GPS", "GPS / IoT Tracker Unit", "Telematics Device", "IMEI · Serial No",
     "Fitted to vehicle"),                   # 5.1 tbl_GPSDeviceMaster
    ("SIM", "Cellular SIM Card", "Telematics Device", "MSISDN · Carrier",
     "Fitted in tracker"),                   # 5.1 SIM MSISDN / carrier
    ("RLY", "Relay Immobilizer Kit", "Telematics Device", "Asset tag",
     "Fitted to vehicle"),                   # 5.1 relay kill switch
    ("HHD", "Staff Handheld Device", "Counter Equipment", "IMEI · Asset tag",
     "Station staff"),                       # 9.6 camera document capture
    ("BCS", "Barcode Scanner", "Counter Equipment", "Asset tag",
     "Station counter"),                     # 4.6 barcode scanner input
    ("POS", "POS Checkout Terminal", "Counter Equipment", "Asset tag",
     "Station counter"),                     # 4.6 station POS checkout
    ("PRN", "Receipt & Invoice Printer", "Counter Equipment", "Asset tag",
     "Station counter"),                     # 4.6 printed invoice
    ("NET", "Network Router / Switch", "IT & Network", "IP · MAC",
     "Station back office"),                 # 8.1 reader LAN addressing
    ("CCTV", "CCTV Surveillance Camera", "Site Security", "Asset tag · IP",
     "Station forecourt"),                   # client-named
    ("TKIT", "Maintenance Tool Kit", "Workshop & Safety", "Asset tag",
     "Workshop"),                            # 3.2 maintenance tools
    ("HLMT", "Safety Helmet Stock", "Workshop & Safety", "Asset tag",
     "Station counter"),                     # 3.2 helmets
]


def asset_types():
    """The catalogue of equipment kinds the business operates.

    Real content, derived from the hardware the rest of the system specifies
    (see _ASSET_TYPES). Unit counts are zero across the board because no
    equipment inventory has been supplied -- the catalogue is what the system
    knows about, not what it owns.
    """
    out = []
    for code, name, cls, identifier, location in _ASSET_TYPES:
        out.append(
            {
                "code": code,
                "name": name,
                "asset_class": cls,
                "identifier": identifier,
                "location": location,
                "units": 0,
                "status": "Active",
            }
        )
    return out


# One demo unit, explicitly requested so the register isn't permanently
# empty for a walkthrough (CLAUDE.md 12's narrow, explicit exception). Class,
# type, station and custodian all resolve to real options this screen already
# offers (Site Security / CCTV Surveillance Camera from _ASSET_TYPES, "Creek
# Park Gate 1" and "Don Bosco Cyril Cyril" from the real station/staff
# lists) -- only the unit-specific values (tag, serial, IP/MAC/IMEI, cost,
# dates) are the requested sample.
_DEMO_ASSETS = [
    {
        "code": "EC001",
        "name": "CCTV 4G GPRS",
        "asset_class": "Site Security",
        "type": "CCTV Surveillance Camera",
        "material_type": "Electronics",
        "model": "Hikvision",
        "serial": "C123456",
        "station": "Creek Park Gate 1",
        "custodian": "Don Bosco Cyril Cyril",
        "ip": "192.168.0.1",
        "mac": "aa:bb:cc:dd",
        "imei": "0123456789",
        "msisdn": "0123456789",
        "acquired": "01 Jan 2026",
        "cost": "1250.00",
        "supplier": "DSTME",
        "warranty_from": "01 Jan 2026",
        "warranty_to": "31 Dec 2026",
        "condition": "New",
        "notes": "Installed on 03/05/2026",
    },
]


def assets():
    """Individual equipment units on the register.

    Otherwise honestly empty: the client's files cover vehicles and staff
    only, and no antenna, tracker, terminal or camera inventory has been
    supplied. See _DEMO_ASSETS above for the one requested exception. The
    grid still renders its real columns so the client can see the shape of
    what is being asked for, and the drawer is live so a unit can be walked
    through end to end in a demo.
    """
    return [dict(a) for a in _DEMO_ASSETS]


def unmapped_assets():
    """Assets registered but not yet posted to a branch -- the pool the
    Map Asset page assigns from.

    Mirrors unmapped_vehicles(): real logic over the real register, which is
    empty today, so the page shows an honest empty state rather than invented
    equipment (CLAUDE.md 12).
    """
    return [
        {
            "code": a["code"],
            "name": a["name"],
            "asset_class": a["asset_class"],
            "identifier": a["identifier"],
        }
        for a in assets()
        if not a.get("station_key")
    ]


def asset_counts():
    types = asset_types()
    rows = assets()
    return {
        "types": len(types),
        "classes": len({t["asset_class"] for t in types}),
        "registered": len(rows),
        # Assets actually posted to a branch, as opposed to registered but
        # unassigned. Real arithmetic over an empty register today, so it
        # reads 0 -- it will move on its own once equipment is supplied.
        "mapped": sum(1 for r in rows if r.get("station_key")),
        "stations": len(seed.STATIONS),
    }
