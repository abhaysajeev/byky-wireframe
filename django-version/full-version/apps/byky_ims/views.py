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
