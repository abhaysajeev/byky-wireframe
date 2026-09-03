"""Module 8 -- RFID Gates screens.

Generated from the FSD field tables into declarative specs; rendered through
byky/generic_screen.html so markup and spacing stay identical across modules.
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core import refdata, screens
from apps.byky_core.views import GenericScreenView, BykyScreenView
from . import data

PERMISSIONS = [
    "Access",
    "Create",
    "Read",
    "Update",
    "Approve"
]
ROLES = [
    "SuperAdmin",
    "RFID Engineer",
    "Security Officer"
]


class RfidScreen(GenericScreenView):
    def reference_lists(self):
        return refdata.lists()


class RfidPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "Station Antenna Gate Setup & IP Configuration",
        [
            True,
            True,
            True,
            True,
            True
        ]
    ],
    [
        "RFID Tag EPC Encoding & Vehicle Tagging",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "Antenna Gate Power & Frequency Calibration",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "RFID Gate Event Telemetry & Security Monitor",
        [
            True,
            False,
            True,
            False,
            False
        ]
    ],
    [
        "RFID Security Privilege Management",
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



class Screen8_1(RfidScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Antenna Code"
        },
        {
            "kind": "select",
            "label": "All Branches",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "select",
            "label": "All Directions",
            "options": [
                "Entry",
                "Exit"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Antenna Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Antenna Name",
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
            "label": "IP Address",
            "key": "ip",
            "align": "",
            "style": "code"
        },
        {
            "label": "Direction",
            "key": "direction",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Connection",
            "key": "status",
            "align": "center",
            "style": "status"
        }
    ],
    "sections": [
        {
            "title": "Antenna",
            "fields": [
                {
                    "id": "an-code",
                    "label": "Antenna Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "an-name",
                    "label": "Antenna Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "an-branch",
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
                    "id": "an-ip",
                    "label": "Reader IP Address",
                    "kind": "text",
                    "required": False,
                    "placeholder": "192.168.1.50",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "an-port",
                    "label": "TCP Port",
                    "kind": "number",
                    "required": False,
                    "placeholder": "8080",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "an-mac",
                    "label": "MAC Address",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "an-dir",
                    "label": "Gate Direction",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Entry",
                        "Exit"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "an-gain",
                    "label": "Antenna Gain dBm",
                    "kind": "number",
                    "required": False,
                    "placeholder": "20",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Antenna",
    "drawer_id": "offcanvasAntenna",
    "wide": True,
    "row_actions": [
        "Edit",
        "Test Ping",
        "Calibrate",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "antennas"


class Screen8_2(RfidScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Vehicle Code"
        },
        {
            "kind": "text",
            "placeholder": "RFID Tag EPC"
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
            "label": "Vehicle Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Vehicle Name",
            "key": "name",
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
            "label": "Tag Position",
            "key": "position",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Encoded Date",
            "key": "encoded",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Station",
            "key": "station",
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
            "title": "Tag Encoding",
            "fields": [
                {
                    "id": "tg-vehicle",
                    "label": "Vehicle",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": "subcategories_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "tg-epc",
                    "label": "Tag EPC Hex Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "10113",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "tg-pos",
                    "label": "Tag Installation Location",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Front Frame",
                        "Rear Axle",
                        "Handlebar"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Encode Tag",
    "drawer_id": "offcanvasTag",
    "wide": False,
    "row_actions": [
        "Verify Read",
        "Replace Tag",
        "Unbind"
    ],
    "kpis": []
}
    def get_rows(self):
        return data.tag_mappings()


class Screen8_3(RfidScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Antenna Code"
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
            "label": "Antenna Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "RF Power dBm",
            "key": "power",
            "align": "center",
            "style": ""
        },
        {
            "label": "RSSI Limit",
            "key": "rssi",
            "align": "center",
            "style": ""
        },
        {
            "label": "Session Mode",
            "key": "session",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Calibrated",
            "key": "date",
            "align": "",
            "style": ""
        },
        {
            "label": "Calibrated By",
            "key": "by",
            "align": "",
            "style": ""
        }
    ],
    "sections": [
        {
            "title": "Calibration",
            "fields": [
                {
                    "id": "cl-antenna",
                    "label": "Antenna",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cl-power",
                    "label": "RF Power dBm",
                    "kind": "number",
                    "required": False,
                    "placeholder": "20",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": "10 to 30 dBm"
                },
                {
                    "id": "cl-rssi",
                    "label": "RSSI Cut-Off dBm",
                    "kind": "number",
                    "required": False,
                    "placeholder": "-60",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": "-30 to -90 dBm"
                },
                {
                    "id": "cl-session",
                    "label": "Read Session Mode",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "S0",
                        "S1",
                        "S2",
                        "S3"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "cl-duty",
                    "label": "Inventory Cycle Duty Time ms",
                    "kind": "number",
                    "required": False,
                    "placeholder": "200",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Apply Calibration",
    "drawer_id": "offcanvasCalibration",
    "wide": False,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "calibration records"


class Screen8_4(RfidScreen):
    spec = {
    "filters": [
        {
            "kind": "select",
            "label": "All Branches",
            "options": [],
            "source": "branches_list"
        },
        {
            "kind": "text",
            "placeholder": "RFID Tag EPC"
        },
        {
            "kind": "select",
            "label": "All Clearance",
            "options": [
                "Authorized",
                "Alarm"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Read Time",
            "key": "time",
            "align": "",
            "style": ""
        },
        {
            "label": "Gate ID",
            "key": "gate",
            "align": "center",
            "style": ""
        },
        {
            "label": "RFID Tag EPC",
            "key": "epc",
            "align": "",
            "style": "code"
        },
        {
            "label": "Vehicle Code",
            "key": "vehicle",
            "align": "",
            "style": ""
        },
        {
            "label": "Agreement No",
            "key": "agreement",
            "align": "",
            "style": ""
        },
        {
            "label": "Clearance",
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
        "View Details",
        "Mute Siren"
    ],
    "kpis": []
}
    awaiting = "gate events"
