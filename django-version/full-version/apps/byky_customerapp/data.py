"""Customer App Management.

Not an FSD module -- built from the client's "RMS WEB" mockups
(RMS WEB 07.09.2026-1.pdf, page 11: "Customer App Management") the same way
Fare & Schemes, Discount Card Management, Request Management and Credit Note
Management were built from mockups rather than an FSD PDF. The referenced
screenshots capture the client's live legacy system -- real customer names,
phone numbers and order data -- not a data export we have programmatic
access to, so none of it is reproducible here. Every list below therefore
starts genuinely empty and nothing is invented (CLAUDE.md 12).

Live Monitoring, Order Status, Wallet Refund, Promo Code, Loyalty Profile,
Loyalty Redemption Profile and Notifications are not built here -- they
already exist as IMS screens and are only re-surfaced under this sidebar
group via vertical_menu.json (see byky-screen-design-system.md). Only Mail
Template & Template Mapping, Advertisement and Customer Management are new
screens owned by this app.
"""

MAIL_EVENTS = [
    "Registration Welcome",
    "Booking Confirmation",
    "Booking Cancellation",
    "Trip Completion",
    "Wallet Top-up",
    "Wallet Refund",
    "Loyalty Point Credit",
    "Password Reset",
]

CUSTOMER_TYPES = ["Individual", "Corporate", "Tourist"]

CUSTOMER_CATEGORIES = ["Regular", "Premium", "VIP"]

CUSTOMER_SEARCH_IN = ["Customer Name", "Phone No", "E-Mail", "Customer ID"]
CUSTOMER_SEARCH_TYPE = ["Exact Match", "Contains"]


def mail_templates():
    """Mail templates configured for customer-app notifications. No source
    data -- honest empty list."""
    return []


def mail_template_mappings():
    """Event -> customer type -> template routing. No source data -- honest
    empty list."""
    return []


def advertisement_profiles():
    """Image-slider profiles shown in the customer app. No source data --
    honest empty list."""
    return []


def advertisement_profile_mappings():
    """Profile -> active-window (from/to date-time) scheduling. No source
    data -- honest empty list."""
    return []
