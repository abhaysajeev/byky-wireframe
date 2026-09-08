from django.urls import path

from . import views

urlpatterns = [
    path(
        "live/live-monitor/",
        views.LiveMonitorView.as_view(
            template_name="live_live_monitor.html",
            screen_no="LM.1",
            screen_title="Live Monitor",
            module_label="Live Monitoring",
            tier="C",
            purpose="Watch running rentals across the network in real time -- running vehicles, orders, and collected amounts, split by Rent Bill and Direct Bill.",
        ),
        name="live-live-monitor",
    ),
    path(
        "live/search-order/",
        views.SearchOrderView.as_view(
            template_name="live_search_order.html",
            screen_no="LM.2",
            screen_title="Search Order",
            module_label="Live Monitoring",
            tier="C",
            purpose="Look up a single order by number and review its customer, payment and vehicle details.",
        ),
        name="live-search-order",
    ),
    path(
        "live/image-sharing/",
        views.ImageSharingView.as_view(
            template_name="live_image_sharing.html",
            screen_no="LM.3",
            screen_title="Image Sharing",
            module_label="Live Monitoring",
            tier="A",
            purpose="Review and approve photos staff share from a station before they go out on social channels.",
        ),
        name="live-image-sharing",
    ),
]
