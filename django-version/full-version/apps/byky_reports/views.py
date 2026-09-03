"""Module 6 -- Reports screens.

Generated from the FSD field tables into declarative specs; rendered through
byky/generic_screen.html so markup and spacing stay identical across modules.
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core import refdata, screens
from apps.byky_core.views import GenericScreenView, BykyScreenView


PERMISSIONS = [
    "Access",
    "Read",
    "Print",
    "Export",
    "Approve"
]
ROLES = [
    "SuperAdmin",
    "Finance Manager",
    "Branch Manager",
    "Auditor"
]


class ReportsScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class ReportsPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Daily Rental Transaction & Revenue Report",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "Station Stock & Inventory Valuation Report",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Customer Rental History & Ledger Report",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Vehicle Fleet Utilization & Performance Report",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Vehicle Maintenance & Overhaul Audit Report",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Wallet Settlement & Refund Audit Report",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "RFID Antenna Gate Read Telemetry Report",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "REPORTS Security Privilege Management",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ]
]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "permissions": PERMISSIONS,
                "roles": ROLES,
                "screens": [{"name": n, "perms": p} for n, p in self.SCREENS],
            }
        )
        return context



class Screen6_1(ReportsScreen):
    spec = {
    "filters": [
        {
            "kind": "date",
            "placeholder": "From date"
        },
        {
            "kind": "date",
            "placeholder": "To date"
        },
        {
            "kind": "select",
            "label": "All Branches",
            "options": [],
            "source": "branches_list"
        }
    ],
    "columns": [
        {
            "label": "Agreement No",
            "key": "agreement",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Customer",
            "key": "customer",
            "align": "",
            "style": ""
        },
        {
            "label": "Station",
            "key": "station",
            "align": "",
            "style": ""
        },
        {
            "label": "Vehicle Code",
            "key": "vehicle",
            "align": "",
            "style": ""
        },
        {
            "label": "Start Time",
            "key": "start",
            "align": "",
            "style": ""
        },
        {
            "label": "End Time",
            "key": "end",
            "align": "",
            "style": ""
        },
        {
            "label": "Duration",
            "key": "duration",
            "align": "center",
            "style": ""
        },
        {
            "label": "Rental Fee",
            "key": "fee",
            "align": "end",
            "style": ""
        },
        {
            "label": "Payment",
            "key": "payment",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Status",
            "key": "status",
            "align": "center",
            "style": "status"
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [],
    "kpis": []
}
    awaiting = "rental agreements"


class Screen6_2(ReportsScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Branches",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "select",
            "label": "All Categories",
            "options": [],
            "source": "categories_list"
        },
        {
            "kind": "select",
            "label": "All Stock Filters",
            "options": [
                "All",
                "Low Stock",
                "Out of Stock"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Item Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Item Name",
            "key": "name",
            "align": "",
            "style": ""
        },
        {
            "label": "Category",
            "key": "category",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Station",
            "key": "station",
            "align": "",
            "style": ""
        },
        {
            "label": "Qty on Hand",
            "key": "qty",
            "align": "center",
            "style": ""
        },
        {
            "label": "Reorder Level",
            "key": "reorder",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Unit Cost",
            "key": "cost",
            "align": "end",
            "style": "muted"
        },
        {
            "label": "Total Value",
            "key": "value",
            "align": "end",
            "style": "muted"
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [],
    "kpis": []
}
    awaiting = "stock valuations"


class Screen6_3(ReportsScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Customer Name"
        },
        {
            "kind": "text",
            "placeholder": "Mobile No"
        },
        {
            "kind": "date",
            "placeholder": "Date range"
        }
    ],
    "columns": [
        {
            "label": "Date",
            "key": "date",
            "align": "",
            "style": ""
        },
        {
            "label": "Type",
            "key": "type",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Vehicle",
            "key": "vehicle",
            "align": "",
            "style": ""
        },
        {
            "label": "Debit",
            "key": "debit",
            "align": "end",
            "style": ""
        },
        {
            "label": "Credit",
            "key": "credit",
            "align": "end",
            "style": ""
        },
        {
            "label": "Balance",
            "key": "balance",
            "align": "end",
            "style": ""
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [],
    "kpis": []
}
    awaiting = "ledger entries"


class Screen6_4(ReportsScreen):
    spec = {
    "filters": [
        {
            "kind": "date",
            "placeholder": "Date range"
        },
        {
            "kind": "select",
            "label": "All Branches",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "select",
            "label": "All Categories",
            "options": [],
            "source": "categories_list"
        }
    ],
    "columns": [
        {
            "label": "Vehicle Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Category",
            "key": "category",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Station",
            "key": "station",
            "align": "",
            "style": ""
        },
        {
            "label": "Rental Hours",
            "key": "hours",
            "align": "center",
            "style": ""
        },
        {
            "label": "Downtime",
            "key": "downtime",
            "align": "center",
            "style": ""
        },
        {
            "label": "Revenue AED",
            "key": "revenue",
            "align": "end",
            "style": ""
        },
        {
            "label": "Utilization %",
            "key": "util",
            "align": "center",
            "style": ""
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [],
    "kpis": []
}
    awaiting = "utilisation figures"


class Screen6_5(ReportsScreen):
    spec = {
    "filters": [
        {
            "kind": "date",
            "placeholder": "Date range"
        },
        {
            "kind": "select",
            "label": "All Branches",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "select",
            "label": "All Repair Categories",
            "options": [
                "Routine",
                "Overhaul",
                "Emergency"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Ticket No",
            "key": "ticket",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Vehicle Code",
            "key": "vehicle",
            "align": "",
            "style": ""
        },
        {
            "label": "Category",
            "key": "category",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Technician",
            "key": "technician",
            "align": "",
            "style": ""
        },
        {
            "label": "Parts Cost",
            "key": "parts",
            "align": "end",
            "style": ""
        },
        {
            "label": "Labor Cost",
            "key": "labor",
            "align": "end",
            "style": ""
        },
        {
            "label": "Total",
            "key": "total",
            "align": "end",
            "style": ""
        },
        {
            "label": "Closed",
            "key": "closed",
            "align": "",
            "style": ""
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [],
    "kpis": []
}
    awaiting = "maintenance tickets"


class Screen6_6(ReportsScreen):
    spec = {
    "filters": [
        {
            "kind": "date",
            "placeholder": "Date range"
        },
        {
            "kind": "select",
            "label": "All Gateways",
            "options": [
                "Network International",
                "Stripe"
            ],
            "source": None
        },
        {
            "kind": "select",
            "label": "All Refund Status",
            "options": [
                "Approved",
                "Pending",
                "Rejected"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Claim ID",
            "key": "claim",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Customer",
            "key": "customer",
            "align": "",
            "style": ""
        },
        {
            "label": "Gateway Ref",
            "key": "ref",
            "align": "",
            "style": "code"
        },
        {
            "label": "Requested",
            "key": "requested",
            "align": "end",
            "style": ""
        },
        {
            "label": "Approved",
            "key": "approved",
            "align": "end",
            "style": ""
        },
        {
            "label": "Refund Date",
            "key": "date",
            "align": "",
            "style": ""
        },
        {
            "label": "Status",
            "key": "status",
            "align": "center",
            "style": "status"
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [],
    "kpis": []
}
    awaiting = "refund claims"


class Screen6_7(ReportsScreen):
    spec = {
    "filters": [
        {
            "kind": "date",
            "placeholder": "Date range"
        },
        {
            "kind": "select",
            "label": "All Branches",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "select",
            "label": "All Event Status",
            "options": [
                "Authorized",
                "Alarm"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Scan Time",
            "key": "time",
            "align": "",
            "style": ""
        },
        {
            "label": "RFID Tag EPC",
            "key": "epc",
            "align": "",
            "style": "code"
        },
        {
            "label": "Vehicle Code",
            "key": "vehicle",
            "align": "",
            "style": ""
        },
        {
            "label": "Station",
            "key": "station",
            "align": "",
            "style": ""
        },
        {
            "label": "Gate ID",
            "key": "gate",
            "align": "center",
            "style": ""
        },
        {
            "label": "RSSI",
            "key": "rssi",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Clearance",
            "key": "status",
            "align": "center",
            "style": "status"
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [],
    "kpis": []
}
    awaiting = "gate scan records"
