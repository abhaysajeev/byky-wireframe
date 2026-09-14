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
    Note tab, each with its own KPI tiles and table.

    Rent Bill/Direct Bill/All now carry 5 deterministic demo rows apiece
    (data.rent_bill_orders/direct_bill_orders), a deliberate, explicitly
    requested exception to this module's usual awaiting-data treatment --
    see data.py's module docstring. Credit Note stays untouched (awaiting
    data), and each row's kebab holds only View, since there's no detail
    page or edit flow built for these demo orders yet."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        rent_rows = data.rent_bill_orders()
        direct_rows = data.direct_bill_orders()
        all_rows = rent_rows + direct_rows
        all_kpis = data.order_kpis(all_rows)
        all_kpis["credit_note_count"] = 0
        all_kpis["credit_note_amount"] = 0.0
        context.update(
            {
                "today_display": datetime.date.today().strftime("%d %b %Y"),
                "rent_rows": rent_rows,
                "direct_rows": direct_rows,
                "all_rows": all_rows,
                "rent_kpis": data.order_kpis(rent_rows),
                "direct_kpis": data.order_kpis(direct_rows),
                "all_kpis": all_kpis,
            }
        )
        return context


class SearchOrderView(LiveScreenView):
    pass


class ImageSharingView(LiveScreenView):
    """RMS WEB APK UI.xlsx feedback on this screen: the Approved/Awaiting
    review/Rejected split is gone entirely -- no Status column, no Status
    filter, no per-row Approve/Reject (a shared photo is either on the list
    or deleted from it). Branch and From/To Date replace Status as the
    header filters. Each row keeps a standalone View button and gains a
    kebab holding only Delete from Database; a Select-All checkbox and a
    per-row checkbox column drive a bulk Delete from Database action
    (byky-image-sharing.js) for handling several photos at once. The new
    Station Count KPI tracks distinct branches among the checked rows
    live, so it starts at 0 and is entirely JS-driven -- see that same
    file."""

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        images = data.shared_images()
        context.update(
            {
                "images": images,
                "counts": data.counts(images),
            }
        )
        return context
