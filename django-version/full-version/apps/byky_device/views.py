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
    """Row 50 of the client's feedback doc: the Add Device Mapping drawer
    is converted off its old hand-rolled .scr-drawer markup onto the shared
    byky/partials/drawer.html component -- spec.scr_name keeps the existing
    data-scr-open="device:add|edit" triggers and edit-mode prefill working
    exactly as before (see that partial's own docstring), only the drawer's
    own markup/styling changed. The Device field is a convenience picker,
    not itself a stored field -- see byky-device.js for how it fills the
    read-only identity fields below it from approved_unmapped's own
    json_script blob."""

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
        approved_unmapped = data.approved_devices()
        branches_list = cms_data.branches()
        mapped_stations = {d["station"] for d in rows}
        context.update(
            {
                "devices": rows,
                "counts": data.counts(rows),
                "approved_unmapped": approved_unmapped,
                "branch_flags": [
                    {
                        "name": b["name"],
                        "multi_user": b["multi_user"],
                        "mapped": b["name"] in mapped_stations,
                    }
                    for b in branches_list
                ],
                "spec": {
                    "scr_name": "device",
                    "title_field": "name",
                    "add_label": "Add Device Mapping",
                    "drawer_id": "offcanvasAddDevice",
                    "sections": [
                        {
                            "title": "",
                            "fields": [
                                {
                                    "id": "device_pick",
                                    "label": "Device",
                                    "kind": "select",
                                    "required": True,
                                    "resolved": [f"{d['name']} — {d['mac']}" for d in approved_unmapped],
                                    "help": "Only devices cleared through Device Approval and not yet mapped are listed.",
                                },
                                {"id": "device_id", "label": "Device ID", "kind": "text", "required": True, "readonly": True},
                                {"id": "name", "label": "Device Name", "kind": "text", "required": True, "readonly": True},
                                {"id": "mac", "label": "MAC Address", "kind": "text", "required": True, "readonly": True},
                                {
                                    "id": "station",
                                    "label": "Station",
                                    "kind": "select",
                                    "required": True,
                                    "resolved": [b["name"] for b in branches_list],
                                },
                                {"id": "apk_version", "label": "APK Version", "kind": "text", "readonly": True},
                            ],
                        }
                    ],
                },
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
