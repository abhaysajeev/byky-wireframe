"""Display data for Print Invoice -- a new module requested against the
client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Print Invoice"
page), not one of the 16 FSD modules. Wireframe phase: no writes, no CRUD,
no API.

Sample data throughout, by explicit instruction for this module (unlike
Live Monitoring, which left its money fields empty per CLAUDE.md 12) -- the
point of this screen is to demonstrate the print layout and its paper
ratio, so it needs representative rows and one representative bill to print.
Station and staff names are real (from apps.byky_core.seed); order numbers,
customer names and amounts are illustrative, deterministic (seeded) so the
numbers never jump between page loads.
"""

import hashlib

from apps.byky_core import seed

CUSTOMER_NAMES = [
    "Menna", "Jinu", "Afafa", "Aleena", "Amro", "Yara", "Khalid",
    "Fatima", "Omar", "Layla",
]


def _amounts(seed_text, base):
    h = int(hashlib.md5(seed_text.encode()).hexdigest()[:6], 16)
    bill = round(base + (h % 4000) / 100, 2)
    tax = round(bill * 0.05, 2)
    discount = round((h % 3) * 3.5, 2)
    net = round(bill + tax - discount, 2)
    return bill, tax, discount, net


def invoices():
    """Sample tax-invoice rows for the list -- see module docstring."""
    out = []
    for i in range(10):
        emp = seed.EMPLOYEES[i % len(seed.EMPLOYEES)]
        bill, tax, discount, net = _amounts(f"inv-{i}", 25)
        out.append(
            {
                "order_no": f"AFA21014400{27 - i:03d}",
                "order_date": "02/09/2026",
                "open_by": f'{emp["name"].split()[0]} {emp["name"].split()[-1]}({emp["emp_no"]})',
                "close_by": f'{emp["name"].split()[0]} {emp["name"].split()[-1]}({emp["emp_no"]})',
                "customer": CUSTOMER_NAMES[i % len(CUSTOMER_NAMES)],
                "bill": bill,
                "tax": tax,
                "discount": discount,
                "net": net,
            }
        )
    return out


def sample_bill():
    """One representative tax invoice to print -- matches the shape and
    field set of the legacy mockup's own example bill exactly (station
    header, TRN, bike rental lines, discount/tax/net breakdown, customer
    footer). Station is real (Creek Park Gate 1); order/amount detail is
    illustrative."""
    station = seed.STATIONS[0]
    emp = seed.EMPLOYEES[0]
    return {
        "station_name": station["name"],
        "emirate": station["emirate"],
        "trn": "100297867200003",
        "date": "01-01-2026",
        "trans_no": 91,
        "inv_no": "CF0110196008151",
        "starting_time": "07:11 PM",
        "open_by": emp["name"],
        "returning_time": "07:56 PM",
        "closed_by": emp["name"],
        "closing_time": "07:56 PM",
        "lines": [
            {"sno": 1, "bike_no": "BL 02", "base_rate": "45.00/45 MINS", "extra_rate": "10.00/15 MINS", "rtn_time": "07:56 PM", "dur": "00:45", "amount": 45.00},
            {"sno": 2, "bike_no": "TW 5034", "base_rate": "25.00/30 MINS", "extra_rate": "10.00/15 MINS", "rtn_time": "07:56 PM", "dur": "00:45", "amount": 25.00},
        ],
        "discount": 0.00,
        "taxable_amount": 56.67,
        "card_discount": 10.50,
        "vat_pct": 5.0,
        "vat_amount": 2.83,
        "rounded_off": 0.00,
        "net_total": 59.50,
        "customer_name": "Abdu",
        "mobile": "+971567190358",
        "id_type": "",
        "id_no": "",
        "balance_to_pay": 0.00,
        "time": "00:45",
    }
