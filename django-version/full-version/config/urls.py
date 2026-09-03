"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from web_project.views import SystemView

urlpatterns = [
    path("admin/", admin.site.urls),

    # auth urls
    path("", include("auth.urls")),

    # BYKY core (owns the "index" landing route)
    path("", include("apps.byky_core.urls")),

    # BYKY module urls
    path("", include("apps.byky_cms.urls")),
    path("", include("apps.byky_hrms.urls")),
    path("", include("apps.byky_ims.urls")),
    path("", include("apps.byky_rms.urls")),
    path("", include("apps.byky_tracking.urls")),
    path("", include("apps.byky_reports.urls")),
    path("", include("apps.byky_sfa.urls")),
    path("", include("apps.byky_rfid.urls")),
    path("", include("apps.byky_mobile.urls")),
    path("", include("apps.byky_notification.urls")),
    path("", include("apps.byky_wallet.urls")),
    path("", include("apps.byky_scheduler.urls")),
    path("", include("apps.byky_sysadmin.urls")),
    path("", include("apps.byky_api.urls")),
    path("", include("apps.byky_security.urls")),
    path("", include("apps.byky_integration.urls")),
]

handler404 = SystemView.as_view(template_name="pages_misc_error.html", status=404)
handler403 = SystemView.as_view(template_name="pages_misc_not_authorized.html", status=403)
handler400 = SystemView.as_view(template_name="pages_misc_error.html", status=400)
handler500 = SystemView.as_view(template_name="pages_misc_error.html", status=500)
