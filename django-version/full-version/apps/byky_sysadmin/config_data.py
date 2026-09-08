"""FSD 13.3 -- Global Application Configuration & Settings.

The enterprise-wide parameters every module reads: regional formatting, rental
defaults, the antenna/RFID polling intervals, service endpoints, asset paths
and the four external integrations.

Values follow CLAUDE.md section 12: nothing is invented. A setting carries a
real value only where one is actually known --

  * Pagination Limit          what the app genuinely does today (15 a page,
                              byky-screen.js and byky-cms-list.js)
  * Default Branch Working    supplied by the client as 04:00 - 03:59
    Time
  * Country / Time Zone       derived from the seed data: 36 stations across
                              the UAE plus one in Kuwait

Everything else renders blank against a placeholder showing the shape of the
value, and is flagged `awaiting` so the tinted input marks it as outstanding.
"""

from apps.byky_core import seed

NOT_SET = ""


def _countries():
    """The countries the client's own station data actually spans."""
    names = []
    for station in seed.STATIONS:
        country = "Kuwait" if station["emirate"] == "Kuwait" else "United Arab Emirates"
        if country not in names:
            names.append(country)
    return sorted(names, reverse=True)


SECTIONS = [
    {
        "title": "Regional & Display",
        "fields": [
            {
                "key": "country",
                "label": "Country",
                "kind": "select",
                "options": _countries,
                "value": "United Arab Emirates",
                "span": 1,
                "help": "Drives address, tax and currency formats.",
            },
            {
                "key": "timezone",
                "label": "Time Zone",
                "kind": "select",
                "options": ["Asia/Dubai (GST, UTC+4)", "Asia/Kuwait (AST, UTC+3)", "UTC"],
                "value": "Asia/Dubai (GST, UTC+4)",
                "span": 1,
            },
            {
                "key": "decimals",
                "label": "No. of Decimal Places",
                "kind": "number",
                "placeholder": "2",
                "value": NOT_SET,
                "span": 1,
                "awaiting": True,
                "help": "Applied to every monetary amount.",
            },
            {
                "key": "pagination",
                "label": "Pagination Limit",
                "kind": "number",
                "value": "15",
                "span": 1,
                "help": "Rows a page on every grid.",
            },
        ],
    },
    {
        "title": "Rental Defaults",
        "fields": [
            {
                "key": "promo_expiry",
                "label": "Promotion Expire After (minutes)",
                "kind": "number",
                "placeholder": "e.g. 30",
                "value": NOT_SET,
                "span": 1,
                "awaiting": True,
            },
            {
                "key": "phones_per_card",
                "label": "Phone Numbers Per Card",
                "kind": "number",
                "placeholder": "e.g. 2",
                "value": NOT_SET,
                "span": 1,
                "awaiting": True,
            },
            {
                "key": "branch_open",
                "label": "Default Branch Working Time — From",
                "kind": "time",
                "value": "04:00",
                "span": 1,
            },
            {
                "key": "branch_close",
                "label": "Default Branch Working Time — To",
                "kind": "time",
                "value": "03:59",
                "span": 1,
                "help": "Runs past midnight; a day closes at 03:59 the next morning.",
            },
            {
                "key": "test_drive_customer",
                "label": "Test Drive Time — Customer (minutes)",
                "kind": "number",
                "placeholder": "e.g. 10",
                "value": NOT_SET,
                "span": 1,
                "awaiting": True,
            },
            {
                "key": "test_drive_cashier",
                "label": "Test Drive Time — Cashier (minutes)",
                "kind": "number",
                "placeholder": "e.g. 15",
                "value": NOT_SET,
                "span": 1,
                "awaiting": True,
            },
        ],
    },
    {
        "title": "Antenna & RFID Processing",
        "fields": [
            {
                "key": "antenna_data_interval",
                "label": "Antenna Data Processing Interval (min)",
                "kind": "number",
                "placeholder": "e.g. 5",
                "value": NOT_SET,
                "span": 1,
                "awaiting": True,
                "help": "How often queued antenna reads are processed.",
            },
            {
                "key": "antenna_status_interval",
                "label": "Antenna Status Check Interval (min)",
                "kind": "number",
                "placeholder": "e.g. 15",
                "value": NOT_SET,
                "span": 1,
                "awaiting": True,
                "help": "Heartbeat poll for gate antenna health.",
            },
        ],
    },
    {
        "title": "Service Endpoints",
        "fields": [
            {
                "key": "rms_url",
                "label": "RMS Service URL",
                "kind": "url",
                "placeholder": "https://",
                "value": NOT_SET,
                "span": 2,
                "awaiting": True,
            },
            {
                "key": "antenna_url",
                "label": "Antenna Data Service URL",
                "kind": "url",
                "placeholder": "https://",
                "value": NOT_SET,
                "span": 2,
                "awaiting": True,
            },
        ],
    },
    {
        "title": "Media & Asset Paths",
        "fields": [
            {
                "key": "vehicle_image_path",
                "label": "Image Path — Vehicle / Card",
                "kind": "text",
                "placeholder": "/media/vehicles/",
                "value": NOT_SET,
                "span": 2,
                "awaiting": True,
            },
            {
                "key": "promo_asset_path",
                "label": "Discount / Share Image Assets",
                "kind": "text",
                "placeholder": "/media/promotions/",
                "value": NOT_SET,
                "span": 2,
                "awaiting": True,
            },
        ],
    },
]


