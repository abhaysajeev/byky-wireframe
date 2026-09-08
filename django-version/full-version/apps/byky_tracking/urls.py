from django.urls import path

from . import views

urlpatterns = [
    path(
        "tracking/gps-iot-hardware-device-registration/",
        views.Screen5_1.as_view(
            template_name="tracking_gps_iot_hardware_device_registration.html",
            screen_no="5.1",
            screen_title="GPS & IoT Hardware Device Registration",
            module_label="Tracking & Telematics",
            legacy_page="DeviceManagement.aspx",
            tier="A",
            phase=5,
            purpose="To register, configure, and manage GPS tracker hardware units, IMEI codes, SIM card numbers, telemetry transmission intervals, and remote relay kill switches.",
            layout="Form Panel (Device IMEI Code, Serial Number, SIM Card MSISDN, Cellular Operator, Ping Interval Secs, Battery Level %, Relay Immobilizer Status), DataGrid displaying registered hardware trackers.",
        ),
        name="tracking-gps-iot-hardware-device-registration",
    ),
    path(
        "tracking/vehicle-fleet-telematics-registry/",
        views.Screen5_2.as_view(
            screen_no="5.2",
            screen_title="Vehicle Fleet Telematics Registry",
            module_label="Tracking & Telematics",
            legacy_page="VehicleManagement.aspx",
            tier="A",
            phase=5,
            purpose="To bind registered GPS devices to vehicle asset codes, configure speed limit governors, set maximum geo-fence radius, and track real-time telemetry coordinates (Latitude/Longitude).",
            layout="Form Panel (Vehicle Code, Chassis / Serial No, Assigned GPS Device, Vehicle Type, Max Speed Governor KM/H, Geo-Fence Zone, Engine Status), Live Telemetry Map Widget, Fleet Registry DataGrid.",
        ),
        name="tracking-vehicle-fleet-telematics-registry",
    ),
    path(
        "tracking/vehicle-type-specification-master/",
        views.Screen5_3.as_view(
            screen_no="5.3",
            screen_title="Vehicle Type & Specification Master",
            module_label="Tracking & Telematics",
            legacy_page="VehicleTypeManagement.aspx",
            tier="A",
            phase=5,
            purpose="To define technical specifications for vehicle models (e.g., Motor Wattage, Max Range KM, Weight Capacity KG, Battery Volts/Ah, Tire Size) across vehicle categories.",
            layout="Form Panel (Type Code, Type Name, Engine/Motor Capacity, Max Range KM, Battery Voltage, Max Load KG, Category), DataGrid displaying vehicle types.",
        ),
        name="tracking-vehicle-type-specification-master",
    ),
    path(
        "tracking/tracking-security-privilege-management/",
        views.TrackingPrivileges.as_view(
            template_name="byky/partials/module_privileges.html",
            screen_no="5.4",
            screen_title="TRACKING Security Privilege Management",
            module_label="Tracking & Telematics",
            legacy_page="Privilege.aspx",
            tier="D",
            phase=5,
            purpose="To configure fine-grained role-based security permissions specifically for GPS tracking screens, telematics stream views, engine immobilizer controls, and geo-fence setups.",
            layout="Header Role Selector Dropdown, Central Privilege Checkbox Matrix Grid per TRACKING Screen, Save/Reset Action Toolbar.",
        ),
        name="tracking-tracking-security-privilege-management",
    ),
]
