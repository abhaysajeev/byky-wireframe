"""Module 3 -- Inventory (IMS) screens.

Four screens run on real client records (stock items, categories, sub-categories,
station mappings). The rest have no source data and show the awaiting-data state.
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core.views import BykyScreenView
from apps.byky_cms import data as cms_data

from . import data


class ImsScreenView(BykyScreenView):
    """Reference lists the IMS dropdowns need, plus an optional awaiting key."""

    awaiting_key = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "categories_list": data.categories(),
                "subcategories_list": data.subcategories(),
                "branches_list": cms_data.branches(),
                "permissions": data.PERMISSIONS,
                "counts": data.counts(),
            }
        )
        if self.awaiting_key:
            context["awaiting"] = data.AWAITING[self.awaiting_key]
        return context


class StockItemView(ImsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["items"] = data.stock_items()
        return context


class CategoryView(ImsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = data.categories()
        return context


class SubCategoryView(ImsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["subcategories"] = data.subcategories()
        return context


class StationMappingView(ImsScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["mappings"] = data.station_mappings()
        return context


class ImsAwaitingView(ImsScreenView):
    """Screens the FSD specifies but the client data has no source for."""


class ImsPrivilegeView(ImsScreenView):
    ROLES = ["SuperAdmin", "Inventory Manager", "Store Keeper", "Branch Manager"]

    SCREENS = [
        ("Inventory Stock Item Management", [1, 1, 1, 1, 1, 0]),
        ("Inventory Category Master", [1, 1, 1, 1, 0, 0]),
        ("Inventory Sub-Category Master", [1, 1, 1, 1, 0, 0]),
        ("Inventory Brand Master", [1, 1, 1, 1, 0, 0]),
        ("Inventory Unit of Measure", [1, 1, 1, 1, 0, 0]),
        ("Vehicle Station Mapping", [1, 1, 1, 1, 0, 0]),
        ("Vehicle Transfer & Relocation", [1, 1, 1, 1, 1, 0]),
        ("E-Commerce Category Master", [1, 1, 1, 1, 0, 0]),
        ("E-Commerce Stock Item Catalog", [1, 1, 1, 1, 0, 0]),
        ("Vehicle & Item Features Master", [1, 1, 1, 1, 0, 0]),
        ("Order Status Management", [1, 0, 1, 1, 0, 0]),
        ("Promotional Coupon & Discount Code", [1, 1, 1, 1, 1, 0]),
        ("Loyalty Rewards Profile", [1, 1, 1, 1, 0, 0]),
        ("Loyalty Redemption Profile", [1, 1, 1, 1, 0, 0]),
        ("Wallet Refund Request Management", [1, 0, 1, 0, 1, 0]),
        ("Newsletter & Marketing Dispatch", [1, 1, 1, 0, 1, 0]),
        ("Push Notification Dispatch", [1, 1, 1, 0, 1, 0]),
        ("Live RFID & Antenna Fleet Monitoring", [1, 0, 1, 0, 0, 0]),
        ("Inventory System Alerts", [1, 0, 1, 1, 0, 0]),
        ("IMS Security Privilege Management", [1, 0, 1, 0, 0, 0]),
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "roles": self.ROLES,
                "screens": [
                    {"name": n, "perms": [bool(x) for x in p]} for n, p in self.SCREENS
                ],
            }
        )
        return context
