"""Module 5 -- Tracking & Telematics.

Two screens run on real records: the fleet registry (1,060 vehicles) and the
vehicle type master (18 models). GPS/IoT hardware is not in the client files.

Antenna Registration, Antenna Branch Mapping, Branch-Vehicle-RFID Tag Mapping
and Antenna Tracking Monitor are FSD Module 8 (RFID & Hardware Antenna
System) screens, built here per the follow-up instruction to implement them
inside Vehicle Tracking Management instead. Two antenna gates (Entry/Exit)
per real station is a reasonable 1:1 assumption for the demo, the same
approach apps/byky_device/data.py uses for POS devices -- deterministic
(seeded on station code) so the numbers never jump between page loads.
RFID EPC codes are the client's own real Barcode column (already used for
this exact purpose on IMS's Vehicle Management/Station Mapping screens).
"""

import hashlib

from apps.byky_core import seed

SHORT = seed.NOT_CAPTURED_SHORT
PERMISSIONS = ["Access", "Create", "Read", "Update", "Approve", "Delete"]

AWAITING = {
    "devices": "registered devices",
    "gate_events": "live RFID gate read events",
}

# FSD 8.1 section 20.
GATE_DIRECTIONS = ["Entry", "Exit"]

# FSD 8.2 section 18 (ddlTagPosition).
TAG_POSITIONS = ["Front Frame", "Rear Axle", "Handlebar", "Under Seat"]


def _mac(seed_text):
    h = hashlib.md5(seed_text.encode()).hexdigest()[:12]
    return ":".join(h[i:i + 2] for i in range(0, 12, 2)).upper()


def antennas():
    """FSD 8.1 -- one Entry and one Exit gate antenna per real station. See
    module docstring for why this is populated rather than awaiting-data."""
    out = []
    aid = 1
    for i, st in enumerate(seed.STATIONS):
        for d_i, direction in enumerate(GATE_DIRECTIONS):
            seed_text = f"{st['code']}-{direction}"
            h = int(hashlib.md5(seed_text.encode()).hexdigest()[:6], 16)
            online = (i + d_i) % 4 != 0
            out.append(
                {
                    "id": aid,
                    "code": f"ANT-{st['code']}-{'IN' if direction == 'Entry' else 'OUT'}",
                    "name": f"{st['name']} Gate {direction}",
                    "branch": st["name"],
                    "ip": f"192.168.{(i % 50) + 1}.{100 + d_i}",
                    "port": 10001,
                    "mac": _mac(seed_text),
                    "direction": direction,
                    "rf_power": 18 + (h % 10),
                    "online": online,
                    "status": "Online" if online else "Offline",
                }
            )
            aid += 1
    return out


def antenna_counts(rows):
    return {
        "total": len(rows),
        "online": sum(1 for r in rows if r["online"]),
        "offline": sum(1 for r in rows if not r["online"]),
        "branches": len(seed.STATIONS),
    }


def vehicle_rfid_mappings():
    """FSD 8.2, reframed as Branch - Vehicle - RFID Tag Mapping per the
    follow-up instruction. Station, vehicle number and EPC (the client's
    Barcode column) are real; Tag Position and Encoded Date are not in the
    source files."""
    return [
        {
            "branch": v["station"],
            "vehicle_code": v["number"],
            "vehicle_name": f'{v["vtype"]} {v["number"]}',
            "epc": v["barcode"],
            "position": SHORT,
            "encoded_date": SHORT,
            "status": "Active",
        }
        for v in seed.VEHICLES
    ]


def fleet_registry():
    """FSD 5.2. Vehicle code and type are real; telemetry columns are not in source."""
    return [
        {
            "code": v["number"],
            "vtype": v["vtype"],
            "chassis": v["number"],
            "imei": SHORT,
            "speed_limit": SHORT,
            "battery": SHORT,
            "engine": "Unknown",
            "station": v["station"],
        }
        for v in seed.VEHICLES
    ]


def vehicle_types():
    """FSD 5.3. The 18 distinct models from the client's Vehicle Type column."""
    counts = {}
    for v in seed.VEHICLES:
        counts[v["vtype"]] = counts.get(v["vtype"], 0) + 1
    out = []
    for name, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        words = [w for w in name.split() if w]
        code = (words[0][:4] if len(words) == 1 else "".join(w[0] for w in words)[:4]).upper()
        out.append(
            {
                "code": code, "name": name, "fleet": n,
                "motor_watts": SHORT, "max_range": SHORT,
                "voltage": SHORT, "max_load": SHORT, "status": "Active",
            }
        )
    return out
