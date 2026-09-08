from django.urls import path

from . import views

urlpatterns = [
    path(
        "request/request-approval/",
        views.RequestApprovalView.as_view(
            template_name="request_request_approval.html",
            screen_title="Request Approval",
            module_label="Request Management",
            tier="C",
            purpose="Review and approve or reject requests submitted across the business -- card discounts, wallet refunds and similar.",
        ),
        name="request-request-approval",
    ),
    path(
        "request/card-discount-approval/",
        views.CardDiscountApprovalView.as_view(
            template_name="request_card_discount_approval.html",
            screen_title="Card Discount Approval",
            module_label="Request Management",
            tier="C",
            purpose="Review discount card requests submitted by customers through the mobile app.",
        ),
        name="request-card-discount-approval",
    ),
    path(
        "request/card-discount-approval/<str:request_no>/",
        views.CardDiscountApprovalDetailView.as_view(
            template_name="request_card_discount_approval_detail.html",
            screen_title="Card Discount Request",
            module_label="Request Management",
            tier="C",
            purpose="Full detail of a single card discount request, with Approve / Reject actions.",
        ),
        name="request-card-discount-approval-detail",
    ),
]
