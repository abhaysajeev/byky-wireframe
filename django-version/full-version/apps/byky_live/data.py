"""Display data for Live Monitoring -- a new module requested against the
client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Live Monitor" /
"Search Order" / "Image Sharing" pages), not one of the 16 FSD modules.
Wireframe phase: no writes, no CRUD, no API.

Live Monitor and Search Order are live rental-transaction feeds -- order
numbers, customer names, fare/deposit/tax amounts. Nothing in the client's
source files supplies real transactions (Customer Details & Registration is
itself still awaiting client data, per apps/byky_rms), so a plain seed here
would mean inventing money figures, which CLAUDE.md section 12 is explicit
about never doing on its own initiative. Live Monitor's Rent Bill/Direct
Bill/All tabs are the one deliberate exception: explicitly requested,
clearly-fabricated demo rows (rent_bill_orders/direct_bill_orders below),
the same spirit as Device Mapping's demo MAC addresses -- deterministic so
they never jump between page loads, station/staff drawn from real seed
data, but order numbers, customers and amounts openly wireframe values, not
claimed as real transactions. Search Order and Live Monitor's own Credit
Note tab stay untouched -- real filters, tabs and column headers with the
awaiting-data state in the body, the same treatment IMS's Live RFID
Monitoring and Inventory System Alerts screens already use.

Image Sharing carries no money and ties naturally to real stations and
staff, so it is populated the same way Device Mapping is: real station and
employee names, deterministic (seeded) so the numbers never jump between
page loads.

RMS WEB APK UI.xlsx feedback dropped this screen's Approved/Awaiting
review/Rejected split entirely (no more Status column, no more approve/
reject actions -- a shared photo is either on the list or deleted from it),
so shared_images() no longer carries a status field and counts() only
reports the total.
"""

import datetime

from apps.byky_core import seed

ORDER_STATUSES = ["Running", "Received", "Cancelled", "Credit Note"]

_ORDER_ROW_STATUSES = ["Running", "Running", "Received", "Cancelled", "Running"]


def _order_row(i, prefix):
    """One demo order row -- see module docstring for why this table is a
    deliberate exception to Live Monitor's usual awaiting-data treatment.
    Station and staff are real seed data; order number, customer and every
    amount are openly fabricated wireframe values, not real transactions."""
    st = seed.STATIONS[i % len(seed.STATIONS)]
    emp = seed.EMPLOYEES[(i * 5) % len(seed.EMPLOYEES)]
    order_date = datetime.date.today() - datetime.timedelta(days=i)
    fare = 60.0 + i * 22.5
    status = _ORDER_ROW_STATUSES[i % len(_ORDER_ROW_STATUSES)]
    collected = 0.0 if status == "Cancelled" else fare
    return {
        "order_number": f"{prefix}-{2026000 + i + 1}",
        "order_datetime": (
            order_date.strftime("%d/%m/%Y")
            + " " + f"{(9 + i) % 12 + 1:02d}:{(i * 13) % 60:02d} "
            + ("AM" if i % 2 == 0 else "PM")
        ),
        "station": st["name"],
        "open_by": f'{emp["name"]} ({emp["emp_no"]})',
        "customer": f"Customer {i + 1}",
        "collected": collected,
        "fare": fare,
        "bill": fare,
        "status": status,
    }


def rent_bill_orders():
    return [_order_row(i, "RB") for i in range(5)]


def direct_bill_orders():
    return [_order_row(i, "DB") for i in range(5)]


def order_kpis(rows):
    running = sum(1 for r in rows if r["status"] == "Running")
    return {
        "running_vehicles": running,
        "running_orders": running,
        "total_orders": len(rows),
        "cancelled_orders": sum(1 for r in rows if r["status"] == "Cancelled"),
        "bill_amount": sum(r["collected"] for r in rows),
    }


def shared_images():
    """Deterministic demo rows: a photo shared from a real station by a real
    staff member. See module docstring -- no money involved, so this one is
    populated rather than left as an awaiting-data screen."""
    out = []
    today = datetime.date.today()
    for i, st in enumerate(seed.STATIONS[:10]):
        emp = seed.EMPLOYEES[(i * 7) % len(seed.EMPLOYEES)]
        taken = today - datetime.timedelta(days=i)
        out.append(
            {
                "id": i + 1,
                "branch": st["name"],
                "shared_by": f'{emp["name"]} ({emp["emp_no"]})',
                "remarks": "",
                "taken_at": (
                    taken.strftime("%d/%m/%Y")
                    + " " + f"{(8 + i) % 12 + 1:02d}:{(i * 11) % 60:02d} "
                    + ("AM" if i % 2 == 0 else "PM")
                ),
            }
        )
    return out


def counts(images):
    return {
        "total": len(images),
    }
