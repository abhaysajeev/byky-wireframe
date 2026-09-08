from django.urls import path

from . import views

urlpatterns = [
    path(
        "invoice/print-invoice/",
        views.PrintInvoiceListView.as_view(
            template_name="invoice_print_invoice.html",
            screen_no="PI.1",
            screen_title="Print Invoice",
            module_label="Print Invoice",
            tier="A",
            purpose="Find a tax invoice and print it directly from the browser, at the same paper size the station's receipt printer uses.",
        ),
        name="invoice-print-invoice",
    ),
]
