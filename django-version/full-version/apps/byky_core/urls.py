from django.urls import path

from apps.byky_core.views import BykyDashboardView, BykyScreenView

# Wireframe phase: no authentication. Every screen opens straight away so the
# prototype can be walked through without a login step (CLAUDE.md section 1).
urlpatterns = [
    path("", BykyDashboardView.as_view(), name="index"),
    path(
        "roles/",
        BykyScreenView.as_view(
            template_name="roles_placeholder.html",
            screen_title="Roles",
            module_label="Roles",
            purpose="Role-based access management across every BYKY module, consolidating "
            "each module's own Privileges screen into one place. Not an FSD module -- "
            "added to the sidebar ahead of being scoped.",
            layout="To be scoped.",
        ),
        name="roles-placeholder",
    ),
]
