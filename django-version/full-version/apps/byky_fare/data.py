"""Reference data for Fare & Schemes.

Both screens come from client-supplied HTML mockups (byky Docs/
Fare_Entry_Advanced_UI_v3.html and Scheme_Creation.html) rather than from the
FSD, so the field lists here mirror those mockups exactly.

Dropdown options that describe real BYKY inventory are pulled from the seed data;
the rest are the fixed enumerations the mockups define.
"""

from apps.byky_core import seed

PRICE_LEVELS = ["Company", "Branch", "Location"]
FARE_STATUS = ["Active", "Inactive"]

DAYS = ["All Days", "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"]

PROMOTION_FOR = ["Value", "Quantity"]
INVENTORY_TYPES = ["Vehicle", "Accessory", "Both"]
PROMOTION_TYPES = ["Free Item", "Discount", "Buy X Get Y"]

# Package durations the client's mockup uses as examples.
PACKAGE_TIMES = [15, 30, 45, 60, 90, 120]


def categories():
    return seed.CATEGORIES


def vehicle_types():
    return seed.VEHICLE_TYPES


def companies():
    return ["BYKY"]
