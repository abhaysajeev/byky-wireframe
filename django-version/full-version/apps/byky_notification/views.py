"""Module 10 -- Notifications screens.

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
    "Communications Manager"
]


class NotificationScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class NotificationPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Notification Broadcasting & Template Master",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "System Security Alert Dispatch & Monitoring",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "SMS Gateway Provider & Gateway Configuration",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Email SMTP Server & HTML Template Setup",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Notification Security Privilege Management",
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



class Screen10_1(NotificationScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Title"
        },
        {
            "kind": "select",
            "label": "All Audiences",
            "options": [
                "All App Users",
                "Active Renters",
                "VIP Customers"
            ],
            "source": None
        },
        {
            "kind": "select",
            "label": "All Channels",
            "options": [
                "Mobile Push",
                "SMS",
                "Email"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Notification ID",
            "key": "id",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Title",
            "key": "title",
            "align": "",
            "style": ""
        },
        {
            "label": "Audience",
            "key": "audience",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Channel",
            "key": "channel",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Sent Count",
            "key": "sent",
            "align": "center",
            "style": ""
        },
        {
            "label": "Sent Date",
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
    "sections": [
        {
            "title": "Broadcast",
            "fields": [
                {
                    "id": "nt-title",
                    "label": "Title",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "nt-audience",
                    "label": "Target Audience",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [
                        "All App Users",
                        "Active Renters",
                        "VIP Customers"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "nt-channel",
                    "label": "Channel",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [
                        "Mobile Push",
                        "SMS",
                        "Email"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "nt-template",
                    "label": "Template",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "nt-schedule",
                    "label": "Scheduled Time",
                    "kind": "date",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "nt-body",
                    "label": "Message Body",
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
    "add_label": "New Broadcast",
    "drawer_id": "offcanvasBroadcast",
    "wide": True,
    "row_actions": [
        "View Analytics",
        "Resend"
    ],
    "kpis": []
}
    awaiting = "broadcasts"


class Screen10_2(NotificationScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Severity",
            "options": [
                "Critical",
                "Warning",
                "Info"
            ],
            "source": None
        },
        {
            "kind": "text",
            "placeholder": "Alert Type"
        },
        {
            "kind": "date",
            "placeholder": "Date range"
        }
    ],
    "columns": [
        {
            "label": "Alert ID",
            "key": "id",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Timestamp",
            "key": "time",
            "align": "",
            "style": ""
        },
        {
            "label": "Severity",
            "key": "severity",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Alert Type",
            "key": "type",
            "align": "",
            "style": ""
        },
        {
            "label": "Vehicle / Gate",
            "key": "source",
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
            "label": "Resolution",
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
        "Acknowledge",
        "Dismiss"
    ],
    "kpis": []
}
    awaiting = "security alerts"


class Screen10_3(NotificationScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Provider Name"
        },
        {
            "kind": "text",
            "placeholder": "Sender ID"
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
            "label": "API URL",
            "key": "url",
            "align": "",
            "style": "code"
        },
        {
            "label": "Sender ID",
            "key": "sender",
            "align": "",
            "style": ""
        },
        {
            "label": "Daily Quota",
            "key": "quota",
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
            "title": "SMS Gateway",
            "fields": [
                {
                    "id": "sg-provider",
                    "label": "Provider Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sg-url",
                    "label": "Gateway API URL",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sg-key",
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
                    "id": "sg-secret",
                    "label": "API Secret",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sg-sender",
                    "label": "Sender ID",
                    "kind": "text",
                    "required": False,
                    "placeholder": "BYKY-RENT",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sg-quota",
                    "label": "Max Daily Quota",
                    "kind": "number",
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
    "add_label": "Add Gateway",
    "drawer_id": "offcanvasSmsGateway",
    "wide": True,
    "row_actions": [
        "Edit",
        "Test SMS Dispatch",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "SMS gateways"


class Screen10_4(NotificationScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Template Code"
        },
        {
            "kind": "text",
            "placeholder": "Subject Line"
        }
    ],
    "columns": [
        {
            "label": "Template Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Template Name",
            "key": "name",
            "align": "",
            "style": ""
        },
        {
            "label": "Subject",
            "key": "subject",
            "align": "",
            "style": ""
        },
        {
            "label": "Last Updated",
            "key": "updated",
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
            "title": "SMTP Server",
            "fields": [
                {
                    "id": "sm-host",
                    "label": "SMTP Host",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sm-port",
                    "label": "SMTP Port",
                    "kind": "number",
                    "required": False,
                    "placeholder": "587",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sm-ssl",
                    "label": "Enable SSL",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Use SSL/TLS",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sm-user",
                    "label": "Username",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sm-pass",
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
                    "id": "sm-from",
                    "label": "From Email",
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
            "title": "HTML Template",
            "fields": [
                {
                    "id": "sm-code",
                    "label": "Template Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sm-subject",
                    "label": "Template Subject",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sm-body",
                    "label": "HTML Body",
                    "kind": "textarea",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 12,
                    "help": "Parameter tags: {CustomerName}, {AgreementNo}, {RentalFee}"
                }
            ]
        }
    ],
    "add_label": "Add Template",
    "drawer_id": "offcanvasEmailTemplate",
    "wide": True,
    "row_actions": [
        "Edit",
        "Preview HTML",
        "Test Email",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "email templates"
