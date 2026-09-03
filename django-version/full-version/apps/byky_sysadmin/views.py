"""Module 13 -- System Administration screens.

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
    "System Administrator"
]


class SysadminScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class SysadminPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Global ERP User Account Management",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "System Role & Authority Hierarchy",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Global Application Configuration & Settings",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Enterprise Audit Log & Compliance Viewer",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "System Administration Privilege Management",
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



class Screen13_1(SysadminScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Username"
        },
        {
            "kind": "select",
            "label": "All Branches",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "select",
            "label": "All Account Status",
            "options": [
                "Active",
                "Locked"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Username",
            "key": "username",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Associated Employee",
            "key": "employee",
            "align": "",
            "style": ""
        },
        {
            "label": "Assigned Role",
            "key": "role",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Branch",
            "key": "branch",
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
            "title": "Account",
            "fields": [
                {
                    "id": "us-username",
                    "label": "Username",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "us-pass",
                    "label": "Password",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "us-pass2",
                    "label": "Confirm Password",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "us-employee",
                    "label": "Associated Employee",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": "employees_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "us-role",
                    "label": "Assigned Role",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "SuperAdmin",
                        "SystemAdmin",
                        "Branch Manager",
                        "Cashier"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "us-branch",
                    "label": "Branch Station",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": "branches_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "us-status",
                    "label": "Account Status",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Active",
                        "Locked"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "us-force",
                    "label": "Force Password Change",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Require change at next login",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add User",
    "drawer_id": "offcanvasUser",
    "wide": True,
    "row_actions": [
        "Edit",
        "Lock",
        "Reset Password",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "user accounts"


class Screen13_2(SysadminScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Role Code"
        },
        {
            "kind": "text",
            "placeholder": "Role Name"
        }
    ],
    "columns": [
        {
            "label": "Role Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Role Name",
            "key": "name",
            "align": "",
            "style": ""
        },
        {
            "label": "Authority Rank",
            "key": "rank",
            "align": "center",
            "style": ""
        },
        {
            "label": "Description",
            "key": "description",
            "align": "",
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
            "title": "Role",
            "fields": [
                {
                    "id": "rl-code",
                    "label": "Role Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "rl-name",
                    "label": "Role Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "rl-rank",
                    "label": "Authority Rank Level",
                    "kind": "number",
                    "required": False,
                    "placeholder": "1",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": "1 to 10"
                },
                {
                    "id": "rl-desc",
                    "label": "Description",
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
    "add_label": "Add Role",
    "drawer_id": "offcanvasRole",
    "wide": False,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "system roles"


class Screen13_3(SysadminScreen):
    spec = {
    "filters": [],
    "columns": [
        {
            "label": "Setting",
            "key": "setting",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Value",
            "key": "value",
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
            "label": "Last Updated",
            "key": "updated",
            "align": "",
            "style": ""
        }
    ],
    "sections": [
        {
            "title": "Company Branding",
            "fields": [
                {
                    "id": "st-legal",
                    "label": "Company Legal Name",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "st-logo",
                    "label": "Logo Image",
                    "kind": "file",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "st-trn",
                    "label": "Tax Registration TRN",
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
            "title": "Financial",
            "fields": [
                {
                    "id": "st-currency",
                    "label": "Default Currency",
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
                    "id": "st-vat",
                    "label": "VAT Rate %",
                    "kind": "number",
                    "required": False,
                    "placeholder": "5.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "st-deposit",
                    "label": "Security Deposit Default AED",
                    "kind": "number",
                    "required": False,
                    "placeholder": "0.00",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        },
        {
            "title": "Security",
            "fields": [
                {
                    "id": "st-timeout",
                    "label": "Session Timeout Mins",
                    "kind": "number",
                    "required": False,
                    "placeholder": "30",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "st-pwage",
                    "label": "Max Password Age Days",
                    "kind": "number",
                    "required": False,
                    "placeholder": "90",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Edit Settings",
    "drawer_id": "offcanvasSettings",
    "wide": True,
    "row_actions": [],
    "kpis": []
}
    awaiting = "configuration values"


class Screen13_4(SysadminScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Users",
            "options": [],
            "source": "employees_list"
        },
        {
            "kind": "text",
            "placeholder": "Module / Table"
        },
        {
            "kind": "date",
            "placeholder": "Date range"
        }
    ],
    "columns": [
        {
            "label": "Timestamp",
            "key": "time",
            "align": "",
            "style": ""
        },
        {
            "label": "User",
            "key": "user",
            "align": "",
            "style": ""
        },
        {
            "label": "Module",
            "key": "module",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Action",
            "key": "action",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Target Table",
            "key": "table",
            "align": "",
            "style": "code"
        },
        {
            "label": "Record ID",
            "key": "record",
            "align": "center",
            "style": ""
        }
    ],
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [
        "View Details"
    ],
    "kpis": []
}
    awaiting = "audit log entries"
