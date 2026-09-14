"""Live Monitoring -- new module, not one of the 16 FSD modules. Requested
against the client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Live
Monitor" / "Search Order" / "Image Sharing" pages).

Wireframe phase: no writes, no CRUD, no API -- frontend only.
"""

import datetime

from apps.byky_core.views import BykyScreenView
from apps.byky_cms import data as cms_data

from . import data


class LiveScreenView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "countries_list": cms_data.countries(),
                "states_list": cms_data.states(),
                "branches_list": cms_data.branches(),
                "order_statuses": data.ORDER_STATUSES,
            }
        )
        return context


class LiveMonitorView(LiveScreenView):
    """RMS WEB APK UI.xlsx feedback on this screen: Location -> Branch and
    Order Status -> Type are label-only renames (both already draw off the
    same branches_list / order_statuses context the base class supplies);
    Type and Search In each gain a Credit Note option; a From/To Date pair
    is added ahead of Search, defaulting to today (today_display) the same
    way a real search bar opens scoped to "today" until the user widens it;
    and the Rent Bill/Direct Bill tabs gain an All (default) and a Credit
    Note tab, each with its own KPI tiles and table, mirroring the
    Rent/Direct Bill pair with real data still awaiting client transactions
    (module docstring)."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "today_display": datetime.date.today().strftime("%d %b %Y"),
            }
        )
        return context


class SearchOrderView(LiveScreenView):
    pass


class ImageSharingView(LiveScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = data.shared_images()
        context.update(
            {
                "images": images,
                "counts": data.counts(images),
                "approval_statuses": data.IMAGE_APPROVAL_STATUSES,
            }
        )
        return context
