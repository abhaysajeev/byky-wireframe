"""Module 3 -- Inventory (IMS) screens.

Four screens run on real client records (stock items, categories, sub-categories,
station mappings). The rest have no source data and show the awaiting-data state.
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core import privileges, seed
from apps.byky_core.views import BykyScreenView
from apps.byky_cms import data as cms_data

from . import data, drawers


class ImsScreenView(BykyScreenView):
    """Reference lists the IMS dropdowns need, plus an optional awaiting key."""

    awaiting_key = None
    drawer_specs = drawers.SPECS

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories_list": data.categories(),
                "subcategories_list": data.subcategories(),
                "branches_list": cms_data.branches(),
                "permissions": data.PERMISSIONS,
                "counts": data.counts(),
                # available to every IMS screen, not just Asset Management --
                # Vehicle Station Mapping shows the mapped-asset figure too
                "asset_counts": data.asset_counts(),
                "item_types": data.ITEM_TYPES,
                "event_locations_list": data.event_locations(),
            }
        )
        if self.awaiting_key:
            context["awaiting"] = data.AWAITING[self.awaiting_key]
        return context


class StockItemView(ImsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = data.stock_items()
        for i, it in enumerate(items):
            it["json_id"] = f"scr-record-item-{i}"
            it["fields_json"] = {
                "code": it["code"],
                "name": it["name"],
                "category": it["category"],
                "subcategory": it["subcategory"],
            }
        context["items"] = items
        return context


class CategoryView(ImsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = data.categories()
        for i, c in enumerate(categories):
            c["json_id"] = f"scr-record-category-{i}"
            c["fields_json"] = {
                "code": c["code"],
                "name": c["name"],
                "description": "" if c["description"] == data.SHORT else c["description"],
            }
        context["categories"] = categories
        return context


class SubCategoryView(ImsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        subcategories = data.subcategories()
        for i, s in enumerate(subcategories):
            s["json_id"] = f"scr-record-subcategory-{i}"
            s["fields_json"] = {
                "code": s["code"],
                "name": s["name"],
                "parent": s["parent"],
                "description": "" if s["description"] == data.SHORT else s["description"],
            }
        context["subcategories"] = subcategories
        return context


class StationMappingView(ImsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mappings"] = data.station_mappings()
        return context


class StationMappingMapView(ImsScreenView):
    """FSD 3.6's "Map Vehicle" action, as a full page rather than a drawer:
    pick a branch, search the unmapped-vehicle pool, select some, map them.
    See data.unmapped_vehicles() for why that pool is empty today."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unmapped"] = data.unmapped_vehicles()
        return context


class AssetManagementView(ImsScreenView):
    """Asset Management -- company-owned operating equipment.

    Deliberately holds no vehicles: rental stock is Vehicle Management's job
    (FSD 3.1). Two panels -- the unit register (empty until the client
    supplies an equipment inventory) and the type catalogue derived from the
    FSD hardware specs. See data._ASSET_TYPES for each type's provenance.

    Custodians are the client's real staff list, so that dropdown is genuine
    even though no unit is assigned to one yet.
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        types = data.asset_types()
        for i, t in enumerate(types):
            t["json_id"] = f"scr-record-assettype-{i}"
            t["fields_json"] = {
                "code": t["code"],
                "name": t["name"],
                "asset_class": t["asset_class"],
                "identifier": t["identifier"],
                "location": t["location"],
            }
        rows = data.assets()
        for i, a in enumerate(rows):
            a["json_id"] = f"scr-record-asset-{i}"
            a["identifier"] = a["code"]
            a["station_key"] = a["station"]
            a["warranty"] = f"{a['warranty_from']} – {a['warranty_to']}"
            a["fields_json"] = {
                k: a[k]
                for k in (
                    "code", "name", "asset_class", "type", "material_type",
                    "model", "serial", "station", "custodian", "ip", "mac",
                    "imei", "msisdn", "acquired", "cost", "supplier",
                    "warranty_from", "warranty_to", "condition", "notes",
                )
            }
        context.update(
            {
                "assets": rows,
                "asset_types": types,
                "asset_counts": data.asset_counts(),
                "asset_classes": data.ASSET_CLASSES,
                "asset_conditions": data.ASSET_CONDITIONS,
                "employees_list": seed.EMPLOYEES,
            }
        )
        return context


class AssetBranchMapView(ImsScreenView):
    """Map Asset to Branch -- the equipment counterpart of FSD 3.6's Map
    Vehicle, reached from the Map Item menu on Inventory Branch Mapping.
    See data.unmapped_assets() for why the pool is empty today."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["unmapped"] = data.unmapped_assets()
        return context


