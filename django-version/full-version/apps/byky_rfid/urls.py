from django.urls import path

from . import views

urlpatterns = [
    path(
        "rfid/station-antenna-gate-setup-ip-configuration/",
        views.Screen8_1.as_view(
            screen_no="8.1",
            screen_title="Station Antenna Gate Setup & IP Configuration",
            module_label="RFID Gates",
            legacy_page="StationAntennaManagement.aspx",
            tier="A",
            phase=6,
            purpose="To configure UHF RFID reader hardware units, gate antenna IDs, IP addresses, TCP ports, MAC addresses, gate orientation (Entry Gate / Exit Gate), and station branch bindings.",
            layout="Form Panel (Antenna Code, Antenna Name, Station Branch, Reader IP Address, TCP Port, MAC Address, Gate Direction [Entry/Exit], Antenna Gain dBm), Configured Station Antennas DataGrid.",
        ),
        name="rfid-station-antenna-gate-setup-ip-configuration",
    ),
    path(
        "rfid/rfid-tag-epc-encoding-vehicle-tagging/",
        views.Screen8_2.as_view(
            screen_no="8.2",
            screen_title="RFID Tag EPC Encoding & Vehicle Tagging",
            module_label="RFID Gates",
            legacy_page="RfidTagMapping.aspx",
            tier="A",
            phase=6,
            purpose="To program, encode, and physically bind 24-character hexadecimal UHF RFID Gen2 EPC tags to vehicle inventory units (bicycles, e-scooters, quad bikes).",
            layout="Vehicle Selection Dropdown, Desktop RFID Encoder Integration Panel, Tag EPC Hex Code Input, Tag Installation Location (Front Frame, Rear Axle, Handlebar), Active Mapped RFID Tags DataGrid.",
        ),
        name="rfid-rfid-tag-epc-encoding-vehicle-tagging",
    ),
    path(
        "rfid/antenna-gate-power-frequency-calibration/",
        views.Screen8_3.as_view(
            screen_no="8.3",
            screen_title="Antenna Gate Power & Frequency Calibration",
            module_label="RFID Gates",
            legacy_page="AntennaCalibration.aspx",
            tier="B",
            phase=6,
            purpose="To calibrate RF transmit power output (10 to 30 dBm), RSSI sensitivity thresholds, hopping frequency channels, and anti-collision read parameters for station antenna gates.",
            layout="Antenna Selector Header, Calibration Control Panel (RF Power Slider 10-30 dBm, RSSI Cut-Off Slider -30 to -90 dBm, Read Session Mode [S0/S1/S2/S3], Inventory Cycle Duty Time ms), Real-Time RSSI Gauge, Calibration Log DataGrid.",
        ),
        name="rfid-antenna-gate-power-frequency-calibration",
    ),
    path(
        "rfid/rfid-gate-event-telemetry-security-monitor/",
        views.Screen8_4.as_view(
            screen_no="8.4",
            screen_title="RFID Gate Event Telemetry & Security Monitor",
            module_label="RFID Gates",
            legacy_page="RfidGateMonitor.aspx",
            tier="C",
            phase=6,
            purpose="To display real-time live RFID tag read streams at station entry/exit gates, audit gate clearance events, and trigger audible security sirens for un-cleared vehicle movements.",
            layout="Station Branch Selection Header, Gate Status Summary Cards (Online Antennas, Total Reads Today, Unauthorized Alarms Today), Real-Time Tag Event Stream Grid (AJAX / SignalR), Security Siren Controls.",
        ),
        name="rfid-rfid-gate-event-telemetry-security-monitor",
    ),
    path(
        "rfid/rfid-security-privilege-management/",
        views.RfidPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="8.5",
            screen_title="RFID Security Privilege Management",
            module_label="RFID Gates",
            legacy_page="RfidPrivilege.aspx",
            tier="D",
            phase=6,
            purpose="To configure fine-grained role-based security permissions specifically for RFID tag encoding, antenna gate IP configuration, RF power calibration, and security siren override rights.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per RFID Screen, Save/Reset Action Toolbar.",
        ),
        name="rfid-rfid-security-privilege-management",
    ),
]
