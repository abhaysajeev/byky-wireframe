from django.urls import path

from . import views

urlpatterns = [
    path(
        "device/device-approval/",
        views.DeviceApprovalView.as_view(
            template_name="device_device_approval.html",
            screen_no="DM.3",
            screen_title="Device Approval",
            module_label="Device Management",
            tier="A",
            purpose="Review newly registered devices, approve or reject them, and manage devices already approved or blocked.",
        ),
        name="device-device-approval",
    ),
    path(
        "device/device-approval/<str:mac>/",
        views.DeviceApprovalDetailView.as_view(
            template_name="device_device_approval_detail.html",
            screen_title="Device Approval Request",
            module_label="Device Management",
            tier="A",
            purpose="Full detail of a single device registration request, read-only, with the actions its current state allows.",
        ),
        name="device-device-approval-detail",
    ),
    path(
        "device/device-mapping/",
        views.DeviceMappingView.as_view(
            template_name="device_device_mapping.html",
            screen_no="DM.1",
            screen_title="Device Mapping",
            module_label="Device Management",
            tier="A",
            purpose="Map approved devices to a station, tracking MAC address, APK version and the last logged-in cashier.",
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
            purpose="Configure per-station receipt print settings.",
        ),
        name="device-device-settings",
    ),
    path(
        "device/upload-apk/",
        views.UploadApkView.as_view(
            template_name="device_upload_apk.html",
            screen_no="DM.4",
            screen_title="Upload APK",
            module_label="Device Management",
            tier="A",
            purpose="Publish a new APK build for devices to fetch and self-update from on their next update check.",
        ),
        name="device-upload-apk",
    ),
]
