from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("src.main.lists.urls")),
    path("auth/", include("src.main.accounts.urls")),
    path("api/", include("src.main.api.urls")),
    path("api-auth/", include("rest_framework.urls")),
    path("admin/", admin.site.urls),
]
