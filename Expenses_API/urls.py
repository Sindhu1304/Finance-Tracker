from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("dashboard/", admin.site.urls),
    path("api/v1/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/", SpectacularSwaggerView.as_view(url_name="schema"), name="api"),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include("apps.expenses.urls")),
    path("api/v1/", include("apps.user_stats.urls")),
    path("api/v1/", include("apps.social_accounts.urls")),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
