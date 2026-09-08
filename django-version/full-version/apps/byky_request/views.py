"""Request Management screens.

Built on the shared byky-screen.css/js base (see byky-screen-design-system.md).
Wireframe phase: no writes, no CRUD, no API.
"""

from apps.byky_core.views import BykyScreenView

from . import data


class RequestApprovalView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "requests": data.pending_requests(),
                "request_types": data.REQUEST_TYPES,
                "statuses": data.STATUSES,
            }
        )
        return context


class CardDiscountApprovalView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(
            {
                "requests": data.card_discount_requests(),
                "card_types_list": data.CARD_TYPES,
                "statuses": data.STATUSES,
            }
        )
        return context


class CardDiscountApprovalDetailView(BykyScreenView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_no = self.kwargs.get("request_no")
        context.update(
            {
                "request_no": request_no,
                "request_detail": data.card_discount_request_detail(request_no),
            }
        )
        return context
