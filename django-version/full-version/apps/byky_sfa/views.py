"""Module 7 -- Sales Force screens.

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
    "Approve",
    "Delete"
]
ROLES = [
    "SuperAdmin",
    "Sales Manager",
    "Sales Agent"
]


class SfaScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class SfaPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Sales Lead & Opportunity Management",
        [
            True,
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "Corporate B2B Rental Contract Setup",
        [
            True,
            False,
            True,
            False,
            False,
            False
        ]
    ],
    [
        "Commercial Quotation & Proposal Generator",
        [
            True,
            False,
            True,
            False,
            False,
            False
        ]
    ],
    [
        "Sales Agent Commission & Incentive Setup",
        [
            True,
            False,
            True,
            False,
            False,
            False
        ]
    ],
    [
        "Sales Pipeline & Target Tracking",
        [
            True,
            False,
            True,
            False,
            False,
            False
        ]
    ],
    [
        "SFA Security Privilege Management",
        [
            True,
            False,
            True,
            False,
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



class Screen7_1(SfaScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Company Name"
        },
        {
            "kind": "select",
            "label": "All Sales Stages",
            "options": [
                "Prospect",
                "Qualified",
                "Proposal",
                "Negotiation",
                "Won",
                "Lost"
            ],
            "source": None
        },
        {
            "kind": "select",
            "label": "All Sales Reps",
            "options": [],
            "source": "employees_list"
        }
    ],
    "columns": [
        {
            "label": "Lead Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Company",
            "key": "company",
            "align": "",
            "style": ""
        },
        {
            "label": "Contact Person",
            "key": "contact",
            "align": "",
            "style": ""
        },
        {
            "label": "Fleet Count",
            "key": "fleet",
            "align": "center",
            "style": ""
        },
        {
            "label": "Deal Value",
            "key": "value",
            "align": "end",
            "style": ""
        },
        {
            "label": "Stage",
            "key": "stage",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Assigned Rep",
            "key": "rep",
            "align": "",
            "style": ""
        }
    ],
    "sections": [
        {
            "title": "Lead",
            "fields": [
                {
                    "id": "ld-company",
                    "label": "Company Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ld-contact",
                    "label": "Contact Person",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ld-desig",
                    "label": "Designation",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ld-mobile",
                    "label": "Mobile No",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ld-email",
                    "label": "Email",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ld-source",
                    "label": "Lead Source",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Website",
                        "Referral",
                        "Cold Call",
                        "Event",
                        "Partner"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ld-value",
                    "label": "Estimated Deal Value AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ld-fleet",
                    "label": "Expected Fleet Count",
                    "kind": "number",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ld-stage",
                    "label": "Sales Stage",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Prospect",
                        "Qualified",
                        "Proposal",
                        "Negotiation",
                        "Won",
                        "Lost"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ld-rep",
                    "label": "Assigned Sales Rep",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": "employees_list",
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Lead",
    "drawer_id": "offcanvasLead",
    "wide": True,
    "row_actions": [
        "Edit",
        "Create Quote",
        "Convert Contract",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "sales leads"


class Screen7_2(SfaScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Contract No"
        },
        {
            "kind": "text",
            "placeholder": "Client Company"
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Active",
                "Expired",
                "Draft"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Contract No",
            "key": "no",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Client Company",
            "key": "client",
            "align": "",
            "style": ""
        },
        {
            "label": "Fleet Units",
            "key": "units",
            "align": "center",
            "style": ""
        },
        {
            "label": "Monthly Fee",
            "key": "fee",
            "align": "end",
            "style": ""
        },
        {
            "label": "Start Date",
            "key": "start",
            "align": "",
            "style": ""
        },
        {
            "label": "End Date",
            "key": "end",
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
    "sections": [
        {
            "title": "Contract",
            "fields": [
                {
                    "id": "ct-no",
                    "label": "Contract No",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ct-client",
                    "label": "Client Company",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ct-start",
                    "label": "Start Date",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ct-end",
                    "label": "End Date",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ct-units",
                    "label": "Leased Vehicle Qty",
                    "kind": "number",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ct-fee",
                    "label": "Monthly Billing AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ct-terms",
                    "label": "Payment Terms",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Net 15",
                        "Net 30",
                        "Net 45",
                        "Advance"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ct-dep",
                    "label": "Security Deposit AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Contract",
    "drawer_id": "offcanvasContract",
    "wide": True,
    "row_actions": [
        "Edit",
        "View Contract PDF",
        "Renew",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "corporate contracts"


class Screen7_3(SfaScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Quote No"
        },
        {
            "kind": "text",
            "placeholder": "Client Name"
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Draft",
                "Sent",
                "Accepted",
                "Expired"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Quote No",
            "key": "no",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Client",
            "key": "client",
            "align": "",
            "style": ""
        },
        {
            "label": "Total Vehicles",
            "key": "vehicles",
            "align": "center",
            "style": ""
        },
        {
            "label": "Net Payable",
            "key": "total",
            "align": "end",
            "style": ""
        },
        {
            "label": "Valid Until",
            "key": "valid",
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
    "sections": [
        {
            "title": "Quotation",
            "fields": [
                {
                    "id": "qt-no",
                    "label": "Quote No",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "qt-lead",
                    "label": "Client Lead",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": "employees_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "qt-valid",
                    "label": "Valid Until",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "qt-disc",
                    "label": "Discount Rate %",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "qt-currency",
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
                }
            ]
        },
        {
            "title": "Line Item",
            "fields": [
                {
                    "id": "qt-cat",
                    "label": "Vehicle Category",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": "categories_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "qt-qty",
                    "label": "Qty",
                    "kind": "number",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "qt-dur",
                    "label": "Rental Duration",
                    "kind": "number",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "qt-rate",
                    "label": "Unit Rate AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "New Quotation",
    "drawer_id": "offcanvasQuote",
    "wide": True,
    "row_actions": [
        "Print PDF",
        "Email Client",
        "Convert to Contract"
    ],
    "kpis": []
}
    awaiting = "quotations"


class Screen7_4(SfaScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Sales Agents",
            "options": [],
            "source": "employees_list"
        },
        {
            "kind": "date",
            "placeholder": "Month"
        }
    ],
    "columns": [
        {
            "label": "Agent",
            "key": "agent",
            "align": "",
            "style": ""
        },
        {
            "label": "Monthly Target",
            "key": "target",
            "align": "end",
            "style": ""
        },
        {
            "label": "Closed Deals",
            "key": "closed",
            "align": "end",
            "style": ""
        },
        {
            "label": "Base Commission",
            "key": "base",
            "align": "end",
            "style": ""
        },
        {
            "label": "Bonus",
            "key": "bonus",
            "align": "end",
            "style": ""
        },
        {
            "label": "Total Payout",
            "key": "payout",
            "align": "end",
            "style": ""
        }
    ],
    "sections": [
        {
            "title": "Commission Plan",
            "fields": [
                {
                    "id": "cm-agent",
                    "label": "Sales Agent",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": "employees_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cm-target",
                    "label": "Target Monthly Sales AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cm-base",
                    "label": "Base Commission %",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cm-tier2",
                    "label": "Tier 2 Bonus %",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cm-min",
                    "label": "Minimum Threshold AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Commission Plan",
    "drawer_id": "offcanvasCommission",
    "wide": False,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "commission plans"


class Screen7_5(SfaScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Sales Reps",
            "options": [],
            "source": "employees_list"
        },
        {
            "kind": "date",
            "placeholder": "Period"
        }
    ],
    "columns": [
        {
            "label": "Sales Rep",
            "key": "rep",
            "align": "",
            "style": ""
        },
        {
            "label": "Monthly Quota",
            "key": "quota",
            "align": "end",
            "style": ""
        },
        {
            "label": "Achieved",
            "key": "achieved",
            "align": "end",
            "style": ""
        },
        {
            "label": "Target %",
            "key": "target_pct",
            "align": "center",
            "style": ""
        },
        {
            "label": "Open Deals",
            "key": "open",
            "align": "end",
            "style": ""
        },
        {
            "label": "Win Rate %",
            "key": "win",
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
    awaiting = "pipeline figures"
