"""Display data for Device Management -- a new module requested against the
client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Device Management"
page), not one of the 16 FSD modules. Wireframe phase: no writes, no CRUD,
no API.

One handheld/POS device per station is a reasonable 1:1 assumption for the
demo -- every station in the real network gets a device row, deterministic
(seeded on station code) so the numbers never jump between page loads, the
same approach apps/byky_core/sales.py uses for indicative revenue. MAC
addresses, APK versions and login timestamps are demo values in the same
spirit; they are not claimed to be real client hardware.
"""

import hashlib
import datetime

from apps.byky_core import seed

NOT_CAPTURED = seed.NOT_CAPTURED
SHORT = seed.NOT_CAPTURED_SHORT

APK_VERSION = "1.12.79"

PRINT_FEED_OPTIONS = ["1", "2", "3"]
PRINT_TYPE_OPTIONS = ["Portrait", "Landscape"]
TAX_TYPE_OPTIONS = ["Included in Basic Fare", "Excluded from Basic Fare"]
ROUND_OFF_OPTIONS = ["Upward", "Downward", "Nearest"]
ROUND_OFF_LIMITS = ["5 Fils", "25 Fils", "50 Fils", "1 AED"]

APPROVAL_STATUSES = ["Approved", "Pending", "Rejected"]


def _mac(seed_text):
    h = hashlib.md5(seed_text.encode()).hexdigest()[:12]
    return ":".join(h[i:i + 2] for i in range(0, 12, 2)).upper()


def _device_id(i):
    return 10100 + i


def devices():
    """One device per real station -- code, MAC and login state are demo
    values (see module docstring), the station itself is not."""
    out = []
    today = datetime.date.today()
    for i, st in enumerate(seed.STATIONS):
        online = i % 3 == 0
        emp = seed.EMPLOYEES[i % len(seed.EMPLOYEES)] if online else None
        from_date = today - datetime.timedelta(days=(i * 11) % 700 + 30)
        out.append(
            {
                "device_id": _device_id(i),
                "name": st["name"],
                "mac": _mac(st["code"]),
                "station": st["name"],
                "station_code": st["code"],
                "apk_version": APK_VERSION,
                "from_date": from_date.strftime("%d/%m/%Y"),
                "login_time": (
                    (today - datetime.timedelta(days=i % 5)).strftime("%d/%m/%Y")
                    + " " + f"{(6 + i) % 12 + 1:02d}:{(i * 7) % 60:02d} "
                    + ("AM" if i % 2 == 0 else "PM")
                ) if online else "",
                "employee": emp["name"] + f" ({emp['emp_no']})" if emp else "",
                "online": online,
                "approval_status": APPROVAL_STATUSES[i % 3] if i % 5 else "Approved",
            }
        )
    return out


def counts(rows):
    return {
        "total": len(rows),
        "online": sum(1 for r in rows if r["online"]),
        "offline": sum(1 for r in rows if not r["online"]),
        "stations": len(seed.STATIONS),
    }
