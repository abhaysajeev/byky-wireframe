"""Credit Note Management screens.

Built on the shared byky-screen.css/js base (see byky-screen-design-system.md).
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_cms import data as cms_data
from apps.byky_core.views import BykyScreenView

from . import data


class CreditNoteRequestView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "requests": data.credit_note_requests(),
                "branches_list": cms_data.branches(),
            }
        )
        return context


class CreditNoteView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "invoices": data.tax_invoices(),
                "branches_list": cms_data.branches(),
            }
        )
        return context
