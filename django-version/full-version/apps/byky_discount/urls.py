from django.urls import path

from . import views

urlpatterns = [
    path(
        "discount/card-management/",
        views.CardManagementView.as_view(
            template_name="discount_card_management.html",
            screen_title="Card Management",
            module_label="Discount Card Management",
            tier="A",
            purpose="Register the discount/loyalty card types the business issues.",
        ),
        name="discount-card-management",
    ),
    path(
        "discount/card-grade-management/",
        views.CardGradeManagementView.as_view(
            template_name="discount_card_grade_management.html",
            screen_title="Card Grade Management",
            module_label="Discount Card Management",
            tier="A",
            purpose="Define the grade tiers within each card type, e.g. Silver, Gold, Platinum.",
        ),
        name="discount-card-grade-management",
    ),
    path(
        "discount/card-discount-management/",
        views.CardDiscountManagementView.as_view(
            template_name="discount_card_discount_management.html",
            screen_title="Card Discount",
            module_label="Discount Card Management",
            tier="B",
            purpose="Configure day-wise discount percentages, promotion type and usage limits for a card grade.",
        ),
        name="discount-card-discount-management",
    ),
]
