"""Module 4 -- Rental Management screens.

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
    "Rental Manager",
    "Cashier",
    "Branch Manager"
]


class RmsScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class RmsPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Customer Details & Registration",
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
        "Customer Card & RFID Mapping",
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
        "Customer Sanction & Blacklist Management",
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
        "Vehicle Delivery & Pickup Location",
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
        "Rental Tariff & Fare Setup",
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
        "Sale Rates & Accessory Pricing",
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
        "Vehicle Fleet Order Allocation",
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
        "Rental Price Updates & Tariff Adjustments",
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
        "RMS Security Privilege Management",
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



class Screen4_1(RmsScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Customer Code / Name"
        },
        {
            "kind": "text",
            "placeholder": "Mobile No"
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Active",
                "Blacklisted"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Customer Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Name",
            "key": "name",
            "align": "",
            "style": ""
        },
        {
            "label": "ID Number",
            "key": "id_no",
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
            "label": "Email",
            "key": "email",
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
            "title": "Personal",
            "fields": [
                {
                    "id": "cu-first",
                    "label": "First Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-last",
                    "label": "Last Name",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-gender",
                    "label": "Gender",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Male",
                        "Female"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-dob",
                    "label": "Date of Birth",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-nat",
                    "label": "Nationality",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        },
        {
            "title": "Identification",
            "fields": [
                {
                    "id": "cu-idtype",
                    "label": "ID Type",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Emirates ID",
                        "Passport"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-idno",
                    "label": "Emirates ID / Passport No",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-lic",
                    "label": "Driving License No",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-doc",
                    "label": "Document Upload",
                    "kind": "file",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 12,
                    "help": ""
                }
            ]
        },
        {
            "title": "Contact",
            "fields": [
                {
                    "id": "cu-mobile",
                    "label": "Mobile No",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-email",
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
                    "id": "cu-addr",
                    "label": "Address",
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
    "add_label": "Add Customer",
    "drawer_id": "offcanvasAddCustomer",
    "wide": True,
    "row_actions": [
        "Edit",
        "Map Card",
        "Sanction",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "customer records"


class Screen4_2(RmsScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Card UID"
        },
        {
            "kind": "select",
            "label": "All Customers",
            "options": [],
            "source": "employees_list"
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Active",
                "Blocked",
                "Expired"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Card UID",
            "key": "uid",
            "align": "",
            "style": "code"
        },
        {
            "label": "Customer",
            "key": "customer",
            "align": "",
            "style": ""
        },
        {
            "label": "Serial No",
            "key": "serial",
            "align": "",
            "style": ""
        },
        {
            "label": "Issue Date",
            "key": "issued",
            "align": "",
            "style": ""
        },
        {
            "label": "Expiry Date",
            "key": "expiry",
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
            "title": "Card Encoding",
            "fields": [
                {
                    "id": "cd-cust",
                    "label": "Customer",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": "employees_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cd-uid",
                    "label": "Card UID / Hex Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cd-serial",
                    "label": "Card Serial No",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cd-wallet",
                    "label": "Initial Wallet Balance",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cd-issue",
                    "label": "Issue Date",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cd-expiry",
                    "label": "Expiry Date",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Issue Card",
    "drawer_id": "offcanvasIssueCard",
    "wide": False,
    "row_actions": [
        "Block",
        "Replace",
        "Unmap"
    ],
    "kpis": []
}
    awaiting = "customer cards"


class Screen4_3(RmsScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Customers",
            "options": [],
            "source": "employees_list"
        },
        {
            "kind": "select",
            "label": "All Sanction Reasons",
            "options": [
                "Damage",
                "Non-payment",
                "Traffic Offence",
                "Misuse"
            ],
            "source": None
        },
        {
            "kind": "date",
            "placeholder": "Start date"
        }
    ],
    "columns": [
        {
            "label": "Customer",
            "key": "customer",
            "align": "",
            "style": ""
        },
        {
            "label": "Emirates ID",
            "key": "eid",
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
            "label": "Reason",
            "key": "reason",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Penalty",
            "key": "penalty",
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
            "label": "Status",
            "key": "status",
            "align": "center",
            "style": "status"
        }
    ],
    "sections": [
        {
            "title": "Sanction",
            "fields": [
                {
                    "id": "sn-cust",
                    "label": "Customer",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": "employees_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sn-reason",
                    "label": "Sanction Category",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [
                        "Damage",
                        "Non-payment",
                        "Traffic Offence",
                        "Misuse",
                        "Other"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sn-penalty",
                    "label": "Penalty Amount AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sn-start",
                    "label": "Sanction Start Date",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sn-end",
                    "label": "Sanction End Date",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sn-detail",
                    "label": "Offense Reason",
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
    "add_label": "Apply Sanction",
    "drawer_id": "offcanvasSanction",
    "wide": False,
    "row_actions": [
        "Revoke",
        "Modify"
    ],
    "kpis": []
}
    awaiting = "sanctions"


class Screen4_4(RmsScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Location Code"
        },
        {
            "kind": "text",
            "placeholder": "Location Name"
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
            "label": "Location Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Location Name",
            "key": "name",
            "align": "",
            "style": ""
        },
        {
            "label": "Branch",
            "key": "branch",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Surcharge",
            "key": "fee",
            "align": "end",
            "style": ""
        },
        {
            "label": "Latitude",
            "key": "lat",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Longitude",
            "key": "lng",
            "align": "center",
            "style": "muted"
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
            "title": "Delivery Point",
            "fields": [
                {
                    "id": "dl-code",
                    "label": "Location Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "dl-name",
                    "label": "Location Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "dl-branch",
                    "label": "Station Branch",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": "branches_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "dl-fee",
                    "label": "Delivery Surcharge AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "dl-lat",
                    "label": "Latitude",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.000000",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": "-90 to +90"
                },
                {
                    "id": "dl-lng",
                    "label": "Longitude",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.000000",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": "-180 to +180"
                }
            ]
        }
    ],
    "add_label": "Add Delivery Point",
    "drawer_id": "offcanvasDelivery",
    "wide": False,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "delivery points"


class Screen4_6(RmsScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Item Code"
        },
        {
            "kind": "text",
            "placeholder": "Item Name"
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
            "label": "Cost Price",
            "key": "cost",
            "align": "end",
            "style": ""
        },
        {
            "label": "Selling Price",
            "key": "price",
            "align": "end",
            "style": ""
        },
        {
            "label": "Tax Rate",
            "key": "tax",
            "align": "center",
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
            "title": "Retail Item",
            "fields": [
                {
                    "id": "sr-code",
                    "label": "Item Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sr-name",
                    "label": "Item Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sr-cat",
                    "label": "Category",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": "categories_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sr-price",
                    "label": "Unit Selling Price AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sr-cost",
                    "label": "Cost Price AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sr-tax",
                    "label": "Tax Rate %",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sr-barcode",
                    "label": "Barcode",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Sale Rate",
    "drawer_id": "offcanvasSaleRate",
    "wide": False,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "accessory pricing"


class Screen4_7(RmsScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Order No"
        },
        {
            "kind": "select",
            "label": "All Branches",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "select",
            "label": "All Allocation Status",
            "options": [
                "Allocated",
                "Pending",
                "Released"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Order No",
            "key": "order",
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
            "label": "Vehicle Code",
            "key": "vehicle",
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
        "Reallocate",
        "Release"
    ],
    "kpis": []
}
    awaiting = "booking orders"


class Screen4_8(RmsScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Categories",
            "options": [],
            "source": "categories_list"
        },
        {
            "kind": "select",
            "label": "All Adjustment Types",
            "options": [
                "% Increase",
                "Fixed Delta"
            ],
            "source": None
        },
        {
            "kind": "date",
            "placeholder": "Effective date"
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
            "label": "Current Rate",
            "key": "current",
            "align": "end",
            "style": ""
        },
        {
            "label": "Proposed Rate",
            "key": "proposed",
            "align": "end",
            "style": ""
        },
        {
            "label": "Effective Date",
            "key": "effective",
            "align": "",
            "style": ""
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [
        "Confirm",
        "Exclude"
    ],
    "kpis": []
}
    awaiting = "price revisions"
