from django.urls import path

from . import views

urlpatterns = [
    path(
        "customerapp/mail-template/",
        views.MailTemplateView.as_view(
            template_name="customerapp_mail_template.html",
            screen_title="Mail Template & Template Mapping",
            module_label="Customer App Management",
            tier="A",
            purpose="Configure the mail templates the customer app sends and map each one to the event and customer type that triggers it.",
        ),
        name="customerapp-mail-template",
    ),
    path(
        "customerapp/advertisement/",
        views.AdvertisementView.as_view(
            template_name="customerapp_advertisement.html",
            screen_title="Advertisement",
            module_label="Customer App Management",
            tier="A",
            purpose="Manage the image-slider profiles shown in the customer app and schedule the date/time window each one is active.",
        ),
        name="customerapp-advertisement",
    ),
    path(
        "customerapp/customer-management/",
        views.CustomerManagementView.as_view(
            template_name="customerapp_customer_management.html",
            screen_title="Customer Management",
            module_label="Customer App Management",
            tier="C",
            purpose="Look up a customer registered through the customer app and review their profile, loyalty and wallet standing.",
        ),
        name="customerapp-customer-management",
    ),
]
