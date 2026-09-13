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

Two separate device populations exist here, deliberately not cross-linked:

- devices() -- the already-approved, already-mapped fleet Device Mapping
  manages day to day. Its own "blocked" flag models an in-service device
  being suspended by an operator (Device Mapping's own Block/Unblock/Logout
  actions), not an approval decision.
- pending_devices() / approved_devices() / blocked_devices() -- a small
  onboarding queue for brand-new devices that have registered but aren't
  mapped to a station yet, which Device Approval's three tabs walk through
  (Pending -> Approved -> rarely Blocked). approved_devices() is also the
  pool Device Mapping's "Add Device Mapping" drawer offers, since only an
  approved-but-unmapped device is eligible to be mapped (row 50).
"""

import hashlib
import datetime

from apps.byky_core import seed

NOT_CAPTURED = seed.NOT_CAPTURED
SHORT = seed.NOT_CAPTURED_SHORT

APK_VERSION = "1.12.79"
APK_VERSION_PREV = "1.12.78"

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
                # An in-service device an operator has suspended -- separate
                # from the approval queue below (see module docstring).
                "blocked": i % 11 == 3,
            }
        )
    return out


def counts(rows):
    return {
        "total": len(rows),
        "online": sum(1 for r in rows if r["online"]),
        "offline": sum(1 for r in rows if not r["online"]),
        "blocked": sum(1 for r in rows if r["blocked"]),
        "stations": len(seed.STATIONS),
    }


def _queue_entry(i, status):
    today = datetime.date.today()
    registered = today - datetime.timedelta(days=(i * 5) % 45 + 1)
    return {
        # device_id/name give a queue device the same identity shape as an
        # already-mapped one (devices()), starting well past the mapped
        # fleet's own 1010x range (36 stations) so the two never collide --
        # needed once a device leaves the queue through Add Device Mapping
        # (row 50), which fills these straight from here.
        "device_id": 10200 + i,
        "name": f"Handheld Unit {i + 1}",
        "mac": _mac(f"queue-device-{i}"),
        "registered_at": (
            registered.strftime("%d/%m/%Y")
            + " " + f"{(8 + i) % 12 + 1:02d}:{(i * 17) % 60:02d} "
            + ("AM" if i % 2 == 0 else "PM")
        ),
        "status": status,
        # A generic login handle, not a real staff identity -- unlike
        # devices()' own `employee` field, this is whoever typed a username
        # into an unapproved device, so it stays anonymised rather than
        # naming real employees.
        "attempted_username": f"user{i + 1}",
        "apk_version": APK_VERSION if i % 2 == 0 else APK_VERSION_PREV,
    }


def pending_devices():
    """New handheld/POS units that have registered but not yet been
    reviewed -- an onboarding queue kept separate from the already-mapped
    devices() fleet (see module docstring)."""
    return [_queue_entry(i, "Pending") for i in range(0, 4)]


def approved_devices():
    """Queue devices cleared for use but not yet mapped to a station --
    the pool Device Mapping's Add Device Mapping drawer offers (row 50)."""
    return [_queue_entry(i, "Approved") for i in range(4, 7)]


def blocked_devices():
    """Queue devices that were approved and then blocked before ever being
    mapped."""
    return [_queue_entry(i, "Blocked") for i in range(7, 9)]


def queue_device_detail(mac):
    """A single queue device's full detail, across all three states, for
    Device Approval's detail page."""
    for d in pending_devices() + approved_devices() + blocked_devices():
        if d["mac"] == mac:
            return d
    return None


def queue_counts():
    return {
        "pending": len(pending_devices()),
        "approved": len(approved_devices()),
        "blocked": len(blocked_devices()),
    }


def device_settings():
    """One receipt/print settings record per real station (row 52 of the
    client's feedback doc) -- every station gets a row since the config
    screen is 1:1 with a station the same way devices() is, not something
    you create new instances of.

    Only operational defaults are pre-filled (paper feed, print type,
    round-off rule, test slot minutes) -- the same kind of constant every
    other device gets (APK_VERSION above). The client-specific business
    copy (header/footer text, order-number prefix, logo) has no source
    anywhere, so it renders not-captured rather than invented, exactly
    like the single-form screen this replaces always left it blank.
    """
    out = []
    for i, st in enumerate(seed.STATIONS):
        out.append(
            {
                "station": st["name"],
                "station_code": st["code"],
                "company": "BYKY",
                "settings_code": f"stn-{st['code'].lower()}",
                "header1": "",
                "header2": "",
                "additional_header2": "",
                "footer1": "",
                "footer2": "",
                "print_logo": False,
                "paper_feed": PRINT_FEED_OPTIONS[0],
                "receipt_copies": 1,
                "print_type": PRINT_TYPE_OPTIONS[0],
                "order_no_prefix": "",
                "customer_test_slot": 5,
                "cashier_test_slot": 5,
                "tax_type": TAX_TYPE_OPTIONS[0],
                "round_off_type": "Nearest",
                "round_off_limit": "25 Fils",
                "approval_status": APPROVAL_STATUSES[i % 3] if i % 5 else "Approved",
            }
        )
    return out


def device_settings_counts(rows):
    return {
        "total": len(rows),
        "approved": sum(1 for r in rows if r["approval_status"] == "Approved"),
        "pending": sum(1 for r in rows if r["approval_status"] == "Pending"),
        "rejected": sum(1 for r in rows if r["approval_status"] == "Rejected"),
    }
