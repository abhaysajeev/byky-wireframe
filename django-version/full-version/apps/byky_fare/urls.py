from django.urls import path

from . import views

urlpatterns = [
    path(
        "fare/fare-entry/",
        views.FareEntryView.as_view(
            template_name="fare_entry.html",
            screen_no="F.1",
            screen_title="Fare Entry",
            module_label="Fare & Schemes",
            tier="B",
            phase=13,
            purpose="Define rental packages, grace periods, concurrent charges and time-based pricing for a vehicle type.",
        ),
        name="fare-entry",
    ),
    path(
        "fare/scheme-creation/",
        views.SchemeCreationView.as_view(
            template_name="scheme_creation.html",
            screen_no="F.2",
            screen_title="Scheme Creation",
            module_label="Fare & Schemes",
            tier="B",
            phase=13,
            purpose="Configure promotional schemes: validity, value bands, promotion items and free-item rules.",
        ),
        name="fare-scheme-creation",
    ),
]
