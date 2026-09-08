"""Display data for Live Monitoring -- a new module requested against the
client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Live Monitor" /
"Search Order" / "Image Sharing" pages), not one of the 16 FSD modules.
Wireframe phase: no writes, no CRUD, no API.

Live Monitor and Search Order are live rental-transaction feeds -- order
numbers, customer names, fare/deposit/tax amounts. Nothing in the client's
source files supplies real transactions (Customer Details & Registration is
itself still awaiting client data, per apps/byky_rms), so inventing sample
orders here would mean inventing money figures, which CLAUDE.md section 12
is explicit about never doing. Both screens therefore render their real
filters, tabs and column headers with the awaiting-data state in the body,
the same treatment already used for IMS's Live RFID Monitoring and
Inventory System Alerts screens.

Image Sharing carries no money and ties naturally to real stations and
staff, so it is populated the same way Device Mapping is: real station and
employee names, deterministic (seeded) so the numbers never jump between
page loads.
"""

import hashlib

from apps.byky_core import seed

ORDER_STATUSES = ["Running", "Received", "Cancelled"]

IMAGE_APPROVAL_STATUSES = ["Approved", "Not Approved", "Rejected"]


def shared_images():
    """Deterministic demo rows: a photo shared from a real station by a real
    staff member, awaiting review. See module docstring -- no money involved,
    so this one is populated rather than left as an awaiting-data screen."""
    out = []
    for i, st in enumerate(seed.STATIONS[:10]):
        emp = seed.EMPLOYEES[(i * 7) % len(seed.EMPLOYEES)]
        h = hashlib.md5(st["code"].encode()).hexdigest()
        out.append(
            {
                "id": i + 1,
                "branch": st["name"],
                "shared_by": f'{emp["name"]} ({emp["emp_no"]})',
                "remarks": "",
                "status": IMAGE_APPROVAL_STATUSES[int(h[:2], 16) % 3],
            }
        )
    return out


def counts(images):
    return {
        "total": len(images),
        "approved": sum(1 for i in images if i["status"] == "Approved"),
        "pending": sum(1 for i in images if i["status"] == "Not Approved"),
        "rejected": sum(1 for i in images if i["status"] == "Rejected"),
    }
