"""Approximate coordinates for the client's stations.

These are the published locations of the real public places the stations sit at
(parks, corniches, marinas), used so the network map has something to plot. They
are approximate to a few hundred metres and are NOT survey data -- FSD 1.7 still
requires exact per-station GPS from the client, which is why Station Address
Mapping continues to show those fields as awaiting.
"""

# station name (as reconciled in seed_data.json) -> (lat, lng)
STATION_COORDS = {
    # Dubai
    "Creek Park Gate 1": (25.2285, 55.3273),
    "Creek Park Gate 4": (25.2320, 55.3310),
    "Al Zabeel Park Gate 1": (25.2308, 55.3050),
    "Al Mamzar Park": (25.3033, 55.3506),
    "Al Barsha Pond Park": (25.1050, 55.1990),
    "Dubai": (25.2048, 55.2708),
    # Abu Dhabi
    "Abu Dhabi Corniche 1": (24.4750, 54.3300),
    "Abu Dhabi Corniche 2": (24.4720, 54.3390),
    "Abu Dhabi Corniche 3": (24.4690, 54.3480),
    "Family Park": (24.4600, 54.3400),
    "Khalifa Square": (24.4900, 54.3700),
    # Sharjah
    "Majaz 1": (25.3280, 55.3830),
    "Sharjah Corniche 1": (25.3570, 55.3900),
    "Sharjah Corniche 2": (25.3600, 55.3950),
    "Sharjah Corniche 3": (25.3630, 55.4000),
    "Kshisha Park": (25.3330, 55.4200),
    # Ajman
    "Ajman Marina": (25.4110, 55.4350),
    "Ajman Corniche": (25.4050, 55.4400),
    "Alalam Park": (25.4000, 55.4450),
    "Safiya Park": (25.3900, 55.4500),
    # Fujairah
    "Fujairah Corniche": (25.1220, 56.3400),
    "Kalba Corniche Park": (25.0400, 56.3500),
    "Qidfa Beach": (25.2800, 56.3500),
    # Ras Al Khaimah
    "RAK Corniche 1": (25.7900, 55.9500),
    "Al Saqr Park": (25.7800, 55.9400),
    "Mina Al Arab": (25.7000, 55.9000),
    # Al Ain
    "Hili Archaeological Park": (24.2500, 55.7600),
    "Al Wadi": (24.2200, 55.7500),
    "Al Towayya Park": (24.2400, 55.7700),
    "Al Zakher Park": (24.1700, 55.7300),
    "Mubazzarah": (24.1300, 55.7800),
    "Asharij Walk Way": (24.2100, 55.7400),
    "Al Salamat Park": (24.1900, 55.7200),
    "Al Dhaher Park": (24.2600, 55.7000),
    "Mazyad Walkway": (24.1500, 55.7600),
    # Kuwait
    "Hilton Kuwait Resort": (29.0500, 48.1000),
}

# Map centre and zoom that frame the whole UAE network.
UAE_CENTRE = (24.9, 55.4)
UAE_ZOOM = 7


def coords_for(name):
    return STATION_COORDS.get(name)


def station_points(with_revenue=False):
    """Map markers for every station: name, emirate, fleet size and coordinates."""
    from apps.byky_core import seed

    revenue = {}
    if with_revenue:
        from apps.byky_core import sales

        revenue = {r["name"]: r["revenue"] for r in sales.by_station()}

    points = []
    for s in seed.STATIONS:
        c = coords_for(s["name"])
        if not c:
            continue
        points.append(
            {
                "name": s["name"],
                "emirate": s["emirate"],
                "fleet": s["vehicle_count"],
                "revenue": revenue.get(s["name"], 0),
                "lat": c[0],
                "lng": c[1],
            }
        )
    return points