# The four external integrations. Each is a set of credentials rather than a
# single value, so they follow the list + drawer pattern the rest of the app
# uses for multi-field rows (CLAUDE.md) instead of being flattened inline.
# Field labels describe the shape of each integration; no keys or endpoints are
# invented -- every value is blank until the client supplies one.
INTEGRATIONS = [
    {
        "key": "whatsapp",
        "name": "WhatsApp Configuration",
        "desc": "Booking confirmations and ride receipts over WhatsApp Business.",
        "fields": [
            {"key": "provider", "label": "Provider", "kind": "text", "placeholder": "e.g. Meta Cloud API"},
            {"key": "number", "label": "Business Phone Number", "kind": "text", "placeholder": "+971"},
            {"key": "endpoint", "label": "API Endpoint", "kind": "url", "placeholder": "https://"},
            {"key": "token", "label": "API Token", "kind": "password", "placeholder": "••••••••"},
            {"key": "sender", "label": "Sender Display Name", "kind": "text", "placeholder": "BYKY"},
        ],
    },
    {
        "key": "sms",
        "name": "SMS Configuration",
        "desc": "OTP and alert delivery through the SMS gateway.",
        "fields": [
            {"key": "provider", "label": "Provider", "kind": "text", "placeholder": ""},
            {"key": "sender_id", "label": "Sender ID", "kind": "text", "placeholder": "BYKY"},
            {"key": "endpoint", "label": "API Endpoint", "kind": "url", "placeholder": "https://"},
            {"key": "api_key", "label": "API Key", "kind": "password", "placeholder": "••••••••"},
            {"key": "route", "label": "Route", "kind": "select", "options": ["Transactional", "Promotional"]},
        ],
    },
    {
        "key": "mail",
        "name": "Mail Configuration",
        "desc": "Outbound SMTP for invoices, reports and account mail.",
        "fields": [
            {"key": "host", "label": "SMTP Host", "kind": "text", "placeholder": "smtp."},
            {"key": "port", "label": "SMTP Port", "kind": "number", "placeholder": "587"},
            {"key": "encryption", "label": "Encryption", "kind": "select", "options": ["TLS", "SSL", "None"]},
            {"key": "username", "label": "Username", "kind": "text", "placeholder": ""},
            {"key": "password", "label": "Password", "kind": "password", "placeholder": "••••••••"},
            {"key": "from_address", "label": "From Address", "kind": "text", "placeholder": "no-reply@"},
            {"key": "from_name", "label": "From Name", "kind": "text", "placeholder": "BYKY RMS"},
        ],
    },
    {
        "key": "payment",
        "name": "Payment Gateway Configuration",
        "desc": "Card and wallet settlement for rentals and top-ups.",
        "fields": [
            {"key": "provider", "label": "Provider", "kind": "text", "placeholder": ""},
            {"key": "merchant_id", "label": "Merchant ID", "kind": "text", "placeholder": ""},
            {"key": "api_key", "label": "API Key", "kind": "password", "placeholder": "••••••••"},
            {"key": "secret", "label": "Secret Key", "kind": "password", "placeholder": "••••••••"},
            {"key": "environment", "label": "Environment", "kind": "select", "options": ["Sandbox", "Live"]},
            {"key": "currency", "label": "Settlement Currency", "kind": "select", "options": ["AED", "KWD"]},
        ],
    },
]


def sections():
    """Config sections with any callable option lists resolved."""
    out = []
    for section in SECTIONS:
        fields = []
        for field in section["fields"]:
            f = dict(field)
            options = f.get("options")
            f["options"] = options() if callable(options) else (options or [])
            f.setdefault("value", NOT_SET)
            f.setdefault("placeholder", "")
            f.setdefault("span", 1)
            f.setdefault("awaiting", False)
            f.setdefault("help", "")
            fields.append(f)
        out.append({"title": section["title"], "fields": fields})
    return out


def integrations():
    """Integrations, each flagged with whether it holds a value yet."""
    out = []
    for item in INTEGRATIONS:
        fields = [dict(f, value=NOT_SET, options=f.get("options", []),
                       placeholder=f.get("placeholder", "")) for f in item["fields"]]
        out.append(dict(item, fields=fields, configured=False))
    return out
