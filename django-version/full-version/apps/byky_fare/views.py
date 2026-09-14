"""Fare & Offers screens.

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


class FareEntryListView(FareScreenView):
    """Client feedback: Fare Entry opened straight on the create form with
    no way to see previously configured fares. Now a real Tier A list --
    "New Fare" opens the same form this screen replaces, at its own /add/
    URL; each row's kebab offers View / Edit / Export / Delete."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rows = data.fares()
        for i, f in enumerate(rows):
            f["json_id"] = f"scr-record-fare-{i}"
        context.update(
            {
                "fares": rows,
                "fare_counts": data.fare_counts(rows),
            }
        )
        return context


class FareEntryFormView(FareScreenView):
    """Add/Edit Fare — price scope, validity, package fare, time slabs,
    preview. One template for both: `fare` is None in Add mode, or the
    record being edited (resolved from the <code> URL kwarg) in Edit mode."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.kwargs.get("code")
        fare = data.fare_by_code(code) if code else None
        context["fare"] = fare
        context["is_edit"] = fare is not None
        # The preview strip mirrors the mockup's five summary boxes. Values
        # reflect the fare being edited, or the form's own defaults in Add
        # mode, until the form is wired to a backend.
        context["preview_items"] = [
            ("Price Level", fare["price_level"] if fare else "Company"),
            ("Scope", fare["scope"] if fare else "BYKY"),
            ("Vehicle Type", fare["vehicle_type"] if fare else "Not selected"),
            ("Validity", f'{fare["from_date"]} – {fare["to_date"]}' if fare else "Not set"),
            ("Package Time", f'{fare["package_time"]} Minutes' if fare else "30 Minutes"),
        ]
        return context


class FareEntryDetailView(FareScreenView):
    """Full read-only detail of one configured fare, reachable from the
    list's own View action."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.kwargs.get("code")
        context["fare"] = data.fare_by_code(code)
        context["code"] = code
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
