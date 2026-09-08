"""Print Invoice -- new module, not one of the 16 FSD modules. Requested
against the client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Print
Invoice" page): a list of tax invoices with a Print action, and the printed
bill itself, sized to match the client's actual receipt-printer paper.

Wireframe phase: no writes, no CRUD, no API -- frontend only.
"""

from django.views.generic import TemplateView

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
            }
        )
        return context


class PrintBillView(TemplateView):
    """The printable bill itself -- deliberately NOT built on the .scr-*
    admin shell (see byky-screen-design-system.md section 9: something
    truly one-of-a-kind doesn't belong in .scr-* at all). A receipt is its
    own document: no navbar, no sidebar, no site chrome, sized to the
    client's actual thermal-printer paper width rather than a screen
    layout, per the request to match the real print ratio.
    """

    template_name = "invoice_print_bill.html"

    def get_context_data(self, **kwargs):
        return {"bill": data.sample_bill()}
