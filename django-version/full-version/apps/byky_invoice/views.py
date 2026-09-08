"""Print Invoice -- new module, not one of the 16 FSD modules. Requested
against the client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Print
Invoice" page): a list of tax invoices with a Print action that opens the
printable bill in a centered modal (not a new tab), sized to match the
client's actual receipt-printer paper.

Wireframe phase: no writes, no CRUD, no API -- frontend only.
"""

from apps.byky_core.views import BykyScreenView
from apps.byky_cms import data as cms_data

from . import data


class PrintInvoiceListView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "branches_list": cms_data.branches(),
                "invoices": data.invoices(),
                "bill": data.sample_bill(),
            }
        )
        return context
