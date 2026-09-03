"""Static seed data for the BYKY clickable wireframe.

Loaded once at import from ``seed_data.json``, which is generated from the two
client Excel files (``Location and Employee Data.xlsx``, ``VehicleDetails.xlsx``).

This is display data for the prototype only -- there is no database write path,
no API and no CRUD in this phase. See CLAUDE.md section 10.
"""

import json
from functools import lru_cache
from pathlib import Path

_DATA = json.loads((Path(__file__).parent / "seed_data.json").read_text())

STATIONS = _DATA["stations"]
EMPLOYEES = _DATA["employees"]
VEHICLES = _DATA["vehicles"]
CATEGORIES = _DATA["categories"]
VEHICLE_TYPES = _DATA["vehicle_types"]
EMIRATES = _DATA["emirates"]

# Value shown wherever the client's spreadsheet had a column but no data.
# Long form for forms and detail views; short form for narrow grid cells, where
# the long string wraps and triples the row height.
NOT_CAPTURED = "— not captured —"
NOT_CAPTURED_SHORT = "—"


@lru_cache(maxsize=None)
def station_by_code(code):
    return next((s for s in STATIONS if s["code"] == code), None)


@lru_cache(maxsize=None)
def vehicles_at(station_code):
    return tuple(v for v in VEHICLES if v["station_code"] == station_code)


@lru_cache(maxsize=None)
def employee_by_no(emp_no):
    return next((e for e in EMPLOYEES if e["emp_no"] == emp_no), None)


def counts():
    """Headline figures for dashboard and list-view KPI tiles."""
    return {
        "stations": len(STATIONS),
        "employees": len(EMPLOYEES),
        "vehicles": len(VEHICLES),
        "emirates": len(EMIRATES),
        "categories": len(CATEGORIES),
        "vehicle_types": len(VEHICLE_TYPES),
    }


# --- Dashboard aggregations -------------------------------------------------
# Every figure below is computed from the client data. Nothing is invented.
# There is no date, price or transaction column in either source file, so no
# trend, revenue or growth metric can be derived -- and none is faked here.

# Categories whose vehicles are electric, per the client's own category names.
_ELECTRIC = ("Electric Bike", "Electric Scooter")


def _is_electric(vehicle):
    return vehicle["category"].startswith(_ELECTRIC)


def _tally(rows, key):
    counts = {}
    for r in rows:
        counts[r[key]] = counts.get(r[key], 0) + 1
    return sorted(counts.items(), key=lambda kv: -kv[1])


def by_emirate():
    """[(emirate, station_count, fleet_size)], largest fleet first."""
    agg = {}
    for s in STATIONS:
        st, fl = agg.get(s["emirate"], (0, 0))
        agg[s["emirate"]] = (st + 1, fl + s["vehicle_count"])
    return sorted(
        ((e, st, fl) for e, (st, fl) in agg.items()), key=lambda r: -r[2]
    )


def by_category():
    return _tally(VEHICLES, "category")


def by_vehicle_type():
    return _tally(VEHICLES, "vtype")


def by_profession():
    return _tally(EMPLOYEES, "profession")


def top_stations(limit=8):
    return sorted(STATIONS, key=lambda s: -s["vehicle_count"])[:limit]


def fleet_curve():
    """Per-station fleet sizes, ranked. A genuine distribution, not a timeline."""
    return [s["vehicle_count"] for s in sorted(STATIONS, key=lambda s: -s["vehicle_count"])]


def station_rows():
    """Station directory rows. `share` is the true share of the total fleet;
    `share_scaled` normalises against the largest station so the bar is readable."""
    total = len(VEHICLES)
    biggest = max(s["vehicle_count"] for s in STATIONS) or 1
    rows = []
    for s in sorted(STATIONS, key=lambda s: -s["vehicle_count"]):
        rows.append(
            dict(
                s,
                share=round(s["vehicle_count"] / total * 100, 1),
                share_scaled=round(s["vehicle_count"] / biggest * 100),
            )
        )
    return rows


def dashboard():
    electric = sum(1 for v in VEHICLES if _is_electric(v))
    stocked = sum(1 for s in STATIONS if s["vehicle_count"] > 0)
    total_v = len(VEHICLES)
    return {
        "vehicles": total_v,
        "stations": len(STATIONS),
        "employees": len(EMPLOYEES),
        "emirates": len(EMIRATES),
        "categories": len(CATEGORIES),
        "vehicle_types": len(VEHICLE_TYPES),
        "electric": electric,
        "standard": total_v - electric,
        "electric_pct": round(electric / total_v * 100, 1),
        "standard_pct": round((total_v - electric) / total_v * 100, 1),
        "stocked_stations": stocked,
        "empty_stations": len(STATIONS) - stocked,
        "deployment_pct": round(stocked / len(STATIONS) * 100),
        "avg_per_station": round(total_v / len(STATIONS), 1),
        "largest_station": max(STATIONS, key=lambda s: s["vehicle_count"]),
        "by_emirate": by_emirate(),
        "by_category": by_category(),
        "by_vehicle_type": by_vehicle_type(),
        "by_profession": by_profession(),
        "top_stations": top_stations(),
        "fleet_curve": fleet_curve(),
        "station_rows": station_rows(),
        # Series handed to ApexCharts via json_script. No time axis exists in the
        # source data, so every series here is categorical or a ranked distribution.
        "chart_data": {
            "fleet_curve": fleet_curve(),
            "emirates": [e for e, _, _ in by_emirate()],
            "emirate_fleet": [f for _, _, f in by_emirate()],
            "categories": [c for c, _ in by_category()],
            "category_counts": [n for _, n in by_category()],
            "deployment_pct": round(stocked / len(STATIONS) * 100),
        },
    }
