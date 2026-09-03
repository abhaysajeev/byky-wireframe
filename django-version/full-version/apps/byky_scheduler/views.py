"""Module 12 -- Scheduler screens.

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
    "System Engineer"
]


class SchedulerScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class SchedulerPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Cron Job & Background Scheduler Management",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "ETL Data Pipeline & Database Sync",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Automated System Maintenance & Log Purge",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Automated Notification Queue & Dispatcher",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Scheduler Security Privilege Management",
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



class Screen12_1(SchedulerScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Job Name"
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Running",
                "Idle",
                "Failed",
                "Disabled"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Job Name",
            "key": "name",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Job Class",
            "key": "cls",
            "align": "",
            "style": "code"
        },
        {
            "label": "Cron Expression",
            "key": "cron",
            "align": "",
            "style": "code"
        },
        {
            "label": "Frequency",
            "key": "frequency",
            "align": "center",
            "style": ""
        },
        {
            "label": "Max Retries",
            "key": "retries",
            "align": "center",
            "style": ""
        },
        {
            "label": "Last Run",
            "key": "last_run",
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
            "title": "Scheduler Job",
            "fields": [
                {
                    "id": "jb-name",
                    "label": "Job Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "jb-class",
                    "label": "Job Class",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "jb-cron",
                    "label": "Cron Expression",
                    "kind": "text",
                    "required": False,
                    "placeholder": "0 */6 * * *",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "jb-freq",
                    "label": "Execution Frequency",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Hourly",
                        "Daily",
                        "Weekly",
                        "Monthly",
                        "Custom"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "jb-retries",
                    "label": "Max Retries",
                    "kind": "number",
                    "required": False,
                    "placeholder": "3",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Job",
    "drawer_id": "offcanvasJob",
    "wide": True,
    "row_actions": [
        "Edit",
        "Run Now",
        "Disable",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "scheduled jobs"


class Screen12_2(SchedulerScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Pipeline Name"
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
            "label": "Source DB",
            "key": "source",
            "align": "",
            "style": ""
        },
        {
            "label": "Target Warehouse",
            "key": "target",
            "align": "",
            "style": ""
        },
        {
            "label": "Batch Size",
            "key": "batch",
            "align": "center",
            "style": ""
        },
        {
            "label": "Sync Interval",
            "key": "interval",
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
            "title": "Data Pipeline",
            "fields": [
                {
                    "id": "pl-name",
                    "label": "Pipeline Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pl-source",
                    "label": "Source DB Connection",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pl-target",
                    "label": "Target DB Warehouse",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pl-batch",
                    "label": "Batch Size",
                    "kind": "number",
                    "required": False,
                    "placeholder": "1000",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": "1,000 to 10,000 rows"
                },
                {
                    "id": "pl-interval",
                    "label": "Sync Interval Mins",
                    "kind": "number",
                    "required": False,
                    "placeholder": "15",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "pl-script",
                    "label": "Transformation Script",
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
    "add_label": "Add Pipeline",
    "drawer_id": "offcanvasPipeline",
    "wide": True,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "data pipelines"


class Screen12_3(SchedulerScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Target Tables",
            "options": [
                "Audit Log",
                "Telemetry Log",
                "Temp Tables"
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
            "label": "Run Date",
            "key": "date",
            "align": "",
            "style": ""
        },
        {
            "label": "Target Table",
            "key": "target",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Rows Purged",
            "key": "rows",
            "align": "end",
            "style": ""
        },
        {
            "label": "Retention Days",
            "key": "retention",
            "align": "center",
            "style": ""
        },
        {
            "label": "Duration",
            "key": "duration",
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
            "title": "Maintenance Policy",
            "fields": [
                {
                    "id": "mt-retention",
                    "label": "Log Retention Days",
                    "kind": "number",
                    "required": False,
                    "placeholder": "90",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": "30 to 365 days"
                },
                {
                    "id": "mt-tables",
                    "label": "Target Tables",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Audit Log",
                        "Telemetry Log",
                        "Temp Tables"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "mt-defrag",
                    "label": "Defragment Index Threshold %",
                    "kind": "number",
                    "required": False,
                    "placeholder": "30",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "mt-time",
                    "label": "Execution Time",
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
    "add_label": "Set Policy",
    "drawer_id": "offcanvasMaintenance",
    "wide": False,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "maintenance runs"


class Screen12_4(SchedulerScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Channels",
            "options": [
                "Push",
                "SMS",
                "Email"
            ],
            "source": None
        },
        {
            "kind": "select",
            "label": "All Status",
            "options": [
                "Queued",
                "Dispatched",
                "Failed"
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
            "label": "Queue ID",
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
            "label": "Recipient",
            "key": "recipient",
            "align": "",
            "style": ""
        },
        {
            "label": "Queued At",
            "key": "queued",
            "align": "",
            "style": ""
        },
        {
            "label": "Attempts",
            "key": "attempts",
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
            "title": "Worker Threads",
            "fields": [
                {
                    "id": "wq-threads",
                    "label": "Worker Thread Count",
                    "kind": "number",
                    "required": False,
                    "placeholder": "4",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "wq-batch",
                    "label": "Dispatch Batch Size",
                    "kind": "number",
                    "required": False,
                    "placeholder": "100",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "wq-retry",
                    "label": "Retry Limit",
                    "kind": "number",
                    "required": False,
                    "placeholder": "3",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Worker Settings",
    "drawer_id": "offcanvasWorker",
    "wide": False,
    "row_actions": [
        "Retry",
        "Cancel"
    ],
    "kpis": []
}
    awaiting = "queued notifications"
