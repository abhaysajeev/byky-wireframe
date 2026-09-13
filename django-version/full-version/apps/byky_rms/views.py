"""Module 4 -- Rental Management screens.

Generated from the FSD field tables into declarative specs; rendered through
byky/generic_screen.html so markup and spacing stay identical across modules.
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core import privileges, refdata, screens
from apps.byky_core.views import GenericScreenView, BykyScreenView


# Row 57 of the client's feedback doc: Customer's Nationality field becomes a
# full country dropdown -- real country names, not client data, so a
# standard reference list is fine to hardcode rather than invented.
COUNTRIES = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    "Argentina", "Armenia", "Australia", "Austria", "Azerbaijan",
    "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus",
    "Belgium", "Belize", "Benin", "Bhutan", "Bolivia",
    "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cambodia", "Cameroon", "Canada",
    "Chad", "Chile", "China", "Colombia", "Comoros",
    "Congo", "Costa Rica", "Croatia", "Cuba", "Cyprus",
    "Czech Republic", "Denmark", "Djibouti", "Dominican Republic", "Ecuador",
    "Egypt", "El Salvador", "Eritrea", "Estonia", "Eswatini",
    "Ethiopia", "Fiji", "Finland", "France", "Gabon",
    "Gambia", "Georgia", "Germany", "Ghana", "Greece",
    "Guatemala", "Guinea", "Guyana", "Haiti", "Honduras",
    "Hungary", "Iceland", "India", "Indonesia", "Iran",
    "Iraq", "Ireland", "Israel", "Italy", "Ivory Coast",
    "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya",
    "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon",
    "Lesotho", "Liberia", "Libya", "Liechtenstein", "Lithuania",
    "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives",
    "Mali", "Malta", "Mauritania", "Mauritius", "Mexico",
    "Moldova", "Monaco", "Mongolia", "Montenegro", "Morocco",
    "Mozambique", "Myanmar", "Namibia", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
    "North Macedonia", "Norway", "Oman", "Pakistan", "Panama",
    "Papua New Guinea", "Paraguay", "Peru", "Philippines", "Poland",
    "Portugal", "Qatar", "Romania", "Russia", "Rwanda",
    "Saudi Arabia", "Senegal", "Serbia", "Seychelles", "Sierra Leone",
    "Singapore", "Slovakia", "Slovenia", "Somalia", "South Africa",
    "South Korea", "South Sudan", "Spain", "Sri Lanka", "Sudan",
    "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan",
    "Tajikistan", "Tanzania", "Thailand", "Togo", "Trinidad and Tobago",
    "Tunisia", "Turkey", "Turkmenistan", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
    "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe",
]

# Row 57: Contact No splits into [Country Code] + [Phone No] -- a shortlist
# of GCC/common codes rather than every dialling code, since the ask is the
# two-part split, not an exhaustive registry.
COUNTRY_CODES = [
    "+971 (UAE)", "+966 (Saudi Arabia)", "+974 (Qatar)", "+973 (Bahrain)",
    "+968 (Oman)", "+965 (Kuwait)", "+91 (India)", "+92 (Pakistan)",
    "+20 (Egypt)", "+44 (UK)", "+1 (USA)",
]


PERMISSIONS = [
    "Access",
    "Create",
    "Read",
    "Update",
    "Approve",
    "Delete"
]


class RmsScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class RmsPrivileges(BykyScreenView):
    """Tier D -- roles list + per-role screen permission matrix. See
    apps/byky_core/privileges.py for the shared role master and defaults;
    screens come live from the sidebar's Rental group."""

    SLUG = "rms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screens = privileges.module_screens(self.SLUG)
        context.update(
            {
                "permissions": PERMISSIONS,
                "roles": privileges.ROLES,
                "mapped_roles": privileges.DEFAULT_MAPPED_ROLES,
                "admin_roles": privileges.ADMIN_ROLES,
                "screens": screens,
                "role_matrices": privileges.role_matrices(privileges.ROLES, screens, PERMISSIONS),
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
                        "Female",
                        "Others"
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
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": COUNTRIES,
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
                        "Passport",
                        "Driving License",
                        "Others"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-idno",
                    "label": "Document No",
                    "kind": "text",
                    "required": True,
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
                    "id": "cu-mobile-code",
                    "label": "Country Code",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": COUNTRY_CODES,
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cu-mobile",
                    "label": "Phone No",
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
                    "id": "cu-remarks",
                    "label": "Remarks",
                    "kind": "textarea",
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

    # Row 57: 5 demo customer records reflecting the redesigned field set --
    # illustrative, added at the user's own explicit request for this
    # screen (not the app's usual "leave empty, no source data" default),
    # using example.com email addresses and non-sequential-looking ID
    # numbers so nothing reads as a real person's document.
    def get_rows(self):
        customers = [
            {
                "code": "CU001", "first": "Ahmed", "last": "Al Mansoori", "gender": "Male",
                "dob": "14 May 1990", "nat": "United Arab Emirates",
                "idtype": "Emirates ID", "idno": "784-1990-1234567-1",
                "mobile_code": "+971 (UAE)", "mobile": "501234567",
                "email": "ahmed.almansoori@example.com", "addr": "Dubai, UAE",
                "remarks": "", "status": "Active",
            },
            {
                "code": "CU002", "first": "Priya", "last": "Nair", "gender": "Female",
                "dob": "02 Nov 1988", "nat": "India",
                "idtype": "Passport", "idno": "P1234567",
                "mobile_code": "+91 (India)", "mobile": "9876543210",
                "email": "priya.nair@example.com", "addr": "Sharjah, UAE",
                "remarks": "", "status": "Active",
            },
            {
                "code": "CU003", "first": "Robert", "last": "Chen", "gender": "Male",
                "dob": "21 Jul 1995", "nat": "United States",
                "idtype": "Driving License", "idno": "DL-84213",
                "mobile_code": "+1 (USA)", "mobile": "2025550123",
                "email": "robert.chen@example.com", "addr": "Abu Dhabi, UAE",
                "remarks": "", "status": "Active",
            },
            {
                "code": "CU004", "first": "Fatima", "last": "Hassan", "gender": "Female",
                "dob": "09 Mar 1992", "nat": "Egypt",
                "idtype": "Emirates ID", "idno": "784-1992-7654321-2",
                "mobile_code": "+20 (Egypt)", "mobile": "1001234567",
                "email": "fatima.hassan@example.com", "addr": "Dubai, UAE",
                "remarks": "Repeated late returns", "status": "Blacklisted",
            },
            {
                "code": "CU005", "first": "Alex", "last": "Rivera", "gender": "Others",
                "dob": "30 Dec 1997", "nat": "United Kingdom",
                "idtype": "Others", "idno": "ID-99201",
                "mobile_code": "+44 (UK)", "mobile": "7700900123",
                "email": "alex.rivera@example.com", "addr": "Ras Al Khaimah, UAE",
                "remarks": "", "status": "Active",
            },
        ]
        rows = []
        for i, c in enumerate(customers):
            row = dict(c)
            row["name"] = f"{c['first']} {c['last']}"
            row["id_no"] = c["idno"]
            row["mobile_display"] = f"{c['mobile_code'].split(' ')[0]} {c['mobile']}"
            row["json_id"] = f"scr-record-customer-{i}"
            row["fields_json"] = {
                "cu-first": c["first"],
                "cu-last": c["last"],
                "cu-gender": c["gender"],
                "cu-dob": c["dob"],
                "cu-nat": c["nat"],
                "cu-idtype": c["idtype"],
                "cu-idno": c["idno"],
                "cu-mobile-code": c["mobile_code"],
                "cu-mobile": c["mobile"],
                "cu-email": c["email"],
                "cu-remarks": c["remarks"],
                "cu-addr": c["addr"],
            }
            rows.append(row)
        return rows


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
