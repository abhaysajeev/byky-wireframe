"""Live Monitoring -- new module, not one of the 16 FSD modules. Requested
against the client's RMS Web feedback doc (RMS WEB 07.09.2026-1.pdf, "Live
Monitor" / "Search Order" / "Image Sharing" pages).

Wireframe phase: no writes, no CRUD, no API -- frontend only.
"""

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
    pass


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
