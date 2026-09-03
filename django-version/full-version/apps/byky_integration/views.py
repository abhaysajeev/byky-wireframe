"""Module 16 -- Integration screens.

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
    "Integration Engineer"
]


class IntegrationScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class IntegrationPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Global Master Data Synchronization & Replication",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "Data Warehouse Schema & Analytical Datamarts",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Third-Party Enterprise API Connectors",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Global System Health & Performance Dashboard",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Final Integration Security Privilege Management",
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



class Screen16_1(IntegrationScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Data Domains",
            "options": [
                "Customer",
                "Vehicle",
                "Fare",
                "RFID"
            ],
            "source": None
        },
        {
            "kind": "select",
            "label": "All Sync Modes",
            "options": [
                "Real-Time CDC",
                "Batch"
            ],
            "source": None
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Active",
                "Paused",
                "Failed"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Pipeline",
            "key": "name",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Source Node",
            "key": "source",
            "align": "",
            "style": ""
        },
        {
            "label": "Target Node",
            "key": "target",
            "align": "",
            "style": ""
        },
        {
            "label": "Data Domain",
            "key": "domain",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Sync Mode",
            "key": "mode",
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
            "title": "Replication",
            "fields": [
                {
                    "id": "sy-source",
                    "label": "Source Node",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sy-target",
                    "label": "Target Node",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sy-domain",
                    "label": "Data Domain",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Customer",
                        "Vehicle",
                        "Fare",
                        "RFID"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sy-mode",
                    "label": "Sync Mode",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Real-Time CDC",
                        "Batch"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "sy-conflict",
                    "label": "Re-Sync Conflict Rule",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Master Wins",
                        "Target Wins"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Pipeline",
    "drawer_id": "offcanvasSync",
    "wide": True,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "replication pipelines"


class Screen16_2(IntegrationScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Object Types",
            "options": [
                "Fact Table",
                "Dimension Table",
                "Aggregate Datamart"
            ],
            "source": None
        },
        {
            "kind": "date",
            "placeholder": "Last refresh"
        }
    ],
    "columns": [
        {
            "label": "Object Name",
            "key": "name",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Object Type",
            "key": "type",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Row Count",
            "key": "rows",
            "align": "end",
            "style": ""
        },
        {
            "label": "Last Refresh",
            "key": "refreshed",
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
    "add_label": "Process Cube",
    "drawer_id": "offcanvasCube",
    "wide": False,
    "row_actions": [
        "Full Process",
        "Incremental Process"
    ],
    "kpis": []
}
    awaiting = "warehouse objects"


class Screen16_3(IntegrationScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Connector Name"
        },
        {
            "kind": "select",
            "label": "All Systems",
            "options": [
                "SAP",
                "Oracle",
                "Dynamics",
                "RTA"
            ],
            "source": None
        },
        {
            "kind": "select",
            "label": "All Auth Types",
            "options": [
                "OAuth2",
                "SAML",
                "Mutual TLS"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Connector",
            "key": "name",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Enterprise System",
            "key": "system",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Endpoint Base URL",
            "key": "url",
            "align": "",
            "style": "code"
        },
        {
            "label": "Auth Type",
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
            "title": "Connector",
            "fields": [
                {
                    "id": "cn-name",
                    "label": "Connector Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cn-system",
                    "label": "Enterprise System",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [
                        "SAP",
                        "Oracle",
                        "Dynamics",
                        "RTA"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cn-url",
                    "label": "Endpoint Base URL",
                    "kind": "text",
                    "required": False,
                    "placeholder": "https://",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cn-client",
                    "label": "Client Credentials",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cn-auth",
                    "label": "Auth Type",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "OAuth2",
                        "SAML",
                        "Mutual TLS"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Connector",
    "drawer_id": "offcanvasConnector",
    "wide": True,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "connectors"


class Screen16_4(IntegrationScreen):
    spec = {
    "filters": [
        {
            "kind": "date",
            "placeholder": "Time window"
        }
    ],
    "columns": [
        {
            "label": "Module",
            "key": "module",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Health",
            "key": "health",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Active Sessions",
            "key": "sessions",
            "align": "center",
            "style": ""
        },
        {
            "label": "DB Response ms",
            "key": "db",
            "align": "center",
            "style": ""
        },
        {
            "label": "API Latency ms",
            "key": "api",
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
    "sections": [],
    "add_label": None,
    "drawer_id": "offcanvasAdd",
    "wide": False,
    "row_actions": [],
    "kpis": []
}
    awaiting = "health metrics"
