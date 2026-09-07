"""Fare & Schemes screens.

Two long, multi-section create forms adapted from the client's HTML mockups into
the Vuexy component set: same fields and same order, rebuilt with our cards,
grid and spacing scale so they sit consistently beside the other 109 screens.

Wireframe phase: nothing is saved.
"""

from apps.byky_core.views import BykyScreenView
from apps.byky_cms import data as cms_data

from . import data


class FareScreenView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "price_levels": data.PRICE_LEVELS,
                "fare_status": data.FARE_STATUS,
                "days": data.DAYS,
                "categories_list": data.categories(),
                "vehicle_types_list": data.vehicle_types(),
                "companies_list": data.companies(),
                "branches_list": cms_data.branches(),
                "states_list": cms_data.states(),
                "package_times": data.PACKAGE_TIMES,
            }
        )
        return context


class FareEntryView(FareScreenView):
    """Create Fare — price scope, validity, package fare, time slabs, preview."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # The preview strip mirrors the mockup's five summary boxes. Values are
        # placeholders until the form is wired to a backend.
        context["preview_items"] = [
            ("Price Level", "Company"),
            ("Scope", "BYKY"),
            ("Vehicle Type", "Not selected"),
            ("Validity", "Not set"),
            ("Package Time", "30 Minutes"),
        ]
        return context


class SchemeCreationView(FareScreenView):
    """Create Promotion — scope, validity/value band, items, free items."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "promotion_for": data.PROMOTION_FOR,
                "inventory_types": data.INVENTORY_TYPES,
                "promotion_types": data.PROMOTION_TYPES,
            }
        )
        return context
