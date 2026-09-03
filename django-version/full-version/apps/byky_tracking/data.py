"""Module 5 -- Tracking & Telematics.

Two screens run on real records: the fleet registry (1,060 vehicles) and the
vehicle type master (18 models). GPS/IoT hardware is not in the client files.
"""

from apps.byky_core import seed

SHORT = seed.NOT_CAPTURED_SHORT
PERMISSIONS = ["Access", "Create", "Read", "Update", "Approve", "Delete"]

AWAITING = {
    "devices": "registered devices",
}


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
