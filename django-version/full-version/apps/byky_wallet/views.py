"""Module 11 -- Wallet & Payments screens.

Generated from the FSD field tables into declarative specs; rendered through
byky/generic_screen.html so markup and spacing stay identical across modules.
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core import refdata, screens
from apps.byky_core.views import GenericScreenView, BykyScreenView


PERMISSIONS = [
    "Access",
    "Create",
    "Read",
    "Update",
    "Approve"
]
ROLES = [
    "SuperAdmin",
    "Finance Manager",
    "Approver"
]


class WalletScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class WalletPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Wallet Refund Request & Approval Management",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "Payment Gateway Provider & Webhook Integration",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Security Deposit Hold & Refund Reconciliation",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Customer Wallet Ledger & Transaction Audit",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Wallet Security Privilege Management",
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



class Screen11_1(WalletScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Claim ID"
        },
        {
            "kind": "text",
            "placeholder": "Customer Phone"
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Pending",
                "Approved",
                "Rejected",
                "Refunded"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Claim ID",
            "key": "id",
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
            "label": "Mobile No",
            "key": "mobile",
            "align": "",
            "style": ""
        },
        {
            "label": "Claim Amount",
            "key": "amount",
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
        },
        {
            "label": "Approver Remarks",
            "key": "remarks",
            "align": "",
            "style": "muted"
        }
    ],
    "sections": [
        {
            "title": "Refund Claim",
            "fields": [
                {
                    "id": "rf-amount",
                    "label": "Claimed Refund Amount AED",
                    "kind": "number",
                    "required": True,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "rf-reason",
                    "label": "Refund Reason",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Overcharge",
                        "Cancelled Booking",
                        "Deposit Return",
                        "Other"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "rf-iban",
                    "label": "IBAN Number",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "rf-bank",
                    "label": "Bank Name",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "rf-remarks",
                    "label": "Approver Remarks",
                    "kind": "textarea",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 12,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "New Claim",
    "drawer_id": "offcanvasRefund",
    "wide": True,
    "row_actions": [
        "Approve",
        "Reject",
        "View Bank Details"
    ],
    "kpis": []
}
    awaiting = "refund claims"


class Screen11_2(WalletScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Gateway Provider"
        },
        {
            "kind": "select",
            "label": "All Environments",
            "options": [
                "Sandbox",
                "Production"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Provider",
            "key": "provider",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Merchant ID",
            "key": "merchant",
            "align": "",
            "style": "code"
        },
        {
            "label": "Currency",
            "key": "currency",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Environment",
            "key": "environment",
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
    "sections": [
        {
            "title": "Payment Gateway",
            "fields": [
                {
                    "id": "pg-provider",
                    "label": "Gateway Provider Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pg-merchant",
                    "label": "Merchant ID",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pg-key",
                    "label": "API Key",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pg-secret",
                    "label": "Webhook Secret Token",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pg-currency",
                    "label": "Currency",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "AED",
                        "USD"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pg-env",
                    "label": "Environment",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Sandbox",
                        "Production"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Gateway",
    "drawer_id": "offcanvasPayGateway",
    "wide": True,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "payment gateways"


class Screen11_3(WalletScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Agreement No"
        },
        {
            "kind": "text",
            "placeholder": "Customer Name"
        },
        {
            "kind": "select",
            "label": "All Deposit Status",
            "options": [
                "Held",
                "Released",
                "Captured",
                "Pending Audit"
            ],
            "source": None
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
            "label": "Deposit AED",
            "key": "amount",
            "align": "end",
            "style": ""
        },
        {
            "label": "Hold Date",
            "key": "held",
            "align": "",
            "style": ""
        },
        {
            "label": "Release Date",
            "key": "released",
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
    "row_actions": [
        "Release",
        "Capture"
    ],
    "kpis": []
}
    awaiting = "deposit holds"


class Screen11_4(WalletScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Customers",
            "options": [],
            "source": "employees_list"
        },
        {
            "kind": "date",
            "placeholder": "Date range"
        },
        {
            "kind": "select",
            "label": "All Types",
            "options": [
                "Credit",
                "Debit"
            ],
            "source": None
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
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Description",
            "key": "description",
            "align": "",
            "style": ""
        },
        {
            "label": "Reference",
            "key": "ref",
            "align": "",
            "style": "code"
        },
        {
            "label": "Amount AED",
            "key": "amount",
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
    "sections": [
        {
            "title": "Manual Adjustment",
            "fields": [
                {
                    "id": "wl-type",
                    "label": "Adjustment Type",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [
                        "Credit",
                        "Debit"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "wl-amount",
                    "label": "Amount AED",
                    "kind": "number",
                    "required": True,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "wl-ref",
                    "label": "Reference No",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "wl-reason",
                    "label": "Reason",
                    "kind": "textarea",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 12,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Manual Adjustment",
    "drawer_id": "offcanvasWalletAdjust",
    "wide": False,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "wallet ledger entries"