class TransferListView(ImsScreenView):
    """FSD 3.7. Rows are demo data -- see data._DEMO_TRANSFERS."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = [dict(t) for t in data.transfers()]
        for i, t in enumerate(rows):
            t["json_id"] = f"scr-record-transfer-{i}"
            t["items_display"] = ", ".join(t["items"])
            t["fields_json"] = {
                "doc_no": t["doc_no"],
                "from_branch": t["from_branch"],
                "to_branch": t["to_branch"],
                "event_location": t["event_location"],
                "dispatch_date": t["dispatch_date"],
                "driver": t["driver"],
                "remarks": t["remarks"],
                "items_count": len(t["items"]),
            }
        context["transfers"] = rows
        return context


class TransferFormView(ImsScreenView):
    """The full-page Transfer / Return flows behind Inventory Transfer &
    Return's Move Item menu.

    The document number is left blank: nothing persists in this phase, so a
    number shown up front would be a made-up one that never becomes real. The
    field stays read-only and says it is assigned on save.
    """

    # a return picks from what is out at a warehouse or event, not from a branch
    returning = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = data.returnable_items() if self.returning else data.transferable_items()
        context.update(
            {
                "transfer_types": data.TRANSFER_TYPES,
                "return_types": data.RETURN_TYPES,
                "warehouses_list": data.warehouses(),
                "event_locations": data.event_locations(),
                "items": items,
                "categories_in_pool": sorted({i["category"] for i in items}),
                "vtypes_in_pool": sorted({i["vtype"] for i in items if i["vtype"]}),
            }
        )
        return context


class TransferEditView(TransferFormView):
    """Row 48's UAT remarks: editing a transfer needs its selected vehicles
    as a removable cart plus an Add action to pick more from the same From
    Branch's pool, and a history log of edits. Reuses TransferFormView's
    full-page layout and item pool wholesale -- only the loaded record and
    its cart/history are new."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doc_no = self.kwargs.get("doc_no")
        context.update(
            {
                "doc_no": doc_no,
                "transfer_detail": data.transfer_detail(doc_no),
            }
        )
        return context


class BrandView(ImsScreenView):
    """FSD 3.4. Rows are demo data -- see data._DEMO_BRANDS."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = [dict(b) for b in data.brands()]
        for i, b in enumerate(rows):
            b["json_id"] = f"scr-record-brand-{i}"
            b["website_short"] = data.SHORT if b["website"] == data.NOT_CAPTURED else b["website"]
            b["fields_json"] = {"code": b["code"], "name": b["name"], "website": ""}
        context["brands"] = rows
        return context


class UnitView(ImsScreenView):
    """FSD 3.5. Rows are demo data -- see data._DEMO_UNITS."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = [dict(u) for u in data.units()]
        for i, u in enumerate(rows):
            u["json_id"] = f"scr-record-unit-{i}"
            u["fields_json"] = {"code": u["code"], "name": u["name"], "description": ""}
        context["units"] = rows
        return context


class ImsAwaitingView(ImsScreenView):
    """Screens the FSD specifies but the client data has no source for."""


class EcomCategoryView(ImsScreenView):
    """FSD 3.8. No source data (grid still shows the awaiting-data state);
    drawer converted off its old inline offcanvas per byky claude
    design/byky-drawer/README.md section 7."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spec"] = {
            "add_label": "Add ECom Category",
            "drawer_id": "offcanvasAddEcomCat",
            "sections": [
                {
                    "title": "",
                    "fields": [
                        {"id": "title", "label": "ECom Category Title", "kind": "text", "required": True},
                        {"id": "sort", "label": "Sort Order", "kind": "number", "required": False},
                        {"id": "meta", "label": "Meta Tags", "kind": "textarea", "required": False},
                        {"id": "banner", "label": "Banner Image", "kind": "file", "required": False},
                    ],
                }
            ],
        }
        return context


class EcomStockItemView(ImsScreenView):
    """FSD 3.9. No source data; drawer converted per README section 7."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spec"] = {
            "add_label": "Add Catalog Entry",
            "drawer_id": "offcanvasAddEcomItem",
            "sections": [
                {
                    "title": "",
                    "fields": [
                        {"id": "title", "label": "Web Title", "kind": "text", "required": True},
                        {
                            "id": "category",
                            "label": "E-Com Category",
                            "kind": "select",
                            "required": True,
                            "resolved": [c["name"] for c in context["categories_list"]],
                        },
                        {"id": "rate", "label": "Online Rate", "kind": "number", "required": False},
                        {"id": "featured", "label": "Featured", "kind": "checkbox", "required": False},
                        {"id": "popular", "label": "Popular", "kind": "checkbox", "required": False},
                    ],
                }
            ],
        }
        return context


class VehicleFeaturesView(ImsScreenView):
    """FSD 3.10. No source data; drawer converted per README section 7."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spec"] = {
            "add_label": "Add Feature",
            "drawer_id": "offcanvasAddFeature",
            "sections": [
                {
                    "title": "",
                    "fields": [
                        {"id": "code", "label": "Feature Code", "kind": "text", "required": True},
                        {"id": "name", "label": "Feature Name", "kind": "text", "required": True},
                        {"id": "description", "label": "Description", "kind": "textarea", "required": False},
                        {"id": "icon", "label": "Icon", "kind": "file", "required": False},
                    ],
                }
            ],
        }
        return context


class NewsletterDispatchView(ImsScreenView):
    """FSD 3.16. No source data; drawer converted per README section 7."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["spec"] = {
            "add_label": "New Dispatch",
            "drawer_id": "offcanvasAddNewsletter",
            "sections": [
                {
                    "title": "",
                    "fields": [
                        {"id": "subject", "label": "Subject Line", "kind": "text", "required": True},
                        {
                            "id": "segment",
                            "label": "Target Segment",
                            "kind": "select",
                            "required": True,
                            "resolved": ["All App Users", "Active Renters", "VIP Customers"],
                        },
                        {"id": "body", "label": "Email Body (HTML)", "kind": "textarea", "required": False},
                    ],
                }
            ],
        }
        return context


class ImsPrivilegeView(ImsScreenView):
    """Tier D -- roles list + per-role screen permission matrix. See
    apps/byky_core/privileges.py for the shared role master and defaults."""

    SLUG = "ims"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        screens = privileges.module_screens(self.SLUG)
        mapped = privileges.DEFAULT_MAPPED_ROLES
        context.update(
            {
                "roles": privileges.ROLES,
                "mapped_roles": mapped,
                "admin_roles": privileges.ADMIN_ROLES,
                "screens": screens,
                "role_matrices": privileges.role_matrices(privileges.ROLES, screens, context["permissions"]),
            }
        )
        return context
