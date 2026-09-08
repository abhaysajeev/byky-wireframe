"""Live alert feed for the navbar bell.

The alert *types* are the ones the FSD actually names, not invented:

  FSD 3.19  Inventory System Alerts & Exception Monitoring
            Low Stock Level, Offline Antenna Sensor, Overdue Rental Return,
            Missing RFID Tag, Unauthorized Gate Clearance
  FSD 10.2  System Security Alert Dispatch & Monitoring
            Geofence Breach, Speeding Violation, Battery Depletion,
            RFID Siren Alarm, Low Hardware Storage
            -- and its severity scale: Critical / Warning / Info

Each alert is raised against a real station or vehicle from the client's own
data (seed.py), so nothing about the subject is fabricated.

What *is* simulated is the arrival: the wireframe has no live telemetry, so
byky-alerts.js replays this catalogue on a timer to demonstrate the alerting
behaviour. Every alert links to the FSD screen that owns it -- there is no
per-alert detail route, and inventing one would imply a screen the FSD does
not specify.
"""

import random

from apps.byky_core import seed

# Where each alert type is investigated. These are registered URL names.
IMS_ALERTS = "ims-inventory-system-alerts-exception-monitoring"
SECURITY_ALERTS = "notification-system-security-alert-dispatch-monitoring"
GATE_MONITOR = "rfid-rfid-gate-event-telemetry-security-monitor"
FLEET_REGISTRY = "tracking-vehicle-fleet-telematics-registry"


# (type, severity, subject, detail template, route)
# `{station}` and `{vehicle}` are filled from the real seed records.
CATALOGUE = [
    # -- FSD 3.19 -------------------------------------------------------
    ("Unauthorized Gate Clearance", "critical", "station",
     "Vehicle {vehicle} passed the gate at {station} without a valid rental.", GATE_MONITOR),
    ("Missing RFID Tag", "warning", "vehicle",
     "{vehicle} at {station} has not reported a tag read in 24 hours.", IMS_ALERTS),
    ("Offline Antenna Sensor", "critical", "station",
     "Gate antenna at {station} stopped responding to status checks.", GATE_MONITOR),
    ("Overdue Rental Return", "warning", "vehicle",
     "{vehicle} from {station} is past its expected return time.", IMS_ALERTS),
    ("Low Stock Level", "warning", "station",
     "{station} is below its minimum available fleet threshold.", IMS_ALERTS),
    # -- FSD 10.2 -------------------------------------------------------
    ("Geofence Breach", "critical", "vehicle",
     "{vehicle} left the permitted zone around {station}.", SECURITY_ALERTS),
    ("Speeding Violation", "warning", "vehicle",
     "{vehicle} exceeded the speed limit near {station}.", SECURITY_ALERTS),
    ("Battery Depletion", "warning", "vehicle",
     "{vehicle} at {station} reported a critically low battery.", FLEET_REGISTRY),
    ("RFID Siren Alarm", "critical", "station",
     "Siren triggered at {station} for an uncleared vehicle movement.", GATE_MONITOR),
    ("Low Hardware Storage", "info", "station",
     "Gate controller at {station} is running low on local storage.", SECURITY_ALERTS),
]


def feed(count=24, rng_seed=20260908):
    """A deterministic pool of alerts for the navbar to replay.

    Seeded so a walkthrough shows the same sequence twice running -- a demo
    that reshuffles on every reload is hard to talk over.
    """
    rng = random.Random(rng_seed)
    stations = [s for s in seed.STATIONS if s["vehicle_count"]]
    vehicles = seed.VEHICLES

    out = []
    for i in range(count):
        kind, severity, subject, template, route = CATALOGUE[i % len(CATALOGUE)]
        station = rng.choice(stations)
        vehicle = rng.choice([v for v in vehicles if v["station"] == station["name"]] or vehicles)

        out.append(
            {
                "id": i + 1,
                "title": kind,
                "severity": severity,
                "detail": template.format(station=station["name"], number=vehicle["number"],
                                          vehicle=vehicle["number"]),
                "subject": vehicle["number"] if subject == "vehicle" else station["name"],
                "station": station["name"],
                "route": route,
            }
        )

    rng.shuffle(out)
    return out
