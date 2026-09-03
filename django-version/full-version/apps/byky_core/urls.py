from django.urls import path

from apps.byky_core.views import BykyDashboardView

# Wireframe phase: no authentication. Every screen opens straight away so the
# prototype can be walked through without a login step (CLAUDE.md section 1).
urlpatterns = [
    path("", BykyDashboardView.as_view(), name="index"),
]
