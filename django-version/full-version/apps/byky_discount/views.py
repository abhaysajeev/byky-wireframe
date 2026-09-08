"""Discount Card Management screens.

Built on the shared byky-screen.css/js base (see byky-screen-design-system.md).
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core.views import BykyScreenView

from . import data


class DiscountScreenView(BykyScreenView):
    """Card Type is used across all three screens' dropdowns."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["card_types_list"] = data.CARD_TYPES
        return context


class CardManagementView(DiscountScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cards"] = data.cards()
        return context


class CardGradeManagementView(DiscountScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["grades"] = data.card_grades()
        return context


class CardDiscountManagementView(DiscountScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "grades_list": data.card_grades(),
                "days": data.DAYS,
                "promotion_types": data.PROMOTION_TYPES,
                "usage_types": data.USAGE_TYPES,
            }
        )
        return context
