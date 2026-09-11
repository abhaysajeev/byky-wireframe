"""Module 5 -- Tracking & Telematics screens.

Generated from the FSD field tables into declarative specs; rendered through
byky/generic_screen.html so markup and spacing stay identical across modules.
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core import geo, refdata, screens
from apps.byky_core.views import GenericScreenView, BykyScreenView
from apps.byky_cms import data as cms_data
from . import data

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
    "Fleet Controller",
    "Technician"
]


class TrackingScreen(GenericScreenView):
    #: screens that show the station map above their grid
    show_map = False
    map_title = "Fleet Distribution"
    map_subtitle = ""

    def reference_lists(self):
        return refdata.lists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.show_map:
            context.update(
                {
                    "show_map": True,
                    "map_data": geo.station_points(),
                    "map_title": self.map_title,
                    "map_subtitle": self.map_subtitle,
                }
            )
        return context


class TrackingPrivileges(BykyScreenView):
    """Tier D -- shared privilege matrix, parameterised by this module."""

    SCREENS = [
    [
        "GPS & IoT Hardware Device Registration",
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
        "Vehicle Fleet Telematics Registry",
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
        "Vehicle Type & Specification Master",
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
        "TRACKING Security Privilege Management",
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



class Screen5_1(TrackingScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Device IMEI"
        },
        {
            "kind": "text",
            "placeholder": "SIM MSISDN"
        },
        {
            "kind": "select",
            "label": "All Carriers",
            "options": [
                "Etisalat",
                "du",
                "Virgin Mobile"
            ],
            "source": None
        }
    ],
    "columns": [
        {
            "label": "Device IMEI",
            "key": "imei",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Serial No",
            "key": "serial",
            "align": "",
            "style": ""
        },
        {
            "label": "SIM MSISDN",
            "key": "sim",
            "align": "",
            "style": ""
        },
        {
            "label": "Carrier",
            "key": "carrier",
            "align": "",
            "style": "badge"
        },
        {
            "label": "Battery",
            "key": "battery",
            "align": "center",
            "style": ""
        },
        {
            "label": "Ping Interval",
            "key": "ping",
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
            "title": "Device",
            "fields": [
                {
                    "id": "dv-imei",
                    "label": "Device IMEI Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "dv-serial",
                    "label": "Serial Number",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "dv-sim",
                    "label": "SIM Card MSISDN",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "dv-carrier",
                    "label": "Cellular Operator",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [
                        "Etisalat",
                        "du",
                        "Virgin Mobile"
                    ],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "dv-ping",
                    "label": "Ping Interval Secs",
                    "kind": "number",
                    "required": False,
                    "placeholder": "30",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "dv-relay",
                    "label": "Relay Immobilizer",
                    "kind": "checkbox",
                    "required": False,
                    "placeholder": "Device has relay",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Register Device",
    "drawer_id": "offcanvasDevice",
    "wide": False,
    "row_actions": [
        "Edit",
        "Test Ping",
        "Cut Relay",
        "Delete"
    ],
    "kpis": []
}
    awaiting = "registered devices"


class Screen5_2(TrackingScreen):
    show_map = True
    map_title = "Fleet Distribution"
    map_subtitle = "Where the fleet sits across the network — marker size reflects vehicles held"

    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Vehicle Code"
        },
        {
            "kind": "select",
            "label": "All Vehicle Types",
            "options": [],
            "source": "subcategories_list"
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
            "label": "Vehicle Type",
            "key": "vtype",
            "align": "",
            "style": ""
        },
        {
            "label": "Chassis / Serial",
            "key": "chassis",
            "align": "",
            "style": "muted"
        },
        {
            "label": "GPS IMEI",
            "key": "imei",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Speed Limit",
            "key": "speed_limit",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Battery %",
            "key": "battery",
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
            "label": "Engine",
            "key": "engine",
            "align": "center",
            "style": "badge"
        }
    ],
    "sections": [
        {
            "title": "Fleet Registry",
            "fields": [
                {
                    "id": "fl-code",
                    "label": "Vehicle Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "fl-chassis",
                    "label": "Chassis / Serial No",
                    "kind": "text",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "fl-gps",
                    "label": "Assigned GPS Device",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "fl-type",
                    "label": "Vehicle Type",
                    "kind": "select",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": "subcategories_list",
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "fl-speed",
                    "label": "Max Speed Governor KM/H",
                    "kind": "number",
                    "required": False,
                    "placeholder": "25",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "fl-zone",
                    "label": "Geo-Fence Zone",
                    "kind": "select",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": "branches_list",
                    "width": 6,
                    "help": ""
                }
            ]
        }
    ],
    "add_label": "Add Vehicle",
    "drawer_id": "offcanvasFleet",
    "wide": True,
    "row_actions": [
        "Edit",
        "View Live Map",
        "Immobilize Engine",
        "Delete"
    ],
    "kpis": []
}
    def get_rows(self):
        return data.fleet_registry()


class Screen5_3(TrackingScreen):
    spec = {
    "filters": [
        {
            "kind": "text",
            "placeholder": "Type Code"
        },
        {
            "kind": "text",
            "placeholder": "Type Name"
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
            "label": "Type Code",
            "key": "code",
            "align": "",
            "style": "strong"
        },
        {
            "label": "Type Name",
            "key": "name",
            "align": "",
            "style": ""
        },
        {
            "label": "Fleet",
            "key": "fleet",
            "align": "center",
            "style": "badge"
        },
        {
            "label": "Motor Watts",
            "key": "motor_watts",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Max Range",
            "key": "max_range",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Battery Volts",
            "key": "voltage",
            "align": "center",
            "style": "muted"
        },
        {
            "label": "Max Load",
            "key": "max_load",
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
            "title": "Specification",
            "fields": [
                {
                    "id": "vt-code",
                    "label": "Type Code",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "vt-name",
                    "label": "Type Name",
                    "kind": "text",
                    "required": True,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "vt-cat",
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
                    "id": "vt-watts",
                    "label": "Engine / Motor Capacity (W)",
                    "kind": "number",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "vt-range",
                    "label": "Max Range KM",
                    "kind": "number",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "vt-volt",
                    "label": "Battery Voltage",
                    "kind": "number",
                    "required": False,
                    "placeholder": "",
                    "options": [],
                    "source": None,
                    "width": 6,
                    "help": ""
                },
                {
                    "id": "vt-load",
                    "label": "Max Load KG",
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
    "add_label": "Add Vehicle Type",
    "drawer_id": "offcanvasVehicleType",
    "wide": False,
    "row_actions": [
        "Edit",
        "Delete"
    ],
    "kpis": []
}
    def get_rows(self):
        return data.vehicle_types()


class AntennaScreenView(BykyScreenView):
    """FSD Module 8 (RFID & Hardware Antenna System) screens, built here per
    the follow-up instruction to implement them inside Antenna Tracking
    Management. See apps/byky_tracking/data.py's docstring for why the
    antenna dataset is populated rather than awaiting-data."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["branches_list"] = cms_data.branches()
        return context


