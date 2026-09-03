"""Module 14 -- Mobile API screens.

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
    "API Administrator"
]


class ApiScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class ApiPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Mobile REST API Gateway & Route Registry",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "JWT Security Token & OAuth Authentication Service",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "FCM & APNS Mobile Push Dispatch Engine",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Third-Party API Webhook & Partner Integration",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Mobile API Security Privilege Management",
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



class Screen14_1(ApiScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Route Name"
        },
        {
            "kind": "select",
            "label": "All Verbs",
            "options": [
                "GET",
                "POST",
                "PUT",
                "DELETE"
            ],
            "source": None
        },
        {
            "kind": "select",
            "label": "All Versions",
            "options": [
                "v1",
                "v2"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Route Name",
            "key": "name",
            "align": "",
            "style": "strong"
        },
        {
            "label": "HTTP Verb",
            "key": "verb",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Controller Route",
            "key": "route",
            "align": "",
            "style": "code"
        },
        {
            "label": "Version",
            "key": "version",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Rate Limit",
            "key": "rate",
            "align": "center",
            "style": ""
        },
        {
            "label": "Requires Auth",
            "key": "auth",
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
            "title": "Endpoint",
            "fields": [
                {
                    "id": "ep-name",
                    "label": "Endpoint Route Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ep-verb",
                    "label": "HTTP Verb",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [
                        "GET",
                        "POST",
                        "PUT",
                        "DELETE"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ep-route",
                    "label": "Controller Route",
                    "kind": "text",
                    "required": False,
                    "placeholder": "/api/v1/vehicles",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ep-version",
                    "label": "Version",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "v1",
                        "v2"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ep-rate",
                    "label": "Rate Limit Req/Min",
                    "kind": "number",
                    "required": False,
                    "placeholder": "60",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ep-auth",
                    "label": "Requires Auth",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Bearer token required",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Register Route",
    "drawer_id": "offcanvasRoute",
    "wide": True,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "API routes"


class Screen14_2(ApiScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Users",
            "options": [],
            "source": "employees_list"
        },
        {
            "kind": "select",
            "label": "All Token Status",
            "options": [
                "Active",
                "Revoked",
                "Expired"
            ],
            "source": None
        },
        {
            "kind": "date",
            "placeholder": "Issued"
        }
    ],
    "columns": [
        {
            "label": "Token ID",
            "key": "id",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Subject",
            "key": "subject",
            "align": "",
            "style": ""
        },
        {
            "label": "Issued At",
            "key": "issued",
            "align": "",
            "style": ""
        },
        {
            "label": "Expires At",
            "key": "expires",
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
            "title": "JWT Configuration",
            "fields": [
                {
                    "id": "jw-secret",
                    "label": "JWT Secret Key",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "jw-access",
                    "label": "Access Token TTL Mins",
                    "kind": "number",
                    "required": False,
                    "placeholder": "15",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "jw-refresh",
                    "label": "Refresh Token TTL Days",
                    "kind": "number",
                    "required": False,
                    "placeholder": "30",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "jw-rotate",
                    "label": "Rotate Refresh Tokens",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Rotate on use",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Token Policy",
    "drawer_id": "offcanvasToken",
    "wide": False,
    "row_actions": [
        "Revoke Token"
    ],
    "kpis": []
}
    awaiting = "active token sessions"


class Screen14_3(ApiScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Channels",
            "options": [
                "FCM Android",
                "APNs iOS"
            ],
            "source": None
        },
        {
            "kind": "date",
            "placeholder": "Date range"
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Delivered",
                "Failed"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Dispatch ID",
            "key": "id",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Channel",
            "key": "channel",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Title",
            "key": "title",
            "align": "",
            "style": ""
        },
        {
            "label": "Sent",
            "key": "sent",
            "align": "",
            "style": ""
        },
        {
            "label": "Delivered",
            "key": "delivered",
            "align": "center",
            "style": ""
        },
        {
            "label": "Failed",
            "key": "failed",
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
            "title": "Push Channel",
            "fields": [
                {
                    "id": "pu-channel",
                    "label": "Push Channel",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [
                        "FCM Android",
                        "APNs iOS"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pu-bundle",
                    "label": "App Bundle ID",
                    "kind": "text",
                    "required": False,
                    "placeholder": "com.byky.app",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pu-key",
                    "label": "Server Key / Auth Certificate",
                    "kind": "file",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pu-keyid",
                    "label": "Key ID",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pu-team",
                    "label": "Team ID",
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
    "add_label": "Configure Channel",
    "drawer_id": "offcanvasPush",
    "wide": True,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "push dispatches"


class Screen14_4(ApiScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Partner Name"
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Active",
                "Disabled"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Partner",
            "key": "partner",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Callback URL",
            "key": "url",
            "align": "",
            "style": "code"
        },
        {
            "label": "Event Subscriptions",
            "key": "events",
            "align": "",
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
            "title": "Partner Integration",
            "fields": [
                {
                    "id": "pi-name",
                    "label": "Partner Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pi-url",
                    "label": "Webhook Callback URL",
                    "kind": "text",
                    "required": True,
                    "placeholder": "https://",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pi-secret",
                    "label": "Secret Signing Key",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pi-events",
                    "label": "Event Subscriptions",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Booking Created",
                        "Trip Ended",
                        "Payment Settled"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Partner",
    "drawer_id": "offcanvasPartner",
    "wide": True,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "webhook partners"
