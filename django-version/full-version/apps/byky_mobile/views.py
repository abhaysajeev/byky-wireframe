"""Module 9 -- Mobile App screens.

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
    "App Administrator",
    "Support Agent"
]


class MobileScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class MobilePrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Mobile App Home & Vehicle Catalog",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "Mobile Vehicle Booking & Station Selection",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Mobile Customer Wallet & Payment Checkout",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Mobile Active Rental Telemetry & Unlock",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Mobile Loyalty Rewards & Coupon Redemption",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Mobile Customer Account & Document Upload",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "RmsResponsive Mobile App Privilege Management",
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



class Screen9_1(MobileScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Stations",
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
            "label": "Model",
            "key": "model",
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
            "label": "Battery %",
            "key": "battery",
            "align": "center",
            "style": ""
        },
        {
            "label": "Max Range KM",
            "key": "range",
            "align": "center",
            "style": ""
        },
        {
            "label": "Hourly Rate",
            "key": "rate",
            "align": "end",
            "style": ""
        },
        {
            "label": "Station",
            "key": "station",
            "align": "",
            "style": ""
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [
        "Book Now",
        "View Specs"
    ],
    "kpis": []
}
    awaiting = "catalog entries"


class Screen9_2(MobileScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "Pickup Station",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "select",
            "label": "Dropoff Station",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "date",
            "placeholder": "Rental date"
        }
    ],
    "columns": [
        {
            "label": "Line Item",
            "key": "item",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Description",
            "key": "description",
            "align": "",
            "style": ""
        },
        {
            "label": "Amount AED",
            "key": "amount",
            "align": "end",
            "style": ""
        }
    ],
    "sections": [
        {
            "title": "Booking",
            "fields": [
                {
                    "id": "bk-pickup",
                    "label": "Pickup Station",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": "branches_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-dropoff",
                    "label": "Dropoff Station",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": "branches_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-date",
                    "label": "Rental Date",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-start",
                    "label": "Start Time",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-duration",
                    "label": "Duration",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "1 hour",
                        "2 hours",
                        "Half day",
                        "Full day"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-helmet",
                    "label": "Add Helmet",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Include helmet",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-seat",
                    "label": "Add Child Seat",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Include child seat",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-promo",
                    "label": "Promo Code",
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
    "add_label": "New Booking",
    "drawer_id": "offcanvasBooking",
    "wide": False,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "bookings"


class Screen9_3(MobileScreen):
    spec = {
    "filters": [
        {
            "kind": "date",
            "placeholder": "Date range"
        },
        {
            "kind": "select",
            "label": "All Types",
            "options": [
                "Top-Up",
                "Rental",
                "Refund"
            ],
            "source": None
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Completed",
                "Pending",
                "Failed"
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
            "label": "Status",
            "key": "status",
            "align": "center",
            "style": "status"
        }
    ],
    "sections": [
        {
            "title": "Wallet Top-Up",
            "fields": [
                {
                    "id": "wt-amount",
                    "label": "Custom Amount AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "wt-method",
                    "label": "Payment Method",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Apple Pay",
                        "Credit Card",
                        "Wallet Balance"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Top Up Wallet",
    "drawer_id": "offcanvasTopUp",
    "wide": False,
    "row_actions": [
        "View PDF Receipt"
    ],
    "kpis": []
}
    awaiting = "wallet transactions"


class Screen9_4(MobileScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Agreement No"
        },
        {
            "kind": "select",
            "label": "All Stations",
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
            "label": "Start Time",
            "key": "start",
            "align": "",
            "style": ""
        },
        {
            "label": "Elapsed",
            "key": "elapsed",
            "align": "center",
            "style": ""
        },
        {
            "label": "Current Speed",
            "key": "speed",
            "align": "center",
            "style": ""
        },
        {
            "label": "Battery %",
            "key": "battery",
            "align": "center",
            "style": ""
        },
        {
            "label": "Fare Accrued",
            "key": "fare",
            "align": "end",
            "style": ""
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [
        "Unlock Vehicle",
        "Pause Ride",
        "End Ride"
    ],
    "kpis": []
}
    awaiting = "live ride telemetry"


class Screen9_5(MobileScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Offer"
        },
        {
            "kind": "select",
            "label": "All Tiers",
            "options": [
                "Bronze",
                "Silver",
                "Gold",
                "Platinum"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Offer",
            "key": "offer",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Description",
            "key": "description",
            "align": "",
            "style": ""
        },
        {
            "label": "Points Cost",
            "key": "points",
            "align": "center",
            "style": ""
        },
        {
            "label": "AED Value",
            "key": "value",
            "align": "end",
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
        "Redeem Points",
        "Claim Voucher"
    ],
    "kpis": []
}
    awaiting = "reward offers"


class Screen9_6(MobileScreen):
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
            "label": "All Verification Status",
            "options": [
                "Verified",
                "Pending",
                "Rejected"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Document Type",
            "key": "doc_type",
            "align": "",
            "style": "strong"
        },
        {
            "label": "File Name",
            "key": "filename",
            "align": "",
            "style": ""
        },
        {
            "label": "Uploaded",
            "key": "uploaded",
            "align": "",
            "style": ""
        },
        {
            "label": "Verification",
            "key": "status",
            "align": "center",
            "style": "status"
        }
    ],
    "sections": [
        {
            "title": "Contact",
            "fields": [
                {
                    "id": "mp-mobile",
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
                    "id": "mp-email",
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
                    "id": "mp-address",
                    "label": "Address",
                    "kind": "textarea",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 12,
                    "help": ""
                },
                {
                    "id": "mp-licence",
                    "label": "Driving License No",
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
            "title": "Documents",
            "fields": [
                {
                    "id": "mp-front",
                    "label": "Emirates ID Front",
                    "kind": "file",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "mp-back",
                    "label": "Emirates ID Back",
                    "kind": "file",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "mp-licence-scan",
                    "label": "Driving License Scan",
                    "kind": "file",
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
    "add_label": "Upload Documents",
    "drawer_id": "offcanvasDocs",
    "wide": True,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "customer documents"
