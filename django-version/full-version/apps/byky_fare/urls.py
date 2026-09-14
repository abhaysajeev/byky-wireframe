from django.urls import path

from . import views

urlpatterns = [
    path(
        "fare/fare-entry/",
        views.FareEntryListView.as_view(
            template_name="fare_entry_list.html",
            screen_no="F.1",
            screen_title="Fare Entry",
            module_label="Fare & Offers",
            tier="A",
            phase=13,
            purpose="Review previously configured fares and open any of them to view, edit or add a new one.",
        ),
        name="fare-entry",
    ),
    path(
        "fare/fare-entry/add/",
        views.FareEntryFormView.as_view(
            template_name="fare_entry.html",
            screen_no="F.1",
            screen_title="Add Fare",
            module_label="Fare & Offers",
            tier="B",
            phase=13,
            purpose="Define rental packages, grace periods, concurrent charges and time-based pricing for a vehicle type.",
        ),
        name="fare-entry-add",
    ),
    path(
        "fare/fare-entry/<str:code>/edit/",
        views.FareEntryFormView.as_view(
            template_name="fare_entry.html",
            screen_no="F.1",
            screen_title="Edit Fare",
            module_label="Fare & Offers",
            tier="B",
            phase=13,
            purpose="Define rental packages, grace periods, concurrent charges and time-based pricing for a vehicle type.",
        ),
        name="fare-entry-edit",
    ),
    path(
        "fare/fare-entry/<str:code>/",
        views.FareEntryDetailView.as_view(
            template_name="fare_entry_detail.html",
            screen_no="F.1",
            screen_title="Fare Detail",
            module_label="Fare & Offers",
            tier="B",
            phase=13,
            purpose="Full detail of one configured fare, read-only.",
        ),
        name="fare-entry-detail",
    ),
    path(
        "fare/scheme-creation/",
        views.SchemeCreationView.as_view(
            template_name="scheme_creation.html",
            screen_no="F.2",
            screen_title="Scheme Creation",
            module_label="Fare & Offers",
            tier="B",
            phase=13,
            purpose="Configure promotional schemes: validity, value bands, promotion items and free-item rules.",
        ),
        name="fare-scheme-creation",
    ),
]
