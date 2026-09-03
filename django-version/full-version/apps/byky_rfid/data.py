"""Module 8 -- RFID Gates.

The client's Barcode column is the RFID tag EPC, so tag-to-vehicle mapping (8.2)
is real for all 1,060 units. Antennas, calibration and read telemetry are not in
the source files.
"""

from apps.byky_core import seed

SHORT = seed.NOT_CAPTURED_SHORT
PERMISSIONS = ["Access", "Create", "Read", "Update", "Approve"]

AWAITING = {
    "antennas": "antennas",
    "calibration": "calibration records",
    "events": "gate events",
}


def tag_mappings():
    """FSD 8.2. Every vehicle already carries an EPC in the client data."""
    return [
        {
            "code": v["number"],
            "name": f'{v["vtype"]} {v["number"]}',
            "epc": v["barcode"],
            "position": SHORT,
            "encoded": SHORT,
            "station": v["station"],
            "status": "Active",
        }
        for v in seed.VEHICLES
    ]
