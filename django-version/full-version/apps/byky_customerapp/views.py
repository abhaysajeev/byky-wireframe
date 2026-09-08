"""Customer App Management screens.

Built on the shared byky-screen.css/js base (see byky-screen-design-system.md).
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core.views import BykyScreenView

from . import data


class MailTemplateView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "templates": data.mail_templates(),
                "mappings": data.mail_template_mappings(),
                "events": data.MAIL_EVENTS,
                "customer_types": data.CUSTOMER_TYPES,
            }
        )
        return context


class AdvertisementView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "profiles": data.advertisement_profiles(),
                "mappings": data.advertisement_profile_mappings(),
            }
        )
        return context


class CustomerManagementView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "search_in": data.CUSTOMER_SEARCH_IN,
                "search_type": data.CUSTOMER_SEARCH_TYPE,
            }
        )
        return context
