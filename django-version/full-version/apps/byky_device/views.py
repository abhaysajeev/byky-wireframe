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
    """Row 52 of the client's feedback doc: rebuilt from a single always-open
    edit form into a real Tier A list -- KPI tiles, a grid of every
    station's settings, and a side drawer (byky/partials/drawer.html) for
    adding or editing one station's settings, matching the list+drawer
    pattern used everywhere else in the app instead of the search-then-
    edit-one-form shape it replaces. spec.scr_name keeps both the header's
    Add Settings trigger (data-scr-open="settings:add") and each row's Edit
    trigger (data-scr-open="settings:edit") working the usual way; the
    Station field is a select rather than fixed text so Add mode can pick
    which station to configure, then locks (disabled, per lock_on_edit on a
    select) once you're editing an existing row so it can't be retargeted."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = data.device_settings()
        for i, s in enumerate(rows):
            s["json_id"] = f"scr-record-settings-{i}"
            s["fields_json"] = {
                "station": s["station"],
                "company": s["company"],
                "settings_code": s["settings_code"],
                "header1": s["header1"],
                "header2": s["header2"],
                "additional_header2": s["additional_header2"],
                "footer1": s["footer1"],
                "footer2": s["footer2"],
                "print_logo": s["print_logo"],
                "paper_feed": s["paper_feed"],
                "receipt_copies": s["receipt_copies"],
                "print_type": s["print_type"],
                "order_no_prefix": s["order_no_prefix"],
                "customer_test_slot": s["customer_test_slot"],
                "cashier_test_slot": s["cashier_test_slot"],
                "tax_type": s["tax_type"],
                "round_off_type": s["round_off_type"],
                "round_off_limit": s["round_off_limit"],
            }
        context.update(
            {
                "settings_rows": rows,
                "settings_counts": data.device_settings_counts(rows),
                "approval_statuses": data.APPROVAL_STATUSES,
                "spec": {
                    "scr_name": "settings",
                    "title_field": "station",
                    "add_label": "Add Settings",
                    "drawer_id": "offcanvasStationSettings",
                    "sections": [
                        {
                            "title": "Scope",
                            "fields": [
                                {
                                    "id": "station",
                                    "label": "Station",
                                    "kind": "select",
                                    "required": True,
                                    "resolved": [b["name"] for b in context["branches_list"]],
                                    "lock_on_edit": True,
                                },
                                {
                                    "id": "company",
                                    "label": "Company",
                                    "kind": "select",
                                    "required": True,
                                    "resolved": context["companies_list"],
                                },
                                {"id": "settings_code", "label": "Settings Code", "kind": "text", "readonly": True},
                            ],
                        },
                        {
                            "title": "Receipt Header & Footer",
                            "fields": [
                                {"id": "header1", "label": "Header 1", "kind": "text"},
                                {"id": "header2", "label": "Header 2 (Arabic)", "kind": "text"},
                                {"id": "additional_header2", "label": "Additional Header 2", "kind": "text"},
                                {"id": "footer1", "label": "Footer 1", "kind": "text"},
                                {"id": "footer2", "label": "Footer 2 (Arabic)", "kind": "text"},
                            ],
                        },
                        {
                            "title": "Print & Copies",
                            "fields": [
                                {"id": "print_logo", "label": "Print Logo", "kind": "checkbox"},
                                {
                                    "id": "paper_feed",
                                    "label": "Paper Feed",
                                    "kind": "select",
                                    "required": True,
                                    "resolved": data.PRINT_FEED_OPTIONS,
                                },
                                {"id": "receipt_copies", "label": "No of Receipt Copy", "kind": "number", "required": True},
                                {
                                    "id": "print_type",
                                    "label": "Print Type",
                                    "kind": "select",
                                    "required": True,
                                    "resolved": data.PRINT_TYPE_OPTIONS,
                                },
                                {"id": "order_no_prefix", "label": "Order No Starting Characters", "kind": "text"},
                            ],
                        },
                        {
                            "title": "Test Slots, Tax & Rounding",
                            "fields": [
                                {"id": "customer_test_slot", "label": "Customer Test Time Slot (Min)", "kind": "number"},
                                {"id": "cashier_test_slot", "label": "Cashier Test Time Slot (Min)", "kind": "number"},
                                {
                                    "id": "tax_type",
                                    "label": "Before Tax / Discount Type",
                                    "kind": "select",
                                    "required": True,
                                    "resolved": data.TAX_TYPE_OPTIONS,
                                },
                                {
                                    "id": "round_off_type",
                                    "label": "Round Off Type",
                                    "kind": "select",
                                    "required": True,
                                    "resolved": data.ROUND_OFF_OPTIONS,
                                },
                                {
                                    "id": "round_off_limit",
                                    "label": "Round Off Limit",
                                    "kind": "select",
                                    "required": True,
                                    "resolved": data.ROUND_OFF_LIMITS,
                                },
                            ],
                        },
                        {
                            "title": "Logo",
                            "fields": [
                                {"id": "logo", "label": "Logo", "kind": "file", "help": "PNG or JPG, printed on every receipt this station's devices issue."},
                            ],
                        },
                    ],
                },
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
