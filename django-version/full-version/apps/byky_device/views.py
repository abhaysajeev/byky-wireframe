"""Device Management -- new module, not one of the 16 FSD modules. Requested
against the client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Device
Management" page): Device Mapping (list of registered POS/handheld devices)
and Device Settings (per-station print/receipt configuration, with Device
Approval and Upload APK folded into a header action menu rather than kept as
separate top-level screens, per the follow-up instruction).

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
            }
        )
        return context


class DeviceSettingsView(DeviceScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = data.devices()
        context.update(
            {
                "devices": rows,
                "print_feed_options": data.PRINT_FEED_OPTIONS,
                "print_type_options": data.PRINT_TYPE_OPTIONS,
                "tax_type_options": data.TAX_TYPE_OPTIONS,
                "round_off_options": data.ROUND_OFF_OPTIONS,
                "round_off_limits": data.ROUND_OFF_LIMITS,
                "approval_statuses": data.APPROVAL_STATUSES,
            }
        )
        return context