class AntennaRegistrationView(AntennaScreenView):
    """FSD 8.1 -- Station Antenna Gate Setup & IP Configuration."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = data.antennas()
        for i, a in enumerate(rows):
            a["json_id"] = f"scr-record-antenna-{i}"
            a["fields_json"] = {
                "code": a["code"],
                "name": a["name"],
                "branch": a["branch"],
                "ip": a["ip"],
                "port": a["port"],
                "mac": a["mac"],
                "direction": a["direction"],
                "rf_power": a["rf_power"],
            }
        context.update({"antennas": rows, "counts": data.antenna_counts(rows)})
        return context


class AntennaBranchMappingView(AntennaScreenView):
    """FSD 8.1's Station Branch binding, surfaced as its own lighter mapping
    view -- same pattern as IMS's Vehicle Station Mapping being a simpler
    subset view of Vehicle Management."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = data.antennas()
        context.update({"antennas": rows, "counts": data.antenna_counts(rows)})
        return context


class RfidTagMappingView(AntennaScreenView):
    """FSD 8.2 -- RFID Tag EPC Encoding & Vehicle Tagging, reframed as
    Branch - Vehicle - RFID Tag Mapping with view and edit, per the
    follow-up instruction."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = data.vehicle_rfid_mappings()
        for i, m in enumerate(rows):
            m["json_id"] = f"scr-record-rfidmap-{i}"
            m["fields_json"] = {
                "vehicle_code": m["vehicle_code"],
                "epc": m["epc"],
                "position": "" if m["position"] == data.SHORT else m["position"],
            }
        context.update(
            {
                "mappings": rows,
                "tag_positions": data.TAG_POSITIONS,
                "counts": {"total": len(rows), "branches": len(cms_data.branches())},
            }
        )
        return context


class AntennaTrackingMonitorView(AntennaScreenView):
    """FSD 8.4 -- RFID Gate Event Telemetry & Security Monitor. Read-only;
    Online Antennas is real (derived from the antenna registry above), the
    live read-event stream has no source without an actual SignalR/gate
    feed, so it renders the awaiting-data state rather than invented
    telemetry (CLAUDE.md 12)."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = data.antennas()
        context.update(
            {
                "counts": data.antenna_counts(rows),
                "awaiting": data.AWAITING["gate_events"],
            }
        )
        return context
