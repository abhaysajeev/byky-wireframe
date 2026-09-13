"""Device Management -- new module, not one of the 16 FSD modules. Requested
against the client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Device
Management" page): Device Approval (a Pending/Approved/Blocked onboarding
queue), Device Mapping (list of registered POS/handheld devices), Device
Settings (per-station print/receipt configuration) and Upload APK (the
build the fleet self-updates from) as four separate top-level screens.

Wireframe phase: no writes, no CRUD, no API -- frontend only.
"""

from apps.byky_core.views import BykyScreenView
from apps.byky_cms import data as cms_data

from . import data


class DeviceScreenView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "branches_list": cms_data.branches(),
                "companies_list": ["BYKY"],
            }
        )
        return context


class DeviceApprovalView(DeviceScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "pending_devices": data.pending_devices(),
                "approved_devices": data.approved_devices(),
                "blocked_devices": data.blocked_devices(),
                "queue_counts": data.queue_counts(),
            }
        )
        return context


class DeviceApprovalDetailView(DeviceScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mac = self.kwargs.get("mac")
        context.update(
            {
                "mac": mac,
                "device_detail": data.queue_device_detail(mac),
            }
        )
        return context


class DeviceMappingView(DeviceScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = data.devices()
        for i, d in enumerate(rows):
            d["json_id"] = f"scr-record-device-{i}"
            d["fields_json"] = {
                "device_id": d["device_id"],
                "name": d["name"],
                "mac": d["mac"],
                "station": d["station"],
            }
        context.update(
            {
                "devices": rows,
                "counts": data.counts(rows),
                "approved_unmapped": data.approved_devices(),
                "mapped_stations": {d["station"] for d in rows},
            }
        )
        return context


class DeviceSettingsView(DeviceScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "print_feed_options": data.PRINT_FEED_OPTIONS,
                "print_type_options": data.PRINT_TYPE_OPTIONS,
                "tax_type_options": data.TAX_TYPE_OPTIONS,
                "round_off_options": data.ROUND_OFF_OPTIONS,
                "round_off_limits": data.ROUND_OFF_LIMITS,
                "approval_statuses": data.APPROVAL_STATUSES,
            }
        )
        return context


class UploadApkView(DeviceScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "current_apk_version": data.APK_VERSION,
            }
        )
        return context
