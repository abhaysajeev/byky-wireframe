"""Illustrative sales figures for the dashboard.

WHY THIS EXISTS
---------------
The client's two spreadsheets are a fleet and staff extract. They contain no
dates, prices, agreements or transactions, so no revenue figure can be derived
from them. The dashboard nonetheless has to show the commercial picture the
business actually cares about.

Everything in this module is therefore GENERATED, not client data. It is:

  * derived from the real fleet -- a station's revenue tracks the vehicles it
    actually holds, so the shape of the numbers matches the real network;
  * deterministic -- seeded, so figures do not jump between page loads;
  * confined to this one module -- when the client supplies real rental data,
    replace the functions here and every dashboard figure follows.

Rates are the AED tariff bands the FSD assumes (hourly / half-day / full-day).

DO NOT reuse these figures on operational screens. The dashboard is the only
place they belong, and it labels them as indicative.
"""

import random
from datetime import date, timedelta

from apps.byky_core import seed

CURRENCY = "AED"

# Indicative tariff bands per category, AED per hour.
_HOURLY_RATE = {
    "Byky": 25,
    "Electric Bike iFun": 45,
    "Electric Bike Ghae": 45,
    "Electric Scooter Vigrous": 40,
    "Kuwait Bike": 25,
    "Barsha Baby": 15,
    "Special Offer": 20,
    "Rent Bike": 30,
}
_DEFAULT_RATE = 25

# Utilisation assumptions behind every figure below, stated once so they can be
# challenged or replaced in one place:
#   a vehicle is rented ~1.6 times a day, ~1.5 hours per rental.
RENTALS_PER_VEHICLE_DAY = 1.6
HOURS_PER_RENTAL = 1.5
DAYS_PER_MONTH = 30


def _rng():
    """Fixed seed: the demo must show the same numbers every time."""
    return random.Random(20260101)


def rate_for(category):
    return _HOURLY_RATE.get(category, _DEFAULT_RATE)


def _station_revenue():
    """Monthly revenue per station, scaled by the fleet it really holds."""
    rng = _rng()
    out = {}
    for s in sorted(seed.STATIONS, key=lambda x: x["name"]):
        fleet = s["vehicle_count"]
        if not fleet:
            out[s["name"]] = 0
            continue
        util = rng.uniform(0.82, 1.18)   # +/-18% station-to-station variance
        revenue = (
            fleet
            * RENTALS_PER_VEHICLE_DAY
            * HOURS_PER_RENTAL
            * _DEFAULT_RATE
            * DAYS_PER_MONTH
            * util
        )
        out[s["name"]] = int(round(revenue))
    return out


def by_station():
    rev = _station_revenue()
    rows = []
    for s in seed.STATIONS:
        rows.append(
            {
                "name": s["name"],
                "emirate": s["emirate"],
                "code": s["code"],
                "fleet": s["vehicle_count"],
                "revenue": rev[s["name"]],
            }
        )
    return sorted(rows, key=lambda r: -r["revenue"])


def by_emirate():
    agg = {}
    for r in by_station():
        agg.setdefault(r["emirate"], 0)
        agg[r["emirate"]] += r["revenue"]
    return sorted(agg.items(), key=lambda kv: -kv[1])


def by_category():
    """Revenue split across categories, weighted by fleet size and tariff band."""
    counts = {}
    for v in seed.VEHICLES:
        counts[v["category"]] = counts.get(v["category"], 0) + 1
    total_units = sum(counts.values())
    total = monthly_revenue()
    weighted = {c: n * rate_for(c) for c, n in counts.items()}
    wsum = sum(weighted.values()) or 1
    return sorted(
        ((c, int(round(total * w / wsum))) for c, w in weighted.items()),
        key=lambda kv: -kv[1],
    )


def monthly_revenue():
    return sum(_station_revenue().values())


def daily_series(days=30):
    """Revenue per day for the last `days` days, with a weekly rhythm."""
    rng = _rng()
    base = monthly_revenue() / days
    today = date.today()
    out = []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        # Fri/Sat are the busiest days in the UAE leisure market.
        weekend = 1.35 if d.weekday() in (4, 5) else 0.93
        out.append(
            {
                "date": d.isoformat(),
                "label": d.strftime("%d %b"),
                "revenue": int(round(base * weekend * rng.uniform(0.88, 1.12))),
            }
        )
    return out


def monthly_series(months=12):
    rng = _rng()
    base = monthly_revenue()
    today = date.today().replace(day=1)
    out = []
    for i in range(months - 1, -1, -1):
        m = (today.month - i - 1) % 12 + 1
        y = today.year + ((today.month - i - 1) // 12)
        # Cooler months draw more riders in the Gulf.
        season = 1.25 if m in (11, 12, 1, 2, 3) else 0.82 if m in (6, 7, 8) else 1.0
        out.append(
            {
                "label": date(y, m, 1).strftime("%b"),
                "revenue": int(round(base * season * rng.uniform(0.92, 1.08))),
            }
        )
    return out


def recent_invoices(limit=8):
    """Latest rental agreements, for the dashboard activity table."""
    rng = _rng()
    stations = by_station()[:12]
    vehicles = seed.VEHICLES
    statuses = ["Paid", "Paid", "Paid", "Pending", "Refunded"]
    out = []
    today = date.today()
    for i in range(limit):
        v = vehicles[rng.randrange(len(vehicles))]
        st = stations[rng.randrange(len(stations))]
        hours = rng.choice([1, 1, 2, 2, 3, 4, 8])
        amount = hours * rate_for(v["category"])
        out.append(
            {
                "agreement": f"AGR-{26000 + i * 137 + rng.randrange(90):05d}",
                "station": st["name"],
                "vehicle": v["number"],
                "category": v["category"],
                "hours": hours,
                "amount": amount,
                "date": (today - timedelta(days=rng.randrange(6))).strftime("%d %b"),
                "status": statuses[rng.randrange(len(statuses))],
            }
        )
    return out


def headline():
    rev = monthly_revenue()
    days = daily_series()
    rentals = int(
        round(len(seed.VEHICLES) * RENTALS_PER_VEHICLE_DAY * DAYS_PER_MONTH)
    )
    return {
        "currency": CURRENCY,
        "monthly_revenue": rev,
        "daily_avg": int(round(rev / 30)),
        "today": days[-1]["revenue"],
        "rentals": rentals,
        "avg_ticket": int(round(rev / rentals)) if rentals else 0,
        "paid_invoices": int(round(rentals * 0.94)),
        "pending_invoices": int(round(rentals * 0.06)),
    }
