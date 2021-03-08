"""foodgram URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views as flatpages_views

from foodgram import views
from recipe.views import index


handler404 = views.page_not_found
handler500 = views.server_error


urlpatterns = [
    path("admin/", admin.site.urls),
    path("about/", include("django.contrib.flatpages.urls")),
    path("auth/", include("users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
    path("recipes/", include("recipe.urls")),
    path("api/", include("api_v1.urls")),
    path("", index, name="index"),
]

urlpatterns += [
    path(
        "about-author/",
        flatpages_views.flatpage,
        {"url": "/about-author/"},
        name="about-author",
    ),
    path(
        "about-project/",
        flatpages_views.flatpage,
        {"url": "/about-project/"},
        name="about-project",
    ),
    path(
        "technologies/",
        flatpages_views.flatpage,
        {"url": "/technologies/"},
        name="technologies",
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )

    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
