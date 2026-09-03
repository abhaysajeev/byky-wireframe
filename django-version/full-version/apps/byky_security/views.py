"""Module 15 -- System Security screens.

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
    "Security Officer",
    "Compliance Auditor"
]


class SecurityScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class SecurityPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "AES-256 Data Encryption & Key Rotation Manager",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "Session Security, 2FA & IP Whitelist Governance",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Database Backup & Disaster Recovery Orchestrator",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "PCI-DSS & GDPR Compliance Audit Manager",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "System Security Privilege Management",
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



class Screen15_1(SecurityScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Key Alias"
        },
        {
            "kind": "select",
            "label": "All Algorithms",
            "options": [
                "AES-256-GCM"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Key Alias",
            "key": "alias",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Algorithm",
            "key": "algorithm",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Active Version",
            "key": "version",
            "align": "center",
            "style": ""
        },
        {
            "label": "Rotated",
            "key": "rotated",
            "align": "",
            "style": ""
        },
        {
            "label": "HSM Bound",
            "key": "hsm",
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
            "title": "Encryption Key",
            "fields": [
                {
                    "id": "ek-alias",
                    "label": "Master Key Alias",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ek-algo",
                    "label": "Algorithm",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "AES-256-GCM"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ek-version",
                    "label": "Active Key Version",
                    "kind": "number",
                    "required": False,
                    "placeholder": "1",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ek-rotate",
                    "label": "Key Rotation Days",
                    "kind": "number",
                    "required": False,
                    "placeholder": "90",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": "30 to 180 days"
                },
                {
                    "id": "ek-hsm",
                    "label": "HSM Binding",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Bind to hardware security module",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ek-reencrypt",
                    "label": "Re-encrypt Database Fields",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Re-encrypt on rotation",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Key",
    "drawer_id": "offcanvasKey",
    "wide": True,
    "row_actions": [
        "Rotate Now",
        "Disable"
    ],
    "kpis": []
}
    awaiting = "encryption keys"


class Screen15_2(SecurityScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Rule Name"
        },
        {
            "kind": "text",
            "placeholder": "IP / CIDR"
        },
        {
            "kind": "select",
            "label": "All Access Levels",
            "options": [
                "Allow",
                "Deny"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Rule Name",
            "key": "name",
            "align": "",
            "style": "strong"
        },
        {
            "label": "IP / CIDR",
            "key": "cidr",
            "align": "",
            "style": "code"
        },
        {
            "label": "Description",
            "key": "description",
            "align": "",
            "style": "muted"
        },
        {
            "label": "Access Level",
            "key": "level",
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
            "title": "IP Whitelist",
            "fields": [
                {
                    "id": "ip-name",
                    "label": "Rule Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ip-cidr",
                    "label": "IP Address / CIDR Range",
                    "kind": "text",
                    "required": True,
                    "placeholder": "192.168.1.0/24",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ip-desc",
                    "label": "Description",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "ip-level",
                    "label": "Access Level",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Allow",
                        "Deny"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        },
        {
            "title": "2FA Policy",
            "fields": [
                {
                    "id": "tf-admin",
                    "label": "Enforce 2FA for Admin Roles",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Required for all admin roles",
                    "options": [],
                    "source": None,
                    "width": 12,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Rule",
    "drawer_id": "offcanvasIpRule",
    "wide": True,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "IP whitelist rules"


class Screen15_3(SecurityScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Backup Types",
            "options": [
                "Full",
                "Differential",
                "Transaction Log"
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
                "Completed",
                "Failed",
                "Running"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Backup ID",
            "key": "id",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Type",
            "key": "type",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Started",
            "key": "started",
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
            "label": "Size",
            "key": "size",
            "align": "end",
            "style": ""
        },
        {
            "label": "Storage",
            "key": "storage",
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
            "title": "Backup Configuration",
            "fields": [
                {
                    "id": "bk-type",
                    "label": "Backup Type",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [
                        "Full",
                        "Differential",
                        "Transaction Log"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-cron",
                    "label": "Schedule Cron",
                    "kind": "text",
                    "required": False,
                    "placeholder": "0 2 * * *",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-retention",
                    "label": "Retention Days",
                    "kind": "number",
                    "required": False,
                    "placeholder": "30",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-storage",
                    "label": "Off-Site Storage Provider",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "AWS S3",
                        "Azure Blob",
                        "Google Cloud Storage"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "bk-password",
                    "label": "Encryption Password",
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
    "add_label": "Configure Backup",
    "drawer_id": "offcanvasBackup",
    "wide": True,
    "row_actions": [
        "Restore",
        "Download",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "backup runs"


class Screen15_4(SecurityScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Scan Types",
            "options": [
                "PCI-DSS Vulnerability",
                "GDPR Data Anonymization",
                "Credit Card PAN Masking"
            ],
            "source": None
        },
        {
            "kind": "date",
            "placeholder": "Date range"
        }
    ],
    "columns": [
        {
            "label": "Scan ID",
            "key": "id",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Scan Type",
            "key": "type",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Run Date",
            "key": "date",
            "align": "",
            "style": ""
        },
        {
            "label": "Findings",
            "key": "findings",
            "align": "center",
            "style": ""
        },
        {
            "label": "Certification",
            "key": "certification",
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
            "title": "Compliance Scan",
            "fields": [
                {
                    "id": "cs-type",
                    "label": "Scan Type",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [
                        "PCI-DSS Vulnerability",
                        "GDPR Data Anonymization",
                        "Credit Card PAN Masking"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cs-customer",
                    "label": "Target Customer ID",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cs-reason",
                    "label": "Data Deletion Reason",
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
    "add_label": "Run Scan",
    "drawer_id": "offcanvasScan",
    "wide": True,
    "row_actions": [
        "View Report",
        "Export"
    ],
    "kpis": []
}
    awaiting = "compliance scans"
