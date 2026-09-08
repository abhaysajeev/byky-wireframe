"""Discount Card Management.

Not an FSD module -- built from the client's own Discount Card Configuration
mockup, the same way Fare & Schemes (apps/byky_fare) was built from its two
HTML mockups rather than an FSD PDF.

No source data exists for cards, card grades or discount rules -- the client
never supplied any -- so both master lists start genuinely empty and every
screen renders the same honest awaiting-data pattern used everywhere else
(CLAUDE.md 12): real column headers, an empty-state body, nothing invented.

CARD_TYPES is a generic classification vocabulary (Prepaid / Loyalty /
Corporate / Membership / Discount), not client-specific data -- the same
category of reference list as refdata.NATIONALITIES. It exists so the Card
Type dropdown is genuinely usable while the Card master itself is still
empty, the same reasoning behind any standard reference list in this app.
"""

CARD_TYPES = [
    "Prepaid Card",
    "Loyalty Card",
    "Corporate Card",
    "Membership Card",
    "Discount Card",
]

DAYS = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

# (key, label) -- FSD-less mockup names these radio options directly.
PROMOTION_TYPES = [
    ("basic_promo", "Promotion Applied On Basic Fare"),
    ("full_promo", "Promotion Applied On Full Fare"),
    ("basic_approval", "Approval Mode On Basic Fare"),
    ("full_approval", "Approval Mode On Full Fare"),
]

# (key, label, needs_count) -- entries with needs_count=True pair a number
# input with the label ("<input> times a Week").
USAGE_TYPES = [
    ("one_time", "One Time", False),
    ("per_day", "times a Day", True),
    ("per_week", "times a Week", True),
    ("per_month", "times a Month", True),
    ("multiple", "Multiple times", False),
]


def cards():
    """No source data for this entity -- honest empty list."""
    return []


def card_grades():
    """No source data for this entity -- honest empty list."""
    return []
