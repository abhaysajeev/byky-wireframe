from django.urls import path

from . import views

urlpatterns = [
    path(
        "device/device-mapping/",
        views.DeviceMappingView.as_view(
            template_name="device_device_mapping.html",
            screen_no="DM.1",
            screen_title="Device Mapping",
            module_label="Device Management",
            tier="A",
            purpose="Register and map POS/handheld devices to a station, tracking MAC address, APK version and the last logged-in cashier.",
        ),
        name="device-device-mapping",
    ),
    path(
        "device/device-settings/",
        views.DeviceSettingsView.as_view(
            template_name="device_device_settings.html",
            screen_no="DM.2",
            screen_title="Device Settings",
            module_label="Device Management",
            tier="A",
            purpose="Configure per-station receipt print settings, and manage device approval and the APK update package from here.",
        ),
        name="device-device-settings",
    ),
]
