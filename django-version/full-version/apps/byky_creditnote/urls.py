from django.urls import path

from . import views

urlpatterns = [
    path(
        "creditnote/credit-note-request/",
        views.CreditNoteRequestView.as_view(
            template_name="creditnote_credit_note_request.html",
            screen_title="Credit Note Request",
            module_label="Credit Note Management",
            tier="C",
            purpose="Review and approve or reject credit note requests submitted by branch staff through the mobile app.",
        ),
        name="creditnote-credit-note-request",
    ),
    path(
        "creditnote/credit-note/",
        views.CreditNoteView.as_view(
            template_name="creditnote_credit_note.html",
            screen_title="Credit Note",
            module_label="Credit Note Management",
            tier="B",
            purpose="Look up a closed rental invoice and raise a credit note against it.",
        ),
        name="creditnote-credit-note",
    ),
]
